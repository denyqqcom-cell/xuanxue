# K2 CDAF-H2 天气信号实现结构审计 v0.1

状态：`V02_RECONCILED / ABSTRACT_STATE_SPACE_ONLY / NO_OUTCOME_DATA / NOT_EMPIRICAL_VALIDATION`  
关联假设：`CDAF-H2`  
关联设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
审计脚本：`tools/test_k2_qimen_weather_structure_audit.py`  
当前 active model：`FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02`  
当前 QimenEngine blob：`046825e480422eb0ac6734ea0330861bbd422997`  
Empirical Credit：`NONE`  
Batch：`NONE`

## 1. 本审计只回答什么

本审计只回答：

> 在锁定的 QimenEngine 盘面实现中，把 24 节气、每节气三个名义元局和固定酉时的五种时干状态做笛卡尔枚举时，`CORE_RAIN_SIGNAL_V01` 在这个抽象盘面状态空间里有多稀疏？

它明确不回答：

- 一年真实民用日期里该信号多久出现一次；
- 正式 weather Batch 需要多少天；
- 该信号是否能预测降雨；
- 该信号是否优于 HKO；
- 奇门是否提供独立于 calendar/time 的信息。

历史天气、HKO 历史 PSR 和任何 outcome 均未被读取。

## 2. 第一轮纠偏：五日符头不能与六甲旬首混用

旧 `CHAI_BU_FUTOU` 曾用：

```text
s - (s % 10)
```

寻找所谓“符头”。这实际寻找的是十个干支一组的六甲旬首，而 QM-SRC-0021 / 0028 所保存的拆补符头结构是每五日一换、以甲日或己日为元首的五日符头。

两者必须分开：

```text
六甲旬首：10-unit grouping
用途：旬首、遁干、旬空等

拆补符头：5-day yuan head
用途：上 / 中 / 下元定局
```

`yuanOfFutou()` 因而改为五日回溯；`xunInfo()` 的十日旬首逻辑保持独立。

## 3. 第二轮纠偏：实际交节时刻不能被“整日换节”替代

后续 boundary regression 发现旧候选 Engine 使用：

```text
lunar.getPrevJieQi(true)
```

这采用 whole-day 口径，会把交节日从 00:00 起全部归入新节气。项目来源层保存的拆补规则却要求按实际交节时辰切换。

2026-08-07 的 implementation-only regression 明确暴露了这个差异：在同一 civil date、同一癸丑日、同一五日符头上元条件下，实际立秋交接前仍应属于大暑上元，交接后才进入立秋上元；Engine 必须能在同一天内从阴遁7局切到阴遁2局，而不是午夜直接切换。

当前 V02 已统一改用 exact transition family：

```text
getPrevJieQi(false)
```

并由：

`QimenEngineTest.futouPreservesIntradaySolarTermBoundaryInsteadOfSwitchingAtMidnight`

直接回归。K2 App UI CI #86 中该测试 PASS。

信用边界必须保留：这个 regression 使用同一个 lunar-java calendar dependency 找 boundary，因此它只获得 implementation credit；它不是独立天文验证，也不是 Gate 0 仍要求的 source-grounded before/after boundary fixture。

## 4. 第三轮纠偏：weather audit 不得自行重写“九星所携天盘干”算法

旧 weather audit 曾在测试文件内重新实现 `carriedHeavenStems()`。即使它与 Engine 当前算法一致，这仍有两个问题：

1. audit 可能与真实 Engine 漂移；
2. source plate fixture 可能只锁九星位置，而 weather audit 用另一套镜像算法生成天盘干，形成循环自证。

V02 已把九星转动后所携三奇六仪正式暴露为：

```text
QimenEngine.Gong.tianGan
```

Engine 内部仍只有一套 authoritative carried-heaven-stem computation。两套 weather Kotlin audit 都直接读取 `gong.tianGan`，不再维护第二套算法。

同时 `QimenSourcePlateFixtureTest` 已对 QM-SRC-0021 2004-05-29 戊午时逐宫直接断言真实 Kotlin Engine 的：

```text
palace -> (tianXing, tianGan)
```

八个外宫 expected pairs 为：

```text
1 -> 天冲 + 壬
2 -> 天心 + 丙
3 -> 天英 + 己
4 -> 天芮天禽 + 辛
6 -> 天任 + 戊
7 -> 天蓬 + 庚
8 -> 天辅 + 癸
9 -> 天柱 + 乙
```

K2 App UI CI #86 中：

`QimenSourcePlateFixtureTest > qm0021_20040529_wuwu_futou_reproduces_source_star_and_heaven_stem_pairs()` = PASS。

这获得的是该来源盘的 source-grounded structural pairing credit，不等于完整九宫体系已全局验证。

## 5. 2002 fixture 撤回不能被重新包装成证据

旧结构记录曾把 `2002-08-01 / 辛丑日 / 壬申时 / 阴遁一局` 当第二 dated fixture。回查后确认：现有 Atomic Evidence / deep-source distillate 并未保存足以支持这组日期—时柱元数据的原页 provenance。

