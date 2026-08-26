# K2 Claim Extraction Readiness Protocol

## Purpose

This gate answers one question only: **is K2 Evidence Extraction complete enough to submit a project-level review for the next phase?**

It does **not** authorize Claim Extraction by itself.

The machine state therefore has only two readiness statuses:

- `CLOSED`
- `READY_FOR_PROJECT_REVIEW`

and always keeps:

- `claim_extraction_authorized = false`
- `transition_policy = PROJECT_REVIEW_REQUIRED_V1_NEVER_AUTO_OPENS`

A future phase change requires a separate project review and a separate state transition commit.

## Why this gate exists

Earlier K2 work exposed a recurrent failure mode: a local sub-gate can be green while the global evidence phase is still incomplete. That is especially dangerous when the project has already accumulated strong-looking distillates, source stance rows, or QCIC inference artifacts.

The readiness gate prevents a local success from being mistaken for global methodological maturity.

It checks the global Evidence state, the machine-materialized semantic-UNKNOWN discovery backlog, domain consistency, and current QCIC materialization before the project may even be reviewed for phase transition.

## Inputs

The generated snapshot is derived only from tracked project state:

- `knowledge/PROJECT_STATE.json`
- `knowledge/K2_EVIDENCE_STATE.json`
- `knowledge/K2_QCIC_INFERENCE_ELIGIBILITY_VIEW.json`
- `knowledge/K2_UNKNOWN_TEXTUAL_BACKLOG.json`

The UNKNOWN-backlog snapshot is itself regenerated from all canonical K1 source rows plus the reviewed K2 semantic-discovery overlay. The readiness gate verifies that materialization is current instead of trusting a manually typed backlog integer.

No private PDF text, local path, or untracked helper artifact is an input.

## Automated prerequisites

The current v1 gate requires all of the following before it can return `READY_FOR_PROJECT_REVIEW`:

1. `K2_EVIDENCE_STATE.status == COMPLETE`;
2. generated remaining semantic-UNKNOWN textual backlog equals zero;
3. the UNKNOWN-backlog materialization is current;
4. `K2_EVIDENCE_STATE.unknown_textual_resolution_backlog` exactly equals the generated remaining backlog;
5. the Evidence state itself no longer blocks Claim Extraction;
6. the project is not globally K2-blocked;
7. Evidence Extraction is not blocked;
8. project and Evidence required-domain sets are consistent;
9. the QCIC downstream eligibility view exactly matches its current registries and gate state.

Any failed prerequisite produces a stable blocker code and keeps the gate `CLOSED`.

## Current expected state

At the time this protocol is updated, three fully reviewed raw-UNKNOWN Qimen sources have been resolved through the K2 semantic-discovery routing overlay. The machine backlog therefore moves from 96 to 93.

K2B is still open, so the correct readiness result remains `CLOSED` with the substantive blockers:

- `K2_EVIDENCE_STATE_NOT_COMPLETE`
- `UNKNOWN_TEXTUAL_BACKLOG_REMAINS`
- `EVIDENCE_STATE_BLOCKS_CLAIM_EXTRACTION`

That is not a failure of the gate. It is the gate correctly preserving the phase boundary while still recognizing genuine backlog reduction.

## Claim Extraction is not empirical validation

Claim Extraction and empirical validation are separate paths.

A future Claim row may represent what a source states, rejects, qualifies, or supports within a defined method layer. That does not give the Claim real-world empirical credit.

The readiness snapshot therefore fixes:

`empirical_credit_path_separate = true`

Prospective validation continues to govern empirical testing. Source-derived Claim Extraction must not bypass that system.

## QCIC relationship

QCIC v0.6 materializes whether reviewed source-stance and enumeration units are eligible for downstream inference. The Claim readiness gate consumes only the **currentness and accounting** of that materialization.

It does not require a positive number of QCIC `claim_eligible` units, because the project-level Claim phase is broader than the current QCIC registry subset. Conversely, a positive QCIC eligibility count would not be sufficient to open Claim Extraction while K2B remains globally incomplete.

## Fail-closed rules

The gate must remain closed when any of the following is true:

- Evidence state is not globally complete;
- semantic-UNKNOWN textual backlog remains;
- UNKNOWN-backlog materialization is stale;
- Evidence-state backlog accounting drifts from the generated backlog;
- Evidence state still blocks Claim Extraction;
- required-domain accounting drifts;
- QCIC eligibility materialization is stale or invalid;
- the generated readiness snapshot is stale;
- the readiness artifact attempts to set `claim_extraction_authorized = true`.

## Transition rule

`READY_FOR_PROJECT_REVIEW` means only that automated prerequisites are satisfied.

It does not mutate `PROJECT_STATE.phase`, does not change `claim_extraction_blocked`, and does not create Claim records.

Only an explicit project review may approve a later transition from `K2_EVIDENCE_EXTRACTION` to `K2_CLAIM_EXTRACTION`.
