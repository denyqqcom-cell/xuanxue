# QCIC v0.6 Machine Gate Closure

状态：IMPLEMENTED_PENDING_CI  
阶段：K2B / Deep Closure  
Claim Extraction：BLOCKED  
Empirical credit：NONE

## 1. 为什么需要这一层

QCIC v0.6 已经在方法文档中提出两个新约束：

1. Source Stance Registry：区分来源“转述、认可、否定、存疑”；
2. Enumeration Compression Gate：把可由同一生成机制展开的大量定局表从“证据数量”中折叠出去。

如果这两个约束只停留在 Markdown，它们仍然可能在后续知识工程中被绕过。因此本轮把它们下沉为 schema、registry、validator、fail-closed tests 和独立 GitHub Actions gate。

## 2. Source Stance 的机器化边界

新增：

- `knowledge/schema/source_stance.schema.json`
- `knowledge/K2_SOURCE_STANCE_PROTOCOL.md`
- `knowledge/K2_SOURCE_STANCE_REGISTRY.jsonl`
- `tools/validate_k2_source_stance.py`
- `tools/test_k2_source_stance.py`

validator 绑定 effective lineage，而不是只相信历史 raw lineage；同时要求 COMPLETE VISUAL_PAGE deep reading 与合法 PDF locator。

硬门：

- `SOURCE_REPORTS / SOURCE_REJECTS / SOURCE_UNCERTAIN` 不能进入 `author_method_pool_eligible=true`；
- 所有 stance 的 `empirical_credit` 固定为 `NONE`；
- supersession 只能发生在同 source、同 topic，且 precedence 必须严格升高。

QM-SRC-0017 首批四条 stance：

- 神化起源：REJECTS；
- 偶然外应/动应：REJECTS；
- 符咒：REJECTS；
- 剩余时空数理部分的科学性程度：UNCERTAIN。

这不是项目替作者作价值判断，而是保存完整阅读中可以直接定位的作者文本立场。

## 3. Enumeration Compression 的机器化边界

新增：

- `knowledge/schema/enumeration_compression.schema.json`
- `knowledge/K2_ENUMERATION_COMPRESSION_PROTOCOL.md`
- `knowledge/K2_ENUMERATION_COMPRESSION_REGISTRY.jsonl`
- `tools/validate_k2_enumeration_compression.py`
- `tools/test_k2_enumeration_compression.py`

硬门：

- `collapsed_structure_units = 1`；
- `empirical_evidence_units = 0`；
- `compression_policy = DERIVED_ENUMERATION_COLLAPSE`；
- `source_credit = SOURCE_STRUCTURE_ONLY`；
- `empirical_credit = NONE`。

QM-SRC-0017 当前登记：

- 时家阳遁540 + 阴遁540 = 1080 enumerated entries，折叠为1个 source-structure unit；
- 日家阳遁60 + 阴遁60 = 120 enumerated entries，折叠为1个 source-structure unit。

二者 `reconstruction_test_status` 都保持 `UNTESTED`。这很重要：本轮只是关闭“条目数量伪装成证据数量”的漏洞，没有虚报排盘重建算法已经完成。

## 4. CI

新增独立 workflow：

`.github/workflows/k2-qcic-v06-gates.yml`

包含四个硬步骤：

1. source stance fail-closed tests；
2. source stance registry validator；
3. enumeration compression fail-closed tests；
4. enumeration compression registry validator。

同时修改既有 `tools/test_knowledge_ci_contract.py`，要求这个 workflow、两个 schema 和两个 registry 必须存在，因此主 Knowledge Engine CI 也会监督新 gate 是否被删除或绕过。

## 5. 本轮自我反省

这次没有继续增加新的奇门解释规则，而是把上一轮发现的两个认知错误变成系统级禁止项：

- “书里出现过”不能再自动变成“作者认可”；
- “书里列了很多局”不能再自动变成“有很多独立证据”。

这比继续堆积口诀更重要，因为知识库越大，如果不控制 source stance 和 derived enumeration，后续模型反而会获得更多事后选择空间。

## 6. Closure criteria

本文件只有在对应提交的：

- 主 Knowledge Engine CI；
- K2 QCIC v0.6 Machine Gates；

均成功后，才允许从 `IMPLEMENTED_PENDING_CI` 解释为工程闭环完成。

即使 CI 全绿，仍然只是：

`machine_control_credit = IMPLEMENTED`

不是：

`empirical_credit = VALIDATED`
