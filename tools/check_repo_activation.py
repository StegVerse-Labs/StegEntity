import json
import tempfile
from pathlib import Path

from src.stegentity.authority import AuthorityToken
from src.stegentity.capsule import MaintenanceCapsule
from src.stegentity.errors import ValidationError
from src.stegentity.hashutil import sha256_json
from src.stegentity.receipt import VerifiedReceipt
from src.stegentity.runtime import StegEntityRuntime
from tools.build_role_context_demo import build_authority, build_capsule, build_receipt


def bound_objects(capsule_data):
    capsule_hash = sha256_json(capsule_data)
    return (
        capsule_hash,
        MaintenanceCapsule.from_dict(capsule_data),
        VerifiedReceipt.from_dict(build_receipt(capsule_hash)),
        AuthorityToken.from_dict(build_authority(capsule_hash)),
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_completion_invariant(data: dict, label: str) -> dict:
    invariant = data.get("completion_invariant")
    require(isinstance(invariant, dict), f"{label} missing completion invariant")
    require(invariant.get("required") is True, f"{label} completion invariant not required")
    require(invariant.get("basis") == "expected_sha256", f"{label} completion invariant basis mismatch")
    require(invariant.get("satisfied") is True, f"{label} completion invariant not satisfied")
    checks = invariant.get("checks")
    require(isinstance(checks, list) and checks, f"{label} completion invariant checks missing")
    for check in checks:
        require(check.get("matched") is True, f"{label} completion invariant hash mismatch")
        require(check.get("verified") is True, f"{label} completion invariant not verified")
        require(check.get("expected_sha256") == check.get("written_sha256"), f"{label} expected and written hash differ")
    return invariant


def check_success_path() -> dict:
    capsule_hash, capsule, receipt, authority = bound_objects(build_capsule())
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        runtime = StegEntityRuntime(root)
        validation = runtime.validate(capsule, receipt, authority)
        dry_run = runtime.dry_run(capsule, receipt, authority)
        applied = runtime.apply(capsule, receipt, authority)

        target_path = root / "role_context_hello.txt"
        execution_receipt_path = Path(applied["receipt_path"])
        apply_report_path = root / "stegentity_reports" / f"{capsule.capsule_id}.apply.outcome.json"

        require(validation["status"] == "ok", "validation failed")
        require(dry_run["status"] == "ok", "dry run failed")
        require(applied["status"] == "ok", "apply failed")
        require(target_path.exists(), "target file missing after apply")
        require(execution_receipt_path.exists(), "execution receipt missing")
        require(apply_report_path.exists(), "apply outcome report missing")

        receipt_body = json.loads(execution_receipt_path.read_text(encoding="utf-8"))
        apply_report = json.loads(apply_report_path.read_text(encoding="utf-8"))
        require(receipt_body["receipt_type"] == "execution", "wrong success receipt type")
        require(receipt_body["role_enforcement"]["decision"] == "ALLOW", "success role enforcement not ALLOW")
        outcome_invariant = require_completion_invariant(applied, "apply outcome")
        receipt_invariant = require_completion_invariant(receipt_body, "execution receipt")
        report_invariant = require_completion_invariant(apply_report, "apply report")
        require(outcome_invariant == receipt_invariant == report_invariant, "completion invariant differs across artifacts")

        return {
            "capsule_hash": capsule_hash,
            "target_written": target_path.exists(),
            "execution_receipt": execution_receipt_path.name,
            "apply_report": apply_report_path.name,
            "completion_invariant_satisfied": outcome_invariant["satisfied"],
        }


def check_refusal_path() -> dict:
    capsule_data = build_capsule()
    capsule_data["role_context"].pop("symmetry_basis")
    capsule_hash, capsule, receipt, authority = bound_objects(capsule_data)

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        runtime = StegEntityRuntime(root)
        try:
            runtime.apply(capsule, receipt, authority)
        except ValidationError:
            pass
        else:
            raise AssertionError("refused apply unexpectedly succeeded")

        target_path = root / "role_context_hello.txt"
        refusal_path = root / "stegentity_receipts" / f"{capsule.capsule_id}.blocked_apply_receipt.json"
        execution_path = root / "stegentity_receipts" / f"{capsule.capsule_id}.execution_receipt.json"
        blocked_report_path = root / "stegentity_reports" / f"{capsule.capsule_id}.apply.blocked.outcome.json"

        require(not target_path.exists(), "target file was written during refusal")
        require(refusal_path.exists(), "refusal receipt missing")
        require(not execution_path.exists(), "execution receipt emitted during refusal")
        require(blocked_report_path.exists(), "blocked outcome report missing")

        refusal = json.loads(refusal_path.read_text(encoding="utf-8"))
        blocked = json.loads(blocked_report_path.read_text(encoding="utf-8"))
        require(refusal["receipt_type"] == "blocked_apply", "wrong refusal receipt type")
        require(blocked["blocked_apply_receipt_hash"] == refusal["receipt_hash"], "blocked outcome not bound to refusal receipt")

        return {
            "capsule_hash": capsule_hash,
            "target_written": target_path.exists(),
            "refusal_receipt": refusal_path.name,
            "blocked_report": blocked_report_path.name,
        }


def main() -> int:
    result = {
        "status": "ok",
        "activation_check": "local_stegentity_runtime",
        "success_path": check_success_path(),
        "refusal_path": check_refusal_path(),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
