# K2 Cognitive Audit：认知偏差与纠偏登记

版本：2026-08-22
阶段：K2B / Deep Closure
状态：ACTIVE

本文件记录项目自身已经暴露出的认知偏差、方法风险与纠偏动作。它不是对古籍真伪的裁决，也不是 Claim 文件。

原则：**错误不删除，误区不美化，修正必须留下来路。**

## A01 实现锚定偏差 / IMPLEMENTATION_ANCHORING

### 旧路径

先有代码、旧 handoff 或既有盘面结构，再寻找书证支持。

### 已观察风险

旧 qimen handoff 曾在“独立重读 PDF = 0”的情况下形成 36 条规则、17 个 fixtures，并对部分排盘结构作工程判断。

### 纠偏

以后代码只能作为待检假设：

`SOURCE -> READING -> EVIDENCE -> STRUCTURE -> BOUNDARY -> HYPOTHESIS -> IMPLEMENTATION`

### 状态

`CORRECTION_ACTIVE`

---

## A02 摘要替代原书 / NOTE_SUBSTITUTION

### 旧路径

把用户笔记、handoff、摘要或提取产物当成原书本身。

### 风险

摘要天然会丢失：上下文、例外、术语原貌、图表关系、作者自限、内部矛盾。

### 纠偏

Reading Credit 只来自真实 source review；packet READY、OCR 成功、笔记完整都不等于 COMPLETE。

### 状态

`CORRECTION_ACTIVE`

---

## A03 符号字典化 / SYMBOL_DICTIONARY_REDUCTION

### 旧路径

把门、星、神、奇仪压成固定吉凶或固定人格/事件词典。

### 风险

失去问题域、对象、角色、宫位关系、旺衰、生克、时间与流派上下文。

### 纠偏

符号只作为候选特征，必须进入场景对象关系中解释。

### 状态

`CORRECTION_ACTIVE`

---

## A04 文本支持膨胀为现实有效 / TEXT_TO_TRUTH_INFLATION

### 旧路径

来源重复、作者自称验证、案例很多，容易被感知为“规则更真”。

### 纠偏

严格拆分：

- SOURCE_CREDIT
- STRUCTURAL_CREDIT
- METHOD_CREDIT
- EMPIRICAL_CREDIT

前三者不能自动升级到第四者。

### 状态

`HARD_GATE`

---

## A05 回顾性命中偏差 / RETROSPECTIVE_HIT_BIAS

### 旧路径

结果已知后仍允许补选规则、调整用神、改解释路径，再把新解释算作原判断命中。

### 纠偏

使用：

`FROZEN_INTERPRETATION_PATH`
`ELIGIBLE_RULE_SET_FREEZE`
`FAILURE_LOG`

反馈后新增解释只能记录为“事后解释”，不能回写为事前预测。

### 状态

`HARD_GATE`

---

## A06 Movement 变量塌缩 / MOVEMENT_VARIABLE_COLLAPSE

### 旧路径

用“阳顺阴逆”等总口诀覆盖所有移动对象。

### 新认识

QM-SRC-0022 的完整阅读已迫使项目拆分 movement：

`object × temporal_context × anchor × cadence × direction × path × center_policy × school_context`

### 状态

`MODEL_REFACTORED`

---

## A07 Ontology 扁平化 / ONTOLOGY_FLATTENING

### 旧路径

看到“神”字就归入同一 gods 集合；看到相似现代名称就直接同义化。

### 风险

八神、九头神、神煞、神遁/鬼遁以及功能身份可能属于不同 ontology 层。

### 纠偏

保留 source-local term；跨源只建立显式 relation，不静默改名。

### 状态

`MODEL_REFACTORED`

---

## A08 伪冲突 / FALSE_CONTRADICTION

### 旧路径

两句话方向不同就直接判定冲突。

### 风险

实际可能是 object、layer、trigger、cadence、temporal_context、relative_order 不同。

### 纠偏

冲突前先拆：

`object / layer / trigger / cadence / direction / relative_order / application_context`

