# K2 CDAF-H2 Calendar Equivalence Control v0.1

状态：`V02_MACHINE_STRUCTURE_VERIFIED / NOT_BATCH_FROZEN / NO_OUTCOME_DATA`  
关联假设：`CDAF-H2`  
关联 weather design：`K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
真实公历审计：`K2_QIMEN_CDAF_H2_REAL_CALENDAR_AUDIT_V01.md`  
机器结构测试：`ziwei-core/src/test/kotlin/com/xuanxue/qimen/QimenWeatherCalendarEquivalenceAuditTest.kt`  
active model：`FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02`  
QimenEngine blob：`046825e480422eb0ac6734ea0330861bbd422997`  
Empirical Credit：`NONE`

## 1. 问题升级：不是普通“季节混杂”而已

weather-v0.1 的 M2 没有读取独立于时间的新外部观测。

它的输入链是：

```text
civil datetime
    -> 干支 / 节气 / 阴阳遁 / 元 / 局
    -> Qimen plate
    -> CORE_RAIN_SIGNAL_V01
```

因此 `CORE_RAIN_SIGNAL_V01` 是时间输入的确定性变换。

这意味着任何 M2 优势都至少存在一个等价解释：

> 某个特定的 calendar/time feature transform 恰好对目标有预测价值。

所以未来不能把 `M2 > M1` 直接写成“奇门获得了日历之外的新信息”。

## 2. 本控制真正检验什么

本控制只检验更窄的问题：

> 在保持节气层级触发数量和局部时间结构时，原始 CORE_RAIN_SIGNAL 的**精确日期相位**是否比相邻 calendar sham 更有区分力？

如果没有，那么 observed improvement 更可能来自：

- 季节/节气 propensity；
- 一段时间内本来就较高的降雨基础率；
- 邻近日天气 persistence；
- 或更一般的 calendar/time structure；
- 而不是这个具体盘面映射恰好落在这一天。

## 3. Solar-term-segment phase shams

对未来 Batch 中每一个完整、实际发生的节气段 `S`：

1. 在不读取任何 HKO forecast/outcome 的情况下，预先用冻结 engine+JuMethod 计算该段每日 `CORE_RAIN_SIGNAL_V01`；
2. 得到二值序列：

```text
C_S = [c1, c2, ..., cn]
```

3. 定义两个固定 negative controls：

```text
SHAM_PLUS_1(S)[i]  = C_S[(i + 1) mod n]
SHAM_MINUS_1(S)[i] = C_S[(i - 1) mod n]
```

也就是在**同一真实节气段内部循环平移一天**。

## 4. 为什么不能用全局随机 shuffle

全局随机 shuffle 会破坏：

- 节气触发倾向；
- 季节结构；
- 局部 trigger clustering；
- signal 在特定节气中的零触发边界。

那样的 sham 太容易被 original 打败，不能形成有意义的负对照。

节气段内 ±1 日循环平移具有以下性质：

- 每一节气段 trigger 数量完全相同；
- 每一节气段 trigger rate 完全相同；
- trigger run structure 主要发生相位移动，不重新估计参数；
- 不读取 weather outcome；
- 不根据未来表现选择 shift；
- 专门破坏“今天这个盘对应今天 outcome”的 exact alignment。

## 5. 三个候选模型必须共用同一个 M1

对每一个 eligible case：

```text
M1 = HKO/context baseline
```

原始 M2：

```text
IF M1 == NO_RAIN10 AND CORE(D) == TRUE:
    M2_ORIGINAL = RAIN10
ELSE:
    M2_ORIGINAL = M1
```

正相位 sham：

```text
IF M1 == NO_RAIN10 AND SHAM_PLUS_1(D) == TRUE:
    M2_SHAM_PLUS_1 = RAIN10
ELSE:
    M2_SHAM_PLUS_1 = M1
```

负相位 sham：

```text
IF M1 == NO_RAIN10 AND SHAM_MINUS_1(D) == TRUE:
    M2_SHAM_MINUS_1 = RAIN10
ELSE:
    M2_SHAM_MINUS_1 = M1
