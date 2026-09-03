# K2 Prospective Validation Protocol：从解释能力进入可证伪能力

版本：2026-09-04
阶段：K2B / Deep Closure
状态：ACTIVE_CONTRACT

## 1. 目的

本协议把 Deep Closure 的“证”从方法论要求变成可审计的工程合同。

核心原则：

`SOURCE / STRUCTURE / METHOD CREDIT != EMPIRICAL CREDIT`

古籍、案例、作者权威、跨页一致、同一传统的重复出现，都不能自动证明现实预测有效。原创模型同样没有特权：只要未经事前冻结、允许失败的前瞻测试，就保持 `empirical_credit = NONE`。

## 2. 四层分离

首次设计 prospective gate 时，项目立即暴露出一个新的自由度：即使单案例已经事前 Freeze，如果“primary metric / threshold / stopping rule”仍可等看完一批结果后再决定，依然会形成批次层的 hindsight freedom。

因此前瞻验证必须分成四个不可互相回写的层：

1. `TEST PLAN`：定义要检验什么、与什么比较、原则上怎样失败；
2. `BATCH PREREGISTRATION`：在该批任何 Outcome 出现前，冻结样本规则、样本量/停止规则、primary metric、scoring rule、decision rule、排除规则；
3. `CASE FREEZE`：在单案例结果未知时冻结对象映射、可用规则、解释路径、预测与置信度；
4. `OUTCOME`：结果出现后只登记观察值与按冻结规则得到的评分，不得修改 Batch 或 Freeze。

流程：

`HYPOTHESIS -> TEST PLAN -> BATCH PREREGISTRATION -> PRE-OUTCOME CASE FREEZE -> OUTCOME -> BATCH REVIEW -> MODEL UPDATE`

仅靠 ID 引用不足以防止合同被悄悄改写。Plan 必须同时绑定 hypothesis 内容本身和会影响该 hypothesis 实验解释范围的受治理上下文：

`HYPOTHESIS --hypothesis_sha256--> PLAN`

`HYPOTHESIS_GOVERNED_CONTEXT --hypothesis_context_sha256--> PLAN --plan_sha256--> BATCH --batch_sha256--> FREEZE --freeze_record_sha256--> OUTCOME`

同时 Outcome 继续引用 `frozen_payload_sha256`。任一上游合同发生变化，当前下游记录必须失配并触发 Gate；历史若确需修改，只能留下新的 Git 历史与新的测试版本，不能把旧结果伪装成原先就采用了新规则。

单个命中案例永远不能直接升级 Empirical Credit。

## 3. TEST PLAN 合同

公开设计文件：

`knowledge/K2_PROSPECTIVE_TEST_PLANS.jsonl`

每个计划必须绑定已经登记的 `hypothesis_id`、`work_family_key`、该 hypothesis 完整对象的 canonical `hypothesis_sha256`，以及受治理 hypothesis context 的 `hypothesis_context_sha256`。Hypothesis registry 的有效输入是完整的逻辑 Work-Family Distillate 集合：

- `knowledge/K2_WORK_FAMILY_DISTILLATES.jsonl`
- `knowledge/K2_WORK_FAMILY_DISTILLATES.d/*.jsonl`

不得只读取主文件而忽略 shards；否则 shard 中已经 REVIEWED 的 hypothesis 会在实验入口静默消失，形成“上游存在、下游不可见”的 provenance 漂移。

Hypothesis 的 ID、内容与上下文绑定必须分开：

`HYPOTHESIS_ID != HYPOTHESIS_CONTENT_BINDING`

`HYPOTHESIS_CONTENT_BINDING != HYPOTHESIS_GOVERNED_CONTEXT_BINDING`

`hypothesis_sha256` 对 `testable_hypotheses` 中当前完整 hypothesis object 做 canonical JSON SHA256。只要 `statement`、`freeze_requirements`、`failure_condition`、`status` 或该对象其他受治理字段发生变化，即使 `hypothesis_id` 没变，既有 Plan 也必须失配。

