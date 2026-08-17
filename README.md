# 玄学工具箱（xuanxue）

一个以 **本地计算、证据分级、资料可追溯、具体事体优先** 为核心的 Android 术数工具箱。

当前 App 不要求账号，不包含广告、支付、推送或自有服务器；Android Manifest 也没有网络权限。
“离线解释”只整理本机输入与排盘结果，并把工程核验成熟度、来源索引和未解决边界一起展示。

## 当前模块

- **紫微斗数**：十二宫、主辅杂曜、亮度、四化、长生/博士/岁前/将前、大限与小限。Kotlin 核心用 7 组 fixture 与 iztro 原版做实现一致性比对。
- **八字**：四柱、藏干、十神、纳音、大运等本地结构。历法基础来自 lunar-java；当前离线解释不再用“单一十二运”直接判身强弱或喜忌。
- **奇门遁甲**：当前 main 引擎能生成转盘时家九宫，但 **完整九宫仍按实验能力管理**。`handoff/qimen` 已整理 17 条历法/表/映射 fixture，却没有完整九宫黄金盘；地盘走法和人盘方向仍有冲突，App 会明确显示这一状态。
- **六爻**：纳甲、八宫、世应、六亲、六神、动爻与变卦；已有内部回归，后续仍需建立多来源 corpus/conflicts/copyright gate。
- **大六壬**：月将加时、天地盘、四课、九宗门、三传与十二天将；已有部分书例/内部回归，但尚未达到奇门 handoff 同等级的多来源审计。
- **黄历**：宜忌、吉神凶煞、彭祖百忌、冲煞等字段由 lunar-java 本地计算并组织展示。

## 为什么有“方法核验中心”

这个项目不把下面三件事混为一谈：

1. **实现一致性**：例如 Kotlin 紫微输出是否与 iztro fixture 一致；
2. **资料/课例可追溯**：规则或案例是否有明确来源与冲突记录；
3. **传统解释**：星曜、用神、课型、吉凶等术数推演。

App 首页直接显示每个模块的工程成熟度，并提供“方法核验中心”。离线解读卡同时显示 evidence grade、source IDs 与 caveats。测试通过不被包装成“预测准确率已验证”。

## 事体优先：不再只凭盘面标签自动断

奇门、六爻、大六壬现在有统一 `ReadingContext`：

- 问题领域；
- 用户真正要问的具体问题；
- 已知现实条件。

UI 会把这些内容与排盘结果分开显示，并标记为 **用户输入**，不会把用户提供的事实当成术数证据。

如果没有具体事体，解释层停在 **Structure（结构）**：只整理盘/卦/课字段，不自动选用神或类神，也不输出成败与应期。后续要进入 Selection / Interpretation，必须由对应模块 handoff 给出带事体条件、流派、来源和 fixture 的规则。

这也是对早期机械解盘方式的纠偏：

- 不再“看到某门/星/六亲/课型 → 直接现实结论”；
- 不用一个局部指标替代整套旺衰/取用逻辑；
- 不把已知答案后的复盘解释当作预测准确率。

## XuanxueAI：离线解释层

`com.xuanxue.ai.XuanxueAI` 是 provider-neutral 的解释编排层，目前 **零网络**。

第一版离线规则库曾存在过度机械解释的问题：例如只凭日柱十二运判断八字身强弱，或在奇门完整九宫尚没有黄金夹具时继续输出八门吉凶。本轮已纠偏：

- 八字：先展示四柱、五行显示权重、十神结构、大运时间线；身强弱等待月令/根气/透藏/制化规则与夹具成熟后再开放。
- 紫微：把主星、亮度、四化先作为盘面字段，不直接翻译成人格或确定事件。
- 奇门：只把历法、局、旬首旬空等已工程化层作为基础；完整九宫继续显示为实验开发视图，不据此自动断成败、吉凶或应期。
- 六爻/六壬：先展示结构；具体取用必须结合用户事体，不从一个标签自动下定论。
- 黄历：明确属于传统历法/民俗字段，不作为科学因果预测。

未来如增加 BYOK 云端 AI，必须复用同一份结构化 evidence，并先完成本次数据预览、目标授权、凭据存储和网络层审计；当前版本尚未启用。

## UI / 响应式体验

App 不再用一行 Tab 塞六个模块，改为首页卡片式入口：

