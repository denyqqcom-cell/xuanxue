# K1 Source Registry — project-side acceptance

Acceptance update: 2026-08-17

## Verdict

`K1_LOCAL_INDEX = PASS`

`K1_PROJECT_IMPORT = PENDING`

`K2_CLAIM_EXTRACTION = BLOCKED`

The private local intake is not stored in GitHub. The project-side evidence for this update is the reported successful execution of the repository validator `tools/validate_k1_intake.py`, together with the reconciled accounting output recorded in `knowledge/K1_LOCAL_VALIDATION.json`. This closes the previous 51-file / 27-SHA accounting blockers, but does **not** yet mean that the repository has absorbed all 515 canonical source records. That final K1 step is the sanitized metadata import.

## Local machine validation reported PASS

Reported validator result:

`k1-intake: PASS`

Reconciled accounting:

- scanned files: **911**
- distinct SHA256: **542**
- canonical sources: **515**
- domain duplicate records: **345**
- excluded files: **51**
- inventory ledger rows: **911**
- inventory ledger distinct SHA: **542**

The previous 910 / 541 totals changed only because one new qimen user note appeared after the original scan and became `QM-SRC-0154`.

## Previous accounting blockers are closed

The original unexplained 51 files are now explicitly dispositioned as **51 EXCLUDED** files. They consist of 27 excluded unique hashes plus 24 additional copies of those excluded hashes.

The original 27-SHA gap is exactly the 27 excluded unique hashes:

- `no_domain_keyword`: 14
- `repo_meta`: 3
- `generic_tool_or_index`: 10

They are not missing occult books and must not be promoted into a domain merely to balance counts.

## Six-domain K1 index verdict

| Domain | Canonical | Duplicates | K1 index | K2 readiness |
|---|---:|---:|---|---|
| ziwei | 148 | 62 | PASS | READY_FOR_EXTRACTION |
| bazi | 168 | 90 | PASS | READY_FOR_EXTRACTION |
| qimen | 154 | 184 | PASS | READY_FOR_EXTRACTION |
| liuyao | 7 | 3 | PASS | THIN_CORPUS |
| liuren | 10 | 4 | PASS | THIN_CORPUS |
| fengshui | 28 | 2 | PASS | READING_REQUIRED |

This distinction is intentional. A thin corpus can still have a complete K1 index. `THIN_CORPUS` and `READING_REQUIRED` are later readiness constraints; they are not reasons to invent sources or fail an otherwise honest Source Registry.

## Domain-specific acceptance notes

- **Ziwei**: current corpus is sufficient to start source-level extraction, but 三合/钦天/历法/时辰/大限/小限 still lack adequate filename/note-title coverage; iztro remains implementation evidence, not traditional truth.
- **Bazi**: corpus volume is large, but many primary books are scans. From格/专旺/子初/早晚子 and several school conflicts still require original-source reading rather than note-level inference.
- **Qimen**: K1 source index now has 154 canonical records. Existing handoff remains evidence to re-audit, not authority. Full-board verification and several school branches are still unresolved.
- **Liuyao**: the local corpus is genuinely thin. 《火珠林》 remains a cross-domain pointer instead of receiving a second LY source ID; 梅花、京房易 and mixed 卜筮 compilations are not inflated into 六爻 corpus.
- **Liuren**: the available corpus is fully indexed but thin; two copies/editions of《大六壬探原》 remain scan-dependent.
- **Fengshui**: K1 indexing is complete for the discoverable corpus, but actual reading is insufficient. Only 玄空飞星/三元/形势 are confirmable from filenames; 八宅/三合/罗盘/坐向 and spatial-input rules remain unsupported.

## Remaining K1 gate — sanitized import

The repository still must not claim `L1_INDEXED` for the newly indexed sources until the 515 canonical records are imported as safe metadata and validated in GitHub.

The official path is:

1. rerun `tools/validate_k1_intake.py` on the local intake;
2. run `tools/sanitize_k1_sources.py` rather than copying local JSONL manually;
3. import only the whitelisted metadata fields to `knowledge/domains/*/sources.jsonl`;
4. strip local paths, sizes, sampled locations and notes;
5. keep source books `local_only=true` and `packaged=false`;
6. run `tools/validate_sanitized_k1.py --force`;
7. run sanitization tests and stable core regression;
8. push only the seven sanitized import files for project-side review.

The dedicated handoff is `LOCAL_CORPUS_K1_SANITIZED_IMPORT_PROMPT.md`.

## Copyright and privacy boundary

No original PDF, scan page, OCR body, modern long quotation, proprietary diagram/table, font, real local path or private directory may be imported. File hashes and bibliographic metadata are provenance fields; they do not authorize redistribution of the source material.

## Promotion rule

After sanitized import is present and project-side validation passes:

- all six domains may be marked at least `L1_INDEXED` for Source Registry maturity;
- qimen may retain its higher legacy claim maturity while clearly separating K1 source coverage from claim validation;
- `K2_CLAIM_EXTRACTION` may be opened only under domain-specific readiness constraints;
- `THIN_CORPUS` and `READING_REQUIRED` continue to block unsupported cross-verification or interpretation claims.

Until then, `k2_blocked=true` remains correct.
