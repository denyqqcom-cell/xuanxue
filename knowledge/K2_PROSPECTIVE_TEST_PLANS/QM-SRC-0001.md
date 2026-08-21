# QM-SRC-0001 Prospective Test Plan

Status: PREREGISTRATION CANDIDATE / Test F source mapping corrected 2026-08-21

Source trigger: `QM-SRC-0001 / 梁湘润《奇门遁甲入门》`

Purpose: convert the strongest source-derived disagreements and method forks into falsifiable tests. This plan does not assume the book is correct.

## Global scoring contract

Every predictive test below must freeze before outcome feedback:

- input timestamp/location and question wording;
- method layer;
- setup method/calibration and seasonal-alignment method;
- time-boundary system;
- time family;
- deity/state system where relevant;
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
5. Record setup divergence, prediction divergence, calibration and abstention/unresolved rates.

Failure condition: if variants differ often but none shows stable out-of-sample advantage, setup choice remains unresolved context rather than doctrine.

## Test B — Deity-system A/B

Question: does `勾陈/朱雀` vs `白虎/玄武` produce distinct repeatable value under matched conditions?

- same timestamp/plate/Role Map/question;
- only deity-system interpretation changes;
- predictions frozen independently;
- no attribute borrowing across systems;
- score exact/partial/miss and calibration.

Failure condition: if both systems remain retrospectively explainable but do not prospectively discriminate, deity symbolism remains source-specific candidate material.

## Test C — 九星 fixed label vs conditional model

Models:

- `M1`: fixed source吉凶 label only;
- `M2`: star + season + task + 旺相休囚 + contextual relations.

Use identical cases and outcome categories. Compare discrimination, calibration, overconfident misses, abstention and cross-domain robustness.

Strong support for M2 requires prospective improvement, not merely richer retrospective narrative.

## Test D — 九星十二时辰应克 independent test

This family remains isolated from normal盘 reading.

Before each trial:

- choose one explicit star/hour mapping path;
- convert traditional statements into predefined scorable event categories;
- define exact time windows and no-event conditions;
- estimate/collect base rates where feasible;
- prohibit standard盘 details from rescuing a miss.

Compare against naive/base-rate, shuffled-hour and randomized controls.

Broad poetic matching without predeclared event classes is unscorable, not a hit.

## Test E — YEAR / MONTH / DAY / HOUR hierarchy

For cases where all four time families can be generated, freeze all four independently and compare them on the same target outcome dimensions.

Never choose the best layer after the result.

Possible outcomes:

- `SUPPORTS`
- `NARROWS`
- `CONTRADICTS`
- `CONTEXT_SPLIT_REQUIRED`

The source hierarchy remains a candidate, not project doctrine.

## Test F — Bureau lookup implementation integrity

Purpose: validate source reproducibility and implementation discrimination, not divination truth.

### F1. Corrected source body mapping

The first fixture pass was wrong because it associated a bureau title on one side of a scanned spread with the table body on the other side of the same PDF raster.

Correct table-body mapping:

- Yang1 p31
- Yang2 p32
- Yang3 p33
- Yang4 p34
- Yang5 p36
- Yang6 p35
- Yang7 p37
- Yang8 p38
- Yang9 p39
- Yin9 p40
- Yin8 p41
- Yin7 p42
- Yin6 p43
- Yin5 p44
- Yin4 p45
- Yin3 p46
- Yin2 p47
- Yin1 p48

PDF p35/p36 are out of printed-page order. PDF p49 is `十二日圖式`, not a missing Yin1 table.

The correction is documented in `K2_SOURCE_FIXTURE_PROTOCOL.md` and the post-review correction log.

### F2. Sparse-anchor state

DONE:

- all 18 table bodies visually located;
- 18 fixtures have `ANCHORS_VERIFIED`;
- two source-safe Jiazi anchors per bureau;
- total tracked sparse anchors: 36;
- no full modern table transcription committed.

Bureau-specific Jiazi pair:

- 1 天蓬/休
- 2 天芮/死
- 3 天衝/傷
- 4 天輔/杜
- 5 天禽/死
- 6 天心/開
- 7 天柱/驚
- 8 天任/生
- 9 天英/景

### F3. Implementation comparison

Next implementation gate:

- compare project engine output against all 18 verified Jiazi pairs;
- isolate any center-palace / bureau-5 handling mismatch;
- do not promote a fixture merely because its star matches while its door is missing/wrong.

### F4. Required negative controls

A positive-only regression is insufficient. Required controls:

1. **wrong-bureau**: compare a bureau against an adjacent bureau's anchors;
2. **shifted-page**: replay the superseded one-page-shift mapping and require failure;
3. **permuted-anchor**: permute verified pairs between bureaus and require failure;
4. **boundary/setup** controls when timestamp-driven generation is later included.

If the implementation test accepts these deliberately wrong inputs, it has not demonstrated discrimination.

Only after correct controls pass may a row move:

`ANCHORS_VERIFIED -> IMPLEMENTATION_CHECKED`

This remains source/implementation integrity only.

### F5. Interpretation stress test

Separate from the engine comparison, later blind interpretation experiments should ask whether analysts can still produce equally convincing narratives from wrong-bureau or permuted inputs.

If yes, interpretive flexibility remains too high even when the setup engine is correct.

## Test G — Auxiliary ablation

Compare:

- `A`: frozen standard盘 only;
- `B`: same standard盘 + preregistered hour-omen family;
- `C`: ritual material remains descriptive only and excluded from outcome scoring.

Record delta separately. Never credit an auxiliary gain to the standard盘 model.

## Minimum evidence for model promotion

No fixed case count equals “validated”. Promotion requires a pattern of:

- preregistered prospective trials;
- independent outcomes;
- explicit misses retained;
- negative controls;
- contamination audit;
- calibration, not only hit count;
- performance against a reasonable baseline;
- stable applicability boundaries.

Three cases can trigger attention; they cannot prove a rule.

## Immediate implementation priority

1. **DONE** — full 57/57 visual reading.
2. **DONE** — corrected 18-table body mapping after spread-topology re-review.
3. **DONE** — 18 × 2 = 36 sparse Jiazi anchors at `ANCHORS_VERIFIED`.
4. **NEXT** — implementation comparison against the 18 verified pairs.
5. **NEXT** — wrong-bureau / shifted-page / permuted negative controls.
6. Only after Test F implementation integrity closes, proceed to Test A/B/C/D/E/G prospective comparisons.
7. Keep ritual and gambling material outside operational scoring.
