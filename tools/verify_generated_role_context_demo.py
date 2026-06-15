import json
from pathlib import Path

from src.stegentity.hashutil import sha256_json
from tools.build_role_context_demo import build_authority, build_capsule, build_receipt
from tools.check_role_context_demo import EXPECTED_ROLE_CONTEXT_CAPSULE_HASH

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    capsule_path = EXAMPLES / "role_context_file_replacement_capsule.json"
    receipt_path = EXAMPLES / "role_context_verified_receipt.json"
    authority_path = EXAMPLES / "role_context_authority_token.json"

    missing = [str(path) for path in (capsule_path, receipt_path, authority_path) if not path.exists()]
    if missing:
        print(json.dumps({"status": "failed", "error": "missing_generated_files", "missing": missing}, indent=2))
        return 1

    expected_capsule = build_capsule()
    actual_capsule = read_json(capsule_path)
    if actual_capsule != expected_capsule:
        print(json.dumps({"status": "failed", "error": "generated_capsule_mismatch"}, indent=2))
        return 1

    capsule_hash = sha256_json(actual_capsule)
    if capsule_hash != EXPECTED_ROLE_CONTEXT_CAPSULE_HASH:
        print(json.dumps({
            "status": "failed",
            "error": "generated_capsule_hash_mismatch",
            "expected": EXPECTED_ROLE_CONTEXT_CAPSULE_HASH,
            "actual": capsule_hash,
        }, indent=2))
        return 1

    expected_receipt = build_receipt(capsule_hash)
    actual_receipt = read_json(receipt_path)
    if actual_receipt != expected_receipt:
        print(json.dumps({"status": "failed", "error": "generated_receipt_mismatch"}, indent=2))
        return 1

    expected_authority = build_authority(capsule_hash)
    actual_authority = read_json(authority_path)
    if actual_authority != expected_authority:
        print(json.dumps({"status": "failed", "error": "generated_authority_mismatch"}, indent=2))
        return 1

    print(json.dumps({
        "status": "ok",
        "capsule_path": str(capsule_path),
        "receipt_path": str(receipt_path),
        "authority_path": str(authority_path),
        "capsule_hash": capsule_hash,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
