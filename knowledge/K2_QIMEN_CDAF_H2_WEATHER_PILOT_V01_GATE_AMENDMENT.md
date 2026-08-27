# K2 CDAF-H2 Weather Pilot v0.1 — Pre-Batch Gate Amendment

状态：`ACTIVE_AMENDMENT / BATCH_NOT_READY`  
基础设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
结构审计：`knowledge/K2_QIMEN_CDAF_H2_IMPLEMENTATION_STRUCTURE_AUDIT_V01.md`  
Empirical Credit：`NONE`

## 1. 为什么需要 amendment

基础 weather-v0.1 已经定义：

- 香港次日显著降雨窄域；
- HKO 16:30 PSR 作为 M1；
- `CORE_RAIN_SIGNAL_V01` 作为 M2 唯一新增信息；
- M2 只允许在 `M1=NO_RAIN10 && signal=true` 时改判；
- outcome proxy、入样、禁用修正规则等边界。

后续审计发现，正式 Batch 前不能只解决统计问题。还必须先回答：究竟使用哪一种定元法、该方法是否被来源结构验证、九星与所携天盘干是否有 chart-only fixture、以及 signal 是否只是携带节气/季节信息。

本 amendment 不创建 Batch、不改写历史结果、不授予 empirical credit。

## 2. Gate 0 — JU_METHOD_VALIDATION

状态：`OPEN / BLOCKING`

### 2.1 发现的实现错误

旧 `CHAI_BU_FUTOU` 曾用十日六甲旬首计算上中下元，把两个不同概念混为一谈：

- 六甲旬首：十个干支为一旬，用于旬首、遁干、旬空；
- 拆补符头：五日为一元，首日天干为甲或己，用于上中下元和局数。

当前实现已经把 `yuanOfFutou()` 改成回溯最近的五日甲/己符头；`xunInfo()` 的十日旬首算法保持不变。

Wave1 Evidence `K2E-W1-QM-0028-0016` 已明确记录：甲或己为每元首日天干，子午卯酉为上元、寅申巳亥为中元、辰戌丑未为下元。`K2E-W1-QM-0028-0018` 另记录拆补法以实际交节时辰切换节气局数体系。

### 2.2 当前候选方法

weather-v0.1 的排盘方法候选固定为：

`WEATHER_JU_METHOD_CANDIDATE = CHAI_BU_FUTOU`

原因是首个天气来源规则来自以拆补/符头体系起局的时家奇门资料；不能继续默认使用 App 的 `CHAI_BU_DAYCOUNT`，也不能在 Outcome 后切换方法寻找有利结果。

这只是候选方法冻结，不代表 `CHAI_BU_FUTOU` 已经全局验真。

### 2.3 当前已有结构证据

目前已有：

1. 12 类甲/己五日符头类别的 source-rule regression；
2. `辛丑 -> 最近符头己亥 -> 中元` 的算法反例，用于防止退回十日旬首实现；
3. QM-SRC-0021 的 2004-05-29 戊午时 chart-only anchor：小满、符头法下元、阳遁八局、甲寅旬、值符天辅，并可核对外八宫九星位置。

但当前只有一张完整 dated plate anchor，不能据此把所有日期、所有交节边界和整个 FUTOU 实现标成 VERIFIED。

### 2.4 未通过来源证据的 fixture 必须降级

曾尝试加入 `2002-08-01 / 辛丑日 / 壬申时 / 阴遁一局` 作为第二 dated fixture。CI 显示该公历时点的时柱断言失败；进一步回查 Atomic Evidence 与 deep-source distillate 后，现有知识层只保留了该天气案例的方法/结果摘要，并没有保存这组日期—时柱元数据。

因此该 fixture 已撤出机器黄金断言，状态改为：

`SOURCE_PAGE_REVERIFICATION_REQUIRED`

不得为了让测试通过而把程序输出反写成“原书事实”，也不得把未留 provenance 的旧学习笔记当黄金盘。

### 2.5 关闭条件

Gate 0 关闭前至少需要：

- 当前五日符头 algorithm tests 全绿；
- 至少增加一个与 2004-05-29 不同局数/不同节气或阴遁的、原页可复核 dated JuMethod fixture；
- fixture 的日期、时柱、节气、元、局数全部来自可追溯原页，而不是事后推回；
- 交节边界行为至少有一个 source-grounded fixture；
- weather Plan 明确冻结 `qimen_ju_method = CHAI_BU_FUTOU` 与 exact engine commit/blob；
- 若后续来源支持另一方法，只能另起 plan/model version，不得回填既有 Freeze。

关闭前：

`WEATHER_BATCH_CREATION = FORBIDDEN`

## 3. Gate A — PLATE_PAIRING_VALIDATION

状态：`PARTIAL / BLOCKING`

