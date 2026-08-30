# K2 CDAF-H2 Weather Pilot — Pre-Batch Gate Amendment v0.2

状态：`ACTIVE_AUTHORITY / V01_HISTORY_PRESERVED / BATCH_NOT_READY`  
基础设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
历史前件：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01_GATE_AMENDMENT.md`  
JuMethod review：`knowledge/K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md`  
Epistemic discipline：`knowledge/K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md`  
active model：`FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02`  
QimenEngine blob：`046825e480422eb0ac6734ea0330861bbd422997`  
Empirical Credit：`NONE`

## 1. Authority / supersession rule

本文件是 weather-v0.1 当前 gate 状态的 active authority。

V01 amendment 不删除、不重写，继续保存当时的真实认知状态，包括曾经把 Gate 0 写成：

`SOURCE_BOUNDARY_FIXTURE_OPEN / BLOCKING`

后续 source review、独立天文边界 regression 与方法向量拆分已经使该状态过时。因此：

```text
V01 = historical audit trail
V02 = current gate authority
```

保留 V01 的目的不是维护旧结论，而是让“错误如何被发现、如何被修正”可追踪。

## 2. Gate 0 — JU_METHOD_VALIDATION

状态：`CLOSED_FOR_WEATHER_V01_CHAIBU_METHOD_IDENTITY / NOT_GLOBAL_VALIDATION`

### 2.1 当前关闭对象

只关闭以下候选 method vector：

```text
WEATHER_V01_CHAIBU_METHOD_VECTOR

DAY_GROUPING
    nearest preceding five-day 甲/己 head

YUAN_CLASSIFICATION
    子午卯酉 -> 上元
    寅申巳亥 -> 中元
    辰戌丑未 -> 下元

SOLAR_TERM_POLICY
    actual astronomical solar-term transition instant
    switches to the new solar term's ju system

SUPER_CONNECT_POLICY
    拆补残元 treatment
    not the置闰 carry policy

LEAP_POLICY
    NONE

JU_LOOKUP
    24 solar terms × 上中下三元 fixed ju table
```

任一组件改变都属于新 method/model version，不能继续沿用旧 Freeze 或旧方法信用。

### 2.2 Source support

QM-SRC-0021 与 QM-SRC-0028 是 Lineage Registry 中不同的 PRIMARY_WORK。现有 Atomic Evidence 分别支持：

- 五天一元；
- 甲/己五日符头；
- 上中下元 branch classification；
- 二十四节气 × 三元用局；
- 拆补以实际交节时辰切换新节气局数体系；
- 无闰拆补与置闰传统必须区分。

QM-SRC-0017 费秉勋《奇门遁甲新述》继续只给共享五日符头、三元分类与 `1990-01-27 -> 大寒下元阳6` 的独立 dated structural credit。其完整语境属于超神接气/置闰传统，因此不得借来证明完整拆补方法等价。

长期保持：

```text
SAME OUTPUT != SAME METHOD
SHARED SUBSTRUCTURE != METHOD EQUIVALENCE
```

### 2.3 Independent boundary checks

当前不再让 lunar-java 单独“自己给 boundary、自己验证自己”。

已通过的边界组合包括：

1. `2026-08-07 立秋`：香港天文台独立年历给出 `19:43 HKT`；Engine regression 在同一 civil date 上验证交节前后切换。
2. `2004-02-04 立春`：QM-SRC-0021 以该癸丑日说明交节后仍取己酉符头判上元、但改用立春阳8；日本国立天文台历书把立春置于 `20:56 JST / 19:56 HKT` 这一分钟。由于 Engine API 只接受整数分钟，测试把 `19:56` 作为事件所在分钟内的 pre-transition sample，把 `19:57` 作为第一个可表示的 post-transition whole minute，并验证：

```text
19:56 -> 大寒 / 上元 / 阳3
19:57 -> 立春 / 上元 / 阳8
```

对应 Kotlin regression：

`QimenJuMethodBoundaryFixtureTest > qm0021ChaibuExampleSwitchesAtFirstWholeMinuteAfterIndependent2004LichunInstant()`

已在 Knowledge Engine CI #799 明确执行并 PASS。

### 2.4 Credit boundary

Gate 0 CLOSED 只表示：

`METHOD IDENTITY / TRANSITION CONTRACT CREDIT`

它不表示：

- 拆补法现实上比置闰更准；
- DAYCOUNT 或 ZHI_RUN 已验证；
- 费氏完整置闰法与当前候选等价；
- 完整九宫 plate 已验证；
- weather prediction 有效；
- 奇门理论获得 empirical credit。

## 3. Gate A — PLATE_PAIRING_VALIDATION

状态：`ONE_SOURCE_DATED_PLATE_DIRECT_KOTLIN_PAIRING_PASS / SECOND_INDEPENDENT_PLATE_OPEN / BLOCKING`

当前已有 QM-SRC-0021 `2004-05-29 戊午时` source-grounded plate fixture，真实 Kotlin `QimenEngine` 直接核对：

```text
palace -> (tianXing, Gong.tianGan)
```

外八宫已通过 source expected pairing regression；weather audit 也直接读取 Engine 一等字段 `Gong.tianGan`，不再在 audit 内重算一个镜像 heaven-stem map。

Gate A 仍缺：

1. 第二张**独立来源** dated complete plate；
2. 必须有足够的日期/时辰/时柱 provenance；
3. 必须能直接核对九星位置与天盘干 pairing；
4. 最好覆盖不同阴阳遁/局数；
5. 只拿盘面做实现验证，不导入来源的事件结果或断语；
6. 若第二来源与 Engine/第一来源冲突，保留冲突并先调查，不得挑对自己有利的版本。

因此：

`GLOBAL_PLATE_VALIDATION = NOT_CLAIMED`

`WEATHER_BATCH_CREATION = FORBIDDEN`

## 4. Gate B — CALENDAR_EQUIVALENCE_CONTROL

状态：`V02_MACHINE_STRUCTURE_VERIFIED / BATCH_SCHEDULE_NOT_FROZEN / BLOCKING`

当前 v0.1 calendar control family 继续是节气段内部 circular phase shams：

- `M2_SHAM_PLUS_1`
- `M2_SHAM_MINUS_1`

V02 100-year structure audit：

```text
complete_segment_count = 2399
complete_segment_days  = 36510
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

