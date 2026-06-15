import json
from pathlib import Path
from typing import Any, Dict

from .adapters import LocalFSAdapter
from .authority import AuthorityToken
from .capsule import MaintenanceCapsule
from .errors import ValidationError
from .receipt import VerifiedReceipt
from .receipts import make_receipt, write_json
from .role_context import apply_role_context_blocks, role_context_warnings
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

    def _with_role_context(self, capsule: MaintenanceCapsule, data: Dict[str, Any]) -> Dict[str, Any]:
        if capsule.role_context:
            data["role_context"] = dict(capsule.role_context)
        warnings = role_context_warnings(capsule.role_context)
        if warnings:
            data["role_context_warnings"] = warnings
        return data

    def _enforce_apply_role_context(self, capsule: MaintenanceCapsule) -> None:
        blocks = apply_role_context_blocks(capsule.role_context)
        if blocks:
            raise ValidationError(f"role_context_apply_block:{blocks}")

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
        })

    def dry_run(self, capsule: MaintenanceCapsule, receipt: VerifiedReceipt, token: AuthorityToken) -> Dict[str, Any]:
        capsule_hash = self.validate_authority(capsule, receipt, token)
        adapter = self._adapter(capsule)
        result = adapter.dry_run(capsule.operations)
        outcome = self._with_role_context(capsule, {"status": "ok", "mode": "dry_run", "created_at": now_text(), "capsule_id": capsule.capsule_id, "capsule_hash": capsule_hash, "result": result})
        self._write_outcome(capsule.capsule_id, "dry_run", outcome)
        return outcome

    def apply(self, capsule: MaintenanceCapsule, receipt: VerifiedReceipt, token: AuthorityToken) -> Dict[str, Any]:
        capsule_hash = self.validate_authority(capsule, receipt, token)
        self._enforce_apply_role_context(capsule)
        adapter = self._adapter(capsule)
        result = adapter.apply(capsule.operations, capsule.capsule_id)
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
            "result": result,
        })
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
