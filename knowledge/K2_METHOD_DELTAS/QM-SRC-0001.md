# QM-SRC-0001 Method Delta — 梁湘润《奇门遁甲入门》

Status: PROVISIONAL / POST-READING

Source: `QM-SRC-0001 / WORK-000217`

Reading basis: canonical 57-page SCAN, `VISUAL_PAGE`, full p1-p57 review.

This document is a project inference artifact. It is **not** source Evidence and does not promote any traditional rule to truth.

## 1. Why this book changes the method model

The strongest lesson from this source is not a new fixed verdict. It is that one short introductory book already contains several materially different method layers:

- 三元/时家排局；
- 正授、超神、置闰、接气与平气/定气校准；
- 年家、月家、日家、时家时间族；
- 九星的季节/事项条件化解释；
- 九星十二时辰应克的独立时辰占验；
- 大量符咒、反闭、步斗、六戊、禁敌等仪式材料。

If all of them are simultaneously eligible, almost any result can acquire a post-hoc explanation. The next iteration therefore reduces degrees of freedom before adding interpretive power.

## 2. New Method-Layer Gate

Before reading a盘 or making a prediction, freeze one primary layer:

1. `STANDARD_PLATE`
   - ordinary 三元/时家排局 and盘面 interpretation.
2. `TIME_FAMILY_VARIANT`
   - YEAR / MONTH / DAY / HOUR methods treated as distinct algorithms.
3. `HOUR_OMEN`
   - 九星十二时辰应克; independently scored method family.
4. `RITUAL_AUXILIARY`
   - 符咒、反闭、步斗、六戊、禁敌 etc.; `eligible=false` by default for prediction scoring.

A result from one layer may not rescue a miss in another layer unless the auxiliary layer was explicitly preregistered before feedback and its incremental contribution is scored separately.

## 3. New first-class context keys

The current theory gains these explicit fields:

```text
method_layer = STANDARD_PLATE | TIME_FAMILY_VARIANT | HOUR_OMEN | RITUAL_AUXILIARY
setup_calibration = PINGQI | DINGQI | SOURCE_DEFINED_OTHER
seasonal_alignment = ZHENGSHOU | CHAOSHEN | ZHIRUN | JIEQI | SOURCE_DEFINED_OTHER
time_family = YEAR | MONTH | DAY | HOUR
deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER
hour_omen_family = NONE | NINE_STAR_TWELVE-HOUR | SOURCE_DEFINED_OTHER
ritual_layer = EXCLUDED_BY_DEFAULT | RESEARCH_ONLY
bureau_table_source = LIANG_18_BUREAU | OTHER
```

Unknown values remain `CONTEXT_REQUIRED`; they must not be guessed from whichever choice fits the outcome.

## 4. Deity-System Context

The source's eight-deity list uses `勾陈 / 朱雀` where the current modern baseline often uses `白虎 / 玄武`.

New rule:

- never silently rename one list into the other;
- never mix attributes from both lists in one prediction unless a source-specific mapping has been explicitly justified before feedback;
- conflicts are decomposed by source/version/layout/application context first;
- if still unresolved, retain parallel models and compare prospectively.

This is a concrete example of why “many books say similar things” cannot substitute for lineage-aware evidence.

## 5. Lookup Determinism, not Predictive Truth

The 18阳/阴遁 bureau tables have a useful methodological property: once time family,局数 and setup system are frozen, the subsequent placement is mechanically auditable.

That deserves a separate concept:

`Lookup Determinism = reproducibility of the source-defined setup`

It is **not**:

`Predictive Validity = ability to forecast reality`

The project should prefer deterministic lookup/algorithm steps where possible because they reduce implementation drift and hindsight freedom, while keeping outcome validation completely separate.

## 6. Refined Symbol-to-Verdict Gate

The 九星 section itself weakens naive global labels: fixed吉凶 categories coexist with season, task and旺相休囚 modifiers.

Therefore the operational path becomes:

`symbol -> source-defined state -> task/season/context -> relation to role/other features -> competing branches -> prediction`

not:

`symbol -> fixed verdict`.

Traditional “吉/凶” labels remain candidate priors at most until prospectively supported in a specified context.

## 7. Time-Family hierarchy is demoted, not deleted

The source proposes a traditional hierarchy in which nearer time levels are treated as stronger than broader ones.

Project treatment:

- retain it as `TESTABLE_CANDIDATE`;
- do not make it a global priority rule;
- compare YEAR/MONTH/DAY/HOUR prospectively under the same scoring protocol;
- allow later outcomes to SUPPORT / NARROW / REJECT the hierarchy.

## 8. Hour-Omen family becomes separately testable

`九星十二时辰应克` is too structurally distinct to be a casual extra signal.

It gets its own family with:

- predefined event categories;
- predefined time windows;
- base-rate controls;
- abstention rules;
- no standard盘 information in the primary test;
- no after-the-fact reinterpretation of broad poetic phrases.

If it fails under this stricter protocol, its source existence remains recorded but its empirical status falls.

## 9. Ritual Exclusion Default

The ritual chapters are valuable for understanding historical/system scope, but not for ordinary predictive scoring.

Default:

`RITUAL_AUXILIARY.eligible = false`

They may be studied as historical/ritual material, but supernatural causal claims, gambling guidance, coercive enemy-disable claims and similar content do not enter the operational prediction model.

## 10. Updated core inference chain

Current candidate theory becomes:

`Reality Baseline`
→ `Question Domain`
→ `Method-Layer Freeze`
→ `Time Family + Setup Calibration + Seasonal Alignment Freeze`
→ `Deity-System / Layout Context Freeze`
→ `Role Map Freeze`
→ `Bureau / Structural Lookup`
→ `Eligible Feature Set`
→ `Contextual Relation Weaving`
→ `Competing Branches`
→ `Frozen Prediction`
→ `Auxiliary Ablation`
→ `Outcome Audit`
→ `Rule Lifecycle Update`

This is an incremental change, not a final theory.

## 11. What this book did NOT establish

The full 57-page reading does not establish that:

- 梁湘润's chosen source lineage is historically correct;
- one setup calibration is more accurate than another;
- 勾陈/朱雀 is empirically superior to白虎/玄武;
- the 18 bureau tables predict reality merely because they are internally deterministic;
- 九星十二时辰应克 has predictive power;
- ritual/符咒/步斗 claims have causal efficacy;
- year/month/day/hour hierarchy is empirically valid.

Those questions move to prospective testing, not doctrinal acceptance.
