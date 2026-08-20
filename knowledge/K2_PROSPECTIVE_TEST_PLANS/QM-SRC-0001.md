# QM-SRC-0001 Prospective Test Plan

Status: PREREGISTRATION CANDIDATE

Source trigger: `QM-SRC-0001 / 梁湘润《奇门遁甲入门》`

Purpose: convert the strongest source-derived disagreements and method forks into falsifiable tests. This plan does not assume the book is correct.

## Global scoring contract

Every test below must freeze before outcome feedback:

- input timestamp/location and question wording;
- method layer;
- setup calibration and seasonal-alignment method;
- time family;
- deity system where relevant;
- Role Map;
- eligible features;
- prediction categories and confidence;
- timing window/tolerance;
- abstention criteria;
- allowed auxiliary information.

Outcome states: `HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`.

Changing any frozen field after feedback creates a new model version; it cannot repair the original score.

## Test A — Setup calibration fork

Question: do 平气/定气 and 正授/超神/置闰/接气 variants produce meaningfully different and prospectively useful predictions?

Protocol:

1. Pre-register all eligible setup variants for a timestamp before the event outcome.
2. Generate each盘 independently and label it.
3. Apply the same downstream Role Map and scoring rubric where comparability allows.
4. Never select the variant that later fits best as the “true” chart.
5. Record:
   - setup divergence rate;
   - prediction divergence rate;
   - accuracy/calibration per variant;
   - abstention and unresolved rates.

Failure condition: if variants differ often but none shows stable out-of-sample advantage, the project should treat setup choice as unresolved context rather than doctrine.

## Test B — Deity-system A/B

Question: does `勾陈/朱雀` vs `白虎/玄武` produce distinct repeatable value under matched conditions?

Protocol:

- same timestamps, same plate, same Role Map, same questions;
- only deity-system interpretation changes;
- predictions frozen independently;
- no attribute borrowing across systems;
- score exact/partial/miss and calibration.

Failure condition: if both systems can explain outcomes equally after broad interpretation but do not prospectively discriminate, deity symbolism remains source-specific candidate material rather than an operational deciding layer.

## Test C — 九星 fixed label vs conditional model

Models:

- `M1`: fixed source吉凶 label only;
- `M2`: star + season + task + 旺相休囚 + contextual relations.

Use identical cases and outcome categories.

Compare:

- discrimination;
- calibration;
- overconfident misses;
- abstention rate;
- robustness across task domains.

Strong support for M2 requires prospective improvement, not merely more elaborate retrospective narratives.

## Test D — 九星十二时辰应克 independent test

This family must be isolated from normal盘 reading.

Before each trial:

- choose only one explicit star/hour mapping path;
- convert traditional statements into predefined scorable event categories;
- define exact time windows;
- define what counts as no-event;
- estimate or collect base rates where feasible;
- prohibit using standard盘 details to rescue a miss.

Compare against:

- naive/base-rate forecast;
- shuffled hour labels;
- randomized event assignment where appropriate.

Failure condition: broad poetic matching without predeclared event classes is unscorable, not a hit.

## Test E — YEAR / MONTH / DAY / HOUR hierarchy

Source candidate: the book states a traditional hierarchy favoring nearer time layers.

Protocol:

1. For cases where all four time families can be generated, freeze all four independently.
2. Use the same target outcome dimensions.
3. Never choose the best layer after the result.
4. Compare predictive performance and calibration by horizon.

Possible outcomes:

- `SUPPORTS`: near-time layers consistently outperform under matched horizons;
- `NARROWS`: hierarchy holds only for specific domains/horizons;
- `CONTRADICTS`: no stable ordering or broader layers outperform;
- `CONTEXT_SPLIT_REQUIRED`: methods target different objects and should not be ranked globally.

## Test F — Bureau lookup implementation integrity

Purpose: validate reproducibility, not divination truth.

Use the book's 阳遁/阴遁十八局 tables as a source-defined reference corpus.

Tests:

- manual vs code-generated placement agreement;
- boundary timestamps around节气/换局;
- positive fixtures from clearly readable table rows;
- deliberately wrong-bureau negative controls;
- deliberately permuted placement controls.

The source index is now fixed without copying the full modern table into Git:

- `knowledge/K2_SOURCE_FIXTURES/QM-SRC-0001_BUREAU_INDEX.jsonl`
- 阳遁一至九局: PDF p32-p40 ascending;
- 阴遁九至一局: PDF p41-p49 descending.

Tracked fixtures obey `K2_SOURCE_FIXTURE_PROTOCOL.md`: full OCR/transcription remains local; only sparse, manually rechecked anchors may later enter Git, with at most four anchors per table under the current copyright rule.

Key audit question: can interpreters still tell convincing outcome stories from wrong inputs? If yes, interpretation flexibility is too high even when the setup engine is correct.

## Test G — Auxiliary ablation

Compare:

- `A`: frozen standard盘 only;
- `B`: same standard盘 + preregistered hour-omen family;
- `C`: if ever studied academically, ritual material remains descriptive only and is excluded from outcome scoring.

Record delta from A→B separately. Never credit B's incremental information to the standard盘 model.

## Minimum evidence for model promotion

No fixed case count equals “validated”. Promotion requires a pattern of:

- preregistered prospective trials;
- independent outcomes;
- explicit misses retained;
- negative controls;
- contamination audit;
- calibration, not just hit count;
- performance against a reasonable baseline;
- stable applicability boundaries.

Three cases can trigger attention; they cannot prove a rule.

## Immediate implementation priority

1. **DONE — fixture page index**: all 18 bureau tables are mapped to visually reviewed PDF pages without full-table republication.
2. **NEXT — sparse anchor verification**: obtain local high-DPI crops/candidate transcription for p32-p49, then main-reviewer recheck and select at most 1-4 anchors per table.
3. Add explicit context fields from the Method Delta to experimental case records.
4. Implement Test F source-fidelity comparison and wrong-bureau/permuted negative controls.
5. Design Test A after the setup engine can preserve each calibration branch without result-driven selection.
6. Only then run deity/star/hour-omen comparisons.
7. Keep ritual and gambling material outside operational scoring.
