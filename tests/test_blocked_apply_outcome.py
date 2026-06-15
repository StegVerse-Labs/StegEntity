import json
import tempfile
import unittest
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
        MaintenanceCapsule.from_dict(capsule_data),
        VerifiedReceipt.from_dict(build_receipt(capsule_hash)),
        AuthorityToken.from_dict(build_authority(capsule_hash)),
    )


class BlockedApplyOutcomeTests(unittest.TestCase):
    def test_blocked_apply_writes_outcome_without_mutation_or_receipt(self):
        capsule_data = build_capsule()
        capsule_data["role_context"].pop("symmetry_basis")
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            runtime = StegEntityRuntime(root)

            with self.assertRaises(ValidationError):
                runtime.apply(capsule, receipt, authority)

            blocked_path = root / "stegentity_reports" / f"{capsule.capsule_id}.apply.blocked.outcome.json"
            receipt_path = root / "stegentity_receipts" / f"{capsule.capsule_id}.execution_receipt.json"
            target_path = root / "role_context_hello.txt"

            self.assertTrue(blocked_path.exists())
            self.assertFalse(receipt_path.exists())
            self.assertFalse(target_path.exists())

            blocked = json.loads(blocked_path.read_text(encoding="utf-8"))

        self.assertEqual(blocked["status"], "blocked")
        self.assertEqual(blocked["mode"], "apply")
        self.assertEqual(blocked["reason"], "role_context_apply_block")
        self.assertFalse(blocked["mutation_attempted"])
        self.assertFalse(blocked["execution_receipt_emitted"])
        self.assertEqual(blocked["role_enforcement"]["decision"], "BLOCK")
        self.assertIn("role_context_missing_recommended_field:symmetry_basis", blocked["role_enforcement"]["blocks"])


if __name__ == "__main__":
    unittest.main()
