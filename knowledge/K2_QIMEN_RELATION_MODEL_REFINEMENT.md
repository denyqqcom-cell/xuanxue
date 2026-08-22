# K2 奇门关系模型修正：从关系配置到生成—状态—关系—场景四层模型

版本：2026-08-23
阶段：K2B / Deep Closure
状态：HYPOTHESIS / UNTESTED
Empirical Credit：NONE
Claim Extraction：BLOCKED

## 1. 为什么需要继续修正

Deep Closure 早期已经把“门、星、神、奇仪 = 固定吉凶词典”降级为候选特征，并提出 `RELATIONAL_CONFIGURATION`：具体判断应由对象在特定盘层、时间与关系中的组合决定。

随后连续来源不断暴露这个表示仍然过粗：

- QM-SRC-0024 显示关系存在方向与顺序，`A+B` 不能自动视为 `B+A`；
- QM-SRC-0025 / 0026 显示同名符号还必须区分天盘、地盘、宫位等具体 instance；
- QM-SRC-0032 / 0034 / 0033 三册完整阅读进一步显示，盘态知识本身还存在“生成规则”和“已经展开的有限状态空间”两种不同表示。

因此当前问题已不只是“怎样解释一个盘”，还必须先回答：

1. 这个状态怎样产生或被索引；
2. 当前完整状态是什么；
3. 状态中的对象实例如何形成有向关系；
4. 哪些关系在当前问题场景中有资格进入推演。

这些仍只是 Source / Structural / Method Credit，不证明现实预测有效。

## 2. 第一层：SOURCE-LOCAL ONTOLOGY

在任何生成、关系或场景推演之前，先确定来源自己如何定义术语。

曾子南《三元奇门遁甲讲义》上册 `pdf:p8` 明确把天干阴阳与三元奇门干支五行放在“以先天六十四卦……为准/为用”的框架中。

因此：

`same label != same ontology`

例如不同来源都写“甲、乙、五行、合化”，不能仅因为文字相同就自动继承同一套现代标准定义。

跨来源必须经过：

`SOURCE TERM`
→ `SOURCE-LOCAL DEFINITION`
→ `EXPLICIT CROSS-SOURCE RELATION`
→ `OPTIONAL NORMALIZATION`

若不能建立可靠映射，则保留并存，不做静默同义化。

这不是新增一个与 A07 重复的认知偏差编号，而是把既有 `ONTOLOGY_FLATTENING` 的纠偏落实到更严格的数据流中。

## 3. 第二层：GENERATIVE LAYER

`GENERATIVE LAYER` 回答：

**状态如何被生成、推进或索引。**

这里可以容纳此前的 `CONTEXTUAL_STATE_TRANSITION`：

`movement_object × temporal_context × anchor × cadence × direction × path × center_policy × school_context`

但它不再被当作盘态知识的全部。

生成规则、移动规则、索引规则可以产生某个状态；它们的正确性应单独测试，不能因为最终解释“看起来合理”就倒推生成过程正确。

## 4. 第三层：STATE LAYER

曾子南三册在完整视觉阅读后形成明确连续状态空间：

- 上册收束至 `360`；
- 中册由 `361` 延续至 `720`；
- 下册由 `721` 延续至 `1080`。

因此需要独立表示：

`ENUMERATED_STATE_LATTICE`

它回答：

**给定某个索引后，完整配置状态是什么。**

这与生成规则不同。

候选关系：

`GENERATIVE RULES -> STATE`

或：

`INDEX / LOOKUP -> ENUMERATED STATE`

同一个 STATE 可以既由算法生成，也由已展开表格查得；两条路径可用于互相校验，但不能因此把“状态表存在”解释成“生成算法已被现实验证”。

### 4.1 State Integrity

状态层至少需要保存：

- state / index identity；
- source / school context；
- 图式中的完整位置结构；
- 若可判定，生成/索引依据；
- carrier integrity 状态。

扫描坏页必须显式表示为缺口，而不是用邻近序号补造内容。

当前已观察：

- QM-SRC-0034 `pdf:p107` 严重扫描损坏；
- QM-SRC-0033 `pdf:p88`、`pdf:p121` 严重扫描损坏；
- QM-SRC-0033 `pdf:p97` 近空白。

这些页获得“已检查”的 Reading Credit，但不可获得可靠 Content Evidence。

## 5. 第四层：LAYER-QUALIFIED RELATION INFERENCE

状态确定以后，关系模型仍不能退回符号词袋。

暂定表示：

`CONTEXTUAL_ORDERED_LAYERED_RELATION_GRAPH`

### 5.1 Node Instance

`node_instance = entity_type × source_local_identity × layer/plane × palace/position × temporal_state × role`

实体可包括：

`person / asked_object / palace / stem / door / star / spirit / qi-yi / temporal_state / action_target`

例如：

`戊@天盘 != 戊@地盘`

除非来源与当前方法明确允许二者在某一步投影为同一抽象 stem type。

### 5.2 Typed Directed Edge

关系必须保存方向与操作语义，例如：

`A@layer1 --add_to--> B@layer2`
`A --reside_in--> palace`
`A --generate--> B`
`A --control--> B`
`A --combine--> B`
`A --clash--> B`
`A --host_of--> B`
`A --precede--> B`

因此：

`A + B != B + A`

并且：

`A@天盘 + B@地盘 != A@地盘 + B@天盘`

