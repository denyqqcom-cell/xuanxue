# K2 Prospective Case Protocol

Status: ACTIVE

Purpose: turn the current anti-hindsight method constraints into a machine-auditable preregistration layer before real outcome feedback arrives.

This protocol is for research bookkeeping. It does not assert that Qimen has predictive validity.

## 1. Why a tracked registry is needed

A prose workflow can still drift in execution. The main recurring failure mode in the historical logs was not only wrong doctrine, but post-feedback freedom:

- changing setup/calibration after seeing the result;
- changing Role Map or eligible features;
- switching between time families, deity systems, or auxiliary methods;
- adding news/background after the fact while crediting the gain to the original method;
- retaining only successful stories and silently losing misses.

The registry therefore records compact hashes of the frozen protocol. Detailed case notes may remain local/private; the tracked registry must not contain unnecessary personal information.

## 2. Registry file

Tracked registry:

`knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

One row = one frozen model run. Parallel A/B variants for the same question must use different `case_id` values and must be frozen before outcome feedback.

The registry may be empty when no eligible prospective case has been run yet. Empty is more truthful than fabricating a case merely to exercise the schema.

## 3. Required fields

Each row must contain exactly:

- `case_id`
- `domain`
- `question_fingerprint_sha256`
- `question_domain`
- `method_family`
- `method_layer`
- `setup_calibration`
- `seasonal_alignment`
- `time_family`
- `layout_method`
- `deity_system`
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

Hashes point to the exact local/private frozen artifacts. They are not hashes of book pages or copyrighted text.

## 4. Method-layer fields

`method_layer`:

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

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

## 5. Freeze semantics

Before `status=FROZEN`, the following must already be fixed:

- question target and horizon;
- method layer and method family;
- setup calibration / seasonal alignment;
- time family / layout / deity system;
- Role Map;
- eligible feature set;
- competing interpretation branches;
- timing protocol;
- auxiliary-information policy;
- observable success/failure criteria in the local frozen artifact.

`outcome_unknown_at_freeze` must be `true` for any row that will later count toward empirical support.

Changing a frozen field after feedback creates a new `case_id`; it may not overwrite the original row and may not repair the original score.

## 6. Status lifecycle

Allowed:

`PREREGISTERED -> FROZEN -> RESOLVED`

or

`PREREGISTERED/FROZEN -> VOID`

`RESOLVED` requires one outcome class:

- `HIT`
- `PARTIAL`
- `MISS`
- `UNRESOLVED`
- `CONTAMINATED`

A non-`RESOLVED` row must have `outcome_class=null`.

`VOID` is for unusable trials such as invalid input, outcome known before freeze, or protocol corruption. It is not a euphemism for a miss.

## 7. Auxiliary information and contamination

`auxiliary_information_policy`:

- `NONE`
- `ALLOWED_AFTER_FREEZE`
- `PRE_EXPOSED`

Allowed contamination flags:

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

A contaminated trial remains in the registry. It is not deleted just because it cannot support the clean model.

## 8. Source fidelity is separate

A prospective case may use a source-defined bureau table or implementation fixture, but the following remain distinct:

`Source Fidelity != Lookup Determinism != Empirical Support`

Passing `K2_SOURCE_FIXTURES` means the implementation reproduces the selected source anchors. Only resolved prospective cases can later contribute to empirical support.

## 9. Privacy / copyright boundary

The tracked registry must not contain:

- raw private conversations;
- names, phone numbers, addresses, account identifiers, medical details, or other unnecessary personal data;
- local filesystem paths;
- copied book passages or table transcriptions.

Use hashes and coarse research metadata instead. Detailed private case packets stay outside Git.

## 10. Validation ownership

Project-side validators may reject malformed or hindsight-permissive rows.

A local helper may generate hashes or run validators, but it must not:

- create synthetic cases to make counts look better;
- decide outcome labels;
- change a frozen protocol after feedback;
- grant empirical support;
- commit/push unless explicitly delegated in a separate execution task.

## 11. Relationship to current theory

This protocol operationalizes, but does not freeze forever, the current chain:

`Reality Baseline`
-> `Question Domain`
-> `Method-Layer Freeze`
-> `Time Family + Setup Calibration + Seasonal Alignment Freeze`
-> `Deity-System / Layout Context Freeze`
-> `Role Map Freeze`
-> `Bureau / Structural Lookup`
-> `Eligible Feature Set`
-> `Contextual Relation Weaving`
-> `Competing Branches`
-> `Frozen Prediction`
-> `Auxiliary Ablation`
-> `Outcome Audit`
-> `Rule Lifecycle Update`

The protocol may itself be revised if prospective use exposes new loopholes.
