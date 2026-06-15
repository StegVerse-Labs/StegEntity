from typing import Any, Dict, List

RECOMMENDED_ROLE_CONTEXT_FIELDS = (
    "actor_role",
    "counterparty_role",
    "role_transition",
    "role_constraint",
    "symmetry_basis",
    "completion_invariant_required",
)

KNOWN_ROLE_TRANSITIONS = {
    "RT-001",
    "RT-002",
    "RT-003",
    "RT-004",
    "RT-005",
    "RT-006",
}


def role_context_warnings(role_context: Dict[str, Any]) -> List[str]:
    """Return warning-only role context findings.

    These warnings intentionally do not block validation or dry-run. They expose
    role posture gaps before broader hard role-transition enforcement is
    introduced.
    """
    if not role_context:
        return ["role_context_missing"]

    warnings: List[str] = []
    for field in RECOMMENDED_ROLE_CONTEXT_FIELDS:
        if field not in role_context:
            warnings.append(f"role_context_missing_recommended_field:{field}")

    role_transition = role_context.get("role_transition")
    if role_transition is not None and str(role_transition) not in KNOWN_ROLE_TRANSITIONS:
        warnings.append(f"role_context_unknown_role_transition:{role_transition}")

    completion_required = role_context.get("completion_invariant_required")
    if completion_required is not None and not isinstance(completion_required, bool):
        warnings.append("role_context_completion_invariant_required_must_be_bool")

    return warnings


def apply_role_context_blocks(role_context: Dict[str, Any]) -> List[str]:
    """Return apply-time role context blocks.

    This is a narrow hard-enforcement slice. It blocks incomplete role context,
    unknown declared role transitions, and invalid completion invariant types
    during apply. Validation and dry-run remain warning-only.
    """
    blocks: List[str] = []
    if not role_context:
        return ["role_context_missing"]

    for field in RECOMMENDED_ROLE_CONTEXT_FIELDS:
        if field not in role_context:
            blocks.append(f"role_context_missing_recommended_field:{field}")

    role_transition = role_context.get("role_transition")
    if role_transition is not None and str(role_transition) not in KNOWN_ROLE_TRANSITIONS:
        blocks.append(f"role_context_unknown_role_transition:{role_transition}")

    completion_required = role_context.get("completion_invariant_required")
    if completion_required is not None and not isinstance(completion_required, bool):
        blocks.append("role_context_completion_invariant_required_must_be_bool")

    return blocks


def role_enforcement_result(role_context: Dict[str, Any], mode: str) -> Dict[str, Any]:
    """Return visible role enforcement posture for runtime outputs."""
    warnings = role_context_warnings(role_context)
    blocks = apply_role_context_blocks(role_context) if mode == "apply" else []
    decision = "BLOCK" if blocks else ("WARN" if warnings else "ALLOW")
    return {
        "stage": "required-role-context-for-apply" if mode == "apply" else "warning-only",
        "mode": mode,
        "role_transition": role_context.get("role_transition") if role_context else None,
        "decision": decision,
        "warnings": warnings,
        "blocks": blocks,
    }