- 手机：单列模块卡片；
- 较宽窗口/平板：自动切换双列卡片；
- 模块内容限制最大阅读宽度，避免平板上整页被拉得过宽；
- 紫微、八字、奇门、六壬的时辰入口支持横向滚动；
- 六爻补齐了时间起卦的时辰选择，数字输入在窄屏改为纵向排列。

## Knowledge Engine v1

知识工程已进入 `K1_CORPUS_INDEX`。六个正式术数域统一治理：

- 紫微 `ziwei`
- 八字 `bazi`
- 奇门 `qimen`
- 六爻 `liuyao`
- 大六壬 `liuren`
- 风水 `fengshui`

黄历作为公共历法/民俗工具，不作为第七个知识域。

Knowledge Engine 使用统一的 Source / Evidence / Claim / School / Conflict / Fixture / Case 协议与 L0-L8 成熟度模型。当前 K1 本地盘点已经收到报告级结果，但项目端发现全局文件会计仍需核对，且本地私有 intake 尚未通过机器 validator，因此 **K2 Claim Extraction 仍被硬锁**。

当前 K1 项目端验收见：

- `knowledge/K1_ACCEPTANCE.md`
- `tools/validate_k1_intake.py`
- `LOCAL_CORPUS_K1_REMEDIATION_PROMPT.md`

其中一个重要纠偏是：**“资料少”不等于 K1 Source Index 失败。** K1 只判断本地可发现资料是否被诚实发现、去重和索引；资料丰富度、可读性和跨来源能力属于下一阶段 readiness/maturity 问题。不能为了让六个域都显示 PASS 而人为增加来源。

## 资料工程

仓库包含学习笔记、来源索引、冲突记录和工程 handoff。它们是研发材料，不等于 App 运行时内容。

`handoff/README.md` 定义统一标准：每个新模块必须分开交付 corpus manifest、system map、algorithm spec、rules、conflicts、fixtures、cases、copyright gate、implementation handoff 和 open questions。

奇门已建立第一套较完整工程交接，但仍不是“全书已经验证完成”。紫微、八字、六爻、大六壬、风水现在统一进入 Knowledge Engine，而不是继续各自走不同的学习标准。

本地 `knowledge-intake/` 已被 `.gitignore` 排除；真实盘符、用户名、本机绝对路径和本地审计总账不得直接进入公开 Git。只有经过 sanitize 后的派生 registry 才能进入 `knowledge/`。

## 版权与发行边界

项目自身代码采用 MIT License。第三方软件许可与权利人单独列在：

- `NOTICE`
- `THIRD_PARTY_NOTICES.md`
- `app/src/main/assets/licenses/`

术数研究资料执行额外 corpus gate：现代出版物扫描件、OCR 全文、现代书籍长段文字、独创图解、未知许可视觉素材不会进入 App 发行包。古籍原典与现代校注/翻译/排版也分开判断。

CI 现在有两层发行检查：

1. **源码 Gate**：许可文本、权利人声明、Manifest 网络权限、未经审查的 `assets/`；
2. **APK 二进制 Gate**：编译完成后直接扫描 APK，阻止 PDF/EPUB/DOC/字体、研究目录、全文/OCR/scan 痕迹和未经批准的 assets 被意外打进发行包。

Knowledge Engine 另有自己的 CI：六域 schema、状态一致性、K1 intake validator 合同测试、研究二进制边界及稳定 core regression。

完整工程审计见 `COPYRIGHT_REVIEW.md`。这是一套工程合规措施，不构成法律意见。

## 技术栈

- Kotlin 2.0
- Jetpack Compose / Material 3
- Java / JVM 17
- compileSdk 35 / targetSdk 35 / minSdk 24
- `cn.6tail:lunar:1.7.7`
- `ziwei-core`：当前承载紫微、八字、奇门、六爻、六壬及离线解释层

## 构建与验证

```bash
export JAVA_HOME=/path/to/jdk17
export ANDROID_HOME=/path/to/android-sdk

./gradlew --no-daemon :ziwei-core:test
./gradlew --no-daemon :app:assembleDebug
bash tools/audit_apk_contents.sh app/build/outputs/apk/debug/app-debug.apk
python3 tools/validate_knowledge.py
python3 tools/test_validate_k1_intake.py
```

Debug APK：

```text
app/build/outputs/apk/debug/app-debug.apk
```

稳定 App 与 Knowledge Engine 使用独立 Gate。知识分支不能因为研究资料增加而降低现有 V1.0 的核心测试、隐私或版权边界。
