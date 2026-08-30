# K2 CDAF-H2 真实公历 FUTOU 结构审计 v0.1

状态：`V02_STRUCTURE_AUDIT_COMPLETE_FOR_PINNED_ENGINE / NO_WEATHER_OUTCOME / NO_EMPIRICAL_CREDIT`  
关联设计：`K2PV-CDAF-H2`  
active model：`FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02`  
方法：`CHAI_BU_FUTOU`  
QimenEngine blob：`046825e480422eb0ac6734ea0330861bbd422997`  
审计窗口：`2000-01-01 .. 2099-12-31`，每日 `17:00 HKT`  
天气预报数据：`未使用`  
天气 Outcome：`未使用`  
Empirical Credit：`NONE`

## 1. 为什么必须重新做 V02 真实公历审计

早期结构审计用：

`24节气 × 3名义元 × 5个酉时状态 = 360`

得到 `64/360 = 17.78%`。这个值只能描述抽象盘面笛卡尔状态空间，不能直接解释为真实 civil-date 触发频率。

随后又发现旧候选 Engine 使用 whole-day 节气切换，会把交节日从 00:00 起全部归入新节气；而项目保存的拆补规则要求按实际交节时辰切换。V02 因而改用 exact transition，并把九星所携天盘干正式暴露为 `Gong.tianGan`，weather audit 不再自行重写 carried-heaven-stem 算法。

因此旧 real-calendar report 即使聚合数字与新结果部分相同，也不能继续承担 V02 provenance。必须对当前 exact Engine 重新逐日运行。

测试文件：

`ziwei-core/src/test/kotlin/com/xuanxue/qimen/QimenWeatherRealCalendarAuditTest.kt`

V02 CI 报告：

`ziwei-core/build/reports/qimen-weather-real-calendar-audit-v02.json`

GitHub Actions：K2 App UI CI #86，run `33264988516` = SUCCESS。

## 2. V02 总体结果

真实 civil dates：`36,525`

`CORE_RAIN_SIGNAL_V01 = TRUE`：`6,498`

真实日期结构触发率：

`6498 / 36525 = 0.17790554414784393 = 17.79055441%`

最长连续触发：`4日`

最长两次触发之间的连续非触发间隔：`33日`

单日最大命中路径数：`1`

命中基数：

- `0 hit = 30,027日`
- `1 hit = 6,498日`

这个 signal 在当前 Engine 中不是恒真，也不是极端稀疏，但有明显的 calendar clustering 与长空窗。

V02 与旧候选聚合 `6,498` 恰好相同，不能反过来证明旧 whole-day transition 实现正确。边界 regression 已直接证明旧实现的交节日语义错误；总数相同只能说明低维 aggregate 恰好相等。

## 3. 三元真实日数相等，但触发倾向明显不同

100年窗口中三元日数恰好各为 `12,175日`，但触发数为：

- 上元：`1,813`，约 `14.8912%`
- 中元：`1,850`，约 `15.1951%`
- 下元：`2,835`，约 `23.2854%`

所以即使三元在这个窗口里总日数等权，signal 仍对不同元具有明显不同 propensity。不能把“样本日数相等”误写成 calendar confounding 已消除。

## 4. 节气结构依旧非常强

V02 真实 `days_by_jieqi` 与 `triggers_by_jieqi` 显示，以下节气在整个100年窗口中 `0` 次触发：

- 冬至：`0 / 1473`
- 惊蛰：`0 / 1505`
- 清明：`0 / 1529`
- 立夏：`0 / 1555`

高触发节气包括：

- 芒种：`522 / 1570 ≈ 33.25%`
- 春分：`507 / 1515 ≈ 33.47%`
- 雨水：`497 / 1491 ≈ 33.33%`
- 大寒：`492 / 1477 ≈ 33.31%`
- 寒露：`403 / 1513 ≈ 26.64%`
- 立冬：`398 / 1491 ≈ 26.69%`

这里的百分比全部是 **signal 自身的日历结构**，不是天气发生率，也不是预测准确率。

## 5. 阴阳九局结构更强

V02 的 `ju_day_counts / ju_trigger_counts` 显示，18 个 `阴/阳 × 九局` 组合中仍只有 8 个出现 signal：

