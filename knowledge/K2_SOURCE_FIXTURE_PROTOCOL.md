# K2 Source Fixture Protocol

Status: ACTIVE / v1.1

Purpose: create small, auditable source-defined implementation fixtures without confusing source reproducibility with predictive truth and without copying modern books wholesale into the repository.

## 1. Fixture is not Evidence and not Truth

A source fixture is a compact implementation reference derived from a fully reviewed source location.

It may answer questions such as:

- which source page labels a bureau;
- whether the expected main table is visibly present on that page;
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

- `INDEXED`: source title/page identity was visually reviewed, but no tracked anchor has been accepted.
- `ANCHORS_VERIFIED`: 1-4 sparse anchors were independently rechecked against the original page image by the main reviewer.
- `IMPLEMENTATION_CHECKED`: code output was compared against the verified anchors.

Tracked anchors are deliberately small. Each anchor stores only a stable locator and the visible cell value. It is not a table transcription.

A title may be visible while the expected table is not. Such a row remains `INDEXED`; absence must not be silently repaired by moving the fixture to another page.

No state here changes Reading Ledger status or Evidence claim readiness.

## 4. Visual obligation

A fixture derived from a `VISUAL_REQUIRED` source may only use pages already credited as `VISUAL_PAGE` review.

OCR may be used locally as a navigation/transcription aid, but every tracked anchor must be rechecked against the visible original page before `ANCHORS_VERIFIED`.

`OCR_CANDIDATE != VERIFIED_ANCHOR`

For the current sparse anchors, the main reviewer uses layout locators such as:

- `MAIN_TABLE/甲子/TOP_STAR_HEADER`
- `MAIN_TABLE/甲子/BOTTOM_DOOR_FOOTER`

These locators describe visible table positions; they do not by themselves assert predictive meaning.

## 5. QM-SRC-0001 bureau index and source-page anomaly

For 梁湘潤《奇門遁甲入門》:

- source: `QM-SRC-0001 / WORK-000217`
- canonical SHA256: `0cbf020b76f866d3c2dc70001d16aa5cee9ce8405a4a725ce643c12ef701f7cf`
- source reading: full 57/57 `VISUAL_PAGE`
- bureau family: `LIANG_18_BUREAU`
- time family: `HOUR`
- method layer: `STANDARD_PLATE`

Main-reviewer reinspection at 300 DPI confirms:

- PDF p32-p40: `陽遁一局圖` through `陽遁九局圖`; title and six-column main table are visible.
- PDF p41-p48: `陰遁九局圖` through `陰遁二局圖`; title and six-column main table are visible.
- PDF p49: the right side visibly labels `陰遁一局圖`, but the facing/left content is `十二日圖式`; the expected six-column bureau table is **not visibly present on this indexed page**.

Therefore `K2F-QM-0001-YIN-01` remains:

- `fixture_status=INDEXED`
- `anchor_count=0`
- `source_table_state=TITLE_VISIBLE_TABLE_NOT_PRESENT`

This is preserved as a source/scan page-content anomaly. Do not silently relocate the Yin-one table by inference. A later source-specific lineage review may determine whether the table was omitted, displaced, or represented elsewhere.

The other 17 rows may advance independently to `ANCHORS_VERIFIED`.

## 6. Local helper boundary

A local AI/helper may:

- resolve the canonical PDF by exact SHA256;
- render/crop source pages at higher DPI outside the repository;
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

The current Test F path is:

`source page index`
-> `high-DPI visual recheck`
-> `sparse anchor selection`
-> `ANCHORS_VERIFIED`
-> `implementation comparison`
-> `wrong-bureau / permuted negative controls`

Current source-side result:

- 17 bureau pages have visible main tables and can carry sparse anchors.
- `YIN-01 / p49` is title-visible but table-not-present and remains unresolved at the fixture-source layer.

An implementation may therefore be checked against the 17 verified visible-table fixtures without pretending the eighteenth source table exists at p49.

A code path that reproduces source anchors has passed a source-fidelity test only. Predictive evaluation remains a separate prospective experiment.
