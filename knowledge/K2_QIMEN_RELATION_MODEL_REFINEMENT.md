# K2 奇门关系模型修正：从关系配置到有向情境关系图

版本：2026-08-22
阶段：K2B / Deep Closure
状态：HYPOTHESIS / UNTESTED
Empirical Credit：NONE
Claim Extraction：BLOCKED

## 1. 为什么需要修正

Deep Closure 早期已经把“门、星、神、奇仪 = 固定吉凶词典”降级为候选特征，并提出 `RELATIONAL_CONFIGURATION`：具体判断应由对象在特定盘层、时间与关系中的组合决定。

QM-SRC-0024 完成 `pdf:p1-p110` 连续视觉复核后，这个模型仍暴露出一个自由度：**关系不能只表示为无序共现。**

来源层目前支持的结构约束包括：

- `QM-SRC-0024@pdf:p24`：同一阴阳遁背景下，不同 movement object 的布行方向可不同，不能把阴/阳遁直接当作所有对象共享的方向开关；
- `QM-SRC-0024@pdf:p40`：奇、门、太阴等条件以组合满足程度参与判断，说明应用逻辑不是单符号查表；
- `QM-SRC-0024@pdf:p44`：主客取用随具体位置条件变化，角色优先级不是全局常量；
- `QM-SRC-0024@pdf:p61`：`庚加直符` 与 `直符加庚` 被分别命名、分别处理；
- `QM-SRC-0024@pdf:p66`：`丙加甲` 与 `甲加丙` 被分别处理；
- `QM-SRC-0024@pdf:p73`：急缓状态会改变优先观察层，说明 layer priority 也属于 context。

这些只是 Source / Structural / Method Credit，不证明现实预测有效。

## 2. 当前修正：CONTEXTUAL_ORDERED_RELATION_GRAPH

暂定模型名：

`CONTEXTUAL_ORDERED_RELATION_GRAPH`

它不是一套已经成立的新奇门理论，而是用于减少解释自由度的候选表示层。

### 2.1 Node

节点不再只是“符号”，而是带类型的对象：

`person / asked_object / palace / stem / door / star / spirit / qi-yi / temporal_state / action_target`

同名术语若来自不同 ontology namespace，不自动合并。

### 2.2 Typed Directed Edge

关系必须保存方向与操作语义，例如：

`A --add_to--> B`
`A --reside_in--> palace`
`A --generate--> B`
`A --control--> B`
`A --combine--> B`
`A --clash--> B`
`A --host_of--> B`
`A --precede--> B`

因此：

`A + B != B + A`

除非来源或已验证规则明确证明该关系在当前语境下可交换。

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

缺失关键 context 时，正确动作可以是 `ABSTAIN / CONTEXT_REQUIRED`，而不是补故事。

### 2.4 Layer Selection

`PRIMARY / SECONDARY / CROSS-CHECK LAYERS` 不再假定全局固定。

候选规则：

`Layer Priority = f(question_domain, asked_object, action_intent, urgency, role, source/school context)`

这与 Dynamic Role Map 相容，但进一步要求把“为什么此时看这一层”事前冻结。

## 3. 场景推演顺序

候选推演流程修正为：

`QUESTION DOMAIN`
→ `ASKED OBJECT`
→ `OBJECT GRAPH`
→ `ROLE MAP`
→ `ACTION INTENT / URGENCY`
→ `ELIGIBLE RULE SET FREEZE`
→ `RELATION ORIENTATION FREEZE`
→ `PRIMARY / SECONDARY / CROSS-CHECK LAYERS`
→ `MOVEMENT CONTEXT`
→ `TYPED DIRECTED RELATION GRAPH`
→ `CONFLICT GRAPH`
→ `BOUNDARY GATE`
→ `PREDICTION / CONFIDENCE / ABSTENTION`

核心目标不是增加解释数量，而是让结果出现以后更难换方向、换角色、换层级、换关系含义。

## 4. 与旧模型的关系

`SYMBOL_DICTIONARY`
→ 降级为候选静态特征层。

`RELATIONAL_CONFIGURATION`
→ 保留为上位思想，但不能再默认关系无序。

`CONTEXTUAL_STATE_TRANSITION`
→ 继续负责 movement object 的状态转换；其输出可作为 relation graph 的 temporal/movement context。

`CONTEXTUAL_ORDERED_RELATION_GRAPH`
→ 负责把对象、方向、角色、关系类型和情境约束组合为可审计解释路径。

三者不是互相替换，而是不同层级：

`STATIC FEATURES -> STATE TRANSITIONS -> ORDERED RELATIONS -> SCENARIO INFERENCE`

## 5. 必须保留的边界

1. QM-SRC-0024 是复合/多装订单元 carrier；不能把整份 PDF 的作者、作品身份和内容自动归为一个 work。
2. p5 的赵普署名 credit 仅限第一文本 segment；不得外推给 p52-p107 第二装订单元。
3. 第二装订单元虽然明确属于 qimen 方法内容，但其完整 work identity / author lineage 当前仍未解决。
4. `庚加直符 != 直符加庚`、`丙加甲 != 甲加丙` 目前只证明该来源使用顺序敏感表示，不证明这些格局在现实中具有预测效度。
5. 任何原创模型都保持 `empirical_credit = NONE`，直到前瞻批次在结果未知时冻结并允许失败。

## 6. 如何证伪这个修正

未来若要把有向关系图从“更漂亮的表示”提升为有效方法，必须至少比较：

`ORDERED_DIRECTED_MODEL`
vs
`UNORDERED_RELATION_BASELINE`

在同一批预注册案例中，事前固定：

- object / role mapping；
- relation types 与方向；
- primary metric；
- threshold；
- stopping / exclusion rules；
- prediction 与 abstention。

如果有向模型不能提高预先固定的复现率、校准、判别或跨解读者一致性，反而只增加复杂度，或者仍需要在结果后改关系方向才能成立，则该模型应被降级或删除。

## 7. 当前结论

真正的认知重构不是“从别人的口诀换成自己的口诀”。

当前更合理的方向是：

**从符号结论转向对象关系，从无序共现转向有向关系，从固定优先级转向情境冻结，从解释能力转向可证伪能力。**

这个方向仍处于候选阶段。下一部来源若否定它，应修改它，而不是让来源迁就模型。
