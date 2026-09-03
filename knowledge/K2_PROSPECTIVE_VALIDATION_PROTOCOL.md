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
2. `BATCH PREREGISTRATION`：在该批任何 Outcome 出现前，冻结样本规则、样本量/停止规则、primary metric、decision rule、排除规则；
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
- planned case count 或明确 stopping rule；
- primary metric；
- decision rule / threshold；
- secondary metrics；
- exclusion rule；
- duplicate-case policy；
- batch status=`PREREGISTERED`；
- `empirical_credit=NONE`。

如果 primary metric、threshold、停止规则或排除规则在看过该批结果后才确定，则该批不能获得 prospective credit。

## 5. CASE FREEZE 合同

后续真实案例使用：

`knowledge/K2_PROSPECTIVE_FREEZES.jsonl`

每条 Freeze 必须属于一个已经 PREREGISTERED 的 batch，并保存该 Batch 的 `batch_sha256`，发生在结果未知时。至少固定：

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
- 记录实际结果的匿名化/结构化表示；
- 按事前规则标记 SUCCESS / PARTIAL / FAIL / ABSTAIN / UNEVALUABLE；
- 记录事后才想到的新解释，但必须显式标记为 `post_hoc`；
- 保留失败与不可判定案例。

Outcome 不得修改原 prediction、confidence、Role Map、Eligible Rule Set、Interpretation Path、`active_domain_routes`、Batch primary metric 或 decision rule。

## 7. 禁止“冻结表演”

以下情形不算 prospective validation：

- 结果已经知道才补写 Freeze；
- 看过部分/全部结果后才选择 primary metric、threshold 或 stopping rule；
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

- 预先承诺的 primary metric 与 decision rule；
- calibration / discrimination / abstention；
- 与 baseline 的差异；
- 失败样本和不可判定比例；
- 是否存在同一案例重复计数；
- 是否发生 hypothesis / governed context / rule / route 漂移；
- 是否违反 stopping / exclusion rule；
- 模型更新是否在新批次重新冻结。

在 Batch Review Gate 建立前，任何前瞻案例或批次都不得把 `empirical_credit` 改成非 `NONE`。

## 10. 原创理论的纪律

“自建理论”不是脱离验证，而是比继承理论承担更严格的反证义务。

项目当前候选方向如 `RELATIONAL_CONFIGURATION` 与 `CONTEXTUAL_STATE_TRANSITION`，只能作为 hypothesis/model candidate。若预注册测试显示它们不优于简单 baseline、无法改善复现性，或需要持续事后补规则才能成立，就必须降级、拆分或放弃。

真正的原创性，不是拥有更多解释，而是能主动删除那些经不起冻结测试的解释自由度。

## 11. 当前工程状态边界

本协议的 hypothesis-content binding、hypothesis-context binding 与 route-freeze hardening 只修改验证合同、设计记录与 fail-closed 测试。它不会自动创建任何真实 Batch、Freeze 或 Outcome，也不会给已有 hypothesis 升级 empirical credit。

当前已有两个 `DESIGN_READY` Plan 会写入与现行 H-JD-001 / H-JD-002 完整对象匹配的 `hypothesis_sha256`，以及与当前 `WF-QM-JIADUN-ZHENSHOU-001 + [qimen]` 受治理上下文匹配的 `hypothesis_context_sha256`；这是对既有设计 referent 的显式绑定，不是新实验结果。

只有在未来单独授权并满足 preregistration、unknown-outcome、hypothesis/content/context binding 与版本绑定条件后，真实 prospective records 才能进入仓库。
