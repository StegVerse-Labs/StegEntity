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


class CompletionInvariantExpectedHashTests(unittest.TestCase):
    def test_apply_blocks_when_completion_invariant_requires_expected_hash(self):
        capsule_data = build_capsule()
        capsule_data["operations"][0].pop("expected_sha256", None)
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            with self.assertRaises(ValidationError):
                runtime.apply(capsule, receipt, authority)

    def test_apply_allows_when_completion_invariant_expected_hash_present(self):
        capsule, receipt, authority = bound_objects(build_capsule())

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.apply(capsule, receipt, authority)

        self.assertEqual(result["status"], "ok")
        operation = result["result"]["operations"][0]
        self.assertEqual(operation["expected_sha256"], operation["written_sha256"])
        self.assertTrue(operation["verified"])


if __name__ == "__main__":
    unittest.main()
