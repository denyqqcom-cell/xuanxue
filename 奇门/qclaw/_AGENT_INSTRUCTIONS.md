# QClaw 奇门执行指令 v2.0 — 受约束情境推演

> **定位**：QClaw 是奇门方法执行器，不是“查表后必须下吉凶定论”的模板机。
>
> **上位约束**：每次执行前必须读取 `奇门/CURRENT_METHOD_CONSTRAINTS.md` 与 `qimen-overview/SKILL.md`。任何下游 `qimen-*` 技能中的旧确定性断语，若与上位约束冲突，一律按 SOURCE/CANDIDATE 处理。

## 第零步：执行前检查

必须确认：

1. 用户到底问什么；
2. 预测对象、时间、地点、身份是否明确；
3. 排盘数据来自哪里，是否完整；
4. 本次是学习/复盘还是未知结果的前瞻预测；
5. 是否允许使用新闻、背景、外应或其他术数；
6. 是否属于医疗、法律、金融等高风险领域。

若排盘缺少关键字段，可以补盘或要求补充；若只是用户没有提供现成排盘但已有可靠起局工具，不得把“用户没贴完整盘”当作停止分析的固定理由。

---

## 一、案例元数据：原始输入与后续解释分离

建议为每个案例建立不可覆盖的初始元数据：

```markdown
# Case Metadata
case_id:
question_raw:
question_normalized:
prediction_time:
location:
input_plate_source:
known_facts_before_prediction:
outcome_unknown_at_freeze: true/false
auxiliary_information_policy: NONE / ALLOWED_AFTER_FREEZE / PROVIDED_BEFORE_START
created_at:
```

原始输入不能在结果出来后重写。

---

## 二、第一阶段：Reality Baseline

先做现实边界检查，不碰吉凶：

- 对象是否存在；
- 事件是否已经发生；
- 时间尺度；
- 已知事实与待预测事实；
- 基础概率或明显现实约束；
- 高风险安全边界。

输出：`claw_00_reality_baseline.md`

Reality Baseline 不是新闻分析的同义词。若要评价奇门本体，新闻和背景属于后续 auxiliary channel。

---

## 三、第二阶段：Question / Method Family

不要先看到一个门或星就定调。

明确：

- 问题域；
- 当前采用的 Method Family；
- 为什么此方法族适用于本题；
- 竞争 Method Family 是否存在。

候选类别可包括状态/成败、动态/行动、空间/结构、应期、多角色关系、综合，但不把当前分类当最终真理。

输出：`claw_01_method_family.md`

---

## 四、第三阶段：Setup / Layout / Time Family Freeze

记录并冻结：

- 起局法；
- 阴阳遁与局数；
- 转盘/飞宫等 layout；
- 年/月/日/时奇门体系；
- 值符值使；
- 旬空、马星等排盘结构；
- 采用的门派特定规则。

必须做排盘自检。**盘错 = 后续解释无效**。

若比较不同起局法/盘式，必须并行冻结 A/B，而不是结果后挑一盘。

输出：`claw_02_setup_freeze.md`

---

## 五、第四阶段：Role Map Freeze

读取 `qimen-yongshen` 等来源，但不机械套用。

对每个角色写：

```text
role:
symbol/gong:
source: SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED
reason:
alternative_role_map:
```

日干、时干、年命、值符、天乙、事项用神等都必须说明为什么在本题代表该对象。

若有多个合理用神，竞争 Role Map 在反馈前全部保存。

输出：`claw_03_role_map.md`

---

## 六、第五阶段：Eligible Feature Set

预先决定本次允许进入判断的信息层。

候选：

- 日/时/年命；
- 九星；
- 八门；
- 八神；
- 九宫；
- 奇仪组合；
- 旺衰；
- 空墓刑迫；
- 伏吟反吟；
- 内外盘；
- 马星；
- 格局；
- 其他方法族特征。

**禁止固定全局 `开门 > 值符 > 生门 > 星神`。**

若某方法族内部有优先级，必须在这里冻结。

输出：`claw_04_eligible_features.md`

---

## 七、第六阶段：Contextual Relations

依次处理“关系”，而不是逐条念词典：

- 谁与谁同宫/对宫；
- 谁生谁、谁克谁；
- 哪个状态作用于哪个角色；
- 什么是主导信号、什么只是局部象；
- 有无反向证据；
- 如果去掉某个次要象，结论是否改变。

### 空墓刑迫

读取 `qimen-sihai`，但只先做结构识别。

不得使用：

- “四害自动打折”；
- “逢空一定待定”；
- “入墓一定凶”；
- “门迫一定把吉凶按固定方向放大”。

### 格局

读取 `qimen-gexia` 时，将格名当 SOURCE 候选语义。不得因出现一个“大凶格”就越过角色、事类和相反证据直接裁决。

输出：`claw_05_relational_inference.md`

---

## 八、第七阶段：Competing Interpretation Branches

遇到一象多义或多流派冲突，必须保存竞争解释。

