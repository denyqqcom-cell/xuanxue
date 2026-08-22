# K2 奇门关系模型修正：从关系配置到有向、分层情境关系图

版本：2026-08-22
阶段：K2B / Deep Closure
状态：HYPOTHESIS / UNTESTED
Empirical Credit：NONE
Claim Extraction：BLOCKED

## 1. 为什么需要修正

Deep Closure 早期已经把“门、星、神、奇仪 = 固定吉凶词典”降级为候选特征，并提出 `RELATIONAL_CONFIGURATION`：具体判断应由对象在特定盘层、时间与关系中的组合决定。

QM-SRC-0024 完成 `pdf:p1-p110` 连续视觉复核后，这个模型首先暴露出一个自由度：**关系不能只表示为无序共现。**

来源层已支持的结构约束包括：

- `QM-SRC-0024@pdf:p24`：同一阴阳遁背景下，不同 movement object 的布行方向可不同，不能把阴/阳遁直接当作所有对象共享的方向开关；
- `QM-SRC-0024@pdf:p40`：奇、门、太阴等条件以组合满足程度参与判断，说明应用逻辑不是单符号查表；
- `QM-SRC-0024@pdf:p44`：主客取用随具体位置条件变化，角色优先级不是全局常量；
- `QM-SRC-0024@pdf:p61`：`庚加直符` 与 `直符加庚` 被分别命名、分别处理；
- `QM-SRC-0024@pdf:p66`：`丙加甲` 与 `甲加丙` 被分别处理；
- `QM-SRC-0024@pdf:p73`：急缓状态会改变优先观察层，说明 layer priority 也属于 context。

继续阅读 QM-SRC-0025 到 `pdf:p150` 后，又出现更强的限制：

- `QM-SRC-0025@pdf:p59-p66`《十干克应诀》不是只写“戊与乙”“乙与丙”等共现，而是系统写成“**天盘某干加地盘某干**”；
- 因此同一个字符/干名若处在不同盘层，不能自动视为同一个 graph node；
- “A 加 B”的方向之外，还必须保留 `A@天盘`、`B@地盘` 这类 layer-qualified identity；
- `QM-SRC-0025@pdf:p68-p89` 九星条目又按时序、方向及外应条件产生大量分支，说明 context 不只是问题类别，还可能进入时间/空间/观察条件；
- `QM-SRC-0025@pdf:p90-p150` 持续出现三奇到宫、十干、八门、九遁、主客与具体占类，进一步说明不能让某一符号脱离所处盘层、角色与占类直接继承固定结论。

这些仍只是 Source / Structural / Method Credit，不证明现实预测有效。

## 2. 当前修正：CONTEXTUAL_ORDERED_LAYERED_RELATION_GRAPH

暂定模型名：

`CONTEXTUAL_ORDERED_LAYERED_RELATION_GRAPH`

它不是一套已经成立的新奇门理论，而是用于减少解释自由度的候选表示层。

### 2.1 Node Instance

节点不再只是“符号类型”，而必须允许表示**具体实例**：

`node_instance = entity_type × source_local_identity × layer/plane × palace/position × temporal_state × role`

实体类型可包括：

`person / asked_object / palace / stem / door / star / spirit / qi-yi / temporal_state / action_target`

例如：

`戊@天盘 != 戊@地盘`

除非来源与当前方法明确允许二者在某一计算步骤中投影为同一抽象 stem type。

同名术语若来自不同 ontology namespace，也不自动合并。

### 2.2 Typed Directed Edge

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

除非来源或已验证规则明确证明该关系在当前语境下可交换、可跨层投影。

### 2.3 Context Vector

每条关系至少绑定可用的情境变量：

`question_domain`
`asked_object`
`temporal_context`
`role`
`action_intent`
`urgency`
`school_context`
`movement_context`
`observation_context`

缺失关键 context 时，正确动作可以是 `ABSTAIN / CONTEXT_REQUIRED`，而不是补故事。

### 2.4 Layer Selection

`PRIMARY / SECONDARY / CROSS-CHECK LAYERS` 不再假定全局固定。

候选规则：

`Layer Priority = f(question_domain, asked_object, action_intent, urgency, role, source/school context)`

这与 Dynamic Role Map 相容，但进一步要求把“为什么此时看这一层”事前冻结。

### 2.5 Type 与 Instance 必须分开

当前进一步规定：

`SYMBOL TYPE` 只回答“它是什么类别”；

