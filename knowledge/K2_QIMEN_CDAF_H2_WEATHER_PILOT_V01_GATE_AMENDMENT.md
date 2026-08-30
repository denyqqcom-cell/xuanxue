# K2 CDAF-H2 Weather Pilot v0.1 — Pre-Batch Gate Amendment

状态：`ACTIVE_AMENDMENT / V02_RECONCILED / BATCH_NOT_READY`  
基础设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
抽象结构审计：`knowledge/K2_QIMEN_CDAF_H2_IMPLEMENTATION_STRUCTURE_AUDIT_V01.md`  
真实公历审计：`knowledge/K2_QIMEN_CDAF_H2_REAL_CALENDAR_AUDIT_V01.md`  
Calendar control：`knowledge/K2_QIMEN_CDAF_H2_CALENDAR_EQUIVALENCE_CONTROL_V01.md`  
Sample/serial plan：`knowledge/K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md`  
JuMethod cross-source review：`knowledge/K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md`  
active model：`FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02`  
QimenEngine blob：`046825e480422eb0ac6734ea0330861bbd422997`  
Empirical Credit：`NONE`

## 1. 为什么需要 amendment

基础 weather-v0.1 已经定义：

- 香港次日显著降雨窄域；
- HKO 16:30 PSR 作为 M1；
- `CORE_RAIN_SIGNAL_V01` 作为 M2 唯一新增信息；
- M2 只允许在 `M1=NO_RAIN10 && signal=true` 时改判；
- outcome proxy、入样、禁用修正规则等边界。

后续审计发现，正式 Batch 前不能只解决统计问题。还必须先回答：

1. 究竟使用哪一种定元法；
2. 该方法的来源身份与实际交节边界是否被充分验证；
3. weather signal 依赖的九星—所携天盘干是否由真实 Engine 的 source fixture 直接验证；
4. signal 的真实 civil-calendar 结构是什么；
5. Qimen-derived signal 与普通 calendar/time transform 在信息来源上能否区分；
6. serial dependence 与 sample adequacy 是否在 Outcome 前冻结。

本 amendment 不创建 Batch、不改写历史结果、不授予 empirical credit。

## 2. Gate 0 — JU_METHOD_VALIDATION

状态：`PARTIAL_MULTI_SOURCE_SHARED_STRUCTURE / IMPLEMENTATION_BOUNDARY_PASS / SOURCE_BOUNDARY_FIXTURE_OPEN / BLOCKING`

### 2.1 已修复：五日符头与六甲旬首不能混用

旧 `CHAI_BU_FUTOU` 曾用十日六甲旬首计算上中下元，把两个不同概念混为一谈：

- 六甲旬首：十个干支为一旬，用于旬首、遁干、旬空；
- 拆补符头：五日为一元，首日天干为甲或己，用于上中下元和局数。

当前 `yuanOfFutou()` 已回溯最近的五日甲/己符头；`xunInfo()` 的十日旬首算法保持独立。

Wave1 Evidence `K2E-W1-QM-0028-0016` 已记录：甲或己为每元首日天干，子午卯酉为上元、寅申巳亥为中元、辰戌丑未为下元。

### 2.2 已修复：实际交节时刻不能被 whole-day semantics 代替

来源层另保存了拆补法按实际交节时辰切换节气局数体系的规则。反审发现旧候选 Engine 使用 `getPrevJieQi(true)`，会让交节日从00:00起整体进入新节气。

当前 V02 已改用 exact transition family：

```text
getPrevJieQi(false)
```

并增加 implementation-only regression：

`QimenEngineTest.futouPreservesIntradaySolarTermBoundaryInsteadOfSwitchingAtMidnight`

测试在同一 2026-08-07 civil date 内寻找实际立秋 boundary，确认交节前仍为大暑、交节后为立秋；同一癸丑日、同一五日符头上元情况下，局数从阴7切到阴2。K2 App UI CI #86 中该测试 PASS。

但信用必须严格限制：boundary minute 由同一个 lunar-java calendar dependency 找出，因此这只证明 **Engine preserves intraday transition semantics**。它不是独立天文验证，也不是 source-grounded before/after boundary fixture。

