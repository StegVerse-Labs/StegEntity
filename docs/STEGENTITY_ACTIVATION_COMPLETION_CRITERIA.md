# STEGENTITY_ACTIVATION_COMPLETION_CRITERIA

## Purpose

This document defines what remains between the current StegEntity local activation candidate posture and 100% local repo activation.

It does not define production readiness.

It does not define org-wide StegVerse governance completion.

It defines the final local-repo activation criteria only.

## Current Local Activation Posture

```text
Activation candidate: local governed runtime module
```

Current estimate:

```text
StegEntity Repo Activation: ~96% complete vs Repo Activation
```

The repo already demonstrates:

- local runtime operation;
- local filesystem adapter behavior;
- maintenance capsule validation;
- TVC-style authority token consumption;
- StegID-style verified receipt consumption;
- dry-run path;
- successful apply path;
- refused apply path;
- execution receipt emission;
- refusal receipt emission;
- outcome report emission;
- blocked outcome report emission;
- role enforcement posture;
- completion invariant evidence;
- activation manifest validation;
- CI activation checks;
- CI failure interpretation.

## Definition of 100% Local Repo Activation

StegEntity reaches 100% local repo activation when the repository can prove, using only checked-in code, checked-in examples, and local/CI commands, that:

1. Every activation artifact is generated, verified, or linked by a repeatable command.
2. Every machine-readable activation claim is validated by CI.
3. Every human-readable activation claim maps to a machine-readable manifest entry.
4. Every activation-critical failure has a documented diagnostic path.
5. Successful mutation and refused mutation remain independently reconstructable.
6. Completion invariant evidence remains consistent across return value, receipt, and outcome report.
7. Role enforcement posture remains visible in runtime outputs and receipts.
8. The repo clearly distinguishes local activation from production readiness.

## Remaining Local Activation Criteria

### C1 — Activation Document Cross-Link Closure

All activation documents must be mutually discoverable from at least one canonical entry point.

Required canonical entry points:

- `README.md`
- `ACTIVATION_STATUS.md`
- `activation_manifest.json`
- `docs/STEGENTITY_VERIFICATION.md`

Completion condition:

```text
Every activation-relevant document is linked from README and registered in activation_manifest.json where machine-readable registration is appropriate.
```

### C2 — Activation Manifest Drift Guard

The manifest verifier must fail if required activation command, evidence, non-claim, gap, or document links drift.

Completion condition:

```text
tools/verify_activation_manifest.py enforces all current activation document links and activation command names.
```

### C3 — Completion Criteria Registration

This document must be registered as an activation document and included in manifest verification.

Completion condition:

```text
activation_manifest.json contains documents.activation_completion_criteria and the verifier requires that key.
```

### C4 — Final Activation Smoke Test

A single local command path must exist for reviewers to run all activation checks.

Current command path:

```bash
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python tools/verify_activation_manifest.py
python -m unittest discover tests
python tools/check_role_context_demo.py
python tools/check_repo_activation.py
```

Completion condition:

```text
The command path is documented in README, verification guide, CI failure guide, and activation runbook.
```

### C5 — Non-Production Boundary Preservation

The repo must preserve the distinction between local activation and production readiness.

Completion condition:

```text
README, ACTIVATION_STATUS, activation_manifest.json, activation doctrine, and completion criteria all explicitly retain production non-claims.
```

## What 100% Local Activation Will Not Mean

Even at 100% local repo activation, StegEntity will not claim:

- production deployment readiness;
- live StegID minting;
- live TV/TVC issuance;
- multi-adapter parity;
- cross-repo admissibility completion;
- org-wide StegVerse governance completion.

## Final Local Activation Statement

When all criteria above are satisfied, the repo may claim:

```text
StegEntity local repo activation complete.
```

It may not claim:

```text
StegEntity production ready.
```

## Governing Sentence

StegEntity local repo activation is complete only when every activation claim is repeatable, documented, machine-checkable where appropriate, CI-enforced, failure-diagnosable, and explicitly bounded away from production or org-wide completion claims.
