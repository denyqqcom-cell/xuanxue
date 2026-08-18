# K2B Wave1 Execution Refactor

## Status

K2B remains `WAVE1_OPEN` and Claim Extraction remains blocked.

This document records an execution-architecture failure without converting failed attempts into reading credit.

## Failed execution model

The first operational attempt delegated whole-domain / whole-source reading to parallel local sub-agents.

Observed failures:

1. the local vision backend returned HTTP 401 / `User not found`, so SCAN sources could not be visually verified;
2. delegated agents had a 600-second hard execution limit, which was too short for complete 254–300 page books and much larger domain bundles;
3. six whole-domain dispatches plus seven single-source retries all timed out without accepted complete output;
4. one Liuren attempt produced 34 provenance-valid candidate Evidence rows before timeout. They remain local candidates only and must be re-reviewed by the project-side main agent before public reuse.

No failed dispatch is counted as COMPLETE reading coverage.

## Accepted replacement architecture

The project-side main agent owns all engineering and final knowledge normalization.

Wave1 is split mechanically by source readability:

- `TEXT_DIRECT`: existing real text layer can be extracted page-by-page by project-owned tooling and reviewed by the project-side main agent;
- `VISUAL_REQUIRED`: SCAN/OCR_WEAK/OCR_FAIL requires original-page visual verification; while the vision backend is unavailable these sources remain honestly BLOCKED;
- `ACCESS_REVIEW`: any other unresolved access state remains blocked until explicitly resolved.

The local AI is reduced to an execution helper. It may fetch/pull, run project-owned tools/tests, locate local source files, and expose requested page packets. It does not edit tracked files, normalize Evidence, commit, push, or decide acceptance.

## Wave1 accounting baseline

At this refactor point the official Wave1 planner is expected to produce 37 unique-coverage reading units:

- TEXT_DIRECT: 22
- VISUAL_REQUIRED: 15
- ACCESS_REVIEW: 0

These counts are now machine-checked against `knowledge/K2_EVIDENCE_STATE.json`; drift fails the K2 Evidence validator.

## Local page packets

`tools/build_k2_local_page_packets.py` is the only project-owned helper for bulk text-layer exposure in this refactor.

It is deliberately non-semantic:

- no Evidence extraction;
- no Claim synthesis;
- no topic ranking;
- no school resolution;
- no OCR substitution for required vision.

Raw page text stays outside the repository under local `knowledge-intake` storage and may contain copyrighted source text.

## Acceptance consequence

A Wave1 ledger may legitimately contain both COMPLETE and BLOCKED rows.

A source is COMPLETE only if its required verification lane is satisfied. A blocked visual source emits zero Evidence and remains an explicit future obligation rather than being silently dropped.