除非来源或已验证规则明确证明当前关系可交换或可跨层投影。

## 6. 第五层：SCENARIO REASONING

关系本身也不能脱离问题场景直接输出结论。

候选 Context Vector：

`question_domain`
`asked_object`
`temporal_context`
`role`
`action_intent`
`urgency`
`school_context`
`movement_context`
`observation_context`

场景层负责：

- Dynamic Role Map；
- Eligible Rule Set；
- Primary / Secondary / Cross-check Layers；
- Conflict Graph；
- Boundary Gate；
- Prediction / Confidence / Abstention。

缺失关键 context 时，合法答案可以是：

`ABSTAIN / CONTEXT_REQUIRED`

而不是补故事。

## 7. 当前总体架构

当前候选架构已经从：

`STATIC SYMBOL TYPES`
→ `STATE TRANSITIONS`
→ `ORDERED RELATIONS`
→ `SCENARIO INFERENCE`

进一步修正为：

`SOURCE-LOCAL ONTOLOGY`
→ `GENERATIVE LAYER`
→ `STATE LAYER`
→ `LAYER-QUALIFIED RELATION INFERENCE`
→ `SCENARIO REASONING`

简写：

**定义 → 生成 → 状态 → 关系 → 场景。**

这不是为了增加层数，而是为了把不同错误拆开：

- ontology mapping error；
- state generation / retrieval error；
- instance / relation error；
- scenario / role error；
- outcome interpretation error。

如果所有错误都压在“断得准不准”一个结果上，模型仍然可以在结果后随意改解释层，无法知道究竟哪里错。

## 8. 关键认知修正：会排盘不等于会解盘

曾子南三册最重要的结构启发之一，是把完整状态空间大规模展开出来。

这迫使项目明确：

`STATE GENERATION / RETRIEVAL ACCURACY`

与

`INTERPRETATION VALIDITY`

是两个独立验证对象。

一个系统可能：

- 状态排得完全正确，但角色映射、关系方向或场景推演错误；
- 解释框架看似自洽，但底层状态生成已错；
- 状态表和解释都来源一致，却现实预测效度仍然不存在。

因此未来任何案例验证都必须至少区分“盘态是否正确”和“推演是否正确”，不能只看最后一句结果是否碰巧命中。

## 9. 场景推演顺序

当前候选流程：

`SOURCE / SCHOOL BINDING`
→ `SOURCE-LOCAL ONTOLOGY`
→ `QUESTION DOMAIN`
→ `ASKED OBJECT`
→ `ROLE MAP`
→ `GENERATIVE / STATE RETRIEVAL`
→ `STATE INTEGRITY CHECK`
→ `ELIGIBLE RULE SET FREEZE`
→ `INSTANCE / LAYER BINDING FREEZE`
→ `RELATION ORIENTATION FREEZE`
→ `PRIMARY / SECONDARY / CROSS-CHECK LAYERS`
→ `TYPED DIRECTED LAYERED RELATION GRAPH`
→ `CONFLICT GRAPH`
→ `BOUNDARY GATE`
→ `PREDICTION / CONFIDENCE / ABSTENTION`

核心目标仍然不是增加解释数量，而是让结果出现后更难换 ontology、换状态、换对象、换盘层、换方向、换角色或换规则。

## 10. 必须保留的边界

1. 完整阅读只提供来源、结构与方法信用，不提供现实预测准确率。
2. 曾子南三册的 `1→1080` 是本 work family 的结构事实，不等于所有奇门体系都必须采用同一状态空间。
3. 同名干支、五行、合化等术语跨流派不得自动归一化。
4. 图式内容必须保留视觉结构，不能用 OCR 字符串替代。
5. 损坏页的前后编号只能帮助定位结构缺口，不能恢复原页具体内容。
6. 任何原创模型继续保持 `empirical_credit = NONE`，直到 prospective batch 在结果未知时冻结并允许失败。
7. 不因新的来源支持了当前模型，就停止寻找反例；后续善天道等现代体系应优先用于攻击该模型，而不是为它补书证。

## 11. 如何证伪当前修正

### H-SY-001：四层架构是否真正有信息增益

比较：

`GENERATIVE -> STATE -> RELATION -> SCENARIO MODEL`

与

`MONOLITHIC RULE -> RESULT BASELINE`

如果分层后不能：

- 更准确定位错误来源；
- 提高重构复现率；
- 降低结果后改规则的自由度；
- 提高跨解读者一致性；

反而只是增加术语和复杂度，则应收缩模型。

### H-SY-002：source-local ontology 是否必要

比较：

`SOURCE_LOCAL_ONTOLOGY + EXPLICIT_MAPPING`

与

`SAME_LABEL_DEFAULT_NORMALIZATION`

如果前者不能减少术语错配、规则冲突或跨解读者分歧，则不应把它神圣化。

## 12. 当前结论

闭关后的模型不应该越来越“会解释”，而应该越来越**难以事后解释**。

当前方向不是创造一套新的万能口诀，而是建立一套能明确回答：

- 我现在采用的是哪一来源定义；
- 盘态是怎样生成或查得的；
- 当前完整状态是什么；
- 谁在什么盘层作用于谁；
- 当前问题为什么允许看这条规则；
- 哪一步若错，整个结论应当怎样失败。

下一批来源如果不能支持这种分层，或者证明某些层没有信息增益，就删层、合并或重构，而不是让来源迁就模型。
