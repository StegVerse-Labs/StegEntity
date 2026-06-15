# STEGENTITY_ROLE_TRANSITION_POLICY

## Purpose

This document defines the role-transition policy table for StegEntity.

It is a design and enforcement-planning document. It does not change runtime behavior by itself.

The goal is to make hard enforcement reviewable before any runtime block rule is introduced.

## Governing Rule

A role may not convert one kind of standing into another kind of standing without an admissible transition.

In StegEntity, a role transition is admissible only when the transition is declared, receipt-bound, authority-scoped, capsule-bound, adapter-bounded, target-bounded, verification-bounded, and completion-aware.

## Current Enforcement Stage

Current stage:

```text
warning-only validation
```

Current behavior:

- `role_context` is optional;
- missing role context emits warnings;
- incomplete role context emits warnings;
- unknown role transitions emit warnings;
- invalid field types emit warnings;
- runtime execution is not blocked by role context warnings yet.

## Enforcement Stages

| Stage | Name | Runtime Effect |
|---|---|---|
| 0 | Doctrine | No runtime behavior |
| 1 | Preservation | Preserve role context when present |
| 2 | Warning | Emit role warnings without blocking |
| 3 | Soft block | Block only explicitly dangerous role conversions |
| 4 | Required role context | Require complete role context for apply |
| 5 | Full role enforcement | Enforce transition table across validate, dry-run, apply, receipts, and outcomes |

StegEntity is currently at Stage 2.

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

---

## Blocked Conversions

These conversions should never be silently allowed.

| Block ID | Conversion | Reason | Future Severity |
|---|---|---|---|
| RB-001 | proposal_to_execution_without_authority | proposal standing is not execution standing | block |
| RB-002 | adapter_capability_to_admissibility | an adapter can act but cannot authorize action | block |
| RB-003 | dry_run_success_to_apply_authority | dry-run success does not release authority | block |
| RB-004 | platform_event_to_completion | platform mutation is not StegVerse completion | block |
| RB-005 | prior_approval_to_current_authority | old approval may be stale or invalid | block |
| RB-006 | recommendation_to_user_delegation | recommendation is not user-bound authority | block |
| RB-007 | automation_to_open_ended_execution | automation scope must remain bounded | block |
| RB-008 | missing_completion_invariant_to_complete | completion cannot be asserted without completion invariant evidence | block |

---

## Minimal Hard-Enforcement Order

Hard enforcement should be introduced in this order:

1. Block unknown `role_transition` values for apply only.
2. Require `completion_invariant_required` to be boolean for apply.
3. Block `proposal_not_execution` when the operation attempts apply without authority.
4. Require full `role_context` for apply.
5. Echo role enforcement result in outcome reports.
6. Include role enforcement result in execution receipts.
7. Extend enforcement to dry-run and validate only after apply behavior is stable.

## Apply-Time Required Fields

Future apply-time enforcement should require:

```text
actor_role
counterparty_role
role_transition
role_constraint
symmetry_basis
completion_invariant_required
```

## Enforcement Result Shape

Future runtime outputs should include:

```json
{
  "role_enforcement": {
    "stage": "warning-only|soft-block|required|full",
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
