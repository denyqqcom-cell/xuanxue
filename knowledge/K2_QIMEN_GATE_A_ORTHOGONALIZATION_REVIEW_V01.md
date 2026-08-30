# K2 Qimen Gate A Orthogonalization Review v0.1

状态：`PROPOSAL_UNDER_TEST / ACTIVE_GATE_A_UNCHANGED / NO_EMPIRICAL_CREDIT`

关联 active authority：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_GATE_AMENDMENT_V02.md`

目的：反审现有 Gate A 是否把两个不同验证对象绑成一个条件，避免“看起来更严格”却重复测试 Gate 0，同时又没有真正隔离 state -> plate construction。

## 1. 发现的问题

当前 Gate A 要求“第二张独立来源 dated complete plate”。这个条件一次包含两段链路：

```text
civil datetime
    -> JuMethod / solar-term / yuan / ju / hour state
    -> plate construction
```

但第一段已经由 Gate 0 负责 method identity、actual-transition 与 dated boundary regression。

如果 Gate A 继续把“第二个 Gregorian date”本身视为必要信用，可能产生两类误区：

1. 重复给 calendar -> state 记信用，却没有增加 state -> plate 的独立检验；
2. 因为追求“dated”形式而排除能够更纯地定义完整 plate state 的独立来源。

因此本审查提出正交化，而不是放宽：

```text
A1 END_TO_END_DATED_PLATE
    验 civil datetime -> state -> plate 全链

A2 INDEPENDENT_STATE_DEFINED_PLATE
    验 frozen state -> plate，不重复借 calendar 层信用
```

Gate A 是否最终采用该拆分，必须先看 A2 candidate 能否真正做到“source-derived expected map 在 Engine comparison 前冻结”。

## 2. A1 当前状态

`A1 = PASS_ONE_SOURCE`

已有 QM-SRC-0021：`2004-05-29 戊午时`。

当前真实 Kotlin regression 已直接核对：

```text
palace -> (tianXing, Gong.tianGan)
```

该 fixture 同时覆盖 dated input、CHAI_BU_FUTOU state 与非零 plate rotation。

A1 的存在不能被 A2 替代。

## 3. A2 candidate：QM-SRC-0017 费秉勋《奇门遁甲新述》

canonical source：QM-SRC-0017 / 费秉勋《奇门遁甲新述》

本轮直接核对原页，不使用事件结果：

- printed p17-p19：把神盘、天盘、地盘、门盘纳入完整活盘；printed p18 为`阳遁一局活盘图`；
- printed p24：明确举 `阳遁一局丙寅时`：丙寅属甲子旬，值符天蓬、值使休门；时干丙对应地盘丙奇所在艮八宫，因此把天盘天蓬拨转到艮八宫；
- printed p24-p25：明确给出“直符随时干，直使随时宫”的活盘拨转原则，并继续以阴遁九局案例说明天盘/门盘的拨转；
- 卷四 printed p105-p107：再次给出`阳遁一局图`及六甲旬各时辰值符值使表，作为独立 state/table reference。

这些材料可以定义一个**不需要 Gregorian date**的来源状态：

```text
YIN_YANG = YANG
JU       = 1
HOUR_GZ  = 丙寅
XUN      = 甲子旬
ZHI_FU   = 天蓬
ZHI_FU_TARGET = 艮8（地盘丙奇）
```

这里 Gregorian date 若用于 Kotlin test，只能是“找到同一 state 的 Engine harness”，不得写成 source date，也不得因此获得 A1/date credit。

## 4. Engine comparison 前冻结的 source-derived expected pairs

从 printed p18 的阳遁一局活盘原始环序，与 printed p24 对丙寅时“天蓬拨到艮8”的 source-local rigid plate rotation，预先冻结外八宫：

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

该 map 在运行 Kotlin comparison 前写入本文件和测试。以后如果 Engine 不同：

```text
SOURCE_EXPECTATION != ENGINE_OUTPUT
    -> preserve conflict
    -> investigate source convention / center-hosting / rotation implementation
    -> DO NOT edit expected map merely to make CI green
```

## 5. A2 acceptance contract

只有同时满足以下条件，A2 才可记 source/implementation credit：

1. source 与 QM-SRC-0021 为独立 work，不得是同 work variant / same-course duplicate vote；
2. source state 在反馈前唯一：阴阳遁、局、旬/时柱、值符定位不能结果后切换；
3. expected full outer `palace -> (star, carried heaven stem)` 必须在 Engine comparison 前冻结；
4. expected map 必须由 source 自身活盘图与拨转规则导出，不得调用 QimenEngine 生成 expected；
5. Kotlin test 可以动态寻找一个 civil datetime 作为同 state harness，但该日期只属于测试输入，不属于 source provenance；
6. 不读取来源事件结果/断语；
7. 冲突即保留，不得因为 QM-SRC-0021 已通过就把第二来源强行同化。

## 6. 当前信用边界

在 A2 machine comparison 完成前：

```text
A1 = ONE_SOURCE_DATED_END_TO_END_PASS
A2 = SOURCE_EXPECTATION_FROZEN / MACHINE_COMPARISON_PENDING
GATE_A = OPEN
WEATHER_BATCH = FORBIDDEN
EMPIRICAL_CREDIT = NONE
```

即使未来 A2 PASS，也只能说明第二独立 source-defined state 对 plate construction 提供实现交叉验证；不说明奇门现实有效，不说明两个作者的所有盘法完全等价，也不自动解决其他 center-hosting / 神盘 / 门盘分歧。