因此：

```text
2002-08-01 candidate fixture = SOURCE_PAGE_REVERIFICATION_REQUIRED
```

它已经从 Python plate-pairing fixture 的“独立来源元数据”断言中删除。不得把 Engine 输出、旧学习摘要或通过测试本身反写为原书事实。

## 6. 为什么 360-state 只能叫抽象状态密度

17:00 HKT 属酉时，固定酉时有五种时干状态：

`癸酉 / 乙酉 / 丁酉 / 己酉 / 辛酉`

枚举：

```text
24节气 × 3名义元局 × 5酉时状态 = 360
```

当前 V02 仍得到：

```text
CORE_RAIN_SIGNAL_V01 = TRUE : 64
state-space density          : 64 / 360 = 17.777...%
```

不同节气的名义 15-state trigger count 仍为：

```text
冬至0  小寒2  大寒5  立春2  雨水5  惊蛰0
春分5  清明0  谷雨2  立夏0  小满2  芒种5
夏至4  小暑2  大暑3  立秋2  处暑3  白露4
秋分3  寒露4  霜降2  立冬4  小雪2  大雪3
```

这个结果只描述映射函数在抽象 nominal plate states 中的覆盖度。拆补法的真实 civil-date 节气段长度、符头相位和局数权重不能由 360-state 等权模型替代。

所以：

```text
360-state audit != civil-date frequency audit
```

## 7. V02 真实公历重算：聚合总数相同不等于旧 Engine 正确

在 V02 exact-transition + first-class `Gong.tianGan` Engine 上，App UI CI #86 已重新运行 2000-01-01..2099-12-31、每日17:00 HKT 的真实公历结构审计。

结果仍为：

```text
total_civil_days        = 36525
core_signal_days        = 6498
civil_date_trigger_rate = 0.17790554414784393
```

这里必须防止一个新的误区：

> V02 与旧候选的聚合 `6498` 恰好相同，不代表 whole-day transition 实现没有错误。

actual-transition regression 已直接证明旧 boundary semantics 错误。聚合计数只是一个低维 summary；不同日期的节气归属、segment boundaries、sham alignment 或局部状态可以变化，同时总 trigger count 仍碰巧相等。

V02 calendar-equivalence 重算也显示其 schedule provenance 必须重新生成：

```text
complete_segment_days  = 36510
plus_1_hamming_days    = 10344
minus_1_hamming_days   = 10344
audit_schedule_sha256 = e7ccd47461a5f75b3e89ffcf2743ab6939521ad27a493ecd6cebf39517ba845f
```

因此旧 V01 report/hash 不得作为 V02 的证据复用。

## 8. 当前 blocker 与信用边界

截至 V02：

```text
FIVE_DAY_FUTOU_REMEDIATION       = IMPLEMENTED / REGRESSION_PASS
EXACT_TRANSITION_IMPLEMENTATION  = IMPLEMENTED / REGRESSION_PASS
FIRST_CLASS_HEAVEN_STEM          = IMPLEMENTED / SOURCE_PAIR_REGRESSION_PASS
JU_METHOD_VALIDATION             = PARTIAL / SOURCE_BOUNDARY_FIXTURE_OPEN
PLATE_PAIRING_SOURCE_FIXTURE     = ONE_DATED_PLATE_DIRECTLY_ASSERTED
GLOBAL_PLATE_VALIDATION          = NOT_CLAIMED
REAL_CALENDAR_FREQUENCY_AUDIT    = CLOSED_FOR_V02_ENGINE_STRUCTURE_ONLY
CALENDAR_EQUIVALENCE_CONTROL     = MACHINE_VERIFIED / BATCH_SCHEDULE_NOT_FROZEN
SERIAL_DEPENDENCE_SAMPLE_GATE    = METHOD_DEFINED / BATCH_PARAMETERS_NOT_FROZEN

BATCH_READY                      = false
BATCH                            = NONE
FREEZE                           = NONE
OUTCOME                          = NONE
EMPIRICAL_CREDIT                 = NONE
```

Gate 0 仍缺 source-grounded actual-transition boundary fixture；Gate A 仍缺第二张独立 dated plate fixture。Implementation correctness 不能替代 source validation，单一 source plate 也不能外推成全局盘法正确。

## 9. 当前可以安全说什么

可以说：

> 当前 active CDAF-H2 V02 Engine blob 为 `046825e480422eb0ac6734ea0330861bbd422997`。360 个抽象名义盘面状态中有64个 core-signal 状态；真实100年17:00 HKT civil-calendar 重算有6498个触发日。V02 已修正 whole-day 节气切换，并把星所携天盘干收回为 Engine 一等字段；2004 source plate 的八个星—天盘干 pairing 已由真实 Kotlin Engine 直接断言通过。

不可以说：

- 17.79% 是天气预测准确率；
- 因为 V01/V02 都是6498，所以旧 whole-day Engine 也是正确的；
- 一张来源盘已经证明完整奇门九宫盘法；
- implementation boundary regression 已经关闭 source-grounded Gate 0；
- weather Batch 已可启动。
