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


class CompletionInvariantArtifactTests(unittest.TestCase):
    def test_apply_outcome_and_receipt_include_completion_invariant(self):
        capsule, receipt, authority = bound_objects(build_capsule())

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            runtime = StegEntityRuntime(root)
            result = runtime.apply(capsule, receipt, authority)
            receipt_body = json.loads(Path(result["receipt_path"]).read_text(encoding="utf-8"))

        self.assertIn("completion_invariant", result)
        self.assertIn("completion_invariant", receipt_body)
        self.assertTrue(result["completion_invariant"]["required"])
        self.assertTrue(result["completion_invariant"]["satisfied"])
        self.assertEqual(result["completion_invariant"], receipt_body["completion_invariant"])
        check = result["completion_invariant"]["checks"][0]
        self.assertEqual(check["expected_sha256"], check["written_sha256"])
        self.assertTrue(check["matched"])
        self.assertTrue(check["verified"])


if __name__ == "__main__":
    unittest.main()