`hypothesis_context_sha256` 则对一个刻意收窄的 canonical envelope 做 SHA256：

`{ hypothesis, work_family_key, effective_domain_routes }`

这里的 `effective_domain_routes` 是 Work-Family Distillate 明示的 `domain_routes`；若未明示，则退回单一 `domain`。因此 route 新增、删除、替换或重排都会使旧 Plan 失配。这样可以阻止在 Plan 已设计后扩大可用 route scope，再让后续案例挑选新增 route。

该 context hash **不**包含与当前前瞻解释范围无关的整份 distillate 文案、摘要或其他注释字段，避免无关编辑导致实验合同被不必要地整体作废。

要采用修订后的 hypothesis 或修订后的 governed route context，必须重新形成设计链，不能让旧 Plan/Batch/Freeze 被解释成“当时本来就是这个版本”。

每个计划至少预先说明：

- 候选模型是什么；
- 竞争模型 / baseline 是什么；
- 允许进入测试的问题范围；
- 分析单位；
- 案例冻结时必须保存哪些字段；
- 候选评价指标；
- 原则上的成功与失败条件；
- 弃权条件；
- 如何防止反馈泄漏；
- 高风险用途如何隔离；
- 模型失败后如何更新而不改写历史。

若 hypothesis 所属 Work-Family Distillate 的 governed `domain_routes` 多于一个，Plan 的 `freeze_required_fields` 还必须包含：

`active_domain_routes`

这不是要求每个案例同时使用所有 route，而是要求**在 outcome 未知时明确冻结本案例实际启用的 route set**。

计划本身只代表 `DESIGN_READY`，不是一个已经开始的数据批次，也不是实证结果。`hypothesis_sha256` 与 `hypothesis_context_sha256` 只证明 Plan 所指的是哪一个精确假设版本及其受治理 route context，不证明该假设真实。

## 4. BATCH PREREGISTRATION 合同

后续真实批次使用：

`knowledge/K2_PROSPECTIVE_BATCHES.jsonl`

Batch 必须在该批第一条 Outcome 之前冻结，并至少写明：

- `plan_id` 及该 Plan 的 canonical `plan_sha256`；
- model / comparator 版本引用；
- sampling rule；
- 正整数 `planned_case_count`；
- 机器键 `primary_metric`；
- 机器可重算 `primary_metric_spec`；
- 机器可执行 `decision_rule`；
- secondary metrics；
- stopping rule；
- exclusion rule；
- duplicate-case policy；
- batch status=`PREREGISTERED`；
- `empirical_credit=NONE`。

### Fixed-N contract

当前合同只允许**固定样本量**的 batch。原因不是宣称固定 N 永远优于序贯/自适应设计，而是目前仓库尚未建立机器可审计的 sequential/adaptive stopping schema。自由文本 `stopping_rule` 可以说明为什么在 N 时停止、如何处理外部中止，但不能替代机器可读的 `planned_case_count`。

因此：

`UNSTRUCTURED_STOPPING_RULE != PREREGISTERED_SAMPLE_SIZE`

在专门的 sequential/adaptive stopping contract 建立并通过 fail-closed gate 之前，`planned_case_count=null`、结果驱动提前停止、看到部分 Outcome 后才决定继续收样，都不具备 prospective batch 资格。

固定 N 还必须是**执行上限**，而不只是一个描述字段。同一 `batch_id` 下的 CASE FREEZE 行数不得超过 `planned_case_count`；超过 N 的第一个 Freeze 必须使 gate 失败。否则即使 N 已经预注册，仍可继续冻结额外案例，再在 Batch Review 时选择最有利的前 N 个结果。

因此：

`PREREGISTERED_N -> FREEZE_COUNT <= N`

这里暂时只执行“不得超 N”，不把“未达到 N”立即判为 validator failure，因为批次可能仍在收集中。是否已完成 N、是否存在事前允许并完整记录的外部中止、以及未满 N 的批次是否只能判为不完整，属于后续 Batch Review Gate 的职责；在该 Gate 建立前，未满 N 当然不能据此升级 empirical credit。