所以：

```text
IMPLEMENTATION_BOUNDARY_PASS != SOURCE_BOUNDARY_VALIDATED
```

### 2.3 当前候选方法

weather-v0.1 的排盘方法候选固定为：

`WEATHER_JU_METHOD_CANDIDATE = CHAI_BU_FUTOU`

不能继续默认使用 App 的 `CHAI_BU_DAYCOUNT`，也不能在 Outcome 后切换方法寻找有利结果。

这只是候选方法冻结，不代表 `CHAI_BU_FUTOU` 已经全局验真。

### 2.4 当前已有 cross-source 结构证据

目前已有：

1. 12 类甲/己五日符头类别的 source-rule regression；
2. `辛丑 -> 最近符头己亥 -> 中元` 的算法反例，用于防止退回十日旬首实现；
3. QM-SRC-0021 的 2004-05-29 戊午时 chart-only anchor；
4. QM-SRC-0017 费秉勋《奇门遁甲新述》独立支持五日一局、甲/己为局头及上中下元地支分类；
5. QM-SRC-0017 PDF p17 的 `1990-01-27 壬辰 -> 己丑五日组 -> 大寒下元 -> 阳遁六局` dated structural example 已进入真实 QimenEngine regression；
6. V02 actual-transition implementation regression 已通过。

但 QM-SRC-0017 相关章节属于“超神接气和置闰”语境。它独立支持的是**共享五日甲/己符头子结构**与该 dated 元/局结果，不意味着费氏完整置闰法与 `CHAI_BU_FUTOU` 完全等价。

因此继续保留：

```text
SAME OUTPUT != SAME METHOD
SHARED SUBSTRUCTURE != METHOD EQUIVALENCE
```

### 2.5 2002 fixture 继续撤回

曾尝试加入 `2002-08-01 / 辛丑日 / 壬申时 / 阴遁一局` 作为第二 dated fixture。回查 Atomic Evidence 与 deep-source distillate 后，现有知识层没有保存足以支撑这组日期—时柱元数据的原页 provenance。

因此状态继续为：

`SOURCE_PAGE_REVERIFICATION_REQUIRED`

该断言已经从 Python plate-pairing fixture 的“独立来源元数据”中删除。不得为了让测试通过而把程序输出反写成原书事实，也不得把旧学习摘要当黄金盘。

### 2.6 证据粒度纪律

`SOURCE GRANULARITY MUST BE SUFFICIENT FOR THE ASSERTED CLAIM`

- 测试五日符头、元、局等日级方法结构：原页给出 civil date + 日干支 + 元/局关系即可；
- 测试完整 plate、值符值使、九星八门或时盘关系：必须有足够的来源时辰/时柱与盘面字段；
- 测试交节 boundary：必须有足以定位 boundary side 的 source-grounded 时间信息。

测试中自行选择的安全 clock time 只是 sampling parameter，不得回写成 source fact。

### 2.7 Gate 0 剩余关闭条件

Gate 0 关闭前仍至少需要：

- `CHAI_BU_FUTOU` 的 actual-transition policy 至少一个 source-grounded before/after boundary fixture，而不是只靠一般规则文字；
- 完整 method vector 把 `DAY_GROUPING / YUAN_CLASSIFICATION / SOLAR_TERM_POLICY / SUPER_CONNECT_POLICY / LEAP_POLICY / JU_LOOKUP` 分开；
- weather Plan 保持冻结 `qimen_ju_method = CHAI_BU_FUTOU` 与 exact V02 engine blob；
- 若后续来源支持另一方法，只能进入后续新 model/plan version，不得回填既有 Freeze；
- Gate A 所需完整 dated plate fixture 按更高字段粒度独立验证，不能由仅有日级元/局的1990例替代。

关闭前：

`WEATHER_BATCH_CREATION = FORBIDDEN`

## 3. Gate A — PLATE_PAIRING_VALIDATION

状态：`ONE_SOURCE_DATED_PLATE_DIRECT_KOTLIN_PAIRING_PASS / SECOND_INDEPENDENT_PLATE_OPEN / BLOCKING`

