import unittest

from src.stegentity.hashutil import sha256_json
from tools.build_role_context_demo import build_authority, build_capsule, build_receipt


EXPECTED_ROLE_CONTEXT_CAPSULE_HASH = "sha256:ef94b71f15b0cbec9d304142ee3635f578a95c274f2da384a40b9d9b88bdd188"


class RoleContextDemoBuilderTests(unittest.TestCase):
    def test_builder_produces_expected_capsule_hash(self):
        capsule = build_capsule()
        self.assertEqual(sha256_json(capsule), EXPECTED_ROLE_CONTEXT_CAPSULE_HASH)

    def test_capsule_contains_complete_role_context_without_warnings(self):
        capsule = build_capsule()
        role_context = capsule["role_context"]
        self.assertEqual(role_context["actor_role"], "StegAgent")
        self.assertEqual(role_context["counterparty_role"], "StegEntity")
        self.assertEqual(role_context["role_transition"], "RT-004")
        self.assertTrue(role_context["completion_invariant_required"])

    def test_receipt_and_authority_bind_to_capsule_hash(self):
        capsule_hash = sha256_json(build_capsule())
        receipt = build_receipt(capsule_hash)
        authority = build_authority(capsule_hash)
        self.assertEqual(receipt["payload_hash"], capsule_hash)
        self.assertEqual(authority["capsule_hash"], capsule_hash)


if __name__ == "__main__":
    unittest.main()
