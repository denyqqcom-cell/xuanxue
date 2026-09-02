# K2 Qimen P2 Role-Map Comparative Protocol v0.3

状态：`PLAN_REPINNED / POST_REPIN_AUDIT_REQUIRED / NO_BATCH / NO_FREEZE / NO_OUTCOME`

Hypothesis：`QRM-H1`
Active Plan：`K2PV-QRM-002`
Retired Plan：`K2PV-QRM-001`
Empirical Credit：`NONE`
Claim Extraction：`BLOCKED`

## 0. 这次只完成 Plan Repin，不提前宣布 Batch Ready

v0.2 的 adversarial hardening 已把 P2 的主要隐藏自由度拆出来：representation parity、complexity budget、blinding/isolation、denominator/abstention、determinism 与 single-difference estimand。

但当时 active prospective plan 仍是按 v0.1 生成的 `K2PV-QRM-001`，所以 v0.2 明确保持：

`BATCH_GATE = BLOCKED_PENDING_PLAN_REPIN`

本 v0.3 只关闭这一层不一致：

- active registry 中 `K2PV-QRM-001` 被 `K2PV-QRM-002` 替代；
- `QRM-H1` 的 project-origin 更新到 `P2-ROLE-MAP-v0.2`；
- `K2PV-QRM-002.freeze_required_fields` 已覆盖 v0.2 的全部未来 freeze 要求；
- 旧 plan 通过显式 history artifact + exact old registry blob/commit 保留；
- 没有创建 Batch、Freeze 或 Outcome。

因此状态不是 `BATCH_READY`，而是：

`BLOCKED_PENDING_POST_REPIN_AUDIT`

## 1. 为什么不能把 DESIGN_READY 当成 Batch Ready

`K2PV-QRM-002.status = DESIGN_READY` 是通用 prospective validator 的 plan-state 术语，只表示该 plan 作为设计记录具有完整字段、来源与失败条件。

它不意味着：

- mapping generator 已经实现并 hash；
- blinding runner 已经实现；
- denominator policy 已经跑过 negative fixture；
- reproducibility fixture 已经生成；
- Batch sampling/stopping 数值已经冻结。

所以项目级 gate 仍高于 plan schema：

`PLAN_DESIGN_READY != BATCH_READY`

## 2. 本次 repin 新增的硬绑定

`K2PV-QRM-002` 除 v0.1 原有 Role/Layer/Prediction 字段外，新增并要求未来 Freeze 携带：

- source role catalog hash；
- comparator / bridge / candidate mapping generator；
- topology feature manifest；
- world-variable manifest hash；
- symbol vocabulary hash；
- feature extraction manifest hash；
- eligible rule pool hash；
- layer-priority generator hash；
- prediction schema hash / cardinality / confidence scale；
- role multiplicity / reasoning branch / rule trace budgets；
- interpreter information / tool access budgets；
- lane blinding protocol / lane-order seed / cross-lane isolation policy；
- primary denominator / abstention scoring / technical-UNEVALUABLE policies；
- reproducibility fixture hash / nondeterminism seed policy；
- interpreter protocol；
- primary metric / decision threshold / sampling / stopping / minimum information floor；
- contamination ledger policy。

这些字段只是**要求未来原子冻结**，本轮并没有偷偷替未来 Batch 填值。

## 3. 旧 Plan 如何保留

旧 `K2PV-QRM-001` 不再保留在 active plan registry，因为通用 prospective validator 要求一个 hypothesis 只能有一个 active design plan。

但它没有被“抹掉”。

`knowledge/K2_QIMEN_P2_ROLE_MAP_PLAN_HISTORY.jsonl` 保存：

- 旧 plan id；
- 旧 registry exact blob SHA；
- 退役时的 parent commit；
- Batch/Freeze/Outcome 均为 0；
- 退役原因 `P2-AUD-012`；
- superseding plan id。

加上 Git 历史，可以精确恢复旧 plan 的原始 JSONL 记录。

## 4. QRM-H1 为什么仍保留同一 hypothesis_id

本轮没有把“Role Map 是否有增量”的科学问题换掉，而是收紧其可识别条件。

因此仍用：

`QRM-H1`

但 origin 从 `P2-ROLE-MAP-v0.1` 更新为 `P2-ROLE-MAP-v0.2`，并把 falsification 条件扩展到：

- representation parity；
- complexity / information / tool budget parity；
- prediction schema parity；
- denominator parity；
- blinding / isolation；
- deterministic rerun。

如果这些控制下增量消失，不能再用“场景化更灵活”保护理论。

## 5. 下一门：Post-Repin Audit

下一笔提交才允许检查是否能关闭 Batch gate。

至少要证明：

1. active plan 的 exact freeze-field set 与 v0.2 约束完全一致；
2. C1/C2 的 single-difference estimand 在 plan serialization 后没有被其它字段变化污染；
3. representation parity / complexity budgets 能转成可执行 fixture，而不是只有文字；
4. blind/isolation runner 与 denominator policy 可以 fail-closed；
5. generator determinism / reproducibility fixture 能在任何 Outcome 前 hash；
6. 仍不存在 QRM Batch / Freeze / Outcome。

在这些条件未关闭前：

`batch_creation_allowed = false`

## 6. 当前状态

```text
P2 V01
= HISTORICAL / NOT_BATCH_SAFE

P2 V02
= ADVERSARIAL_HARDENED

P2 V03
= PLAN_REPINNED
= POST_REPIN_AUDIT_REQUIRED

QRM-H1
= UNTESTED

ACTIVE PLAN
= K2PV-QRM-002
= DESIGN_READY (plan schema only)

BATCH_READY
= false

BATCH
= NONE
FREEZE
= NONE
OUTCOME
= NONE

EMPIRICAL_CREDIT
= NONE
CLAIM_EXTRACTION
= BLOCKED
```

这次推进的是实验可识别性，不是预测结论。
