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


class ApplyRoleTransitionEnforcementTests(unittest.TestCase):
    def test_validate_allows_unknown_role_transition_as_warning_only(self):
        capsule_data = build_capsule()
        capsule_data["role_context"]["role_transition"] = "RT-999"
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.validate(capsule, receipt, authority)

        self.assertEqual(result["status"], "ok")
        self.assertIn("role_context_unknown_role_transition:RT-999", result["role_context_warnings"])

    def test_dry_run_allows_unknown_role_transition_as_warning_only(self):
        capsule_data = build_capsule()
        capsule_data["role_context"]["role_transition"] = "RT-999"
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.dry_run(capsule, receipt, authority)

        self.assertEqual(result["status"], "ok")
        self.assertIn("role_context_unknown_role_transition:RT-999", result["role_context_warnings"])

    def test_apply_blocks_unknown_role_transition(self):
        capsule_data = build_capsule()
        capsule_data["role_context"]["role_transition"] = "RT-999"
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            with self.assertRaises(ValidationError):
                runtime.apply(capsule, receipt, authority)

    def test_apply_allows_known_role_transition(self):
        capsule, receipt, authority = bound_objects(build_capsule())

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.apply(capsule, receipt, authority)

        self.assertEqual(result["status"], "ok")
        self.assertNotIn("role_context_warnings", result)


if __name__ == "__main__":
    unittest.main()
