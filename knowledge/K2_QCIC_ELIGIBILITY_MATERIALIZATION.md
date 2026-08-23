# QCIC v0.6 Inference Eligibility Materialization

状态：IMPLEMENTED_PENDING_CI  
阶段：K2B / Deep Closure  
Claim Extraction：BLOCKED  
Empirical credit：NONE

## 1. 为什么还要多一层

Source Stance Registry 和 Enumeration Compression Registry 已经能够阻止两类错误：

- “书里写过”被误当成“作者认可”；
- “表项很多”被误当成“独立证据很多”。

但如果未来的推演、Claim extraction 或检索消费者直接绕过这两个 registry，重新从原始蒸馏或全文条目取数，上述控制仍可能只存在于校验层，而没有进入实际消费路径。

因此本轮新增一个**确定性生成、不可手工漂移的下游 eligibility view**：

`knowledge/K2_QCIC_INFERENCE_ELIGIBILITY_VIEW.json`

它不是新的知识来源，而是从三个受控输入物化出来：

1. `K2_QCIC_V06_GATE_STATE.json`；
2. `K2_SOURCE_STANCE_REGISTRY.jsonl`；
3. `K2_ENUMERATION_COMPRESSION_REGISTRY.jsonl`。

## 2. Source Stance 必须先解析成唯一 effective leaf

此前 stance validator 已经验证 supersedes 的 source/topic 和 precedence，但仍存在一个隐藏漏洞：同一个 `source_id + topic_key` 可以出现两条都没有被 supersede 的合法记录。

每条记录单看都正确，下游却不知道该采用哪一条。

本轮补上硬约束：

> 每个 `source_id + topic_key` 必须恰好只有一个未被 supersede 的 effective stance leaf。

如果有两个 leaf，registry 直接 fail closed；不能让下游自行选择较顺眼的一条。

这实际上把 Source Stance 从“记录集合”升级成了可确定求值的状态机。

## 3. Enumeration 也要防止结构单元重复计数

原 validator 已阻止重复 label，但还可能出现：

- 两条不同 label；
- 却使用同一个 `source_id + generative_rule_id`。

如果下游把两条都各算一个 `collapsed_structure_units=1`，同一个生成机制又会被重复计算。

因此新增：

> `source_id + generative_rule_id` 必须唯一。

若同一生成机制跨多个页面区间，应在同一 compression row 中表达，而不是拆成多条来增加 structure unit。

## 4. Materialized eligibility view

新增：

- `knowledge/schema/qcic_inference_eligibility_view.schema.json`
- `tools/generate_k2_qcic_eligibility_view.py`
- `tools/validate_k2_qcic_eligibility_view.py`
- `tools/test_k2_qcic_eligibility_view.py`
- `knowledge/K2_QCIC_INFERENCE_ELIGIBILITY_VIEW.json`

生成器首先重新执行 stance / enumeration 的真实 validator 和 coverage state，再生成 view。输入不合法时不会输出“尽力而为”的结果。

### stance topic 的下游状态

当前映射为：

- `SOURCE_ENDORSES + author_method_pool_eligible=true`
  -> `ALLOW_SOURCE_LOCAL_CANDIDATE`
- `SOURCE_ENDORSES + author_method_pool_eligible=false`
  -> `EXCLUDE_NOT_AUTHOR_METHOD_POOL`
- `SOURCE_REPORTS`
  -> `EXCLUDE_SOURCE_REPORTS_ONLY`
- `SOURCE_REJECTS`
  -> `EXCLUDE_SOURCE_REJECTED`
- `SOURCE_UNCERTAIN`
  -> `HOLD_SOURCE_UNCERTAIN`

注意：`ALLOW_SOURCE_LOCAL_CANDIDATE` 也只表示“可以作为作者本地方法候选”，不是现实有效、不是 Claim、不是 empirical validation。

### enumeration 的下游状态

- reconstruction PASS -> `STRUCTURE_ONLY_RECONSTRUCTION_PASS`
- reconstruction UNTESTED -> `STRUCTURE_ONLY_RECONSTRUCTION_UNTESTED`
- reconstruction FAIL -> `HOLD_STRUCTURE_RECONSTRUCTION_FAILED`

无论哪一种：

`empirical_evidence_units = 0`

而且当前全局：

`claim_eligible = false`

## 5. 当前物化结果

当前 gate state 覆盖 QM0015、QM0017、QM0019。

物化结果中：

- 9 个 effective stance topics；
- 0 个 author-method candidates；
- QM0017 的 1200 个枚举条目被保持为 2 个 structure units；
- empirical evidence units 仍为 0；
- 所有 topic / enumeration 的 `claim_eligible=false`。

这不是说三本书“没有价值”，而是说明目前登记进 Source Stance 的内容全部是边界、批判、存疑或元方法信息，并没有被偷换成已验证预测规则。

## 6. Generated-file stale gate

`validate_k2_qcic_eligibility_view.py` 会重新生成期望内容，并与仓库中的 materialized JSON 做字节级比较。

所以如果未来：

- stance precedence 改变；
- 新增/删除 stance；
- enumeration 被重构；
- gate target 改变；

却没有重新生成 eligibility view，CI 必须失败。

这避免了一个常见知识工程问题：源 registry 已修正，但下游缓存仍悄悄使用旧结论。

## 7. CI

`K2 QCIC v0.6 Machine Gates` 新增：

1. `test_k2_qcic_eligibility_view.py`；
2. `validate_k2_qcic_eligibility_view.py`。

同时 `test_knowledge_ci_contract.py` 要求：

- dedicated workflow 必须实际调用这两个 gate；
- schema、generator、validator 和 materialized view 必须存在。

## 8. 本轮自我反省

本轮又发现一个典型误区：

> “上游已经有正确规则”并不等于“下游一定会使用正确规则”。

如果没有唯一 effective stance、没有唯一 generative mechanism、没有 materialized consumer view，后续模型仍可以绕过约束，重新获得选择自由度。

所以知识工程的闭环不能止于：

`我知道这条规则应该怎么处理`

而要继续变成：

`任何下游如果不用这个处理结果，就不能通过 gate`

这才是真正把自我反省转成系统能力。

## 9. 状态边界

即使对应 CI 全部通过，也只允许写：

`QCIC_ELIGIBILITY_MATERIALIZATION = ENGINEERING_ACCEPTED`

仍然不允许写：

`QIMEN_RULES_VALIDATED`

`EMPIRICAL_CREDIT_GRANTED`

`CLAIM_EXTRACTION_OPEN`
