# K2 Qimen P2 Role-Map Comparative Protocol v0.2

状态：`ADVERSARIAL_HARDENED / BATCH_BLOCKED / NO_FREEZE / NO_OUTCOME`

Hypothesis：`QRM-H1`
Current Plan Shell：`K2PV-QRM-001`
Empirical Credit：`NONE`
Claim Extraction：`BLOCKED`
Supersedes：`K2-QIMEN-P2-ROLE-MAP-COMPARATIVE-V01`

反向审计：`K2_QIMEN_P2_ROLE_MAP_ADVERSARIAL_AUDIT_V01`

## 0. v0.2 为什么不是简单“加更多规则”

v0.1 已经建立三 lane：

- `P2-A`：source-faithful role catalog + fixed global layer priority；
- `P2-A'`：topology-conditioned Role Binding + fixed global layer priority；
- `P2-B`：topology-conditioned Role Binding + topology-conditioned Layer Priority。

它也已经要求 Role/Layer Map 在 current plate values 之前冻结。

但 adversarial audit 发现：这还不足以保证 C1/C2 真正只比较 Role Binding 或 Layer Priority。

如果 Candidate 可以得到更多 world variables、更多 symbol features、更多 reasoning branches、更高 tool budget，或者通过 selective abstention 缩小分母，那么“胜出”仍然可能只是搜索空间更大。

v0.2 因此把研究对象从：

`哪条解释路径更会讲`

收窄为：

`在严格信息与复杂度等价条件下，只改变指定处理变量，是否仍有增量`

## 1. 来源基础不变

本 protocol 的 source-grounded anchors 继续来自：

- `QM-SRC-0003 / K2E-W1-QM-0003-0065`：固定全局优先级 `奇仪 -> 八门 -> 八神 -> 九星`；
- `QM-SRC-0003 / -0009 / -0063 / -0068`：证明 fixed-global 来源本身仍包含 domain-specific role catalog，不能造弱 baseline；
- `QM-SRC-0021 / -0239 / -0327 / -0330`：证明问题域角色结构、动态 mapping 与 competing mapping 确实存在。

这些只提供候选方法来源，不提供现实准确率信用。

## 2. 三条 lane 的模型身份保持不变

### P2-A

`GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01`

- Role Binding：`SOURCE_CATALOG_DOMAIN_SELECTION_ONLY`
- Layer Priority：固定 `奇仪 -> 八门 -> 八神 -> 九星`

### P2-A'

`GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01`

- Role Binding：`QUESTION_TOPOLOGY_CONDITIONED`
- Layer Priority：仍固定 `奇仪 -> 八门 -> 八神 -> 九星`

### P2-B

`TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01`

- Role Binding：`QUESTION_TOPOLOGY_CONDITIONED`
- Layer Priority：`QUESTION_TOPOLOGY_CONDITIONED`

模型名字没有在本轮升级，因为本轮改变的是**实验识别与执行公平性合同**，不是这些 lane 的符号逻辑本身。

## 3. Estimand Lock

### P2-C1

`A' - A`

唯一允许不同：

`ROLE_BINDING_POLICY`

其余信息、feature、规则、预算、输出与评分必须相等。

### P2-C2

`B - A'`

唯一允许不同：

`LAYER_PRIORITY_POLICY`

其余必须相等。

### P2-C3

`B - A`

只表示：

`ROLE_BINDING + LAYER_PRIORITY full bundle`

禁止拿 C3 单独给任一组件授信。

## 4. Mapping Boundary

顺序仍然是：

`Question/Reality`
`-> Scenario Graph`
`-> world_variable_manifest`
`-> three Role/Layer Maps FREEZE`
`-> current plate values`
`-> same feature extraction`
`-> same eligible rules`
`-> isolated predictions`
`-> unblind`
`-> future Outcome`

映射阶段明确禁止：

