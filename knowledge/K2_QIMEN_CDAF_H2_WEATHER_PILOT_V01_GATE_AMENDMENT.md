# K2 CDAF-H2 Weather Pilot v0.1 — Pre-Batch Gate Amendment

状态：`ACTIVE_AMENDMENT / BATCH_NOT_READY`  
基础设计：`knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01.md`  
抽象结构审计：`knowledge/K2_QIMEN_CDAF_H2_IMPLEMENTATION_STRUCTURE_AUDIT_V01.md`  
真实公历审计：`knowledge/K2_QIMEN_CDAF_H2_REAL_CALENDAR_AUDIT_V01.md`  
Calendar control：`knowledge/K2_QIMEN_CDAF_H2_CALENDAR_EQUIVALENCE_CONTROL_V01.md`  
Sample/serial plan：`knowledge/K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md`  
JuMethod cross-source review：`knowledge/K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md`  
Empirical Credit：`NONE`

## 1. 为什么需要 amendment

基础 weather-v0.1 已经定义：

- 香港次日显著降雨窄域；
- HKO 16:30 PSR 作为 M1；
- `CORE_RAIN_SIGNAL_V01` 作为 M2 唯一新增信息；
- M2 只允许在 `M1=NO_RAIN10 && signal=true` 时改判；
- outcome proxy、入样、禁用修正规则等边界。

后续审计发现，正式 Batch 前不能只解决统计问题。还必须先回答：究竟使用哪一种定元法、该方法是否被来源结构验证、九星与所携天盘干是否有 chart-only fixture、signal 的真实公历结构是什么，以及 Qimen-derived signal 与普通 calendar/time transform 在信息来源上究竟能否区分。

本 amendment 不创建 Batch、不改写历史结果、不授予 empirical credit。

## 2. Gate 0 — JU_METHOD_VALIDATION

状态：`PARTIAL_MULTI_SOURCE_SHARED_STRUCTURE / FULL_METHOD_IDENTITY_OPEN / BLOCKING`

### 2.1 发现的实现错误

旧 `CHAI_BU_FUTOU` 曾用十日六甲旬首计算上中下元，把两个不同概念混为一谈：

- 六甲旬首：十个干支为一旬，用于旬首、遁干、旬空；
- 拆补符头：五日为一元，首日天干为甲或己，用于上中下元和局数。

当前实现已经把 `yuanOfFutou()` 改成回溯最近的五日甲/己符头；`xunInfo()` 的十日旬首算法保持不变。

Wave1 Evidence `K2E-W1-QM-0028-0016` 已记录：甲或己为每元首日天干，子午卯酉为上元、寅申巳亥为中元、辰戌丑未为下元。`K2E-W1-QM-0028-0018` 另记录拆补法以实际交节时辰切换节气局数体系。

### 2.2 当前候选方法

weather-v0.1 的排盘方法候选固定为：

`WEATHER_JU_METHOD_CANDIDATE = CHAI_BU_FUTOU`

不能继续默认使用 App 的 `CHAI_BU_DAYCOUNT`，也不能在 Outcome 后切换方法寻找有利结果。

这只是候选方法冻结，不代表 `CHAI_BU_FUTOU` 已经全局验真。

### 2.3 当前已有结构证据

目前已有：

1. 12 类甲/己五日符头类别的 source-rule regression；
2. `辛丑 -> 最近符头己亥 -> 中元` 的算法反例，用于防止退回十日旬首实现；
3. QM-SRC-0021 的 2004-05-29 戊午时 chart-only anchor：小满、符头法下元、阳遁八局、甲寅旬、值符天辅，并可核对外八宫九星位置；
4. `%5` 修复、遗留测试纠偏和 Prospective JuMethod freeze contract 已在 `d25cdcb65668634f36bb49b29edf739716fe3afd` 后四套 CI 全绿；
5. QM-SRC-0017 费秉勋《奇门遁甲新述》canonical carrier（SHA-256 `f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`）提供独立 cross-source corroboration：PDF p15-p16 明确五日一局、甲/己为局头及上中下元地支分类；PDF p17 给出 `1990-01-27 壬辰 -> 己丑五日组 -> 大寒下元 -> 阳遁六局` 的 dated structural example；
6. 该 1990 dated fixture 已进入真实 `QimenEngine` regression，并在 Knowledge Engine V1 CI #768 的 stable-core test 中通过 `壬辰 / 大寒 / 下元 / 阳6` 断言。

