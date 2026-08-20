---
name: qimen-overview
description: >
  奇门遁甲受约束情境推演入口。用于定义问题、方法层/方法族、起局校准、盘式/时间体系、
  八神体系、Role Map、结构查表、候选信息层、竞争解释、冻结预测与结果审计。
  调用时必须服从 CURRENT_METHOD_CONSTRAINTS.md 与 K2_PROSPECTIVE_CASE_PROTOCOL.md，
  不把旧书断语、查表一致或历史经验当作跨场景真理。
---

# 奇门解盘总览：受约束情境推演入口 v2.1

> **当前约束**：先读 `奇门/CURRENT_METHOD_CONSTRAINTS.md`。若属于未知结果的正式前瞻验证，同时读 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`。本技能中的传统规则属于 SOURCE / CANDIDATE，除非另有经验支持，不等于项目事实。

## 一、旧七步流程的当前定位

历史版本使用：

```text
明确问题 → 看大局 → 取用神 → 查四害 → 析宫盘 → 看生克 → 定应期
```

它仍可作为历史检查清单，但不再是所有问题必须采用同一固定顺序的通用定律。

当前运行流程：

```text
0. Reality Baseline
1. Question Domain
2. Method-Layer / Method-Family Freeze
3. Setup Calibration + Seasonal Alignment + Layout + Time Family + Deity-System Freeze
4. Role Map Freeze
5. Bureau / Structural Lookup
6. Eligible Feature Set
7. Contextual Relations
8. Competing Interpretation Branches
9. Timing Freeze
10. Frozen Prediction
11. Optional Auxiliary Context Ablation
12. Outcome Audit
13. Rule Lifecycle Update
```

核心不是“盘上每个符号都解释”，而是先限制本次允许使用哪些方法、结构和信息，避免反馈后补规则。

---

## 二、Stage 0：Reality Baseline

开始解盘前先确认：

- 所问对象、事件、时间、地点真实且定义正确；
- 哪些信息已经知道，哪些才是待预测目标；
- 时间范围是时、日、月、年还是长期；
- 是否存在很高的基础概率；
- 是否属于医疗、法律、金融等高风险领域；
- 用户是否已经提供大量背景，造成 `PRE_EXPOSED`。

现实背景可以进入实际决策，但若要评价奇门本体效果，应与 method-only 结果分开记录。

---

## 三、Stage 1-2：Question Domain + Method-Layer / Method-Family Freeze

先确定“这是什么问题”，再确定“本次究竟在用哪一种奇门方法层”。

### 3.1 Question Domain

候选问题域可包括：

- 状态/成败；
- 动态/行动；
- 空间/结构；
- 时间/应期；
- 多角色关系；
- 综合。

这不是最终 taxonomy。不同作者/流派若分类不同，应并列保存、比较适用域，不能强行合并。

### 3.2 Method Layer

当前强制区分：

- `STANDARD_PLATE`：标准三元/时家盘与盘面解释；
- `TIME_FAMILY_VARIANT`：年/月/日/时家作为独立算法；
- `HOUR_OMEN`：如九星十二时辰应克，独立计分；
- `RITUAL_AUXILIARY`：符咒、反闭、步斗、六戊、禁敌等，默认不参加预测评分。

**禁止**：STANDARD_PLATE 没断中后，临时切到 HOUR_OMEN、年/月/日家或仪式层救援。

若要比较 A/B，必须在结果未知时并行冻结独立模型。

---

## 四、Stage 3：起局校准、盘式、时间体系与八神体系冻结

反馈前至少记录：

```text
setup_method
setup_calibration = PINGQI | DINGQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU | CHAOSHEN | ZHIRUN | JIEQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
yin_yang_dun
ju_number
layout_method
time_family = YEAR | MONTH | DAY | HOUR | NOT_APPLICABLE
deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
hour_omen_family
ritual_layer
bureau_table_source
school_context
```

若并行比较不同起局法、平气/定气、正授/超神/置闰/接气、盘式、时间族或八神体系，应同时冻结多个版本，不能结果出来后选“最像”的一盘。

### 4.1 八神体系冲突

梁湘潤《奇門遁甲入門》使用勾陈/朱雀体系，而现代资料中常见白虎/玄武体系。当前处理：

- 不静默改名；
- 不在一个模型里互借象意；
- 未经来源/版本/布局拆解，不假设完全同义；
- 若要比较，使用反馈前冻结的平行模型。

---

## 五、Stage 4：Role Map Freeze

根据问题明确：

- 求测者；
- 所问事件；
- 对手、合作方或第三方；
- 财、职位、疾病、文书、出行等事项角色；
- 主客关系。

角色来源标记：

- `SOURCE_DEFINED`：原书/门派明确规定；
- `METHOD_DEFINED`：当前方法族固定；
- `CONTEXT_INFERRED`：本次情境推断。

若同一对象存在多个合理用神，保留竞争 Role Map，反馈前冻结，不得结果后换用神。

---

## 六、Stage 5：Bureau / Structural Lookup

把“排盘/查表是否执行正确”与“解释是否有效”分开。

候选结构包括：

- 阴/阳遁与局数；
- 值符、值使；
- 星门神宫位置；
- 旬空、马星；
- source-defined bureau table lookup。

当前已建立梁书十八局 source fixture index。使用 fixture 时必须牢记：

```text
Source Fidelity != Lookup Determinism != Predictive Validity
```

- **Source Fidelity**：是否忠实复刻来源；
- **Lookup Determinism**：同输入是否稳定得到同结构；
- **Predictive / Empirical Support**：是否在未知结果前瞻测试中有区分力。

查表一致不能被表述为预测已验证。

---

## 七、Stage 6：Eligible Feature Set

按本次方法族预先选择可用信息层。候选包括：

- 日干、时干、年命；
- 事项用神；
- 九星；
- 八门；
- 八神；
- 九宫；
- 天盘/地盘奇仪；
- 旺衰；
- 空亡、入墓、击刑、门迫；
- 伏吟、反吟；
- 内外盘；
- 马星；
- 十干克应及其他格局。

**没有全局固定优先级。**

旧的 `开门 > 值符 > 生门 > 星神` 已废弃为跨场景硬规则。若某个方法族规定特定优先级，应在预测前写明来源与适用域。

未进入 Eligible Feature Set 的信息，反馈后不能补入救援。

---

## 八、传统“大局”信息：保留来源，不自动定吉凶

### 8.1 伏吟 / 反吟

传统资料常将伏吟解释为偏静/迟缓，将反吟解释为偏动/变化。当前只先作为 SOURCE 候选语义。

实际使用继续问：

- 所问本来就是“静”还是“动”？
- 慢对这个问题是坏事还是保护机制？
- 反复是失败、调整还是必要过程？
- 星伏、门伏、星门俱伏是否在当前方法族有不同权重？

不得把“伏吟=凶”“反吟=凶/利客”直接当作跨场景事实。

### 8.2 日干 / 时干

部分现代体系以日干表示求测者、时干表示事件，并用宫间生克描述关系。保留为常见 Role Map 候选；若目标方法族另有定义，应按该体系冻结，不得混搭。

### 8.3 天显时格

相关古今资料存在门派表述，应以具体 source、起局体系和例证保存。不得因为出现该格就自动反转伏吟结论。

---

## 九、空、墓、刑、迫：从“打折器”改为状态特征

旧版把空亡、入墓、击刑、门迫统称“四害”，并常写成“吉门打折、凶门加重”。这种固定系数式解释现已撤销。

当前处理：

1. 先准确识别状态；
2. 记录状态作用于哪个角色/用神；
3. 检查当前方法族怎样使用该状态；
4. 与其他关系共同推演；
5. 若作用方向存在多解，建立竞争分支。

### 空亡

不再固定解释为“凶”或“方向待定”。可能对应未落实、暂缺、落空、脱离、延迟等，需按事类检验。

### 入墓

先确认具体天干与墓支/宫，再判断该方法族是否把它作为受限、收藏、延迟、结束等语义。不得自动判凶。

### 击刑

先确认结构是否真的成立，再看对当前角色的作用。传统“大凶”标签只是 SOURCE 层描述。

### 门迫 / 门宫关系

门克宫、宫克门、门生宫、宫生门、比和可以作为关系 feature；现实意义仍取决于事项和角色，不使用固定“迫=凶、义=吉”的无条件输出。

---

## 十、Stage 7：宫内、宫间与条件化关系

传统常用的信息包括：

- 九星：天时/性质候选；
- 八门：人事/事项候选；
- 八神：辅助象候选；
- 九宫：空间、属性与关系载体；
- 奇仪/克应：组合语义候选。

旧版固定“九星→八门→八神→八卦→十干克应”的顺序，不再作为全局要求。

梁书九星章节同时存在固定吉凶类别、旺相休囚、季节和具体事项宜忌。这本身就说明：即使忠实遵循传统文本，也不能把一个星压成跨场景恒定 verdict。

当前至少检查：

- 哪个是主角色，哪个是辅助角色；
- 同宫、对宫、生克、比和怎样作用；
- 有无明显反向信号；
- 去掉某个局部象，主结论是否改变；
- 当前推理是否只是把多个古断语串成故事。

---

## 十一、主客、急缓等传统规则的处理

### 五阳 / 五阴、天地盘主客

相关传统规则可作为某些动态/行动型方法的 SOURCE 候选，不再跨所有预测自动执行。

### 急从神 / 缓从门

善天道体系把急缓作为信息选择机制之一。这一规则可作为该方法族的候选 protocol，但必须：

- 先定义何为“急/缓”；
- 在预测前选择；
- 不在反馈后因为结果不符而切换。

---

## 十二、Stage 8：竞争解释分支

遇到一象多义、信号冲突或流派分歧时，禁止立刻挑最顺眼的解释。

每个重要分支写：

- 前提；
- 主导证据；
- 区分观察；
- 失败条件；
- 与竞争分支的冲突点。

例如空亡可形成“延迟 / 落空 / 暂离 / 非关键变量”等竞争解释。反馈后只允许评分，不允许新增分支后计为命中。

叙事连贯性是解释质量，不是经验支持。

---

## 十三、Stage 9：应期冻结

应期详见 `qimen-yingqi`，但当前有硬约束：

1. 不凭感觉跳步；
2. 某流派的“严格优先级”只在该方法族内有效；
3. 先冻结应期方法，再看结果；
4. 禁止结果后从空、墓、马、值使、地盘干、外应中任选一个最接近实际日期的再称命中。

内外盘分组使用：

- 阳遁内：1、8、3、4；外：9、2、7、6；
- 阴遁内：9、2、7、6；外：1、8、3、4。

传统“内快外慢”仍需前瞻验证，不是固定天数系数。

---

## 十四、Stage 10：Frozen Prediction

反馈前至少保存：

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
主结论 / 竞争结论
可观察成功条件
可观察失败条件
freeze_timestamp
outcome_unknown_at_freeze
```