无法确定时使用 `CONTEXT_REQUIRED`。

### 状态

`CORRECTION_ACTIVE`

---

## A09 重复来源票数膨胀 / LINEAGE_VOTE_INFLATION

### 旧路径

按 PDF 文件数或书名数计算“多来源一致”。

### 风险

上下册、同一讲义变体、重印、摘录、派生本可能并不独立。

### 纠偏

任何跨源共识先过 Source Lineage；没有独立性，不增加 independent evidence credit。

### 状态

`HARD_GATE`

---

## A10 权威与年代偏差 / AUTHORITY_ANTIQUITY_BIAS

### 旧路径

古籍更早、作者更有名、传统流传更久，容易被心理上赋予更高有效性。

### 纠偏

年代和作者只能影响 provenance/historical credit，不直接增加 empirical credit。

### 状态

`CORRECTION_ACTIVE`

---

## A11 统一理论冲动 / PREMATURE_UNIFICATION

### 旧路径

遇到流派差异时倾向尽快找一个“正确版本”。

### 风险

过早统一会抹掉适用条件，造成错误普适化。

### 纠偏

竞争规则长期并存，直到对象、场景、来源与前瞻测试足以支持缩并。

### 状态

`CORRECTION_ACTIVE`

---

## A12 协议自指漂移 / SELF_REFERENTIAL_STATE_DRIFT

### 事件

K2 Deep Closure 首版把创建前的 exact HEAD 与 CI run 直接写入长期协议。文件一提交，文中的“当前 HEAD”立即变旧。

### 反省

这是工程层面的同类认知错误：把动态事实误当稳定真理。

### 纠偏

Stable Contract 与 Runtime Fact 分离；每次执行前 fresh read，而不是让长期协议保存“当前”。

### 状态

`FIXED_2026-08-22`

---

## A13 载体—作品塌缩 / COMPOSITE_CARRIER_FLATTENING

### 事件

QM-SRC-0023 在完整 `pdf:p1-p185` 连续视觉复核前，看起来可以被文件名直接理解为“《甲遁真授秘录》下册，薛凤祚著”。完整阅读后才发现，同一个 PDF 实际包含至少三个作品层级与出版附页：

- p1-p67：《甲遁真授秘錄（下）》；
- p68-p104：《瑞應圖記》；
- p105-p177：《乾坤變異錄》；
- p178-p185：现代出版目录、版权及书目资料。

### 暴露的旧假设

项目过去默认：

`one PDF/source_id = one work = one author = one domain`

这个假设不是来源事实，而是旧 schema 为方便工程处理偷偷加入的简化。

### 风险

若按文件名直接升格：

- 会把 p68-p177 两个附载作品错误归给薛凤祚；
- 会把非奇门材料错误计入 qimen Evidence；
- 会把一个 composite carrier 错配到单一 work_id；
- 任何后续“多来源一致”都会被错误 lineage 污染。

### 纠偏

强制增加 carrier/work 中间层：

`CARRIER -> SEGMENT -> WORK -> AUTHOR / DOMAIN / LINEAGE -> EVIDENCE`

已建立 `K2_SOURCE_SEGMENTS.jsonl` 与 fail-closed validator。遇到 composite carrier 时，旧 source-level schema 不够表达，就修改 schema，不把事实压扁去迎合旧 schema。

### 状态

`MODEL_REFACTORED`

---

## A14 冻结表演与批次后见自由度 / VALIDATION_THEATER

### 事件

项目第一次把“证”工程化时，初版 prospective gate 已要求单案例在结果未知前冻结 Role Map、Eligible Rule Set、Interpretation Path、Prediction 与 Confidence，但仍遗漏了两个更隐蔽的自由度：

1. primary metric、threshold、stopping rule、exclusion rule 若在看过一批结果后才确定，单案例 Freeze 仍会被批次层 hindsight 污染；
2. 如果 Plan、Batch、Freeze、Outcome 之间只靠 ID 引用，上游合同仍可能在后来被改写而不立即触发当前态校验。

### 反省