### Machine-evaluable primary metric / decision rule

仅把一句自然语言 decision rule 写进 Batch 再做 hash，仍不足以冻结真正的判定门槛。例如：

`candidate must exceed baseline by frozen threshold T`

这句话虽然字面被冻结，但 `T` 没有数值化，aggregation 也没有固定；结果出来后仍可决定 T 是 0、0.05 还是 0.20，也可把平均值改成 best-case selection，而不改写原句。

因此：

`FROZEN_TEXT != MACHINE_EVALUABLE_DECISION_RULE`

当前合同要求：

- `primary_metric` 必须是稳定的 uppercase machine key，例如 `PRIMARY_SCORE`，不能是解释性散文；
- `decision_rule` 必须是 exact-key object：`aggregation / operator / threshold`；
- 当前只允许 `aggregation = MEAN`，不允许 `BEST_CASE`、事后挑子集或其他未治理 aggregation；
- `operator` 只能是 `> / >= / < / <=`；
- `threshold` 必须在 preregistration 时就是有限数值，不能写 `T`、`TBD`、`later`、NaN 或 Infinity；
- Batch 的 canonical hash 会把 exact metric key、scoring spec 与 exact decision object 一起绑定到后续 Freeze。

### Scoring-function provenance

机器 metric key 和数值 score 仍然不足以证明评分过程已经冻结。若 Outcome 只提交：

`score_components = {PRIMARY_SCORE: 0.73}`

而仓库不知道 `0.73` 是怎样从事前预测和事后观察值计算出来的，那么使用者仍可在结果出现后更换 scoring function，再把一个合法数值写入 `PRIMARY_SCORE`。这种做法虽然字段、类型和 threshold 都合法，本质上仍保留了 outcome-dependent scoring freedom。

因此：

`MACHINE_METRIC_KEY + NUMERIC_SCORE != PREREGISTERED_SCORING_FUNCTION`

当前第一版合同刻意只支持一个极窄、可完全重算的评分器：

`primary_metric_spec = {scoring_rule: EXACT_MATCH_V1}`

`EXACT_MATCH_V1` 的定义固定为：

- 输入一：CASE FREEZE 中已经 hash 锁定的 `frozen_payload.prediction`；
- 输入二：Outcome 中登记的结构化 `observed_value`；
- 二者完全相等，primary score = `1.0`；
- 二者不等，primary score = `0.0`；
- evaluable Outcome 的 `observed_value` 必须是非空文本；
- validator 必须重新计算该分数，并拒绝任何与重算值不一致的 `score_components[primary_metric]`。

因此：

`FROZEN_PREDICTION + OBSERVED_VALUE + VERSIONED_SCORING_RULE -> RECOMPUTABLE_PRIMARY_SCORE`

这里故意不支持模糊匹配、部分相似、人工裁量分、加权复合分、LLM judge 或事后定义的 normalization。不是说这些方法永远不可用，而是它们需要各自独立、机器可审计且带版本的 scoring contract；在此之前不能用自由文本说明来冒充预注册评分器。

一个当前可接受的结构例子：

`primary_metric = PRIMARY_SCORE`

`primary_metric_spec = {scoring_rule: EXACT_MATCH_V1}`

`decision_rule = {aggregation: MEAN, operator: >=, threshold: 0.5}`

这仍然**不是** Batch Review 本身。当前 gate 只确保每个可评价案例的主分数可由 frozen prediction 与 observed value 重算，并确保未来存在唯一、可机器应用的 aggregation/operator/threshold。最终检查批次完整性、聚合全部 Outcome、应用 decision rule 并形成 batch-level verdict，仍由后续 Batch Review Gate 承担。

如果 primary metric、scoring rule、threshold、aggregation、operator、样本量、停止规则或排除规则在看过该批结果后才确定，则该批不能获得 prospective credit。

## 5. CASE FREEZE 合同

后续真实案例使用：

`knowledge/K2_PROSPECTIVE_FREEZES.jsonl`

