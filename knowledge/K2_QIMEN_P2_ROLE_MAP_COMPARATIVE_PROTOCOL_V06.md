# K2 Qimen P2 Role-Map Comparative Protocol V06

## Current state

V06 closes exactly one additional execution blocker beyond V05:

- `P2-EXEC-003 REPRESENTATION_MANIFEST_MATERIALIZER`

The closure is narrow. It establishes an executable deterministic materializer that accepts one shared representation source and binds the same five representation components to all three lanes:

- world-variable manifest;
- symbol vocabulary;
- feature-extraction manifest;
- eligible-rule pool;
- prediction schema.

Each component is canonically serialized with `UTF8_JSON_SORT_KEYS_COMPACT`, hashed with SHA-256, and then bound into one shared representation identity. `P2-A`, `P2-A_PRIME`, and `P2-B` must carry the identical component-hash map and shared representation hash.

## Fail-first evidence

The fail-first commit was:

`caa9a4ab1863ee8e29cdecfc6c0404b22c8e3572`

`K2 Qimen P2 Execution Readiness #3` first passed the existing 14 execution-contract negative cases, then failed exactly at the new representation test because the production materializer did not yet exist:

`ModuleNotFoundError: No module named 'k2_qimen_p2_materialize_representation'`

The implementation commit therefore closes a demonstrated missing capability rather than declaring readiness from prose alone.

## Machine authority

Representation contract:

`knowledge/K2_QIMEN_P2_REPRESENTATION_CONTRACT_V01.json`

Canonical SHA-256:

`1a7128dd4c1ba5846c1d74f78645ff7b1ea87032898bbd83f61859283182393d`

Materializer:

`tools/k2_qimen_p2_materialize_representation.py`

The materializer rejects missing or extra top-level source fields and validates the generated lane bindings before returning or writing output. The test suite also mutates lane-specific hashes, lane cardinality, the combined representation hash, missing source components, and attempted top-level lane overrides; all must fail closed.

## What V06 does not close

The state remains deliberately incomplete:

`EXECUTION_SUBSTRATE_READY = false`

`BATCH_READY = false`

`BATCH = NONE`

`FREEZE = NONE`

`OUTCOME = NONE`

`EMPIRICAL_CREDIT = NONE`

The following blockers remain open:

- `P2-EXEC-004` deterministic Role/Layer generators;
- `P2-EXEC-005` complexity-budget enforcement;
- `P2-EXEC-006` blinding and cross-lane isolation runner;
- `P2-EXEC-007` ABSTAIN/denominator scorer;
- `P2-EXEC-008` exact reproducibility fixture pipeline;
- `P2-EXEC-009` P2 Freeze serializer.

Representation parity machinery does not implement Role Binding or Layer Priority, does not create a production Freeze, and does not validate QRM-H1. Claim Extraction remains blocked.
