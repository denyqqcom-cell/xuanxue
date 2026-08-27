# K2 奇门情境差分消融框架 v0.1

English: Contextual Differential Ablation Framework  
简称：CDAF  
状态：`CANDIDATE_UNTESTED / DESIGN_ONLY`  
Empirical Credit：`NONE`  
Claim Extraction：`BLOCKED`

## 0. 为什么不是继续升级《情境推演法》

《情境推演法 v0.1》把“定事定位、能量状态、取用神、情境转译、加权裁决”整合成一个五层框架。它确实比逐条背书更重视具体情境，但存在一个根本的归因问题：

> 即使整体表现变好，也不知道改善究竟来自更认真地定义现实问题、来自奇门符号、来自关系推演，还是仅仅来自更完整的叙事和更多信息。

如果这些作用不拆开，未来任何成功都可能被整体框架吸收，任何失败也可能由另一层解释。这会让“情境推演法”变成一个难以证伪的组合包。

CDAF 因此不再问“情境推演法好不好”，而问：

`每增加一个组件，相比更简单的前一层，到底增加了什么可重复、可区分的价值？`

本文件不是新的奇门规则库，也不建立新的经验信用。它只把已有框架拆成可以被删除的候选组件。

## 1. 对《情境推演法 v0.1》的组件审计

### C-01 定事定位 / 问题定义

旧功能：先明确所问事项，再进入盘面。

当前判断：`RETAIN_AS_GENERIC_BASELINE`

原因：这是普通问题建模能力，不属于奇门独有贡献。明确对象、时间窗和结果定义本身就可能显著提高回答质量。

纪律：未来如果加入这一步后表现改善，改善首先记入 `context/problem-definition credit`，不得自动记给奇门。

### C-02 能量状态前置

旧功能：旺相休囚死、空亡、入墓、击刑、门迫先于象意判断，并出现“休囚减半、四害加重”等规则。

当前拆分：

- 旺衰、空墓刑迫等传统判断：`SOURCE/METHOD CANDIDATE`；
- “减半”“加重”“叠加”等数值或固定强度：`DISABLED_UNTIL_CALIBRATED`。

传统存在只能获得 source/method credit。任何数值权重必须经过独立 ablation，不能因听起来符合五行逻辑而保留。

### C-03 四分法前置分类 / 取用神路由

旧功能：静态、动态、九宫拟象、综合先分类，再决定取神方向。

当前判断：`ROUTING_CANDIDATE`

它可能减少“回答错问题”和结果后换用神，但“分类错误就全错”仍只是来源/方法主张。

测试重点不是求测者觉得是否贴合，而是：冻结分类后，是否降低 role-map drift、结果后重映射率和不可复现率。

### C-04 📖 / 🧠 分离标注

旧功能：区分书本断语与个人情境推演。

当前判断：`RETAIN_AS_PROVENANCE_TOOL_ONLY`

应保留“谁说的/从哪里来的”这一审计价值，但废止两个旧假设：

- `📖 = 高现实可信度`；
- `📖与🧠冲突时默认🧠胜出`。

来源标注不能参与现实正确性的加权。

### C-05 情境转译三问

旧功能：问事体、问正反面、问能量，再把符号转成现实含义。

当前判断：`MERGE_INTO_MAPPING_HYPOTHESIS`

三问本身可以帮助暴露映射前提，但“哪个正/负象意最贴合当前情境”仍有选择性解释风险。

因此不再把三问当作真值裁决器，而改写为：

`现实变量 -> 候选符号映射 -> 来源/理由 -> 竞争映射 -> 失败条件`

这与 SCRM 的 Symbolic Mapping Hypothesis 合并，不再作为独立理论层重复存在。

### C-06 多层推演链

旧功能：要求“象意 -> 情境映射 -> 行动含义”至少推两层。

当前判断：`EXPLANATION_TRACE_ONLY`

完整推理链有助于审计跳步，但层数更多不代表正确率更高。它属于可读性、可追踪性和错误定位能力，不能获得预测信用。

### C-07 加权裁决

旧功能：固定符号优先级、凶格计分、星级主导信号、叠加相乘等。

当前判断：`DECOMPOSE_OR_REMOVE`

尤其以下部分当前停止 promotion authority：

- `开门 > 值符 > 生门 > 星神` 一类固定全局优先级；
- `>=3分断大凶`；
- `⭐⭐⭐` 等未经校准的权重；
- 结果后形成的政策/新闻优先级。

若某个子组件值得研究，必须单独进入未来 batch；不能把整个加权包一起测试后再声称其中每条都有效。

### C-08 马星、逢空、主客等具体规则

当前判断：`SEPARATE_RULE_OPERATORS`

它们不能因为被收编进同一个框架就共享证据。每条规则继续服从来源、method layer、role frame、边界和 prospective validation。

框架成功不能替单条规则背书；单条规则成功也不能替框架背书。

### C-09 不确定性高/中/低与 0-1 confidence

当前判断：`QUALITATIVE_ONLY_UNTIL_CALIBRATED`