每条 Freeze 必须属于一个已经 PREREGISTERED 的 batch，并保存该 Batch 的 `batch_sha256`，发生在结果未知时。对于固定 N batch，同一 `batch_id` 的 Freeze 总数还必须满足 `freeze_count <= planned_case_count`。至少固定：

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

### Multi-domain route freeze

当绑定 hypothesis 的 work family 有多个 governed routes 时，Freeze payload 必须包含 `active_domain_routes`，并满足：

1. 是非空字符串数组；
2. 不得包含重复 route；
3. 每个 active route 都必须属于该 work family 已治理、并由 Plan 的 `hypothesis_context_sha256` 绑定的 `domain_routes`；
4. active route 的排列必须保持 governed route 的既定顺序，不得为了结果或解释便利重新排序；
5. 可以只激活一个 route，也可以显式激活多个 route；但选择发生在 outcome 未知时，随后进入 frozen payload SHA；
6. 结果出现后不得新增、删除、替换或重排 active routes。

因此：

`UPSTREAM_ROUTE_SCOPE_BINDING != DOWNSTREAM_ACTIVE_ROUTE_FREEZE`

`MULTI_DOMAIN_HYPOTHESIS -> PLAN_BINDS_GOVERNED_ROUTE_SCOPE -> PRE_OUTCOME_ACTIVE_ROUTE_FREEZE`

Plan 的 context hash 解决“允许使用哪些 route 能否在设计后漂移”；Freeze 的 `active_domain_routes` 解决“本案例实际用了哪些 route 能否在结果后挑选”。二者缺一不可。

Freeze 的 payload 必须生成 canonical SHA256。Outcome 只能引用这个 hash 与完整 Freeze record hash，不能把结果出现后的新解释写回 Freeze。

## 6. OUTCOME 合同

后续结果文件：

`knowledge/K2_PROSPECTIVE_OUTCOMES.jsonl`

Outcome 只允许：

- 引用既有 Freeze；
- 绑定完整 `freeze_record_sha256` 与 `frozen_payload_sha256`；
- 记录 `observed_value` 以及实际结果的匿名化/结构化摘要；
- 按事前规则标记 SUCCESS / PARTIAL / FAIL / ABSTAIN / UNEVALUABLE；
- 记录事后才想到的新解释，但必须显式标记为 `post_hoc`；
- 保留失败与不可判定案例。

对于 `SUCCESS / PARTIAL / FAIL` Outcome：

- `observed_value` 必须是非空文本；
- `score_components` 必须包含所属 Batch 已预注册的 `primary_metric` machine key；
- primary score 必须是有限数值；
- 对当前 `EXACT_MATCH_V1`，validator 必须从 Freeze prediction 与 Outcome observed_value 重算 `0.0/1.0`，提交值与重算值不一致即 fail closed。

`ABSTAIN / UNEVALUABLE` 可以没有 primary metric score；`observed_value` 可为 `null`，若真实结果后来可观察，也允许保留非空结构化文本。它们必须被保留，后续 Batch Review 必须把 abstention / unevaluable rate 纳入审查，不能从样本分母中静默消失。

因此：

`PREREGISTERED_PRIMARY_METRIC -> PREREGISTERED_SCORING_RULE -> RECOMPUTABLE_EVALUABLE_OUTCOME_SCORE`

Outcome 不得修改原 prediction、confidence、Role Map、Eligible Rule Set、Interpretation Path、`active_domain_routes`、Batch primary metric、primary metric spec 或 decision rule。

## 7. 禁止“冻结表演”

以下情形不算 prospective validation：

