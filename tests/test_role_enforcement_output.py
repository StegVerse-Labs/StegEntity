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


class RoleEnforcementOutputTests(unittest.TestCase):
    def test_validate_emits_allow_role_enforcement_for_complete_context(self):
        capsule, receipt, authority = bound_objects(build_capsule())

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.validate(capsule, receipt, authority)

        self.assertEqual(result["role_enforcement"]["decision"], "ALLOW")
        self.assertEqual(result["role_enforcement"]["stage"], "warning-only")
        self.assertEqual(result["role_enforcement"]["warnings"], [])
        self.assertEqual(result["role_enforcement"]["blocks"], [])

    def test_validate_emits_warn_role_enforcement_for_missing_context(self):
        capsule_data = build_capsule()
        capsule_data.pop("role_context")
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.validate(capsule, receipt, authority)

        self.assertEqual(result["role_enforcement"]["decision"], "WARN")
        self.assertEqual(result["role_enforcement"]["stage"], "warning-only")
        self.assertIn("role_context_missing", result["role_enforcement"]["warnings"])
        self.assertEqual(result["role_enforcement"]["blocks"], [])

    def test_dry_run_emits_warn_without_blocks_for_unknown_transition(self):
        capsule_data = build_capsule()
        capsule_data["role_context"]["role_transition"] = "RT-999"
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.dry_run(capsule, receipt, authority)

        self.assertEqual(result["role_enforcement"]["decision"], "WARN")
        self.assertIn("role_context_unknown_role_transition:RT-999", result["role_enforcement"]["warnings"])
        self.assertEqual(result["role_enforcement"]["blocks"], [])

    def test_apply_emits_allow_role_enforcement_for_complete_context(self):
        capsule, receipt, authority = bound_objects(build_capsule())

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.apply(capsule, receipt, authority)

        self.assertEqual(result["role_enforcement"]["decision"], "ALLOW")
        self.assertEqual(result["role_enforcement"]["stage"], "required-role-context-for-apply")
        self.assertEqual(result["role_enforcement"]["blocks"], [])


if __name__ == "__main__":
    unittest.main()
