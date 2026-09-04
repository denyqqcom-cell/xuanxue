# K2 Prospective Empirical Credit Review Protocol

版本：2026-09-04
状态：ACTIVE_CONTRACT
上游：`K2_PROSPECTIVE_VALIDATION_PROTOCOL.md`、`K2_PROSPECTIVE_BATCH_REVIEW_PROTOCOL.md`

## 1. 目的

单个 Batch Review 的 `PASS` 只证明该批在固定 N、完整 retained outcome set、同案 comparator、固定 scoring rule 和冻结 decision rule 下通过了预注册门槛。

它不等于经验有效性，更不等于理论或形上命题为真。

核心不变量：

`MACHINE_VALID_BATCH_PASS != EMPIRICAL_VALIDITY`

`ONE_PASSING_BATCH != REPLICATION`

本 Gate 的最高输出只允许：

`READY_FOR_MANUAL_EMPIRICAL_REVIEW`

它仍然必须保持：

`empirical_credit = NONE`

因此本 Gate 是“是否值得进入人工经验信用审查”的机器门禁，不是自动授予经验信用的机制。

## 2. Review ledger

正式记录：

`knowledge/K2_PROSPECTIVE_EMPIRICAL_CREDIT_REVIEWS.jsonl`

每条 Review 绑定：

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
- 固定 policy 参数；
- `credit_readiness`；
- `research_only=true`、`empirical_credit=NONE`、`status=REVIEWED`。

## 3. Replication contract

两个 Batch 只有在以下受治理字段完全一致时，才属于同一个 V1 replication cohort：

- Plan 与 `plan_sha256`；
- exact `model_commit_sha`；
- comparator；
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

改模型版本、改 comparator、改样本量、改评分、改阈值、改排除规则，都必须进入新的 cohort，不能与旧批次混算成“重复验证”。

## 4. Complete cohort rule

Credit Review 不允许自行挑选有利的 Batch Review。

对于 exact：

`plan_id + model_commit_sha + comparator_ref + replication_contract_sha256`

仓库中属于该 cohort 的所有 Batch 都必须已有 Batch Review；Review 的 `batch_review_ids` 必须等于该 cohort 的完整 Review 集合，`batch_review_records_sha256` 必须绑定这些 exact records。

因此禁止：

- 只选 PASS batch；
- 隐去同 cohort 的 FAIL batch；
- 忽略尚未 review 的 batch 后宣布 replication；
- Batch Review 改写后继续沿用旧 Credit Review。

## 5. V1 replication / uncertainty policy

V1 采用保守、固定、机器可重算的政策：

- `minimum_batch_count = 2`；
- 每个 included Batch Review 必须 `PASS`；
- 每个 batch 的 `aggregate_value > 0`，即方向一致地支持 candidate 优于 comparator；
- `minimum_discordant_count = 20`；
- `alpha = 0.05`；
- pooled direction 必须为正；
- candidate wins 必须多于 comparator wins；
- one-sided exact paired-binomial p-value 必须 `<= 0.05`。

当前 scorer 是 `PAIRED_EXACT_MATCH_DELTA_V1`，因此每个可评价案例的 paired delta 只能由冻结 candidate/comparator prediction 与同一 observed value 机器重算。

不采用人工打分、自由文本置信判断或事后统计模型。

## 6. Case-token uniqueness 只是最小反重复控制

V1 会要求 cohort 内 `case_id` token 不重复，以阻止同一仓库案例 token 被多批次直接重复计票。

但必须明确：

`CASE_TOKEN_UNIQUENESS != REAL_WORLD_SAMPLE_INDEPENDENCE`

匿名 token 唯一不能证明两个现实事件真正独立，也不能排除同一现实事件被重新编码成不同 token。

因此即使所有 V1 条件满足，输出仍只能是 `READY_FOR_MANUAL_EMPIRICAL_REVIEW`，不能自动升级 empirical credit。

未来若要机器证明更强的跨批独立性，需要另建隐私安全、事前生成且跨批稳定的 case fingerprint contract，并单独 RED→GREEN。

## 7. 为什么使用 exact paired-binomial tail

对于当前 paired exact-match scorer，每个 evaluable case 的 candidate-vs-comparator delta 是：

- `+1`：candidate 独赢；
- `0`：两者同胜或同败；
- `-1`：comparator 独赢。

V1 只在 discordant pairs 上计算：

`P(X >= candidate_wins | n = discordant_count, p = 0.5)`

这提供一个确定、无第三方统计依赖的机器不确定性检查。

但它仍依赖样本独立、采样代表性、无未建模泄漏等假设；这些假设当前不能由该 p-value 自己证明。

所以：

`P_VALUE_THRESHOLD_CROSSED != EMPIRICAL_TRUTH`

## 8. Readiness 状态

机器只允许：

- `NOT_ELIGIBLE`
- `READY_FOR_MANUAL_EMPIRICAL_REVIEW`

要进入 `READY_FOR_MANUAL_EMPIRICAL_REVIEW`，必须同时满足：

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

即使未来出现机器合法的 `READY_FOR_MANUAL_EMPIRICAL_REVIEW`，仍必须经过独立人工审查，并审计：样本独立性、采样偏差、泄漏、外部复现、版本漂移、失败批次与适用边界。

当前没有真实 Batch、Freeze、Outcome、Batch Review 或 Credit Review；本协议只建立 fail-closed 方法合同。
