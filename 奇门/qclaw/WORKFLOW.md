# 奇门受约束情境推演工作流 v2.0

> 本模板用于保存一次解盘从原始输入到冻结预测、辅助信息增量与结果审计的全过程。
>
> 上位约束：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`qimen-overview/SKILL.md`、`_AGENT_INSTRUCTIONS.md`。

## 一、核心变化

旧工作流按固定八步输出，并要求每一步都必须明确吉凶、最终必须给成败与应期。这会在证据不足时制造确定性，也容易让不同书的规则在同一盘中无限叠加。

v2.0 改为：

`Reality Baseline -> Method Freeze -> Role Map -> Eligible Features -> Relational Inference -> Competing Branches -> Timing Freeze -> Frozen Prediction -> Auxiliary Ablation -> Outcome Audit`

单次预测中可以灵活推演，但反馈前必须冻结自由度。

---

## 二、推荐案例目录

```text
YYYYMMDD_问题关键词_时分/
├── _META.md
├── claw_00_reality_baseline.md
├── claw_01_method_family.md
├── claw_02_setup_freeze.md
├── claw_03_role_map.md
├── claw_04_eligible_features.md
├── claw_05_relational_inference.md
├── claw_06_competing_branches.md
├── claw_07_timing_freeze.md
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
- prediction_time:
- location:
- plate_source:
- known_facts_before_prediction:
- outcome_unknown_at_freeze: true/false
- auxiliary_information_policy: NONE / ALLOWED_AFTER_FREEZE / PRE_EXPOSED
- created_at:
```

原始输入与初始已知事实不得在结果后覆盖。

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

## 五、Method Freeze

```markdown
# Method Family
- question_domain:
- method_family:
- alternative_method_family:
- reason:

# Setup Freeze
- setup_method:
- yin_yang_dun:
- ju_number:
- layout_method:
- time_family:
- school_context:
- plate_self_check:
- frozen_at:
```

若比较多个方法，A/B 都必须在反馈前建立。

---

## 六、Role Map

```markdown
# Role Map

| Role | Symbol / Palace | Basis | Alternative |
|---|---|---|---|
| 求测者 | ... | SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED | ... |
| 事件 | ... | ... | ... |
| 对方 | ... | ... | ... |
```

反馈后换用神必须在 Outcome Audit 标记为 `POST_FEEDBACK_ROLE_SWITCH`，不能覆盖原 Role Map。

---

## 七、Eligible Feature Set

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
```

未进入 IN 的信息，结果后不得补入救援。

---

## 八、Relational Inference

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

---

## 九、Competing Branches

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
```

存在真实多解时，保留多解比强行造确定性更合格。

---

## 十、Timing Freeze

```markdown
# Timing Freeze

- prediction_horizon:
- resolution_target:
- timing_method_family:
- eligible_timing_features:
- main_window:
- scoring_tolerance:

## Reasoning chain
1. ...
2. ...
3. ...

## Alternative timing window
...
```

内外盘分组使用：

- 阳遁内 `1、8、3、4`；外 `9、2、7、6`；
- 阴遁内 `9、2、7、6`；外 `1、8、3、4`。

“内快外慢”仍是传统候选语义，不是固定天数系数。

---

## 十一、Frozen Prediction

```markdown
# Frozen Prediction

## Protocol
- question_domain:
- method_family:
- setup_method:
- layout_method:
- time_family:
- role_map_version:
- eligible_features_version:
- timing_method:

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

## Auxiliary information
NOT USED / PRE_EXPOSED

## Freeze
- timestamp:
- immutable_after_outcome_feedback: true
```

若信息不足，可输出 `INSUFFICIENT_EVIDENCE`；若方法不适用，可输出 `OUT_OF_SCOPE`。禁止为了格式完整硬造答案。

---

## 十二、Auxiliary Context Ablation

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

## New practical conclusion
...

## Attribution
method-only contribution:
auxiliary contribution:
```

---

## 十三、Outcome Audit

```markdown
# Outcome Audit

## Actual outcome
...

## Frozen score
- exact_hit:
- within_window:
- miss:
- unscorable:

## Competing branch score
...

## Error class
INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR /
FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR /
BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE

## Post-feedback changes observed
- role_switch:
- factor_switch:
- method_switch:
- timing_rule_switch:
- external_information_added:

## Rule lifecycle decision
KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT

## Why
...
```

成功与失败都要记录。成功案例必须讨论基础概率与污染，失败案例不得自动用“体系天花板”解释。

---

## 十四、final_case_summary.md

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

## 评分
...

## 最大误差来源
...

## 对当前理论的影响
...
```

这是用于跨案例学习的核心摘要，不再使用“徒弟→师傅天然权威”的固定交接结构。

---

## 十五、文献引用与方法权威

- 原书断语：标 SOURCE；
- 项目转译：标 INFERENCE；
- 前瞻结果：进入 EMPIRICAL_SUPPORT；
- 新闻/背景/外应：标 CONTAMINATION/AUXILIARY。

多个古籍同意一条规则，只说明传统来源之间有共识，不自动证明现实有效。

---

*Workflow v2.0 | 2026-08-21 | 受约束情境推演版*