可以保留“不确定/敏感/需弃权”等结构化描述，但未经校准不得把主观分值解释为概率，也不得用主观高/中/低制造经验信用。

### C-10 “不推翻任何东西，只做整合”

当前判断：`REJECTED_AS_PROMOTION_POLICY`

渐进迭代不等于旧组件永久保留。任何组件都必须允许：

`retain -> constrain -> test -> downgrade -> merge -> remove`

### C-11 “>=3次成功即可升级”

当前判断：`SUPERSEDED`

固定小样本成功数不再是升级标准。继续服从 K2 Prospective Validation 的 Plan -> Batch -> Freeze -> Outcome -> Review 链。

## 2. CDAF 的最小嵌套模型

为了真正知道提升来自哪里，后续不直接比较“背书式 vs 完整 SCRM”，而使用嵌套模型。

### M0：Reality-only Baseline

只使用：

- 明确的问题与 outcome definition；
- 已知现实事实；
- 可获得的 base rate；
- 时间窗、参与者、资源、制度和流程状态。

禁止使用任何奇门符号。

目的：建立最低限度的现实基准。

### M1：Context-Structured Baseline

`M0 + Scenario State Graph + Question Decomposition`

仍然禁止奇门符号。

目的：测量“只是把问题想清楚、把现实关系画清楚”本身能带来多少提升。

若 M1 明显优于 M0，这属于通用场景建模贡献，不属于奇门贡献。

### M2：Frozen Symbolic Mapping

`M1 + 反馈前冻结的奇门角色映射 + 最小合格规则集`

限制：

- 不允许结果后换用神；
- 不允许叙事层自由补充；
- 不使用未经校准的固定权重；
- 输出必须落到明确 state variable / observable outcome。

目的：测量奇门符号层相对于已充分建模现实情境的**增量信息**。

### M3：Relational Qimen

`M2 + SCRM relational inference`

加入：

- 角色之间的盘面关系；
- micro/macro relation；
- competing symbolic mappings；
- 明确的 relational path。

但仍不允许以“故事更顺”为 tie-break。

目的：测量关系推演是否比简单冻结符号映射提供额外价值。

### M4：Narrative Expression

`M3 + narrative explanation layer`

叙事层只能改善：

- 可理解性；
- 决策信息组织；
- 推理链可读性；
- 假设与边界呈现。

它不得改写 M3 已冻结的 prediction、role map、rule path 或 outcome score。

目的：把“会不会判断”和“会不会解释”彻底分开。

## 3. 五个候选差分假设

### CDAF-H1：问题建模增量

`M1 > M0`

如果成立，只证明 Scenario Graph / Question Decomposition 有通用建模价值，不证明奇门有效。

### CDAF-H2：符号增量

`M2 > M1`

只有这个差分及其后续复制，才可能开始讨论“冻结后的奇门符号层是否在现实 baseline 之外提供信息”。

当前状态：`UNTESTED / DESIGN_READY / EMPIRICAL_CREDIT_NONE`

正式 provenance：

- `origin_type = PROJECT_GENERATED`
- `origin_key = CDAF-v0.1`
- identity registry：`knowledge/K2_QIMEN_PROJECT_HYPOTHESES.jsonl`
- prospective plan：`K2PV-CDAF-H2`
- comparator：`CONTEXT_STRUCTURED_BASELINE (M1)`
- candidate：`FROZEN_SYMBOLIC_MAPPING (M2)`

这里的 `DESIGN_READY` 只表示：CDAF-H2 已经能够以**项目自生假设**而不是伪造 work-family 来源的方式，合法进入既有 Prospective Validation 链。它不表示实验已经开始，更不表示它被验证。

截至本版本：

`BATCH = 0`

`FREEZE = 0`

`OUTCOME = 0`

因此 CDAF-H2 的 Empirical Credit 仍严格为 `NONE`。

### CDAF-H3：关系增量

`M3 > M2`

如果 M2 已经足够，而 M3 没有改善或增加漂移，则 relational layer 应简化或删除，而不是继续扩张关系网。

当前状态：`UNTESTED / EMPIRICAL_CREDIT_NONE`

当前正式对应的 source-derived 设计为 `H-JD-001 / K2PV-JD-001`。它已经收紧为共享同一现实情境、同一冻结符号映射与同一 eligible rule pool，只允许 candidate 相对 comparator 增加 relational inference path。因此它测试的是 `M3 - M2`，而不是“复杂情境模型 vs 查表”的混合差分。

### CDAF-H4：叙事只属于表达层

预测层固定后，M4 可以提高人类理解度，但不应改变 outcome-scoring performance。

如果加入叙事后预测结果本身发生变化，说明叙事层正在越权参与模型选择，必须重新限制。

当前状态：`UNTESTED`

### CDAF-H5：敏感性与弃权质量

Sensitivity / ABSTAIN 的价值不是让命中率看起来更高，而是识别脆弱案例、降低高置信错误和结果后重映射。

