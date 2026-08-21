# 奇门学习全链路复盘 — 2026-08-21

状态：ACTIVE / SELF-AUDIT / NO EMPIRICAL CREDIT

目的：进入深度闭关攻坚期后，不再把“继续读书、继续加规则、继续写协议”本身视为成长。回溯学习、实现、验证、解盘和研究选择的完整链路，找出会反复制造假进步的误区，并给出可执行的修正路径。

本文件不是新理论版本，不增加 `反证情境压缩法 v0.3-alpha` 的经验支持。

---

## 1. 当前真实位置

最新已通过的 exact-head 基线（写本文前）：

- head: `b67e69d02ca69782f0b7b5d3af5a6e072b62b08a`
- Knowledge Engine V1 CI #323: `completed / success`
- aggregate K2 per-book gate: `37 expected reading units / 5 COMPLETE / 32 NOT_STARTED`
- aggregate evidence: `718 reviewed Evidence rows`
- Prospective Registry: `0` clean scored rows

因此必须同时承认两件事：

1. 知识工程已经明显比早期严谨；
2. 文献全覆盖和现实预测验证都远没有完成。

`Engineering maturity != Corpus mastery != Predictive validity`。

---

## 2. 历史误区一：把“来源明确”误当“规律有效”

早期常见链：

`书里写了 -> 多本书也写 -> 规则可信 -> 解盘直接使用`

问题：

- 多书可能共享同一祖本或教学谱系；
- 作者案例通常是 retrospective selection；
- 书内没有 baseline、连续失败记录和 unknown-outcome freeze；
- 古籍/讲义内部也会自相矛盾、讹误、编辑拼接。

已经发生的具体教训：

- 梁湘润序言自己就提醒历代文献存在讹错、校错和后人增补；
- 八神在不同来源出现 `勾陈/朱雀`、`白虎/玄武`、hidden-layer、yin-yang substitution 与 `朱/白` 双位置等不同结构；
- 九星旺相休囚即使两个现代载体一致，也只能先记 `Source Convergence / Possible Shared Lineage`。

修正：

`SOURCE -> LINEAGE -> APPLICABILITY -> IMPLEMENTATION -> EMPIRICAL TEST`

任何一步都不能由前一步自动继承 credit。

---

## 3. 历史误区二：一次成败就长出全局规则

旧学习记录曾从少量案例迅速推出：

- 固定 `开门 > 值符 > 生门 > 星神`；
- `逢空 = 方向待定`；
- `凶格>=3分` 等固定分值；
- 旺相全额、休囚减半；
- 单次失败后直接归因某一门、某一层级或所谓“系统天花板”。

这类学习看似敏捷，实际是：

`Outcome -> immediate patch -> global rule`

它会让模型越来越能解释旧案例，却越来越难被未来数据击穿。

修正：

`Outcome -> CASE_LESSON_CANDIDATE -> falsifiable hypothesis -> matched prospective test -> lifecycle update`

单案例永远没有直接升级 ACTIVE global rule 的资格。

---

## 4. 历史误区三：把“情境化”从反模板走向另一种自由发挥

最早为了反对背书式解盘，曾形成：

`书本给符号，情境给答案`

这个表达已废弃。

它的问题是：现实背景越丰富，分析者越容易从宽象意中选择最贴近现实的解释，形成 context leakage 与 narrative rescue。

当前改为：

`书给候选 -> 情境限定角色/对象/语义边界 -> 关系形成可失败判断 -> 现实结果事后评分`

新的核心判据：

> **情境越具体，合法解释空间应当越窄。**

若加入更多背景后：

- eligible meaning 增多；
- competing branches 增多；
- 原本会失败的结论反而更容易被救回；

则标：

`CONTEXT_EXPANSION / NARRATIVE_RESCUE_RISK`

这不是“更会活断”，而是模型自由度增加。

---

## 5. 历史误区四：会写正确规则，不等于会正确执行

项目已经出现多次：

`Written Knowledge != Executable Knowledge`

典型复发：

- 文档已经要求区分宫号序与几何旋转序，production 仍把 `1..9` 飞布数序当成外八宫转盘序；
- `甲时` 语言对象与盘内旬首遁干 representation 混淆，触发 `HIDDEN_JIA_REPRESENTATION_ERROR`；
- App 曾经没有显式暴露 MethodProfile，研究层要求 Method Freeze，但 shipped execution 仍静默选择默认实现。

修正形成三类 Type Safety：

1. `Sequence-Object Type Safety`
2. `Representation-Object Type Safety`
3. `Semantic-Object Type Safety`

统一原则：

> **词相同、数字相同、方向相同，都不能证明操作对象相同。**

任何“顺/逆/飞/转/移”、任何“甲/旬首/遁干”、任何“白虎/朱雀/天乙”等 token，进入算法前必须先说明对象类型。

---

## 6. 历史误区五：验证器与实现一起错，CI 仍然会绿

曾发生：fixture、expected mapping 与 validator 共用同一错误理解，因此自洽地全部 PASS。

所以：

`Validator PASS != Oracle Correctness`

修正：

- source witness 尽量与 implementation 独立；
- expected/oracle 不从 system under test 自动导出；
- 加 wrong-bureau / wrong-hour / permuted / shuffled controls；
- 错误输入必须真正输；
- selected cross-source implementation agreement 与 Empirical Support 分开记账。

最新 source-profile tests 能拒绝部分 wrong input，这是 implementation fidelity 的进步，不是预测有效性证明。

---

## 7. 历史误区六：研究者的自由度被低估

过去主要冻结单次模型里的自由度：

`MODEL_DOF`

但研究者还可以通过以下方式自我欺骗：

