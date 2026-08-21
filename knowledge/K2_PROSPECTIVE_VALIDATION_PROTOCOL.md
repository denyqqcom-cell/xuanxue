# K2 Prospective Validation Protocol：从解释能力进入可证伪能力

版本：2026-08-22
阶段：K2B / Deep Closure
状态：ACTIVE

## 1. 目的

本协议把 Deep Closure 的“证”从方法论要求变成可审计的工程合同。

核心原则：

`SOURCE / STRUCTURE / METHOD CREDIT != EMPIRICAL CREDIT`

古籍、案例、作者权威、跨页一致、同一传统的重复出现，都不能自动证明现实预测有效。原创模型同样没有特权：只要未经事前冻结、允许失败的前瞻测试，就保持 `empirical_credit = NONE`。

## 2. 三层分离

前瞻验证必须分成三个不可互相回写的层：

1. `TEST PLAN`：在具体案例之前定义要检验什么、与什么比较、怎样失败；
2. `FREEZE`：在结果未知时冻结该案例的对象映射、可用规则、解释路径、预测与置信度；
3. `OUTCOME`：结果出现后只登记观察值与按冻结规则得到的评分，不得修改 Freeze。

流程：

`HYPOTHESIS -> TEST PLAN -> PRE-OUTCOME FREEZE -> OUTCOME -> BATCH REVIEW -> MODEL UPDATE`

单个命中案例永远不能直接升级 Empirical Credit。

## 3. TEST PLAN 合同

公开设计文件：

`knowledge/K2_PROSPECTIVE_TEST_PLANS.jsonl`

每个计划必须绑定已经登记的 `hypothesis_id` 与 `work_family_key`，并至少预先说明：

- 候选模型是什么；
- 竞争模型 / baseline 是什么；
- 允许进入测试的问题范围；
- 分析单位；
- 案例冻结时必须保存哪些字段；
- 评价指标；
- 成功条件；
- 失败条件；
- 弃权条件；
- 如何防止反馈泄漏；
- 高风险用途如何隔离；
- 模型失败后如何更新而不改写历史。

计划本身只代表 `DESIGN_READY`，不是实证结果。

## 4. FREEZE 合同

后续真实案例使用：

`knowledge/K2_PROSPECTIVE_FREEZES.jsonl`

Freeze 必须发生在结果未知时，并至少固定：

`QUESTION DEFINITION`
→ `ASKED OBJECT`
→ `OBJECT GRAPH`
→ `ROLE MAP`
→ `ELIGIBLE RULE SET`
→ `PRIMARY LAYERS`
→ `BOUNDARY CONDITIONS`
→ `INTERPRETATION PATH`
→ `PREDICTION`
→ `CONFIDENCE`
→ `ABSTENTION CONDITION`

具体计划可要求额外字段，例如 movement 测试必须冻结：

`movement_object / temporal_context / anchor / cadence / direction / path / center_policy / school_context`

Freeze 的 payload 必须生成 canonical SHA256。Outcome 只能引用这个 hash，不能把结果出现后的新解释写回 Freeze。

## 5. OUTCOME 合同

后续结果文件：

`knowledge/K2_PROSPECTIVE_OUTCOMES.jsonl`

Outcome 只允许：

- 引用既有 Freeze；
- 记录实际结果的匿名化/结构化表示；
- 按事前规则标记 SUCCESS / PARTIAL / FAIL / ABSTAIN / UNEVALUABLE；
- 记录事后才想到的新解释，但必须显式标记为 `post_hoc`；
- 保留失败与不可判定案例。

Outcome 不得修改原 prediction、confidence、Role Map、Eligible Rule Set 或 Interpretation Path。

## 6. 禁止“冻结表演”

以下情形不算 prospective validation：

- 结果已经知道才补写 Freeze；
- 预测写得足够模糊，任何结果都能解释为命中；
- 反馈后更换用神、主观察层或规则集；
- 只保留命中案例；
- 没有失败条件；
- 没有竞争模型 / baseline；
- 单案例命中直接提升理论信用；
- 用古籍案例、网络复盘或已知答案数据冒充未知结果前瞻测试。

## 7. 高风险边界

医疗、法律、金融、战争、人身安全、重大关系决策等高风险内容只允许研究性记录，不得通过本协议升级为现实行动建议。

公开仓库不得保存真实姓名、联系方式、精确地址、账户信息等个人敏感资料。案例必须使用匿名 `case_id` 或只保存结构化派生数据。

## 8. Empirical Credit 升级规则

当前所有候选模型保持：

`empirical_credit = NONE`

未来即使已有多个 Outcome，也必须经过独立的 `BATCH REVIEW` 才能讨论升级。Batch Review 至少要检查：

- 预先承诺的 primary metric 与 threshold；
- calibration / discrimination / abstention；
- 与 baseline 的差异；
- 失败样本和不可判定比例；
- 是否存在同一案例重复计数；
- 是否发生规则漂移；
- 模型更新是否在新批次重新冻结。

在 Batch Review Gate 建立前，任何前瞻案例都不得把 `empirical_credit` 改成非 `NONE`。

## 9. 原创理论的纪律

“自建理论”不是脱离验证，而是比继承理论承担更严格的反证义务。

项目当前候选方向如 `RELATIONAL_CONFIGURATION` 与 `CONTEXTUAL_STATE_TRANSITION`，只能作为 hypothesis/model candidate。若预注册测试显示它们不优于简单 baseline、无法改善复现性，或需要持续事后补规则才能成立，就必须降级、拆分或放弃。

真正的原创性，不是拥有更多解释，而是能主动删除那些经不起冻结测试的解释自由度。