- current plate symbol values；
- 当前盘旺衰/吉凶；
- prediction；
- Outcome / feedback；
- 未注册外应；
- 其它 lane 的任何中间输出。

## 5. Representation Parity

三 lane 必须共享并在未来 Batch freeze：

- `world_variable_manifest_hash`
- `symbol_vocabulary_hash`
- `feature_extraction_manifest_hash`
- `eligible_rule_pool_hash`
- `prediction_schema_hash`
- prediction cardinality
- confidence scale
- output granularity

任何 lane 不得增加自己的 world variable、symbol vocabulary 或专属 feature。

## 6. Layer Priority 的精确定义

v0.2 明确：

`Layer Priority = aggregation policy`

它不是：

- feature visibility switch；
- rule eligibility switch；
- early-stop permission；
- per-layer extraction-depth budget。

因此所有 lane 都必须完整可见：

`奇仪 / 八门 / 八神 / 九星`

且使用同一 feature extraction depth。

P2-B 只能在 current plate values 可见前，由冻结 topology generator 决定 aggregation priority。

## 7. Complexity Budget

为了避免 Candidate 通过更大搜索树获利，未来 Batch 必须等额冻结：

- role multiplicity budget；
- competing mapping count；
- reasoning branch budget；
- rule trace budget；
- interpreter information budget；
- tool access budget。

并逐 case 记录：

- bound_role_count；
- competing_mapping_count；
- active_rule_count；
- feature_count；
- reasoning_branch_count；
- rule_trace_count。

Candidate 不得使用 shared catalog 之外的新角色，也不得拥有额外 eligible rules。

## 8. Blinding / Isolation

执行时：

- interpreter 只看到 neutral lane labels；
- 不告诉 interpreter 哪条是 Candidate；
- 不暴露 QRM-H1 的期待方向；
- lane 顺序由 freeze 的 seed 决定；
- 不允许跨 lane 中间推理共享；
- 三条 prediction 全部冻结后才允许 unblind。

如果使用 LLM interpreter，同一 case 的三 lane 还必须共享同一 raw input manifest 与预算。

## 9. Denominator / Abstention

case inclusion 必须在任何 lane 执行之前冻结。

禁止：

- Candidate 单独排除难例；
- ABSTAIN 后把 case 从 denominator 静默删除；
- Outcome 后重新定义 UNEVALUABLE。

未来 Batch 必须冻结：

- `primary_denominator_policy`
- `abstention_scoring_policy`
- `technical_unevaluable_policy`

并至少同时报告 coverage-penalized metric。

## 10. Determinism

future Batch 之前必须：

- mapping generator version + hash；
- layer-priority generator version + hash；
- nondeterminism seed freeze；
- synthetic reproducibility fixture freeze；
- 同输入同 lane 重跑得到完全相同 Role/Layer Map。

如果做不到，不能把跨解读者差异解释为理论差异。

## 11. 当前 Plan Alignment Blocker

现有 `K2PV-QRM-001` 是 v0.1 plan shell。

它尚未绑定 v0.2 新增的 parity / complexity / blinding / denominator / determinism freeze fields。

所以当前：

`BATCH_READY = false`
`BATCH_GATE = BLOCKED_PENDING_PLAN_REPIN`

V02 validator 必须拒绝任何在 repin 前创建的 `K2PV-QRM-001` Batch。

下一阶段只能先产生新的 prospective plan identity/version，再重新审计。

## 12. 当前非主张

```text
QRM-H1 = UNTESTED
P2-A = UNVALIDATED
P2-A' = UNVALIDATED
P2-B = UNVALIDATED
BATCH = NONE
FREEZE = NONE
OUTCOME = NONE
EMPIRICAL_CREDIT = NONE
CLAIM_EXTRACTION = BLOCKED
```

`ADVERSARIAL_HARDENED` 只表示方法合同比 v0.1 更难被事后自由度钻空子，不表示任何奇门规则获得现实信用。
