# 奇门受约束情境推演工作流 v2.2

> 本模板用于保存一次解盘从原始输入到冻结预测、辅助信息增量与结果审计的全过程。
>
> 上位约束：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`、`qimen-overview/SKILL.md`、`_AGENT_INSTRUCTIONS.md`。

## 一、核心链

```text
Reality Baseline
-> Question Domain
-> Method-Layer Freeze
-> Setup / Time / Deity Freeze
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

原则：一个方法层的 miss 不得由另一层结果后救援；一个 state system 的 miss 也不得通过结果后切换旺衰算法修补。

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
├── claw_AUGMENTED_PREDICTION_YYYYMMDD.md      # 可选
├── claw_OUTCOME_AUDIT_YYYYMMDD.md             # 结果已知后
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

原始输入与已知事实不得在结果后覆盖。私人信息不进入 tracked registry。

## 四、Reality Baseline

```markdown
# Reality Baseline
## Object existence
...
## Known facts
...
## Unknown target
...
## Time horizon
...
## Base-rate considerations
...
## Safety / professional-boundary notes
...
```

这里不做盘面吉凶判断。

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

- `RITUAL_AUXILIARY` 默认不评分；
- A/B 必须反馈前建立独立 `case_id`；
- STANDARD_PLATE miss 后不得临时切 HOUR_OMEN 或其他 time family 救援。

## 六、Setup / Layout / Time / Deity / State-System Freeze

```markdown
# Setup Freeze
- setup_method:
- setup_calibration: PINGQI / DINGQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
- seasonal_alignment: ZHENGSHOU / CHAOSHEN / ZHIRUN / JIEQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
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
- school_context:
- plate_self_check:
- frozen_at:
```

### State-System rules

- 如果本模型不使用九星/八门季节状态，写 `NOT_APPLICABLE`；
- 如果要使用，必须写明确 source/method identifier；
- 可评分的 FROZEN model 不得把 `star_state_system` 或 `door_state_system` 留成 `CONTEXT_REQUIRED`；
- 不同系统需 A/B 独立冻结；
- 结果后换 state system 不得修补原预测。

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

只负责可机械核验的结构：阴阳遁、局数、值符值使、星门神宫位置、旬空马星、source-defined bureau lookup 等。

```markdown
# Structural Lookup
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

未进入 IN 的信息，结果后不得补入救援。仪式、符咒、博奕、禁敌默认 OUT。

## 十、Component / Relation Analysis

宫盘至少区分：

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
## Source / Inference split
- SOURCE:
- INFERENCE:
- EMPIRICAL_SUPPORT:
- CONTAMINATION:
```

禁止固定星门神加总、旺衰乘数和“四害自动打折”。

## 十一、Pattern Registry

格局由 `qimen-gexia` 处理，至少区分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

进入本次预测的 Pattern 必须已在 Eligible Feature Set 中，且结构/来源/适用域可说明。同一底层结构不得因多个格名重复计票。

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

存在真实多解时保留多解，不用叙事连贯性冒充证据。

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

内外盘当前结构：阳遁内 `1、8、3、4`、外 `9、2、7、6`；阴遁反转。“内快外慢”不是固定天数系数。

## 十四、Frozen Prediction

```markdown
# Frozen Prediction
## Protocol
- case_id:
- question_fingerprint_sha256:
- question_domain:
- method_family:
- method_layer:
- setup_calibration:
- seasonal_alignment:
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

信息不足可 `INSUFFICIENT_EVIDENCE`；方法不适用可 `OUT_OF_SCOPE`；无法评分可 `UNSCORABLE`。

正式前瞻案例同步到 `K2_PROSPECTIVE_CASE_REGISTRY.jsonl`。

## 十五、Auxiliary Context Ablation

```markdown
# Augmented Prediction
## Frozen method-only reference
...
## Added information
- news:
- user background:
- external omen:
- other method:
## Augmentation delta
- what changed:
- why:
## Attribution
method-only contribution:
auxiliary contribution:
```

辅助信息不能回写成原 method-only “本来就看到了”。

## 十六、Outcome Audit

```markdown
# Outcome Audit
## Actual outcome
...
## Frozen score
- outcome_class: HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED
- exact_hit:
- within_window:
- unscorable:
## Error class
INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR /
METHOD_LAYER_ERROR / SETUP_CALIBRATION_ERROR / DEITY_SYSTEM_ERROR /
STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR /
TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION /
UNSPECIFIED_MODEL_FAILURE
## Post-feedback changes observed
- role_switch:
- factor_switch:
- method_switch:
- method_layer_switch:
- setup_calibration_switch:
- deity_system_switch:
- star_state_system_switch:
- door_state_system_switch:
- time_family_switch:
- timing_rule_switch:
- external_information_added:
## Contamination flags
...
## Rule lifecycle decision
KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT
```

成功与失败都保留。污染案例不能删除。

## 十七、Prospective Registry Gate

正式未知结果测试必须遵守 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`。结果后任何冻结字段变化都必须产生新 `case_id`，不得覆盖原记录。

## 十八、final_case_summary.md

```markdown
# Final Case Summary
## 原问题
...
## 冻结协议
...
## 冻结预测
...
## 辅助信息增量
...
## 实际结果
...
## 评分与污染状态
...
## 最大误差来源
...
## 对当前理论的影响
...
```

## 十九、文献引用与方法权威

- 原书断语：SOURCE；
- 项目转译：INFERENCE；
- 前瞻结果：EMPIRICAL_SUPPORT；
- 新闻/背景/外应：CONTAMINATION/AUXILIARY。

多个古籍一致只说明 SOURCE consensus，不自动证明现实有效。

---

*Workflow v2.2 | 2026-08-21 | 加入 State-System Freeze / Component-Relation / Pattern Registry Gate*
