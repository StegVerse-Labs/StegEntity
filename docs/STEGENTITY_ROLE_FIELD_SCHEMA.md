# STEGENTITY_ROLE_FIELD_SCHEMA

## Purpose

This document defines the proposed schema surface for role symmetry fields in StegEntity.

It is a doctrine and schema-planning document only. It does not change runtime behavior.

## Assumptions

- Current working demo capsules must not be modified until matching receipt and authority hashes are regenerated.
- Role symmetry fields should be introduced first as documentation and examples.
- Runtime enforcement should come later with validators and tests.
- Existing capsule, receipt, and authority token behavior remains valid.

## Done Criteria

This document is complete when it defines:

- proposed role fields;
- where those fields should appear;
- which fields are required later versus optional now;
- how role symmetry maps to capsule, receipt, authority token, and outcome records;
- why the existing demo capsule should remain unchanged for now.

---

## 1. Current State

StegEntity currently validates:

- maintenance capsule structure;
- admissibility decision;
- operation scopes;
- StegID-style verified receipt structure;
- receipt expiration and assurance level;
- receipt payload hash;
- TVC-style authority token status;
- token expiration;
- adapter and target match;
- token capsule hash;
- required scopes;
- post-write hash verification.

Role symmetry is currently documented in:

```text
docs/STEGENTITY_ROLE_SYMMETRY.md
```

It is not yet enforced by runtime validators.

---

## 2. Proposed Capsule Field

Future maintenance capsules may include:

```json
"role_context": {
  "actor_role": "StegAgent",
  "counterparty_role": "StegEntity",
  "role_transition": "RT-002",
  "role_constraint": "proposal_not_execution",
  "symmetry_basis": "receipt+tvc+capsule",
  "completion_invariant_required": true
}
```

### Field Meanings

| Field | Meaning |
|---|---|
| `actor_role` | Role initiating or proposing the transition |
| `counterparty_role` | Role expected to validate, execute, review, or receive the transition |
| `role_transition` | Declared role transition class, such as `RT-002` |
| `role_constraint` | Constraint that prevents role overreach |
| `symmetry_basis` | Evidence basis required for convergence |
| `completion_invariant_required` | Whether completion must satisfy StegEntity completion invariant |

---

## 3. Proposed Receipt Field

Future verified receipts may include:

```json
"role_context": {
  "actor_role": "StegAgent",
  "role_scope": "proposal",
  "delegation_state": "none",
  "role_transition_allowed": ["RT-001", "RT-002"]
}
```

This would allow StegID to bind identity evidence to role posture.

---

## 4. Proposed Authority Token Field

Future TVC-style authority tokens may include:

```json
"role_authority": {
  "authorized_role": "StegEntity",
  "authorized_transition": "RT-004",
  "blocked_role_conversions": [
    "proposal_to_execution_without_authority",
    "adapter_capability_to_admissibility",
    "platform_event_to_completion"
  ]
}
```

This would allow TVC to release authority for a role transition, not just a generic operation scope.

---

## 5. Proposed Outcome Field

Future outcome reports may include:

```json
"role_outcome": {
  "executing_role": "StegEntity",
  "originating_role": "StegAgent",
  "role_transition_completed": "RT-005",
  "completion_invariant_satisfied": true,
  "publication_allowed": true
}
```

This would preserve the role path after execution.

---

## 6. Enforcement Stages

### Stage 0: Doctrine Only

Role symmetry is documented but not enforced.

Current repo stage.

### Stage 1: Non-Executable Examples

Role symmetry fields are shown in example fragments but not used by the working demo.

Recommended next stage.

### Stage 2: Optional Parsing

Runtime accepts and preserves role fields without requiring them.

### Stage 3: Validator Warnings

Runtime warns when role fields are missing or inconsistent.

### Stage 4: Required Enforcement

Runtime requires role fields and blocks invalid role transitions.

### Stage 5: Cross-System Enforcement

StegID, TVC, StegEntity, and adapters all preserve and validate role symmetry.

---

## 7. Why Not Modify the Working Demo Capsule Yet

The existing demo capsule participates in hash-bound validation.

Changing the capsule body changes the capsule hash.

That would require updating matching receipt and authority examples.

Until the validator and examples are updated together, the working demo capsule should remain unchanged.

Therefore role symmetry should first be introduced as:

```text
docs/STEGENTITY_ROLE_FIELD_SCHEMA.md
examples/role_symmetry_capsule_fragment.json
```

---

## 8. Minimal Next Runtime Change

The smallest future runtime change is to preserve `role_context` from the capsule into validate, dry-run, apply, receipt, and outcome outputs when present.

That would make role posture visible without enforcing it yet.

Later validators can enforce allowed transitions.

---

## 9. Governing Sentence

Role symmetry fields should make role posture explicit without allowing role posture to replace receipt-bound identity, TVC-scoped authority, declared capsule scope, adapter boundaries, verification, or completion evidence.
