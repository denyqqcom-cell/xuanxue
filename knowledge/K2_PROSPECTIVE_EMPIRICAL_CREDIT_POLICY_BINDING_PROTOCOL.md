# K2 Prospective Empirical-Credit Policy Binding Protocol

版本：2026-09-04
状态：ACTIVE_CONTRACT
上游：`K2_PROSPECTIVE_VALIDATION_PROTOCOL.md`
下游：`K2_PROSPECTIVE_EMPIRICAL_CREDIT_REVIEW_PROTOCOL.md`

## 1. 目的

一个统计/复制审查规则即使写成机器代码，也不能在结果出现后再选择。

核心不变量：

`POSTOUTCOME_POLICY_SELECTION != PREREGISTRATION`

`POLICY_VERSION_NAME != POLICY_CONTENT_BINDING`

`BATCH_PREREGISTRATION + VERSIONED_POLICY_SHA256 -> PREOUTCOME_CREDIT_POLICY_BINDING`

本协议只解决经验信用政策的 provenance 与 hindsight-control，不授予任何 empirical credit。

## 2. 版本化政策注册表

正式注册表：

`knowledge/K2_PROSPECTIVE_EMPIRICAL_CREDIT_POLICIES.jsonl`

每个 policy version 是一个不可依赖“当前默认值”解释的完整机器对象。当前 V1 记录包括：

- `policy_version = EMPIRICAL_CREDIT_REVIEW_V1`
- `minimum_batch_count = 2`
- `minimum_discordant_count = 20`
- `alpha = 0.05`
- `uncertainty_test = ONE_SIDED_EXACT_PAIRED_BINOMIAL_V1`
- required primary metric / scoring rule / aggregation
- batch PASS 与正方向一致性要求
- candidate win / pooled delta 条件
- case-token anti-duplication 条件
- readiness ceiling
- `automatic_empirical_credit_upgrade = false`
- `research_only = true`

未来若要改变样本批次数、discordant floor、alpha、uncertainty test 或其他 governed 条件，必须新增新的 policy version，并通过新的代码/测试审查；不得把 V1 同名内容原地改写后继续声称旧 Batch 当初绑定的就是新规则。

## 3. Batch preregistration 直接绑定政策

每个未来真实 Batch 必须新增并冻结：

- `empirical_credit_policy_version`
- `empirical_credit_policy_sha256`

其中 SHA256 是对注册表中该 exact policy object 的 canonical JSON SHA-256。

因此：

`BATCH -> { POLICY_VERSION, POLICY_CONTENT_SHA256 }`

后续 CASE FREEZE 已经通过 `batch_sha256` 绑定 exact Batch，所以政策绑定自动进入既有 provenance 链：

`POLICY -> BATCH -> FREEZE -> OUTCOME -> BATCH_REVIEW -> EMPIRICAL_CREDIT_REVIEW`

如果 Batch 的 policy version 不存在、hash 不是 lowercase SHA-256、hash 与注册表 exact content 不符，或 Batch 使用的 metric/scoring/aggregation 与该 policy 不兼容，Prospective Validation 必须 fail closed。

## 4. 为什么只冻结版本名不够

下面这种记录不充分：

`policy_version = EMPIRICAL_CREDIT_REVIEW_V1`

如果 V1 内容后来从 `alpha=0.05` 改成 `alpha=0.10`，但版本名不变，只靠字符串不能证明 Batch 当时面对的是哪一套门槛。

因此：

`POLICY_VERSION_NAME != POLICY_CONTENT_IDENTITY`

必须同时保存 canonical policy hash。只要 V1 内容发生任何受治理改变，旧 Batch 的 hash 就必须失配；不能静默继承新解释。

## 5. Empirical Credit Review 必须使用 cohort 事前绑定的政策

Credit Review 不能读取“现在仓库默认政策”后直接评估历史 cohort。

Review 必须记录：

- `policy_version`
- `policy_sha256`

并且该 version/hash 必须与 cohort 内所有 Batch 的预注册绑定完全一致。

`replication_contract_sha256` 也包含 policy version/hash，因此两个其他字段完全相同、但经验信用政策不同的 Batch 不属于同一个 replication cohort。

Review 中的：

- `minimum_batch_count`
- `minimum_discordant_count`
- `alpha`
- readiness 判定

必须由 Batch 事前绑定的 exact policy 重新取得并机器复算，不能使用结果后人工输入的门槛。

## 6. 当前 V1 仍然不自动授予 empirical credit

即使 cohort 满足 policy，并得到：

`READY_FOR_MANUAL_EMPIRICAL_REVIEW`

仍必须保持：

- `empirical_credit = NONE`
- `research_only = true`

因为 policy binding 只能证明统计/复制门槛没有在结果后偷换，不证明：

- 现实样本真正独立；
- 样本具有代表性；
- 不存在资料泄漏；
- 外部复现成立；
- 模型在其他版本、地区、时期或问题域保持效果；
- 术数理论或形上命题为真。

## 7. Fail-closed 规则

以下任一情况必须拒绝：

- policy registry 为空；
- policy version 重复或 schema 非法；
- Batch 缺少 policy version/hash；
- Batch 引用了未知 policy version；
- Batch policy hash 与注册表 exact content 不一致；
- policy 与 Batch 的 primary metric / scoring rule / aggregation 不一致；
- Review 的 policy version/hash 与 cohort 预注册政策不一致；
- replication cohort 混入不同政策版本或内容；
- Review 试图使用与预注册政策不同的 minimum batch count、discordant floor 或 alpha；
- 任一 Review 试图自动升级 `empirical_credit`。

## 8. 当前项目边界

当前没有真实 Batch、Freeze、Outcome、Batch Review 或 Empirical Credit Review。

本协议只是为未来数据建立先验约束：

`PREOUTCOME_POLICY_BINDING = ENGINEERING/PROVENANCE CREDIT ONLY`

不等于：

`PREDICTIVE_VALIDITY`

更不等于：

`METAPHYSICAL_TRUTH`
