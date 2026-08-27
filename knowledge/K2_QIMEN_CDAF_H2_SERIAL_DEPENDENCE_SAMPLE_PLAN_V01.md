# K2 CDAF-H2 Serial Dependence / Sample Adequacy Plan v0.1

状态：`DESIGN_DEFINED / NOT_BATCH_FROZEN / NO_OUTCOME_DATA`  
关联假设：`CDAF-H2`  
关联 weather design：`K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
Gate amendment：`K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01_GATE_AMENDMENT.md`  
Calendar control：`K2_QIMEN_CDAF_H2_CALENDAR_EQUIVALENCE_CONTROL_V01.md`  
Empirical Credit：`NONE`

## 1. 为什么“跑 N 天”不是样本充分性

CDAF-H2 weather-v0.1 中，M2 只有在：

```text
M1 == NO_RAIN10
AND CORE_RAIN_SIGNAL_V01 == TRUE
```

时才与 M1 分叉。

Calendar-equivalence control 又增加：

```text
M2_ORIGINAL
M2_SHAM_PLUS_1
M2_SHAM_MINUS_1
```

因此 365 个 civil dates 绝不等于 365 个独立信息样本。真正决定可识别性的，是：

- baseline 是否为 `NO_RAIN10`；
- original / sham signals 是否导致预测分叉；
- outcome 是否最终 evaluable；
- 分叉是否集中在连续天气过程；
- 是否覆盖完整季节周期。

连续天气具有显著 serial dependence，故不得把每日 paired outcomes 直接视为独立 Bernoulli observations。

## 2. 候选日与分析日

候选 cadence 仍固定为：

```text
每日读取 HKO 16:30 D+1 PSR
17:00 HKT 冻结 M1 / Qimen plate / original+sham predictions
```

`PSR=Medium` 或无法可靠取得 16:30 snapshot 的日期，按既有 protocol 在 Outcome 前即为 `INELIGIBLE`。

其余符合 protocol 的日期进入冻结时间轴。

Outcome 打开后，若冻结 station panel 任一站点缺失或 completeness 非 C，则该日：

`UNEVALUABLE`

不得把它回写成事前排除。

## 3. 三个预先定义的信息计数

这些计数全部只依赖冻结预测，不依赖天气 Outcome，因此可以用于 non-outcome-driven stopping。

### 3.1 Original vs M1

```text
INFO_ORIGINAL_M1(D) =
    eligible(D)
    AND M1(D) == NO_RAIN10
    AND CORE_ORIGINAL(D) == TRUE
```

因为只有这时 M2_ORIGINAL 与 M1 的预测不同。

### 3.2 Original vs +1 sham

```text
INFO_ORIGINAL_PLUS(D) =
    eligible(D)
    AND M1(D) == NO_RAIN10
    AND CORE_ORIGINAL(D) != SHAM_PLUS_1(D)
```

### 3.3 Original vs -1 sham

```text
INFO_ORIGINAL_MINUS(D) =
    eligible(D)
    AND M1(D) == NO_RAIN10
    AND CORE_ORIGINAL(D) != SHAM_MINUS_1(D)
