# K2 CDAF-H2 Weather Pilot — Pre-Batch Gate Amendment v0.4

状态：`ACTIVE_AUTHORITY / V01_V02_V03_HISTORY_PRESERVED / ENGINE_V03_REAUDIT_COMPLETE / WEATHER_RELEVANT_STRUCTURAL_EQUIVALENCE_VERIFIED / BATCH_NOT_READY`  
基础设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
历史 authority：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01_GATE_AMENDMENT.md`、`...V02.md`、`...V03.md`  
JuMethod review：`knowledge/K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md`  
Gate A review：`knowledge/K2_QIMEN_GATE_A_ORTHOGONALIZATION_REVIEW_V01.md`  
值使门 correction review：`knowledge/K2_QIMEN_ZHISHI_GATE_SOURCE_REVIEW_V01.md`  
active model candidate：`FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V03`  
QimenEngine blob：`3a741348b46a43ef1f2e2bffe7c0a8be12ec42cd`  
Empirical Credit：`NONE`

## 1. Why V04 exists

V03 weather authority 正确地把 exact `QimenEngine` blob 当作冻结身份的一部分。随后 canonical `QM-SRC-0017` p24-p25 visual review 暴露了一个不属于 weather CORE、但属于同一 Engine 的值使门实现错误：旧代码在时宫顺逆计数经过中五时直接跳过 5，而 source p25 明确按 `6 -> 5 -> 4 -> 3 -> 2` 计数。

本项目没有因为“weather CORE 不读八门”就忽略这次变更。相反，旧 V02 whole-engine pin 正确 fail closed：

```text
ANY_ENGINE_BLOB_CHANGE
    => ACTIVE_WEATHER_MODEL_IDENTITY_CHANGED
    => PRE_BATCH_REPIN_REQUIRED
    => STRUCTURE_AUDITS_MUST_RERUN
```

因此：

```text
V03 authority = historical state before source-grounded gate correction
V04 authority = active state after Engine V03 repin and re-audit
```

## 2. Source-grounded gate correction

载体：`QM-SRC-0017` 费秉勋《奇门遁甲新述》  
canonical SHA-256：`f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`

visual review：

- printed p24 / PDF p33：阳遁一局丙寅时，休门值使随时宫落震3；
- printed p25 / PDF p34：阴遁九局戊戌时，开门值使从乾6逆数，明确经过中五，最终落坤2；
- 最终时宫为中五时，门再寄坤2；“途中经过 5”不能与“最终 5 寄宫”混为一件事。

fail-first fixture commit：`fa433339fabd7a6dcd649974ea0fb50ad79867fd`。

Knowledge Engine #827：

```text
阳1 / 丙寅 / 休门 -> 震3    PASS
阴9 / 戊戌 / 开门 -> 坤2    FAIL
61 tests / 1 failed
```

最小修复 commit：`3b695096a997f661091b72e524b182ac5d6235eb`。

Knowledge Engine #828：`SUCCESS`。

该 correction 的完整边界见：

`knowledge/K2_QIMEN_ZHISHI_GATE_SOURCE_REVIEW_V01.md`

## 3. Weather dependency boundary

`CORE_RAIN_SIGNAL_V01` 只消费：

```text
palace
九星
Gong.tianGan carried heaven stem
```

它不读取：

```text
renMen
shenPan
吉凶格局
值使门 target
```

因此本轮 correction 没有直接修改 weather feature definition。

但“没有直接依赖”不等于“可以跳过 re-audit”。whole-engine blob 已改变，所以 V02 数值只作为 frozen historical comparator；V03 必须由新 blob 独立重算后才能获得结构等价信用。

## 4. Engine V03 repin

active candidate：

```text
MODEL = FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V03
ENGINE_GIT_BLOB = 3a741348b46a43ef1f2e2bffe7c0a8be12ec42cd
JU_METHOD = CHAI_BU_FUTOU
CORE_SIGNAL = CORE_RAIN_SIGNAL_V01
BATCH = NONE
FREEZE = NONE
OUTCOME = NONE
```

old V02 candidate 不删除；其历史 audit 保留并作为 V03 regression comparator，但不冒充当前 V03 machine result。

## 5. V03 re-audit results

本节结果来自 current Engine blob 的实际机器重算。没有读取 HKO forecast 或 rainfall outcome；全部 `empirical_credit=NONE`。

### A. Abstract weather state-space — PASS

K2 Qimen Cognitive Reconstruction #223：`SUCCESS`。

```text
nominal_states              = 360
core_trigger_states         = 64
state_space_density         = 0.17777777777777778
hit_cardinality             = 1 on every trigger state
per_jieqi_nominal_distribution = unchanged vs V02
```

machine audit 同时重新验证 source-grounded QM-SRC-0021 star/heaven-stem pairing fixture 在新 blob 上仍 PASS。

### B. Real civil calendar — PASS / V02 comparator exact match

K2 App UI #131 重新运行 `QimenWeatherRealCalendarAuditTest`，artifact：

`qimen-weather-real-calendar-audit-v03.json`

```text
calendar_window             = 2000-01-01 / 2099-12-31
civil_time_hkt              = 17:00
qimen_ju_method             = CHAI_BU_FUTOU
engine_blob                 = 3a741348b46a43ef1f2e2bffe7c0a8be12ec42cd
v02_weather_relevant_structure_equivalent = true

total_civil_days            = 36525
core_signal_days            = 6498
civil_date_trigger_rate     = 0.17790554414784393
max_consecutive_trigger_days = 4
max_non_trigger_gap_days    = 33
max_hits_in_one_day         = 1

