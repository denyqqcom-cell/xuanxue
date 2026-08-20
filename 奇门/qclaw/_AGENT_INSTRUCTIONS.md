# QClaw 奇门执行指令 v2.1 — 受约束情境推演

> **定位**：QClaw 是奇门方法执行器，不是“查表后必须下吉凶定论”的模板机。
>
> **上位约束**：每次执行前必须读取 `奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md` 与 `qimen-overview/SKILL.md`。任何下游 `qimen-*` 技能中的旧确定性断语，若与上位约束冲突，一律按 SOURCE/CANDIDATE 处理。

## 第零步：执行前检查

必须确认：

1. 用户到底问什么；
2. 预测对象、时间、地点、身份是否明确；
3. 排盘数据来自哪里，是否完整；
4. 本次是学习/复盘还是未知结果的前瞻预测；
5. 是否允许使用新闻、背景、外应或其他术数；
6. 是否属于医疗、法律、金融等高风险领域；
7. 本次究竟使用哪一个 `method_layer`，是否存在平行 A/B 模型。

若排盘缺少关键字段，可以补盘或要求补充；若只是用户没有提供现成排盘但已有可靠起局工具，不得把“用户没贴完整盘”当作停止分析的固定理由。

---

## 一、案例元数据：原始输入与后续解释分离

建议为每个案例建立不可覆盖的初始元数据：

```markdown
# Case Metadata
case_id:
question_raw:
question_normalized:
question_fingerprint_sha256:
prediction_time:
location:
input_plate_source:
known_facts_before_prediction:
outcome_unknown_at_freeze: true/false
auxiliary_information_policy: NONE / ALLOWED_AFTER_FREEZE / PRE_EXPOSED
created_at:
```

原始输入不能在结果出来后重写。正式前瞻案例若要进入经验支持，必须能同步为 Prospective Case Registry 的机器可审计记录。

---

## 二、第一阶段：Reality Baseline

先做现实边界检查，不碰吉凶：

- 对象是否存在；
- 事件是否已经发生；
- 时间尺度；
- 已知事实与待预测事实；
- 基础概率或明显现实约束；
- 高风险安全边界。

Reality Baseline 不是新闻分析的同义词。若要评价奇门本体，新闻和背景属于后续 auxiliary channel。

---

## 三、第二阶段：Question / Method-Layer Freeze

不要先看到一个门或星就定调。

先明确：

- `question_domain`；
- `method_family`；
- `method_layer`；
- 为什么此方法族适用于本题；
- 是否存在竞争模型。

`method_layer` 只允许：

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

硬规则：

- `RITUAL_AUXILIARY` 默认不参与预测评分；
- 一个方法层的 miss 不得由另一方法层在反馈后救援；
- A/B 比较必须在反馈前创建独立冻结模型与 `case_id`。

---

## 四、第三阶段：Setup / Layout / Time / Deity Freeze

记录并冻结：

```text
setup_method
setup_calibration = PINGQI / DINGQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU / CHAOSHEN / ZHIRUN / JIEQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
yin_yang_dun
ju_number
layout_method
time_family = YEAR / MONTH / DAY / HOUR / NOT_APPLICABLE
deity_system = GOUCHEN_ZHUQUE / BAIHU_XUANWU / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
hour_omen_family
ritual_layer
bureau_table_source
school_context
plate_self_check
```

必须做排盘自检。**盘错 = 后续解释不能计为原模型有效命中。**

若比较不同起局法、节气校准、盘式、时间族或八神体系，必须并行冻结 A/B，而不是结果后挑一套。

### 八神体系红线

- 梁书勾陈/朱雀体系与白虎/玄武体系不得静默混合；
- 不得把一套体系的象意借给另一套后再说“古法相通”；
- 未经来源/版本/布局拆解，只能标 `CONTEXT_REQUIRED`。

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

若有多个合理用神，竞争 Role Map 在反馈前全部保存。反馈后换用神只能记为模型修改，不能覆盖原版本。

---

## 六、第五阶段：Structural Lookup

把可机械核验的结构与解释层分开：

- 阴阳遁、局数；
- 值符、值使；
- 星门神宫位置；
- 旬空、马星等；
- source-defined bureau table lookup。

若使用梁书十八局，优先引用 `K2_SOURCE_FIXTURES` 的已验证 sparse anchors 做实现回归。

必须牢记：

`Source Fidelity != Lookup Determinism != Predictive Validity`

排盘程序稳定、查表一致，只证明执行可重复，不证明预测现实有效。

---

## 七、第六阶段：Eligible Feature Set

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
- 当前已冻结方法族允许的其他特征。

**禁止固定全局 `开门 > 值符 > 生门 > 星神`。**

未进入 IN 的信息，结果后不得补入救援。仪式、符咒、博奕、禁敌默认 OUT。

---

## 八、第七阶段：Contextual Relations

依次处理“关系”，而不是逐条念词典：

