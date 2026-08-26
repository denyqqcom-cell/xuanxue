# DEPRECATED — LOCAL CORPUS K2B Wave 1 Helper Prompt

此文件保留仅用于历史 provenance。

**不要再把下面旧职责作为当前本地助手权限。** 当前权威提示词是：

- `LOCAL_HELPER_CURRENT_PROMPT.md`
- `LOCAL_AI_EXECUTION_BOUNDARY.json`

当前本地助手固定为 `EXECUTION_HELPER_ONLY`，只允许：

1. GitHub → 本地的只读状态检查、fetch，以及 tracked clean 前提下的 `merge --ff-only`；
2. 本地资料定位、canonical SHA256 / 页数 / packet 完整性校验，以及主 Agent 明确点名的单文件发布。

当前明确禁止本地助手：

- 写代码或修改 tracked 文件；
- 运行任何项目测试、Gradle、instrumentation、physical-device acceptance；
- ADB/手机操作；
- 安装依赖；
- 修改 `knowledge/`；
- 写 Evidence / Claim / Reading Ledger / lineage / distillate；
- commit / push / reset / stash / clean；
- 删除未跟踪文件。

旧版 Wave1 prompt 曾授权本地助手运行 extractor、测试和 Gradle；该授权已被项目主 Agent 撤销，不能继续引用为当前执行权限。

如需本地助手执行任务，请复制 `LOCAL_HELPER_CURRENT_PROMPT.md` 并附上主 Agent 本轮点名的 source / SHA / remote HEAD。
