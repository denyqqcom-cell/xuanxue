# K2 奇门 JuMethod 跨来源复核 v0.1

状态：`WEATHER_CHAIBU_METHOD_IDENTITY_CLOSED / GLOBAL_METHOD_EQUIVALENCE_REJECTED / NO_EMPIRICAL_CREDIT`  
用途：区分“weather-v0.1 当前 CHAI_BU_FUTOU method vector 已有足够 source+boundary 约束”与“所有起局传统/完整奇门盘法已验证”，防止局部关闭被扩张成全局信用。

## 1. 研究问题

当前 `QimenEngine` 同时存在：

- `CHAI_BU_DAYCOUNT`；
- `CHAI_BU_FUTOU`；
- `ZHI_RUN`（当前 fail closed / unsupported）。

此前修复确认：拆补符头用于定元的时间单位是五日甲/己符头，而六甲旬首仍是十日单位，二者不能混用。

跨来源复核进一步确认：

> “甲/己五日符头”可以被多个传统共享；完整方法身份必须继续比较交节切换、超神/接气、置闰和局表等组件，不能只看最后局数是否相同。

因此长期保持：

```text
SAME OUTPUT != SAME METHOD
SHARED SUBSTRUCTURE != METHOD EQUIVALENCE
```

本轮关闭的对象只定义为：

`WEATHER_V01_CHAIBU_METHOD_VECTOR`

不关闭 DAYCOUNT、ZHI_RUN、费氏完整置闰法或其他流派的全局方法身份。

## 2. Weather-v0.1 当前 method vector

当前 `CHAI_BU_FUTOU` 候选明确拆成：

```text
DAY_GROUPING
    nearest preceding five-day 甲/己 head

YUAN_CLASSIFICATION
    head branch class:
    子午卯酉 -> 上元
    寅申巳亥 -> 中元
    辰戌丑未 -> 下元

SOLAR_TERM_POLICY
    actual astronomical solar-term transition instant switches to the new term's ju system

SUPER_CONNECT_POLICY
    拆补残元处理；允许残上 / 中 / 下 / 补上
    不借用置闰法的超神/接气 carry policy

LEAP_POLICY
    NONE for this chaibu candidate

JU_LOOKUP
    24 solar terms × 上中下三元 fixed ju table
```

以后任何一个组件改变，都属于新 method/model version；不得继续沿用 `CHAI_BU_FUTOU` 名字掩盖内部政策变化。

## 3. QM-SRC-0021 — 幺学声《奇门遁甲预测学》

K2 状态：

- source_id: `QM-SRC-0021`
- work_id: `WORK-000027`
- relation: `PRIMARY_WORK`
- lineage confidence: `PRIMARY_CANDIDATE`

相关 Atomic Evidence：

- `K2E-W1-QM-0021-0015`：五天为一元，一个节气十五天分上中下三元；
- `K2E-W1-QM-0021-0016`：二十四节气 × 三元用局结构；
- `K2E-W1-QM-0021-0017`：甲/己为每元首日，并按符头地支分类上中下元；
- `K2E-W1-QM-0021-0018`：明确区分超神、接气、置闰；
- `K2E-W1-QM-0021-0019`：拆补法以**实际交节时辰**为换局点，进入新节气即使用新节气规定的局，同时继续向前取当前适用的甲/己符头判元，可形成残上、中、下、补上；
- `K2E-W1-QM-0021-0020`：作者主张拆补较准确，但这是作者立场，不是独立经验验证。

### 3.1 2004-02-04 来源案例

QM-SRC-0021 pdf:p67-p68 以 `2004-02-04 癸丑日` 说明拆补：

- 最近五日符头为前面的 `己酉`；
- 己酉属上元；
- **进入立春交节以后**，虽然继续用己酉判上元，但局数必须改用立春节气规定；
- 因而得到 `立春上元 -> 阳遁八局`。

这个案例给的是 method-specific post-transition expectation，而不是天气结果。

## 4. QM-SRC-0028 — 善天道《奇门遁甲讲义71页》

K2 状态：

- source_id: `QM-SRC-0028`
- work_id: `WORK-000018`
- relation: `PRIMARY_WORK`
- lineage confidence: `PRIMARY_CANDIDATE`
- reading: `COMPLETE / TEXT_LAYER_FULL / p1-p71`

相关 Atomic Evidence：

- `K2E-W1-QM-0028-0013`：五天一元、十五天一节气、三元结构；
- `K2E-W1-QM-0028-0015`：二十四节气三元局表；
- `K2E-W1-QM-0028-0016`：甲/己符头及三元地支分类；
- `K2E-W1-QM-0028-0017`：先以符头定元，再按所在节气查局；
- `K2E-W1-QM-0028-0018`：拆补法以**实际交节时辰**切换新节气局数体系；
- `K2E-W1-QM-0028-0019`：作者明确主张无闰拆补，同时承认少数比较中置闰法似乎更准，要求继续验证。

因此 0021 与 0028 对 weather-v0.1 method vector 的作用是：

`DISTINCT PRIMARY-WORK SOURCE SUPPORT FOR THE SAME CHAIBU COMPONENT VECTOR`

它们是不同 work 的来源支持，但这仍然只是 source-method credit，不是 empirical validation。

## 5. QM-SRC-0017 — 费秉勋《奇门遁甲新述》只能给共享子结构信用

Carrier identity：

- source_id: `QM-SRC-0017`
- work_id: `WORK-000224`
- relation: `PRIMARY_WORK`
- title: `奇门遁甲新述`
- author: `费秉勋`
- edition: `时代文艺出版社 1991年3月第1版`
- canonical_sha256: `f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`

视觉复核的 PDF p15-p17 / printed p6-p8 位于“超神接气和置闰”章节，支持：

