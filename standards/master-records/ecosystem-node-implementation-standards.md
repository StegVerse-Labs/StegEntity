# Master-Records: Ecosystem Node Implementation Standards

Generated: `2026-06-14`

## Purpose

This record establishes the current ecosystem-wide implementation standards for nodes, orgs, and repos before cross-org ingestion expands.

The Master-Records node should treat this as the controlling standards note for early ecosystem-wide node implementation until a dedicated Master-Records repository or registry supersedes it.

## Current standard objects

| Standard | Role |
|---|---|
| Governed Admissibility Bundle | Portable governance artifact containing packet, result, reference, optional execution receipt, and hashes. |
| Governed Admissibility Exchange | Site/SDK import-export wrapper around a valid bundle. |
| Governance Tightness Profile | Sliding-scale control for ingestion posture. |
| Dynamic Admissibility Packet | Discipline-aware input shape used by Site, SDK, LLM bridge, math bridge, and ingestion. |
| Admissibility Receipt Reference | Local stable reference to an evaluated admissibility result. |
| Bundle Check | Local re-evaluation and posture/hash comparison for a bundle. |

## Governance tightness nomenclature

```text
0-20    observe
21-40   assist
41-60   balanced
61-80   strict
81-100  fail_closed
```

Supported input forms:

```text
observe
assist
balanced
strict
fail_closed
numeric scale 0-100
{"scale": 55}
{"label": "strict"}
```

## Cross-org and cross-repo ingestion rule

Every cross-org or cross-repo ingestion task should carry a governance tightness profile.

The profile determines whether a task may move automatically, requires receipt, requires replay, requires human review, or routes fail-closed.

Lower tightness permits more automated movement.

Higher tightness requires more receipts, replay, and review before writes.

The strictest posture routes fail-closed by default.

## Required packet fields for ecosystem ingestion

A cross-org or cross-repo ingestion packet should include:

```text
schema
source_org
source_repo
target_org
target_repo
task
intent
proposed_files
governance_tightness
admissibility_bundle or gax_exchange
```

## Node implementation expectation

Each node should be able to:

1. Receive a task packet.
2. Resolve governance tightness.
3. Verify GAX if present.
4. Verify GAB if present.
5. Run bundle check when a bundle is present.
6. Refuse mutation when required posture is missing.
7. Emit a receipt reference for the evaluated task.
8. Preserve enough metadata for Master-Records reconstruction.

## Master-Records responsibility

The Master-Records node should track:

```text
standard versions
schema names
repo implementation status
org implementation status
node compatibility
blocked ingestion events
tightness overrides
receipt references
GAX/GAB exchange history
```

## Initial standards source

The current standards implementation exists in:

```text
StegVerse-org/StegVerse-SDK
```

Primary files:

```text
stegverse/governance_tightness.py
schemas/admissibility/governance-tightness.schema.json
stegverse/admissibility_bundle.py
stegverse/admissibility_exchange.py
stegverse/admissibility_replay.py
stegverse/admissibility_receipts.py
```

## Next implementation phase

The next phase should create ingestible task packets for cross-org and cross-repo updates so ecosystem changes are routed through governed ingestion rather than direct per-repo edits.