但第5项的信用必须严格限界：QM-SRC-0017 的相关章节属于“超神接气和置闰”语境。它独立支持的是**共享五日甲/己符头子结构**与该 dated 元/局结果，不意味着费氏完整置闰法与 `CHAI_BU_FUTOU` 等价，也不能把一个流派的来源信用迁移给另一个流派未被该来源陈述的交节/置闰政策。

因此当前认识是：

```text
SAME OUTPUT != SAME METHOD
SHARED SUBSTRUCTURE != METHOD EQUIVALENCE
```

目前仍只有一张足以承担完整九宫核对的 dated plate anchor；JuMethod 的交节边界与完整 method identity 也尚未关闭，所以不能把当前 FUTOU 实现标成 VERIFIED。

### 2.4 未通过来源证据的 fixture 必须降级

曾尝试加入 `2002-08-01 / 辛丑日 / 壬申时 / 阴遁一局` 作为第二 dated fixture。CI 显示该公历时点的时柱断言失败；进一步回查 Atomic Evidence 与 deep-source distillate 后，现有知识层只保留了该天气案例的方法/结果摘要，并没有保存这组日期—时柱元数据。

因此该 fixture 已撤出机器黄金断言，状态改为：

`SOURCE_PAGE_REVERIFICATION_REQUIRED`

不得为了让测试通过而把程序输出反写成“原书事实”，也不得把未留 provenance 的旧学习笔记当黄金盘。

### 2.5 证据粒度纪律

旧关闭条件曾要求每个 JuMethod fixture 都同时提供“日期、时柱、节气、元、局数”。这把**日级定元/定局命题**与**完整时盘命题**错误地绑成同一证据粒度。

现在改为：

`SOURCE GRANULARITY MUST BE SUFFICIENT FOR THE ASSERTED CLAIM`

- 若只测试五日符头、元、局等日级方法结构，原页给出 civil date + 日干支 + 元/局关系即可；测试中选择的安全 clock time 只能是计算采样参数，不得回写成 source fact；
- 若测试完整 plate、值符值使、九星八门或时盘关系，则必须有足够的来源时辰/时柱与盘面字段；
- 若测试交节边界，则必须有足以定位 boundary side 的 source-grounded 时间信息。

### 2.6 剩余关闭条件

Gate 0 关闭前仍至少需要：

- `CHAI_BU_FUTOU` 特有的实际交节切换政策至少有一个 source-grounded boundary fixture，而不是只靠一般规则文字；
- 完整 method vector 必须把 `DAY_GROUPING / YUAN_CLASSIFICATION / SOLAR_TERM_POLICY / SUPER_CONNECT_POLICY / LEAP_POLICY / JU_LOOKUP` 分开，禁止因为局数偶然一致而静默合并拆补与置闰；
- weather Plan 保持冻结 `qimen_ju_method = CHAI_BU_FUTOU` 与 exact engine blob；
- 若后续来源支持另一方法，只能另起 plan/model version，不得回填既有 Freeze；
- Gate A 所需完整 dated plate fixture 继续按更高字段粒度独立验证，不能由仅有日级元/局的 1990 例替代。

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

## 4. Gate B — CALENDAR_EQUIVALENCE_CONTROL

状态：`MACHINE_STRUCTURE_VERIFIED / BATCH_SCHEDULE_NOT_FROZEN / BLOCKING`

真实公历审计把问题从普通的“季节性混杂”提升成更严格的 calendar equivalence：

```text
civil datetime -> Qimen plate -> CORE_RAIN_SIGNAL_V01
```

当前 M2 没有引入独立于时间的新外部观测源。因此即使未来 `M2 > M1`，也不能直接解释为“奇门获得了日历之外的额外信息”。

v0.1 已冻结 control family 的定义，不使用 weather outcome 选 control：