- 每五天一局；
- 每局第一天日干必须甲或己；
- 上/中/下元地支分类；
- `1990-01-27 壬辰 -> 己丑五日组 -> 大寒下元 -> 阳遁六局`。

该 dated structural example 已进入 Engine regression 并 PASS。

但它所在的完整方法语境属于超神/接气/置闰传统。因此 0017 只能增加：

- 五日甲/己 head 的跨来源结构信用；
- 三元 branch class 的跨来源结构信用；
- 1990-01-27 这一 dated 元/局子结构 corroboration。

它不能被拿来证明：

- 费氏完整置闰法 = weather-v0.1 `CHAI_BU_FUTOU`；
- 拆补比置闰现实上更准确；
- weather prediction 有效；
- 完整九宫 plate 已验证。

## 6. 交节边界如何从“循环自证”升级为组合验证

旧 regression 曾让 lunar-java 自己找到立秋 boundary，再检查 Engine 是否随它切换；这只能证明 implementation internal consistency，不能独立验证 astronomical boundary。

现在分成三层：

### 6.1 Source policy

QM-SRC-0021 `0019` 与 QM-SRC-0028 `0018` 两个不同 PRIMARY_WORK 都明确：

`拆补在实际交节时辰切换到新节气局数体系。`

### 6.2 Independent astronomy

- 香港天文台 2026 年历：`2026-08-07 立秋 = 19:43 HKT`；
- 日本国立天文台 2004 暦要項：`2004-02-04 立春 = 20:56 JST`，即事件位于 `19:56 HKT` 这一分钟。

NAOJ 官方表只显示到分钟；公开秒级历算资料把 2004 立春放在约 `19:56:13 HKT`。由于 `QimenEngine.bySolar()` 当前只接受整数分钟，`19:56:00` 仍是交节前，`19:57:00` 才是第一个可表示的 post-transition sample。不得把“官方显示19:56”误解释成事件恰在 `19:56:00`。

### 6.3 Source + astronomy + Engine composite fixtures

当前两条独立天文 regression：

1. `2026-08-07`：Engine 第一个立秋 minute 必须与 HKO `19:43 HKT` 一致；同一癸丑日/同一己酉上元，交节前大暑阴7，交节后立秋阴2；
2. `2004-02-04`：QM-SRC-0021 给出 post-transition `立春上元阳8`，NAOJ 给出交节所在分钟；minute-resolution Engine 必须表现为 `19:56 大寒上元阳3 -> 19:57 立春上元阳8`。

机器测试：

`QimenJuMethodBoundaryFixtureTest > qm0021ChaibuExampleSwitchesAtFirstWholeMinuteAfterIndependent2004LichunInstant()` = PASS  
`QimenEngineTest > futouPreservesIndependentAstronomicalLiqiuBoundaryInsteadOfSwitchingAtMidnight()` = PASS

Knowledge Engine V1 CI #799 明确执行并通过两项测试。

这消除了“calendar dependency 自己找边界、再自己验证边界”的主要循环。

## 7. Gate 0 现在关闭到什么粒度

对 weather-v0.1 的冻结候选：

```text
WEATHER_JU_METHOD_CANDIDATE = CHAI_BU_FUTOU

DAY_GROUPING         = SOURCE_CROSS_SUPPORTED
YUAN_CLASSIFICATION  = SOURCE_CROSS_SUPPORTED
SOLAR_TERM_POLICY    = SOURCE_CROSS_SUPPORTED + INDEPENDENT_ASTRONOMY_REGRESSION_PASS
SUPER_CONNECT_POLICY = CHAIBU_RESIDUAL_POLICY_SOURCE_SUPPORTED
LEAP_POLICY          = NONE_FOR_CHAIBU_SOURCE_SUPPORTED
JU_LOOKUP             = SOURCE_CROSS_SUPPORTED
```

因此：

`JU_METHOD_VALIDATION = CLOSED_FOR_WEATHER_V01_CHAIBU_METHOD_IDENTITY`

这个 CLOSED 的含义只有：

> 当前 weather-v0.1 所谓 `CHAI_BU_FUTOU` 已被拆成明确 component vector；两个不同 PRIMARY_WORK 支持其核心拆补政策；实际交节 boundary 又由独立天文资料与 Engine regression 约束，因此可以作为后续 weather pre-Batch pipeline 的一个冻结方法身份使用。

它**不表示**：

- 拆补在现实预测上优于置闰；
- DAYCOUNT、ZHI_RUN 或其他 JuMethod 已验证；
- 所有拆补流派细节完全一致；
- 完整奇门九宫已验证；
- weather Batch 已可创建。

Gate A 仍缺第二张独立完整 dated plate，因此：

`WEATHER_BATCH_CREATION = FORBIDDEN`

## 8. 后续版本规则

如果以后改变任何一项：

```text
DAY_GROUPING
YUAN_CLASSIFICATION
SOLAR_TERM_POLICY
SUPER_CONNECT_POLICY
LEAP_POLICY
JU_LOOKUP
```

或者改变 calendar provider / time resolution，使交节边界发生变化，则必须：

- 升新的 JuMethod/model version；
- 重新跑 boundary fixture；
- 必要时重开 real-calendar / sham audits；
- 不得回填既有 Freeze/Outcome。

## 9. 认识论结论

当前最重要的区分是：

```text
SOURCE METHOD IDENTITY != EMPIRICAL SUPERIORITY
METHOD BOUNDARY CORRECTNESS != WEATHER PREDICTIVE VALIDITY
ONE METHOD VECTOR CLOSED != GLOBAL QIMEN VALIDATED
```

Gate 0 的本轮关闭只消除了“我们到底在实现哪一种拆补”的身份歧义；它没有给奇门理论本身增加经验信用。
