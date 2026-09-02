# K2 CDAF-H2 Weather Pilot — Pre-Batch Gate Amendment v0.3

状态：`ACTIVE_AUTHORITY / V01_V02_HISTORY_PRESERVED / BATCH_NOT_READY`  
基础设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
历史前件：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01_GATE_AMENDMENT.md`、`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_GATE_AMENDMENT_V02.md`  
JuMethod review：`knowledge/K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md`  
Gate A review：`knowledge/K2_QIMEN_GATE_A_ORTHOGONALIZATION_REVIEW_V01.md`  
Epistemic discipline：`knowledge/K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md`  
active model：`FROZEN_SYMBOLIC_MAPPING_WITH_CALENDAR_EQUIVALENCE_CONTROLS_V02`  
QimenEngine blob：`046825e480422eb0ac6734ea0330861bbd422997`  
Empirical Credit：`NONE`

## 1. Authority / supersession rule

本文件是 weather-v0.1 当前 gate 状态的 active authority。

V01/V02 amendment 不删除、不回写，继续保存各自当时的真实认知状态：

```text
V01 = historical audit trail before Gate 0 closure
V02 = historical audit trail before Gate A orthogonalization
V03 = current gate authority
```

V03 的变化只发生在 Gate A：旧条件把“第二张 dated plate”同时绑定 calendar -> state 与 state -> plate，造成 Gate 0 与 Gate A 信用混层。本版通过 A1/A2 正交化纠正这一验证设计，不降低 source expected-map 要求。

## 2. Gate 0 — JU_METHOD_VALIDATION

状态：`CLOSED_FOR_WEATHER_V01_CHAIBU_METHOD_IDENTITY / NOT_GLOBAL_VALIDATION`

关闭对象仍是 V02 已冻结的 method vector：

```text
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

Source support、2026 HKO 立秋独立 boundary、2004-02-04 QM-SRC-0021 + independent astronomy boundary regression 均继续沿用 V02 已核验事实。

Gate 0 只提供 `METHOD IDENTITY / TRANSITION CONTRACT CREDIT`，不提供拆补预测优越性、其他 JuMethod 等价性、完整 plate 或 empirical credit。

## 3. Gate A — WEATHER-RELEVANT PLATE PAIRING

状态：`CLOSED_FOR_WEATHER_V01_STAR_HEAVEN_STEM_CONSTRUCTION / NOT_GLOBAL_PLATE_VALIDATION`

### 3.1 为什么不再要求“第二张 Gregorian dated complete plate”

旧 Gate A 把两段链路绑成一个条件：

```text
civil datetime -> state -> plate
```

其中 `civil datetime -> state` 已由 Gate 0 专门验证。继续要求第二个 Gregorian date 会重复给 calendar 层记信用，并不能更纯地检验 weather 真正依赖的 plate construction。

因此 Gate A 正交化为：

```text
A1 END_TO_END_DATED_PLATE
    civil datetime -> state -> plate

A2 INDEPENDENT_STATE_DEFINED_PLATE
    frozen state -> plate
```

正交化不是放宽。A2 要求第二独立来源在任何 Engine comparison 前冻结完整外八宫 `palace -> (star, carried heaven stem)` expected map，并以 mismatch fail closed。

### 3.2 A1 — QM-SRC-0021 dated end-to-end fixture

`A1 = PASS`

QM-SRC-0021 `2004-05-29 戊午时` 已由真实 Kotlin `QimenEngine` 直接核对：

```text
palace -> (tianXing, Gong.tianGan)
```

外八宫完整 source expected pairing regression 通过；它承担 dated end-to-end credit。

### 3.3 A2 — QM-SRC-0017 independent state-defined fixture

`A2 = PASS`

Lineage Registry：

```text
QM-SRC-0017 = PRIMARY_WORK / PRIMARY_CANDIDATE / WORK-000224
QM-SRC-0021 = PRIMARY_WORK / PRIMARY_CANDIDATE / WORK-000027
```

二者不是 same-work variant / same-course duplicate vote。

QM-SRC-0017 费秉勋《奇门遁甲新述》原页在 Engine comparison 前定义：

```text
YIN_YANG = YANG
JU       = 1
HOUR_GZ  = 丙寅
XUN      = 甲子旬
ZHI_FU   = 天蓬
ZHI_FU_TARGET = 艮8（地盘丙奇）
```

source-derived frozen expected outer pairs：

```text
1 -> (天心, 癸)
2 -> (天英, 乙)
3 -> (天任, 丙)
4 -> (天冲, 庚)
6 -> (天柱, 丁)
7 -> (天芮天禽, 己)
8 -> (天蓬, 戊)
9 -> (天辅, 辛)
```

对应 Kotlin：

`QimenIndependentStatePlateFixtureTest > qm0017_yang1_bingyin_state_matches_source_derived_star_heaven_stem_pairs()`

