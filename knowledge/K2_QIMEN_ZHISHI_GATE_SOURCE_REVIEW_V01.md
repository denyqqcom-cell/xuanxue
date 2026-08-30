# K2 Qimen 值使门 Source / Implementation Review v0.1

状态：`SOURCE_IMPLEMENTATION_CORRECTION_ACCEPTED / GLOBAL_GATE_BOARD_NOT_VALIDATED / NO_EMPIRICAL_CREDIT`

目的：把本轮值使门修复限定为一个可追溯、可证伪的来源—实现纠错，不把两页原书案例扩张成“完整八门盘已验证”。

## 1. Carrier identity

来源：`QM-SRC-0017` / 费秉勋《奇门遁甲新述》 / `WORK-000224`。

canonical SHA-256：

`f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`

本轮在项目会话已上传 PDF 上重新计算 SHA-256，与项目 canonical identity 完全一致，因此本次 p24-p25 visual review 不依赖文件名相似性，也不依赖旧 distillate 转述。

页码映射：正文 printed p24 = PDF p33；printed p25 = PDF p34。

## 2. Source object

printed p24 给出阳遁一局丙寅时案例，并明确规则：

> 直符随时干，直使随时宫

该例 source-local state 为：

```text
YIN_YANG = YANG
JU       = 1
HOUR_GZ  = 丙寅
XUN      = 甲子旬
ZHI_SHI  = 休门
SOURCE_START_PALACE = 坎1
SOURCE_TARGET_PALACE = 震3
```

printed p25 给出阴遁九局戊戌时案例。甲午旬的辛在乾6，值使为开门；原页逆推时宫明确按九宫数字序计数：

```text
6 -> 5 -> 4 -> 3 -> 2
```

最后值使开门落坤2。

该页同时保留“若最终时宫落中五，则门寄坤二”的 center-hosting 处理。这里必须区分：

```text
CENTER_5_PARTICIPATES_IN_TRAVEL_COUNT = true
FINAL_TARGET_5_HAS_NO_GATE = true
FINAL_TARGET_5_HOSTS_TO_KUN2 = true
```

“途中经过 5”与“最终落 5 后寄宫”不是同一个动作。

## 3. Historical implementation error

修复前 `QimenEngine` 的值使 target 计算在每一步遇到 5 时立即改写为 6（阳）或 4（阴）。因此 5 被从 travel count 中删除。

旧实现等价于：

```text
NEXT == 5
    -> SKIP_CENTER_IMMEDIATELY
```

这与 QM-SRC-0017 printed p25 的 `6 -> 5 -> 4 -> 3 -> 2` 直接冲突。

该错误不能由既有 weather Gate A 掩盖，因为 Gate A 只关闭 weather-v0.1 实际依赖的：

`palace -> (九星, carried heaven stem)`

它从未授予完整门盘信用。

## 4. Fail-first reproduction

先新增 source-defined regression：

`ziwei-core/src/test/kotlin/com/xuanxue/qimen/QimenSourceGateFixtureTest.kt`

包含：

1. `qm0017_yang1_bingyin_zhiShi_xiu_gate_lands_on_zhen3`
2. `qm0017_yin9_wuxu_zhiShi_kai_gate_counts_center5_and_lands_on_kun2`

commit：`fa433339fabd7a6dcd649974ea0fb50ad79867fd`

Knowledge Engine V1 CI #827 的真实失败结果：

```text
阳遁一局 / 丙寅 / 休门 -> 震3    PASS
阴遁九局 / 戊戌 / 开门 -> 坤2    FAIL
61 core tests / 1 failed
```

因此冲突被隔离为“跨中五计数策略”，而不是泛化成“全部八门算法错误”。

## 5. Minimal correction

`QimenEngine` 只修改值使 target travel：

```text
START = 旬首遁干所在九宫
TRAVEL = 按九宫数字 1..9 阳顺 / 阴逆正常计数
CENTER_5 = 正常参与 travel
IF FINAL_TARGET == 5:
    HOST_GATE_AT = 坤2
ELSE:
    HOST_GATE_AT = FINAL_TARGET
```

未借机修改：

- JuMethod；
- 地盘三奇六仪；
- 九星转盘；
- `Gong.tianGan` carried-heaven-stem；
- 神盘；
- 日空 / 时空；
- 马星；
- weather `CORE_RAIN_SIGNAL_V01`；
- 吉凶判断与解释层。

修复 commit：`3b695096a997f661091b72e524b182ac5d6235eb`。

新 `QimenEngine.kt` Git blob：

`3a741348b46a43ef1f2e2bffe7c0a8be12ec42cd`

Knowledge Engine V1 CI #828 已完成 SUCCESS，说明新 source fixtures 与既有 core regression 同时通过。

## 6. Why the weather model must still repin

这次实现变化发生在门盘，而 `CORE_RAIN_SIGNAL_V01` 只读取：

```text
九星
Gong.tianGan
palace
```

因此从代码依赖图看，weather CORE 没有直接消费 `renMen`。

但项目既有 fail-closed 协议绑定的是 exact whole-engine blob，而不是“我们主观认为相关的几行”。所以 #215 正确拒绝新 Engine：

```text
expected old V02 engine blob
!=
actual new V03 engine blob
```

处理方式不是放宽 gate，而是：

1. 升 candidate model / engine version；
2. 重新运行 abstract weather-state、real-calendar、calendar-equivalence audits；
3. 比较 V02/V03 weather-relevant outputs；
4. 只有实际审计显示等价时，才记录“weather-relevant structural equivalence”。

即使全部统计不变，也只能说明本次门盘纠错没有改变已审计的 weather feature family，不能说明完整 Engine 等价。

## 7. Credit boundary

本轮可获得：

```text
SOURCE_CREDIT = QM-SRC-0017 p24-p25
IMPLEMENTATION_CORRECTION_CREDIT = YES
FAIL_FIRST_REPRODUCTION = YES
CORE_REGRESSION = PASS_ON_CI_828
```

不得获得：

```text
GLOBAL_GATE_BOARD_VALIDATION = NO
ALL_QIMEN_SCHOOLS_EQUIVALENT = NO
FULL_QIMEN_MATURITY_UPGRADE = NO
EMPIRICAL_CREDIT = NONE
CLAIM_EXTRACTION = BLOCKED
```

后续若其他 PRIMARY_WORK 对中五计数、寄宫或门盘转动给出冲突规则，必须保留 source conflict；不得用本次两例把其他传统消音。
