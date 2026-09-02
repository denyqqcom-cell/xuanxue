# K2 Qimen Gate A Orthogonalization Review v0.1

状态：`ACCEPTED_FOR_WEATHER_PLATE_CONSTRUCTION / NO_EMPIRICAL_CREDIT`

后续 active authority：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_GATE_AMENDMENT_V04.md`

目的：反审旧 Gate A 把两个不同验证对象绑成一个“第二张 dated complete plate”条件的问题，避免“形式更严格”却重复给 Gate 0 的 calendar -> state 链记信用，同时真正隔离 state -> plate construction。

## 1. 为什么必须正交化

旧 Gate A 一次要求：

```text
civil datetime
    -> JuMethod / solar-term / yuan / ju / hour state
    -> plate construction
```

但第一段已经由 Gate 0 负责 method identity、actual-transition 与 dated boundary regression。

继续强制“第二个 Gregorian date”会产生两个偏差：

1. 重复测试 calendar -> state，却把重复信用误认为 plate validation 更充分；
2. 因追求 dated 形式，排除能够更纯地定义完整 plate state 的独立来源。

因此 Gate A 采用两个正交子对象：

```text
A1 END_TO_END_DATED_PLATE
    验 civil datetime -> state -> plate 全链

A2 INDEPENDENT_STATE_DEFINED_PLATE
    验 frozen state -> plate，不重复借 calendar 层信用
```

这不是降低标准。A2 比“再找一个日期但只核星位”更严格地要求第二来源在 Engine comparison 前给出完整 weather-relevant `palace -> (star, carried heaven stem)` expected map。

## 2. A1：QM-SRC-0021 dated end-to-end plate

`A1 = PASS`

已有 QM-SRC-0021：`2004-05-29 戊午时`。

真实 Kotlin regression 直接核对：

```text
civil datetime
-> CHAI_BU_FUTOU state
-> palace -> (tianXing, Gong.tianGan)
```

该 fixture 覆盖 dated input、阳遁八局、甲寅旬、非零天盘转动与完整外八宫星—天盘干 pairing。

A1 不能被 A2 替代；它继续承担 end-to-end credit。

## 3. A2：QM-SRC-0017 independent state-defined plate

canonical source：QM-SRC-0017 / 费秉勋《奇门遁甲新述》

Lineage Registry 已确认：

```text
QM-SRC-0017 = PRIMARY_WORK / PRIMARY_CANDIDATE / WORK-000224
QM-SRC-0021 = PRIMARY_WORK / PRIMARY_CANDIDATE / WORK-000027
```

二者不是 same-work variant，也不是同一 course-family duplicate vote。

本轮直接核对 QM-SRC-0017 原页，不使用事件结果：

- printed p17-p19：把神盘、天盘、地盘、门盘纳入完整活盘；printed p18 为`阳遁一局活盘图`；
- printed p24：明确举 `阳遁一局丙寅时`：丙寅属甲子旬，值符天蓬、值使休门；时干丙对应地盘丙奇所在艮八宫，因此把天盘天蓬拨转到艮八宫；
- printed p24-p25：明确给出“直符随时干，直使随时宫”的活盘拨转原则，并继续以阴遁九局案例说明天盘/门盘的拨转；
- 卷四 printed p105-p107：再次给出`阳遁一局图`及六甲旬各时辰值符值使表，作为独立 state/table reference。

来源状态在 Engine comparison 前固定为：

```text
YIN_YANG = YANG
JU       = 1
HOUR_GZ  = 丙寅
XUN      = 甲子旬
ZHI_FU   = 天蓬
ZHI_FU_TARGET = 艮8（地盘丙奇）
```

Gregorian date 只用于 Kotlin test 寻找一个能实例化同一 state 的 Engine harness，不属于 source provenance，也不获得 A1/date credit。

## 4. Engine comparison 前冻结的 source-derived expected pairs

从 printed p18 的阳遁一局活盘原始星—carrier 同扇区结构，与 printed p24 对丙寅时“天蓬拨到艮8”的 source-local rigid plate rotation，在任何 Engine comparison 前冻结：

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

冲突处理原则始终是：

```text
SOURCE_EXPECTATION != ENGINE_OUTPUT
    -> preserve conflict
    -> investigate source convention / center-hosting / rotation implementation
    -> DO NOT edit expected map merely to make CI green
```

## 5. A2 machine result

测试：

`ziwei-core/src/test/kotlin/com/xuanxue/qimen/QimenIndependentStatePlateFixtureTest.kt`

测试名：

`qm0017_yang1_bingyin_state_matches_source_derived_star_heaven_stem_pairs`

GitHub Knowledge Engine V1 CI #810：`PASSED`

测试实际从 public `QimenEngine.bySolar(..., CHAI_BU_FUTOU)` 寻找同 state harness，并直接比较 Kotlin：

```text
c.gongs.filter(palace != 5)
    -> palace -> (tianXing, tianGan)
```

结果与上述 source-derived expected map 全部一致。

A2 因而满足：

1. 独立 PRIMARY_WORK；
2. state 在结果前唯一；
3. expected outer pair map 在 Engine comparison 前冻结；
4. expected map 来自 source 图与 source-local rotation，不由 Engine 生成；
5. test harness date 不冒充 source date；
6. 不读取占验结果；
7. Kotlin mismatch 原本会直接 fail，而不是调整 expected。

## 6. Gate A 的正确关闭对象

因此本审查接受：

```text
A1 = DATED_END_TO_END_PASS
A2 = INDEPENDENT_STATE_DEFINED_PLATE_PASS
```

足以关闭的只是 weather-v0.1 真正依赖的构造层：

```text
palace -> (九星, carried heaven stem)
```

推荐 active 状态：

```text
PLATE_PAIRING_VALIDATION =
CLOSED_FOR_WEATHER_V01_STAR_HEAVEN_STEM_CONSTRUCTION
/ NOT_GLOBAL_PLATE_VALIDATION
```

这里“CLOSED”不覆盖：

- 门盘完整多源一致性；
- 神盘完整多源一致性；
- 中五寄宫的所有流派分歧；
- DAYCOUNT / ZHI_RUN / 其他起局传统；
- 任意吉凶断语；
- 现实预测有效性。

后续 `K2_QIMEN_ZHISHI_GATE_SOURCE_REVIEW_V01.md` 用 canonical QM-SRC-0017 p24-p25 关闭了一个更窄的实现错误：值使门 travel 经过中五时必须计入 5，只有最终 target=5 才寄坤2。该 correction 不扩大本 Gate A 的 weather credit，也不把“中五寄宫的所有流派分歧”判成已解决。

## 7. 信用边界

本审查只提供 source/implementation cross-validation：

```text
EMPIRICAL_CREDIT = NONE
CLAIM_EXTRACTION = BLOCKED
FULL_QIMEN_MATURITY = EXPERIMENTAL
```

它不说明奇门现实有效，不说明 QM-SRC-0017 与 QM-SRC-0021 的所有盘法完全等价，也不允许把 weather 所需的星—天盘干 pairing credit 扩张成“完整九宫已经全局验证”。