- 结果已经知道才补写 Freeze；
- 看过部分/全部结果后才选择 primary metric、scoring rule、threshold、aggregation、operator、sample size 或 stopping rule；
- 使用自由文本 `decision_rule`、符号阈值 `T/TBD` 或结果后才解释的判定门槛；
- 只登记一个数值 `PRIMARY_SCORE`，却没有预注册可重算 scoring function；
- evaluable Outcome 不记录结构化 observed value，或提交的 primary score 与预注册评分器重算结果不同；
- evaluable Outcome 不记录预注册 primary metric，却在 Batch Review 时临时采用其他 score；
- 使用 `planned_case_count=null` 配合自由文本 stopping rule 作为当前合同下的“预注册”；
- 预注册 N 后继续建立第 N+1 个及后续 CASE FREEZE，再在结果出现后挑选样本；
- hypothesis 内容修改后只保留原 `hypothesis_id`，继续沿用旧 Plan/Batch/Freeze；
- Work-Family 的 governed route scope 改变后继续沿用旧 `hypothesis_context_sha256` / Plan；
- 预测写得足够模糊，任何结果都能解释为命中；
- 反馈后更换用神、主观察层、规则集或 active domain route；
- multi-domain family 在 outcome 后才决定采用哪个 route，或为了结果调整 route 顺序；
- 只保留命中案例；
- 没有失败条件；
- 没有竞争模型 / baseline；
- 单案例命中直接提升理论信用；
- 用古籍案例、网络复盘或已知答案数据冒充未知结果前瞻测试。

## 8. 高风险边界

医疗、法律、金融、战争、人身安全、重大关系决策等高风险内容只允许研究性记录，不得通过本协议升级为现实行动建议。

公开仓库不得保存真实姓名、联系方式、精确地址、账户信息等个人敏感资料。案例必须使用匿名 `case_id` 或只保存结构化派生数据。

## 9. Empirical Credit 升级规则

当前所有候选模型保持：

`empirical_credit = NONE`

未来即使已有多个 Outcome，也必须经过独立的 `BATCH REVIEW` 才能讨论升级。Batch Review 至少要检查：

- 预先承诺的 primary metric machine key、versioned scoring rule 与 machine-evaluable decision rule；
- 每个 evaluable Outcome 的 primary score 是否可由 frozen prediction + observed value 重算；
- 按预注册 aggregation/operator/threshold 对全部可评价 Outcome 的主分数执行判定；
- calibration / discrimination / abstention；
- 与 baseline 的差异；
- 失败样本和不可判定比例；
- 是否存在同一案例重复计数；
- 是否达到预注册 `planned_case_count`，或是否存在经事前规则允许且完整记录的外部中止；
- 是否发生 hypothesis / governed context / rule / route / metric / scoring-function 漂移；
- 是否违反 stopping / exclusion rule；
- 模型更新是否在新批次重新冻结。

在 Batch Review Gate 建立前，任何前瞻案例或批次都不得把 `empirical_credit` 改成非 `NONE`。

## 10. 原创理论的纪律

“自建理论”不是脱离验证，而是比继承理论承担更严格的反证义务。

项目当前候选方向如 `RELATIONAL_CONFIGURATION` 与 `CONTEXTUAL_STATE_TRANSITION`，只能作为 hypothesis/model candidate。若预注册测试显示它们不优于简单 baseline、无法改善复现性，或需要持续事后补规则才能成立，就必须降级、拆分或放弃。

真正的原创性，不是拥有更多解释，而是能主动删除那些经不起冻结测试的解释自由度。

## 11. 当前工程状态边界

本协议的 hypothesis-content binding、hypothesis-context binding、route-freeze、fixed-sample-size、machine-decision-rule 与 scoring-function-provenance hardening 只修改验证合同、设计记录与 fail-closed 测试。它不会自动创建任何真实 Batch、Freeze 或 Outcome，也不会给已有 hypothesis 升级 empirical credit。

当前已有两个 `DESIGN_READY` Plan 会写入与现行 H-JD-001 / H-JD-002 完整对象匹配的 `hypothesis_sha256`，以及与当前 `WF-QM-JIADUN-ZHENSHOU-001 + [qimen]` 受治理上下文匹配的 `hypothesis_context_sha256`；这是对既有设计 referent 的显式绑定，不是新实验结果。

只有在未来单独授权并满足 preregistration、unknown-outcome、hypothesis/content/context binding、fixed-N batch、Freeze 数量上限、machine-evaluable primary metric / scoring function / decision rule 与版本绑定条件后，真实 prospective records 才能进入仓库。
