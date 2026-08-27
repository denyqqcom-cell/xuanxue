# K2 CDAF-H2 天气信号实现结构审计 v0.1

状态：`ABSTRACT_STATE_SPACE_ONLY / NO_OUTCOME_DATA / NOT_CIVIL_DATE_FREQUENCY / NOT_EMPIRICAL_VALIDATION`  
关联假设：`CDAF-H2`  
关联设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
审计脚本：`tools/test_k2_qimen_weather_structure_audit.py`  
Empirical Credit：`NONE`  
Batch：`NONE`

## 1. 本审计现在只回答什么

本审计只回答：

> 在锁定的 QimenEngine 盘面实现中，把 24 节气、每节气三个**名义元局**和固定酉时的五种时干状态做笛卡尔枚举时，`CORE_RAIN_SIGNAL_V01` 在这个抽象盘面状态空间里有多稀疏？

它明确不回答：

- 一年真实民用日期里该信号多久出现一次；
- 需要观察多少天；
- 该信号是否能预测降雨；
- 该信号是否优于 HKO。

历史天气、HKO 历史 PSR 和任何 outcome 均未被读取。

## 2. 2026-08-28 纠偏：旧 FUTOU 实现混淆了两个不同对象

审计推进到来源日期 fixture 后发现，旧 `CHAI_BU_FUTOU` 用：

```text
s - (s % 10)
```

寻找所谓“符头”。这实际寻找的是十个干支一组的**六甲旬首**，而 QM-SRC-0021 的拆补符头是每五日一换、以甲日或己日为元首的**五日符头**。

两者必须分开：

```text
六甲旬首：10-unit grouping
用途：旬首、遁干、旬空等

拆补符头：5-day yuan head
用途：上 / 中 / 下元定局
```

旧实现因此被修为：

```text
s - (s % 5)
```

当前锁定 `QimenEngine.kt` Git blob：

`1912760ccd10cb4a58eb8faec06669c0d690657b`

这个修复不改 `xunInfo()` 的十日旬首逻辑。

## 3. 为什么旧 360-state 数字不能再被叫作“实际触发频率”

17:00 HKT 属酉时，固定酉时有五种时干状态：

`癸酉 / 乙酉 / 丁酉 / 己酉 / 辛酉`

若只枚举：

```text
24节气 × 3名义元局 × 5酉时状态
```

得到 360 个抽象合同状态。

但 QM-SRC-0021 的拆补法明确允许节气交接后出现：

```text
残上 → 中 → 下 → 补上
```

即真实公历日期不会自动给每个节气的上、中、下元各恰好五天等权重。

因此：

```text
360-state audit ≠ civil-date frequency audit
```

任何“平均每 5.625 天一次”之类表述全部撤回。

## 4. 抽象盘面状态空间结果仍可保留

在 360 个**名义盘面状态**中：

```text
CORE_RAIN_SIGNAL_V01 = TRUE : 64
state-space density          : 64 / 360 = 17.777...%
```

这个数只描述映射函数在抽象状态空间中的覆盖度。

不同节气的名义 15-state trigger count 为：

```text
冬至0  小寒2  大寒5  立春2  雨水5  惊蛰0
春分5  清明0  谷雨2  立夏0  小满2  芒种5
夏至4  小暑2  大暑3  立秋2  处暑3  白露4
秋分3  寒露4  霜降2  立冬4  小雪2  大雪3
```

这仍提示 signal 与节气/局数结构高度相关，所以 `CALENDAR_CONFOUNDING_CONTROL` 继续是硬 blocker。

## 5. 来源日期 fixture 带来的第二层验证

### Fixture A — 2004-05-29 戊午时

QM-SRC-0021 明确给出：

```text
甲申年 己巳月 戊申日 戊午时
小满
阳遁八局
甲寅旬
值符天辅
```

并给出转动后的九星及所携天盘奇仪。项目已建立 chart-only fixture，验证外八宫星位，并以独立结构测试复核星—所携天盘干配对。

这只验证该来源盘，不等于完整九宫体系已全局毕业。

### Fixture B — 2002-08-01 壬申时

QM-SRC-0021 另给：

```text
壬午年 丁未月 辛丑日 壬申时
甲午旬
阴遁一局
```

这个日期正是发现旧 FUTOU bug 的反例：

```text
old ten-unit rollback -> 甲午 -> 错当上元 -> 大暑阴7
correct five-day head -> 己亥 -> 中元 -> 大暑阴1
```

因此该 fixture 不使用书中“是否下雨”的结果，只用日期、干支、节气/局数验证排盘算法身份。

## 6. 当前 blocker 重新排序

截至本纠偏：

```text
FUTOU_ALGORITHM_REMEDIATION     = IMPLEMENTED / CI_PENDING
JU_METHOD_VALIDATION            = OPEN
PLATE_PAIRING_SOURCE_FIXTURE    = IMPLEMENTED / CI_PENDING
GLOBAL_PLATE_VALIDATION         = NOT_CLAIMED
CALENDAR_CONFOUNDING_CONTROL    = OPEN
CIVIL_DATE_FREQUENCY_AUDIT      = OPEN
SERIAL_DEPENDENCE_SAMPLE_GATE   = OPEN

BATCH_READY                     = false
BATCH                           = NONE
FREEZE                          = NONE
OUTCOME                         = NONE
EMPIRICAL_CREDIT                = NONE
```

## 7. 下一步的正确频率审计

如果 weather-v0.1 最终冻结 `CHAI_BU_FUTOU`，下一次频率审计必须直接枚举**真实公历日期**，例如固定多年窗口、每日固定 17:00 HKT 调用真实 `QimenEngine.bySolar(..., CHAI_BU_FUTOU)`，再统计：

- 每日使用的节气 / 元 / 局；
- `CORE_RAIN_SIGNAL_V01` 是否触发；
- 季节与节气分层触发率；
- 信号连续性与自相关结构。

这一审计仍不得读取天气 outcome。

只有 civil-date frequency 建立后，才能讨论 observation window；64/360 不再允许用于样本天数推算。

## 8. 当前可以安全说什么

可以说：

> 当前盘面映射在 360 个抽象名义状态中有 64 个 core-signal 状态，但这只是 state-space density。来源 fixture 进一步发现并修复了五日符头与十日旬首混淆；真实 FUTOU 民用日期频率尚未建立。

不可以说：

- 奇门平均每 5.625 天出现一次降雨信号；
- 17.78% 是天气预测率或准确率；
- 一张来源盘已经证明完整奇门盘法；
- weather Batch 已可启动。
