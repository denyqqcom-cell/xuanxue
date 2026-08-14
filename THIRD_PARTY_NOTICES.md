# Third-Party Notices

本文件记录 xuanxue 当前使用或参考的第三方软件。第三方权利人与项目自身版权分开陈述；
完整许可文本同时打包在 `app/src/main/assets/licenses/` 中。

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

## Kotlin

- Project: https://github.com/JetBrains/kotlin
- License: Apache License 2.0
- Usage: Kotlin 编译器、标准库及 Gradle 插件生态。

## 测试侧依赖

`org.json:json:20240303` 当前只在 `ziwei-core` JVM 测试中使用，不作为 Android App
运行时依赖。若未来进入发行包，必须重新独立审查其许可与分发义务。

## Distribution

发行包内置：

- `app/src/main/assets/licenses/OPEN_SOURCE_NOTICES.txt`
- `app/src/main/assets/licenses/APACHE-2.0.txt`

研究目录、书籍笔记与工程 handoff 不因本文件而获得再分发授权；其内容边界见
`COPYRIGHT_REVIEW.md` 与各模块 copyright gate。
