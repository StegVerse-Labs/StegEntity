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


class RefusalReceiptArtifactTests(unittest.TestCase):
    def test_refused_apply_has_non_execution_receipt(self):
        capsule_data = build_capsule()
        capsule_data["role_context"].pop("symmetry_basis")
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            runtime = StegEntityRuntime(root)
            with self.assertRaises(ValidationError):
                runtime.apply(capsule, receipt, authority)

            refusal_path = root / "stegentity_receipts" / f"{capsule.capsule_id}.blocked_apply_receipt.json"
            execution_path = root / "stegentity_receipts" / f"{capsule.capsule_id}.execution_receipt.json"
            outcome_path = root / "stegentity_reports" / f"{capsule.capsule_id}.apply.blocked.outcome.json"

            self.assertTrue(refusal_path.exists())
            self.assertFalse(execution_path.exists())
            self.assertTrue(outcome_path.exists())
            refusal = json.loads(refusal_path.read_text(encoding="utf-8"))
            outcome = json.loads(outcome_path.read_text(encoding="utf-8"))

        self.assertEqual(refusal["receipt_type"], "blocked_apply")
        self.assertEqual(refusal["schema"]["name"], "stegverse.stegentity.blocked_apply_receipt")
        self.assertEqual(outcome["blocked_apply_receipt_hash"], refusal["receipt_hash"])


if __name__ == "__main__":
    unittest.main()
