# STEGENTITY_CI_FAILURE_GUIDE

## Purpose

This guide maps StegEntity CI failures to the activation posture they threaten.

CI is not merely a software-health signal for this repo. CI is part of the local activation evidence chain.

## Workflow

Canonical workflow:

```text
.github/workflows/stegentity-verify.yml
```

Current workflow steps:

```text
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python tools/verify_activation_manifest.py
python -m unittest discover tests
python tools/check_role_context_demo.py
python tools/check_repo_activation.py
```

## Failure Map

| Failing Step | Activation Meaning | First Diagnostic |
|---|---|---|
| `build_role_context_demo.py` | generated demo evidence cannot be produced | check deterministic capsule/receipt/authority builder inputs |
| `verify_generated_role_context_demo.py` | generated files drifted from builder contract | rebuild fixtures and compare expected hash |
| `verify_activation_manifest.py` | machine-readable activation posture drifted or is incomplete | inspect `activation_manifest.json` and missing-key error |
| `python -m unittest discover tests` | runtime, evidence, or helper behavior regressed | inspect failing test name before changing docs |
| `check_role_context_demo.py` | role-context demo is not warning-free or not admissible | inspect role-context warnings and capsule hash |
| `check_repo_activation.py` | local activation evidence failed | inspect success-path and refusal-path assertion message |

## Activation-Critical Failures

These failures directly weaken the current activation claim:

- missing execution receipt after successful apply;
- missing apply outcome report after successful apply;
- missing completion invariant object;
- unsatisfied completion invariant;
- completion invariant mismatch across return value, execution receipt, and apply report;
- target mutation during refused apply;
- missing refusal receipt;
- execution receipt emitted during refusal;
- blocked outcome report not bound to refusal receipt.

Any of these failures means the repo should not claim stronger local activation until fixed.

## Manifest Failures

If `tools/verify_activation_manifest.py` fails, the likely causes are:

- schema name/version drift;
- missing top-level manifest section;
- activation evidence flag missing or false;
- canonical command mismatch;
- success/refusal requirement missing;
- non-claim incorrectly set true;
- gap status drift;
- linked document path missing.

Fix the source truth first, then update the manifest.

Do not weaken the verifier merely to pass CI.

## Runtime Test Failures

If unit tests fail, do not assume the test is stale.

StegEntity tests encode governance expectations, not just code behavior.

A failing test may mean one of these posture regressions occurred:

- role context is not preserved;
- role enforcement is not emitted;
- apply enforcement is too weak;
- refusal evidence is missing;
- execution receipt fields drifted;
- completion invariant evidence is not reconstructable.

## Activation Check Failures

If `tools/check_repo_activation.py` fails, activation posture is directly affected.

Use the assertion message to classify the problem:

```text
validation failed                        -> authority or capsule admissibility issue
dry run failed                           -> adapter simulation issue
apply failed                             -> admissible mutation path issue
target file missing after apply          -> mutation did not occur
execution receipt missing                -> successful mutation not receipt-bearing
apply outcome report missing             -> successful mutation not reportable
completion invariant not satisfied       -> completion evidence invalid
completion invariant differs             -> receipt/report/return drift
refused apply unexpectedly succeeded     -> precondition enforcement regression
target file was written during refusal   -> refused mutation safety failure
refusal receipt missing                  -> refusal not receipt-bearing
execution receipt emitted during refusal -> refusal masqueraded as execution
blocked outcome report missing           -> refusal not reportable
blocked outcome not bound                -> refusal evidence not reconstructable
```

## Fix Order

When CI fails, fix in this order:

1. Runtime safety or mutation issues.
2. Receipt/report reconstructability issues.
3. Completion invariant issues.
4. Role enforcement issues.
5. Manifest or documentation drift.
6. Cosmetic formatting.

## Non-Claims

Passing CI does not claim:

- production readiness;
- live StegID minting;
- live TV/TVC issuance;
- multi-adapter parity;
- cross-repo admissibility completion;
- org-wide governance completion.

Passing CI only supports the current local activation candidate claim.

## Governing Sentence

A StegEntity CI failure is an activation-evidence failure until proven otherwise; fixes must preserve admissible execution, refused execution, receipt evidence, outcome evidence, role enforcement, completion invariants, and manifest truth.
