# K1 Source Registry — project-side acceptance

Acceptance update: 2026-08-17

## Verdict

`K1_LOCAL_INDEX = PASS`

`K1_SANITIZED_IMPORT_STRUCTURE = PASS`

`K1_PROJECT_IMPORT = BLOCKED_ON_ATTRIBUTION_QUALITY`

`K2_CLAIM_EXTRACTION = BLOCKED`

The local corpus accounting is closed and the 515 canonical records are now present in GitHub as privacy-safe metadata. Project-side review confirmed the expected seven-file import commit and CI run, but a deeper semantic audit found that the current sanitized registries are **not yet trustworthy bibliographic metadata**. K1 therefore remains open at `K1_ATTRIBUTION_REVIEW`.

## What passed

Local machine validation remains accepted:

- scanned files: **911**
- distinct SHA256: **542**
- canonical sources: **515**
- duplicate records: **345**
- excluded files: **51**
- six-domain K1 index verdict: **PASS**

Sanitized import commit `d1f54f09ec2850cc805efccc22e62ead2e5f8e0b` contains exactly:

- `knowledge/K1_SANITIZED_IMPORT.json`
- six `knowledge/domains/<domain>/sources.jsonl` registries

The manifest declares 148 / 168 / 154 / 7 / 10 / 28 sources = **515 total**. GitHub Actions run `32024210050` passed the existing structural, privacy, hash, binary-boundary and stable-core gates.

These facts prove that the import is structurally complete and privacy-safe. They do **not** prove that author, school, era, copyright or page-count metadata is correct.

## Project-side semantic audit findings

### Blocker A — author attribution is contaminated by directory/collection context

Examples visible directly in the sanitized registries:

- `BZ-SRC-0003` title `八字论命苏民峰` has author `王亭之 / 苏民峰`.
- `BZ-SRC-0009` title `韦千里 - 千里命稿` has author `王亭之 / 韦千里`.
- `LY-SRC-0001` `六爻新大陸`, `LY-SRC-0002` `卜筮正宗`, and `LY-SRC-0003` `增刪卜易` are all attributed to `王亭之`.
- `QM-SRC-0001` `梁湘润-奇门遁甲入门` is attributed to `王亭之 / 梁湘润`.
- multiple Fengshui Liang Xiangrun titles are attributed to `王亭之 / 梁湘润`.
- Liuren entries include `王亭之` in multi-person author strings even when the title itself names 袁树珊/主编/校者 instead.

This pattern is consistent with parent-directory or collection-context leakage into the `author` field. Parent folder ownership is not author evidence.

### Blocker B — sanitized records do not conform to the canonical Source enum contract

`knowledge/schema/source.schema.json` defines canonical `era` values as:

`ANCIENT / PRE_MODERN / MODERN / UNKNOWN`

and canonical copyright values as:

`PUBLIC_DOMAIN_TEXT_ONLY / LICENSED / RESEARCH_ONLY / UNKNOWN / FORBIDDEN_TO_PACKAGE`.

Current sanitized rows include non-canonical values such as:

- `modern`
- `pre_1950_text_in_modern_file`
- `modern_publication_or_scan`
- `pre1950_text_modern_scan_or_typeset`
- `user_owned_notes`
- `project_or_mit_code`

The previous `validate_sanitized_k1.py` validated counts, IDs, hashes, local-path stripping and package boundaries, but did not validate Source schema enums or attribution provenance. A green run therefore could not close this semantic gap.

### Blocker C — `pages` is being used for non-page extents

Examples such as `_books_digest`, `_books_toc`, Markdown notes and Kotlin/code records carry large integer `pages` values. For non-paginated text/code this is likely a line/extent count, not a page count. `pages` must mean actual document pages or be null; the basis must be explicit.

### Blocker D — canonical titles contain distribution noise

Some titles contain download-site or contact/promotional material such as `www.*` or `更多教程加微信...`. Those strings are not bibliographic titles and must not become canonical Source identity fields.

## Corrective contract

K1 source metadata now distinguishes fact from inference. New provenance fields are documented in `knowledge/schema/source.schema.json`:

- `author_basis` / `author_evidence`
- `school_basis` / `school_evidence`
- `pages_basis`
- `evidence_role`

Allowed author evidence does **not** include parent directory, neighboring file, collection folder, model memory or author-to-school inference.

`evidence_role` separates:

- textual source material;
- secondary notes;
- implementation/code evidence;
- auxiliary indexes.

This prevents CODE and prior AI notes from being counted as independent traditional-source truth in K2.

## New fail-closed quality gate

`tools/validate_k1_source_quality.py` now checks:

- canonical era/copyright enums;
- author attribution provenance;
- filename-author consistency when `author_basis=FILENAME`;
- school provenance;
- page-count provenance;
- evidence-role separation;
- promotional/contact noise in canonical titles;
- existing privacy/package boundaries.

While `PROJECT_STATE.source_quality=REVIEW_REQUIRED`, CI requires the project to remain explicitly blocked and reports the defects without pretending K1 is complete. Once remediation claims `source_quality=COMPLETE`, the same validator becomes hard fail-closed and requires **zero** source-quality issues.

## Promotion rule

K1 project import closes only when:

1. all 515 source records still reconcile with the accepted local index;
2. `validate_sanitized_k1.py --force` passes;
3. `validate_k1_source_quality.py --force` passes with zero issues;
4. author/school/page metadata has explicit evidence or is conservatively reset to `UNKNOWN`/null;
5. canonical Source enum values are normalized;
6. titles are bibliographic and free of distribution/contact noise;
7. no local paths or source bodies enter Git;
8. stable-core regression and Knowledge Engine CI pass on the exact corrected head.

Only then may the six domains be promoted to at least `L1_INDEXED` and K2 be opened under each domain's readiness constraints.
