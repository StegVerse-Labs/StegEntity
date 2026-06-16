# STEGENTITY_ACTIVATION_GAP_LIST

## Purpose

This document tracks the remaining work between the current StegEntity activation candidate posture and stronger repo activation.

It is not a production roadmap.

It is a focused activation checklist for the local governed runtime module.

## Current Activation Posture

```text
Activation candidate: local governed runtime module
```

Current local activation is supported by:

- activation status document;
- activation doctrine;
- local activation check command;
- CI activation check;
- successful apply path;
- refused apply path;
- execution receipts;
- refusal receipts;
- outcome reports;
- role enforcement output.

## Activation Gap Checklist

### G1 — Full Role Transition Enforcement

Status: partial

Implemented:

- RT-002 proposal-to-execution apply is blocked without explicit authority evidence;
- RT-002 apply is allowed when authority evidence is declared as `receipt+tvc+capsule`, `tvc+receipt+capsule`, or `explicit_authority`.

Still needed:

- enforce more role transition classes beyond required role context;
- distinguish role standing from adapter capability;
- keep validation and dry-run behavior stable while apply enforcement expands.

Activation impact: high.

### G2 — Completion Invariant Enforcement

Status: open

Need:

- enforce completion invariant requirements beyond boolean shape;
- verify destination state against declared expected state;
- ensure completion cannot be asserted from platform mutation alone.

Activation impact: high.

### G3 — Refusal Evidence Expansion

Status: partial

Need:

- preserve refusal receipt posture for more refusal classes;
- ensure refusal receipts remain non-execution artifacts;
- ensure refused paths are linked to blocked outcome reports by hash.

Activation impact: medium.

### G4 — Multi-Adapter Readiness

Status: open

Need:

- add at least one additional adapter beyond `local_fs`;
- preserve the same receipt and outcome contract across adapters;
- document adapter-specific authority scope requirements.

Activation impact: medium.

### G5 — Live StegID Integration

Status: open

Need:

- replace demo verified receipt consumption with live StegID-compatible receipt verification;
- preserve local demo mode for offline activation checks;
- document boundary between consumed receipt and minted receipt.

Activation impact: high for org integration, medium for local activation.

### G6 — Live TV/TVC Integration

Status: open

Need:

- replace demo authority token consumption with live TV/TVC-compatible authority release;
- preserve local demo mode for activation checks;
- document token issuance, expiry, revocation, and scope matching.

Activation impact: high for org integration, medium for local activation.

### G7 — Cross-Repo Compatibility

Status: open

Need:

- run StegEntity against adjacent governance repositories;
- verify CGE decision-manager compatibility;
- verify TV/TVC provider compatibility;
- verify StegID receipt compatibility;
- verify output artifacts remain reconstructable across repo boundaries.

Activation impact: high.

## Activation Bands

| Activation Percent | Meaning |
|---|---|
| 0-25% | Conceptual activation only |
| 26-50% | Local runtime works, incomplete governance evidence |
| 51-75% | Local governed runtime candidate |
| 76-90% | Strong local activation with broader enforcement |
| 91-100% | Activation-ready with integration evidence |

## Current Estimate

```text
StegEntity Repo Activation: ~83% complete vs Repo Activation
```

This estimate is local-activation oriented. It does not claim production completion.

## Governing Sentence

StegEntity activation gaps must remain explicit until the repo can prove admissible execution, refused execution, completion invariants, and role-transition boundaries across the relevant runtime and integration surfaces.
