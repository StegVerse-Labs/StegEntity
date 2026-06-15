import json
import tempfile
from pathlib import Path

from src.stegentity.authority import AuthorityToken
from src.stegentity.capsule import MaintenanceCapsule
from src.stegentity.receipt import VerifiedReceipt
from src.stegentity.runtime import StegEntityRuntime
from tools.build_role_context_demo import build_authority, build_capsule, build_receipt

EXPECTED_ROLE_CONTEXT_CAPSULE_HASH = "sha256:ef94b71f15b0cbec9d304142ee3635f578a95c274f2da384a40b9d9b88bdd188"


def main() -> int:
    capsule = MaintenanceCapsule.from_dict(build_capsule())
    capsule_hash = capsule.hash()
    if capsule_hash != EXPECTED_ROLE_CONTEXT_CAPSULE_HASH:
        print(json.dumps({
            "status": "failed",
            "error": "capsule_hash_mismatch",
            "expected": EXPECTED_ROLE_CONTEXT_CAPSULE_HASH,
            "actual": capsule_hash,
        }, indent=2))
        return 1

    receipt = VerifiedReceipt.from_dict(build_receipt(capsule_hash))
    authority = AuthorityToken.from_dict(build_authority(capsule_hash))

    with tempfile.TemporaryDirectory() as temp_dir:
        runtime = StegEntityRuntime(Path(temp_dir))
        result = runtime.validate(capsule, receipt, authority)

    if result.get("role_context_warnings"):
        print(json.dumps({
            "status": "failed",
            "error": "role_context_warnings_present",
            "warnings": result["role_context_warnings"],
        }, indent=2))
        return 1

    print(json.dumps({
        "status": "ok",
        "capsule_id": capsule.capsule_id,
        "capsule_hash": capsule_hash,
        "role_context": result.get("role_context", {}),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
