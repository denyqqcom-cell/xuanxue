# K2 Qimen P2 Role-Map Adversarial Audit v0.1

状态：`PRE_BATCH / PRE_FREEZE / PRE_OUTCOME`

Audit Target：`K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V01`
Target Plan：`K2PV-QRM-001`
Audit Result：`V01_NOT_BATCH_SAFE`
Prior Status Reassessment：`DESIGN_READY_WAS_PREMATURE`
Empirical Credit：`NONE`

## 0. 为什么这次要反审自己，而不是继续往 Batch 推

上一轮把三条 lane、plate-value access 前冻结、bridge ablation 与 P2-C1/C2/C3 拆分建立起来后，我把 v0.1 标成了 `DESIGN_READY`。

这一步现在需要主动纠正。

v0.1 已经防住“看完结果换用神”“看完盘再选角色”“把 combined win 冒充 Role Map 单项信用”等明显污染，但它仍然没有证明三条 lane 除了目标处理变量之外具有**同等的信息量、复杂度、可见信号、输出难度和弃权成本**。

如果这些量不相等，那么即使未来 P2-B 赢了，也可能只是因为它拥有更大的搜索空间，而不是 question topology 真有增量。

因此本审计把 v0.1 从 `DESIGN_READY` 降级为：

`V01_NOT_BATCH_SAFE`

这是方法学纠错，不是理论失败，也不是经验结论。

## 1. 本次发现的 12 个攻击面

### P2-AUD-001 — Layer Priority 语义不充分

v0.1 只说“固定优先级”与“topology-conditioned priority”，却没有锁死 priority 到底只是聚合次序，还是可以改变：

- 哪些层被看见；
- 哪些规则被激活；
- 是否允许 early stop；
- 每层抽取多少 feature。

若不锁死，P2-C2 测到的就不是纯 Layer Priority。

V02 规定：四层对所有 lane 都可见；feature extraction depth 相同；priority 只允许改变事前冻结的 aggregation policy，不得改变 rule eligibility，也不得 early stop。

### P2-AUD-002 — Symbol / Feature Vocabulary 未 hash-bound

共享 `eligible_rule_pool` 不等于共享 symbol vocabulary 与 feature extractor。

Candidate 如果能看到更多符号派生量，仍然会形成隐藏信息优势。

V02 新增共享并冻结：

- `symbol_vocabulary_hash`
- `feature_extraction_manifest_hash`
- `eligible_rule_pool_hash`

### P2-AUD-003 — World Variable Expansion

Topology lane 可能在 Scenario Graph 上额外创建更多 state variable，再把它们绑定到更多盘面角色。

这会把“更会建模”与“更多解释自由度”混在一起。

V02 要求三 lane 使用同一 `world_variable_manifest`，任何 lane 不得自行增加 world variable。

### P2-AUD-004 — Role Multiplicity / Branch Budget 不对称

即使输入相同，如果 Candidate 可保留 4 个 competing mappings，而 baseline 只能保留 1 个，Candidate 就拥有更大的搜索空间。

V02 要求：

- role multiplicity budget 相等；
- competing mapping 上限事前冻结；
- reasoning branch budget 相等；
- 同时记录 branch count。

### P2-AUD-005 — Interpreter / Tool / Rule-Trace Budget 不对称

同样的资料不代表同样的推理预算。

如果某 lane 得到更长上下文、更多工具调用、更多 rule trace，未来胜出不能归因给 Role Map。

V02 强制：

- interpreter information budget 相等；
- tool access budget 相等；
- rule trace budget 相等。

### P2-AUD-006 — Abstention Denominator Gaming

v0.1 要求共享 abstention policy，但仍没有阻止某 lane 在难例上弃权后把这些 case 从主指标分母移除。

V02 要求：

- case inclusion 在 lane 执行前冻结；
- lane-specific exclusion 禁止；
- ABSTAIN 不得静默删除 case；
- 必须冻结 abstention scoring；
- 必须同时报告 coverage-penalized metric。

### P2-AUD-007 — Prediction Schema / Granularity Drift

如果一条 lane 只输出二分类，另一条允许多档模糊结论，它们的评分难度不同。

