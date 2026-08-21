# K2 Prospective Case Protocol

Status: ACTIVE / v1.3

Purpose: turn anti-hindsight method constraints into a machine-auditable preregistration layer before real outcome feedback arrives. This protocol is research bookkeeping, not a claim that Qimen has predictive validity.

## 1. Why a tracked registry is needed

Historical failures show post-feedback freedom can enter through:

- changing setup method/calibration after seeing the result;
- changing solar-term alignment or day/子时 boundary;
- changing Role Map or eligible features;
- switching time families, deity systems, star/door state algorithms or auxiliary methods;
- adding news/background after the fact while crediting the gain to the original method;
- retaining only successful stories and silently losing misses;
- pre-registering so many branches that almost any outcome can later be called a hit;
- hiding unresolved choices behind permanent `CONTEXT_REQUIRED`.

The registry stores compact frozen metadata and hashes. Detailed/private case notes stay outside Git.

## 2. Registry

`knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

One row = one frozen model run. Parallel A/B variants for the same question require different `case_id` values and must be frozen before outcome feedback.

The registry may be empty. Empty is more truthful than fabricating a case merely to exercise the schema.

## 3. Required fields

The JSONL schema remains unchanged from v1.2. Each row contains:

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

No new top-level field is added merely because the methodology became more careful. New discipline should use the existing hashed local artifacts unless a future demonstrated need justifies schema expansion.

## 4. Main context fields

`method_layer`: `STANDARD_PLATE / TIME_FAMILY_VARIANT / HOUR_OMEN / RITUAL_AUXILIARY`.

`setup_method` is a non-empty source/method/version identifier, such as `FUTOU_ZHIRUN`, `CHAIBU_SOLAR_TERM`, `MAOSHAN_SOLAR_TERM`, `SOURCE_DEFINED_OTHER`, `NOT_APPLICABLE`.

`setup_calibration`: `PINGQI / DINGQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE`.

`seasonal_alignment`: `ZHENGSHOU / CHAOSHEN / ZHIRUN / JIEQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE`.

`time_boundary_system`: `CIVIL_MIDNIGHT / ZI_START_23 / SOURCE_DEFINED_OTHER / NOT_APPLICABLE`.

`time_family`: `YEAR / MONTH / DAY / HOUR / NOT_APPLICABLE`.

`deity_system`: `GOUCHEN_ZHUQUE / BAIHU_XUANWU / SOURCE_DEFINED_OTHER / NOT_APPLICABLE`.

`ritual_layer`: `EXCLUDED_BY_DEFAULT / RESEARCH_ONLY`.

A `RITUAL_AUXILIARY` row must always set `eligible_for_scoring=false`.

## 5. State-system fields

Every row freezes `star_state_system` and `door_state_system`. If a model does not use star/door seasonal state, write `NOT_APPLICABLE`.

A scored `FROZEN/RESOLVED` model may not leave either field as `CONTEXT_REQUIRED`.

## 6. Baseline Firewall inside the question packet

The local artifact hashed by `question_fingerprint_sha256` must distinguish:

### `NEUTRAL_SETUP_FACTS`

Only information required to identify the target and make it scorable: object identity, timestamp/location/timezone, question wording, horizon and scoring target/definition.

### `PREDICTIVE_AUXILIARY_FACTS`

Information that itself could predict the result: news, weather forecasts, market futures/odds/price action, subject history with direct predictive value, external omen, another divination system, or any near-answer clue.

If `PREDICTIVE_AUXILIARY_FACTS` are seen before method-only freeze, `auxiliary_information_policy` must not be `NONE`; normally use `PRE_EXPOSED` and treat attribution accordingly.

The fact that information is public or true does not make it neutral.

## 7. Branch-Discrimination requirements

The local artifact hashed by `competing_branches_sha256` must contain, where multiple branches exist:

- finite branch IDs;
- one pre-feedback primary branch, or pre-feedback probabilities/weights;
- discriminating observations for each branch;
- explicit failure conditions;
- outcome classes that do not overlap trivially.

A branch set is invalid for scoring if it effectively enumerates the full outcome space while allowing “any branch hit = model hit”.

Outcome audit scores the primary/probabilistic forecast and records secondary-branch behavior separately.

If branches cannot be observationally distinguished, merge them or mark the local forecast unscorable rather than manufacturing false precision.

## 8. Ambiguity Debt

`CONTEXT_REQUIRED` is not a permanent non-falsifiability device.

Before a scored model reaches `FROZEN`, any critical unresolved choice must be:

1. resolved;
2. split into explicit A/B cases;
3. removed from the model and marked `NOT_APPLICABLE`; or
4. left outside scoring in a tracked/local `AMBIGUITY_DEBT` note with the evidence needed for resolution.

A case cannot repeatedly escape scoring by moving essential decisions into unresolved context.

## 9. Freeze semantics

Before `status=FROZEN`, already fixed:

- question target and horizon;
- Baseline Firewall classification;
- method layer/family;
- setup method/calibration/alignment;
- time-boundary system;
- time family/layout/deity/state systems;
- Role Map;
- eligible feature set/patterns;
- finite discriminative competing branches;
- primary branch or weights;
- timing protocol;
- auxiliary policy;
- observable success/failure criteria.

`outcome_unknown_at_freeze=true` is required for any row later contributing to Empirical Support.

Changing a frozen field after feedback creates a new `case_id`; it cannot repair the original score.

## 10. Status lifecycle

Allowed: `PREREGISTERED -> FROZEN -> RESOLVED`, or `PREREGISTERED/FROZEN -> VOID`.

`RESOLVED` outcome: `HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`.

Non-RESOLVED row has `outcome_class=null`.

`VOID` is for unusable trials such as invalid input, known outcome before freeze or corrupted protocol. It is not a euphemism for a miss.

## 11. Auxiliary information and contamination

`auxiliary_information_policy`: `NONE / ALLOWED_AFTER_FREEZE / PRE_EXPOSED`.

Contamination flags remain:

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

## 12. Model-Compression obligation

Prospective accumulation is not only for promoting rules. It must also support deletion.

At periodic review, test whether any of the following can be removed/merged without degrading out-of-sample discrimination or calibration:

- context keys;
- eligible features;
- pattern families;
- branch count;
- fixed priority layers;
- auxiliary channels.

A more complex model does not beat a simpler one merely because it explains more retrospectively.

Compression decisions belong to later model versions; they never rewrite old frozen cases.

## 13. Source fidelity remains separate

`Source Fidelity != Lookup Determinism != Applicability != Empirical Support`

Passing source fixtures or runtime contracts means the implementation follows selected source/contract constraints. Qualified resolved prospective cases are still required for Empirical Support.

## 14. Privacy / copyright boundary

Tracked registry must not contain raw private conversations, identifying personal data, local filesystem paths or copied book passages/tables. Use hashes and coarse research metadata.

## 15. Validation ownership

A local helper may generate hashes/run validators but must not create synthetic cases, decide outcome labels, alter frozen protocols, grant empirical support, or commit/push unless separately delegated.

## 16. Current theory chain

`Reality Baseline`
-> `Baseline Firewall`
-> `Question Domain`
-> `Method-Layer Freeze`
-> `Setup/Time/Deity/State Freeze`
-> `Role Map Freeze`
-> `Bureau / Structural Lookup`
-> `Eligible Feature Set`
-> `Component / Relation Weaving`
-> `Pattern Registry`
-> `Competing Branches`
-> `Branch-Discrimination Gate`
-> `Frozen Prediction`
-> `Auxiliary Ablation`
-> `Outcome Audit`
-> `Rule Lifecycle Update`
-> `Model-Compression Review`

The protocol itself remains revisable when new loopholes appear.
