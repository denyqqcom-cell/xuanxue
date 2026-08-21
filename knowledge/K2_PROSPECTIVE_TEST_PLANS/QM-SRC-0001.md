# QM-SRC-0001 Prospective Test Plan

Status: ACTIVE TEST PLAN / TEST F JIAZI-SPARSE IMPLEMENTATION SCOPE PASSED

Source trigger: `QM-SRC-0001 / 梁湘润《奇门遁甲入门》`

Purpose: convert the strongest source-derived disagreements and method forks into falsifiable tests. This plan does not assume the book is correct.

## Global scoring contract

Every empirical test below must freeze before outcome feedback:

- input timestamp/location and question wording;
- Baseline Firewall classification;
- method layer;
- setup method/calibration and seasonal-alignment method;
- time-boundary system;
- time family;
- deity/state system where relevant;
- Role Map;
- eligible features;
- finite discriminative prediction branches and primary branch/weights;
- timing window/tolerance;
- abstention criteria;
- allowed auxiliary information.

Outcome states: `HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`.

Changing any frozen field after feedback creates a new model version; it cannot repair the original score.

A single outcome generates at most `CASE_LESSON_CANDIDATE`; it cannot directly create a new global rule.

## Test A — Setup calibration fork

Question: do 平气/定气 and 正授/超神/置闰/接气 variants produce meaningfully different and prospectively useful predictions?

Protocol:

1. Pre-register all eligible setup variants for a timestamp before the event outcome.
2. Generate each盘 independently and label it.
3. Apply the same downstream Role Map and scoring rubric where comparability allows.
4. Never select the variant that later fits best as the “true” chart.
5. Record setup divergence, prediction divergence, calibration, abstention and unresolved rates.

Failure condition: if variants differ often but none shows stable out-of-sample advantage, setup choice remains unresolved context rather than doctrine.

## Test B — Deity-system A/B

Question: does `勾陈/朱雀` vs `白虎/玄武` produce distinct repeatable value under matched conditions?

Protocol:

- same timestamps, plate, Role Map, questions and scoring;
- only deity-system interpretation changes;
- predictions frozen independently;
- no attribute borrowing across systems;
- compare discrimination/calibration, not retrospective narrative fit.

Failure condition: if both systems can retrospectively explain outcomes but do not prospectively discriminate, deity symbolism remains source-specific candidate material rather than an operational deciding layer.

## Test C — 九星 fixed label vs conditional model

Models:

- `M1`: fixed source吉凶 label only;
- `M2`: star + season + task + 旺相休囚 + contextual relations.

Use identical unknown-outcome cases and outcome categories.

Compare:

- discrimination;
- calibration;
- overconfident misses;
- abstention rate;
- robustness across task domains;
- complexity cost.

Strong support for M2 requires prospective improvement, not merely more elaborate retrospective narratives.

## Test D — 九星十二时辰应克 independent test

This family must be isolated from normal盘 reading.

Before each trial:

- choose only one explicit star/hour mapping path;
- convert traditional statements into predefined scorable event categories;
- define exact time windows and no-event conditions;
- estimate/collect base rates where feasible;
- prohibit standard盘 details from rescuing a miss.

Compare against:

- naive/base-rate forecast;
- shuffled hour labels;
- randomized event assignment where appropriate.

Failure condition: broad poetic matching without predeclared event classes is unscorable, not a hit.

## Test E — YEAR / MONTH / DAY / HOUR hierarchy

Source candidate: the book states a traditional hierarchy favoring nearer time layers.

Protocol:

1. Where all four time families can be generated, freeze all four independently.
2. Use the same target outcome dimensions.
3. Never choose the best layer after the result.
4. Compare predictive performance and calibration by horizon.

Possible outcomes:

- `SUPPORTS`
- `NARROWS`
- `CONTRADICTS`
- `CONTEXT_SPLIT_REQUIRED`

No hierarchy is promoted globally from book authority alone.

