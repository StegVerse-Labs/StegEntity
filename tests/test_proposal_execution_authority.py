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


class ProposalExecutionAuthorityTests(unittest.TestCase):
    def test_apply_blocks_rt002_without_explicit_authority_evidence(self):
        capsule_data = build_capsule()
        capsule_data["role_context"]["role_transition"] = "RT-002"
        capsule_data["role_context"]["symmetry_basis"] = "proposal_only"
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            with self.assertRaises(ValidationError):
                runtime.apply(capsule, receipt, authority)

    def test_apply_allows_rt002_with_explicit_authority_evidence(self):
        capsule_data = build_capsule()
        capsule_data["role_context"]["role_transition"] = "RT-002"
        capsule_data["role_context"]["authority_evidence"] = "receipt+tvc+capsule"
        capsule, receipt, authority = bound_objects(capsule_data)

        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = StegEntityRuntime(Path(temp_dir))
            result = runtime.apply(capsule, receipt, authority)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["role_enforcement"]["decision"], "ALLOW")


if __name__ == "__main__":
    unittest.main()
