# K2 奇门实战输入完整性协议 v0.2

状态：`ACTIVE / FAIL-CLOSED`  
阶段：K2B Cognitive Reconstruction  
Empirical Credit：`NONE`

## 1. 为什么需要这一层

前瞻冻结只能保证“冻结以后没有改”，不能保证“冻结进去的输入一开始就是对的”。

因此新增核心区分：

`FREEZE INTEGRITY != INPUT CORRECTNESS`

一次低风险实战复核已经暴露出典型风险：同一个天干在不同盘层可以形成不同 symbol instance；如果只记“某干落某宫”而不标天盘/地盘，后续角色、生克与场景解释可能建立在错误宫位上。这个错误必须在 Outcome 之前被输入完整性 Gate 拦截，而不是等结果出来以后用新解释修补。

随后完整复核 `QM-SRC-0010` 又增加了一项来源内约束：在该来源的阳遁/阴遁实例中，八神 vocabulary 并非完全相同。因此 `dun_mode` 不能只被当作一个旋转方向的实现参数；在某些 source-local method 中，它参与定义 symbol system 本身。

## 2. Symbol type 与 symbol instance

统一执行：

`SYMBOL TYPE != SYMBOL INSTANCE`

`SAME STEM != SAME STATE`

`DUN MODE != ROTATION DIRECTION ONLY`

“辛”“戊”“开门”“天辅”等名称首先只是 symbol type/value。进入具体盘局时，至少还要保存它属于哪一个 plate/layer、落哪一宫、处于哪一种遁法模式、在什么 source/method context 下被读取。

对需要盘层定位的对象，最低表示升级为：

`symbol_value × plate_layer × palace × dun_mode × source_method_basis`

缺任一关键维度，不允许静默压成唯一角色状态。

如果来源明确不依赖阴/阳遁，可用 `NOT_APPLICABLE`；如果方法层尚未确定，则必须用 `UNRESOLVED`，不能猜。

## 3. Plate layer 标签不等于时间语义

继续执行：

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

`RAW PLATE -> DUN MODE TAG -> SYMBOL INSTANCE REGISTER -> PLATE/PALACE TAG -> READBACK -> SOURCE-LOCAL SEMANTICS -> ROLE MAPPING -> SCENARIO INFERENCE -> DECISION TIE-BREAK FREEZE -> PREDICTION FREEZE`

不能从截图/盘面直接跳到“某人=某宫=某结果”。

### 4.1 Symbol Instance Register

每条 `symbolic_mapping_hypothesis` 至少保存：

- world_variable；
- candidate_symbolic_role；
- symbol_type；
- symbol_value；
- plate_layer；
- palace；
- dun_mode；
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

## 6. 多输出不是唯一决策

完整复核 1080 局时反复出现一个盘同时给出多个合法吉方/候选方向的情况。这说明：

`DETERMINISTIC MULTI-OUTPUT != UNIQUE DECISION`

算法能够反馈前确定多个候选，不等于行动已经唯一。

如果当前场景存在多个合法候选输出，必须在 Outcome 之前写入 `decision_tie_break_policy`，至少明确：

- `applies`；
- candidate_outputs；
- selection_rule；
- selected_output；
- freeze_status。

当 `applies=true` 时，至少要有两个候选，且 selection_rule 与 selected_output 必须在反馈前冻结。若无法形成合法选择规则，`freeze_status = UNRESOLVED` 并考虑 ABSTAIN；不得在结果后从多个候选里挑一个命中者。

这一步冻结的是“如何从合法候选中行动”，不是把来源中的所有候选强行压成一个“唯一真答案”。

## 7. 实战错误如何记分

以下都属于模型/执行失败信号，而不是可以被解释掉的“小误差”：

- 盘层未标导致落宫读错；
- 同一天干的天/地盘实例被压成一个“唯一宫位”；
- 阴/阳遁模式未记录，导致 source-local symbol vocabulary 或状态读取被混用；
- 读取错误直到结果后才被发现；
- 结果后才决定原来应该看另一盘层；
- 多个合法候选在结果后才临时选择“命中”的一个；
- 用流派A的盘层语义解释流派B而没有显式桥接；
- 为保住原预测而修改原始读盘记录。

如果错误在 Outcome 前发现，可以更正输入并重新 Freeze；旧错误必须保留为 practice lesson。若 Outcome 已知后才发现，只能记 `post_hoc correction`，原预测不能被洗成命中。

## 8. 与 QCIC / SCRM / Prospective Gate 的关系

QCIC 控制来源、规则、程序与反馈后自由度；SCRM 控制场景、角色映射与 competing explanations；Prospective Gate 控制冻结链。

本协议补的是它们之间以前缺失的两层：

`INPUT CORRECTNESS / SYMBOL INSTANCE INTEGRITY`

以及：

`MULTI-OUTPUT DECISION FREEZE`

所以：

`VALID HASH CHAIN + WRONG PLATE READ = WRONG FROZEN CASE`

同时：

`CORRECT PLATE + POST-HOC TIE-BREAK = INVALID DECISION EVALUATION`

工程冻结不能替代盘面读取正确性，也不能替代事前决策规则。

## 9. 验证方向

该协议本身也没有经验特权。后续至少比较：

1. layer/dun-tagged mapping 与未完整标记 mapping 的读盘错误率；
2. 单次读取与独立 readback 的错误发现率；
3. layer/dun tagging 是否提高跨解读者复现性；
4. 多输出场景加入反馈前 tie-break 后，是否减少结果后选择自由度；
5. 增加这些字段后是否只增加文档复杂度而没有降低错误。

如果没有增量价值，应简化；如果仍频繁发生错误，应继续收紧输入协议，而不是增加解释口诀。

Empirical Credit 始终保持：`NONE`。
