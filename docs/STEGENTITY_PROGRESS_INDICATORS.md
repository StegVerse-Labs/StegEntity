# STEGENTITY_PROGRESS_INDICATORS

## Purpose

This document defines how progress indicators should be stated for StegEntity work.

Progress indicators are not claims of final completion. They are bounded estimates of work completed against the known governance, runtime, documentation, testing, and integration surface.

## Required Response Format

When reporting ongoing StegVerse-Labs / StegEntity work, include two lines:

```text
Org completion: <percent>% — <short basis>
Repo completion: <percent>% — <short basis>
```

The organization line estimates StegVerse-Labs governance coverage across the broader org.

The repository line estimates completion for `StegVerse-Labs/StegEntity` specifically.

## Current Baseline

As of this document:

```text
Org completion: ~6%
Repo completion: ~48%
```

These are working estimates, not audited final metrics.

## Org Completion Basis

The org-level percentage should consider:

- how many repositories have explicit governance doctrine;
- how many repositories have README-level boundary declarations;
- how many repositories have runtime enforcement instead of doctrine only;
- how much TV/TVC, StegID, CGE, StegEntity, and repo-specific governance are wired together;
- how much testing exists across repos;
- whether completion events are receipt-bound and reconstructable across the org.

A low org percentage is expected while most repositories still lack explicit, wired governance layers.

## Repo Completion Basis

The StegEntity repo-level percentage should consider:

- README clarity;
- runtime implementation;
- maintenance capsule validation;
- StegID-style receipt consumption;
- TVC-style authority token validation;
- adapter behavior;
- safe path enforcement;
- dry-run / apply separation;
- receipt and outcome emission;
- rollback material capture;
- unit tests;
- role symmetry doctrine;
- role symmetry field schema notes;
- role context preservation in capsule parsing;
- role context preservation in runtime outputs;
- role context preservation in execution receipts;
- warning-only role context validation;
- role symmetry runtime enforcement;
- multi-adapter support;
- integration with live TV/TVC issuance;
- integration with live StegID receipt minting;
- completion invariant enforcement;
- cross-repo governance compatibility.

## Repo Progress Bands

| Band | Meaning |
|---|---|
| 0-10% | Concept only or empty scaffold |
| 11-25% | Basic structure and doctrine started |
| 26-40% | Working local runtime plus core documentation |
| 41-60% | Runtime plus stronger doctrine, tests, and first enforcement expansions |
| 61-75% | Multi-adapter readiness and stronger schema enforcement |
| 76-90% | Integrated with live StegID / TVC and cross-repo governance |
| 91-100% | Production-ready, audited, reconstructable, and org-integrated |

## Current Repo Assessment

StegEntity is currently past scaffold stage because it includes:

- working Python runtime;
- local filesystem adapter;
- capsule validation;
- authority token validation;
- verified receipt consumption;
- safe path enforcement;
- dry-run and apply flow;
- hash verification;
- rollback material capture;
- execution receipts;
- outcome reports;
- unit tests;
- role symmetry doctrine;
- role field schema notes;
- non-executable role context example fragment;
- optional role context parsing;
- optional role context runtime output preservation;
- optional role context execution receipt preservation;
- warning-only role context validation;
- runtime output of role context warnings;
- tests for role context parsing, execution receipt inclusion, and role context warnings.

StegEntity is not yet complete because it still needs:

- hard runtime validation of role transitions;
- validator warnings for full runtime paths beyond focused unit checks;
- multi-adapter support beyond local filesystem;
- live TV/TVC token issuance integration;
- live StegID receipt minting integration;
- stronger completion invariant checks;
- cross-repo governance compatibility testing.

## Update Rule

Percentages should move only when evidence changes.

Do not increase a percentage because a concept was discussed.

Increase a percentage only when a file, runtime behavior, test, schema, integration, receipt, or documented governance boundary exists.

## Governing Sentence

Progress indicators must describe the current evidence-backed completion posture of the organization and repository. They are estimates constrained by observable governance, runtime, testing, integration, and receipt-bound completion evidence.
