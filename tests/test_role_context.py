import unittest

from src.stegentity.capsule import MaintenanceCapsule
from src.stegentity.errors import ValidationError


def base_capsule():
    return {
        "schema": {"name": "stegverse.maintenance_capsule", "version": "0.1.0"},
        "capsule_id": "test-role-context-0001",
        "created_at": "2026-05-18T13:21:29Z",
        "target": {"adapter": "local_fs", "target_id": "demo_target"},
        "transition": {"transition_id": "T-ROLE", "transition_name": "Role Context Test"},
        "admissibility": {"decision": "ALLOW"},
        "dependencies": [],
        "consequences": [],
        "rollback_plan": [],
        "verification": {"required": True, "method": "sha256_after_write"},
        "operations": [
            {
                "op_id": "op-role-context",
                "operation": "create_or_replace",
                "destination": "role-context.txt",
                "required_scopes": ["local_fs:write"],
                "description": "Write role context test file.",
                "allow_create": True,
                "allow_replace": True
            }
        ]
    }


class RoleContextTests(unittest.TestCase):
    def test_role_context_defaults_to_empty_object(self):
        capsule = MaintenanceCapsule.from_dict(base_capsule())
        self.assertEqual(capsule.role_context, {})

    def test_role_context_is_preserved_when_present(self):
        data = base_capsule()
        data["role_context"] = {
            "actor_role": "StegAgent",
            "counterparty_role": "StegEntity",
            "role_transition": "RT-002"
        }
        capsule = MaintenanceCapsule.from_dict(data)
        self.assertEqual(capsule.role_context["actor_role"], "StegAgent")
        self.assertEqual(capsule.role_context["counterparty_role"], "StegEntity")

    def test_role_context_must_be_object_when_present(self):
        data = base_capsule()
        data["role_context"] = "StegAgent"
        with self.assertRaises(ValidationError):
            MaintenanceCapsule.from_dict(data)


if __name__ == "__main__":
    unittest.main()
