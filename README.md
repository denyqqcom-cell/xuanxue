# 玄学排盘（xuanxue）

纯净版紫微斗数排盘 App —— **无支付、无广告、无推送、无账号、无网络权限**，所有计算在设备本地完成。

> 灵感来源：逆向分析了一款典型命理 App（`oms.mmc.fortunetelling.gmpay.lingdongziwei2`，广东很久文化传播有限公司）后，将其"排盘核心"用开源算法重写，**剔除全部变现功能**（灵符付费、大师咨询、广告、推送、裂变深链）。

## 功能

- 紫微斗数排盘（default 派别，基于《紫微斗数全书》安星法）
- 十二宫盘面（命宫/兄弟/夫妻/子女/财帛/疾厄/迁移/仆役/官禄/田宅/福德/父母）
- 十四主星 + 亮度（庙旺得利平不陷）+ 四化（禄权科忌）
- 14 辅星 + 38 杂耀 + 长生12神 + 博士12神 + 岁前/将前12神
- 五行局、命主、身主、大限、小限
- 支持闰月修正、早晚子时（13 时辰）
- 本地存档（无网络，隐私安全）

## 技术栈

- Kotlin 2.0 + Jetpack Compose (Material3)
- 排盘引擎：`ziwei-core`（iztro MIT → Kotlin 移植，见 NOTICE）
- 农历基础：`cn.6tail:lunar` (lunar-java, MIT)

## 构建

```bash
export JAVA_HOME=/path/to/jdk17
export ANDROID_HOME=/path/to/android-sdk
./gradlew :ziwei-core:test    # 排盘算法黄金夹具测试（7 组对照 iztro 原版）
./gradlew :app:assembleDebug  # 打包 APK
```

APK 输出：`app/build/outputs/apk/debug/app-debug.apk`

## 正确性验证

`ziwei-core` 的排盘算法与 iztro（TypeScript 原版，4058★）**逐字段 1:1 对齐**：
7 组黄金夹具（阳男午时 / 阴女子时 / 闰月 / 晚子时 / 立春边界 / 现代儿童 / 深冬）
由 iztro 原版生成，Kotlin 移植版输出完全一致（`fixtures.jsonl` 断言测试）。

## 许可证

MIT。排盘算法数据表移植自 [iztro](https://github.com/SylarLong/iztro)（MIT），
农历基础来自 [lunar-java](https://github.com/6tail/lunar-java)（MIT）。
详见 [NOTICE](NOTICE.md)。