- `M2_SHAM_PLUS_1`：在每一次实际节气段内部，把 CORE signal 序列循环平移 `+1日`；
- `M2_SHAM_MINUS_1`：同段循环平移 `-1日`。

两套 sham 保留同一节气段的 trigger 数量和节气 propensity，只破坏“具体日期的 exact plate alignment”。详见：

`K2_QIMEN_CDAF_H2_CALENDAR_EQUIVALENCE_CONTROL_V01.md`

### 4.1 机器结构验证

`QimenWeatherCalendarEquivalenceAuditTest` 已对 pinned engine 的 2000–2099 真实 civil calendar 执行结构审计，K2 App UI CI run `33113150132` = SUCCESS。

结果：

```text
complete_segment_count = 2399
complete_segment_days  = 36509
mixed_segments         = 2000
all_zero_segments      = 399

original_triggers      = 6498
plus_1_triggers        = 6498
minus_1_triggers       = 6498

plus_1_hamming_days    = 10352
minus_1_hamming_days   = 10352

audit_schedule_sha256 = 2760b8e94ada03b0a9d0e2b6dcae6ef27b73df31089f741536eddb5ab29710da
```

24 个节气逐项满足 original / +1 / -1 的 trigger counts 完全相同；两套 sham 又都在 10,352 个 civil-date positions 上改变 exact alignment。生成过程没有读取 HKO forecast 或 rainfall outcome。

这证明的是 `CONTROL_STRUCTURE_CREDIT`，不是 plate/predictive/empirical credit。

未来若要讨论 exact plate-alignment credit，必要条件至少是：

```text
M2_ORIGINAL > M2_SHAM_PLUS_1
AND
M2_ORIGINAL > M2_SHAM_MINUS_1
```

即使满足，也只能讨论“这个预注册时间变换的精确相位在该模型类中更有区分力”，不能宣称出现了独立于时间的信息源。

Gate B 剩余 Batch-specific 关闭条件：

- Batch horizon 冻结后重新生成该 Batch 的完整 sham schedule；
- schedule 生成必须只读取 calendar/engine，不读取 HKO forecast/outcome；
- segment identity、边界日、+1/-1 规则和 schedule hash 进入 Freeze；
- original 与两套 sham 共用同一 M1、outcome、exclusion、loss 和 serial-dependence treatment。

本次100年 audit hash 不能冒充未来 Batch schedule hash。

## 5. Gate C — REAL_CALENDAR_FUTOU_FREQUENCY

状态：`CLOSED_FOR_PINNED_ENGINE_STRUCTURE_ONLY`

已由真实 `QimenEngine` 对：

`2000-01-01 .. 2099-12-31` 共 `36,525` 个 civil dates，每日 `17:00 HKT`，`CHAI_BU_FUTOU`

逐日枚举。

结果：

- core signal days：`6,498`
- civil-date structural trigger rate：`17.79055441%`
- max consecutive trigger days：`4`
- max non-trigger gap：`33日`
- 每个触发日最多 1 条 core hit path
- 24节气触发率高度不均；冬至/惊蛰/清明/立夏为0
- 18个阴阳九局组合只有8个会触发

机器证据：

- `QimenWeatherRealCalendarAuditTest` = PASS
- K2 App UI CI run `33109453828` = SUCCESS
- report 已作为 CI artifact 上传

完整结果见：

`K2_QIMEN_CDAF_H2_REAL_CALENDAR_AUDIT_V01.md`

这个 gate 的 CLOSED 只表示“当前 exact engine+method 的真实日期结构已知”。若 `QimenEngine blob / CHAI_BU_FUTOU / 17:00 freeze / CORE signal` 任一改变，Gate C 自动重开。

它不授予任何 weather empirical credit，也不能用17.79%直接反推未来 Batch 天数。

## 6. Gate D — SERIAL_DEPENDENCE / SAMPLE_ADEQUACY

状态：`METHOD_DEFINED / BATCH_PARAMETERS_NOT_FROZEN / BLOCKING`

方法设计已落盘：

`K2_QIMEN_CDAF_H2_SERIAL_DEPENDENCE_SAMPLE_PLAN_V01.md`