Knowledge Engine V1 CI #810 明确执行并 `PASSED`。

测试中动态找到的 civil datetime 只是 public Engine API 的同 state harness，不属于 QM-SRC-0017 source provenance，也不增加 dated/source credit。

### 3.4 Gate A credit boundary

Gate A CLOSED 只表示 weather-v0.1 当前 `CORE_RAIN_SIGNAL_V01` 所依赖的这一层已经获得两个正交来源夹具的 source/implementation cross-validation：

```text
palace -> (九星, carried heaven stem)
```

不表示：

- 门盘完整多源一致性已验证；
- 神盘完整多源一致性已验证；
- 中五寄宫所有传统分歧已解决；
- 所有阴阳遁/十八局/六十时全状态都成为 source golden truth；
- QM-SRC-0017 与 QM-SRC-0021 的完整体系等价；
- 吉凶断语、应期或现实预测有效；
- 完整 QimenEngine 可升级成熟度。

因此长期保持：

```text
FULL_QIMEN_MATURITY = EXPERIMENTAL
GLOBAL_PLATE_VALIDATION = NOT_CLAIMED
EMPIRICAL_CREDIT = NONE
```

## 4. Gate B — CALENDAR_EQUIVALENCE_CONTROL

状态：`V02_MACHINE_STRUCTURE_VERIFIED / BATCH_SCHEDULE_NOT_FROZEN / BLOCKING`

calendar control family 继续是同一实际节气段内部 circular phase shams：

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

该 hash 仍只属于100年结构审计，不能冒充未来 Batch schedule hash。

未来 Batch horizon 确定后必须重新生成 exact schedule，并在任何 Outcome 前 Freeze。

## 5. Gate C — REAL_CALENDAR_FUTOU_FREQUENCY

状态：`CLOSED_FOR_V02_PINNED_ENGINE_STRUCTURE_ONLY`

固定：

`2000-01-01 .. 2099-12-31 / daily 17:00 HKT / CHAI_BU_FUTOU / V02 Engine`

V02 机器结果：

```text
civil dates             = 36525
core signal days        = 6498
structural trigger rate = 17.79055441%
max trigger run         = 4
max non-trigger gap     = 33 days
yuan trigger counts     = 1813 / 1850 / 2835
```

仍只是结构频率。Engine blob、方法、17:00 freeze 或 CORE signal 任一变化，Gate C 自动重开。

## 6. Gate D — SERIAL_DEPENDENCE / SAMPLE_ADEQUACY

状态：`METHOD_DEFINED / BATCH_PARAMETERS_NOT_FROZEN / BLOCKING`

继续沿用：

`knowledge/K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md`

当前设计继续要求：

- HKO 16:30 PSR / 17:00 HKT Freeze；
- 从真实节气段起点开始，最少48个完整节气段；
- 只有完全不读取 Outcome 且 pre-outcome information count 不足时才整体扩到72段；
- Original-vs-M1、Original-vs-+1、Original-vs--1 三个 pre-outcome information counts 各至少80；
- acquisition 关闭后才统一进入 Outcome；
- Outcome QC 后不足80则 `INSUFFICIENT_INFORMATION_AFTER_OUTCOME_QC`，不得补样；
- daily paired accuracy delta；
- Bartlett calendar-lag HAC，`HAC_MAX_LAG=30`；
- family-wise alpha 0.05，三个 primary contrasts 使用冻结 Bonferroni 单侧阈值。

`80` 只是 information floor，不是“80例证明有效”。

Gate D 仍需在真实 Batch contract 中绑定起始节气段、horizon、station panel、outcome quarantine、统计参数与 exact sample-plan version/hash。

## 7. Closed-retreat reasoning discipline

继续执行：

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

本次 Gate A 自身也接受同一内校准：旧标准“第二张 dated plate”并不因为更苛刻就天然更科学。发现它重复测试 Gate 0 后，应拆分验证对象，而不是为了维护既有门禁而继续寻找形式匹配的案例。

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
PLATE_A1_DATED_END_TO_END           = PASS_QM_SRC_0021
PLATE_A2_INDEPENDENT_STATE_DEFINED  = PASS_QM_SRC_0017
PLATE_PAIRING_VALIDATION            = CLOSED_FOR_WEATHER_V01_STAR_HEAVEN_STEM_CONSTRUCTION
GLOBAL_PLATE_VALIDATION             = NOT_CLAIMED
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

## 9. Next blockers

Gate A 不再是当前最靠前 blocker。

进入真实 weather Batch 前仍至少需要共同关闭：

```text
Gate B = future Batch exact +/-1 sham schedule not frozen
Gate D = Batch horizon/start/station-panel/statistical contract not frozen
```

两者都必须在任何 Outcome 前冻结；不得因为 Gate A 关闭就立即创建 Batch 或提升 empirical credit。
