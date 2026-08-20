# K2 Prospective Case Protocol

Status: ACTIVE / v1.2

Purpose: turn anti-hindsight method constraints into a machine-auditable preregistration layer before real outcome feedback arrives. This protocol is research bookkeeping, not a claim that Qimen has predictive validity.

## 1. Why a tracked registry is needed

Historical failures show post-feedback freedom can enter through:

- changing setup method or calibration after seeing the result;
- changing solar-term alignment or day/子时 boundary;
- changing Role Map or eligible features;
- switching time families, deity systems, star/door state algorithms, or auxiliary methods;
- adding news/background after the fact while crediting the gain to the original method;
- retaining only successful stories and silently losing misses.

The registry stores compact frozen metadata and hashes. Detailed/private case notes stay outside Git.

## 2. Registry

`knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

One row = one frozen model run. Parallel A/B variants for the same question require different `case_id` values and must be frozen before outcome feedback.

The registry may be empty. Empty is more truthful than fabricating a case merely to exercise the schema.

## 3. Required fields

Each row must contain exactly:

- `case_id`
- `domain`
- `question_fingerprint_sha256`
- `question_domain`
- `method_family`
- `method_layer`
- `setup_method`
- `setup_calibration`
- `seasonal_alignment`
- `time_boundary_system`
- `time_family`
- `layout_method`
- `deity_system`
- `star_state_system`
- `door_state_system`
- `hour_omen_family`
- `ritual_layer`
- `bureau_table_source`
- `role_map_sha256`
- `eligible_features_sha256`
- `competing_branches_sha256`
- `timing_protocol_sha256`
- `auxiliary_information_policy`
- `outcome_unknown_at_freeze`
- `eligible_for_scoring`
- `freeze_timestamp`
- `status`
- `outcome_class`
- `contamination_flags`
- `review_status`

Hashes point to exact local/private frozen artifacts, not book pages.

## 4. Main context fields

`method_layer`:

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

`setup_method` is a non-empty source/method/version identifier, for example:

- `FUTOU_ZHIRUN`
- `CHAIBU_SOLAR_TERM`
- `MAOSHAN_SOLAR_TERM`
- `SOURCE_DEFINED_OTHER`
- `NOT_APPLICABLE`

This field freezes the algorithm family. It does not assert that any named method is correct.

`setup_calibration`:

- `PINGQI`
- `DINGQI`
- `SOURCE_DEFINED_OTHER`
- `NOT_APPLICABLE`

`seasonal_alignment`:

- `ZHENGSHOU`
- `CHAOSHEN`
- `ZHIRUN`
- `JIEQI`
- `SOURCE_DEFINED_OTHER`
- `NOT_APPLICABLE`

`time_boundary_system` is a non-empty identifier for civil-day / 子时 boundary handling, such as:

- `CIVIL_MIDNIGHT`
- `ZI_START_23`
- `SOURCE_DEFINED_OTHER`
- `NOT_APPLICABLE`

If competing boundary rules generate different plates, use separate A/B cases. The registry does not choose which rule is metaphysically correct.

`time_family`:

- `YEAR`
- `MONTH`
- `DAY`
- `HOUR`
- `NOT_APPLICABLE`

`deity_system`:

- `GOUCHEN_ZHUQUE`
- `BAIHU_XUANWU`
- `SOURCE_DEFINED_OTHER`
- `NOT_APPLICABLE`

`ritual_layer`:

- `EXCLUDED_BY_DEFAULT`
- `RESEARCH_ONLY`

A `RITUAL_AUXILIARY` row must always set `eligible_for_scoring=false`.

## 5. State-system fields

Every row freezes:

- `star_state_system`
- `door_state_system`

If a model does not use star/door seasonal state, write `NOT_APPLICABLE`.

A scored `FROZEN/RESOLVED` model may not leave either field as `CONTEXT_REQUIRED`. If the state algorithm is unresolved, resolve it before freeze, remove those features and use `NOT_APPLICABLE`, or run explicit A/B models.

## 6. Freeze semantics

Before `status=FROZEN`, already fixed:

- question target and horizon;
- method layer/family;
- setup method, setup calibration and seasonal alignment;
- time-boundary system;
- time family / layout / deity system;
- star-state and door-state systems if used;
- Role Map;
- eligible feature set / patterns;
- competing branches;
- timing protocol;
- auxiliary policy;
- observable success/failure criteria in local artifact.

`outcome_unknown_at_freeze=true` is required for any row later contributing to empirical support.

Changing a frozen field after feedback creates a new `case_id`; it cannot repair the original score.

## 7. Status lifecycle

Allowed:

`PREREGISTERED -> FROZEN -> RESOLVED`

or

`PREREGISTERED/FROZEN -> VOID`

`RESOLVED` outcome:

- `HIT`
- `PARTIAL`
- `MISS`
- `UNRESOLVED`
- `CONTAMINATED`

Non-RESOLVED row has `outcome_class=null`.

`VOID` is for unusable trials such as invalid input, known outcome before freeze, or corrupted protocol. It is not a euphemism for a miss.

## 8. Auxiliary information and contamination

`auxiliary_information_policy`:

- `NONE`
- `ALLOWED_AFTER_FREEZE`
- `PRE_EXPOSED`

Contamination flags:

- `AUXILIARY_CONTAMINATION`
- `PRIOR_SOCIAL_INFORMATION`
- `EXTERNAL_OMEN`
- `CROSS_METHOD_CONFIRMATION`
- `POST_FEEDBACK_ROLE_SWITCH`
- `POST_FEEDBACK_FACTOR_SWITCH`
- `POST_FEEDBACK_METHOD_SWITCH`
- `POST_FEEDBACK_TIMING_SWITCH`
- `INVALID_INPUT_ACCEPTED_POST_HOC`
- `OTHER`

A contaminated trial remains in the registry.

Changing `setup_method`, `time_boundary_system`, `star_state_system` or `door_state_system` after feedback is a model/method/factor switch and must not repair the old score.

## 9. Source fidelity remains separate

`Source Fidelity != Lookup Determinism != Empirical Support`

Passing source fixtures or runtime contracts means the implementation follows selected source/contract constraints. Only qualified resolved prospective cases may contribute to Empirical Support.

## 10. Privacy / copyright boundary

Tracked registry must not contain raw private conversations, identifying personal data, local filesystem paths, or copied book passages/tables. Use hashes and coarse research metadata.

## 11. Validation ownership

A local helper may generate hashes/run validators but must not create synthetic cases, decide outcome labels, alter frozen protocols, grant empirical support, or commit/push unless separately delegated.

## 12. Current theory chain

`Reality Baseline`
-> `Question Domain`
-> `Method-Layer Freeze`
-> `Setup Method + Calibration + Seasonal Alignment Freeze`
-> `Time-Boundary + Time-Family Freeze`
-> `Deity-System / Layout Context Freeze`
-> `State-System Freeze`
-> `Role Map Freeze`
-> `Bureau / Structural Lookup`
-> `Eligible Feature Set`
-> `Component / Relation Weaving`
-> `Pattern Registry`
-> `Competing Branches`
-> `Frozen Prediction`
-> `Auxiliary Ablation`
-> `Outcome Audit`
-> `Rule Lifecycle Update`

The protocol itself remains revisable when new loopholes appear.
