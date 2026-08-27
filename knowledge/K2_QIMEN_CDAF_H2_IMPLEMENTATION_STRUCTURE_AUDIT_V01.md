# K2 CDAF-H2 天气信号实现结构审计 v0.1

状态：`STRUCTURE_ONLY / NO_OUTCOME_DATA / NOT_EMPIRICAL_VALIDATION`  
关联假设：`CDAF-H2`  
关联设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
审计脚本：`tools/test_k2_qimen_weather_structure_audit.py`  
Empirical Credit：`NONE`  
Batch：`NONE`

## 1. 本审计回答什么

本审计只回答一个工程问题：

> 在当前被冻结的 QimenEngine 实现合同中，若每天固定 17:00 HKT 起局，`CORE_RAIN_SIGNAL_V01` 本身有多稀疏？

它不读取：

- 历史降雨结果；
- HKO 历史 PSR 命中情况；
- 任何结果后的天气叙事。

因此这里得到的数字没有 empirical credit，也不是“奇门天气有效率”。

## 2. 引擎锁定

审计锁定当前 `QimenEngine.kt` Git blob：

`028747358ba78507d17b77e906222bb6739c0c32`

脚本会按 Git blob 算法重新计算本地文件 SHA；若引擎文件发生任何变化，审计直接失败，要求重新检查，而不是继续复用旧频率。

这条锁的意义是：

`implementation frequency belongs to one exact engine implementation`

而不是把旧数字错误迁移到未来修改后的盘法。

## 3. 为什么不需要历史日期或天气数据

17:00 HKT 固定属于酉时。

按五鼠遁，酉时干只有五个状态：

`癸酉 / 乙酉 / 丁酉 / 己酉 / 辛酉`

它们以 5 日为周期重复，因此任意连续 5 个日干日中，这五个酉时状态各出现一次。

当前 `CHAI_BU_DAYCOUNT` 实现又只接受节气内：

- 第 1–5 日：上元；
- 第 6–10 日：中元；
- 第 11–15 日：下元；
- 第 16 日及以后：fail closed。

所以在引擎允许的合同状态中，每个节气可写成：

`3个元 × 5个酉时状态 = 15 states`

24 节气合计：

`24 × 3 × 5 = 360 engine-eligible contract states`

这里枚举的是合同状态空间，不是假装已经遍历真实公历年份。

## 4. CORE_RAIN_SIGNAL_V01 实现重建

审计脚本不修改 `QimenChart` API，也不向 `Gong` 新增尚未黄金盘验证的 `tianGan` 字段。

它只按当前锁定引擎内部已有算法，重建 weather-v0.1 所需的 `tianYi`，然后检查：

```text
EXISTS star IN {天柱, 天蓬}
SUCH THAT
  star.heaven_plate_carried_stem IN {壬, 癸}
  AND star.palace IN {1, 3, 6, 7}
```

这叫 **implementation reconstruction**，不能被重新命名为“经典盘法已经验真”。

## 5. 结构审计结果

总 engine-eligible contract states：`360`

`CORE_RAIN_SIGNAL_V01 = TRUE`：`64`

实现合同触发率：

`64 / 360 = 17.777777...%`

等价为平均：

`每 5.625 个 engine-eligible contract states 出现 1 次 core signal`

这仍然不是实际 weather batch 的 M1/M2 discordant rate，因为 M2 只有在：

`M1 == NO_RAIN10 AND core signal == TRUE`

时才真正改变 M1。

因此真实 paired-information opportunity 一定不高于 17.78%，具体多低目前未知，不能从这里猜。

## 6. 节气分布不是均匀的

每个节气的分母固定为 15 个合同状态。触发数如下：

| 节气 | trigger / 15 |
|---|---:|
| 冬至 | 0 |
| 小寒 | 2 |
| 大寒 | 5 |
| 立春 | 2 |
| 雨水 | 5 |
| 惊蛰 | 0 |
| 春分 | 5 |
| 清明 | 0 |
| 谷雨 | 2 |
| 立夏 | 0 |
| 小满 | 2 |
| 芒种 | 5 |
| 夏至 | 4 |
| 小暑 | 2 |
| 大暑 | 3 |
| 立秋 | 2 |
| 处暑 | 3 |
| 白露 | 4 |
| 秋分 | 3 |
| 寒露 | 4 |
| 霜降 | 2 |
| 立冬 | 4 |
| 小雪 | 2 |
| 大雪 | 3 |