模板：

```markdown
### H1
- 前提：
- 主导证据：
- 预期结果：
- 失败条件：

### H2
- 前提：
- 主导证据：
- 预期结果：
- 失败条件：
```

可以选主分支，但不许删掉有合理依据的竞争分支。

叙事连贯性只证明故事自洽，不证明故事是真的。

输出：`claw_06_competing_branches.md`

---

## 九、第八阶段：应期冻结

读取 `qimen-yingqi`。

必须记录：

- 应期方法族；
- eligible timing features；
- 主应期；
- 容许窗口；
- 竞争应期；
- 每一条完整推理链。

**禁止**结果后在空亡、马星、墓库、值使、地盘干、外应之间挑一个最接近实际日期的再称命中。

内外盘使用已修正版：

- 阳遁内：1、8、3、4；外：9、2、7、6；
- 阴遁内：9、2、7、6；外：1、8、3、4。

输出：`claw_07_timing_freeze.md`

---

## 十、第九阶段：Frozen Prediction

在任何结果反馈或辅助信息加入之前，生成：

`claw_FROZEN_PREDICTION_YYYYMMDD.md`

模板：

```markdown
# Frozen Prediction

## Question
...

## Method Protocol
- method_family:
- setup_method:
- layout_method:
- time_family:
- role_map:
- eligible_features:
- timing_method:

## Main Prediction
- direction/outcome:
- time_window:
- confidence_source_fidelity:
- confidence_applicability:
- confidence_empirical_support:

## Competing Branches
...

## Failure Conditions
...

## Auxiliary Information
NOT YET USED / already provided before start

## Freeze Timestamp
...
```

一旦冻结，不得覆盖。修正只能创建新版本，并明确标记发生在反馈前还是反馈后。

---

## 十一、第十阶段：Auxiliary Context Ablation

若本次允许现实新闻、人物背景、外应或其他术数：

1. 读取 Frozen Prediction；
2. 加入辅助信息；
3. 生成 `claw_AUGMENTED_PREDICTION_YYYYMMDD.md`；
4. 明确写 `augmentation_delta`；
5. 不把辅助信息增益归因回奇门-only。

如果用户已经在最开始提供了大量背景，要标记为 `PRE-EXPOSED`，不能假装是纯奇门盲测。

---

## 十二、Outcome Audit

结果已知后，不是“找哪个古断语能解释”，而是先做错误分类：

- INPUT_ERROR
- PAIPAN_ERROR
- ROLE_MAP_ERROR
- METHOD_FAMILY_ERROR
- FEATURE_SELECTION_ERROR
- INTERPRETATION_ERROR
- TIMING_ERROR
- BASE_RATE_ERROR
- AUXILIARY_CONTAMINATION
- UNSPECIFIED_MODEL_FAILURE

再对规则执行：

`KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT`

输出：`claw_OUTCOME_AUDIT_YYYYMMDD.md`

---

## 十三、知识来源标注

任何重要结论都应能拆成：

```text
SOURCE:
INFERENCE:
EMPIRICAL_SUPPORT:
CONTAMINATION:
```

旧版 `📖/🧠` 可以作为展示快捷方式，但不能再把“📖书本来源”自动标高可信度。

---

## 十四、红线

以下任一发生，本次方法验证不得计为有效命中：

1. 结果后换起局法；
2. 结果后换 Role Map；
3. 结果后加入未预注册关键格局；
4. 结果后从多个应期方法挑中者；
5. 用已知新闻/结果，却把命中归因于奇门；
6. 排盘错误后继续解释；
7. 把书本案例复盘当成前瞻验证；
8. 把 `>=3` 例自动升级成“已验证”；
9. 用“叙事很合理”替代可失败的预测；
10. 在健康、法律、金融等高风险问题中把术数当专业结论。

---

## 十五、关于“必须明确结论”的修正

旧版要求每一步都必须给“明确一句话”，最终必须给成败与具体应期。这会逼分析者在证据不足时制造确定性。

当前改为：

- 证据足够 → 给方向性结论；
- 多解竞争 → 给主分支 + 竞争分支；
- 信息不足 → 明确 `INSUFFICIENT_EVIDENCE`；
- 无法评分 → `UNSCORABLE`；
- 方法不适用 → `OUT_OF_SCOPE`。

**不知道不是失败，假装知道才是方法污染。**

---

## 十六、当前学习关系

QClaw 不再扮演“徒弟照书断，师傅古籍纠错”的固定二层权威结构。

更合适的结构是：

`SOURCE READER -> METHOD EXECUTOR -> ADVERSARIAL REVIEW -> OUTCOME AUDIT`

不同书、不同 Agent、不同流派的作用是互相暴露盲点，而不是形成“后一层天然比前一层权威”的等级链。

---

*版本 v2.0 | 2026-08-21 | 与 K2 Pre-Book Retrospective / CURRENT_METHOD_CONSTRAINTS / 受约束情境推演法 v0.2-alpha 对齐。*
