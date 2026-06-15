import tempfile
import unittest
from pathlib import Path

from src.stegentity.authority import AuthorityToken
from src.stegentity.capsule import MaintenanceCapsule
from src.stegentity.receipt import VerifiedReceipt
from src.stegentity.runtime import StegEntityRuntime
from tools.build_role_context_demo import build_authority, build_capsule, build_receipt


class RoleContextRuntimeValidateTests(unittest.TestCase):
    def test_role_context_demo_validates_without_role_context_warnings(self):
        capsule = MaintenanceCapsule.from_dict(build_capsule())
        capsule_hash = capsule.hash()
        receipt = VerifiedReceipt.from_dict(build_receipt(capsule_hash))
        authority = AuthorityToken.from_dict(build_authority(capsule_hash))

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.validate(capsule, receipt, authority)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["capsule_hash"], capsule_hash)
        self.assertEqual(result["role_context"]["actor_role"], "StegAgent")
        self.assertNotIn("role_context_warnings", result)


if __name__ == "__main__":
    unittest.main()