yuan days                   = 上元 12175 / 中元 12175 / 下元 12175
yuan triggers               = 上元 1813 / 中元 1850 / 下元 2835
```

24 节气 day-count / trigger-count、100 年逐年 trigger counts、18 个阴阳遁×局数 day/trigger counts 也由 test 与 V02 frozen comparator 比对通过。

### C. Calendar-equivalence controls — PASS / schedule identity preserved

K2 App UI #131 重新运行 `QimenWeatherCalendarEquivalenceAuditTest`，artifact：

`qimen-weather-calendar-equivalence-audit-v03.json`

```text
complete_segment_count      = 2399
complete_segment_days       = 36510
segment_length              = 14..16 days
mixed_segments              = 2000
all_zero_segments           = 399
all_one_segments            = 0

original_triggers           = 6498
plus_1_triggers             = 6498
minus_1_triggers            = 6498
plus_1_hamming_days         = 10344
minus_1_hamming_days        = 10344

audit_schedule_sha256       = e7ccd47461a5f75b3e89ffcf2743ab6939521ad27a493ecd6cebf39517ba845f
future_batch_schedule_frozen = false
```

该 SHA-256 与 V02 frozen comparator 完全一致，因此不是只比较 aggregate totals；完整节气段内 original / +1 / -1 signal schedule 也保持同一结构身份。

### D. Correct interpretation

A/B/C 全部一致后，现在可以记录：

`WEATHER_RELEVANT_STRUCTURAL_EQUIVALENCE_V02_TO_V03 = VERIFIED`

但严禁扩张为：

```text
FULL_ENGINE_EQUIVALENCE = VERIFIED
FULL_QIMEN_VALIDATION = VERIFIED
PREDICTIVE_VALIDITY = VERIFIED
```

值使门逻辑已经有意改变，所以 whole-engine 本来就不等价；这里验证的只是 CDAF-H2 weather-v0.1 实际消费的结构在 V02→V03 之间没有漂移。

## 6. Gate 0 / Gate A remain narrow

本轮值使门修复不撤销已经获得的窄信用：

```text
Gate 0 = CLOSED_FOR_WEATHER_V01_CHAIBU_METHOD_IDENTITY
Gate A = CLOSED_FOR_WEATHER_V01_STAR_HEAVEN_STEM_CONSTRUCTION
```

原因是本轮没有修改这两个 gate 对应的来源对象本身，而且新 blob 下的 source fixtures 已重新通过。

但完整门盘成熟度不能因为新 p24-p25 fixture 通过而升级：

```text
GLOBAL_GATE_BOARD_VALIDATION = NOT_CLAIMED
GLOBAL_PLATE_VALIDATION = NOT_CLAIMED
FULL_QIMEN_MATURITY = EXPERIMENTAL
```

两例只能证明当前 center-counting/hosting correction 与该 canonical source 一致。

## 7. Gate B / Gate D remain blockers

V04 不改变真实 Batch 的最靠前 blockers：

```text
Gate B = future Batch exact +/-1 sham schedule not frozen
Gate D = Batch horizon/start/station-panel/statistical contract not frozen
```

这里的 `audit_schedule_sha256` 只是 2000-2099 structure audit identity，明确 `future_batch_schedule_frozen=false`；不能偷换成未来 prospective Batch Freeze。

V03 re-audits 全部 PASS 也不自动创建 Batch。

## 8. Current active status after re-audit

```text
JU_METHOD_VALIDATION                 = CLOSED_NARROWLY
PLATE_PAIRING_VALIDATION             = CLOSED_NARROWLY_FOR_STAR_HEAVEN_STEM
ZHISHI_CENTER_COUNT_SOURCE_FIXTURE   = PASS_AFTER_FAIL_FIRST_CORRECTION
ENGINE_V03_CORE_REGRESSION           = PASS
ABSTRACT_WEATHER_V03_REAUDIT         = PASS
REAL_CALENDAR_V03_REAUDIT            = PASS
CALENDAR_EQUIVALENCE_V03_REAUDIT     = PASS
WEATHER_RELEVANT_V02_V03_EQUIVALENCE = VERIFIED

BATCH_READY                          = false
BATCH                                = NONE
FREEZE                               = NONE
OUTCOME                              = NONE
EMPIRICAL_CREDIT                     = NONE
CLAIM_EXTRACTION                     = BLOCKED
```

## 9. Repository / Android acceptance closure at this checkpoint

Exact source head before this documentation-only closure commit：

`cff35f3e3cbd1934c1d18470ad91a7a71a9d42e5`

五套机器门禁均完成：

```text
K2 Qimen Cognitive Reconstruction #223 = SUCCESS
K2 QCIC v0.6 Machine Gates #292        = SUCCESS
Knowledge Engine V1 CI #836            = SUCCESS
K2 App UI CI #131                       = SUCCESS
V1.0 Emulator Acceptance #43            = SUCCESS
```

Android 35 / API 35 emulator acceptance：

```text
NARROW / LIGHT = 5 tests, 0 skipped, 0 failed
WIDE / DARK    = 5 tests, 0 skipped, 0 failed
narrow evidence screenshots pulled = 16
wide evidence screenshots pulled   = 16
```

这提供产品/布局 instrumentation credit，不提供玄学有效性信用，也不替代真实 Moto X30 Pro physical-device acceptance。

CI 中仍有非阻塞维护警告：当前 Android Gradle Plugin 8.5.2 官方测试上限为 compileSdk 34，而项目 compileSdk=35；另有 emulator console 5554 启动提示，但 ADB、Android boot 与两轮 `connectedDebugAndroidTest` 均实际成功。警告保留为工程维护债，不改写成验收失败，也不静默删除。

任何后续 Engine / CORE / JuMethod / sham / sample-stat contract 变化，继续执行同一 fail-closed 规则：重新升 model/version、重新审计，历史结果不得回填。