QM-SRC-0021 2004-05-29 戊午时 chart-only fixture 已经从“只核对星位”升级为真实 Kotlin `QimenEngine` 直接核对：

```text
palace -> (tianXing, Gong.tianGan)
```

外八宫 source expected pairs：

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

V02 同时把“九星所携天盘干”收回为 Engine 一等字段 `Gong.tianGan`。`QimenWeatherRealCalendarAuditTest` 和 `QimenWeatherCalendarEquivalenceAuditTest` 都直接读取该字段，已经删除 audit 内部重复实现的 `carriedHeavenStems()`。

Python `test_k2_qimen_plate_pairing_fixture.py` 继续作为 cross-language mirror/structure guard；它不再替代真实 Kotlin fixture 的 source-pairing credit。

这关闭的是“真实 Engine 完全没有 source-grounded star/heaven-stem pair assertion”的旧空洞，但不能把一张来源盘推广为“完整九宫全局已验证”。

Gate A 关闭前仍需要：

1. 至少再有一张独立 dated plate fixture，最好覆盖不同阴阳遁/局数；
2. fixture 包含足以核对的九星位置与天盘干 pairing；
3. 只验证盘面，不导入书中天气 outcome/断语；
4. weather signal 所依赖的天柱/天蓬—天盘干 pairing 与这些 fixture 一致；
5. 若来源 fixture 冲突，保留冲突并先修 Engine/protocol，禁止选择性覆盖。

因此：

`GLOBAL_PLATE_VALIDATION = NOT_CLAIMED`

## 4. Gate B — CALENDAR_EQUIVALENCE_CONTROL

状态：`V02_MACHINE_STRUCTURE_VERIFIED / BATCH_SCHEDULE_NOT_FROZEN / BLOCKING`

真实公历审计把问题从普通“季节混杂”提升成 calendar equivalence：

```text
civil datetime -> Qimen plate -> CORE_RAIN_SIGNAL_V01
```

当前 M2 没有引入独立于时间的新外部观测源。因此即使未来 `M2 > M1`，也不能直接解释为“奇门获得了日历之外的额外信息”。

v0.1 control family 继续冻结为：

- `M2_SHAM_PLUS_1`：每一次实际节气段内部把 CORE signal 序列循环平移 `+1日`；
- `M2_SHAM_MINUS_1`：同段循环平移 `-1日`。

两套 sham 保留同一节气段 trigger count / propensity，只破坏具体日期 exact alignment。

### 4.1 V02 机器结构验证

K2 App UI CI #86 / run `33264988516` 已在当前 V02 Engine 上重新执行 `QimenWeatherCalendarEquivalenceAuditTest`：

```text
active model           = FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02
QimenEngine blob       = 046825e480422eb0ac6734ea0330861bbd422997
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

24个节气逐项满足 original/+1/-1 trigger counts 完全相同；两套 sham 又都在 10,344 个 civil-date positions 上改变 exact alignment。生成过程没有读取 HKO forecast 或 rainfall outcome。

这证明的是：

`CONTROL_STRUCTURE_CREDIT`

不是：

`PLATE_ALIGNMENT_CREDIT / PREDICTIVE_CREDIT / EMPIRICAL_CREDIT`

### 4.2 为什么旧 V01 schedule 不能复用

旧 whole-day candidate 与 V02 exact-transition Engine 的 `original_triggers` 聚合值都恰好为6498，但 segment-level schedule 已发生变化：

```text
old complete_segment_days = 36509
V02                        = 36510

old hamming days           = 10352
V02                        = 10344

