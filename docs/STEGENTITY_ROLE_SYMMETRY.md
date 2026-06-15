# STEGENTITY_ROLE_SYMMETRY

## Purpose

This document defines symmetrical role determinations for governed AI roles in `StegEntity`.

It exists to keep proposal, delegation, automation, execution, verification, and publication distinct.

`StegEntity` roles are governance positions, not interchangeable capabilities.

## Assumptions

- `StegEntity` is a governed runtime for AI-role expressions.
- Existing role names are preserved:
  - `StegBot`
  - `StegAgent`
  - `StegEntity`
  - `StegVerseAI`
  - `UserAI`
- A role may not mutate state merely because it can.
- Execution requires convergence between identity, authority, capsule, adapter, target, verification, and receipt.
- Platform events are not StegVerse completion events.
- This file adds doctrine only; it does not change runtime code.

## Done Criteria

This document is complete when it defines:

- the governing symmetry rule for all roles;
- the primary role functions;
- the symmetrical constraint for each role;
- allowed role transitions;
- blocked role conversions;
- publication and completion constraints;
- future runtime fields that may later enforce these determinations.

---

## 1. Governing Rule

StegEntity treats AI roles as symmetrical governance positions, not interchangeable capabilities.

A role may reason, propose, review, delegate, execute, verify, or report only within its:

- receipt-bound identity;
- TVC-scoped authority;
- declared transition posture;
- maintenance capsule;
- adapter boundary;
- target boundary;
- verification requirement;
- completion invariant.

No role may convert reasoning standing into execution standing without a receipt-bound authority transition.

---

## 2. Role Symmetry Thesis

A governed transition becomes admissible only when the following converge:

```text
acting role
+ verified receipt
+ scoped authority token
+ declared capsule
+ adapter boundary
+ target boundary
+ required scopes
+ verification requirement
+ outcome receipt
```

This is the StegEntity equivalent of a convergence point.

The convergence point does not erase role distinctions.

It binds them.

---

## 3. Role Matrix

| Role | Primary Function | Symmetrical Constraint | May Propose | May Review | May Execute | Requires Receipt | Requires TVC |
|---|---|---|---|---|---|---|---|
| StegBot | Task automation | Automation does not erase accountability | Yes, bounded | Limited | Only through capsule/adapter path | Yes | Yes |
| StegAgent | Reasoning, proposal, and review | Proposal does not equal execution | Yes | Yes | No by default | Yes | Yes if action-bound |
| StegEntity | Governed executable entity | Execution requires admissibility | No by default | Runtime validation | Yes, through adapter | Yes | Yes |
| StegVerseAI | Ecosystem-side counterpart intelligence | Counterpart status does not absorb user authority | Yes | Yes | No by default | Yes | Yes if action-bound |
| UserAI | User-bound delegated intelligence | Delegation is scoped and expiring | Yes | User-side review | No by default | Yes | Yes if action-bound |

---

## 4. Role Determinations

### 4.1 StegBot

`StegBot` is a task automation role.

Determination:

```text
Automation does not erase accountability.
```

A `StegBot` may perform bounded automated tasks only through declared scope, receipt-backed identity, TVC-scoped authority, and capsule-defined operation.

A `StegBot` may not silently convert recurring or automated task standing into open-ended authority.

### 4.2 StegAgent

`StegAgent` is a reasoning, proposal, and review role.

Determination:

```text
Proposal does not equal execution.
```

A `StegAgent` may reason, draft, propose, validate, review, and recommend transitions.

A `StegAgent` may not execute merely because its reasoning is accepted.

Execution requires a separate admissible transition through `StegEntity`.

### 4.3 StegEntity

`StegEntity` is a governed executable entity role.

Determination:

```text
Execution requires admissibility.
```

`StegEntity` may execute only when:

- the capsule is structurally valid;
- the admissibility decision is `ALLOW`;
- the acting identity has a valid receipt;
- the TVC-style authority token is valid;
- required scopes are present;
- the adapter and target match authority;
- verification requirements are declared;
- the result can produce receipt and outcome report.

### 4.4 StegVerseAI

`StegVerseAI` is the StegVerse-side counterpart intelligence.

Determination:

```text
Counterpart intelligence does not absorb user authority.
```

`StegVerseAI` may represent ecosystem-side reasoning, review posture, policy comparison, and governance support.

It may not silently inherit `UserAI` authority, user delegation, or execution standing.

### 4.5 UserAI

`UserAI` is a user-bound delegated intelligence.

Determination:

```text
Delegation is scoped and expiring.
```

`UserAI` may act only within the user's declared, receipt-bound, time-bound, and scope-bound delegation.

A `UserAI` may not convert user preference, prior approval, or conversational consent into current execution authority unless the authority is present at commit time.

---

## 5. Symmetrical Role Transitions

### RT-001: Reasoning to Proposal

A reasoning role may form a proposed transition.

Allowed roles:

- `StegAgent`
- `StegVerseAI`
- `UserAI`

Constraint:

```text
A proposal is not execution authority.
```

### RT-002: Proposal to Capsule

A proposed transition may become a maintenance capsule only when the capsule declares:

- target;
- adapter;
- transition ID;
- transition name;
- dependencies;
- consequences;
- rollback plan;
- verification requirements;
- operations;
- required scopes.

