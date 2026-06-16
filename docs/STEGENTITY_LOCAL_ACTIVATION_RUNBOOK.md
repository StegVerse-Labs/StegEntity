# STEGENTITY_LOCAL_ACTIVATION_RUNBOOK

## Purpose

This runbook gives an operator-facing procedure for verifying local StegEntity activation.

It is designed for repeatable local checks and CI parity.

It does not claim production deployment readiness.

## Preconditions

From the repository root, use Python 3.11 or later.

No external Python packages are required.

## Full Local Verification

Run:

```bash
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python -m unittest discover tests
python tools/check_role_context_demo.py
python tools/check_repo_activation.py
```

Expected result:

```text
all commands exit 0
```

## Activation Command

Run:

```bash
python tools/check_repo_activation.py
```

Expected top-level result:

```json
{
  "status": "ok",
  "activation_check": "local_stegentity_runtime"
}
```

The command prints a JSON object with success-path and refusal-path evidence.

## Success Path Evidence

The success path must show:

- validation succeeded;
- dry-run succeeded;
- apply succeeded;
- target state was written;
- execution receipt was emitted;
- apply report was emitted;
- completion invariant was satisfied.

Expected success-path fields include:

```json
{
  "target_written": true,
  "execution_receipt": "role-context-demo.execution_receipt.json",
  "apply_report": "role-context-demo.apply.outcome.json",
  "completion_invariant_satisfied": true
}
```

## Refusal Path Evidence

The refusal path must show:

- apply was refused before mutation;
- target state was not written;
- non-execution refusal receipt was emitted;
- execution receipt was not emitted;
- blocked outcome report was emitted;
- blocked outcome report is hash-bound to the refusal receipt.

Expected refusal-path fields include:

```json
{
  "target_written": false,
  "refusal_receipt": "role-context-demo.blocked_apply_receipt.json",
  "blocked_report": "role-context-demo.apply.blocked.outcome.json"
}
```

## Failure Interpretation

| Failure | Meaning |
|---|---|
| validation failed | capsule, receipt, or authority object is not internally admissible |
| dry run failed | local adapter cannot simulate transition safely |
| target file missing after apply | mutation did not occur when apply was admissible |
| execution receipt missing | successful mutation was not receipt-bearing |
| apply outcome report missing | successful mutation was not reportable |
| completion invariant missing | completion was not exposed as first-class evidence |
| completion invariant not satisfied | written state does not satisfy declared expected hash evidence |
| refused apply unexpectedly succeeded | precondition enforcement failed |
| target file was written during refusal | refusal path mutated state and is invalid |
| refusal receipt missing | refusal was not receipt-bearing |
| execution receipt emitted during refusal | refusal incorrectly masqueraded as execution |
| blocked outcome report missing | refusal was not reportable |
| blocked outcome not bound to refusal receipt | refusal evidence is not reconstructably linked |

## Current Activation Claim

If the full local verification succeeds, the repo may claim:

```text
Activation candidate: local governed runtime module
```

This means StegEntity can locally demonstrate:

- admissible mutation;
- refused mutation;
- execution receipts;
- refusal receipts;
- outcome reports;
- role enforcement posture;
- completion invariant evidence.

## Current Non-Claims

Successful local activation does not claim:

- production deployment readiness;
- live StegID minting;
- live TV/TVC issuance;
- multi-adapter parity;
- cross-repo admissibility completion;
- org-wide governance completion.

## CI Parity

The GitHub Actions workflow runs the same activation command:

```text
.github/workflows/stegentity-verify.yml
```

The CI path is expected to fail if local activation evidence is missing, inconsistent, or no longer reproducible.

## Governing Sentence

A local activation run is valid only when admissible execution and refused execution are both reconstructable, receipt-bearing, outcome-reportable, role-enforced, and completion-invariant checked.
