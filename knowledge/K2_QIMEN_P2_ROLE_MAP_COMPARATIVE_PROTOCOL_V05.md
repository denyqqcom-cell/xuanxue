# K2 Qimen P2 Role-Map Comparative Protocol V05

## Current state

V05 closes only the first two execution-contract blockers discovered by the V04
post-repin audit:

- `P2-EXEC-001 MACHINE_STRUCTURED_ESTIMAND_BINDING`
- `P2-EXEC-002 CANONICAL_GENERATOR_FREEZE_SHAPE`

The current state is deliberately still:

`EXECUTION_SUBSTRATE_READY = false`

`BATCH_READY = false`

`BATCH_GATE = BLOCKED_REMAINING_EXECUTION_SUBSTRATE_P2_EXEC_003_TO_009`

`BATCH = NONE / FREEZE = NONE / OUTCOME = NONE / EMPIRICAL_CREDIT = NONE`

## Why a separate P2 execution contract is used

The generic prospective-plan validator enforces an exact `PLAN_FIELDS` set for every
active design plan. Adding ad-hoc P2 keys such as `estimand_lock` or
`bridge_model_name` directly to `K2PV-QRM-002` would weaken or fork that generic registry
contract.

V05 therefore keeps `K2PV-QRM-002` generic-schema compatible and binds the extra P2
semantics in:

`knowledge/K2_QIMEN_P2_EXECUTION_CONTRACT_V01.json`

Its canonical JSON SHA-256 is:

`218bf3dbc8e83421db34d3d8678a17b93c7e1ed981d28ba70ede02c1c145264b`

The contract makes all three lanes first-class machine data and binds the exact three
estimands:

- C1: A' − A, only Role Binding may differ.
- C2: B − A', only Layer Priority may differ.
- C3: B − A, bundle only; component credit is forbidden.

This closes the serialization gap without changing QRM-H1 or rewriting the generic plan.

## Generator descriptor contract

`knowledge/schema/qimen_p2_generator_descriptor.schema.json` now defines the canonical
future descriptor shape for each lane generator: generator id, lane id, version,
implementation ref, implementation SHA-256, input/output schema SHA-256, nondeterminism
policy and seed.

Canonical descriptor hashing is fixed as:

`UTF-8 JSON -> sort_keys=true -> compact separators -> SHA-256(full descriptor object)`

A three-lane fixture verifies that this canonicalization is stable. The fixture is
explicitly test-only. Its fake implementation hashes and paths are not production
generators.

Therefore closing `P2-EXEC-002` means only that a future generator can be frozen without
ambiguous ref/version/hash/seed semantics. It does **not** close
`P2-EXEC-004 DETERMINISTIC_ROLE_LAYER_GENERATORS`.

## Future Freeze schema

`knowledge/schema/qimen_p2_execution_freeze.schema.json` binds a future production Freeze
to:

- `K2PV-QRM-002 / QRM-H1`;
- mapping-before-current-plate-values;
- exact A / A' / B lane identities;
- exact C1 / C2 / C3 estimands;
- shared representation hashes;
- equal complexity-budget fields;
- blinding/isolation fields;
- denominator/ABSTAIN policy fields;
- reproducibility fixture hash;
- `research_only=true` and `outcome_data_used=false`.

The schema is a shape contract only. No object conforming to it has been promoted as a
production Freeze.

## Remaining blockers

`P2-EXEC-003` through `P2-EXEC-009` remain open. In particular there is still no
production representation materializer, no deterministic Role/Layer generator, no budget
enforcer, no isolated blinded runner, no ABSTAIN scorer, no production reproducibility
fixture pipeline, and no P2 production Freeze serializer.

V05 cannot authorize a Batch. A later protocol version may re-evaluate execution readiness
only after those blockers close with executable machine evidence.

## Non-claims

Closing machine contracts is engineering credit, not奇门经验信用. No source claim is
promoted, no predictive result exists, and QRM-H1 remains `UNTESTED`.