```

这些是“预测分叉机会数”，不是独立样本数、不是成功数，也没有 empirical credit。

## 4. 为什么最低信息门槛设为 80

v0.1 固定：

```text
MIN_PREOUTCOME_INFO_PER_CONTRAST = 80
```

这个数字不是从 weather Outcome 调出来的，也不是“80例就证明有效”。

其作用只是阻止在极少 prediction-discordant days 下做强结论。作为规划尺度，若错误地暂时假设独立 Bernoulli，单侧 exact sign-test 在 `H0:p=0.5`、目标 `p=0.65`、alpha=0.05 下，大约 69 个 discordant observations 才达到约 80% nominal power。项目把 planning floor 向上取整为 80，并另外使用完整季节周期与 serial-dependence correction；因此 80 不能解释成最终统计保证。

正式推断不使用“80个独立样本”的假设。

## 5. 时间覆盖：完整 24 节气周期，而不是任意天数

Batch 必须从一个由冻结 engine 判定的**真实节气段起点**开始。

第一阶段固定采集：

```text
48 个完整连续 solar-term segments
```

即两个完整 24 节气周期。这样每个节气名称在最小 horizon 中恰好出现两次，不因从某个季节开始就只覆盖偏向性月份。

第 48 段结束时，**在仍未读取 Outcome 的情况下**检查三个 pre-outcome information counts。

若三者全部：

```text
>= 80
```

则 Batch acquisition 关闭，随后才允许进入 Outcome ingestion。

若任一不足 80，不允许逐日滚动到“刚好够”；只能事前规则化地增加**一个完整 24 节气周期**：

```text
MAX_SEGMENTS = 72
```

第 72 段结束时无条件关闭 acquisition。

如果此时 pre-outcome information counts 仍有任一 `<80`：

`BATCH_RESULT_CLASS = INSUFFICIENT_INFORMATION`

无需为了制造结果打开 Outcome。

## 6. Outcome 必须在 acquisition 关闭后统一打开

为了阻止 optional stopping：

- acquisition 期间可以读取并冻结 HKO forecast snapshot；
- 可以计算 calendar/Qimen/original/sham predictions；
- 可以累计三个 pre-outcome information counts；
- **不得读取目标日 rainfall outcome 进入研究表**；
- 不得依据任何已知 correct/incorrect 结果决定是否延长到第三周期。

公开 Outcome 即使现实中已经存在，也必须保持在研究流程之外，直到 acquisition 被第5节规则关闭。

如果 Outcome ingestion 后，因为 station completeness 导致 evaluable information counts 下降到任一 `<80`：

`BATCH_RESULT_CLASS = INSUFFICIENT_INFORMATION_AFTER_OUTCOME_QC`

同一个 Batch 不得重新开放 acquisition 补样本。需要继续只能创建新 Batch/version，并保留旧结果。

## 7. 每日 paired score

对每个 `EVALUABLE` eligible civil date：

```text
score(model, D) = 1  if frozen_prediction(model,D) == frozen_outcome(D)
                  0  otherwise
```

三个固定 contrast：

```text
d_M1(D)    = score(M2_ORIGINAL,D) - score(M1,D)
d_PLUS(D)  = score(M2_ORIGINAL,D) - score(M2_SHAM_PLUS_1,D)
d_MINUS(D) = score(M2_ORIGINAL,D) - score(M2_SHAM_MINUS_1,D)
```

每个 `d` 只能为 `-1 / 0 / +1`。

Primary estimands 是所有 evaluable eligible dates 上的：

```text
DELTA_M1    = mean(d_M1)
DELTA_PLUS  = mean(d_PLUS)
DELTA_MINUS = mean(d_MINUS)
```

因此没有预测分叉的日期保留为 `0`，不会被删除来放大效果。

同时报告：

- `unique_correction_count`；
- `unique_degradation_count`；
- 每个 contrast 的 evaluable discordant count；
- 每个节气的 paired delta；
- UNEVALUABLE rate。

这些 secondary diagnostics 不得替换 primary estimands。

## 8. Serial dependence：固定 30 日 calendar-lag HAC

v0.1 不使用普通独立样本标准误。

三个 daily paired-difference series 都使用相同的：

```text
HAC_KERNEL   = Bartlett
HAC_MAX_LAG  = 30 civil days
```

30 日约覆盖两个连续节气段，用于保留短中期天气持续性。该 lag 在 Outcome 前固定，不允许结果后改成 7/14/60 日挑显著值。

对于存在 INELIGIBLE / UNEVALUABLE 日期的情况，lag 按**真实 civil-date difference**计算，不把剩余观测重新编号后假装连续。

对 contrast `c`，设 evaluable paired differences 为 `d_t`、总数 `N`、均值 `d_bar`：

```text
gamma_0 = (1/N) * SUM_t (d_t - d_bar)^2

