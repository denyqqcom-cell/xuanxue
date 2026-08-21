---
name: qimen-cases
description: >
  奇门遁甲案例研究技能。用于重建来源案例的方法路径、分类案例证据等级、识别后见污染与实现错误，
  不把书本复盘、直断条目或作者自述准确率直接当作预测有效性证据。
---

# 案例研究：Case Classification / Method Reconstruction v2.0

> 上位约束：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`。
>
> 核心原则：**案例先分类，再解释；复盘吻合不等于前瞻命中。**

## 一、为什么旧案例库必须迁移

旧版把财运、婚姻、健康、事业、出行、官讼等文献条目与“实战直断”放在同一运行层，并出现：

- 固定事项用神直接当答案入口；
- “吉门+吉星”“凶神+凶格”等机械判断；
- 书中作者声称“实践验证”即被视作已验证；
- 未给出可审计样本却写“预测有约八成准确率”；
- `玄武=假冒伪劣`、`惊门凶格=必有官司` 等确定性现实分类；
- 书本案例、项目复盘、真实未知结果预测没有证据等级区分。

这些内容可以保留为 SOURCE 研究对象，但不能继续作为自动裁决器。

## 二、Case Classification Protocol

所有案例至少分为以下一类：

### `SOURCE_RETROSPECTIVE_CASE`

书本、讲义、文章或作者提供的既知结果案例。用途：重建作者如何起局、取用神、选 feature、定应期和解释结果。

**不获得 Empirical Support credit。**

### `PROJECT_RETROSPECTIVE_REANALYSIS`

项目在结果已知或已接触背景后重新分析旧事件。用途：寻找解释自由度、错误类型、候选假设。

**不作为 clean hit。**

### `PROSPECTIVE_FROZEN_CASE`

结果未知时已完成协议冻结，并在 `K2_PROSPECTIVE_CASE_REGISTRY.jsonl` 留下可审计记录的正式前瞻案例。

只有这一类在满足独立性、可评分、污染控制后，才可能贡献 Empirical Support。

### `CONTAMINATED_CASE`

预测过程受到结果、新闻、人物背景、其他术数、外应或反馈后切换规则等污染。必须保留，不得为了提高命中率删除。

### `IMPLEMENTATION_FAILURE_CASE`

排盘、时间边界、局数、Role Map 执行、软件实现或输入本身有错误。此类用于工程纠错，不能把结果追认为原方法命中。

### `UNSCORABLE_ANECDOTE`

缺少原始预测、时间戳、明确目标、结果定义或其他必要资料，无法可靠评分的故事性材料。

## 三、来源案例的正确读取方式

对每个 `SOURCE_RETROSPECTIVE_CASE`，重建而不是照抄：

```text
source / page / chapter
question_domain
method_layer / method_family
setup_method / time_boundary_system / layout / deity system
Role Map
eligible features actually used
features present but ignored
competing interpretation branches
claimed timing method
known outcome at analysis time
post-hoc freedom observed
source conclusion
project audit
```

重点不是“这个案例断中了什么”，而是：

1. 作者真正优先使用了哪些信息；
2. 同一盘还有多少未使用但可事后调用的象；
3. 是否出现结果后选用神、格局、应期或辅助信息；
4. 规则是否只在该事项/流派成立；
5. 是否能转化成反馈前可失败的前瞻假设。

## 四、旧事项模板的当前地位

旧资料常见：

- 求财看生门、戊；
- 婚姻看六合、乙、庚；
- 健康看天芮、天心等；
- 事业看开门、值符；
- 官讼看惊门、庚；
- 出行看门、马星等。

当前统一处理为：

`SOURCE_DEFINED_ROLE_CANDIDATE`

不是跨方法族固定用神表。实际运行必须进入 `Role Map Freeze`；若存在多个合理 Role Map，反馈前保存竞争版本。

## 五、“直断”条目的地位

旧 skill 收录了《奇门直断》等来源的单位、工作、产品、婚姻、财运、官讼、健康条目，并出现“必定”“必有”“主……”等语言。

当前读取方式：

```text
SOURCE_CLAIM
→ identify object / layer / method family / role binding
→ define observable prediction
→ define failure condition
→ prospective test candidate
```

不得把这些条目直接改写成现实事实分类器。

例如：

- “玄武对应假冒伪劣”只能保留为来源象意/候选假设；
- “惊门凶格对应官司”只能保留为来源断语；
- 健康类人体、疾病、治疗方向属于 `HIGH_RISK_SOURCE_SYMBOLISM`，不是医学诊断。

## 六、准确率数字 Gate

任何总体准确率数字必须同时具备：

- 明确样本总数与连续取样规则；
- 预注册或可验证的反馈前预测；
- 完整 HIT / PARTIAL / MISS / VOID / CONTAMINATED 记录；
- 可审计评分标准；
- 基础概率/合理 baseline；
- 失败样本不丢失；
- 辅助信息与选择偏差说明。

旧版“预测有约八成准确率”不满足这些条件，当前标：

`UNSUPPORTED_ACCURACY_CLAIM`

不得继续展示为项目事实。

## 七、前瞻案例必须走 Registry

正式未知结果案例：

`Reality Baseline`
→ `Method / Setup / Time / Deity / State Freeze`
→ `Role Map Freeze`
→ `Eligible Features`
→ `Competing Branches`
→ `Timing Freeze`
→ `Frozen Prediction`
→ `K2_PROSPECTIVE_CASE_REGISTRY`
→ `Outcome Audit`

没有冻结记录的“后来应验”不能补登记成 clean prospective case。

## 八、Outcome Audit

正式案例结果统一：

`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`

同时记录错误类型，例如：

`INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_LAYER_ERROR / SETUP_METHOD_ERROR / TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE`

结果后修改只能进入新版本，不能覆盖原预测。

## 九、统计口径

案例统计只允许基于满足同一 scoring contract 的合格样本。

不得：

- 把书本 retrospective case 混进分母；
- 把 `CONTAMINATED / VOID / UNSCORABLE` 偷偷删掉；
- 只统计“有应验”的案例；
- 用不同问题域、不同方法层、不同评分标准混成一个总命中率；
- 用“部分应验”任意折算而不预先定义。

样本不足时输出“当前不足以估计准确率”，而不是填一个经验百分比。

## 十、来源索引的地位

legacy skill 曾归因/引用：

- 《奇门遁甲最新实例解析》；
- 曾子南《三元奇门遁甲讲义》；
- 《奇门遁甲应用学》；
- 《奇门直断》；
- 《日家奇门运筹秘法》；
- 其他图解/讲义类资料。

这些 attribution 先视作 legacy provenance，具体原文、页码、作者与版本需要回到 K2 source lineage / 原页重新核验；不得因为旧 skill 写了引用就自动升级 Source Fidelity。

## 十一、Case 与理论的关系

案例的主要价值是迫使理论面对失败条件。

一个新规则只有在：

`SOURCE/INFERENCE -> TESTABLE -> preregistered prospective cases -> outcome audit`

之后，才有资格进入 `PROVISIONAL / SUPPORTED` 讨论。

单个漂亮案例只能生成假设，不能生成全局规律。

---

*Cases v2.0 | 2026-08-21 | retrospective / prospective / contaminated / implementation-failure 分层；旧准确率与直断确定性退出运行层。*