v0.1 现在固定：

- cadence：每日 HKO 16:30 PSR / 17:00 HKT Freeze；
- 最小时间覆盖：从真实节气段起点开始，连续 `48` 个完整节气段；
- 若且仅若 Outcome 未读取且任一 pre-outcome information count `<80`，再增加完整 `24` 段；
- 最大 horizon：`72` 个完整节气段；
- 三个最低 pre-outcome information counts：Original-vs-M1、Original-vs-+1、Original-vs--1，各 `>=80`；
- Outcome 只允许在 acquisition 正式关闭后统一进入研究表；
- Outcome QC 后若 evaluable information 任一 `<80`，同一 Batch 直接 `INSUFFICIENT_INFORMATION_AFTER_OUTCOME_QC`，不得重新开放补样本；
- primary estimands：三个模型对比的 daily paired accuracy delta；
- serial dependence：Bartlett calendar-lag HAC，固定 `HAC_MAX_LAG=30 civil days`；
- family-wise alpha：0.05，三个 primary contrasts 用 Bonferroni 单侧阈值，`Z_CRITICAL=2.1280452342`；
- success / no increment / calendar alignment not distinguished / inconclusive / insufficient-information 已分别定义。

80 是 sample-planning floor，不是“80例验证有效”。它不授予经验信用。

Gate D 剩余 Batch-specific 关闭条件：

- 实际起始节气段进入 Freeze；
- 48/72 horizon、80门槛、HAC=30、三重比较阈值进入 Freeze；
- outcome quarantine / unlock procedure 进入 Batch contract；
- frozen station panel 与 data-completeness policy 确认；
- sample-plan exact file/hash 进入 Freeze。

## 7. 当前优先顺序

```text
0. JU_METHOD_VALIDATION [PARTIAL / FULL-METHOD IDENTITY OPEN]
        ↓
A. PLATE_PAIRING_VALIDATION [PARTIAL]
        ↓
B. CALENDAR_EQUIVALENCE_CONTROL [MACHINE VERIFIED / BATCH SCHEDULE NOT FROZEN]
        ↓
C. REAL_CALENDAR_FUTOU_FREQUENCY [CLOSED FOR PINNED ENGINE]
        ↓
D. SERIAL_DEPENDENCE / SAMPLE_ADEQUACY [METHOD DEFINED / BATCH PARAMETERS NOT FROZEN]
        ↓
E. Batch preregistration
        ↓
F. Freeze
        ↓
G. Outcome
        ↓
H. Batch Review
```

Gate C 的完成、Gate B/D 的方法定义，都不允许越过更靠前的 Gate 0/A。

## 8. 当前状态口径

```text
DOMAIN_DESIGN_DEFINED               = true
SOURCE_RULE_MINIMIZED               = true
M1_DEFINITION_DEFINED               = true
M2_UPDATE_FUNCTION_DEFINED          = true
OUTCOME_PROXY_POLICY_DEFINED        = true
WEATHER_JU_METHOD_CANDIDATE         = CHAI_BU_FUTOU

JU_METHOD_VALIDATION                = PARTIAL_MULTI_SOURCE_SHARED_STRUCTURE
JU_METHOD_FULL_IDENTITY             = OPEN
PLATE_PAIRING_VALIDATION            = PARTIAL
CALENDAR_EQUIVALENCE_CONTROL        = MACHINE_VERIFIED_NOT_BATCH_FROZEN
REAL_CALENDAR_FUTOU_FREQUENCY       = CLOSED_FOR_PINNED_ENGINE_STRUCTURE_ONLY
SERIAL_DEPENDENCE_SAMPLE_GATE       = METHOD_DEFINED_NOT_BATCH_FROZEN

BATCH_READY                         = false
BATCH                               = NONE
FREEZE                              = NONE
OUTCOME                             = NONE
EMPIRICAL_CREDIT                    = NONE
CLAIM_EXTRACTION                    = BLOCKED
```

如果其他文档仍以较宽松的 `DESIGN_READY` 描述 CDAF-H2，它只能理解为“已有可审计设计对象”，不得解释为“已经可以开始正式 Batch”。
