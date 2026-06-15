# STEGENTITY_ACTIVATION

## Purpose

This document defines what repo activation means for `StegVerse-Labs/StegEntity`.

Activation is not the same as production completion.

Activation means the repository can be run as a governed local runtime module with repeatable evidence that the core transition paths work as declared.

## Activation Claim

StegEntity may claim local repo activation only when the repo demonstrates:

- local runtime execution;
- local adapter operation;
- capsule validation;
- authority-token validation;
- verified-receipt consumption;
- dry-run behavior;
- successful apply behavior;
- execution receipt emission;
- outcome report emission;
- refused apply behavior;
- non-execution refusal receipt emission;
- no mutation during refused apply;
- no execution receipt during refused apply;
- CI coverage for the activation check.

## Activation Check Command

The activation check is:

```bash
python tools/check_repo_activation.py
```

The check verifies two paths.

### Successful Apply Path

The success path verifies:

- validation returns `ok`;
- dry-run returns `ok`;
- apply returns `ok`;
- target state is written;
- execution receipt exists;
- apply outcome report exists;
- role enforcement decision is `ALLOW`.

### Refused Apply Path

The refusal path verifies:

- invalid apply posture raises before mutation;
- target state is not written;
- non-execution refusal receipt exists;
- execution receipt does not exist;
- refused apply outcome report exists;
- refused outcome is hash-bound to the refusal receipt.

## Activation Scope

Current activation scope is local-only.

It covers the `local_fs` adapter and generated role-context demo artifacts.

It does not claim live StegID minting, live TV/TVC issuance, multi-adapter readiness, or cross-repo governance enforcement.

## Current Activation Status

Current status:

```text
Activation candidate: local governed runtime module
```

This means the repo has enough evidence to be run locally as a governed module, but not enough evidence to be called production complete.

## Non-Claims

StegEntity activation does not claim:

- production deployment readiness;
- live authority issuance;
- live identity minting;
- complete role-transition enforcement across every runtime mode;
- multi-adapter parity;
- org-wide governance completion;
- cross-repo admissibility completion.

## Remaining Activation Work

Before stronger activation can be claimed, StegEntity still needs:

- stronger role-transition policy checks;
- fuller completion invariant enforcement;
- additional adapter support;
- richer blocked-path receipt coverage;
- stable integration with TV/TVC issuance;
- stable integration with StegID receipt minting;
- compatibility checks against adjacent StegVerse governance repositories.

## Governing Sentence

StegEntity repo activation means the local governed runtime can prove both admissible mutation and refused mutation paths with receipts, outcome reports, and reconstructable role-enforcement posture, without claiming production or org-wide completion.
