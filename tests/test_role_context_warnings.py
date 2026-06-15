import unittest

from src.stegentity.role_context import role_context_warnings


class RoleContextWarningTests(unittest.TestCase):
    def test_missing_role_context_warns(self):
        self.assertEqual(role_context_warnings({}), ["role_context_missing"])

    def test_complete_role_context_has_no_warnings(self):
        warnings = role_context_warnings({
            "actor_role": "StegAgent",
            "counterparty_role": "StegEntity",
            "role_transition": "RT-002",
            "role_constraint": "proposal_not_execution",
            "symmetry_basis": "receipt+tvc+capsule",
            "completion_invariant_required": True,
        })
        self.assertEqual(warnings, [])

    def test_missing_recommended_fields_warn(self):
        warnings = role_context_warnings({"actor_role": "StegAgent"})
        self.assertIn("role_context_missing_recommended_field:counterparty_role", warnings)
        self.assertIn("role_context_missing_recommended_field:role_transition", warnings)

    def test_unknown_role_transition_warns(self):
        warnings = role_context_warnings({
            "actor_role": "StegAgent",
            "counterparty_role": "StegEntity",
            "role_transition": "RT-999",
            "role_constraint": "proposal_not_execution",
            "symmetry_basis": "receipt+tvc+capsule",
            "completion_invariant_required": True,
        })
        self.assertIn("role_context_unknown_role_transition:RT-999", warnings)

    def test_completion_invariant_required_must_be_bool(self):
        warnings = role_context_warnings({
            "actor_role": "StegAgent",
            "counterparty_role": "StegEntity",
            "role_transition": "RT-002",
            "role_constraint": "proposal_not_execution",
            "symmetry_basis": "receipt+tvc+capsule",
            "completion_invariant_required": "yes",
        })
        self.assertIn("role_context_completion_invariant_required_must_be_bool", warnings)


if __name__ == "__main__":
    unittest.main()