`SYMBOL INSTANCE` 回答“它此刻在哪一盘、哪一宫、什么时态、承担什么角色”。

同一个 type 可以在同一局内产生多个 instance。若模型把所有同名 instance 先合并再推演，就会在进入关系计算前已经丢失信息。

## 3. 场景推演顺序

候选推演流程修正为：

`QUESTION DOMAIN`
→ `ASKED OBJECT`
→ `OBJECT GRAPH`
→ `ROLE MAP`
→ `ACTION INTENT / URGENCY`
→ `ELIGIBLE RULE SET FREEZE`
→ `INSTANCE / LAYER BINDING FREEZE`
→ `RELATION ORIENTATION FREEZE`
→ `PRIMARY / SECONDARY / CROSS-CHECK LAYERS`
→ `MOVEMENT CONTEXT`
→ `TYPED DIRECTED LAYERED RELATION GRAPH`
→ `CONFLICT GRAPH`
→ `BOUNDARY GATE`
→ `PREDICTION / CONFIDENCE / ABSTENTION`

核心目标不是增加解释数量，而是让结果出现以后更难换对象实例、换盘层、换方向、换角色、换观察层或换关系含义。

## 4. 与旧模型的关系

`SYMBOL_DICTIONARY`
→ 降级为候选静态特征层。

`RELATIONAL_CONFIGURATION`
→ 保留为上位思想，但不能再默认关系无序，也不能默认同名符号只有一个实例。

`CONTEXTUAL_STATE_TRANSITION`
→ 继续负责 movement object 的状态转换；其输出可作为 relation graph 的 temporal/movement context。

`CONTEXTUAL_ORDERED_LAYERED_RELATION_GRAPH`
→ 负责把对象实例、盘层、方向、角色、关系类型和情境约束组合为可审计解释路径。

因此当前层级更准确地写成：

`STATIC SYMBOL TYPES`
→ `LAYERED INSTANCES`
→ `STATE TRANSITIONS`
→ `ORDERED RELATIONS`
→ `SCENARIO INFERENCE`

## 5. 必须保留的边界

1. QM-SRC-0024 是复合/多装订单元 carrier；不能把整份 PDF 的作者、作品身份和内容自动归为一个 work。
2. p5 的赵普署名 credit 仅限第一文本 segment；不得外推给 p52-p107 第二装订单元。
3. QM-SRC-0025 当前仅完成 `pdf:p1-p150 / 383`，仍是 PARTIAL；不能用当前阶段观察代表整册。
4. QM-SRC-0025 题名页“诸葛亮等著 / 刘伯温点校 / 陈管明注评”只属于 edition attribution；历史作者真实性尚未验证。
5. QM-SRC-0025 的 `[白话译释]` 属于现代 translation/paraphrase voice，不得和 base text 共用一个 Evidence voice。
6. `庚加直符 != 直符加庚`、`丙加甲 != 甲加丙`、以及“天盘 A 加地盘 B”的层级表达，目前只证明相关来源采用顺序/层级敏感表示，不证明这些格局在现实中具有预测效度。
7. 任何原创模型都保持 `empirical_credit = NONE`，直到前瞻批次在结果未知时冻结并允许失败。

## 6. 如何证伪这个修正

未来若要把有向、分层关系图从“更完整的表示”提升为有效方法，必须至少比较：

`ORDERED_LAYERED_MODEL`
vs
`ORDERED_UNLAYERED_BASELINE`
vs
`UNORDERED_RELATION_BASELINE`

在同一批预注册案例中，事前固定：

- object / role mapping；
- instance/layer bindings；
- relation types 与方向；
- primary metric；
- threshold；
- stopping / exclusion rules；
- prediction 与 abstention。

如果保留 layer identity 不能提高预先固定的复现率、校准、判别或跨解读者一致性，反而只增加复杂度，或者仍需要在结果后重新指定“这个戊到底算天盘还是地盘”才能成立，则 layer-qualified refinement 应被降级或删除。

## 7. 当前结论

真正的认知重构不是“从别人的口诀换成自己的口诀”。

当前更合理的方向是：

**从符号结论转向对象实例，从无序共现转向有向关系，从同名符号合并转向盘层绑定，从固定优先级转向情境冻结，从解释能力转向可证伪能力。**

这个方向仍处于候选阶段。下一批来源若否定它，应修改它，而不是让来源迁就模型。