“有 Freeze 文件”不等于真正的前瞻验证。验证制度自身也可能成为一种仪式：表面上减少了自由度，实际上把自由度转移到指标选择、停止规则、排除规则或上游记录改写。

### 纠偏

Prospective Validation 被升级为：

`TEST PLAN -> BATCH PREREGISTRATION -> CASE FREEZE -> OUTCOME -> BATCH REVIEW`

并建立 hash-bound provenance：

`PLAN --plan_sha256--> BATCH --batch_sha256--> FREEZE --freeze_record_sha256--> OUTCOME`

批次指标、decision rule、停止/排除规则必须在该批 Outcome 前冻结；单案例与单批次仍不得直接升级 Empirical Credit。

### 状态

`MODEL_REFACTORED_2026-08-22`

---

## A15 无序关系塌缩 / UNORDERED_RELATION_COLLAPSE

### 事件

QM-SRC-0024 完成 `pdf:p1-p110` 连续视觉复核后，第二装订单元出现明确的顺序敏感结构：p61 将“庚加直符”与“直符加庚”列为不同格局，p66 又将“丙加甲”与“甲加丙”分别处理；p73 还显示观察层的取用可随急缓而变化。第一装订单元 p24 同时显示六仪、三奇的布行方向并不能被压成一个对所有对象相同的方向开关，p44 的主客取用也随具体位置条件变化。

### 暴露的旧假设

项目从 SYMBOL_DICTIONARY 转向 RELATIONAL_CONFIGURATION 后，仍可能潜藏一个更细的简化：

`relationship = unordered co-occurrence set`

如果把局面只编码成 `{甲, 丙}`、`{庚, 直符}` 或“这些要素同时出现”，那么 `A -> B`、`B -> A`、A 临 B、A 克 B、A 为主/B 为客都会被压成同一个关系袋。

### 风险

- `A + B` 与 `B + A` 被错误视为同一配置；
- 主客、作用方向、先后、临乘、生克等操作语义丢失；
- 模型表面上已经脱离固定吉凶词典，实际上只是把“符号词典”升级成“关系词袋”；
- 事后解释者可以重新选择关系方向，继续保留大量 hindsight freedom。

### 纠偏

下一阶段的候选表示必须至少区分：

`NODE = object / palace / stem / door / star / spirit`

`TYPED DIRECTED EDGE = add_to / reside_in / generate / control / combine / clash / host_guest / precede`

`CONTEXT = question_domain / temporal_context / role / action_intent / urgency / school_context`

因此当前 `RELATIONAL_CONFIGURATION` 只保留为上位候选概念，不能假定关系天然无序；更严格的方向是构造 **有向、有序、类型化、情境约束的关系图**。这仍只是来源驱动的模型修正，不获得现实有效性信用。

### 状态

`MODEL_REFINEMENT_REQUIRED_2026-08-22`

---

# 每书复盘最小问题集

每完成一本书或一个 work family，PROJECT_MAIN_AGENT 必须回答：

1. 这本书真正增加了什么结构理解？
2. 哪些只是重复传统说法？
3. 哪些规则的边界原先被我忽略？
4. 哪些旧认知被推翻、降级或拆分？
5. 哪些冲突其实不是同一个对象？
6. 哪些内容完全不能从本书获得 reality/empirical credit？
7. 有哪些规则最容易产生 hindsight freedom？
8. 如果要验证，怎样在反馈前冻结？
9. 什么结果会迫使我承认该假设失败？
10. 当前模型是否因为这本书变得更可约束，而不是仅仅更复杂？
11. 我是否把一个 PDF/载体误当成了一个作品、一个作者或一个领域？
12. 我的验证协议是否仍允许在结果后改变指标、阈值、停止/排除规则，或悄悄改写上游合同？
13. 我的关系表示是否保留顺序、方向、角色与操作语义，而不是把 `A+B` 与 `B+A` 压成同一个共现集合？

如果第 9 问无法回答，该理论当前不可证伪，只能保留为来源描述或解释性假设。