范围从 `0/15` 到 `5/15`，说明信号在当前实现中带有明显的节气结构。

## 7. 新发现：CALENDAR_CONFOUNDING_CONTROL 必须成为 Batch blocker

weather-v0.1 原本主要防的是：

- 结果后换天气规则；
- 多条天气口诀自由搜索；
- 外应与地域修正；
- 天气序列相关。

本次结构审计又揭示了一层：

`CORE_RAIN_SIGNAL_V01` 的触发机会本身随节气明显变化。

因此未来若 M2 比 M1 好，至少有两个竞争解释：

1. 奇门具体盘面结构确实提供了 M1 之外的信息；
2. 该 signal 只是间接编码了节气/季节，而 M1 的剩余误差恰好也有季节结构。

只比较 `M2 vs M1` 不能自动区分这两个解释。

因此 Batch 前新增硬门：

`CALENDAR_CONFOUNDING_CONTROL = OPEN`

后续必须预先冻结一种不读取 outcome 的控制，例如：

- M1.5：M1 + 明确的 calendar/season-only comparator；或
- 在节气/季节 strata 内构造保持触发率的 sham/negative-control signal；或
- 其他能把“日历季节信息”与“具体盘面映射”分开的预注册设计。

具体采用哪一种必须在 Batch 前确定，不能看结果后挑最有利的控制。

## 8. 另一个未关闭问题：PLATE_PAIRING_VALIDATION

`handoff/qimen/05_FIXTURES.jsonl` 当前没有完整九宫黄金盘；`06_CASES.md` 也记录 chart independently rebuilt = 0。

因此当前 `天柱/天蓬 — heaven-plate carried stem` 的配对仍是实现层候选，而不是已被 chart-only fixture 独立确认的盘面事实。

新增硬门：

`PLATE_PAIRING_VALIDATION = OPEN`

Batch 前至少需要建立可独立复核的 chart-only fixture，验证 weather signal 所依赖的九星位置与其所携天盘干配对。fixture 只记录盘面事实，不导入书中结果断语，也不能拿回溯案例命中率替代排盘验证。

## 9. 原有统计 blocker 仍然存在

`SERIAL_DEPENDENCE / SAMPLE_ADEQUACY = OPEN`

17.78% 不能直接变成“需要 30 天/60 天/100 天”。

原因有三：

1. 只有 M1=NO_RAIN10 且 signal=true 才产生 paired discordance；
2. 连续天气结果存在依赖；
3. signal 自身带节气结构。

所以 observation window 必须在以上两层结构问题关闭后，再根据真正的 information unit 设计。

## 10. 当前三重 Batch gate

截至本审计：

```text
PLATE_PAIRING_VALIDATION       = OPEN
CALENDAR_CONFOUNDING_CONTROL   = OPEN
SERIAL_DEPENDENCE_SAMPLE_GATE  = OPEN

BATCH_READY                    = false
BATCH                          = NONE
FREEZE                         = NONE
OUTCOME                        = NONE
EMPIRICAL_CREDIT               = NONE
```

没有任何一项可以因为 CI 通过而自动关闭。

## 11. 当前可以安全得出的结论

可以说：

> 对锁定的 QimenEngine 实现，weather-v0.1 core signal 在 360 个 engine-eligible 合同状态中触发 64 次，状态密度 17.78%，且触发机会随节气明显不均匀。

不可以说：

- 奇门约每 5.6 天预测一次雨；
- 这个信号有 17.78% 的准确率；
- 这个信号已经比 HKO 好；
- 传统天盘配对已经被程序证明；
- weather Batch 已准备完成。

下一步应先处理 `PLATE_PAIRING_VALIDATION` 与 `CALENDAR_CONFOUNDING_CONTROL`，而不是直接开始收 outcome。
