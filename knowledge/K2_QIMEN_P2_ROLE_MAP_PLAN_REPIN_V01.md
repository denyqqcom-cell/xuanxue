# K2 Qimen P2 Role-Map Plan Repin v0.1

状态：`PRE_BATCH / PLAN_REPINNED / POST_REPIN_AUDIT_PENDING`

Trigger：`P2-AUD-012`
Old Plan：`K2PV-QRM-001`
New Plan：`K2PV-QRM-002`
Empirical Credit：`NONE`

## 1. 为什么必须换 active plan

P2 v0.1 的 plan 只冻结了 Role Map、Layer Priority、prediction 与基本 shared controls。

反向审计发现，它没有原子绑定：

- world-variable / symbol / feature manifests；
- complexity / reasoning / rule-trace budgets；
- interpreter information / tool budgets；
- blinding / cross-lane isolation；
- denominator / abstention scoring；
- deterministic generator / reproducibility fixture。

继续让 `K2PV-QRM-001` 作为 active plan，会出现“protocol 已变严，但 future Freeze 仍按旧字段生成”的断层。

## 2. Repin 动作

本轮在 `Batch=0 / Freeze=0 / Outcome=0` 条件下：

1. 从 active `K2_PROSPECTIVE_TEST_PLANS.jsonl` 移除 `K2PV-QRM-001`；
2. 加入 `K2PV-QRM-002`；
3. `QRM-H1` origin 更新为 `P2-ROLE-MAP-v0.2`；
4. 旧 active-registry blob `c67e906f18dbbbff601174fcb0406a67a61e6076` 与 parent commit `2f578f597bb9ad8faed28d2179270dd819c8883b` 写入 history artifact；
5. 不创建任何 Batch / Freeze / Outcome。

## 3. K2PV-QRM-002 新增冻结边界

新 plan 的 freeze 字段覆盖 P2 v0.2 全部 hardening 要求，包括：

- `world_variable_manifest_hash`
- `symbol_vocabulary_hash`
- `feature_extraction_manifest_hash`
- `eligible_rule_pool_hash`
- comparator / bridge / candidate generator identities
- `layer_priority_generator_hash`
- `prediction_schema_hash`
- prediction cardinality / confidence scale
- role multiplicity / reasoning branch / rule trace budgets
- interpreter information / tool access budgets
- lane blinding / lane order / cross-lane isolation
- primary denominator / abstention scoring / technical UNEVALUABLE policies
- reproducibility fixture hash / nondeterminism seed policy
- interpreter protocol
- primary metric / decision threshold / sampling / stopping / minimum information floor
- contamination ledger policy

## 4. 仍然没有关闭的门

Plan repin 只解决“active plan 有没有字段承载 v0.2 约束”。

它还没有证明：

- generator 真的 deterministic；
- blind runner 真的不能跨 lane 泄漏；
- denominator policy 的 fail-closed 行为正确；
- complexity budgets 在真实 case runner 中不会漂移；
- future Freeze serialization 能完整保存这些字段。

所以：

`BATCH_GATE = BLOCKED_PENDING_POST_REPIN_AUDIT`

下一阶段必须先做 post-repin audit + machine fixtures。

## 5. 当前状态

```text
QRM-H1 = UNTESTED
ACTIVE_PLAN = K2PV-QRM-002
RETIRED_PLAN = K2PV-QRM-001
BATCH_READY = false
BATCH = NONE
FREEZE = NONE
OUTCOME = NONE
EMPIRICAL_CREDIT = NONE
CLAIM_EXTRACTION = BLOCKED
```
