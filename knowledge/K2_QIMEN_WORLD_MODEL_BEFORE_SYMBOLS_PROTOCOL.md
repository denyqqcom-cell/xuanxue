# K2 Qimen World Model Before Symbols Protocol

版本：2026-09-04  
状态：ACTIVE_CONTRACT  
适用范围：奇门认知重构、实验 Engine、产品解释与验收报告  
Claim Extraction：BLOCKED  
Empirical Credit：NONE

## 1. 总原则

本项目从本版本起把 `WORLD_MODEL_BEFORE_SYMBOLS` 作为默认推演纪律：

`现实问题 -> 现实状态模型 -> 奇门映射 -> 冻结预测 -> 叙事呈现`

不得倒置为：

`盘面符号 -> 找口诀 -> 拼叙事 -> 反推现实`

符号层只能在现实世界模型冻结之后进入。任何来源规则、奇门符号、盘面格局都不能回写 M1 的现实事实。

## 2. M0–M4

### M0_INPUT_FREEZE

冻结问题定义、决策对象、时间窗口、用户已知事实、未知项、现实约束与允许的结果集合。M0 只描述输入，不进行奇门推断。

### M1_REALITY_ONLY

M1 是现实情境模型，只允许消费 M0 的现实输入与可直接核验的现实信息：参与者、资源、约束、时间、流程、基准事实、未知变量、竞争性现实解释。

硬边界：

`M1_REALITY_ONLY -> QIMEN_INPUT_FORBIDDEN`

M1 不读取九宫、门、星、神、干、格局、用神、值符值使或任何奇门派生状态；也不得为了配合后续奇门结果而修改现实模型。

### M2_SYMBOL_MAPPING

M2 只能在 M1 冻结后建立奇门映射假设。盘面事实、来源规则与项目自定义映射必须保留 provenance，不得伪装成现实事实。

### M3_FROZEN_PREDICTION

M3 在结果未知时形成可验证预测或明确 `ABSTAIN / UNEVALUABLE`。若存在多个合法输出，必须执行预先冻结的 tie-break 或保留多输出，不得结果后挑选命中项。

### M4_NARRATIVE_IMMUTABLE_PREDICTION

M4 只负责解释与呈现已经冻结的 M3。叙事可以增加来源、边界、反例、解释文字，但不得改变预测对象、方向、时间窗、类别、弃权状态或 M3 的冻结指纹。

`M4_NARRATIVE != SECOND_PREDICTION_CHANNEL`

## 3. 三链分离

项目状态必须分别报告：

`COGNITIVE / EMPIRICAL / PRODUCT`

- COGNITIVE：资料覆盖、来源结构、理论边界、场景模型与认知误区修正；
- EMPIRICAL：Plan / Batch / Freeze / Outcome / Review、比较器、公平评分、复现与不确定性；
- PRODUCT：Core、App、UI、Emulator、Physical、发布与用户可见 provenance。

禁止用一个“总完成度”把三条链压成单一百分比。资料覆盖率也不能冒充实验成熟度或产品成熟度。

资源规划默认目标为：认知资料约 60%，实验 Engine 约 25%，产品治理约 15%。这是资源配比，不是完成度 KPI，也不要求每个 commit 精确满足比例。

## 4. 四层工程验收

任何工程状态必须拆成：

`CORE / KNOWLEDGE / EMULATOR / PHYSICAL`

- CORE：确定性算法、数据结构、单元/集成测试；
- KNOWLEDGE：来源、认知、实验与治理合同的机器门禁；
- EMULATOR：Android 模拟器上的真实 App 行为；
- PHYSICAL：指定真机上的真实 App 行为。

`EMULATOR != PHYSICAL`

模拟器通过不能替代真机通过。

如果某一 exact-head 没有重新执行对应层，即使 App binary 与先前通过版本相同，也只能记：

`INHERITED`

不得写 exact-head PASS。

## 5. 11 步闭环

后续默认 Definition of Done：

1. `DEFINE`
2. `BASELINE`
3. `FAIL-FIRST`
4. `IMPLEMENT`
5. `UNIT VERIFY`
6. `SYSTEM VERIFY`
7. `PRODUCT VERIFY`
8. `PHYSICAL VERIFY`
9. `EPISTEMIC VERIFY`
10. `CHECKPOINT`
11. `ONLY THEN CONTINUE`

硬约束：任何一层失败，都不叠下一层改动。若某层因任务范围不适用，应明确写 `NOT_APPLICABLE`；若因工具/环境不可执行，应写 `BLOCKED / NOT_RUN`，不能伪装成 PASS。

## 6. 反 KPI 化

规则或理论组件接受 adversarial review 后，允许五种结果：

`KEEP / MERGE / DOWNGRADE / SPLIT / DELETE`

`DELETE` 只是五种证据驱动结果之一，不是必须完成的 KPI。不得为了显示“有进步”而强制删除规则。

`LATENT_FACTOR_NOT_REQUIRED`

只有当资料或前瞻数据支持 latent factor 假设且存在可区分预测时才研究；不得把“必须发现潜变量”设为阶段完成条件。

`WAVE1_PROGRESS_NOT_SINGLE_EXPERIMENT_THRESHOLD`

诸如 `10/37` 的资料完成计数只描述 corpus workflow，不是任何单一实验的样本量、成功门槛、停止规则或 empirical-credit 阈值。

## 7. 禁止伪精确

`NO_PSEUDO_PRECISION_SCORE`

不得把来源规则、项目推论或未验证假设压成类似“综合吉凶分 87”这样的单一精确数字，除非未来存在事前定义、可机器重算、经过前瞻校准且有明确统计含义的指标；即使存在，也必须使用其真实统计名称，不能伪装成客观吉凶真值。

## 8. 用户可见 provenance

产品 UI 最终必须把以下四类信息分开呈现，不能混成一段权威叙事：

1. 盘面事实：确定性排盘/历法/宫位字段；
2. 来源规则：来源确实记载的规则、作者立场与适用边界；
3. 项目推论：项目自己的关系建模、冲突处理、映射与推演；
4. 未经验证假设：尚无 empirical credit 的候选解释或预测假设。

用户上下文属于现实输入，不等于来源规则，也不能提高传统规则的证据等级。

## 9. 认识论边界

`CORE_PASS != KNOWLEDGE_TRUTH`

`KNOWLEDGE_PASS != EMPIRICAL_VALIDITY`

`EMPIRICAL_SIGNAL != METAPHYSICAL_TRUTH`

`PRODUCT_PASS != PREDICTIVE_VALIDITY`

World Model Before Symbols 的目的，是降低答错问题、结果后重构现实、符号先验污染和叙事回写，而不是预先宣告奇门有效。
