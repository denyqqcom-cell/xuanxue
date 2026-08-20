# 奇门受约束情境推演工作流 v2.1

> 本模板用于保存一次解盘从原始输入到冻结预测、辅助信息增量与结果审计的全过程。
>
> 上位约束：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`、`qimen-overview/SKILL.md`、`_AGENT_INSTRUCTIONS.md`。

## 一、核心变化

旧工作流按固定八步输出，并要求每一步都必须明确吉凶、最终必须给成败与应期。这会在证据不足时制造确定性，也容易让不同书的规则在同一盘中无限叠加。

v2.1 改为：

`Reality Baseline -> Question Domain -> Method-Layer Freeze -> Setup/Time/Deity Freeze -> Role Map -> Structural Lookup -> Eligible Features -> Relational Inference -> Competing Branches -> Timing Freeze -> Frozen Prediction -> Auxiliary Ablation -> Outcome Audit`

新增原则：**一个方法层的 miss 不得由另一个方法层在结果后救援。**

---

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

旧 `claw_问题分类 / 看大局 / 取用神 / 查四害 / 析宫盘 / 看生克 / 格局详解` 文件可为兼容历史案例继续存在，但新案例不再强制按这些文件拆分。

---

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

原始输入与初始已知事实不得在结果后覆盖。若案例涉及私人信息，Git 仓库只保存哈希与粗粒度研究元数据。

---

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

---

## 五、Question / Method-Layer Freeze

先冻结问题域与主方法层：

```markdown
# Question / Method Layer
- question_domain:
- method_family:
- method_layer: STANDARD_PLATE / TIME_FAMILY_VARIANT / HOUR_OMEN / RITUAL_AUXILIARY
- alternative_model_id:
- reason:
- eligible_for_scoring: true/false
```

规则：

- `RITUAL_AUXILIARY` 默认 `eligible_for_scoring=false`；
- 若比较多个方法层，A/B 都必须在反馈前建立独立 `case_id`；
- 不允许标准盘 miss 后临时调用 HOUR_OMEN、年/月/日家或仪式层补救。

输出：`claw_01_method_family.md`

---

## 六、Setup / Layout / Time / Deity Freeze

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
- hour_omen_family:
- ritual_layer: EXCLUDED_BY_DEFAULT / RESEARCH_ONLY
- bureau_table_source:
- school_context:
- plate_self_check:
- frozen_at:
```

若比较不同起局法、节气校准、八神体系或时间族，必须并行冻结独立模型，而不是结果后挑一套。

输出：`claw_02_setup_freeze.md`

---

## 七、Role Map

```markdown
# Role Map

| Role | Symbol / Palace | Basis | Alternative |
|---|---|---|---|
| 求测者 | ... | SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED | ... |
| 事件 | ... | ... | ... |
| 对方 | ... | ... | ... |

role_map_sha256:
```

反馈后换用神必须在 Outcome Audit 标记为 `POST_FEEDBACK_ROLE_SWITCH`，不能覆盖原 Role Map。

---

## 八、Structural Lookup

此步骤只负责可机械核验的结构输入，例如：

- 阴阳遁与局数；
- 值符、值使；
- 宫位与九星/八门/八神位置；
- source-defined bureau table lookup；
- 旬空、马星等结构。

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

必须牢记：

`Source Fidelity != Lookup Determinism != Predictive Validity`

排盘正确只说明结构执行正确，不说明预测有效。

输出：`claw_04_structural_lookup.md`

---

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

未进入 IN 的信息，结果后不得补入救援。

仪式、符咒、博奕、禁敌材料默认 OUT。

---

## 十、Relational Inference

```markdown
# Relational Inference

## Primary relations
...

## State features
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

不使用“有四害所以自动打折”“有大凶格所以直接判败”等固定裁决。

九星等来源固定吉凶标签只能作为候选 prior；必须经过季节、事项、状态、角色与其他关系后解释。

---

## 十一、Competing Branches

```markdown
# Competing Interpretation Branches

## H1 — 主分支
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

存在真实多解时，保留多解比强行造确定性更合格。

---

## 十二、Timing Freeze

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

内外盘分组使用：

- 阳遁内 `1、8、3、4`；外 `9、2、7、6`；
- 阴遁内 `9、2、7、6`；外 `1、8、3、4`。

“内快外慢”仍是传统候选语义，不是固定天数系数。

---

## 十三、Frozen Prediction

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

若信息不足，可输出 `INSUFFICIENT_EVIDENCE`；若方法不适用，可输出 `OUT_OF_SCOPE`。禁止为了格式完整硬造答案。

正式前瞻案例的冻结字段应同步到 `K2_PROSPECTIVE_CASE_REGISTRY.jsonl`。

---

## 十四、Auxiliary Context Ablation

只在需要时创建：

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

任何辅助信息进入后，都不得回写成原 method-only 预测的“本来就看到了”。

---

## 十五、Outcome Audit

```markdown
# Outcome Audit

## Actual outcome
...

## Frozen score
- outcome_class: HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED
- exact_hit:
- within_window:
- unscorable:

## Competing branch score
...

## Error class
INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR /
METHOD_LAYER_ERROR / SETUP_CALIBRATION_ERROR / DEITY_SYSTEM_ERROR /
FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR /
BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE

## Post-feedback changes observed
- role_switch:
- factor_switch:
- method_switch:
- method_layer_switch:
- setup_calibration_switch:
- deity_system_switch:
- time_family_switch:
- timing_rule_switch:
- external_information_added:

## Contamination flags
...

## Rule lifecycle decision
KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT
```

成功与失败都要保留。污染案例不能删除；只能标记为不能支持 clean model。

---

## 十六、Prospective Registry Gate

未知结果的正式测试必须遵守：

`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`

Git 中只保存机器可审计的冻结元数据和哈希，不保存不必要的私人信息。

结果后任何冻结字段变化都必须产生新 `case_id`，不得覆盖原记录。

---

## 十七、final_case_summary.md

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

---

## 十八、文献引用与方法权威

- 原书断语：标 SOURCE；
- 项目转译：标 INFERENCE；
- 前瞻结果：进入 EMPIRICAL_SUPPORT；
- 新闻/背景/外应：标 CONTAMINATION/AUXILIARY。

多个古籍同意一条规则，只说明传统来源之间有共识，不自动证明现实有效。

---

*Workflow v2.1 | 2026-08-21 | 纳入 QM-SRC-0001 Method-Layer / Deity-System / Prospective Registry Gate*