正式前瞻案例同步到 `knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`。

信息不足允许 `INSUFFICIENT_EVIDENCE`；方法不适用允许 `OUT_OF_SCOPE`；无法评分允许 `UNSCORABLE`。

---

## 十五、Stage 11：现实信息 / 外应 / 其他术数消融

新闻、求测者背景、外貌、外应、其他术数若加入，必须标为 auxiliary channel。

推荐：

`method-only -> freeze -> context-augmented -> record delta`

外部信息带来的改进不能倒算成奇门本体能力。

---

## 十六、仪式材料与 HOUR_OMEN 的隔离

梁书后段包含玉女反闭、咒法、禹罡、六戊、步斗、禁敌、博奕等材料。它们可以保留为 SOURCE / ritual-history 研究，但默认不进入普通预测评分。

九星十二时辰应克属于 `HOUR_OMEN`，若研究其预测能力必须独立预注册事件类别、时间窗、基准率与负对照，不得作为标准盘的临时额外证据。

---

## 十七、传统八神八门与格局表的当前用法

历史 `qclaw` 中保存了大量“值符+门”“白虎+门”“十干克应”等断语。

统一按以下方式调用：

```text
SOURCE: 原书/技能记录的传统断语
INFERENCE: 本情境如何转译
EMPIRICAL_SUPPORT: 是否有独立前瞻支持
CONTAMINATION: 是否借用了结果/背景/其他方法
```