若加入这些控制后只是大量回避难题，却没有改善预注册 selective-risk / calibration 指标，则应简化。

当前状态：`UNTESTED`

## 4. 结果归因规则

未来出现性能差异时，必须按差分归因：

```text
M1 - M0 = 通用情境建模增量
M2 - M1 = 冻结奇门符号增量
M3 - M2 = 奇门关系推演增量
M4 - M3 = 表达/可理解性增量
```

禁止：

`M4整体表现较好 -> 奇门/SCRM/情境推演法整体都有效`

也禁止：

`某一层失败 -> 整个奇门体系已经被证明无效`

每个差分只对被改变的组件负责。

## 5. 未来 Batch 的最低设计要求

CDAF 不自己建立第二套 prospective schema，直接复用现有 K2 Prospective Validation Protocol。

正式测试至少必须做到：

- 同一批案例、同一 outcome definition；
- M0-M3 输入截止时间一致；
- M2/M3 的 role map 与 eligible rules 在结果前冻结；
- 不同模型不得看到彼此的结果后解释；
- primary metric、stopping rule、exclusion rule 在 Batch 前冻结；
- 所有失败、ABSTAIN、UNEVALUABLE 保留；
- 比较 post-hoc edit rate、role-map drift、reproducibility、selective risk；
- 若使用概率/分数，必须先有校准定义，否则保持类别输出。

具体 primary metric 不在本文件中预设，因为不同 question scope 的 outcome 结构不同。必须在每个 Batch preregistration 中按目标定义，不能由本框架使用一个万能分数。

尤其，**Design Plan 已存在并不自动授权创建 Batch**。在建立 `K2PV-CDAF-H2` 的第一批正式数据前，还必须明确：

- 一个外生、低风险、可客观观察的 target domain；
- outcome normalization；
- observation cutoff；
- sampling frame；
- base-rate / context baseline；
- primary metric 与 decision rule；
- exclusion rule；
- stopping / sample-adequacy rule；
- candidate 与 comparator 的信息隔离方式。

这些条件没有冻结之前，不为“赶进度”生成 Batch。

## 6. 消融决策树

### 情况 A：M1 明显优于 M0，但 M2/M3 不优于 M1

结论：改善主要来自现实场景建模。

处理：保留 Scenario Graph 作为通用推理工具；奇门符号/关系层不获得增量 empirical credit。

### 情况 B：M2 优于 M1，但 M3 不优于 M2

结论：若结果可复制，简单冻结符号层可能有增量，而复杂关系层没有证明必要。

处理：简化 SCRM，删除或降级无增益 relational complexity。

### 情况 C：M3 稳定优于 M2

结论：关系结构成为值得继续研究的候选核心。

处理：进入新的独立 Batch；仍不得由一次 Batch 直接推广到全部题型。

### 情况 D：只有 M4 被评价更好

结论：我们更会解释了，不等于更会预测。

处理：把叙事层固定为 communication layer，不给 prediction credit。

### 情况 E：所有模型都接近现实 baseline

结论：当前数据不支持复杂层级带来稳定增量。

处理：优先简化，而不是继续加规则找优势。

## 7. 与 SCRM 的关系

CDAF 不替代 SCRM。

SCRM 提供完整候选场景模型；CDAF 提供拆解它的方法。

可以理解为：

`SCRM = candidate full model`

`CDAF = component attribution / deletion discipline`

特别重要的是，SCRM 当前的五个 0-1 confidence research score 不进入 CDAF 的经验比较，除非未来先完成校准。它们可作为研究字段，但不能用来证明 M3 比 M2 更强。

## 8. 与 Epistemic Debt 的关系

CDAF 直接响应当前认知债：

- QED-002：自生成推演无认知特权；
- QED-004：未经校准权重不得进入模型；
- QED-006：传统/旧框架必须允许退出；
- QED-008：未经校准分数不是 validation credit；
- QED-010：叙事连贯性不是现实正确性；
- QED-011：不为本框架另造一套 schema/gate，先证明组件差分是否值得正式化。

新增的 project-generated hypothesis registry 只解决**身份与 provenance 缺口**。它复用原有 Prospective Validation 的 Plan -> Batch -> Freeze -> Outcome hash-bound 链，不是第二套经验验证系统。因此它不因“新增了一个登记表”获得任何结构之外的信用。

## 9. 当前处理结论

《情境推演法 v0.1》不删除，因为它是认知演化的重要历史记录；但它不再作为一个不可拆分的整体候选理论参与未来验证。

从本文件开始，未来只验证**可隔离的组件增量**，不验证“整套理论感觉更好”。

当前正式进入 Design Plan 的差分有两个：

- `CDAF-H2 / K2PV-CDAF-H2`：项目自生，测试 `M2 - M1`；
- `H-JD-001 / K2PV-JD-001`：来源派生，测试 `M3 - M2`。

二者目前都没有 Batch/Freeze/Outcome，均不得声称已测试或已验证。

当前没有任何一个 CDAF 差分获得 empirical credit。

Empirical Credit: `NONE`
