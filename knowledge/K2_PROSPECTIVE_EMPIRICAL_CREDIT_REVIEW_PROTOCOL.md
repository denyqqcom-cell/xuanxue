# K2 Prospective Empirical Credit Review Protocol

版本：2026-09-04
状态：ACTIVE_CONTRACT
上游：`K2_PROSPECTIVE_VALIDATION_PROTOCOL.md`、`K2_PROSPECTIVE_BATCH_REVIEW_PROTOCOL.md`、`K2_PROSPECTIVE_EMPIRICAL_CREDIT_POLICY_BINDING_PROTOCOL.md`

## 1. 目的

单个 Batch Review 的 `PASS` 只证明该批在固定 N、完整 retained outcome set、同案 comparator、固定 scoring rule 和冻结 decision rule 下通过了预注册门槛。

它不等于经验有效性，更不等于理论或形上命题为真。

核心不变量：

`MACHINE_VALID_BATCH_PASS != EMPIRICAL_VALIDITY`

`ONE_PASSING_BATCH != REPLICATION`

`POSTOUTCOME_POLICY_SELECTION != PREREGISTERED_EMPIRICAL_REVIEW`

本 Gate 的最高输出只允许：

`READY_FOR_MANUAL_EMPIRICAL_REVIEW`

并始终保持：

`empirical_credit = NONE`

因此本 Gate 是“是否值得进入人工经验信用审查”的机器门禁，不是自动授予经验信用的机制。

## 2. Review ledger

正式记录：

`knowledge/K2_PROSPECTIVE_EMPIRICAL_CREDIT_REVIEWS.jsonl`

每条 Review 必须绑定：

- exact `policy_version` 与 `policy_sha256`；
- exact `plan_id`、`hypothesis_id`、`hypothesis_sha256`、`hypothesis_context_sha256`；
- exact `model_commit_sha`；
- exact `comparator_ref`；
- `replication_contract_sha256`；
- 完整 replication cohort 的 `batch_review_ids`；
- 完整 Batch Review records 的 `batch_review_records_sha256`；
- 批次数、总案例数、discordant pair 数、candidate win / comparator win / tie 数；
- pooled paired delta；
- one-sided exact paired-binomial p-value；
- replication consistency；
- case token uniqueness；
- 从 preregistered policy 重新取得的 minimum batch count、minimum discordant count 与 alpha；
- `credit_readiness`；
- `research_only=true`、`empirical_credit=NONE`、`status=REVIEWED`。

Review 不得读取“现在仓库默认采用哪套 policy”来替代历史 Batch 的事前绑定。

## 3. Replication contract

两个 Batch 只有在以下受治理字段完全一致时，才属于同一个 replication cohort：

- Plan 与 `plan_sha256`；
- exact `model_commit_sha`；
- comparator；
- exact `empirical_credit_policy_version`；
- exact `empirical_credit_policy_sha256`；
- planned N；
- sampling rule；
- primary metric 与 scoring spec；
- decision rule；
- secondary metrics；
- stopping rule；
- exclusion rule；
- duplicate-case policy；
- research-only boundary。

这些字段组成 canonical `replication_contract_sha256`。

因此：

`SAME_HYPOTHESIS != SAME_REPLICATION_CONTRACT`

`SAME_POLICY_NAME != SAME_POLICY_CONTENT`

改模型版本、改 comparator、改样本量、改评分、改阈值、改排除规则、改经验信用政策版本或政策内容，都必须进入新的 cohort，不能与旧批次混算成“重复验证”。

## 4. Complete cohort rule

Credit Review 不允许自行挑选有利的 Batch Review。

对于 exact：

`plan_id + model_commit_sha + comparator_ref + policy_version + policy_sha256 + replication_contract_sha256`

仓库中属于该 cohort 的所有 Batch 都必须已有 Batch Review；Review 的 `batch_review_ids` 必须等于该 cohort 的完整 Review 集合，`batch_review_records_sha256` 必须绑定这些 exact records。

因此禁止：

- 只选 PASS batch；
- 隐去同 cohort 的 FAIL batch；
- 忽略尚未 review 的 batch 后宣布 replication；
- Batch Review 改写后继续沿用旧 Credit Review；
- 用结果出来后新增的统计政策重新解释旧 Batch。

