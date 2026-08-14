# xuanxue 版权与开源合规审计

审计日期：2026-08-14

> 这是一份工程合规检查，不构成针对任何司法辖区的法律意见。真正商业发行前，
> 如需零争议级别的法律结论，应由专业律师进行最终审查。

## 1. 当前结论

### GREEN：新版 App UI/UX

`uiux-v2` 的界面必须坚持独立设计：只使用 Jetpack Compose、系统字体、基础几何图形
与项目自有文案。不得从任何商业命理 App 复制源码、布局代码、截图、图片、图标、
插画、商业字体、动画素材或长段文案。

本轮 UI 重构不引入外部图片、字体或图标包，因此没有新增视觉素材授权风险。

### GREEN：iztro

`ziwei-core` 的主要排盘逻辑与数据表来自 iztro。上游仓库当前明确采用 MIT License，
其 LICENSE 版权声明为 `Copyright (c) 2023 All Contributors`。MIT 允许复制、修改、
分发与再许可，但要求保留版权声明和许可文本。

本仓库通过 `NOTICE`、`THIRD_PARTY_NOTICES.md` 与 APK 内置许可文本保留该信息。

### GREEN：lunar-java

`cn.6tail:lunar` 上游采用 MIT License，版权声明为 `Copyright (c) 2018 6tail`。
本项目将其作为运行时依赖，并保留完整 MIT 许可文本。

### GREEN：lunar-lite

本仓库只把 lunar-lite 作为 iztro 适配层语义参考。上游采用 MIT License，版权声明为
`Copyright (c) 2023 Sylar`。许可信息已保留。

### GREEN：AndroidX / Jetpack Compose / Kotlin

AndroidX、Jetpack Compose 与 Kotlin 使用 Apache License 2.0。本仓库不复制其源码来
冒充自有代码，而是通过标准 Gradle 依赖使用。Apache 2.0 完整文本随 APK 打包。

### YELLOW：测试依赖 org.json

`org.json:json` 仅用于 `ziwei-core` 的 JVM 黄金夹具测试，不进入 Android 运行时 APK。
它不应被误写成 App 的运行时开源依赖。若未来把该库打入发行包，需要单独复核其许可。

### YELLOW：书籍研究笔记

仓库明确不提交已出版扫描书，这是正确的边界；但“没有 PDF”不等于研究笔记自动没有
版权风险。若笔记包含大量连续原文、逐页转录、完整表格或可替代原书阅读的内容，仍可能
形成风险。

因此研究目录执行以下规则：

1. 以自己的总结、交叉验证、案例复盘和方法论提炼为主体。
2. 引文保持必要且短，并记录书名/作者/页码或章节。
3. 不上传扫描页、整章 OCR、完整原文表格或可还原原书的大段文字。
4. 古籍原文与现代整理本区分处理；现代校注、翻译、排版和注释可能仍受版权保护。
5. App 发行包不得自动打包仓库根目录的学习资料。

当前这部分只能标为 **YELLOW**：尚未逐行与每本现代出版物做文本相似度比对，不能宣称
“全部版权已清零”。

## 2. 本轮已修复的问题

- 根目录 `LICENSE` 恢复为标准、纯净的项目 MIT License，避免把第三方版权行混进自有
  LICENSE 头部造成许可识别和权属表达混乱。
- 第三方权利人及许可拆到 `NOTICE` 和 `THIRD_PARTY_NOTICES.md`。
- 第三方许可文本加入 `app/src/main/assets/licenses/`，确保二进制 APK 发行时仍携带许可。
- README 不再把商业 App 的逆向分析作为产品来源叙事，避免造成 UI/源码来源混淆。
- 新版 UI 明确禁止复用商业 App 的视觉素材与文案。

## 3. 发布前版权 Gate

任何 release APK / AAB 在发布前必须满足：

- `app/src/main/assets/licenses/OPEN_SOURCE_NOTICES.txt` 存在。
- `app/src/main/assets/licenses/APACHE-2.0.txt` 存在。
- 新增依赖逐个记录 license 与 copyright owner。
- 新增图片、字体、音效、插画必须记录来源、作者、许可和商业使用权限。
- 无来源证明的素材直接拒绝进入 release。
- 不把 `奇门/`、`八字/`、`紫薇/`、`风水/`、`学习资料/` 的研究内容打入 App，除非完成
  单独的内容版权审查。
- 不使用第三方商标/logo 作为 App 图标、品牌识别或造成官方关联暗示。

## 4. 允许进入 UI 的素材策略

默认只允许三类：

- Jetpack Compose 自绘图形；
- Android 系统字体；
- 项目成员原创且权属明确的图片/图标。

需要引入第三方视觉资产时，必须先过版权 Gate，再写代码。
