# Role Context Demo Status

## Purpose

This note records the current role-context demo state.

The original legacy demo remains unchanged.

## Added Files

```text
examples/role_context_verified_receipt.json
examples/role_context_authority_token.json
```

## Current Status

The role-context receipt and authority examples have been added.

The executable role-context capsule is still pending.

## Bound Demo Hash

```text
sha256:ef94b71f15b0cbec9d304142ee3635f578a95c274f2da384a40b9d9b88bdd188
```

## Intended Role Context

```json
{
  "actor_role": "StegAgent",
  "counterparty_role": "StegEntity",
  "role_transition": "RT-004",
  "role_constraint": "execution_requires_admissibility",
  "symmetry_basis": "receipt+tvc+capsule",
  "completion_invariant_required": true
}
```

## Next Required Action

Add the matching executable capsule JSON once the repository path accepts the encoded operation content safely.

## Non-Claim

This demo is not complete until the matching executable capsule exists and validates with the role-context receipt and authority token.