不得仅凭“白虎+杜门”“死门+某星”等传统字样输出死亡、重大疾病、犯罪等高风险结论。

---

## 十八、健康类材料的边界

九宫人体、天干脏腑、天芮/天心等疾病象意属于传统术数材料，可用于文献研究和理解作者方法，但不能替代医疗诊断、预后或治疗建议。

如涉及真实健康问题：

- 可说明传统来源怎样映射；
- 必须把术数解释标成低经验支持/非医学证据；
- 不得以吉凶格局判断生死、癌症、手术必要性等医学事实。

---

## 十九、Stage 12-13：Outcome Audit + Rule Lifecycle

结果出现后，先分类错误来源：

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

Outcome 统一：

`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`

再决定规则：

`KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT`

成功案例必须讨论基础概率与污染；失败案例不得自动用“体系天花板”解释；污染案例不得删除。

---

## 二十、快速导航

| 任务 | 技能 |
|---|---|
| 起局 | `qimen-qiju` |
| 取用神 | `qimen-yongshen` |
| 空墓刑迫 | `qimen-sihai` |
| 宫盘关系 | `qimen-gongpan` |
| 主客生克 | `qimen-shengke` |
| 应期 | `qimen-yingqi` |
| 格局来源 | `qimen-gexia` |
| 基础 | `qimen-basics` |

调用任何下游技能时，本文件、`CURRENT_METHOD_CONSTRAINTS.md` 与 Prospective Case Protocol 的方法约束优先于旧技能中的无条件断语。

---

*方法论来源层：善天道、幺学声/《奇门遁甲预测学》、王云鹏《奇门遁甲应用学》、梁湘潤《奇門遁甲入門》与项目修炼日志。当前运行语义由 K2 Evidence、Book Distillate、Method Delta、Pre-Book Retrospective、`CURRENT_METHOD_CONSTRAINTS.md` 与前瞻 Registry Gate 共同约束。*