- 谁与谁同宫/对宫；
- 谁生谁、谁克谁；
- 哪个状态作用于哪个角色；
- 什么是主导信号、什么只是局部象；
- 有无反向证据；
- 如果去掉某个次要象，结论是否改变。

不得使用：

- “四害自动打折”；
- “逢空一定待定”；
- “入墓一定凶”；
- “门迫一定按固定方向放大”；
- “九星固定吉凶标签可直接裁决所有事项”。

九星、门、神等固定标签最多作为 SOURCE prior；应结合季节、事项、状态、角色和竞争信号。

---

## 九、第八阶段：Competing Interpretation Branches

遇到一象多义或多流派冲突，必须保存竞争解释。

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

---

## 十、第九阶段：应期冻结

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

---

## 十一、第十阶段：Frozen Prediction

在任何结果反馈或辅助信息加入之前，生成不可覆盖版本。

至少冻结：

```text
case_id
question_fingerprint_sha256
question_domain
method_family
method_layer
setup_calibration
seasonal_alignment
layout_method
time_family
deity_system
hour_omen_family
ritual_layer
bureau_table_source
role_map_sha256
eligible_features_sha256
competing_branches_sha256
timing_protocol_sha256
auxiliary_information_policy
observable_success_criteria
observable_failure_criteria
freeze_timestamp
outcome_unknown_at_freeze
```

一旦冻结，不得覆盖。修正只能创建新版本或新 `case_id`，并明确发生在反馈前还是反馈后。

正式未知结果测试按 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md` 登记。

---

## 十二、第十一阶段：Auxiliary Context Ablation

若本次允许现实新闻、人物背景、外应或其他术数：

1. 先读取 Frozen Prediction；
2. 再加入辅助信息；
3. 明确写 `augmentation_delta`；
4. 不把辅助信息增益归因回奇门-only。

如果用户已经在最开始提供了大量背景，要标记为 `PRE_EXPOSED`，不能假装是纯奇门盲测。

---

## 十三、Outcome Audit

结果已知后，不是“找哪个古断语能解释”，而是先做错误分类：

- INPUT_ERROR
- PAIPAN_ERROR
- ROLE_MAP_ERROR
- METHOD_FAMILY_ERROR
- METHOD_LAYER_ERROR
- SETUP_CALIBRATION_ERROR
- DEITY_SYSTEM_ERROR
- FEATURE_SELECTION_ERROR
- INTERPRETATION_ERROR
- TIMING_ERROR
- BASE_RATE_ERROR
- AUXILIARY_CONTAMINATION
- UNSPECIFIED_MODEL_FAILURE

再检查反馈后是否发生：

- role switch；
- factor switch；
- method/method-layer switch；
- setup calibration switch；
- deity-system switch；
- time-family switch；
- timing-rule switch；
- external information added。

Outcome 统一：

`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`

污染案例不得删除，只能标记不能支持 clean model。

---

## 十四、知识来源标注

任何重要结论都应能拆成：

```text
SOURCE:
INFERENCE:
EMPIRICAL_SUPPORT:
CONTAMINATION:
```

旧版 `📖/🧠` 可以作为展示快捷方式，但不能再把“📖书本来源”自动标高可信度。

---

## 十五、红线

以下任一发生，本次方法验证不得计为有效 clean hit：

1. 结果后换起局法；
2. 结果后换节气校准；
3. 结果后换 method layer；
4. 结果后换 time family；
5. 结果后换 deity system；
6. 结果后换 Role Map；
7. 结果后加入未预注册关键格局/feature；
8. 结果后从多个应期方法挑中者；
9. 用已知新闻/结果，却把命中归因于奇门；
10. 排盘错误后继续解释并追认命中；
11. 把书本案例复盘当成前瞻验证；
12. 把 `>=3` 例自动升级成“已验证”；
13. 用“叙事很合理”替代可失败的预测；
14. 用 HOUR_OMEN、年/月/日家或仪式层去事后救标准盘；
15. 在健康、法律、金融等高风险问题中把术数当专业结论。

---

## 十六、关于“必须明确结论”的修正

- 证据足够 → 给方向性结论；
- 多解竞争 → 给主分支 + 竞争分支；
- 信息不足 → `INSUFFICIENT_EVIDENCE`；
- 无法评分 → `UNSCORABLE`；
- 方法不适用 → `OUT_OF_SCOPE`。

**不知道不是失败，事后换轨并假装本来就知道才是方法污染。**

---

## 十七、当前学习关系

QClaw 的合理结构是：

`SOURCE READER -> METHOD EXECUTOR -> ADVERSARIAL REVIEW -> PROSPECTIVE REGISTRY -> OUTCOME AUDIT`

不同书、不同 Agent、不同流派的作用是互相暴露盲点，而不是形成“后一层天然比前一层权威”的等级链。

---

*版本 v2.1 | 2026-08-21 | 与 QM-SRC-0001 Method Delta / Prospective Case Gate / Source Fixture Gate 对齐。*
