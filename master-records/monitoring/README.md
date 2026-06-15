# Master-Records Monitoring

Generated: `2026-06-14`

## Purpose

This namespace tracks ecosystem implementation posture for nodes, orgs, repos, ingestion events, governance tightness, GAX/GAB history, and receipt references.

Master-Records monitoring is not only archival. It is the observability layer for governed ecosystem implementation.

## Initial monitoring areas

```text
org-status.json
repo-status.json
node-status.json
ingestion-events/
blocked-events/
governance-overrides/
schema-adoption/
gax-history/
gab-history/
receipt-reference-index/
```

## Required observation questions

```text
Which orgs are GAX-aware?
Which repos support Governance Tightness profiles?
Which nodes can verify GABs?
Which ingestion tasks are blocked?
Why are they blocked?
Which tightness profile was active?
Which standards version was active?
Which receipt reference preserves the decision?
```

## Monitoring principle

A blocked task is not only a failure. It is a governed state transition that should be observable, recorded, and later re-evaluated when policy, evidence, or governance tightness changes.
