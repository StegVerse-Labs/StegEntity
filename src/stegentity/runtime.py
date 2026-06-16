import json
from pathlib import Path
from typing import Any, Dict, List

from .adapters import LocalFSAdapter
from .authority import AuthorityToken
from .capsule import MaintenanceCapsule
from .errors import ValidationError
from .receipt import VerifiedReceipt
from .receipts import make_blocked_apply_receipt, make_receipt, write_json
from .role_context import apply_role_context_blocks, role_context_warnings, role_enforcement_result
from .timeutil import now_text

class StegEntityRuntime:
    def __init__(self, root: Path, receipts_dir: Path | None = None, reports_dir: Path | None = None):
        self.root = root.resolve()
        self.receipts_dir = (receipts_dir or (self.root / "stegentity_receipts")).resolve()
        self.reports_dir = (reports_dir or (self.root / "stegentity_reports")).resolve()

    def _adapter(self, capsule: MaintenanceCapsule):
        if capsule.adapter == "local_fs":
            return LocalFSAdapter(self.root)
        raise ValidationError(f"unsupported_adapter:{capsule.adapter}")

    def _with_role_context(self, capsule: MaintenanceCapsule, data: Dict[str, Any], mode: str) -> Dict[str, Any]:
        if capsule.role_context:
            data["role_context"] = dict(capsule.role_context)
        warnings = role_context_warnings(capsule.role_context)
        if warnings:
            data["role_context_warnings"] = warnings
        data["role_enforcement"] = role_enforcement_result(capsule.role_context, mode)
        return data

    def _completion_invariant_blocks(self, capsule: MaintenanceCapsule) -> List[str]:
        if not capsule.role_context.get("completion_invariant_required"):
            return []
        blocks: List[str] = []
        for op in capsule.operations:
            if not op.expected_sha256:
                blocks.append(f"completion_invariant_missing_expected_sha256:{op.op_id}")
        return blocks

    def _completion_invariant_result(self, capsule: MaintenanceCapsule, result: Dict[str, Any]) -> Dict[str, Any]:
        required = bool(capsule.role_context.get("completion_invariant_required"))
        operations = result.get("operations", [])
        checks = []
        for item in operations:
            expected = item.get("expected_sha256")
            written = item.get("written_sha256")
            checks.append({
                "op_id": item.get("op_id"),
                "destination": item.get("destination"),
                "expected_sha256": expected,
                "written_sha256": written,
                "matched": bool(expected and written and expected == written),
                "verified": bool(item.get("verified")),
            })
        satisfied = all(check["matched"] and check["verified"] for check in checks) if required else True
        return {
            "required": required,
            "basis": "expected_sha256",
            "satisfied": satisfied,
            "checks": checks,
        }

    def _enforce_apply_role_context(self, capsule: MaintenanceCapsule, capsule_hash: str, receipt: VerifiedReceipt, token: AuthorityToken) -> None:
        blocks = apply_role_context_blocks(capsule.role_context)
        blocks.extend(self._completion_invariant_blocks(capsule))
        if blocks:
            role_enforcement = role_enforcement_result(capsule.role_context, "apply")
            refusal = make_blocked_apply_receipt(
                capsule_hash=capsule_hash,
                capsule_id=capsule.capsule_id,
                actor_receipt_id=receipt.receipt_id,
                authority_token_id=token.token_id,
                adapter=capsule.adapter,
                target=capsule.target,
                reason="apply_precondition_block",
                blocks=blocks,
                role_context=capsule.role_context,
                role_enforcement=role_enforcement,
            )
            refusal_path = self.receipts_dir / f"{capsule.capsule_id}.blocked_apply_receipt.json"
            write_json(refusal_path, refusal)
            outcome = self._with_role_context(capsule, {
                "status": "blocked",
                "mode": "apply",
                "created_at": now_text(),
                "capsule_id": capsule.capsule_id,
                "capsule_hash": capsule_hash,
                "reason": "apply_precondition_block",
                "blocks": blocks,
                "mutation_attempted": False,
                "execution_receipt_emitted": False,
                "blocked_apply_receipt_path": str(refusal_path),
                "blocked_apply_receipt_hash": refusal["receipt_hash"],
            }, "apply")
            self._write_outcome(capsule.capsule_id, "apply.blocked", outcome)
            raise ValidationError(f"apply_precondition_block:{blocks}")

    def validate_authority(self, capsule: MaintenanceCapsule, receipt: VerifiedReceipt, token: AuthorityToken) -> str:
        capsule_hash = capsule.hash()
        required_scopes = capsule.required_scopes()
        receipt.validate_for_capsule(capsule_hash, required_scopes)
        token.validate_for_capsule(capsule_hash=capsule_hash, adapter=capsule.adapter, target=capsule.target, required_scopes=required_scopes)
        return capsule_hash

    def validate(self, capsule: MaintenanceCapsule, receipt: VerifiedReceipt, token: AuthorityToken) -> Dict[str, Any]:
        capsule_hash = self.validate_authority(capsule, receipt, token)
        return self._with_role_context(capsule, {
            "status": "ok",
            "capsule_id": capsule.capsule_id,
            "capsule_hash": capsule_hash,
            "adapter": capsule.adapter,
            "target": capsule.target,
            "operation_count": len(capsule.operations),
            "required_scopes": capsule.required_scopes(),
        }, "validate")

    def dry_run(self, capsule: MaintenanceCapsule, receipt: VerifiedReceipt, token: AuthorityToken) -> Dict[str, Any]:
        capsule_hash = self.validate_authority(capsule, receipt, token)
        adapter = self._adapter(capsule)
        result = adapter.dry_run(capsule.operations)
        outcome = self._with_role_context(capsule, {"status": "ok", "mode": "dry_run", "created_at": now_text(), "capsule_id": capsule.capsule_id, "capsule_hash": capsule_hash, "result": result}, "dry_run")
        self._write_outcome(capsule.capsule_id, "dry_run", outcome)
        return outcome

    def apply(self, capsule: MaintenanceCapsule, receipt: VerifiedReceipt, token: AuthorityToken) -> Dict[str, Any]:
        capsule_hash = self.validate_authority(capsule, receipt, token)
        self._enforce_apply_role_context(capsule, capsule_hash, receipt, token)
        adapter = self._adapter(capsule)
        result = adapter.apply(capsule.operations, capsule.capsule_id)
        role_enforcement = role_enforcement_result(capsule.role_context, "apply")
        completion_invariant = self._completion_invariant_result(capsule, result)
        receipt_body = make_receipt(
            receipt_type="execution",
            capsule_hash=capsule_hash,
            capsule_id=capsule.capsule_id,
            actor_receipt_id=receipt.receipt_id,
            authority_token_id=token.token_id,
            adapter=capsule.adapter,
            target=capsule.target,
            result=result,
            role_context=capsule.role_context,
            role_enforcement=role_enforcement,
            completion_invariant=completion_invariant,
        )
        receipt_path = self.receipts_dir / f"{capsule.capsule_id}.execution_receipt.json"
        write_json(receipt_path, receipt_body)
        outcome = self._with_role_context(capsule, {
            "status": "ok",
            "mode": "apply",
            "created_at": now_text(),
            "capsule_id": capsule.capsule_id,
            "capsule_hash": capsule_hash,
            "receipt_path": str(receipt_path),
            "receipt_hash": receipt_body["receipt_hash"],
            "completion_invariant": completion_invariant,
            "result": result,
        }, "apply")
        self._write_outcome(capsule.capsule_id, "apply", outcome)
        return outcome

    def _write_outcome(self, capsule_id: str, mode: str, outcome: Dict[str, Any]) -> None:
        path = self.reports_dir / f"{capsule_id}.{mode}.outcome.json"
        write_json(path, outcome)

def load_json_file(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def load_capsule(path: Path) -> MaintenanceCapsule:
    return MaintenanceCapsule.from_dict(load_json_file(path))

def load_receipt(path: Path) -> VerifiedReceipt:
    return VerifiedReceipt.from_dict(load_json_file(path))

def load_authority(path: Path) -> AuthorityToken:
    return AuthorityToken.from_dict(load_json_file(path))
