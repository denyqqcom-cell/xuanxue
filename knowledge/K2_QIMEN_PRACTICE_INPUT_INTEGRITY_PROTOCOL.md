# K2 奇门实战输入完整性协议 v0.1

状态：`ACTIVE / FAIL-CLOSED`  
阶段：K2B Cognitive Reconstruction  
Empirical Credit：`NONE`

## 1. 为什么需要这一层

前瞻冻结只能保证“冻结以后没有改”，不能保证“冻结进去的输入一开始就是对的”。

因此新增核心区分：

`FREEZE INTEGRITY != INPUT CORRECTNESS`

一次低风险实战复核已经暴露出典型风险：同一个天干在不同盘层可以形成不同 symbol instance；如果只记“某干落某宫”而不标天盘/地盘，后续角色、生克与场景解释可能建立在错误宫位上。这个错误必须在 Outcome 之前被输入完整性 Gate 拦截，而不是等结果出来以后用新解释修补。

## 2. Symbol type 与 symbol instance

统一执行：

`SYMBOL TYPE != SYMBOL INSTANCE`

`SAME STEM != SAME STATE`

“辛”“戊”“开门”“天辅”等名称首先只是 symbol type/value。进入具体盘局时，至少还要保存它属于哪一个 plate/layer、落哪一宫、在什么 source/method context 下被读取。

对需要盘层定位的对象，最低表示为：

`symbol_value × plate_layer × palace × source_method_basis`

缺任一关键维度，不允许静默压成唯一角色状态。

## 3. Plate layer 标签不等于时间语义

再执行一个独立边界：

`PLATE LAYER TAG != PLATE LAYER SEMANTICS`

标记 `SKY_PLATE / EARTH_PLATE` 只是识别 symbol instance；“天盘代表什么、地盘代表什么”仍然属于 source-local / school-local 方法语义。

因此禁止仅凭项目统一命名就宣称：

- 天盘必然等于未来；
- 地盘必然等于过去；
- 某一盘层必然优先代表人物；
- 不同流派同名盘层语义完全相同。

若来源语义未冻结，`semantics_status = UNRESOLVED`，必要时 HOLD/ABSTAIN。

## 4. 实战输入链

正式场景推演顺序改为：

`RAW PLATE -> SYMBOL INSTANCE REGISTER -> PLATE/PALACE TAG -> READBACK -> SOURCE-LOCAL SEMANTICS -> ROLE MAPPING -> SCENARIO INFERENCE -> FREEZE`

不能从截图/盘面直接跳到“某人=某宫=某结果”。

### 4.1 Symbol Instance Register

每条 `symbolic_mapping_hypothesis` 至少保存：

- world_variable；
- candidate_symbolic_role；
- symbol_type；
- symbol_value；
- plate_layer；
- palace；
- readback_status；
- source_method_basis；
- plate_layer_semantics；
- semantics_status；
- alternatives；
- boundary；
- failure_condition；
- `instance_collapse_blocked=true`。

### 4.2 Readback

读取盘面后至少要显式标记：

- `VERIFIED`：已完成独立复读/交叉核验；
- `SINGLE_READ`：只有一次读取，允许研究但降低置信；
- `CONTESTED`：两次读取或来源解释冲突，不能当成稳定输入；
- `NOT_APPLICABLE`：该映射本身不依赖盘层读取。

如果关键角色映射处于 `CONTESTED`，正式预测不得假装输入稳定。

## 5. Role mapping 与 plate mapping 分离

“这个符号在哪里”与“它代表现实中的谁/什么”是两道不同问题。

先回答：

`symbol instance identity`

再回答：

`world_variable -> candidate_symbolic_role`

即使年命、日干、年干、值符等都能成为某类人物候选，也不能因为其中一个解释顺手，就结果后切换。plate readback 正确也不代表 role mapping 正确。

## 6. 实战错误如何记分

以下都属于模型/执行失败信号，而不是可以被解释掉的“小误差”：

- 盘层未标导致落宫读错；
- 同一天干的天/地盘实例被压成一个“唯一宫位”；
- 读取错误直到结果后才被发现；
- 结果后才决定原来应该看另一盘层；
- 用流派A的盘层语义解释流派B而没有显式桥接；
- 为保住原预测而修改原始读盘记录。

如果错误在 Outcome 前发现，可以更正输入并重新 Freeze；旧错误必须保留为 practice lesson。若 Outcome 已知后才发现，只能记 `post_hoc correction`，原预测不能被洗成命中。

## 7. 与 QCIC / SCRM / Prospective Gate 的关系

QCIC 控制来源、规则、程序与反馈后自由度；SCRM 控制场景与角色映射；Prospective Gate 控制冻结链。

本协议补的是它们之间以前缺失的一层：

`INPUT CORRECTNESS / SYMBOL INSTANCE INTEGRITY`

所以：

`VALID HASH CHAIN + WRONG PLATE READ = WRONG FROZEN CASE`

工程冻结不能替代盘面读取正确性。

## 8. 验证方向

该协议本身也没有经验特权。后续至少比较：

1. layer-tagged mapping 与未标层 mapping 的读盘错误率；
2. 单次读取与独立 readback 的错误发现率；
3. layer-tagging 是否提高跨解读者复现性；
4. 增加这一层后是否只增加文档复杂度而没有降低错误。

如果没有增量价值，应简化；如果仍频繁发生错误，应继续收紧输入协议，而不是增加解释口诀。

Empirical Credit 始终保持：`NONE`。
