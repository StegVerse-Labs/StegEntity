# STEGENTITY_VERIFICATION

## Purpose

This document defines the repeatable verification path for StegEntity.

Verification is not the same as governance completion. It proves that the current runtime, examples, role-context warning path, generated fixtures, role-context demo check, and local activation check remain internally consistent.

## Local Verification

From the repository root, run:

```bash
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python -m unittest discover tests
python tools/check_role_context_demo.py
python tools/check_repo_activation.py
```

## Local Activation Check

The local activation check is:

```bash
python tools/check_repo_activation.py
```

It verifies:

- validation succeeds;
- dry-run succeeds;
- successful apply writes target state;
- successful apply emits execution receipt;
- successful apply emits apply outcome report;
- successful apply exposes a first-class `completion_invariant` object;
- `completion_invariant` is present, required, satisfied, hash-matched, and verified;
- `completion_invariant` is identical across apply return value, execution receipt, and persisted apply report;
- refused apply does not write target state;
- refused apply emits a non-execution refusal receipt;
- refused apply does not emit an execution receipt;
- refused apply emits a blocked outcome report;
- blocked outcome report is hash-bound to the refusal receipt.

## Automated Verification

The GitHub Actions workflow is:

```text
.github/workflows/stegentity-verify.yml
```

It runs on:

- push;
- pull request;
- manual workflow dispatch.

The workflow performs:

```text
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python -m unittest discover tests
python tools/check_role_context_demo.py
python tools/check_repo_activation.py
```

## What This Verifies

The current verification path checks:

- maintenance capsule parsing;
- optional role_context parsing;
- role_context warning behavior;
- role enforcement output behavior;
- apply-time required role context enforcement;
- proposal-to-execution authority evidence enforcement;
- completion invariant expected-hash enforcement;
- first-class completion invariant artifact output;
- execution receipt role_context preservation;
- execution receipt role_enforcement preservation;
- execution receipt completion_invariant preservation;
- refused apply outcome reports;
- non-execution refusal receipt artifacts;
- role-context demo builder hash binding;
- generated role-context capsule, receipt, and authority file consistency;
- role-context demo runtime validation;
- warning-free role-context demo posture;
- local activation path consistency.

## What This Does Not Verify Yet

This verification path does not yet prove:

- full runtime enforcement of all role transitions;
- multi-adapter behavior beyond local filesystem;
- live StegID receipt minting;
- live TV/TVC token issuance;
- cross-repo governance compatibility;
- production audit readiness.

## Governing Sentence

StegEntity verification proves the current local runtime, role-context demo, activation path, refusal path, and completion-invariant artifact path are internally consistent. It does not by itself establish org-wide governance completion or production admissibility.
