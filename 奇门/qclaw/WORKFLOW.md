# 奇门受约束情境推演工作流 v2.3

> 本模板用于保存一次解盘从原始输入到冻结预测、辅助信息增量与结果审计的全过程。
>
> 上位约束：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`、`qimen-overview/SKILL.md`、`_AGENT_INSTRUCTIONS.md`。

## 一、核心链

```text
Reality Baseline
-> Question Domain
-> Method-Layer Freeze
-> Setup Method / Calibration / Seasonal Alignment Freeze
-> Time-Boundary / Time-Family / Layout / Deity Freeze
-> State-System Freeze
-> Role Map Freeze
-> Structural Lookup
-> Eligible Feature Set
-> Component / Relation Analysis
-> Pattern Registry
-> Competing Branches
-> Timing Freeze
-> Frozen Prediction
-> Prospective Registry
-> Auxiliary Ablation
-> Outcome Audit
```

原则：一个方法层的 miss 不得由另一层结果后救援；起局法、日界规则或旺衰系统也不得结果后切换来修补原模型。

## 二、推荐案例目录

```text
YYYYMMDD_问题关键词_时分/
├── _META.md
├── claw_00_reality_baseline.md
├── claw_01_method_family.md
├── claw_02_setup_freeze.md
├── claw_03_role_map.md
├── claw_04_structural_lookup.md
├── claw_05_eligible_features.md
├── claw_06_relational_inference.md
├── claw_07_competing_branches.md
├── claw_08_timing_freeze.md
├── claw_FROZEN_PREDICTION_YYYYMMDD.md
├── claw_AUGMENTED_PREDICTION_YYYYMMDD.md
├── claw_OUTCOME_AUDIT_YYYYMMDD.md
└── final_case_summary.md
```

## 三、_META.md

```markdown
# Case Metadata
- case_id:
- question_raw:
- question_normalized:
- question_fingerprint_sha256:
- prediction_time:
- location:
- input_plate_source:
- known_facts_before_prediction:
- outcome_unknown_at_freeze: true/false
- auxiliary_information_policy: NONE / ALLOWED_AFTER_FREEZE / PRE_EXPOSED
- tracked_registry_eligible: true/false
- created_at:
```

原始输入与已知事实不得结果后覆盖。私人信息不进入 tracked registry。

## 四、Reality Baseline

确认对象存在、已知/未知、时间范围、基础概率、安全边界。这里不做盘面吉凶。

## 五、Question / Method-Layer Freeze

```markdown
# Question / Method Layer
- question_domain:
- method_family:
- method_layer: STANDARD_PLATE / TIME_FAMILY_VARIANT / HOUR_OMEN / RITUAL_AUXILIARY
- alternative_model_id:
- reason:
- eligible_for_scoring: true/false
```

`RITUAL_AUXILIARY` 默认不评分；A/B 反馈前独立建 `case_id`。

## 六、Setup / Time / Deity / State-System Freeze

```markdown
# Setup Freeze
- setup_method: FUTOU_ZHIRUN / CHAIBU_SOLAR_TERM / MAOSHAN_SOLAR_TERM / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
- setup_method_version/source:
- setup_calibration: PINGQI / DINGQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
- seasonal_alignment: ZHENGSHOU / CHAOSHEN / ZHIRUN / JIEQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
- time_boundary_system: CIVIL_MIDNIGHT / ZI_START_23 / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
- yin_yang_dun:
- ju_number:
- layout_method:
- time_family: YEAR / MONTH / DAY / HOUR / NOT_APPLICABLE
- deity_system: GOUCHEN_ZHUQUE / BAIHU_XUANWU / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
- star_state_system:
- door_state_system:
- hour_omen_family:
- ritual_layer: EXCLUDED_BY_DEFAULT / RESEARCH_ONLY
- bureau_table_source:
- solar_term_timestamp_source:
- input_timezone:
- school_context:
- plate_self_check:
- frozen_at:
```

规则：

- setup method、日界/子时、八神、state system 都是可改变整盘/解释的模型选择；
- 不使用的字段写 `NOT_APPLICABLE`；
- 可评分 FROZEN model 不得把 `setup_method / time_boundary_system / star_state_system / door_state_system` 留为 `CONTEXT_REQUIRED`；
- 竞争选择需反馈前独立 A/B；
- 结果后切换不能修补原预测。

## 七、Role Map Freeze

```markdown
# Role Map
| Role | Symbol / Palace | Basis | Alternative |
|---|---|---|---|
| 求测者 | ... | SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED | ... |
| 事件 | ... | ... | ... |
| 对方 | ... | ... | ... |
role_map_sha256:
```

反馈后换用神标 `POST_FEEDBACK_ROLE_SWITCH`。

## 八、Structural Lookup

只负责机械结构：阴阳遁、局数、值符值使、星门神位置、旬空马星、source-defined bureau lookup 等。

```markdown
# Structural Lookup
- setup_method:
- time_boundary_system:
- bureau_table_source:
- source_fixture_family:
- source_fixture_status:
- implementation_version:
- input_hash:
- output_hash:
- self_check:
```

`Source Fidelity != Lookup Determinism != Predictive Validity`。

## 九、Eligible Feature Set

```markdown
# Eligible Feature Set
IN:
- ...
OUT:
- ...
Priority rule within this method family:
- NONE / ...
Reason:
...
eligible_features_sha256:
```

未进入 IN 的信息结果后不得补入。仪式、博奕、禁敌默认 OUT。

## 十、Component / Relation Analysis

宫盘先分：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

```markdown
# Relational Inference
## Primary relations
...
## State features
- star_state_system:
- door_state_system:
- 空亡：结构 + 作用对象 + 当前解释
- 入墓：结构 + 作用对象 + 当前解释
- 击刑：结构 + 作用对象 + 当前解释
- 门迫：结构 + 作用对象 + 当前解释
## Contrary evidence
...
## Epistemic split
- SOURCE:
- INFERENCE:
- EMPIRICAL_SUPPORT:
- CONTAMINATION:
```

禁止固定星门神加总、旺衰乘数和四害自动折扣。

## 十一、Pattern Registry

格局由 `qimen-gexia` 处理：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

必须预先进入 Eligible Feature Set；同一底层结构不得多格名重复计票。

## 十二、Competing Branches

```markdown
# Competing Interpretation Branches
## H1
- assumptions:
- evidence:
- predicted observation:
- failure_condition:
## H2
- assumptions:
- evidence:
- predicted observation:
- failure_condition:
competing_branches_sha256:
```

叙事连贯性不等于证据。

## 十三、Timing Freeze

```markdown
# Timing Freeze
- prediction_horizon:
- resolution_target:
- timing_method_family:
- eligible_timing_features:
- main_window:
- scoring_tolerance:
- alternative_window:
- timing_protocol_sha256:
```

阳遁内 `1、8、3、4`、外 `9、2、7、6`；阴遁反转。“内快外慢”不是固定天数系数。

## 十四、Frozen Prediction

```markdown
# Frozen Prediction
## Protocol
- case_id:
- question_fingerprint_sha256:
- question_domain:
- method_family:
- method_layer:
- setup_method:
- setup_calibration:
- seasonal_alignment:
- time_boundary_system:
- layout_method:
- time_family:
- deity_system:
- star_state_system:
- door_state_system:
- hour_omen_family:
- ritual_layer:
- bureau_table_source:
- role_map_sha256:
- eligible_features_sha256:
- competing_branches_sha256:
- timing_protocol_sha256:
- auxiliary_information_policy:
## Main prediction
- outcome/direction:
- time_window:
- observable_success_criteria:
- observable_failure_criteria:
## Alternatives
...
## Confidence split
- source_fidelity:
- applicability:
- empirical_support:
## Freeze
- timestamp:
- outcome_unknown_at_freeze: true/false
- immutable_after_outcome_feedback: true
```

允许 `INSUFFICIENT_EVIDENCE / OUT_OF_SCOPE / UNSCORABLE`。正式前瞻案例同步 Prospective Registry。

## 十五、Auxiliary Context Ablation

先 freeze method-only，再加入 news/background/external omen/other method，记录 augmentation delta 与 attribution。不能回写成原预测本来就包含这些信息。

## 十六、Outcome Audit

```markdown
# Outcome Audit
## Actual outcome
...
## Frozen score
- outcome_class: HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED
## Error class
INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR /
METHOD_LAYER_ERROR / SETUP_METHOD_ERROR / SETUP_CALIBRATION_ERROR /
TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR /
FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR /
BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE
## Post-feedback changes observed
- setup_method_switch:
- setup_calibration_switch:
- time_boundary_system_switch:
- method_layer_switch:
- time_family_switch:
- deity_system_switch:
- star_state_system_switch:
- door_state_system_switch:
- role_switch:
- factor_switch:
- timing_rule_switch:
- external_information_added:
## Contamination flags
...
## Rule lifecycle decision
KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT
```

成功、失败、污染都保留。

## 十七、Prospective Registry Gate

正式未知结果测试遵守 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`。任何冻结字段结果后变化都必须新建 `case_id`。

## 十八、final_case_summary.md

记录原问题、冻结协议、冻结预测、辅助信息增量、实际结果、评分/污染、最大误差来源、对理论影响。

## 十九、文献与经验支持

原书断语=SOURCE；项目转译=INFERENCE；合格前瞻结果=EMPIRICAL_SUPPORT；背景/外应=CONTAMINATION/AUXILIARY。多书一致不自动等于现实有效。

---

*Workflow v2.3 | 2026-08-21 | Setup Method / Time-Boundary / State-System 全链冻结*