## 5. V1 replication / uncertainty policy

版本化政策注册表：

`knowledge/K2_PROSPECTIVE_EMPIRICAL_CREDIT_POLICIES.jsonl`

当前 V1 为：

- `policy_version = EMPIRICAL_CREDIT_REVIEW_V1`；
- `minimum_batch_count = 2`；
- 每个 included Batch Review 必须 `PASS`；
- 每个 batch 的 `aggregate_value > 0`；
- `minimum_discordant_count = 20`；
- `alpha = 0.05`；
- pooled direction 必须为正；
- candidate wins 必须多于 comparator wins；
- uncertainty test 为 `ONE_SIDED_EXACT_PAIRED_BINOMIAL_V1`；
- readiness ceiling 为 `READY_FOR_MANUAL_EMPIRICAL_REVIEW`；
- `automatic_empirical_credit_upgrade = false`。

这些数值不再只是 validator 当前写死的“默认值”。每个 Batch 在 Outcome 出现前已经保存 policy version 与 canonical policy SHA256；Credit Review 必须用 cohort 当时绑定的 exact policy 重新计算。

未来若出现 V2，只能新增 version，并修改相应 machine implementation/test；不能原地修改 V1 后让旧 Batch 静默继承新门槛。

## 6. Scoring 与 uncertainty

当前 scorer 是 `PAIRED_EXACT_MATCH_DELTA_V1`，每个 evaluable case 的 candidate-vs-comparator delta 是：

- `+1`：candidate 独赢；
- `0`：两者同胜或同败；
- `-1`：comparator 独赢。

V1 只在 discordant pairs 上计算：

`P(X >= candidate_wins | n = discordant_count, p = 0.5)`

所有 win/loss/tie、pooled delta 和 p-value 都必须从 hash-bound Freeze 与 retained Outcome 机器重算，而不是信任 Credit Review 提交的数字。

但：

`P_VALUE_THRESHOLD_CROSSED != EMPIRICAL_TRUTH`

该 exact tail 仍依赖样本独立、采样代表性、无未建模泄漏等假设；这些假设不能由 p-value 自己证明。

## 7. Case-token uniqueness 只是最小反重复控制

V1 要求 cohort 内 `case_id` token 不重复，以阻止同一仓库案例 token 被多批次直接重复计票。

但：

`CASE_TOKEN_UNIQUENESS != REAL_WORLD_SAMPLE_INDEPENDENCE`

匿名 token 唯一不能证明两个现实事件真正独立，也不能排除同一现实事件被重新编码成不同 token。

因此即使所有 V1 条件满足，输出仍只能是 `READY_FOR_MANUAL_EMPIRICAL_REVIEW`，不能自动升级 empirical credit。

## 8. Readiness 状态

机器只允许：

- `NOT_ELIGIBLE`
- `READY_FOR_MANUAL_EMPIRICAL_REVIEW`

要进入 readiness ceiling，必须按 cohort preregistered policy 同时满足其全部机器条件。对于当前 V1，即至少包括：

- cohort 完整；
- 至少 2 个 batch；
- 所有 batch PASS；
- 每批效果方向为正；
- 全部 raw paired score 可重算；
- cohort case token 无重复；
- discordant pairs 至少 20；
- candidate wins > comparator wins；
- pooled paired delta > 0；
- exact one-sided p-value <= 0.05。

否则为 `NOT_ELIGIBLE`。

## 9. Empirical boundary

本 Gate 不负责：

- 自动把 `empirical_credit` 从 `NONE` 升为任何级别；
- 证明外部有效性；
- 证明现实样本独立；
- 证明跨地区、跨时间、跨人群可迁移；
- 证明未测试模型版本同样有效；
- 证明传统术数整体有效；
- 解锁 Claim Extraction。

即使未来出现机器合法的 `READY_FOR_MANUAL_EMPIRICAL_REVIEW`，仍必须经过独立人工/项目审查，并审计样本独立性、采样偏差、泄漏、外部复现、版本漂移、失败 cohort 与适用边界。

当前没有真实 Batch、Freeze、Outcome、Batch Review 或 Credit Review；本协议只建立 fail-closed 方法合同。
