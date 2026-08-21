# K2 Source Fixture Protocol

Status: ACTIVE / v1.1

Purpose: create small, auditable source-defined implementation fixtures without confusing source reproducibility with predictive truth and without copying modern books wholesale into the repository.

## 1. Fixture is not Evidence and not Truth

A source fixture is a compact implementation reference derived from a fully reviewed source location.

It may answer questions such as:

- which source page actually contains a bureau table body;
- which polarity/bureau number the table body encodes;
- a small number of manually verified anchor cells for implementation regression tests;
- whether code reproduces those source-defined anchors.

A fixture does **not** establish that the underlying divination method predicts reality.

Keep these dimensions separate:

`Source Fidelity != Lookup Determinism != Applicability != Empirical Support`

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

- `INDEXED`: source table identity/locator is known, but no cell anchor has entered the repository.
- `ANCHORS_VERIFIED`: 1-4 sparse anchors were independently rechecked against the visible original table body by the main reviewer.
- `IMPLEMENTATION_CHECKED`: code output was compared against the verified anchors and required negative controls.

No state here changes Reading Ledger status or Evidence claim readiness.

## 4. Visual obligation

A fixture derived from a `VISUAL_REQUIRED` source may only use pages already credited as `VISUAL_PAGE` review.

OCR may be used locally as a navigation/transcription aid, but every tracked anchor must be rechecked against the visible original page before `ANCHORS_VERIFIED`.

`OCR_CANDIDATE != VERIFIED_ANCHOR`

The 2026-08-21 Liang correction adds another rule:

`Visual Presence != Semantic Association`

Seeing a title and a table on the same PDF raster does not prove the title labels that table. When a scan contains two printed pages/spreads, table identity must be reconstructed from printed-page topology and table-internal structure.

## 5. QM-SRC-0001 bureau body mapping

For 梁湘潤《奇門遁甲入門》:

- source: `QM-SRC-0001 / WORK-000217`
- canonical SHA256: `0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf`
- source reading: full 57/57 `VISUAL_PAGE`
- bureau family: `LIANG_18_BUREAU`
- time family: `HOUR`
- method layer: `STANDARD_PLATE`

### 5.1 Why the original page index was wrong

The first fixture pass incorrectly matched a right-side visible bureau title to the large table body on the left side of the same PDF raster. That produced a one-bureau shift and a false claim that `YIN-01 / p49` had a title but no table.

Re-review against:

- printed physical-page sequence;
- polarity labels;
- the internal `甲子` palace/star/door structure;
- neighboring bureau progression;

showed that this was a reviewer/page-topology error, not a source anomaly.

PDF p35/p36 are also out of printed-page order, so simple `PDF page number + 1` progression is unsafe.

### 5.2 Correct table-body PDF mapping

Yang bureau table bodies:

- 陽遁一局 -> PDF p31
- 陽遁二局 -> PDF p32
- 陽遁三局 -> PDF p33
- 陽遁四局 -> PDF p34
- 陽遁五局 -> PDF p36
- 陽遁六局 -> PDF p35
- 陽遁七局 -> PDF p37
- 陽遁八局 -> PDF p38
- 陽遁九局 -> PDF p39

Yin bureau table bodies:

- 陰遁九局 -> PDF p40
- 陰遁八局 -> PDF p41
- 陰遁七局 -> PDF p42
- 陰遁六局 -> PDF p43
- 陰遁五局 -> PDF p44
- 陰遁四局 -> PDF p45
- 陰遁三局 -> PDF p46
- 陰遁二局 -> PDF p47
- 陰遁一局 -> PDF p48

PDF p49 is the `十二日圖式` body, not a missing Yin-1 bureau table.

### 5.3 Bureau-specific Jiazi anchors

For this fixture family, the tracked `甲子` anchors are not merely checked against a global star/door vocabulary. They are checked against the bureau-specific expected pair:

- 1: 天蓬 / 休
- 2: 天芮 / 死
- 3: 天衝 / 傷
- 4: 天輔 / 杜
- 5: 天禽 / 死
- 6: 天心 / 開
- 7: 天柱 / 驚
- 8: 天任 / 生
- 9: 天英 / 景

This closes the loophole that allowed a globally valid but one-bureau-shifted pair to pass validation.

## 6. Local helper boundary

A local AI/helper may:

- resolve the canonical PDF by exact SHA256;
- render/crop p31-p48 at higher DPI outside the repository;
- produce candidate transcriptions or OCR strictly as local `NAVIGATION_ONLY` material;
- report unreadable cells and conflicting candidate readings.

It must not:

- infer table identity from same-raster title proximity alone;
- write tracked fixture anchors;
- mark Reading/Evidence/Distillate state;
- decide which candidate cell reading is accepted;
- commit or push;
- infer predictive validity from table consistency.

Final anchor selection and Git normalization belong to the project-side main reviewer.

## 7. Test F use

The corrected Test F path is:

`source table-body mapping`
-> `main visual recheck`
-> `bureau-specific sparse anchors`
-> `ANCHORS_VERIFIED`
-> `implementation comparison`
-> `wrong-bureau / shifted-page / permuted negative controls`
-> `IMPLEMENTATION_CHECKED`

The former one-bureau-shifted page mapping is now itself a required negative control. A validator or implementation test that accepts it lacks discrimination.

A code path that reproduces the book has passed a source-fidelity/implementation-integrity test only. Predictive evaluation remains a separate prospective experiment.