```

三者不得拥有不同的 HKO snapshot、outcome proxy、exclusion rule 或评分规则。

## 6. Plate-alignment credit 的必要条件

未来不能只要求：

`M2_ORIGINAL > M1`

若要讨论“精确 plate alignment 有增量”，至少还必须满足：

```text
M2_ORIGINAL > M2_SHAM_PLUS_1
AND
M2_ORIGINAL > M2_SHAM_MINUS_1
```

比较必须使用同一事前冻结的 paired loss / decision rule，并服从同一 serial-dependence treatment。

如果 original 只胜 M1、却没有稳定胜过 ±1 sham，则：

`PLATE_ALIGNMENT_CREDIT = NONE`

## 7. 即使 original 胜过两个 sham，也仍不能证明什么

即使未来 original 同时优于两套 sham，也只能说：

> 在这个预注册模型类、时间窗和 outcome 下，原始 Qimen-derived calendar transform 的 exact phase 比两个相邻 phase controls 更有区分力。

仍不能直接推出：

- 奇门获得独立于时间的信息；
- 玄学机制被证明；
- 所有奇门天气规则有效；
- 结果可推广到其他地区、阈值或问题域。

因为 original 与 shams 仍来自同一个 calendar/time information set。

## 8. 防止 control shopping

v0.1 只允许：

- `+1日`
- `-1日`

不得在看 Outcome 后再尝试：

- +2 / +3 / +5；
- 只保留表现最差的 sham；
- 改成随机 shuffle；
- 改节气 strata；
- 改成月度/季节 strata；
- 删除边界日。

任何新的 negative-control family 都必须成为后续新 model/plan version，进入后续新 Batch，不得回填当前设计。

## 9. 节气边界如何处理

循环只发生在**同一次实际节气段内部**，不是把同名节气跨年份混在一起。

segment identity 必须至少包含：

```text
segment_start_datetime_hkt
jieqi_name
engine_blob_sha
qimen_ju_method
```

V02 关键修正是：节气所属段由 exact transition Engine 决定，不再用 whole-day semantics。若某节气在17:00以后交接，17:00 civil-date state 仍留在前一节气段；若在17:00前交接，则进入新段。不得人工按 civil date 标签覆盖 Engine boundary。

## 10. V02 机器结构审计结果

当前 pinned implementation：

```text
active model       = FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02
QimenEngine blob   = 046825e480422eb0ac6734ea0330861bbd422997
JuMethod           = CHAI_BU_FUTOU
civil time         = 17:00 HKT
calendar window    = 2000-01-01 .. 2099-12-31
report             = qimen-weather-calendar-equivalence-audit-v02.json
GitHub Actions run = 33264988516 / K2 App UI CI #86 / SUCCESS
```

机器测试向窗口两端各扩40日，只用于识别被窗口边界截断的真实节气段；正式统计只纳入完整落在100年窗口内的连续节气段。

V02 结果：

```text
complete_segment_count = 2399
complete_segment_days  = 36510
min_segment_days       = 14
max_segment_days       = 16
mixed_segments         = 2000
all_zero_segments      = 399
all_one_segments       = 0

original_triggers      = 6498
plus_1_triggers        = 6498
minus_1_triggers       = 6498

plus_1_hamming_days    = 10344
minus_1_hamming_days   = 10344

audit_schedule_sha256 = e7ccd47461a5f75b3e89ffcf2743ab6939521ad27a493ecd6cebf39517ba845f
```

并且 24 个节气逐项满足：

```text
original_triggers_by_jieqi
== plus_1_triggers_by_jieqi
== minus_1_triggers_by_jieqi
```

因此 V02 当前已经机器验证：

1. sham 不跨真实连续节气段；
2. `+1/-1` 不改变每一完整节气段的 trigger count / propensity；
3. 两套 sham 都确实改变大量 civil-date exact alignments；
4. 生成过程不读取 HKO forecast；
5. 生成过程不读取 rainfall/outcome；
6. 100年 audit schedule hash 只是结构审计证据，不是未来 Batch Freeze hash。

这项通过获得的是：

`CONTROL_STRUCTURE_CREDIT`

不是：

`PLATE_ALIGNMENT_CREDIT`、`PREDICTIVE_CREDIT` 或 `EMPIRICAL_CREDIT`。

## 11. 为什么旧 V01 hash 必须作废，即使 trigger 总数没变

旧候选 whole-day Engine 与 V02 exact-transition Engine 都聚合得到 `6498` 个 original trigger days，但这不是版本等价证据。

V02 重算的 segment-level 结构已经变化：

```text
old complete_segment_days  = 36509
V02 complete_segment_days  = 36510

old hamming days           = 10352
V02 hamming days           = 10344

old audit schedule hash    = 2760b8e94ada03b0a9d0e2b6dcae6ef27b73df31089f741536eddb5ab29710da
V02 audit schedule hash    = e7ccd47461a5f75b3e89ffcf2743ab6939521ad27a493ecd6cebf39517ba845f
```

所以：

```text
SAME AGGREGATE COUNT != SAME CALENDAR ALIGNMENT
SAME AGGREGATE COUNT != SAME MODEL VERSION
```

旧 schedule/hash 不得作为 V02 provenance 复用。

## 12. 当前 gate 状态

```text
CALENDAR_EQUIVALENCE_CONTROL_PROTOCOL = DEFINED
CALENDAR_EQUIVALENCE_MACHINE_AUDIT    = VERIFIED_FOR_V02_PINNED_ENGINE
SHAM_SCHEDULE                         = NOT_BATCH_FROZEN
OUTCOME_DATA_USED                     = false
PLATE_ALIGNMENT_CREDIT                = NONE
EMPIRICAL_CREDIT                      = NONE
```

Gate B 的 control family 与机器结构可执行性已经在 V02 当前 Engine 上重新验证；但在未来 Batch horizon、engine、JuMethod 与实际节气段 schedule 真正冻结之前，**Batch-specific Gate B 仍保持 blocking**。

不能把这次100年结构审计的 `e7ccd4...` hash 直接拿来冒充未来实验 Freeze。
