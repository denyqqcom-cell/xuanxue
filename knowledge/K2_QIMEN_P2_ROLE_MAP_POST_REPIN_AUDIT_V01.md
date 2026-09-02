# K2 Qimen P2 Role-Map Post-Repin Audit V01

## Verdict

This audit is executed at `PRE_BATCH_PRE_FREEZE_PRE_OUTCOME` against parent head
`e4aed3c5cb2d40ee89f9a5e314234cafec62fef7`.

The result is:

- `POST_REPIN_COMPLETE_EXECUTION_BLOCKED`
- `ACTIVE_PLAN = K2PV-QRM-002`
- `QRM-H1 = UNTESTED`
- `EXECUTION_SUBSTRATE_READY = false`
- `BATCH_READY = false`
- `BATCH_GATE = BLOCKED_MISSING_EXECUTION_SUBSTRATE`
- `BATCH = NONE`
- `FREEZE = NONE`
- `OUTCOME = NONE`
- `EMPIRICAL_CREDIT = NONE`
- `CLAIM_EXTRACTION = BLOCKED`

The important correction is that a green protocol validator proves that the contract is
internally consistent. It does **not** prove that the three-lane experiment can actually
be executed without leakage or asymmetry.

## What passed

`K2PV-QRM-002` correctly repins the prospective plan to `P2-ROLE-MAP-v0.2` and carries
the V02 future-freeze field names. It also preserves the intended conceptual contrasts in
prose:

- `P2-C1`: A' vs A, Role Binding only.
- `P2-C2`: B vs A', Layer Priority only.
- `P2-C3`: B vs A, bundle only and not component attribution.

This is enough to close the **plan-field repin** problem. It is not enough to execute a
Batch.

## New finding: plan serialization is still weaker than the protocol

The active plan does not contain a machine-structured `estimand_lock` object and does not
bind `bridge_model_name` as a first-class plan field. The three-lane meaning survives in
human-readable controls, but a future generic serializer could still lose A' or construct
the contrasts incorrectly unless a P2-specific schema rejects that state.

Therefore `P2-EXEC-001` remains open. This is not a change to the hypothesis. It is a
machine-binding defect between the protocol and a future Freeze.

## Execution blockers

Nine blockers are now explicit:

1. `P2-EXEC-001 MACHINE_STRUCTURED_ESTIMAND_BINDING`
   The exact A / A' / B graph and C1 / C2 / C3 single-difference contract are not yet
   machine-bound in a P2 execution schema.
2. `P2-EXEC-002 CANONICAL_GENERATOR_FREEZE_SHAPE`
   V02 requires versioned and hashed generators, but ref/version/hash/seed serialization
   is not yet canonical.
3. `P2-EXEC-003 REPRESENTATION_MANIFEST_MATERIALIZER`
   Shared world-variable, symbol, feature, rule and prediction manifests are policy only.
4. `P2-EXEC-004 DETERMINISTIC_ROLE_LAYER_GENERATORS`
   No executable A/A'/B Role/Layer mapping generator interface is registered.
5. `P2-EXEC-005 COMPLEXITY_BUDGET_ENFORCEMENT`
   Equal role multiplicity, branch, rule-trace, information and tool budgets are not
   machine-enforced.
6. `P2-EXEC-006 BLINDING_AND_CROSS_LANE_ISOLATION_RUNNER`
   Neutral labels, frozen lane order and isolation exist as requirements but not as an
   execution runner.
7. `P2-EXEC-007 ABSTAIN_DENOMINATOR_SCORER`
   No P2-specific scorer currently prevents ABSTAIN from silently shrinking the
   denominator and calculates the coverage-penalized metric.
8. `P2-EXEC-008 EXACT_REPRODUCIBILITY_FIXTURE_PIPELINE`
   `reproducibility_fixture_hash` is a future Freeze field, not yet a generated replayable
   artifact.
9. `P2-EXEC-009 P2_FREEZE_SERIALIZER`
   The generic Batch manifest binder can bind canonical JSON and basic Batch identity, but
   it does not enforce all P2 parity, generator, blinding, denominator, or pre-plate-value
   mapping invariants.

## Why the generic Batch binder is not enough

`tools/validate_k2_batch_manifest_bindings.py` is useful shared infrastructure. It checks
canonical manifest hashing, plan/model identity, `research_only=true`,
`outcome_data_used=false`, and path hygiene. It is deliberately recorded as
`PARTIAL_REUSE_ONLY`.

Promoting that generic binder to P2 execution evidence would be a category error: it does
not know what A', `P2-C1`, equal complexity budgets, lane isolation, or mapping-before-
plate-value access mean.

## Closure discipline

Every blocker requires executable machine evidence. A blocker cannot be closed because a
document says that the control exists. Once all nine blockers are closed, a **new**
protocol version must re-evaluate `execution_substrate_ready` and `batch_ready`; V04 must
not be edited into a success state.

No Outcome may be read while closing these blockers. No Batch may be preregistered from
this V04 state.

## Self-correction

The earlier mental model was:

`protocol complete -> plan repinned -> post-repin audit -> Batch-ready`

The corrected model is:

`protocol semantics -> plan serialization -> executable substrate -> reproducibility /
isolation proof -> Batch preregistration -> prospective Freeze -> Outcome`

That extra execution layer is essential. Without it, "freeze before plate values" and
"same budget across lanes" remain intentions rather than falsifiable controls.
