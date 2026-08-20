# QM-SRC-0001 Visual Review Session

Status: VISUAL_REVIEW_COMPLETE / 57_OF_57 / CLOSURE_PENDING_CI

Start date: 2026-08-21

## Source lock

- source_id: `QM-SRC-0001`
- work_id: `WORK-000217`
- page-verified title: `奇门遁甲入门`
- page-verified author: `梁湘润`
- registered pages: `57`
- readability: `SCAN`
- execution lane: `VISUAL_REQUIRED`
- canonical SHA256: `0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf`
- copyright boundary: `FORBIDDEN_TO_PACKAGE / local_only`

The uploaded PDF was re-hashed in the main-review environment and matched the canonical SHA256 exactly; PDF page count was verified as 57. Page-internal visual evidence on p1-p2 directly supports the title and author. Edition/publication metadata remains unclaimed unless stronger internal evidence is available.

## Review integrity

- Pre-Book Retrospective: DONE
- original-page visual inspection: DONE p1-p57
- OCR/text extraction as substitute: NOT USED
- OCR assistance: limited secondary navigation/checking only after visual inspection on selected difficult pages; original page images remained authoritative
- modern copyrighted text copied into Evidence: NO; Evidence is paraphrased and `verbatim_quote=null`
- Prediction Protocol Freeze: ACTIVE as anti-hindsight constraint, not Theory Freeze

## Final page accounting

- registered_pages: 57
- visually_reviewed_pages: 57
- reviewed_range: `pdf:p1-p57`
- verification_mode: `VISUAL_PAGE`
- reading_status: `COMPLETE`
- atomic_evidence_count: 32
- Book Distillate: CREATED / REVIEWED
- Method Delta: CREATED / PROVISIONAL
- Prospective Test Plan: CREATED / PREREGISTRATION CANDIDATE
- source closure: PENDING aggregate validators/tests + exact-head CI

No claim extraction is enabled by this completion.

## Full-book distillation summary

### A. The source is internally heterogeneous

The book contains at least six different evidence/method layers:

1. source criticism / traditional history;
2. 三元 and standard plate setup;
3. 九星 seasonal/task interpretation;
4. 九星十二时辰应克;
5. 年家/月家/日家/时家 variants and 18 bureau lookup tables;
6. ritual/符咒/反闭/步斗/六戊/禁敌 materials.

The project must not flatten these into one universal rule pool.

### B. Setup choice is a first-order degree of freedom

The book explicitly distinguishes 平气/定气 and 正授/超神/置闰/接气. These choices must be declared before outcome feedback. If multiple variants are compared, all must be preregistered and scored separately.

### C. Deity-system conflict is real

The source uses:

`值符 / 螣蛇 / 太阴 / 六合 / 勾陈 / 朱雀 / 九地 / 九天`

This conflicts with the modern 白虎/玄武 baseline. The project records a `CONFLICT_CANDIDATE` and adds `deity_system` as an explicit context field rather than silently harmonizing the systems.

### D. 九星 is not source-internally reducible to one fixed label

The book has rough吉凶 categories but also conditions star use by season, task and旺相休囚. Therefore fixed labels are insufficient as verdicts even on the book's own terms.

### E. The 18 bureau tables are structurally valuable but not empirical proof

The阳遁/阴遁 lookup tables are visually explicit and mechanically auditable. They can reduce implementation drift after a method is frozen. Their reproducibility is `Lookup Determinism`, not predictive validity.

### F. Hour-omen doctrine must be isolated

`九星十二时辰应克` maps star/hour combinations to concrete future events and timing. It is too distinct to be used as an undeclared extra signal; it becomes a separate prospectively testable method family.

### G. Ritual material is default-excluded

The final pages contain incantations,符,禹罡/步斗,六戊,博奕胜负 and禁敌 methods. These are preserved as source evidence but excluded from operational prediction scoring and from claims of empirical efficacy.

## Strongest theory deltas

- add `Method-Layer Gate`;
- add `setup_calibration` and `seasonal_alignment`;
- add `deity_system`;
- elevate `time_family` to first-class context;
- add separate `hour_omen_family`;
- set `ritual_layer = EXCLUDED_BY_DEFAULT`;
- distinguish `Lookup Determinism` from `Predictive Validity`;
- demote year/month/day/hour hierarchy to testable candidate;
- strengthen Symbol-to-Verdict Gate.

## What remains unresolved

- which setup calibration performs better;
- whether either deity system has prospective advantage;
- whether 九星 conditional rules outperform fixed labels;
- whether 九星十二时辰应克 beats base rates;
- whether year/month/day/hour hierarchy has stable predictive meaning;
- historical truth of the lineage/reduction narrative;
- any supernatural efficacy of ritual material.

These are test obligations, not doctrinal conclusions.

## Closure chain status

`canonical bytes` ✅
→ `Pre-Book Retrospective` ✅
→ `original-page visual packet / visibility` ✅
→ `main-reviewer full visual reading` ✅ 57/57
→ `Atomic Evidence` ✅ 32
→ `Book Distillate` ✅ REVIEWED
→ `Conflict / Anti-pattern Review` ✅ inside distillate
→ `Method Delta` ✅
→ `Prospective Test Plan` ✅
→ `aggregate validators/tests` ⏳
→ `exact-head CI` ⏳
→ `CLOSED` ⏳

The source is fully read, but project closure must wait for validators and exact-head CI. PR #9 remains Draft / unmerged unless the user explicitly requests otherwise.
