# STEGENTITY_ROLE_TRANSITION_POLICY

## Purpose

This document defines the role-transition policy table for StegEntity.

It is a design and enforcement-planning document. Runtime behavior must not exceed this document.

The goal is to make hard enforcement reviewable before each runtime block rule is introduced.

## Governing Rule

A role may not convert one kind of standing into another kind of standing without an admissible transition.

In StegEntity, a role transition is admissible only when the transition is declared, receipt-bound, authority-scoped, capsule-bound, adapter-bounded, target-bounded, verification-bounded, and completion-aware.

## Current Enforcement Stage

Current stage:

```text
Stage 4 required role context for apply
```

Current behavior:

- `role_context` is optional for validate and dry-run;
- missing role context emits warnings during validate and dry-run;
- incomplete role context emits warnings during validate and dry-run;
- unknown role transitions emit warnings during validate and dry-run;
- invalid field types emit warnings during validate and dry-run;
- apply blocks missing role context;
- apply blocks incomplete role context;
- apply blocks unknown `role_transition` values;
- apply blocks non-boolean `completion_invariant_required` values;
- refused apply attempts write `apply.blocked` outcome reports before raising;
- refused apply attempts emit `blocked_apply` receipts, not execution receipts;
- refused apply attempts do not mutate target state;
- validate, dry-run, and apply outputs include a visible `role_enforcement` result;
- successful execution receipts include the apply-time `role_enforcement` result.

## Enforcement Stages

| Stage | Name | Runtime Effect |
|---|---|---|
| 0 | Doctrine | No runtime behavior |
| 1 | Preservation | Preserve role context when present |
| 2 | Warning | Emit role warnings without blocking |
| 3 | Soft block | Block only explicitly dangerous role conversions |
| 4 | Required role context | Require complete role context for apply |
| 5 | Full role enforcement | Enforce transition table across validate, dry-run, apply, receipts, and outcomes |

StegEntity is currently at Stage 4 for apply and Stage 2 for validate/dry-run.

---

## Role Transition Classes

| Transition | Source Role | Counterparty Role | Allowed Posture | Current Stage | Future Hard Rule |
|---|---|---|---|---|---|
| RT-001 | StegBot | StegAgent | automation-to-proposal | warning-only | StegBot may propose but may not execute without StegEntity authority |
| RT-002 | StegAgent | StegEntity | proposal-to-execution-request | warning-only | StegAgent proposal may not become execution without TVC authority and admissible capsule |
| RT-003 | StegVerseAI | UserAI | counterpart-to-delegation-request | warning-only | StegVerseAI recommendation may not become user delegation without user-bound authority |
| RT-004 | StegAgent | StegEntity | execution-requires-admissibility | warning-only | execution requires receipt, TVC token, capsule, adapter, target, verification, and completion invariant |
| RT-005 | StegEntity | StegAgent | execution-to-report | warning-only | completion report requires verified outcome and execution receipt |
| RT-006 | UserAI | StegEntity | delegated-user-action | warning-only | UserAI delegation must be current, scoped, receipt-bound, and target-bounded |
| UNKNOWN | Any | Any | not allowed for apply | apply-blocked | unknown role transitions are blocked at apply time |

---

## Refusal Receipts

Refused apply attempts emit a non-execution receipt:

```text
stegverse.stegentity.blocked_apply_receipt
```

This receipt proves the refusal posture without implying that execution occurred.

It is linked from the blocked outcome report by hash.

---

## Blocked Conversions

These conversions should never be silently allowed.

| Block ID | Conversion | Reason | Current Status | Future Severity |
|---|---|---|---|---|
| RB-000 | unknown_role_transition_on_apply | unknown role transition cannot authorize mutation | implemented for apply | block |
| RB-000B | invalid_completion_invariant_type_on_apply | completion invariant posture must be explicit boolean when declared | implemented for apply | block |
| RB-000C | missing_or_incomplete_role_context_on_apply | apply requires declared role posture | implemented for apply | block |
| RB-000D | refused_apply_without_outcome | refused attempts must be reconstructable | implemented | block |
| RB-000E | refused_apply_as_execution_receipt | refusal receipt must not masquerade as execution | implemented | block |
| RB-001 | proposal_to_execution_without_authority | proposal standing is not execution standing | planned | block |
| RB-002 | adapter_capability_to_admissibility | an adapter can act but cannot authorize action | planned | block |
| RB-003 | dry_run_success_to_apply_authority | dry-run success does not release authority | planned | block |
| RB-004 | platform_event_to_completion | platform mutation is not StegVerse completion | planned | block |
| RB-005 | prior_approval_to_current_authority | old approval may be stale or invalid | planned | block |
| RB-006 | recommendation_to_user_delegation | recommendation is not user-bound authority | planned | block |
| RB-007 | automation_to_open_ended_execution | automation scope must remain bounded | planned | block |
| RB-008 | missing_completion_invariant_to_complete | completion cannot be asserted without completion invariant evidence | planned | block |

---

## Minimal Hard-Enforcement Order

Hard enforcement should be introduced in this order:

1. Block unknown `role_transition` values for apply only. **Implemented.**
2. Require `completion_invariant_required` to be boolean for apply. **Implemented.**
3. Block `proposal_not_execution` when the operation attempts apply without authority.
4. Require full `role_context` for apply. **Implemented.**
5. Echo role enforcement result in outcome reports. **Implemented for successful and refused outputs.**
6. Include role enforcement result in execution receipts. **Implemented for successful apply receipts.**
7. Emit non-execution refusal receipts for blocked apply attempts. **Implemented.**
8. Extend enforcement to dry-run and validate only after apply behavior is stable.

## Apply-Time Required Fields

Apply-time enforcement requires:

```text
actor_role
counterparty_role
role_transition
role_constraint
symmetry_basis
completion_invariant_required
```

## Enforcement Result Shape

Runtime outputs, refused outcome reports, successful execution receipts, and refusal receipts include:

```json
{
  "role_enforcement": {
    "stage": "warning-only|required-role-context-for-apply",
    "mode": "validate|dry_run|apply",
    "role_transition": "RT-004",
    "decision": "ALLOW|WARN|BLOCK",
    "warnings": [],
    "blocks": []
  }
}
```

## Non-Claim

This document does not claim role-transition enforcement is complete.

It defines the policy table that hard enforcement must follow.

## Governing Sentence

Role-transition enforcement must prevent role standing from silently converting into execution standing, completion standing, delegation standing, or publication standing without current receipt-bound and authority-scoped admissibility evidence.
