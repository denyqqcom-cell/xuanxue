# K2 Source Fixture Protocol

Status: ACTIVE

Purpose: create small, auditable source-defined implementation fixtures without confusing source reproducibility with predictive truth and without copying modern books wholesale into the repository.

## 1. Fixture is not Evidence and not Truth

A source fixture is a compact implementation reference derived from a fully reviewed source location.

It may answer questions such as:

- which source page contains a bureau table;
- which polarity/bureau number the table labels itself as;
- a small number of manually verified anchor cells for implementation regression tests;
- whether code reproduces those source-defined anchors.

A fixture does **not** establish that the underlying divination method predicts reality.

Keep these dimensions separate:

`Source Fidelity != Lookup Determinism != Empirical Support`

## 2. Copyright boundary

For modern copyrighted books, do not commit a full transcription of a large table merely to test implementation.

Allowed repository material should normally be limited to:

- table identity and page locator;
- structural metadata;
- sparse non-substantial anchors needed for regression testing;
- derived hashes, counts and verification state;
- paraphrased analytical notes.

Raw page images, full OCR, full table transcriptions and crop packets remain local/private.

For `LIANG_18_BUREAU`, no more than four sparse anchor cells per table may enter the tracked fixture layer unless a later copyright review explicitly changes this limit.

## 3. Fixture lifecycle

`INDEXED -> ANCHORS_VERIFIED -> IMPLEMENTATION_CHECKED`

- `INDEXED`: source table identity and locator were visually verified; no cell anchor has entered the repository.
- `ANCHORS_VERIFIED`: 1-4 sparse anchors were independently rechecked against the original page image by the main reviewer.
- `IMPLEMENTATION_CHECKED`: code output was compared against the verified anchors.

No state here changes Reading Ledger status or Evidence claim readiness.

## 4. Visual obligation

A fixture derived from a `VISUAL_REQUIRED` source may only use pages already credited as `VISUAL_PAGE` review.

OCR may be used locally as a navigation/transcription aid, but every tracked anchor must be rechecked against the visible original page before `ANCHORS_VERIFIED`.

`OCR_CANDIDATE != VERIFIED_ANCHOR`

## 5. QM-SRC-0001 bureau index

For 梁湘潤《奇門遁甲入門》:

- source: `QM-SRC-0001 / WORK-000217`
- canonical SHA256: `0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf`
- source reading: full 57/57 `VISUAL_PAGE`
- bureau family: `LIANG_18_BUREAU`
- time family: `HOUR`
- method layer: `STANDARD_PLATE`

The visually verified table-title/page mapping is:

- 陽遁一局至九局: PDF p32-p40, ascending;
- 陰遁九局至一局: PDF p41-p49, descending.

This mapping is an implementation index, not a prediction result.

## 6. Local helper boundary

A local AI/helper may:

- resolve the canonical PDF by exact SHA256;
- render/crop p32-p49 at higher DPI outside the repository;
- produce candidate transcriptions or OCR strictly as local `NAVIGATION_ONLY` material;
- report unreadable cells and conflicting candidate readings.

It must not:

- write tracked fixture anchors;
- mark Reading/Evidence/Distillate state;
- decide which candidate cell reading is accepted;
- commit or push;
- infer predictive validity from table consistency.

Final anchor selection and Git normalization belong to the project-side main reviewer.

## 7. Test F use

The initial Test F path is:

`source page index`
-> `local high-DPI crops`
-> `candidate sparse anchors`
-> `main visual recheck`
-> `ANCHORS_VERIFIED`
-> `implementation comparison`
-> `wrong-bureau / permuted negative controls`

A code path that reproduces the book has passed a source-fidelity test only. Predictive evaluation remains a separate prospective experiment.
