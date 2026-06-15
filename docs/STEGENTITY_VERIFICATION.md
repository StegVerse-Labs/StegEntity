# STEGENTITY_VERIFICATION

## Purpose

This document defines the repeatable verification path for StegEntity.

Verification is not the same as governance completion. It proves that the current runtime, examples, role-context warning path, generated fixtures, and role-context demo check remain internally consistent.

## Local Verification

From the repository root, run:

```bash
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python -m unittest discover tests
python tools/check_role_context_demo.py
```

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
```

## What This Verifies

The current verification path checks:

- maintenance capsule parsing;
- optional role_context parsing;
- role_context warning behavior;
- execution receipt role_context preservation;
- role-context demo builder hash binding;
- generated role-context capsule, receipt, and authority file consistency;
- role-context demo runtime validation;
- warning-free role-context demo posture.

## What This Does Not Verify Yet

This verification path does not yet prove:

- hard runtime enforcement of role transitions;
- multi-adapter behavior beyond local filesystem;
- live StegID receipt minting;
- live TV/TVC token issuance;
- cross-repo governance compatibility;
- production audit readiness.

## Governing Sentence

StegEntity verification proves the current runtime and role-context demo are internally consistent. It does not by itself establish org-wide governance completion or production admissibility.
