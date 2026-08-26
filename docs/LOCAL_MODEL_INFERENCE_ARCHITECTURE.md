# 手机本地模型解释层架构

状态：PHASE-1 CONTRACT / BACKEND_UNVERIFIED  
目标设备：Moto X30 Pro  
目标模型：用户设备中现有的“Gemma 4 2B”（实际模型标识、文件格式、量化方式与运行后端尚待设备侧重新核验）

## 1. 目标

把手机现有本地语言模型接入玄学排盘 App，但只作为**受控解释层**，不让生成模型接管排盘算法、来源证据或知识状态。

固定调用链：

`用户输入 -> 确定性 Engine -> XuanxueAI/Reading -> LocalInferencePacket -> LocalModelProvider -> 本地模型文字输出`

禁止反向链：

`本地模型 -> 重算/修改 QimenEngine -> 改写 Evidence/Claim -> 写入知识库`

## 2. 为什么不能把模型直接塞进 QimenEngine

`QimenEngine` 的职责是可重复的历法/排盘计算；语言模型具有采样、上下文依赖和幻觉风险。两者混在一起会让“盘面事实”和“模型推演”失去可审计边界。

因此：

- 排盘结果对模型是 immutable input；
- 模型输出永远标为实验性解释；
- 模型不能提高 `EvidenceGrade`；
- 模型不能生成新的 source id；
- 模型不能因为流畅表达而获得 Claim 或 empirical credit。

## 3. 2B 模型的正确工作量

2B 级本地模型第一阶段不承担“读完整知识库并自主决定用哪本书”的工作。输入应保持小而结构化，只提供：

1. `ReadingContext`：问题域、具体问题、现实已知条件；
2. 确定性排盘后经过 `XuanxueAI` 整理的 Reading；
3. 每条 Reading 的证据等级和已存在 source ids；
4. 当前核验 caveats；
5. 固定的不可越权约束。

这样本地模型的任务是“组织、比较候选解释、指出不确定性”，不是自由检索几千页术数资料。

## 4. Provider contract

core 模块只认识 `LocalModelProvider`：

- `descriptor`：模型 id、显示名、backend、localOnly 与非敏感 metadata；
- `availability()`：UNAVAILABLE / READY / BUSY / ERROR；
- `generate(request)`：消费 `LocalModelRequest`，返回 Success / Unavailable / Failure。

core 不依赖 Android、LiteRT、MediaPipe、llama.cpp 或任何特定 Gemma SDK。

## 5. Android backend 的两种允许实现

### A. 已有本地模型服务/系统接口

如果 Moto X30 Pro 上现有 AI 应用或系统组件提供稳定、可授权的 Binder/AIDL、ContentProvider、SDK 或 localhost 推理 API，优先做薄 adapter。

优点：

- 不重复占用数 GB 模型空间；
- 模型更新由原运行环境管理；
- Xuanxue APK 保持轻量。

前提：接口必须真实存在并可被第三方 App 调用。**不能通过自动点击另一个 App UI 来伪装成模型 API。**

### B. App 内本地推理

如果现有模型只是另一 App 私有 sandbox 文件、没有可调用服务，则 Xuanxue App 无法合法直接读取该私有模型。此时只能：

- 用户明确提供一份可访问的模型文件；或
- 使用官方/兼容的设备端推理 runtime 加载用户选择的本地模型。

模型文件不进入 Git，不打包进 APK。

## 6. 当前不做的事情

在设备 backend 未核验前，Phase 1 明确不做：

- 不添加 INTERNET 权限；
- 不添加任何 Gemma/LiteRT/MediaPipe/llama.cpp dependency；
- 不硬编码 `/sdcard/...` 或其他模型路径；
- 不假设“Gemma 4 2B”就是某个公开发行模型的正式 model id；
- 不把模型复制进仓库或 APK；
- 不让模型访问 raw Evidence/Claim 文件并自由选规则；
- 不加入自动 fallback 到云端模型。

当前 Manifest 继续维持无网络权限。

## 7. 奇门调用策略

第一版只接奇门，且只在已经生成 `QimenChart` 后允许调用：

1. `QimenEngine.bySolar(...)` 生成确定性/实验盘结构；
2. `XuanxueAI.qimen(chart, context)` 生成受控 Reading；
3. `LocalModelPromptCompiler.forReading(reading, context)` 生成输入包；
4. Android adapter 调 `LocalModelProvider.generate()`；
5. UI 单独显示“本地 AI · 实验解释”，同时显示 model/backend；
6. 原来的 `ReadingCard` 永远保留，模型不可覆盖它。

如果问题不具体、模型不可用、推理失败或输出为空，必须 fail closed：继续展示确定性 Reading，不伪造 AI 结果。

## 8. Prompt 的 epistemic contract

输入中必须明确：

- 盘面不可重新计算；
- USER_CONTEXT 不提升证据；
- EvidenceGrade != truth probability；
- experimental/caveat 字段不得升级；
- 未提供的古籍规则/source id 不得补造；
- 输出分离“盘面事实 / 来源候选 / 模型推演 / 不确定性”；
- 无法区分竞争解释时允许 abstain。

这与项目现有 QCIC / SCRM 原则一致：模型的语言能力服务于情境推演，不绕过证据边界。

## 9. Moto X30 Pro backend discovery 清单

连接器恢复后由主 Agent直接检查，不交给本地资料助手：

1. 设备中实际模型名称、版本、大小、量化/容器格式；
2. 模型由哪个 package/process 持有；
3. 是否有 exported service / provider / Binder / SDK / localhost endpoint；
4. 若有服务，其调用权限、输入输出 schema、并发和上下文窗口；
5. 若没有服务，模型文件是否有用户可授权读取的副本；
6. NPU/GPU/CPU backend、首 token 延迟、持续 tokens/s、峰值内存；
7. 后台/锁屏行为和热管理；
8. 断网条件下完整调用验证。

这些事实确认后，才选择具体 Android adapter。

## 10. 验收顺序

Phase 1：provider-neutral contract + prompt compiler + JVM unit tests。  
Phase 2：Moto backend discovery + Android adapter + fake-provider UI test。  
Phase 3：真机离线 smoke：同一盘、同一问题、固定参数，多次调用检查输入未变、来源不伪造、失败可回退。  
Phase 4：再考虑八字/六爻/六壬复用，不在第一版扩大范围。

任何模型质量测试都不能转化为术理 empirical credit。