V02 要求共享：

- prediction schema；
- prediction cardinality；
- confidence scale；
- output granularity。

### P2-AUD-008 — Lane Identity / Hypothesis Leakage

解释者知道“这是 Candidate”本身就可能产生确认偏差。

V02 要求：

- interpreter 只看到 neutral lane labels；
- QRM-H1 身份对解释者隐藏；
- lane 顺序用预注册 seed 决定。

### P2-AUD-009 — Cross-Lane Intermediate Contamination

若先做 A，再把 A 的中间推理暴露给 A' 或 B，三 lane 已经不独立。

V02 规定：

- 不得共享中间 Role Map / reasoning / prediction；
- 三条 prediction 全部 freeze 后才允许 unblind。

### P2-AUD-010 — Mapping Generator 非确定性

“generator 名称固定”不等于同一输入一定生成同一 mapping。

V02 要求：

- generator version + hash；
- nondeterminism seed 冻结；
- Batch 前 synthetic reproducibility fixture；
- 同输入同 lane 必须精确重建相同 map。

### P2-AUD-011 — Attribution 只有标签，没有 single-difference machine lock

v0.1 已经写出 C1/C2/C3，但没有机器声明：

`C1 除 Role Binding 外所有维度必须相等`
`C2 除 Layer Priority 外所有维度必须相等`

V02 新增 `estimand_lock`，把这两条作为机器合同。

### P2-AUD-012 — 现有 Prospective Plan 尚未绑定新字段

这是当前唯一保持 `OPEN_BLOCKER` 的问题。

`K2PV-QRM-001` 是按 v0.1 生成的，尚未包含 V02 新增的：

- world-variable / symbol / feature hashes；
- complexity budgets；
- blinding；
- denominator policy；
- reproducibility fixture；
- seed policy 等。

因此即使 V02 protocol 已经补强，也不能直接创建 Batch。

当前必须保持：

`BATCH_READY = false`
`BATCH_GATE = BLOCKED_PENDING_PLAN_REPIN`

## 2. 本次自我修正的核心结论

旧判断：

`冻结用神 + 三 lane + bridge ablation = DESIGN_READY`

现在修正为：

`冻结用神只是必要条件，不是充分条件。`

真正可识别的 P2 对照至少需要：

`same reality`
`+ same Scenario Graph`
`+ same world variables`
`+ same symbol vocabulary`
`+ same feature extractor`
`+ same eligible rules`
`+ same prediction schema`
`+ same complexity budget`
`+ same interpreter/tool budget`
`+ same denominator cost`
`+ blind / isolated execution`
`+ deterministic generators`
`+ only-one-difference estimand lock`

之后才有资格讨论：

`Role Binding / Layer Priority 是否存在增量`

## 3. 为什么没有现在就 repin Plan

本轮刻意不把 `K2PV-QRM-001` 直接改成新的可执行 plan。

原因是：

1. 本轮的任务是先完成 adversarial audit 与 protocol hardening；
2. 旧 plan 必须作为“曾经认为足够、后来发现不够”的历史证据保留；
3. 先让 CI 对 `V01_NOT_BATCH_SAFE -> V02_HARDENED -> PLAN_REPIN_REQUIRED` 这条状态链做机器验收；
4. 下一笔提交再单独 repin prospective plan，避免把“发现漏洞”和“宣布漏洞已完全解决”压在同一个不可审计动作里。

## 4. 当前状态

```text
V01 PROTOCOL
= HISTORICAL
= DESIGN_READY_WAS_PREMATURE
= NOT_BATCH_SAFE

V02 PROTOCOL
= ADVERSARIAL_HARDENED
= EMPIRICAL_CREDIT_NONE

QRM-H1
= UNTESTED

CURRENT PLAN
= K2PV-QRM-001
= V0.1 SHELL

PLAN ALIGNMENT
= REPIN_REQUIRED

BATCH_READY
= false

BATCH
= NONE
FREEZE
= NONE
OUTCOME
= NONE

CLAIM EXTRACTION
= BLOCKED
```

这次关闭的是方法学漏洞，不是奇门理论真实性问题。
