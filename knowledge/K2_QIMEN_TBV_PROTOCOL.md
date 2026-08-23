# K2 奇门 TBV 反向重析协议 v1

TBV = Theory — Boundary — Validation（理论—边界—验证）。

状态：`ACTIVE / PARTIAL`  
阶段：K2B Cognitive Reconstruction  
Claim Extraction：`BLOCKED`  
Empirical Credit：`NONE`

## 1. 目的

本协议用于第二遍反向阅读已经完成 Deep Visual Review 的奇门材料。

第一遍完整阅读主要解决：

`来源到底写了什么 -> 作品/作者/章节/方法结构是什么 -> 哪些材料应保留或隔离`

TBV 第二遍不再追求“记住更多口诀”，而是把已有理解重新拆成三个互相不能偷换的层：

`THEORY -> BOUNDARY -> VALIDATION`

只有三层都被显式记录，某个来源局部方法才有资格进入后续 SCRM 的候选 operator；即使如此也不获得现实有效性信用。

## 2. THEORY：理论核心

TBV 不把“规则列表”本身等同理论。

应尽量提炼来源真正依赖的推演结构，例如：

- 静态符号词典；
- 关系配置；
- 主客/角色模型；
- 时间状态转移；
- 程序优先级；
- 多观察通道；
- 生成规则与查表；
- 作者自己的方法批判。

若一个来源同时包含多个 method layer，必须分别表示，不能因为共处一本书就合并为单一理论。

## 3. BOUNDARY：适用边界

每一条理论核心都至少反查：

- 它回答什么问题域；
- 使用哪个 method layer；
- role frame 是什么；
- 使用什么时间模型；
- 属于哪个 source/school context；
- 使用前必须满足什么前置条件；
- 什么情形禁止调用；
- 边界是 EXPLICIT、PARTIAL 还是 UNCLEAR。

规则若缺少边界，不允许补成“奇门通用真理”。

因此统一执行：

`SOURCE CONTAINS RULE != RULE IS UNIVERSAL`

`SOURCE ENDORSES RULE != RULE IS EMPIRICALLY VALID`

## 4. VALIDATION：信用分层

每条 TBV review 都分别记录：

- `source_credit`：是否已经完整视觉核验来源；
- `structure_credit`：内部结构能否稳定重建；
- `method_credit`：能否明确还原来源怎样使用；
- `empirical_credit`：现实未知结果下是否经过前瞻验证。

本阶段所有条目：

`empirical_credit = NONE`

古籍年代、作者名气、案例数量、表项数量、来源自我批判、现代作者强调实践，都不能越级为 empirical credit。

## 5. Universalization Gate

所有 TBV review 的：

`universalization_status = BLOCKED`

只有 source-local/context-local candidate 可以进入后续建模。

跨来源出现相似规则时，先检查：

1. 是否同 work family / 同传承导致的伪独立；
2. 术语是否同名异义；
3. role frame 是否一致；
4. temporal model 是否一致；
5. method layer 是否一致；
6. 前置条件是否一致。

在 Claim Extraction 与冲突解析正式开放前，不建立“多数书都这么说所以是真的”的规则。

## 6. 与 SCRM 的关系

TBV 是 SCRM 的上游知识过滤器。

流程：

`SOURCE -> Deep Reading -> TBV -> QCIC eligibility -> SCRM scenario mapping/operator -> prospective validation`

TBV 允许输出：

- source-local candidate；
- boundary-only principle；
- mixed-stance hold；
- historical-only；
- hold。

TBV 不允许输出：

- 已验证现实规律；
- 无边界的万能口诀；
- 高风险现实操作建议；
- 因来源数量多而自动成立的共识真理。

## 7. 当前 Wave A

首轮 TBV 反向重析只使用已经存在完整视觉阅读和正式 distillate 的材料，不冒充全库覆盖：

- QM-SRC-0015；
- QM-SRC-0017；
- QM-SRC-0019；
- QM-SRC-0020；
- QM-SRC-0021；
- WF-QM-JIADUN-ZHENSHOU-001。

机器账本仍有 16 个奇门 deep visual reviewed source，而 TBV 当前只覆盖 5 个 standalone deep-source unit + 1 个 work-family unit，因此：

`full_reviewed_material_tbv_coverage = false`

同时全项目仍有：

`global_unknown_textual_backlog = 93`

故不得宣称全知识库已经完成掌握。

## 8. 当前认知结果

Wave A 已经足以确认一个重要方向：

传统材料中真正可被工程化保留的内容，往往不是“某符号固定等于某结果”，而是：

`对象定义 + 问题域 + 角色坐标 + 时间模型 + 方法层 + 条件关系 + 程序顺序 + 现实边界`

这与 SCRM 的 scenario-conditioned relational 路线相容，但“相容”只代表方法结构能够衔接，并不代表 SCRM 已经被证实。

## 9. 失败条件

TBV 本身也允许失败。

如果后续第二遍阅读发现：

- 当前提炼遗漏来源关键前提；
- 关系模型只是项目自己的现代重写而非来源支持；
- 所谓 context split 实际是不可调和矛盾；
- 某静态规则在来源内确实被明确写成无条件规则；
- SCRM 为了吸收来源而不断增加例外和字段，却没有提高复现性；

则必须修改/降级 TBV 条目和 SCRM，而不能修改来源以适配模型。

## 10. 下一阶段

下一步分两路并行：

A. 对剩余已经完成视觉深读的奇门 source/work family 继续做 TBV Wave B；

B. 对尚未解决的 semantic UNKNOWN corpus 继续真实 content review，禁止按文件名、目录或猜测批量清零。

只有当覆盖、边界与验证路径同时推进，‘认知重构’才不是另一种形式的书本整理。

## 11. Known-outcome training 与评价隔离

TBV 新增一个明确的验证边界：

`KNOWN_OUTCOME_TRAINING != PROSPECTIVE_EVALUATION`

来源若建议使用“自己假设的事情”、已经知道结果的历史事件、事后反馈案例或其他 target-known 材料反复推演，这些材料可以用于：

- 熟悉 source-local 算法；
- 训练状态重建；
- 检查是否能复述来源的方法路径；
- 发现规则冲突与表示错误。

但它们只能取得 `TRAINING / METHOD RECONSTRUCTION` 信用，不能进入同一模型版本的 prospective accuracy、calibration 或 empirical-credit 评价。

因此后续验证必须：

1. 给 known-outcome / retrospective / invented-event 练习显式标记 `TRAINING_ONLY`；
2. 评价批次使用结果未知、反馈前冻结的 clean holdout；
3. 已用于训练/复盘的案例不得再次作为盲测样本；
4. 对语义近重复、同一事件改写、同源案例复制建立 contamination 检查；
5. 一旦发现 training/evaluation leakage，该批结果降为方法研究材料，不得升级 empirical credit。

这一控制首先来自《三元奇门遁甲讲义》上册 p5 对假设事件与已知事件反复推演的 source-local 训练建议。它不是对来源学习方法的否定，而是严格区分“练熟一个解释体系”与“在未知结果条件下证明它能预测”。
