from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .errors import ValidationError
from .hashutil import sha256_json

@dataclass(frozen=True)
class MaintenanceOperation:
    op_id: str
    operation: str
    destination: str
    content_b64: Optional[str]
    expected_sha256: Optional[str]
    required_scopes: List[str]
    description: str
    allow_create: bool
    allow_replace: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MaintenanceOperation":
        required = ["op_id", "operation", "destination", "required_scopes"]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValidationError(f"operation_missing_fields:{missing}")
        operation = str(data["operation"])
        if operation not in ("create", "replace", "create_or_replace", "append"):
            raise ValidationError(f"unsupported_operation:{operation}")
        scopes = data["required_scopes"]
        if not isinstance(scopes, list) or not all(isinstance(x, str) for x in scopes):
            raise ValidationError("operation_required_scopes_must_be_string_list")
        return cls(
            op_id=str(data["op_id"]),
            operation=operation,
            destination=str(data["destination"]),
            content_b64=data.get("content_b64"),
            expected_sha256=data.get("expected_sha256"),
            required_scopes=list(scopes),
            description=str(data.get("description", "")),
            allow_create=bool(data.get("allow_create", operation in ("create", "create_or_replace", "append"))),
            allow_replace=bool(data.get("allow_replace", operation in ("replace", "create_or_replace", "append"))),
        )

@dataclass(frozen=True)
class MaintenanceCapsule:
    raw: Dict[str, Any]
    capsule_id: str
    created_at: str
    adapter: str
    target: str
    admissibility_decision: str
    transition_id: str
    transition_name: str
    operations: List[MaintenanceOperation]
    dependencies: List[str]
    consequences: List[str]
    rollback_plan: List[str]
    verification: Dict[str, Any]
    role_context: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MaintenanceCapsule":
        required = ["schema", "capsule_id", "created_at", "target", "transition", "admissibility", "operations", "dependencies", "consequences", "rollback_plan", "verification"]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValidationError(f"capsule_missing_fields:{missing}")
        target = data["target"]
        if not isinstance(target, dict) or "adapter" not in target or "target_id" not in target:
            raise ValidationError("capsule_target_missing_adapter_or_target_id")
        transition = data["transition"]
        if not isinstance(transition, dict) or "transition_id" not in transition or "transition_name" not in transition:
            raise ValidationError("capsule_transition_missing_fields")
        admissibility = data["admissibility"]
        if not isinstance(admissibility, dict) or "decision" not in admissibility:
            raise ValidationError("capsule_admissibility_missing_decision")
        if admissibility["decision"] != "ALLOW":
            raise ValidationError(f"capsule_not_allowed:{admissibility['decision']}")
        operations_data = data["operations"]
        if not isinstance(operations_data, list) or not operations_data:
            raise ValidationError("capsule_operations_must_be_nonempty_list")
        operations = [MaintenanceOperation.from_dict(item) for item in operations_data]
        for field in ("dependencies", "consequences", "rollback_plan"):
            if not isinstance(data[field], list) or not all(isinstance(x, str) for x in data[field]):
                raise ValidationError(f"capsule_{field}_must_be_string_list")
        role_context = data.get("role_context", {})
        if not isinstance(role_context, dict):
            raise ValidationError("capsule_role_context_must_be_object")
        return cls(
            raw=dict(data),
            capsule_id=str(data["capsule_id"]),
            created_at=str(data["created_at"]),
            adapter=str(target["adapter"]),
            target=str(target["target_id"]),
            admissibility_decision=str(admissibility["decision"]),
            transition_id=str(transition["transition_id"]),
            transition_name=str(transition["transition_name"]),
            operations=operations,
            dependencies=list(data["dependencies"]),
            consequences=list(data["consequences"]),
            rollback_plan=list(data["rollback_plan"]),
            verification=dict(data["verification"]),
            role_context=dict(role_context),
        )

    def hash(self) -> str:
        return sha256_json(self.raw)

    def required_scopes(self) -> List[str]:
        scopes = []
        for op in self.operations:
            for scope in op.required_scopes:
                if scope not in scopes:
                    scopes.append(scope)
        return scopes
