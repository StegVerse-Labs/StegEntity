# ACTIVATION_STATUS

## Current Status

```text
Activation candidate: local governed runtime module
```

StegEntity currently has enough evidence to be run as a governed local runtime module.

This is not a production-complete claim.

Machine-readable status is available in `activation_manifest.json`.

## Activation Evidence

Current activation evidence includes:

- local Python runtime;
- local filesystem adapter;
- maintenance capsule validation;
- verified receipt consumption;
- authority token consumption;
- dry-run path;
- successful apply path;
- execution receipt emission;
- outcome report emission;
- first-class completion invariant output;
- refused apply path;
- refusal receipt emission;
- blocked outcome report emission;
- CI activation check.

## Activation Command

```bash
python tools/check_repo_activation.py
```

The activation command verifies that completion invariant output is present, satisfied, and identical across the apply return value, execution receipt, and persisted apply report.

For operator steps and failure interpretation, see `docs/STEGENTITY_LOCAL_ACTIVATION_RUNBOOK.md`.

For CI failure interpretation, see `docs/STEGENTITY_CI_FAILURE_GUIDE.md`.

## Current Non-Claims

This status does not claim:

- production deployment readiness;
- live TV/TVC issuance;
- live StegID minting;
- multi-adapter readiness;
- full org-wide governance completion;
- cross-repo admissibility completion.

## Linked Documents

- `README.md`
- `activation_manifest.json`
- `docs/STEGENTITY_ACTIVATION.md`
- `docs/STEGENTITY_ACTIVATION_GAP_LIST.md`
- `docs/STEGENTITY_LOCAL_ACTIVATION_RUNBOOK.md`
- `docs/STEGENTITY_CI_FAILURE_GUIDE.md`
- `docs/STEGENTITY_ROLE_TRANSITION_POLICY.md`
- `docs/STEGENTITY_VERIFICATION.md`

## Governing Sentence

StegEntity activation status must remain evidence-bound: local activation may be claimed only when admissible and refused transition paths are both reproducible, receipt-bearing, outcome-reportable, and completion-invariant checked without claiming production completion.