## Test F — Bureau lookup implementation integrity

Purpose: validate reproducibility and discrimination of implementation tests, not divination truth.

### F1 — Source topology / sparse oracle — DONE

梁书 source body mapping was re-reviewed after an initial main-reviewer one-bureau shift error.

Current source side:

- 18/18 bureau table bodies visible;
- 18/18 rows have two main-reviewed `甲子` sparse anchors;
- 36 tracked anchors total;
- p35/p36 scan-order swap preserved explicitly;
- former shifted mapping and Yin1→p49 are negative controls.

This established `ANCHORS_VERIFIED` before implementation comparison.

### F2 — Production Jiazi sparse comparison — PASSED

Production implementation tested:

`ziwei-core/src/main/kotlin/com/xuanxue/qimen/QimenEngine.kt`

Test commit:

`86e0b37d31549c0b2c16154ab1b8b81d83ebe454`

Exact-head Knowledge Engine V1 CI `#282`: `completed / success`.

Observed before the narrow fix:

- chief-star anchors: 18/18 matched;
- chief-door anchors: 16/18 matched;
- Yang-5 and Yin-5 exposed `CENTER_CHIEF_DOOR_IDENTITY`: production returned empty while source oracle = `死`.

The implementation was narrowed to return `天禽 / 死门` for chief identity when the旬首遁干 falls in center palace 5. This does **not** claim the full door-wheel hosting/rotation algorithm is verified.

The Kotlin regression test reads the tracked JSONL fixture rather than duplicating a second hard-coded oracle and passed:

- 18 positive Yang/Yin bureau comparisons;
- wrong-bureau controls;
- permuted star/door controls;
- explicit bureau-5 regression.

After the post-CI status commit itself passes exact-head CI, the 18 source rows may be treated as `IMPLEMENTATION_CHECKED` **only for their tracked Jiazi sparse-anchor scope**.

### F3 — Remaining implementation work

Still unverified:

- non-Jiazi cells of the 18 source tables;
- complete star rotation;
- complete eight-door rotation and center-host semantics;
- deity-system-specific rotation;
- setup boundary timestamps;
- wrong-time / shuffled full-chart controls.

Key interpretive audit question remains: can interpreters still tell convincing outcome stories from deliberately wrong or perturbed full-chart inputs? If yes, interpretation flexibility remains too high even if lookup code is correct.

## Test G — Auxiliary ablation

Compare:

- `A`: frozen standard盘 only;
- `B`: same standard盘 + preregistered hour-omen family;
- `C`: ritual material remains descriptive/research-only and excluded from outcome scoring.

Record delta A→B separately. Never credit B's incremental information to the standard盘 model.

The Baseline Firewall also requires separating `NEUTRAL_SETUP_FACTS` from `PREDICTIVE_AUXILIARY_FACTS` before freeze.

## Minimum evidence for model promotion

No fixed case count equals “validated”. Promotion requires a pattern of:

- preregistered prospective trials;
- independent outcomes;
- explicit misses retained;
- negative controls;
- contamination audit;
- calibration, not just hit count;
- performance against a reasonable baseline;
- stable applicability boundaries;
- evidence that added complexity improves out-of-sample discrimination.

Outcome-known, contaminated and book-retrospective cases receive zero Empirical Support credit by default. `PARTIAL` is an outcome class, not “half a validation”.

## Immediate priority after Test F sparse scope

1. Let the fixture-status/audit update itself pass exact-head CI before claiming final `IMPLEMENTATION_CHECKED` closure.
2. Keep full door/star/deity rotation explicitly experimental; do not inherit sparse-anchor credit upward.
3. Begin clean unknown-outcome prospective cases rather than indefinitely expanding source engineering.
4. Use the first real failures to decide which source-specific lineage question should be read next.
5. Run Test A/B/C/D only when their compared variants can be frozen without information leakage.
6. Periodically run Model Compression: delete/merge features, branches or context keys that do not add prospective discrimination/calibration.
