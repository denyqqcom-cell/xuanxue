# K2 CDAF-H2 Weather Pilot — Pre-Batch Gate Amendment v0.4

状态：`ACTIVE_AUTHORITY / V01_V02_V03_HISTORY_PRESERVED / ENGINE_V03_REAUDIT_IN_PROGRESS / BATCH_NOT_READY`  
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
V04 authority = active state during/after Engine V03 repin
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

`CORE_RAIN_SIGNAL_V01` 仍只消费：

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

但“没有直接依赖”不是“可以跳过 re-audit”。whole-engine blob 已改变，所以 V02 的数值结果在 V04 重跑完成前只能作为 historical comparator，不能自动复制到 V03 candidate。

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

old V02 candidate 不删除；其历史 audit 继续保留，但不能作为当前 V03 的 machine result。

## 5. Required V03 re-audits

V04 在本文件创建时不预设“统计一定不变”。以下三组必须由新 blob 实际重新计算：

### A. Abstract weather state-space

必须重新验证：

- 360 nominal states；
- CORE trigger state count；
- 每节气 nominal trigger distribution；
- hit cardinality。

### B. Real civil calendar

必须重新验证固定 100-year window 下：

- civil dates；
- core signal days / rate；
- trigger-run / non-trigger-gap；
- yuan / jieqi / ju structure。

### C. Calendar-equivalence controls

必须重新验证：

- complete solar-term segments；
- original/+1/-1 trigger totals；
- Hamming differences；
- schedule audit hash。

若 A/B/C 与 V02 数值完全一致，只允许记录：

`WEATHER_RELEVANT_STRUCTURAL_EQUIVALENCE_V02_TO_V03 = VERIFIED`

这不等于：

`FULL_ENGINE_EQUIVALENCE`。

## 6. Gate 0 / Gate A remain narrow

本轮值使门修复不撤销已经获得的窄信用：

```text
Gate 0 = CLOSED_FOR_WEATHER_V01_CHAIBU_METHOD_IDENTITY
Gate A = CLOSED_FOR_WEATHER_V01_STAR_HEAVEN_STEM_CONSTRUCTION
```

原因是本轮没有修改这两个 gate 所对应的来源对象本身。

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

即使 V03 re-audits 全部恢复 PASS，也不自动创建 Batch。

## 8. Current active status at creation

```text
JU_METHOD_VALIDATION                = CLOSED_NARROWLY
PLATE_PAIRING_VALIDATION            = CLOSED_NARROWLY_FOR_STAR_HEAVEN_STEM
ZHISHI_CENTER_COUNT_SOURCE_FIXTURE  = PASS_AFTER_FAIL_FIRST_CORRECTION
ENGINE_V03_CORE_REGRESSION          = PASS_KNOWLEDGE_CI_828
ABSTRACT_WEATHER_V03_REAUDIT        = PENDING
REAL_CALENDAR_V03_REAUDIT           = PENDING
CALENDAR_EQUIVALENCE_V03_REAUDIT    = PENDING
WEATHER_RELEVANT_V02_V03_EQUIVALENCE = NOT_YET_CLAIMED

BATCH_READY                         = false
BATCH                               = NONE
FREEZE                              = NONE
OUTCOME                             = NONE
EMPIRICAL_CREDIT                    = NONE
CLAIM_EXTRACTION                    = BLOCKED
```

完成 A/B/C 重跑后，本文件只允许按真实机器结果从 `PENDING` 更新；任何差异都必须保留并调查，不得为了恢复旧数字而调 Engine、CORE signal 或 audit code。
