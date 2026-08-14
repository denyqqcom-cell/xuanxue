# 玄学排盘（xuanxue）

一个以**本地计算、可验证算法、隐私优先、低权限**为核心原则的 Android 玄学排盘项目。

当前 App 已实现紫微斗数排盘；奇门遁甲、八字命理、六爻、大六壬已经纳入统一 App 架构。新增模块不会在算法与资料没有验证完成前伪装成“可用”。

## App 模块

- 紫微斗数：已接入 `ziwei-core`，支持十二宫、主星、辅星、杂曜、大限与小限；核心结果通过 iztro 黄金夹具验证。
- 奇门遁甲：已进入 App 主架构；本地资料完成起局、用神、宫盘、生克、应期与流派差异整理后实现 `qimen-core`。
- 八字命理：已进入 App 主架构；本地资料完成排盘、旺衰、格局、十神、大运流年与流派差异整理后实现 `bazi-core`。
- 六爻：已进入 App 主架构；待整理起卦、装卦、纳甲、六亲、世应、动变、用神与应期规则后实现 `liuyao-core`。
- 大六壬：已进入 App 主架构；待整理月将、天地盘、四课、三传、天将、课体与断课规则后实现 `liuren-core`。

## UI/UX v2

新版界面在 `uiux-v2` 分支开发，设计原则是：

- 现代东方视觉，而不是仿古模板堆叠
- 五门术数使用统一导航与设计系统，各自保留独立核心模型
- 排盘摘要与详细信息分层显示
- 不使用第三方图片、商业字体、商业 App 截图或视觉素材
- UI 与各 core module 分离，界面重构不得改变排盘算法

## 技术栈

- Kotlin 2.0 + Jetpack Compose + Material 3
- Java 17
- Android minSdk 24 / targetSdk 35
- `ziwei-core`：iztro（MIT）到 Kotlin 的移植
- `cn.6tail:lunar`：农历/干支/节气基础（MIT）

## 构建

```bash
export JAVA_HOME=/path/to/jdk17
export ANDROID_HOME=/path/to/android-sdk
./gradlew :ziwei-core:test
./gradlew :app:assembleDebug
```

APK 输出：`app/build/outputs/apk/debug/app-debug.apk`

## 正确性验证

`ziwei-core` 通过黄金夹具与 iztro 原版逐字段对照。当前夹具覆盖阳男午时、阴女子时、闰月、晚子时、立春边界、现代儿童与深冬等边界场景。

后续 `qimen-core`、`bazi-core`、`liuyao-core`、`liuren-core` 也必须先建立可复现 fixture，再允许首页状态从“资料准备”改成“可用”。

## 本地资料如何进入工程

本地书籍不直接进入 App。能访问本机资料的 AI 应先按照 [`LOCAL_CORPUS_HANDOFF_PROMPT.md`](LOCAL_CORPUS_HANDOFF_PROMPT.md) 生成结构化交接包，至少拆分：

- 可编码排盘/起局算法
- 流派差异与冲突
- 经验断法
- 可复现黄金夹具
- 回溯/半盲/真盲案例
- 版权与许可状态

只有通过来源审计、交叉验证和版权 Gate 的规则，才允许进入正式 core module。

## 版权与开源许可

本项目自有代码采用 MIT License。第三方许可与来源见：

- `NOTICE`
- `THIRD_PARTY_NOTICES.md`
- `COPYRIGHT_REVIEW.md`
- `app/src/main/assets/licenses/`（随 APK 打包）

新版 UI/UX 为独立设计，不复制商业命理 App 的代码、视觉素材、截图、字体或长段文案。

研究资料方面，已出版扫描书不进入 Git；仓库只保留书目与研究笔记。研究笔记仍需遵守“以总结和验证为主、不大段照录原文”的版权规则，具体见 `COPYRIGHT_REVIEW.md`。

## 学习资料

总索引见 `资料总目.md`。奇门、八字、紫微、风水分别位于仓库同名目录中。六爻与大六壬的本地资料在完成盘点后再建立对应研究目录，不提前伪造资料完整度。
