# 玄学排盘（xuanxue）

一个以**本地计算、隐私优先、无广告**为核心原则的 Android 玄学排盘项目。
当前 App 已实现紫微斗数排盘；仓库同时保留奇门、八字、紫微、风水的研究笔记与工具。

## 当前 App

- 紫微斗数排盘（default 派别）
- 十二宫盘面
- 十四主星、亮度与四化
- 辅星、杂曜、长生 12 神、博士 12 神、岁前/将前 12 神
- 五行局、命主、身主、大限、小限
- 闰月修正与早/晚子时
- 无账号、无支付、无广告、无推送、无网络权限
- 所有排盘计算在设备本地完成

## UI/UX v2

新版界面在 `uiux-v2` 分支开发，设计原则是：

- 现代东方视觉，而不是仿古模板堆叠
- 优先解决紫微命盘的高信息密度问题
- 宫位摘要与宫位详情分层显示
- 不使用第三方图片、图标包、商业字体或商业 App 视觉素材
- UI 与 `ziwei-core` 分离，重构界面不改变排盘算法

## 技术栈

- Kotlin 2.0 + Jetpack Compose + Material 3
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

`ziwei-core` 通过黄金夹具与 iztro 原版逐字段对照。当前夹具覆盖阳男午时、
阴女子时、闰月、晚子时、立春边界、现代儿童与深冬等边界场景。

## 版权与开源许可

本项目自有代码采用 MIT License。第三方许可与来源见：

- `NOTICE`
- `THIRD_PARTY_NOTICES.md`
- `COPYRIGHT_REVIEW.md`
- `app/src/main/assets/licenses/`（随 APK 打包）

新版 UI/UX 为独立设计，不复制商业命理 App 的代码、视觉素材、截图、字体或文案。

研究资料方面，已出版扫描书不进入 Git；仓库只保留书目与研究笔记。研究笔记仍需
遵守“以总结和验证为主、不大段照录原文”的版权规则，具体见 `COPYRIGHT_REVIEW.md`。

## 学习资料

总索引见 `资料总目.md`。奇门、八字、紫微、风水分别位于仓库同名目录中。