old schedule hash          = 2760b8e94ada03b0a9d0e2b6dcae6ef27b73df31089f741536eddb5ab29710da
V02 schedule hash          = e7ccd47461a5f75b3e89ffcf2743ab6939521ad27a493ecd6cebf39517ba845f
```

因此：

```text
SAME AGGREGATE COUNT != SAME ALIGNMENT
SAME AGGREGATE COUNT != SAME MODEL VERSION
```

旧 V01 hash 不得作为 V02 provenance。

### 4.3 Future plate-alignment credit

未来若要讨论 exact plate-alignment credit，必要条件至少是：

```text
M2_ORIGINAL > M2_SHAM_PLUS_1
AND
M2_ORIGINAL > M2_SHAM_MINUS_1
```

即使满足，也只能讨论“该预注册时间变换的精确相位在这个模型类中更有区分力”，不能宣称出现独立于时间的信息源。

Gate B 剩余 Batch-specific 条件：

- Batch horizon 冻结后重新生成该 Batch 的完整 sham schedule；
- schedule 生成只读取 calendar/engine，不读取 HKO forecast/outcome；
- segment identity、boundary、+1/-1 rule 与 schedule hash 进入 Freeze；
- original 与两套 sham 共用同一 M1、outcome、exclusion、loss 与 serial-dependence treatment。

这次100年 `e7ccd4...` hash 不能冒充未来 Batch schedule hash。

## 5. Gate C — REAL_CALENDAR_FUTOU_FREQUENCY

状态：`CLOSED_FOR_V02_PINNED_ENGINE_STRUCTURE_ONLY`

当前 V02 由真实 `QimenEngine` 对：

`2000-01-01 .. 2099-12-31` 共 `36,525` 个 civil dates，每日 `17:00 HKT`，`CHAI_BU_FUTOU`

逐日枚举。K2 App UI CI #86 / run `33264988516`：

`QimenWeatherRealCalendarAuditTest > realCivilCalendarFutouSignalStructureAudit()` = PASS。

V02 结果：

- core signal days：`6,498`
- civil-date structural trigger rate：`17.79055441%`
- max consecutive trigger days：`4`
- max non-trigger gap：`33日`
- 每个触发日最多1条 core hit path
- 上/中/下元触发：`1813 / 1850 / 2835`
- 24节气触发高度不均；冬至/惊蛰/清明/立夏为0
- 18个阴阳九局组合只有8个会触发

完整 V02 report：

`ziwei-core/build/reports/qimen-weather-real-calendar-audit-v02.json`

完整解释见：

`K2_QIMEN_CDAF_H2_REAL_CALENDAR_AUDIT_V01.md`

这个 gate 的 CLOSED 只表示“当前 V02 exact engine+method 的真实日期 signal structure 已知”。若 `QimenEngine blob / CHAI_BU_FUTOU / 17:00 freeze / CORE signal` 任一改变，Gate C 自动重开。

它不授予任何 weather empirical credit，也不能用17.79%直接反推未来 Batch 天数。

## 6. Gate D — SERIAL_DEPENDENCE / SAMPLE_ADEQUACY

状态：`METHOD_DEFINED / BATCH_PARAMETERS_NOT_FROZEN / BLOCKING`

方法设计继续由：

`K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md`

冻结。V02 Engine 修复没有读取 Outcome，也没有改变既有 sample/statistical contract。

当前固定：

- cadence：每日 HKO 16:30 PSR / 17:00 HKT Freeze；
- 最小时间覆盖：从真实节气段起点开始，连续 `48` 个完整节气段；
- 若且仅若 Outcome 未读取且任一 pre-outcome information count `<80`，再增加完整 `24` 段；
- 最大 horizon：`72` 个完整节气段；
- 三个最低 pre-outcome information counts：Original-vs-M1、Original-vs-+1、Original-vs--1，各 `>=80`；
- Outcome 只允许在 acquisition 正式关闭后统一进入研究表；
- Outcome QC 后若 evaluable information 任一 `<80`，同一 Batch 直接 `INSUFFICIENT_INFORMATION_AFTER_OUTCOME_QC`，不得重新开放补样本；
- primary estimands：三个模型对比的 daily paired accuracy delta；
- serial dependence：Bartlett calendar-lag HAC，固定 `HAC_MAX_LAG=30 civil days`；
- family-wise alpha：0.05，三个 primary contrasts 用 Bonferroni 单侧阈值，`Z_CRITICAL=2.1280452342`；
- success / no increment / calendar alignment not distinguished / inconclusive / insufficient-information 分别定义。

`80` 是 sample-planning information floor，不是“80例验证有效”。它不授予经验信用。

Gate D 剩余 Batch-specific 条件：

- 实际起始节气段进入 Batch contract；
- 48/72 horizon、80门槛、HAC=30、三重比较阈值被精确绑定；
- outcome quarantine / unlock procedure 被精确绑定；
- frozen station panel 与 data-completeness policy 确认；
- sample-plan exact file/version/hash 进入 Batch-level preregistration contract。

## 7. 当前优先顺序

```text
0. JU_METHOD_VALIDATION
   [implementation boundary PASS / source boundary fixture OPEN]
        ↓
