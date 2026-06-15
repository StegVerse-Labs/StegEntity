import json
import tempfile
import unittest
from pathlib import Path

from src.stegentity.authority import AuthorityToken
from src.stegentity.capsule import MaintenanceCapsule
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


class ExecutionReceiptRoleEnforcementTests(unittest.TestCase):
    def test_apply_execution_receipt_includes_role_enforcement(self):
        capsule, receipt, authority = bound_objects(build_capsule())

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.apply(capsule, receipt, authority)
            receipt_path = Path(result["receipt_path"])
            receipt_body = json.loads(receipt_path.read_text(encoding="utf-8"))

        self.assertIn("role_enforcement", receipt_body)
        self.assertEqual(receipt_body["role_enforcement"]["decision"], "ALLOW")
        self.assertEqual(receipt_body["role_enforcement"]["stage"], "required-role-context-for-apply")
        self.assertEqual(receipt_body["role_enforcement"]["mode"], "apply")
        self.assertEqual(receipt_body["role_enforcement"]["blocks"], [])
        self.assertIn("receipt_hash", receipt_body)


if __name__ == "__main__":
    unittest.main()
