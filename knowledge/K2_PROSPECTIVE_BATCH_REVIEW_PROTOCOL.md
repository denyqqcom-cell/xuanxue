# K2 Prospective Batch Review Protocol

版本：2026-09-04
状态：ACTIVE_CONTRACT
上游：`K2_PROSPECTIVE_VALIDATION_PROTOCOL.md`

## 1. 目的

单案例已经满足 paired comparator parity，并不等于整个批次可以形成比较性结论。

核心不变量：

`VALID_PAIRED_OUTCOMES != VALID_BATCH_LEVEL_CONCLUSION`

`PREREGISTERED_N + COMPLETE_RETAINED_OUTCOME_SET + MACHINE_AGGREGATION + FROZEN_DECISION_RULE -> AUDITABLE_BATCH_VERDICT`

本 Gate 只审查批次完整性与机器可重算 verdict，不授予 empirical credit。

## 2. Review ledger

正式记录：

`knowledge/K2_PROSPECTIVE_BATCH_REVIEWS.jsonl`

每条 Review 必须绑定：

- exact `batch_id` 与 canonical `batch_sha256`；
- `planned_case_count`；
- 实际 Freeze / Outcome / evaluable / abstain / unevaluable 数量；
- 全部 batch Outcome 的 `outcome_ids`；
- 全部 Outcome record 的 canonical `outcome_records_sha256`；
- Batch 预注册的 `aggregate_primary_metric`；
- 可重算 `aggregate_value`；
- `decision_met` 与最终 `batch_verdict`；
- `reviewed_at_utc` 必须晚于该 batch 已保留的所有 Freeze/Outcome；
- `research_only=true`、`empirical_credit=NONE`、`status=REVIEWED`。

## 3. Fixed-N completion

当前只治理 fixed-N batch。

Review 必须重新计算：

`freeze_count == planned_case_count`

并检查每一个 Freeze 都有且只有一个 retained Outcome。Outcome 集合不得由 Review 自选；`outcome_ids` 必须等于仓库中属于该 batch 的完整 Outcome 集合，`outcome_records_sha256` 必须绑定这些 exact records。

因此不得：

- N 未完成就宣布 PASS/FAIL；
- 只聚合有利 Outcome；
- 删除失败案例后重新计算；
- 一个 Freeze 重复计票；
- Outcome 在 Review 后静默改写而继续沿用旧 Review。

## 4. Aggregation / decision

只有 fixed-N 完整、每个 Freeze 都有 Outcome、且当前 V1 中所有 Outcome 都可评价时，Review 才能形成 PASS/FAIL。

当前 paired scorer 为：

`PAIRED_EXACT_MATCH_DELTA_V1`

每个可评价 Outcome 的主分数：

`PAIRED_SCORE_DELTA = CANDIDATE_SCORE - COMPARATOR_SCORE`

Batch Review 不信任提交的 batch aggregate，而是重新从 hash-bound Freeze + Outcome 重算每个 paired delta，再按 Batch 已冻结的：

`decision_rule = {aggregation, operator, threshold}`

执行判定。当前只接受上游已经允许的 `aggregation=MEAN`。

`aggregate_value = mean(all preregistered case paired deltas)`

之后机器应用 `operator/threshold`：满足则 `batch_verdict=PASS`，否则 `FAIL`。

## 5. Abstain / UNEVALUABLE V1 policy

当前 Batch contract 虽允许单案例 `ABSTAIN / UNEVALUABLE` 被保留，但尚未预注册机器可执行的最大弃权率、缺失值处理或 denominator policy。

因此 V1 Batch Review 采用 fail-closed 策略：

- 所有这些案例必须继续保留在 Outcome 集合与计数中；
- 只要存在 `ABSTAIN` 或 `UNEVALUABLE`，batch review 必须为 `INCOMPLETE`；
- `aggregate_value=null`；
- `decision_met=null`；
- 不允许从 denominator 静默删除后宣布 PASS/FAIL。

未来若需要允许带弃权率的正式 verdict，必须先在 Batch preregistration 中建立机器可审计的 missingness/abstention policy，并单独做 RED→GREEN gate。

## 6. INCOMPLETE 是合法审计结果

Batch Review 可以合法记录 `INCOMPLETE`，用于明确证明批次尚未满足判定条件。

以下情况必须是 `INCOMPLETE`：

- Freeze 数少于预注册 N；
- 仍有 Freeze 没有 Outcome；
- 存在 ABSTAIN / UNEVALUABLE；
- 当前合同无法重算完整 paired delta 集合。

`INCOMPLETE` 不是 FAIL，也不是 PASS，更不能升级 empirical credit。

## 7. Empirical boundary

本 Gate 的输出只代表：

`BATCH_CONTRACT_INTEGRITY + MACHINE_RECOMPUTABLE_VERDICT`

它不代表：

`PREDICTIVE_VALIDITY`

也不代表：

`METAPHYSICAL_TRUTH`

即使未来某 batch 的 `batch_verdict=PASS`，当前 Review 仍必须保持 `empirical_credit=NONE`。是否、如何升级 empirical credit 必须由后续独立 Credit Review 规则承担，且必须考虑重复批次、效应稳定性、校准、样本独立性、模型版本变化与失败复现。

当前没有创建真实 Batch、Freeze、Outcome 或 Batch Review；本协议只建立 fail-closed 工程合同。