Allowed roles:

- `StegAgent`
- `StegVerseAI`
- `UserAI`
- `StegBot`, under bounded automation

Constraint:

```text
A capsule describes intended transition; it does not authorize itself.
```

### RT-003: Capsule to Admissibility

A capsule may enter admissibility review only when identity and authority requirements can be evaluated.

Constraint:

```text
Admissibility requires receipt and authority comparison.
```

### RT-004: Admissibility to Execution

Execution is allowed only when:

```text
admissibility decision = ALLOW
```

and receipt, token, capsule, adapter, target, scope, and verification requirements converge.

Allowed role:

- `StegEntity`

Constraint:

```text
Execution authority is not inherited from proposal authority.
```

### RT-005: Execution to Completion

Execution becomes complete only when:

- target state changed as authorized;
- destination hash matches expected hash, where required;
- execution receipt is emitted;
- outcome report is written;
- state is reconstructable.

Constraint:

```text
Platform mutation is not StegVerse completion.
```

### RT-006: Completion to Publication

A result may be reported as a StegVerse completion event only when the completion invariant is satisfied.

Constraint:

```text
A platform event may be mentioned as a platform event, but not elevated into StegVerse completion unless StegEntity completion requirements are satisfied.
```

---

## 6. Blocked Role Conversions

The following conversions are blocked unless separately authorized through receipt-bound transition authority:

```text
StegAgent proposal -> StegEntity execution
StegVerseAI recommendation -> UserAI delegation
UserAI preference -> current commit-time authority
StegBot automation -> open-ended execution
Adapter capability -> admissibility
Platform event -> StegVerse completion
Prior approval -> current authority
Dry-run success -> apply authority
```

---

## 7. Symmetrical Counterpart Rule

`StegVerseAI` and `UserAI` are counterpart roles.

They may interact, compare, review, and produce proposals.

They may not silently merge.

```text
StegVerseAI represents ecosystem-side reasoning.
UserAI represents user-bound delegated reasoning.
Neither role may absorb the other's authority.
```

When both roles participate in a transition, the capsule should preserve which role supplied:

- proposal;
- review;
- delegation;
- policy comparison;
- user-bound authorization;
- ecosystem-side governance posture.

---

## 8. Automation Rule

A `StegBot` may automate only within bounded authority.

Automation must preserve:

- actor class;
- scope;
- target;
- adapter;
- operation;
- authority basis;
- verification;
- receipt trail.

```text
Automation is not anonymity.
Automation is not authority expansion.
Automation is not completion by itself.
```

---

## 9. Adapter Boundary Rule

Adapters perform environment-specific mutation.

Adapters do not decide admissibility.

```text
StegEntity governs transition execution.
Adapters perform bounded state mutation.
Adapter capability is not execution authority.
```

This rule applies to GitHub, local filesystem, cloud storage, API, or any future adapter.

---

## 10. Completion Invariant

A transition is complete only when:

```text
target state changed as authorized
destination hash matches expected hash, where required
receipt emitted
outcome report written
state is reconstructable
```

No role may report a transition as a StegVerse completion event before this invariant is satisfied.

---

## 11. Future Runtime Fields

Future capsule, receipt, or outcome schemas may add fields such as:

```json
{
  "actor_role": "StegAgent",
  "counterparty_role": "StegEntity",
  "role_transition": "RT-002",
  "role_constraint": "proposal_not_execution",
  "symmetry_basis": "receipt+tvc+capsule",
  "completion_invariant_required": true
}
```

These fields are not required by this doctrine file yet.

They are candidate enforcement fields for later runtime versions.

---

## 12. Future Validator Checks

Future StegEntity validators may check:

- actor role is declared;
- role transition is allowed;
- proposal roles cannot directly execute;
- execution roles require `ALLOW`;
- TVC token scopes match operation scopes;
- adapter and target match authority;
- completion cannot be reported before receipt and outcome report exist;
- delegated roles expire with their authority;
- counterpart roles do not silently merge.

---

## 13. Publication Language

Allowed:

```text
This role proposed a transition.
This role reviewed a transition.
This role executed an admissible capsule.
This transition completed under StegEntity completion requirements.
```

Cautionary:

```text
This platform event occurred, but StegVerse completion has not yet been established.
```

Blocked unless separately supported:

```text
The proposal authorized execution.
The adapter authorized the transition.
The user previously approved, therefore current authority exists.
The workflow succeeded, therefore StegVerse completion occurred.
The bot automated it, therefore accountability is reduced.
```

---

## 14. Relationship to Existing Runtime

This doctrine aligns with current StegEntity runtime behavior:

- capsules declare transition intent;
- receipts identify actor standing;
- TVC-style tokens release scoped authority;
- adapters perform bounded mutation;
- dry-run and apply remain distinct;
- execution receipts and outcome reports preserve completion evidence.

This file clarifies role symmetry without requiring immediate code changes.

---

## 15. Governing Sentence

StegEntity treats AI roles as symmetrical governance positions, not interchangeable capabilities. A role may reason, propose, review, delegate, execute, verify, or report only within its receipt-bound identity, TVC-scoped authority, declared transition posture, adapter boundary, and completion invariant.
