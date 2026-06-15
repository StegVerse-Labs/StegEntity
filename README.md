# StegEntity

StegEntity is the platform-agnostic runtime environment for governed AI entities in the StegVerse ecosystem.

It hosts and constrains AI-role expressions including:

- `StegBot`
- `StegAgent`
- `StegEntity`
- `StegVerseAI`
- `UserAI`

StegEntity does **not** assume GitHub as the execution authority. GitHub is only one possible adapter.

The runtime exists to inspect state, evaluate proposed transitions, request or validate scoped authority, apply admissible maintenance capsules through adapters, verify outcomes, and emit receipts.

## Core Thesis

A StegEntity may not mutate state merely because it can.

It may mutate state only when:

1. The acting entity has a valid StegID-style verified receipt.
2. Required authority is released through a TVC-style authority token.
3. The proposed transition is captured in a maintenance capsule.
4. The capsule declares dependencies, consequences, rollback, and verification requirements.
5. The ingestion/admissibility decision is `ALLOW`.
6. The selected adapter applies the transition.
7. The result is verified.
8. Receipts are emitted.

## What This Repo Provides Now

This repository is a working runtime, not a scaffold.

It includes:

- A complete StegEntity Python runtime.
- A working local filesystem adapter.
- A maintenance capsule validator.
- TVC-style authority token validation.
- StegID-style verified receipt consumption.
- Safe path enforcement.
- Dry-run execution.
- Apply execution.
- Hash verification.
- Rollback material capture.
- Execution receipt generation.
- Outcome report generation.
- Blocked apply outcome reporting without mutation.
- Non-execution `blocked_apply` receipt artifacts for refused apply attempts.
- A complete demo capsule.
- A complete local demo runner.
- Role symmetry doctrine.
- Role transition enforcement policy.
- Repo activation doctrine.
- Optional role context parsing and preservation.
- Warning-only role context validation.
- Apply-time required role context enforcement.
- Apply-time blocking for unknown role transitions.
- Apply-time blocking for invalid completion invariant type.
- Visible `role_enforcement` runtime outputs.
- Execution receipts that preserve apply-time `role_enforcement`.
- Local repo activation check command.
- A reproducible role-context demo fixture builder.
- A generated role-context fixture verifier.
- A role-context demo verification script.
- Built-in unit tests using Python standard library only.
- A GitHub Actions verification workflow.

No external Python packages are required.

## What This Repo Does Not Do Yet

This repo does not issue TV/TVC tokens. It consumes TVC-style authority tokens so that the runtime can be integrated with TV/TVC once token issuance is finished.

This repo does not mint StegID receipts. It consumes StegID-style verified receipt JSON so that the runtime can be integrated with StegID receipt minting and verification.

This repo does not yet fully enforce role transitions across all runtime modes. It preserves role context, emits warning-only findings for validate and dry-run, requires complete role context at apply time, writes refused apply outcome reports without mutation, emits non-execution refusal receipts, emits visible role enforcement posture in runtime outputs, and preserves apply-time role enforcement posture in execution receipts.

## Quick Start

From the repo root:

```bash
python tools/run_demo.py
```

Expected result:

```text
demo_target/hello.txt
demo_target/stegentity_receipts/
demo_target/stegentity_reports/
```

Run tests:

```bash
python -m unittest discover tests
```

Run the role-context demo checks:

```bash
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python tools/check_role_context_demo.py
```

Run the local activation check:

```bash
python tools/check_repo_activation.py
```

For activation scope, see `docs/STEGENTITY_ACTIVATION.md`.

For the full verification path, see `docs/STEGENTITY_VERIFICATION.md`.

## CLI

Validate structurally:

```bash
python -m src.stegentity.cli validate examples/local_file_replacement_capsule.json
```

Dry run:

```bash
python -m src.stegentity.cli dry-run examples/local_file_replacement_capsule.json --root demo_target --receipt examples/verified_receipt.json --authority examples/authority_token.json
```

Apply:

```bash
python -m src.stegentity.cli apply examples/local_file_replacement_capsule.json --root demo_target --receipt examples/verified_receipt.json --authority examples/authority_token.json
```

## Runtime Flow

```text
maintenance capsule
  ↓
schema and semantic validation
  ↓
StegID-style receipt validation
  ↓
TVC-style authority token validation
  ↓
transition/admissibility decision check
  ↓
adapter selection
  ↓
dry-run or apply
  ↓
post-write hash verification
  ↓
receipt emission
  ↓
outcome report
```

## Role Model

### StegBot

A task automation role.

### StegAgent

A reasoning, proposal, and review role.

### StegEntity

A governed executable entity role.

### StegVerseAI

The StegVerse-side counterpart intelligence.

### UserAI

A user-bound delegated intelligence.

All roles must operate through StegID identity, TV/TVC scoped authority, maintenance capsules, adapters, receipts, and verification.

For symmetrical role constraints, see `docs/STEGENTITY_ROLE_SYMMETRY.md`.

For role field schema notes, see `docs/STEGENTITY_ROLE_FIELD_SCHEMA.md`.

For role transition enforcement policy, see `docs/STEGENTITY_ROLE_TRANSITION_POLICY.md`.

For activation scope, see `docs/STEGENTITY_ACTIVATION.md`.

## Relationship to StegID

StegID is the identity and receipt authority layer.

StegEntity expects a verified receipt containing:

```text
receipt_id
actor_class
scopes
issued_at
expires_at
assurance_level
issuer
kid
payload_hash
sig
```

For v0, StegEntity validates the structure, time bounds, required scopes, and expected payload hash. Cryptographic receipt verification remains owned by StegID.

## Relationship to TV/TVC

TV/TVC is the scoped authority release layer.

StegEntity expects a TVC-style authority token containing:

```text
token_id
status
adapter
target
scopes
issued_at
expires_at
capsule_hash
receipt_hash
```

For v0, StegEntity validates token structure, time bounds, adapter, target, required scopes, and capsule hash. Token issuance and revocation remain owned by TV/TVC.

## Verification

Local verification:

```bash
python tools/build_role_context_demo.py
python tools/verify_generated_role_context_demo.py
python -m unittest discover tests
python tools/check_role_context_demo.py
python tools/check_repo_activation.py
```

Automated verification is declared in:

```text
.github/workflows/stegentity-verify.yml
```

## Critical Invariant

Platform events are not StegVerse completion events.

A transition is complete only when:

```text
target state changed as authorized
destination hash matches expected hash
receipt emitted
outcome report written
state is reconstructable
```
