# Third-Party Notices

本文件记录 xuanxue 当前使用或参考的第三方软件。第三方权利人与项目自身版权分开陈述；
Android 发行包所需的完整许可文本同时打包在 `app/src/main/assets/licenses/` 中。仅用于仓库外
研究/构建辅助且不进入 APK/AAB 的依赖，在对应条目中单独说明其分发边界。

## iztro

- Project: https://github.com/SylarLong/iztro
- License: MIT
- Copyright: Copyright (c) 2023 All Contributors
- Usage: `ziwei-core` 的紫微排盘流程、数据表与 i18n 映射移植/生成来源。

## lunar-java

- Project: https://github.com/6tail/lunar-java
- License: MIT
- Copyright: Copyright (c) 2018 6tail
- Usage: `cn.6tail:lunar:1.7.7` 运行时依赖；用于农历、干支、节气、黄历字段，并为多模块历法计算提供基础。

## lunar-lite

- Project: https://github.com/SylarLong/lunar-lite
- License: MIT
- Copyright: Copyright (c) 2023 Sylar
- Usage: iztro 农历适配层的语义参考。

## AndroidX / Jetpack Compose

- Project: https://android.googlesource.com/platform/frameworks/support
- License: Apache License 2.0
- Usage: Android UI、Activity、Lifecycle、DataStore、Compose 与 Material 3。
- RC 测试侧额外使用 `androidx.test.ext:junit`、`androidx.test.espresso:espresso-core`、Compose UI Test；这些只进入 androidTest/test APK，不进入正式 release APK 的运行时功能。

## Kotlin

- Project: https://github.com/JetBrains/kotlin
- License: Apache License 2.0
- Usage: Kotlin 编译器、标准库及 Gradle 插件生态。

## K2 local PDF research helpers

以下依赖只通过 `pip --target` 安装到仓库外的隔离目录，用于本地 K2 材料准备/视觉页渲染；
它们不是 Android App 的运行时依赖，不进入 APK/AAB，也不授权把研究 PDF 或渲染页提交到 Git。

### pypdfium2 / PDFium

- Project: https://github.com/pypdfium2-team/pypdfium2
- pypdfium2 License: Apache-2.0 OR BSD-3-Clause
- PDFium: BSD-style license；其二进制发行还包含 PDFium 自身第三方组件的 notices/licenses。
- Usage: `tools/build_k2_local_visual_pages.py` 将 `VISUAL_REQUIRED` PDF 原页渲染成仓库外 PNG，供后续视觉复核；不做 OCR，也不授予 Reading/Evidence/Claim credit。
- Distribution boundary: 若未来重新分发 pypdfium2/PDFium 二进制，必须随其上游发行物保留适用的 PDFium/third-party notices；当前仓库不会把这些二进制打包进 App。

### Pillow

- Project: https://github.com/python-pillow/Pillow
- License: MIT-CMU
- Usage: 仅作为 pypdfium2 bitmap 的 PNG 编码桥接，输出仍强制位于仓库外。
- Distribution boundary: 当前不进入 Android APK/AAB。

现有 `pypdf` / `pdfminer.six` 同样属于仓库外 K2 文本层材料 helper 依赖；其作用是读取已有 PDF
文本层/页树，不做 OCR，也不改变来源版权与 Knowledge packaging 边界。

## CI-only GitHub Actions

`actions/upload-artifact@v4` 仅用于 GitHub Actions 在版权 Gate、核心测试、Android Lint、APK 构建与 APK 内容审计全部通过之后发布测试构建产物；它不会进入 Android APK。

- Project: https://github.com/actions/upload-artifact
- License: MIT
- Copyright: Copyright (c) 2018 GitHub, Inc. and contributors
- Distribution boundary: workflow 只引用 Action，不把其源码复制进 App；因此不把该许可混入 APK 的运行时 notices。仓库级审计仍在此记录其来源与许可。

RC 设备验收还使用：

- Project: https://github.com/ReactiveCircus/android-emulator-runner
- License: Apache License 2.0
- Usage: GitHub Actions 中启动 Android Emulator，运行 `connectedDebugAndroidTest`、飞行模式/屏幕尺寸/深浅色验收与截图采集。
- Distribution boundary: 仅 CI/build-time 使用，不进入 APK/AAB；上游仓库元数据已核对为 Apache-2.0。

已有 `actions/checkout`、`actions/setup-java`、`gradle/actions/setup-gradle` 同样属于 CI/build-time 基础设施，不属于 App 运行时依赖；若未来复制、修改或重新分发其源码，应按各自上游许可重新检查。

## 测试侧依赖

`org.json:json:20240303` 当前只在 `ziwei-core` JVM 测试中使用，不作为 Android App
运行时依赖。若未来进入发行包，必须重新独立审查其许可与分发义务。

Android instrumentation 测试依赖属于 Apache-2.0 的 AndroidX 测试栈，只进入测试构建；正式 release APK 仍由现有 APK 内容审计反向确认没有测试代码/测试资源混入。

## Distribution

发行包内置：

- `app/src/main/assets/licenses/OPEN_SOURCE_NOTICES.txt`
- `app/src/main/assets/licenses/APACHE-2.0.txt`

研究目录、书籍笔记与工程 handoff 不因本文件而获得再分发授权；其内容边界见
`COPYRIGHT_REVIEW.md` 与各模块 copyright gate。
