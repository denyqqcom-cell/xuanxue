# K1 Source Registry — project-side acceptance

Acceptance date: 2026-08-15

Evidence available to project-side reviewer: user-provided `K1_MASTER_REPORT.md` summary and per-domain summary/self-audit results. The raw local-only files under `/home/joe/knowledge-intake/` are **not directly accessible to GitHub CI or this repository**, therefore this document is a **REPORT_LEVEL_REVIEW**, not machine verification of the local files.

## Verdict

`K1 = CONDITIONAL / NOT YET CLOSED`

K2 Claim Extraction remains blocked until the local intake passes the repository-side machine contract in `tools/validate_k1_intake.py` and the accounting gaps below are reconciled.

The validator implementation itself is closed-loop tested in CI. Knowledge Engine V1 CI run `31872816497` on head `ee2397ce68ead4799597426e3dbd2ab10c894d5d` passed:

- six-domain knowledge contracts;
- generated STATUS consistency;
- positive and fail-closed negative tests for `validate_k1_intake.py`;
- knowledge-tree copyright binary guard;
- stable `:ziwei-core:test` regression.

This proves the **validator contract and existing core** are green. It does not prove the private local intake is green until that exact intake is run through the validator on the local machine.

## Reported domain results

| Domain | Reported gate | Unique | Duplicates | Book READ | Metadata self-audit |
|---|---|---:|---:|---:|---|
| ziwei | PASS | 148 | 62 | 0 | 5/5 |
| bazi | PASS | 168 | 90 | 0 | 5/5 |
| qimen | PASS | 153 | 184 | 0 | 5/5 |
| liuyao | PARTIAL | 7 | 3 | 0 | 5/5 |
| liuren | PASS | 10 | 4 | 0 | 5/5 |
| fengshui | PARTIAL | 28 | 2 | 0 | 5/5 |

Reported positives:

- 910 files scanned; 541 distinct SHA256 values reported.
- Canonical duplicates were deduplicated by SHA256 rather than by filename alone.
- No BOOK was labelled READ.
- TEXT_OK was explicitly treated as a text-layer observation, not proof that the book was read.
- No original books, scan pages or full OCR were placed in the delivery directory.
- Each domain reports a 5/5 source metadata/hash spot-check.
- Existing qimen handoff and iztro implementation evidence were not silently promoted to independent truth evidence.

## Blocker A — global accounting does not yet reconcile

The six reported domain totals sum to:

- canonical unique sources = **514**
- duplicate records = **345**
- classified canonical + duplicates = **859**

But the master report says **910 files** were scanned and **541 distinct SHA256** values were observed.

Therefore the current summary leaves two explicit accounting questions:

1. `910 - 859 = 51` scanned files are not explained by the domain unique+duplicate totals.
2. `541 - 514 = 27` distinct SHA256 values are not represented as canonical domain sources.

These may be legitimate exclusions, cross-domain/common candidates, unsupported file types, archive members or out-of-scope project files. They are not assumed to be errors, but K1 cannot close until every scanned file has an explicit disposition in a local-only inventory ledger.

## Blocker B — K1 gate semantics were applied too strictly to sparse domains

The reported reasons for `liuyao=PARTIAL` (few books / no note pack) and `fengshui=PARTIAL` (no note pack / systems not yet read apart) are **coverage/readiness concerns**, but they are not automatically K1 Source Index failures.

K1 asks: "Did we discover, deduplicate and index the local corpus honestly?"

It does **not** ask: "Do we already have enough books to validate the doctrine?"

A domain may therefore be `L1_INDEXED` while still carrying a high corpus-coverage risk and being unable to reach later `CROSS_VERIFIED`, `FIXTURE_VERIFIED` or `INTERPRETATION_READY` levels.

For this reason, the local recheck must distinguish:

- `K1_INDEX_STATUS`: completeness of discovery/indexing;
- `K2_READINESS`: whether the indexed corpus is rich/readable enough to begin useful claim extraction and later cross-verification.

Do not manufacture extra sources to turn a thin corpus into PASS.

## Blocker C — raw intake has not passed the project machine validator

The report says all six domains performed 5/5 manual source checks, which is useful but not equivalent to validating every JSONL record and global invariant. Before sanitized import, the local intake must pass `tools/validate_k1_intake.py` against the exact `/home/joe/knowledge-intake/` tree.

The validator checks domain/source IDs, required metadata, hash shape, canonical-vs-duplicate separation, local-only status, forbidden binaries, and the global accounting ledger.

## Promotion rule

K1 closes only when all of the following are true:

1. local machine validator PASS;
2. 910-file / 541-SHA accounting is reconciled by explicit dispositions, or corrected totals are documented;
3. each domain receives a K1 index verdict based on indexing completeness rather than corpus richness;
4. sanitized registries contain no real local paths/usernames and no copyrighted source text;
5. project-side import validation passes;
6. all six domains can be promoted to `L1_INDEXED` without pretending that source coverage or doctrinal truth is complete.

Only then may the project enter K2 Claim Extraction. K2 itself still does not imply cross-verification or implementation readiness.
