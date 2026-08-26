# LOCAL AI PROMPT — K2 Source Lineage

> 本文件保留 K2A 初始协议作为历史入口。当前项目端已发现 `SAME_WORK_VARIANT` 与互补卷册/分页混用的问题。实际执行请改读并严格遵守：
>
> `LOCAL_CORPUS_K2_LINEAGE_COVERAGE_REMEDIATION_PROMPT.md`
>
> 在 coverage remediation 完成并经项目端复验前，严禁开始 Evidence / Claim Extraction。

K1 已由项目端正式关闭。K2 当前阶段仍为 `K2_SOURCE_LINEAGE`，`claim_extraction_blocked=true`。

初始 K2A 的目标仍然有效：对 515 条 canonical source 建立 underlying work / edition / commentary / note / implementation 谱系，防止不同载体、笔记和代码被重复计算为独立证据。

但第一版 relation 模型已被升级：

- `PRIMARY_WORK` 仅用于完整 work carrier；
- `WORK_PART` 用于互补卷/册/篇/分页，并保持 `k2_eligible=true`；
- `SAME_WORK_VARIANT` 只表示相同 coverage 的另一载体，必须有 `variant_of_source_id`；
- out-of-scope code 仍保持 `IMPLEMENTATION` source role，而不是伪装成 textual `OUT_OF_SCOPE`。

请不要使用本文件旧版本中的“上中下册可直接归 SAME_WORK_VARIANT”类含混规则。以仓库中的：

- `knowledge/K2_SOURCE_LINEAGE_PROTOCOL.md`
- `knowledge/K2_LINEAGE_PROJECT_REVIEW.md`
- `LOCAL_CORPUS_K2_LINEAGE_COVERAGE_REMEDIATION_PROMPT.md`
- `tools/validate_k2_source_lineage.py`

为当前正式真值。
