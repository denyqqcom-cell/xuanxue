# qimen-gongpan Source-Layer Migration Audit

Status: ACTIVE / RUNTIME-MIGRATED / SOURCE-REVIEW-INCOMPLETE

Purpose: document why the old宫盘 skill could not remain a flat symbolism table, and preserve unresolved source/system conflicts for later K2 review.

## 1. Category errors found in the legacy skill

The old file mixed these layers without clear boundaries:

- structural palace metadata;
- traditional symbolic lexicons;
- seasonal strength systems;
- role assignments;
- medical/body correspondences;
- fengshui-specific mappings;
- deterministic combination rules;
- high-risk real-world event claims.

The migration therefore separates:

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`.

## 2. Nine-star seasonal-state internal inconsistency

The same legacy file gave two incompatible examples for 天蓬:

- one section: `旺于亥子， 相于寅卯`;
- later “应用学体系” section: `旺于寅卯， 相于亥子`.

This difference changes the state label itself, so it cannot be hidden under “different wording”.

Status:

`SOURCE_INCONSISTENCY / STAR_STATE_SYSTEM_REQUIRED`

Operational consequence:

- no generic九星旺衰 calculation unless a specific source/system is frozen;
- no result-after selection of whichever state assignment fits the outcome;
- later source review must compare exact original pages and terminology.

## 3. Deity-system conflict

The old gongpan file assumes a `白虎 / 玄武` eight-deity set.

`QM-SRC-0001 / 梁湘潤《奇門遁甲入門》` visibly uses `勾陈 / 朱雀` in the corresponding positions.

Status:

`CONTEXT_SPLIT_REQUIRED`.

Operational consequence:

`deity_system` is a first-class frozen field. Attribute borrowing between systems is forbidden unless a source-specific mapping is justified before feedback.

## 4. Deterministic combination table removed

The old file contained rules equivalent to:

- 吉星 + 吉门 + 吉神 → 大吉;
- 凶星 + 凶门 → 大凶;
- 吉神 automatically mitigates;
- 凶神 automatically worsens.

Problems:

- no calibrated weights;
- possible duplicate counting of the same underlying structure;
- source labels were treated as commensurable numerical evidence;
- Role Map and task context were bypassed.

Status:

`DEPRECATED_AS_GLOBAL_RULE`.

Replacement:

`component -> role -> relation -> contrary evidence -> competing branches`.

## 5. Fixed five-layer order demoted

Old global order:

`九星 -> 八门 -> 八神 -> 八卦 -> 十干`.

Status:

`DEPRECATED_AS_GLOBAL_PRIORITY`.

Replacement:

`METHOD-FAMILY-SPECIFIC FEATURE ORDER` frozen before feedback when a method actually defines one.

## 6. High-risk person/event lexicons

Legacy tables associated stars, doors and deities with categories such as:

- criminals / thieves / deception;
- death / cancer / cardiovascular disease;
- traffic accidents / injury;
- imprisonment / lawsuits.

These are traditional symbolic lexicons, not factual classifiers.

Status:

`HIGH_RISK_SOURCE_SYMBOLISM`.

Operational consequence:

- no inference that a real person is a criminal or dishonest from a star/deity;
- no medical diagnosis/prognosis from palace/star/door symbolism;
- no automatic prediction of death, imprisonment or disaster from a single component.

## 7. Medical/body mappings demoted

The old file included palace-to-body, organ and disease mappings.

Status:

`SOURCE_ONLY / NON_MEDICAL_EVIDENCE`.

They may be retained for history-of-method study, but they cannot replace clinical evidence or professional medical judgment.

## 8. Fengshui-specific rules separated from general宫盘

The old file embedded a fengshui method with rules such as `日干=人 / 时干=宅` and strong good/bad conclusions from their relation.

Status:

`METHOD_SPECIFIC_SOURCE`.

Operational consequence:

- only eligible under a frozen `method_family=FENGSHUI`;
- Role Map must be frozen;
- physical-building claims still require real inspection/evidence;
- the fengshui rule cannot override a normal Qimen case merely because the symbols are present.

## 9. Provenance correction

The old file repeatedly wrote `《奇门遁甲应用学》佚名`.

K2 verified metadata identifies the reviewed work as authored by **王云鹏**.

Status:

`PROVENANCE_CORRECTED`.

This corrects attribution only. It does not promote any traditional claim to empirical truth.

## 10. Runtime result

After migration, qimen-gongpan no longer acts as a deterministic symbolism dictionary. It acts as a component and relation registry constrained by:

- method layer / family;
- deity system;
- source-specific state system;
- frozen Role Map;
- eligible features;
- relation graph;
- contrary evidence;
- prospective freeze.

Remaining source work:

- visually verify competing九星旺衰 systems at page level;
- trace old body/fengshui tables to their original pages;
- compare white-tiger/black-tortoise vs gouchen/zhuque deity lineages prospectively only after source definitions are stable.

*Migration audit v1 | 2026-08-21*