gamma_h = (1/N) * SUM_{(t,s): date(s)-date(t)=h}
                    (d_t-d_bar)(d_s-d_bar)

w_h = 1 - h/(HAC_MAX_LAG+1)

Omega = gamma_0 + 2 * SUM_{h=1..30} w_h * gamma_h
SE_HAC(d_bar) = sqrt(max(0, Omega) / N)
```

同一实现必须用于 M1、+1 sham、-1 sham 三个 contrast。

## 9. 三重比较的 family-wise control

Plate-alignment credit 要同时通过三个方向：

```text
M2_ORIGINAL > M1
M2_ORIGINAL > M2_SHAM_PLUS_1
M2_ORIGINAL > M2_SHAM_MINUS_1
```

因此不能对三个 0.05 单侧检验各自独立报喜。

v0.1 固定 family-wise alpha：

```text
FWER_ALPHA = 0.05
NUMBER_OF_PRIMARY_CONTRASTS = 3
BONFERRONI_ONE_SIDED_ALPHA = 0.05 / 3
Z_CRITICAL = 2.1280452342
```

对每个 primary delta：

```text
LOWER_BOUND_c = DELTA_c - Z_CRITICAL * SE_HAC_c
```

不得在 Outcome 后改用未预注册的 p-value、bootstrap、lag 或只保留通过的 contrast。

## 10. Batch Review 判据

只有在：

1. acquisition 按 48/72 segment rule 正常关闭；
2. Outcome QC 后三个 evaluable information counts 均 `>=80`；
3. protocol / station panel / JuMethod / engine / sham schedule 无 drift；
4. `LOWER_BOUND_M1 > 0`；
5. `LOWER_BOUND_PLUS > 0`；
6. `LOWER_BOUND_MINUS > 0`；

时，才允许：

```text
BATCH_REVIEW_CLASS = PLATE_ALIGNMENT_INCREMENT_CANDIDATE
```

这仍不是“奇门有效”或机制证明，只允许进入复制与 Batch Review。

若信息充分但：

```text
DELTA_M1 <= 0
```

或 `unique_degradation >= unique_correction`，则：

`BATCH_REVIEW_CLASS = NO_SYMBOLIC_INCREMENT`

若 `DELTA_M1 > 0`，但 original 未同时胜过两套 sham：

`BATCH_REVIEW_CLASS = CALENDAR_ALIGNMENT_NOT_DISTINGUISHED`

若三个 point estimates 均为正，但任一 adjusted HAC lower bound `<=0`：

`BATCH_REVIEW_CLASS = INCONCLUSIVE`

任何单节气、单案例、单次暴雨命中不得覆盖这些批次规则。

## 11. 当前 Gate D 状态

```text
SAMPLING_CADENCE_DEFINED             = true
ANALYSIS_UNIT_DEFINED                = true
PREOUTCOME_STOPPING_RULE_DEFINED     = true
MIN_INFORMATION_THRESHOLD_DEFINED    = true
SERIAL_DEPENDENCE_METHOD_DEFINED     = true
PRIMARY_STATISTIC_DEFINED            = true
MULTIPLICITY_CONTROL_DEFINED         = true
SUCCESS_FAILURE_INSUFFICIENT_DEFINED = true

BATCH_SPECIFIC_START_SEGMENT         = NONE
BATCH_SPECIFIC_48_72_HORIZON         = NOT_FROZEN
OUTCOME_PANEL_FREEZE                 = NONE
BATCH                                = NONE
OUTCOME                              = NONE
EMPIRICAL_CREDIT                     = NONE
```

因此 Gate D 的**方法设计问题**已经定义，但在实际 Batch 起始节气段、station panel、engine/JuMethod、calendar sham schedule 与本文件 hash 一起进入 Freeze 前，不能标为 Batch-ready closed。