- 只挑支持当前算法的书和 worked plate；
- 失败时换研究题；
- 赢了就停止，输了就继续找样本；
- 只记录 PASS，不记录 NO-OP / UNRESOLVED。

因此新增观察：

`SELECTION_DOF`

与：

`STOPPING_DOF`

`RESEARCH_ATTACK_QUEUE.md` 目前只是轻量实验。它若不能实际减少 cherry-picking，就删除，不再变成新官僚层。

---

## 8. 历史误区七：把“文献全覆盖”误解为“越快读越多”

当前 K2 gate 的真实状态是：

`37 expected reading units -> 5 COMPLETE -> 32 NOT_STARTED`

因此“库中文献须尽数研习”应该解释为**长期可审计目标**，而不是口头宣布“已经掌握”。

新的全覆盖含义：

- 每一个 expected reading unit 最终必须有诚实的 `COMPLETE / PARTIAL / BLOCKED`；
- 每本 source 的 provenance、method objects、冲突、适用域、风险断语和 test hooks 都要留下结构化记录；
- 同一内容重复出现不重复计算独立支持；
- OCR/targeted review 不能冒充 full reading；
- “已经看过”若违反 Pre-Book gate，不追认流程 credit；
- 完成阅读不等于采纳规则。

详细执行见：`奇门/K2_FULL_COVERAGE_MASTER_PLAN.md`。

---

## 9. 历史误区八：过度书本化的真正根因不是“读书太多”

真正问题不是读书，而是推理链过短：

`符号 -> 书中断语 -> 结论`

这会导致两个问题：

1. 同一星门神在不同问题中被机械复制；
2. 用户具体约束、行动空间、时间窗口和角色关系没有进入模型。

因此场景化不能只做“加一段现实背景”。它必须改变**关系模型**，但不能结果后改变规则。

新的推演最小对象：

`QUESTION -> ACTORS -> TARGET -> HORIZON -> ACTION SPACE -> CONSTRAINTS -> ROLE MAP -> STRUCTURAL FEATURES -> RELATIONS -> PRIMARY BRANCH -> FAILURE CONDITION`

其中：

- `ACTORS/TARGET/HORIZON/ACTION SPACE/CONSTRAINTS` 来自现实问题；
- `ROLE MAP` 必须说明 source/method/context basis；
- `STRUCTURAL FEATURES` 来自盘；
- `RELATIONS` 才是情境化的核心；
- `PRIMARY BRANCH/FAILURE CONDITION` 保证不是事后故事。

详细规范见：`奇门/CONTEXT_REASONING_PROTOCOL.md`。

---

## 10. “理论 - 验证 - 落地”闭环

以后每条理论主张必须经过三种不同 Gate。

### T — THEORY

必须回答：

- 具体 claim 是什么？
- claimed applicability 是什么？
- 哪个来源/推断产生它？
- 什么结果会反驳？
- simpler rival model 是什么？

只满足 T，最多为 `CANDIDATE / TESTABLE`。

### V — VALIDATION

至少区分：

- source fidelity test；
- implementation fidelity test；
- negative control；
- clean prospective outcome test；
- baseline / shuffled / ablation comparison。

`SOURCE PASS` 不能代替 `PROSPECTIVE PASS`。

### L — LANDING

若要进入 runtime / App / 解盘流程：

- profile/variant 必须显式；
- unresolved 必须 fail closed；
- source-specific rule 不得冒充 global default；
- UI/Interpreter 不能隐藏方法选择；
- implementation contract 要覆盖真正 shipped path；
- 若没有足够 Empirical Support，产品文案必须保留 evidence boundary。

因此：

`THEORY READY != VALIDATION READY != SHIPPED READY`

以及：

`SHIPPED != VALIDATED`。

---

## 11. 当前针对性优化路径

### P0 — 先建立可失败的解盘，而不是继续加象意

- 真正启动 clean unknown-outcome prospective pilot；
- 先检验 frozen contextual reasoning 是否比 simpler source-restricted baseline 有增量；
- 对 broad-context / shuffled-role-map 做反证；
- 没有真实 unknown-outcome，不伪造 prospectives。

### P1 — 完成文献全覆盖，但按问题驱动轮换

- 按 `K2_FULL_COVERAGE_MASTER_PLAN` 推进剩余 32 reading units；
- 不连续读同一 lineage 形成回音室；
- 每本必须产生 conflict/test/compression 之一，否则只算摘录。

### P2 — 继续攻击实现边界

- 中五值使 full-door witness；
- 真实 23:00/00:00 boundary worked plate；
- 更多反例型 full-rotation witness；
- star/door state system 的独立来源与 ablation。

### P3 — 每轮必须允许做减法

至少问一次：

- 哪个 rule 可以删？
- 哪个 branch 可以合并？
- 哪个 context key 没有增量？
- 哪个 Gate 只是 paperwork？

没有删掉任何东西不是失败，但长期只增不减就是警报。

---

## 12. 原创方法论当前真正长出来的部分

目前最像“自己的东西”的，不是新断诀，而是四个约束族：

1. **Object Type Safety**：先识别操作/语义对象，再谈规则；
2. **Degrees-of-Freedom Control**：冻结模型、选择与停止自由；
3. **Context Compression**：情境越具体，解释空间应越窄；
4. **Falsification + Compression**：能输、能删、能退级。

它们目前仍只是 `v0.3-alpha` 的研究骨架。

如果未来 clean prospective data 证明它们没有比更简单模型提高 discrimination / calibration / reproducibility，则应该被缩窄甚至放弃。

这才是“自成一家”必须接受的代价：

> **自己的理论，也没有免于被自己推翻的特权。**
