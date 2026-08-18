# K2B Wave1 Execution Refactor

## Status

K2B remains `WAVE1_OPEN` and Claim Extraction remains blocked.

This document records execution failures without converting them into reading credit.

## Failed execution model

The first operational attempt delegated whole-domain / whole-source reading to parallel local sub-agents.

Observed failures:

1. the local vision backend returned HTTP 401 / `User not found`, so SCAN sources could not be visually verified;
2. delegated agents had a 600-second hard execution limit, which was too short for complete 254–300 page books and larger domain bundles;
3. six whole-domain dispatches plus seven single-source retries all timed out without accepted complete output;
4. one Liuren attempt produced 34 provenance-valid candidate Evidence rows before timeout, but that local artifact is no longer available on the current Windows helper machine and is therefore not a Wave1 dependency.

No failed dispatch is counted as COMPLETE reading coverage.

## Windows helper report: second execution failure

A later Windows helper run successfully reproduced the official planner result (`37 = 22 TEXT_DIRECT + 15 VISUAL_REQUIRED`) and kept the worktree clean, but page-packet construction returned `ready=0 / blocked=37 / FILE_MISSING=37`.

The cause was architectural: the helper machine did not contain the original Linux private K1 intake registry (`/home/joe/knowledge-intake/*/sources.jsonl`), so the earlier builder could not resolve `source_id -> local_path` and never reached the canonical byte identity check.

The same run also exposed two environment-specific issues:

- a POSIX-only `Path.__str__` assertion in `test_k2_evidence.py` failed on Windows;
- local Gradle could not start because the helper machine had no Java/JDK.

None of these failures grants reading credit. They are execution-environment findings only.

## Accepted replacement architecture

The project-side main agent owns all engineering and final knowledge normalization.

Wave1 is split mechanically by source readability:

- `TEXT_DIRECT`: existing real text layer can be extracted page-by-page by project-owned tooling and reviewed by the project-side main agent;
- `VISUAL_REQUIRED`: SCAN/OCR_WEAK/OCR_FAIL requires original-page visual verification; while the vision backend is unavailable these sources remain honestly BLOCKED;
- `ACCESS_REVIEW`: any other unresolved access state remains blocked until explicitly resolved.

The local AI is an execution helper only. It may fetch/pull, run project-owned tools/tests, locate canonical local source bytes, and expose requested page packets. It does not edit tracked files, normalize Evidence, commit, push, or decide acceptance.

## Wave1 accounting baseline

The official Wave1 planner produces 37 unique-coverage reading units:

- TEXT_DIRECT: 22
- VISUAL_REQUIRED: 15
- ACCESS_REVIEW: 0

These counts are machine-checked against `knowledge/K2_EVIDENCE_STATE.json`; drift fails the K2 Evidence validator.

## Portable canonical source resolution

The original Linux private intake path `/home/joe/knowledge-intake` is not present on the current Windows helper machine. That is an environment relocation, not a reason to rebuild or falsify K1 metadata.

`tools/build_k2_local_page_packets.py` therefore supports two resolution modes:

1. `PRIVATE_REGISTRY` — optional fast path when a private K1 `sources.jsonl` with `local_path` is available;
2. `CANONICAL_SHA256_SEARCH` — scan explicitly supplied local corpus roots and accept a file only when its actual SHA256 equals the official canonical `file_sha256` carried in the Wave1 plan.

Canonical SHA256 is the identity authority. Filename similarity is never sufficient. Archives and build trees are excluded from discovery so the fallback does not hash unrelated multi-GB artifacts.

This makes the page-packet bridge portable across Linux/WSL/Windows without weakening provenance.

## Local page packets

`tools/build_k2_local_page_packets.py` is the project-owned helper for bulk text-layer exposure.

For READY text packets it records:

- canonical `source_file_sha256`;
- `identity_mode`;
- page-preserving extracted text;
- per-page `text_sha256` and `char_count`;
- complete `packet_sha256`.

`tools/show_k2_page_packet.py` is a read-only verified slice tool. It revalidates packet/page hashes and exposes at most 25 pages per call for project-side review.

The helpers are deliberately non-semantic:

- no Evidence extraction;
- no Claim synthesis;
- no topic ranking;
- no school resolution;
- no OCR substitution for required vision.

Raw page text stays outside the repository under local `knowledge-intake` storage and may contain copyrighted source text.

## Environment-specific tests

The Windows path-separator failure is now fixed in project code: path normalization is host-aware and tests compare `Path.as_posix()` rather than assuming POSIX `Path.__str__` output.

GitHub Actions now contains a dedicated `windows-latest` K2 helper portability job so this class of bug is tested by the project rather than delegated to the local helper.

A missing local JDK is not a helper-side engineering failure. The local helper reports `SKIP_ENV_NO_JDK`; the authoritative stable-core regression remains GitHub Actions with JDK 17.

## Liuren candidate policy

The missing 34-row Liuren candidate artifact is no longer an input dependency. It must not be reconstructed from memory. Liuren Evidence will be re-extracted from verified canonical page packets.

## Acceptance consequence

A Wave1 ledger may legitimately contain both COMPLETE and BLOCKED rows.

A source is COMPLETE only if its required verification lane is satisfied. A blocked visual source emits zero Evidence and remains an explicit future obligation rather than being silently dropped.
