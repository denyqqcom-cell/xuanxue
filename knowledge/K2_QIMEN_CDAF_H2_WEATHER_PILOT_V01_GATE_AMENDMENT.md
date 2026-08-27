# K2 CDAF-H2 Weather Pilot v0.1 — Pre-Batch Gate Amendment

状态：`ACTIVE_AMENDMENT / BATCH_NOT_READY`  
基础设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
结构审计：`knowledge/K2_QIMEN_CDAF_H2_IMPLEMENTATION_STRUCTURE_AUDIT_V01.md`  
Empirical Credit：`NONE`

## 1. 为什么需要 amendment

基础 weather-v0.1 已经冻结：

- 香港次日显著降雨窄域；
- HKO 16:30 PSR 作为 M1；
- `CORE_RAIN_SIGNAL_V01` 作为 M2 唯一新增信息；
- M2 只允许在 `M1=NO_RAIN10 && signal=true` 时改判；
- outcome proxy、入样、禁用修正规则等边界。

后续审计发现，基础设计第 9 节把主要未关闭问题集中在 `SERIAL_DEPENDENCE / SAMPLE_ADEQUACY`，但这还不够。正式 Batch 前还必须增加两个更靠前的有效性门。

本文件不创建新 Batch，不改写历史设计，也不授予 empirical credit；它只把新发现的 blocker 明确升级为强制前置条件。

## 2. Gate A — PLATE_PAIRING_VALIDATION

状态：`OPEN / BLOCKING`

原因：

当前 `QimenEngine` 内部能够生成九星位置和 `tianYi`，但：

- `handoff/qimen/05_FIXTURES.jsonl` 没有完整九宫黄金盘；
- `handoff/qimen/06_CASES.md` 记录 chart independently rebuilt = 0；
- 因此 weather signal 所依赖的“天柱/天蓬所在宫所携天盘干”仍属于实验实现的一部分。

关闭条件：

1. 从可追溯来源建立至少一个 chart-only fixture；
2. fixture 必须包含足以独立核对的九星位置与天盘干配对；
3. 只验证盘面，不把书中天气结果或断语当作排盘正确性的替代证据；
4. 当前 weather signal 依赖的配对必须与 fixture 一致；
5. 若不一致，先修 engine / protocol 并升版本，旧 weather-v0.1 不得回填。

关闭前：

`WEATHER_BATCH_CREATION = FORBIDDEN`

## 3. Gate B — CALENDAR_CONFOUNDING_CONTROL

状态：`OPEN / BLOCKING`

结构审计在当前锁定实现的 360 个 engine-eligible contract states 中得到：

- core signal trigger = 64；
- state density = 17.78%；
- 不同节气 trigger/15 从 0 到 5，明显不均匀。

这意味着 signal 本身携带节气/季节结构。

因此未来即使 M2 相对 M1 改善，也必须区分：

- `plate-specific incremental information`；
- `calendar/season residual information`。

关闭条件：Batch preregistration 必须事先冻结一种 calendar-only control，并证明它不读取未来 outcome。可选方向包括：

- `M1.5 = M1 + calendar/season-only comparator`；
- 节气/季节 strata 内、保持触发率的 sham signal；
- 其他能把 calendar encoding 与具体盘面 mapping 分开的预注册 negative control。

不得在 Outcome 后根据哪个 control 最有利再选择方法。

关闭前：

`M2 > M1` 不能被直接解释为“奇门盘面增量”。

## 4. Gate C — SERIAL_DEPENDENCE / SAMPLE_ADEQUACY

状态：`OPEN / BLOCKING`

原基础设计中的统计 blocker 保持有效。

新增结构审计不会把 17.78% 自动转成固定天数或固定案例数，因为 M2 真正与 M1 分叉还要求：

`M1 == NO_RAIN10 && CORE_RAIN_SIGNAL_V01 == TRUE`

所以实际 discordant information rate 低于或等于结构 trigger rate。

关闭条件仍需在结果未知时冻结：

- sampling cadence / analysis unit；
- planned duration 或合法的 non-outcome-driven stopping rule；
- paired primary statistic；
- serial-dependence treatment；
- minimum information threshold；
- success / failure / insufficient-information decision rule。

## 5. 当前优先顺序

三个 blocker 不应并行乱解。

正确顺序：

```text
A. PLATE_PAIRING_VALIDATION
        ↓
B. CALENDAR_CONFOUNDING_CONTROL
        ↓
C. SERIAL_DEPENDENCE / SAMPLE_ADEQUACY
        ↓
D. Batch preregistration
        ↓
E. Freeze
        ↓
F. Outcome
        ↓
G. Batch Review
```

理由：如果盘面配对本身没有验证，讨论样本量没有意义；如果 calendar confounding 没有控制，统计显著也无法唯一归因给盘面符号。

## 6. 当前状态口径

从本 amendment 起，weather-v0.1 的执行口径固定为：

```text
DOMAIN_DESIGN_DEFINED           = true
SOURCE_RULE_MINIMIZED           = true
M1_DEFINITION_DEFINED           = true
M2_UPDATE_FUNCTION_DEFINED      = true
OUTCOME_PROXY_POLICY_DEFINED    = true

PLATE_PAIRING_VALIDATION        = OPEN
CALENDAR_CONFOUNDING_CONTROL    = OPEN
SERIAL_DEPENDENCE_SAMPLE_GATE   = OPEN

BATCH_READY                     = false
BATCH                           = NONE
FREEZE                          = NONE
OUTCOME                         = NONE
EMPIRICAL_CREDIT                = NONE
CLAIM_EXTRACTION                = BLOCKED
```

如果其他文档仍以较宽松的 `DESIGN_READY` 描述 CDAF-H2，它只能理解为“已有可审计设计对象”，不得解释为“已经可以开始正式 Batch”。
