# K2 CDAF-H2 真实公历 FUTOU 结构审计 v0.1

状态：`STRUCTURE_AUDIT_COMPLETE_FOR_PINNED_ENGINE / NO_WEATHER_OUTCOME / NO_EMPIRICAL_CREDIT`  
关联设计：`K2PV-CDAF-H2`  
方法：`CHAI_BU_FUTOU`  
QimenEngine blob：`1912760ccd10cb4a58eb8faec06669c0d690657b`  
审计窗口：`2000-01-01 .. 2099-12-31`，每日 `17:00 HKT`  
天气预报数据：`未使用`  
天气 Outcome：`未使用`  
Empirical Credit：`NONE`

## 1. 为什么要做真实公历审计

早期结构审计用：

`24节气 × 3名义元 × 5个酉时状态 = 360`

得到 `64/360 = 17.78%`。

这个值只能描述一个抽象盘面笛卡尔状态空间，不能直接解释为真实公历日期触发频率。拆补法的节气交接、甲己五日符头与真实日期序列必须由实际历法运行才能确定。

因此本轮直接调用真实 `QimenEngine.bySolar(..., CHAI_BU_FUTOU)`，逐日生成 100 个完整公历年的 17:00 HKT 盘。测试文件：

`ziwei-core/src/test/kotlin/com/xuanxue/qimen/QimenWeatherRealCalendarAuditTest.kt`

CI 报告：

`ziwei-core/build/reports/qimen-weather-real-calendar-audit-v01.json`

GitHub Actions run：`33109453828`，App UI CI = SUCCESS。

## 2. 总体结果

真实 civil dates：`36,525`

`CORE_RAIN_SIGNAL_V01 = TRUE`：`6,498`

真实日期结构触发率：

`6498 / 36525 = 0.1779055441 = 17.79055441%`

最长连续触发：`4日`

最长两次触发之间的连续非触发间隔：`33日`

单日最大命中路径数：`1`

命中基数：

- `0 hit = 30,027日`
- `1 hit = 6,498日`

因此这个 signal 在当前引擎中不是恒真，也不是罕见到几乎不出现，但具有明显聚集和长空窗。

这个 17.79% 与旧抽象状态空间 17.78% 数值接近，只说明长期状态权重碰巧接近；不能反过来证明旧 `360-state` 可以代替真实公历枚举。

## 3. 三元的真实日数与触发并不等价

100年窗口中：

- 上元：`12,175日`，触发 `1,814`，约 `14.90%`
- 中元：`12,175日`，触发 `1,849`，约 `15.19%`
- 下元：`12,175日`，触发 `2,835`，约 `23.29%`

三元总日数在这个完整100年窗口中刚好相等，但 signal 条件对下元的触发倾向明显更高。因此“元本身在样本中等权”不能消除 calendar/ju confounding。

## 4. 节气结构非常强

以下节气在整个100年窗口中 `0` 次触发：

- 冬至：`0 / 1472`
- 惊蛰：`0 / 1501`
- 清明：`0 / 1529`
- 立夏：`0 / 1554`

高触发节气包括：

- 芒种：`525 / 1570 ≈ 33.44%`
- 雨水：`497 / 1492 ≈ 33.31%`
- 大寒：`491 / 1474 ≈ 33.31%`
- 春分：`505 / 1517 ≈ 33.29%`
- 寒露：`404 / 1513 ≈ 26.70%`
- 立冬：`398 / 1491 ≈ 26.69%`

这不是天气结果，而是 signal 自身的日历结构。

## 5. 阴阳九局结构更强

100年真实日期中，18 个 `阴/阳 × 九局` 组合只有 8 个出现 signal：

- 阳2：`809 / 2021 ≈ 40.03%`
- 阳3：`404 / 2020 = 20.00%`
- 阳6：`1614 / 2018 ≈ 79.98%`
- 阴2：`407 / 2038 ≈ 19.97%`
- 阴3：`815 / 2040 ≈ 39.95%`
- 阴4：`1223 / 2038 ≈ 60.01%`
- 阴5：`408 / 2037 ≈ 20.03%`
- 阴6：`818 / 2043 ≈ 40.04%`

其余组合：

`阳1/4/5/7/8/9、阴1/7/8/9 = 0`。

这说明 `CORE_RAIN_SIGNAL_V01` 在当前算法下高度受 Ju/历法状态约束，而不是在所有时间均匀寻找“雨象”。

## 6. 对 CDAF-H2 的方法学影响：从 calendar confounding 升级为 calendar equivalence 问题

当前 weather-v0.1 的奇门盘只以日期时间作为输入；`CORE_RAIN_SIGNAL_V01` 又是该盘的确定性函数。

因此：

`calendar/time -> Qimen plate -> CORE_RAIN_SIGNAL_V01`

从信息论角度，M2 在这个设计里没有引入一个独立于时间的外部观测源。任何具体 signal 都可以等价写成某个更复杂的 calendar/time deterministic function。

所以未来即使：

`M2 > M1`

也不能直接解释为：

`奇门盘获得了独立于日历的额外现实信息。`

最多只能先得到：

> 在预先冻结的模型复杂度和 comparator 约束下，这个特定的奇门时间变换可能比指定的较简单日历 baseline 更有预测/压缩价值。

若要主张 plate-specific mapping 的价值，至少需要与复杂度匹配、事前冻结的 calendar-only comparator 或 negative control 比较；即使胜出，也仍是“特定变换在该模型类中表现更好”，不是证明超出时间输入的信息来源。

这是比普通季节性控制更严格的边界。

## 7. 对 Sample Adequacy 的影响

不能用 `17.79%` 直接计算正式 weather Batch 需要多少天，因为真正产生 M1/M2 差异还要求：

`M1 == NO_RAIN10 && CORE_RAIN_SIGNAL_V01 == TRUE`

目前没有读取任何 HKO PSR 历史数据，所以这个 discordant-opportunity rate 未知。

此外 signal 最大连续触发4日、最大非触发空窗33日，说明观察机会有时间聚集性。未来样本设计必须保留 serial dependence，不得把 6,498 个结构日视为 IID Bernoulli 样本。

## 8. Gate 状态

对 exact method+engine：

`REAL_CALENDAR_FUTOU_FREQUENCY = CLOSED_FOR_PINNED_ENGINE_STRUCTURE_ONLY`

关闭仅表示：真实 civil-date signal 结构已经被机器遍历并留档。

它不表示：

- `JU_METHOD_VALIDATION` 已全局关闭；
- `PLATE_PAIRING_VALIDATION` 已全局关闭；
- calendar equivalence 已解决；
- Batch 已准备好；
- signal 有预测价值。

只要 `CHAI_BU_FUTOU` 实现、QimenEngine blob、17:00 freeze time 或 CORE signal 定义发生变化，本审计必须重新运行，旧结构频率不得继承。

## 9. 当前可安全使用的数字

可以说：

> 对 QimenEngine blob `1912760...`、CHAI_BU_FUTOU、17:00 HKT，在 2000-01-01 至 2099-12-31 的 36,525 个真实 civil dates 中，CORE_RAIN_SIGNAL_V01 结构性触发 6,498 日（17.7906%）。该 signal 对节气、元和阴阳九局高度不均匀。

不可以说：

- 它有17.79%的天气准确率；
- 奇门每5.6天预测一次雨；
- 未来 Batch 只需按 17.79% 反推样本天数；
- M2 若优于 M1 就证明奇门产生了独立于日历的额外信息。
