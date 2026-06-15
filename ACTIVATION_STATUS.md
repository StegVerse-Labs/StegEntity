# ACTIVATION_STATUS

## Current Status

```text
Activation candidate: local governed runtime module
```

StegEntity currently has enough evidence to be run as a governed local runtime module.

This is not a production-complete claim.

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
- refused apply path;
- refusal receipt emission;
- blocked outcome report emission;
- CI activation check.

## Activation Command

```bash
python tools/check_repo_activation.py
```

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
- `docs/STEGENTITY_ACTIVATION.md`
- `docs/STEGENTITY_ACTIVATION_GAP_LIST.md`
- `docs/STEGENTITY_ROLE_TRANSITION_POLICY.md`
- `docs/STEGENTITY_VERIFICATION.md`

## Governing Sentence

StegEntity activation status must remain evidence-bound: local activation may be claimed only when admissible and refused transition paths are both reproducible, receipt-bearing, and outcome-reportable without claiming production completion.
