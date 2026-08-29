# K2 奇门 JuMethod 跨来源复核 v0.1

状态：`PARTIAL_MULTI_SOURCE_STRUCTURAL_SUPPORT / METHOD_EQUIVALENCE_REJECTED / NO_EMPIRICAL_CREDIT`  
用途：区分“不同起局传统共享的五日符头子结构”与“完整 JuMethod 身份”，防止把局部一致误写成整套方法一致。

## 1. 研究问题

当前 `QimenEngine` 同时存在：

- `CHAI_BU_DAYCOUNT`；
- `CHAI_BU_FUTOU`；
- `ZHI_RUN`（当前 fail closed / unsupported）。

此前修复确认：拆补符头用于定元的时间单位是五日甲/己符头，而六甲旬首仍是十日单位，二者不能混用。

新的跨来源复核进一步发现：

> “甲/己五日符头”并不只存在于某一个命名方法里。不同传统可以共享这一子结构，却在超神、接气、置闰、交节切换等后续政策上分叉。

因此：

```text
shared substructure agreement
!=
full JuMethod equivalence
```

## 2. QM-SRC-0028 — 善天道《奇门遁甲讲义71页》

K2 状态：

- work_id: `WORK-000018`
- relation: `PRIMARY_WORK`
- reading: `COMPLETE / TEXT_LAYER_FULL / p1-p71`
- evidence: 50
- canonical_sha256: `bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243`

相关 Atomic Evidence：

- `K2E-W1-QM-0028-0016`：甲或己为每元首日天干；子午卯酉上元、寅申巳亥中元、辰戌丑未下元；
- `K2E-W1-QM-0028-0017`：先找符头判断上中下元，再结合节气查局；
- `K2E-W1-QM-0028-0018`：拆补法以实际交节时辰切换节气局数体系；
- `K2E-W1-QM-0028-0019`：作者明确偏向无闰拆补法，同时承认少数实践案例中置闰法似乎更准，要求继续验证。

因此 0028 对当前 `CHAI_BU_FUTOU` 的意义是：

`METHOD-SPECIFIC SOURCE SUPPORT CANDIDATE`

但 source support 仍不是 empirical validation。

## 3. QM-SRC-0017 — 费秉勋《奇门遁甲新述》

Carrier identity：

- work_id: `WORK-000224`
- title: `奇门遁甲新述`
- author: `费秉勋`
- edition: `时代文艺出版社 1991年3月第1版`
- canonical_sha256: `f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`
- pages: `419`
- 本次可访问 PDF SHA-256 与 K1 canonical SHA 完全一致：`CANONICAL_CARRIER_MATCH`

本次对 canonical carrier 的视觉复核：

### PDF p15 / printed p6

章节标题为“第二讲 超神接气和置闰”。正文明确说明：

- 每五天为一局；
- 每局第一天的日干必须是甲或己；
- 甲乙丙丁戊五日成一组，下一组己庚辛壬癸，再循环回甲。

### PDF p16 / printed p7

正文把每个节气上中下三元头一天的地支归类为：

- 上元：子、午、卯、酉；
- 中元：寅、申、巳、亥；
- 下元：辰、戌、丑、未。

并进一步给出甲/己与这些地支组成的符头干支类别。

### PDF p17 / printed p8

正文给出 dated example：

- `1990-01-27`；
- 日干支：`壬辰`；
- 位于 `己丑 -> 癸巳` 五日组；
- `己丑` 为这一元头一天；
- 己丑属于 `大寒下元`；
- 大寒处于阳遁区间；
- 大寒三元口诀为“三九六”，所以下元为 `阳遁六局`。

这个例子已经进入真实 `QimenEngine` regression，要求：

```text
dayGZ      = 壬辰
jieQi      = 大寒
yuanFutou  = 下元
yuan        = 下元
yinYang     = +1
ju          = 6
juMethodUsed= CHAI_BU_FUTOU
```

测试使用 12:00 只是远离交节边界的 engine sampling time；原书没有把 12:00 作为案例时柱，因此不得把该时间写成 source fact。

## 4. 这份独立来源到底增加什么信用

QM-SRC-0017 增加的是：

1. `甲/己五日符头` 并非 0028 单一课程中的孤立写法；
2. 上/中/下元的地支分类存在独立现代著作交叉支持；
3. `1990-01-27 -> 壬辰 -> 己丑五日组 -> 大寒下元 -> 阳6` 提供一个不同 work 的 dated structural fixture；
4. 当前 `%5` 修复不再只依赖同一教学 lineage。

它**不增加**：

- “拆补法比置闰法正确”的经验信用；
- `CHAI_BU_FUTOU` 与费氏完整置闰法等价的信用；
- weather prediction credit；
- 任意完整九宫 plate credit。

原因是该材料所在章节本身属于“超神接气和置闰”传统。它与 0028 的无闰拆补在五日符头子结构上相交，但完整 method policy 并不相同。

## 5. 当前 JuMethod 模型应怎样拆

以后不把起局法只保存成一个字符串标签，而至少概念上分成：

```text
DAY_GROUPING
    five-day 甲/己 head

YUAN_CLASSIFICATION
    branch class -> 上/中/下元

SOLAR_TERM_POLICY
    how current 节气 is selected / switched

SUPER_CONNECT_POLICY
    超神 / 接气 treatment

LEAP_POLICY
    置闰 / 不置闰

JU_LOOKUP
    solar-term × yuan -> ju
```

两个来源可以在前两层一致、后几层不同。

因此未来比较方法时，应比较 component vector，而不是看到最后 `ju=6` 一样就宣布同一方法。

## 6. 对 Gate 0 的影响

`JU_METHOD_VALIDATION` 不能关闭，但状态应理解为：

`PARTIAL / MULTI-SOURCE SHARED-STRUCTURE SUPPORT / FULL-METHOD IDENTITY OPEN`

已经新增的独立支持：

- 五日甲/己 head：multi-source structural support；
- 上中下元 branch class：multi-source structural support；
- 1990-01-27 大寒下元阳6：independent dated structural corroboration。

仍缺：

1. `CHAI_BU_FUTOU` 特有的交节切换政策需要 source-grounded boundary fixture；
2. 拆补与置闰必须作为不同完整 method vectors 并行保存，不能互相借信用；
3. 对完整 method 的验证仍需要更多不同节气/边界案例；
4. `PLATE_PAIRING_VALIDATION` 仍需第二张独立完整 dated plate，不由本例替代。

因此：

`WEATHER_BATCH_CREATION = FORBIDDEN`

## 7. 认识论更新

本轮反审新增一条方法纪律：

```text
SAME OUTPUT != SAME METHOD
SHARED SUBSTRUCTURE != METHOD EQUIVALENCE
```

如果两个流派在某一日期给出相同局数，只能给共享组件增加结构信用；不能把一个流派的来源信用迁移给另一个流派未被该来源陈述的政策。
