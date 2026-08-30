# K2 Qimen P2 Role-Map Comparative Protocol V04

## Current authority

`K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V04`

Status: `POST_REPIN_AUDITED_EXECUTION_BLOCKED`.

V04 does not alter the QRM-H1 theory or the A / A' / B comparison semantics introduced in
V02. It records the result of the required post-repin audit after V03 repinned the active
plan to `K2PV-QRM-002`.

The current machine state is:

`DESIGN_READY != EXECUTION_READY != BATCH_READY`

`EXECUTION_SUBSTRATE_READY = false`

`BATCH_GATE = BLOCKED_MISSING_EXECUTION_SUBSTRATE`

`BATCH = NONE / FREEZE = NONE / OUTCOME = NONE / EMPIRICAL_CREDIT = NONE`

## Lineage

- V02 remains the authority for the adversarially hardened experiment semantics.
- V03 remains the immutable historical record of plan repinning and the requirement for a
  post-repin audit.
- V04 is the current execution-readiness authority.
- `K2_QIMEN_P2_ROLE_MAP_POST_REPIN_AUDIT_V01.json` is the machine audit result.

## Gate

Nine `P2-EXEC-*` blockers are open. They cover machine-structured estimands, canonical
generator descriptors, representation materialization, deterministic mapping,
complexity-budget enforcement, blinding/isolation, denominator scoring, exact
reproducibility, and P2-specific Freeze serialization.

All nine must close with executable evidence before another protocol version may even
consider setting `execution_substrate_ready=true`.

V04 itself can never authorize a Batch.

## Non-claims

This protocol does not validate QRM-H1. It does not upgrade source credit, method credit,
or empirical credit. It does not create a prospective case, Batch, Freeze, prediction, or
Outcome. CI success is contract evidence only.