A. PLATE_PAIRING_VALIDATION
   [one direct Kotlin source plate PASS / second independent plate OPEN]
        ↓
B. CALENDAR_EQUIVALENCE_CONTROL
   [V02 machine verified / Batch schedule not frozen]
        ↓
C. REAL_CALENDAR_FUTOU_FREQUENCY
   [CLOSED for V02 pinned-engine structure only]
        ↓
D. SERIAL_DEPENDENCE / SAMPLE_ADEQUACY
   [method defined / Batch parameters not frozen]
        ↓
E. Batch preregistration
        ↓
F. Freeze
        ↓
G. Outcome
        ↓
H. Batch Review
```

Gate C 的完成、Gate B/D 的方法定义，都不允许越过更靠前的 Gate 0/A。

## 8. 当前状态口径

```text
DOMAIN_DESIGN_DEFINED               = true
SOURCE_RULE_MINIMIZED               = true
M1_DEFINITION_DEFINED               = true
M2_UPDATE_FUNCTION_DEFINED          = true
OUTCOME_PROXY_POLICY_DEFINED        = true
WEATHER_JU_METHOD_CANDIDATE         = CHAI_BU_FUTOU
ACTIVE_MODEL                        = FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02
QIMEN_ENGINE_BLOB                   = 046825e480422eb0ac6734ea0330861bbd422997

FIVE_DAY_FUTOU_IMPLEMENTATION       = PASS
EXACT_TRANSITION_IMPLEMENTATION     = PASS
JU_METHOD_VALIDATION                = PARTIAL_MULTI_SOURCE_SHARED_STRUCTURE
JU_METHOD_SOURCE_BOUNDARY_FIXTURE   = OPEN
PLATE_PAIRING_DIRECT_KOTLIN_FIXTURE = ONE_DATED_SOURCE_PLATE_PASS
PLATE_PAIRING_VALIDATION            = PARTIAL_SECOND_PLATE_OPEN
CALENDAR_EQUIVALENCE_CONTROL        = V02_MACHINE_VERIFIED_NOT_BATCH_FROZEN
REAL_CALENDAR_FUTOU_FREQUENCY       = CLOSED_FOR_V02_PINNED_ENGINE_STRUCTURE_ONLY
SERIAL_DEPENDENCE_SAMPLE_GATE       = METHOD_DEFINED_NOT_BATCH_FROZEN

BATCH_READY                         = false
BATCH                               = NONE
FREEZE                              = NONE
OUTCOME                             = NONE
EMPIRICAL_CREDIT                    = NONE
CLAIM_EXTRACTION                    = BLOCKED
```

如果其他文档仍以较宽松的 `DESIGN_READY` 描述 CDAF-H2，它只能理解为“已有可审计设计对象”，不得解释为“已经可以开始正式 Batch”。

## 9. 本轮最重要的认识修正

这次 V02 反审暴露了两个容易重复出现的错误模式：

### 9.1 聚合结果相同不能证明实现等价

V01/V02 的100年 core trigger 总数都恰好是6498，但 exact-transition regression 和新 sham schedule 已证明两者不是同一 calendar alignment。

因此：

`SAME SUMMARY STATISTIC != SAME IMPLEMENTATION`

### 9.2 镜像测试不能代替真实模型输出的 source fixture

旧 weather audit 曾自己重算 carried heaven stems。V02 把该事实收回 `Gong.tianGan`，并让真实 Kotlin source fixture 直接断言它。

因此：

`MIRROR CONSISTENCY != MODEL OUTPUT VALIDATION`

这两条作为后续自我迭代纪律保留，但本身仍只是方法学/工程信用，不是奇门经验有效性证据。