当前已建立 QM-SRC-0021 2004-05-29 戊午时 chart-only fixture，并将九星位置与其所携天盘干配对单独纳入机器核对。这个进展可以关闭“完全没有 plate fixture”的旧状态，但不能把一张来源盘推广为“完整九宫全局已验证”。

关闭条件：

1. 至少再有一张独立 dated plate fixture，最好覆盖不同阴阳遁/局数；
2. fixture 包含足以核对的九星位置与天盘干配对；
3. 只验证盘面，不导入书中天气结果或断语；
4. weather signal 所依赖的天柱/天蓬—天盘干配对与这些 fixture 一致；
5. 若 fixture 冲突，保留冲突并先修 engine/protocol，不允许选有利来源静默覆盖。

## 4. Gate B — CALENDAR_CONFOUNDING_CONTROL

状态：`OPEN / BLOCKING`

早期结构审计枚举过：

`24节气 × 3名义元 × 5个17:00酉时状态 = 360` 个抽象盘面合同状态，core signal 触发 64 个。

这个 `64/360 = 17.78%` 现在只能叫：

`ABSTRACT_PLATE_STATE_SPACE_DENSITY`

不能再解释为“真实公历平均每5.625天触发一次”。拆补法存在交节后的残上/中/下/补上结构，真实日期对三元并非天然等权。

即便以后用真实公历枚举重新得到触发频率，signal 仍可能携带节气/季节信息。因此 Batch preregistration 必须冻结 calendar-only control，例如：

- `M1.5 = M1 + calendar/season-only comparator`；或
- 在节气/季节 strata 内保持触发机会的 sham/negative-control signal；或
- 其他能分离 calendar encoding 与 plate-specific mapping 的预注册方法。

不得在 Outcome 后选择最有利的 control。

## 5. Gate C — REAL_CALENDAR_FUTOU_FREQUENCY

状态：`OPEN / BLOCKING FOR SAMPLE DESIGN`

在 Gate 0 的 JuMethod 算法稳定后，必须使用真实公历时点而不是名义三元笛卡尔积重新枚举：

- 固定 17:00 HKT；
- 固定 `CHAI_BU_FUTOU` 候选版本；
- 记录真实节气切换与五日符头；
- 计算 core signal 的真实 civil-date trigger rate、节气分布、连续/聚集结构；
- 不读取任何 HKO forecast 或 rainfall outcome。

它仍只是结构频率，不授予预测 empirical credit。

## 6. Gate D — SERIAL_DEPENDENCE / SAMPLE_ADEQUACY

状态：`OPEN / BLOCKING`

只有在真实公历 trigger structure 与 calendar confounding control 明确后，才设计统计窗口。

M2 真正与 M1 分叉还要求：

`M1 == NO_RAIN10 && CORE_RAIN_SIGNAL_V01 == TRUE`

所以实际 paired discordant information rate 必然不高于 core trigger rate。

Batch 前仍需冻结：

- sampling cadence / analysis unit；
- planned duration 或合法 non-outcome-driven stopping rule；
- paired primary statistic；
- serial-dependence treatment；
- minimum discordant/information threshold；
- success / failure / insufficient-information decision rule。

## 7. 当前优先顺序

```text
0. JU_METHOD_VALIDATION
        ↓
A. PLATE_PAIRING_VALIDATION
        ↓
B. CALENDAR_CONFOUNDING_CONTROL
        ↓
C. REAL_CALENDAR_FUTOU_FREQUENCY
        ↓
D. SERIAL_DEPENDENCE / SAMPLE_ADEQUACY
        ↓
E. Batch preregistration
        ↓
F. Freeze
        ↓
G. Outcome
        ↓
H. Batch Review
```

## 8. 当前状态口径

```text
DOMAIN_DESIGN_DEFINED            = true
SOURCE_RULE_MINIMIZED            = true
M1_DEFINITION_DEFINED            = true
M2_UPDATE_FUNCTION_DEFINED       = true
OUTCOME_PROXY_POLICY_DEFINED     = true
WEATHER_JU_METHOD_CANDIDATE      = CHAI_BU_FUTOU

JU_METHOD_VALIDATION             = OPEN
PLATE_PAIRING_VALIDATION         = PARTIAL
CALENDAR_CONFOUNDING_CONTROL     = OPEN
REAL_CALENDAR_FUTOU_FREQUENCY    = OPEN
SERIAL_DEPENDENCE_SAMPLE_GATE    = OPEN

BATCH_READY                      = false
BATCH                            = NONE
FREEZE                           = NONE
OUTCOME                          = NONE
EMPIRICAL_CREDIT                 = NONE
CLAIM_EXTRACTION                 = BLOCKED
```

如果其他文档仍以较宽松的 `DESIGN_READY` 描述 CDAF-H2，它只能理解为“已有可审计设计对象”，不得解释为“已经可以开始正式 Batch”。