该 hash 只属于100年结构审计，不能冒充未来 Batch schedule hash。

未来 Batch horizon 确定后必须重新生成 exact schedule，并在 outcome 前 Freeze。

## 5. Gate C — REAL_CALENDAR_FUTOU_FREQUENCY

状态：`CLOSED_FOR_V02_PINNED_ENGINE_STRUCTURE_ONLY`

固定：

`2000-01-01 .. 2099-12-31 / daily 17:00 HKT / CHAI_BU_FUTOU / current V02 Engine`

V02 机器结果：

```text
civil dates             = 36525
core signal days        = 6498
structural trigger rate = 17.79055441%
max trigger run         = 4
max non-trigger gap     = 33 days
yuan trigger counts     = 1813 / 1850 / 2835
```

这只是结构频率。Engine blob、方法、17:00 freeze 或 CORE signal 任一变化，Gate C 自动重开。

## 6. Gate D — SERIAL_DEPENDENCE / SAMPLE_ADEQUACY

状态：`METHOD_DEFINED / BATCH_PARAMETERS_NOT_FROZEN / BLOCKING`

继续沿用：

`knowledge/K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md`

当前设计包括：

- 每日 HKO 16:30 PSR / 17:00 HKT Freeze；
- 从真实节气段起点开始，最少48个完整节气段；
- 只有 outcome 未读取且 pre-outcome information count 不足时，才按预设规则扩到72段；
- Original-vs-M1、Original-vs-+1、Original-vs--1 三个 pre-outcome information counts 各至少80；
- outcome acquisition 关闭后才统一进入研究表；
- Outcome QC 后不足80则 `INSUFFICIENT_INFORMATION_AFTER_OUTCOME_QC`，不得补样；
- daily paired accuracy delta；
- Bartlett calendar-lag HAC，`HAC_MAX_LAG=30`；
- family-wise alpha 0.05，三个 primary contrasts 使用预定义 Bonferroni 单侧阈值。

`80` 是 information floor，不是“80例证明有效”。

Gate D 仍需在真实 Batch contract 中绑定起始节气段、horizon、station panel、outcome quarantine、统计参数与 exact sample-plan version/hash。

## 7. Closed-retreat reasoning discipline

本轮把方法 gate 与今天的内校准原则统一：

```text
EXTERNAL LEARNING
    != AUTOMATIC KNOWLEDGE PROMOTION

SOURCE MEANING
    != CASE CONCLUSION

METHOD REPRODUCTION
    != EMPIRICAL VALIDITY

CONTEXT FIT
    != OUTCOME EVIDENCE
```

书本先作为 SOURCE MODEL 被完整保留；然后必须回到内部反审，检查来源假设、适用边界、与其他来源冲突，以及项目是否只是因为熟悉某一套书而形成路径依赖。

具体解盘时，静态星门神/格局含义只能是候选 feature。必须先固定具体事体、角色/取用、时间尺度和现实约束，再决定哪些规则满足适用前提；推演应基于关系结构，并保留竞争解释或弃权，而不是把书本条目串成一个看似完整的故事。

自创理论也不享有优先权。任何 project-generated component 必须能被 ablation、counterfactual、unknown-outcome test 推翻，并允许在失败后被降级、删除或简化。

## 8. Current active status

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
JU_METHOD_VALIDATION                = CLOSED_FOR_WEATHER_V01_CHAIBU_METHOD_IDENTITY
JU_METHOD_GLOBAL_EQUIVALENCE        = NOT_CLAIMED
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

## 9. Next blocker

当前最靠前的真实 blocker 已从 Gate 0 移到 Gate A：

`SECOND_INDEPENDENT_DATED_COMPLETE_PLATE`

在它完成前，不创建 weather Batch。