- 阳2：`808 / 2019 ≈ 40.0198%`
- 阳3：`403 / 2017 ≈ 19.9802%`
- 阳6：`1615 / 2019 ≈ 79.9901%`
- 阴2：`408 / 2040 = 20.0000%`
- 阴3：`816 / 2040 = 40.0000%`
- 阴4：`1224 / 2040 = 60.0000%`
- 阴5：`407 / 2037 ≈ 19.9804%`
- 阴6：`817 / 2041 ≈ 40.0294%`

其余组合：

`阳1/4/5/7/8/9、阴1/7/8/9 = 0`。

因此 `CORE_RAIN_SIGNAL_V01` 高度受 Ju/历法状态约束，而不是在所有时间均匀寻找“雨象”。

## 6. 年度结构稳定，但不能被当成 IID

100个年度的 trigger count 大多落在 `63..68` 之间。这个稳定性只是长期 deterministic calendar structure 的表现，不能把每天视作独立 Bernoulli trial。

同时：

```text
max_consecutive_trigger_days = 4
max_non_trigger_gap_days     = 33
```

说明信号机会有明显的连续性与空窗。未来正式 weather Batch 必须保留 serial-dependence treatment。

## 7. 对 CDAF-H2 的方法学影响：calendar equivalence 仍是核心限制

当前 weather-v0.1 的奇门盘只以日期时间作为输入；`CORE_RAIN_SIGNAL_V01` 是该盘的确定性函数：

```text
calendar/time -> Qimen plate -> CORE_RAIN_SIGNAL_V01
```

因此 M2 在这个设计里没有引入一个独立于时间的外部观测源。

未来即使：

`M2 > M1`

也不能直接解释为：

`奇门获得了独立于日历的额外现实信息。`

最多只能先讨论：在事前冻结的 comparator 与模型复杂度下，这个具体 Qimen-derived 时间变换是否比指定 calendar-equivalence controls 有额外区分力。

若要获得 exact plate-alignment credit，至少还必须同时优于冻结的 `+1日 / -1日` 同节气段 sham。即便如此，也不能推出超出 calendar/time information set 的新信息来源。

## 8. 对 Sample Adequacy 的影响

不能用 `17.79055441%` 直接计算正式 weather Batch 需要多少天，因为真正产生 M1/M2 prediction discordance 还要求：

```text
M1 == NO_RAIN10
AND
CORE_RAIN_SIGNAL_V01 == TRUE
```

目前没有读取历史 HKO PSR/outcome 来估计这个 joint opportunity rate，这一点是刻意保持 outcome-blind。

正式 sample plan 因此继续使用预先冻结的完整 solar-term segments、pre-outcome information counts 与 serial-dependence contract，而不是用 6498/36525 倒推“需要 N 天”。

## 9. Gate 状态

对当前 exact method+engine：

`REAL_CALENDAR_FUTOU_FREQUENCY = CLOSED_FOR_V02_PINNED_ENGINE_STRUCTURE_ONLY`

关闭仅表示：

> 当前 V02 Engine、CHAI_BU_FUTOU、17:00 HKT、CORE_RAIN_SIGNAL_V01 的真实 civil-date signal 结构已经被机器遍历并留档。

它不表示：

- `JU_METHOD_VALIDATION` 已全局关闭；
- `PLATE_PAIRING_VALIDATION` 已全局关闭；
- calendar equivalence 已解决到未来 Batch Freeze；
- Batch 已准备好；
- signal 有预测价值。

只要 `CHAI_BU_FUTOU` 实现、QimenEngine blob、17:00 freeze time 或 CORE signal 定义发生变化，本审计必须重新运行，旧结构频率不得继承。

## 10. 当前可安全使用的数字

可以说：

> 对 QimenEngine V02 blob `046825e480422eb0ac6734ea0330861bbd422997`、CHAI_BU_FUTOU、17:00 HKT，在 2000-01-01 至 2099-12-31 的 36,525 个真实 civil dates 中，CORE_RAIN_SIGNAL_V01 结构性触发 6,498 日（17.79055441%）。该 signal 对节气、元和阴阳九局高度不均匀。该结果由 K2 App UI CI #86 在无 weather forecast/outcome 数据条件下重新生成。

不可以说：

- 它有17.79%的天气准确率；
- 奇门每5.6天预测一次雨；
- V01/V02 总数相同证明旧 whole-day Engine 正确；
- 未来 Batch 只需按17.79%反推样本天数；
- M2 若优于 M1 就证明奇门产生了独立于日历的额外信息。
