# 奇门当前方法约束层（2026-08-21）

状态：**ACTIVE / AUTHORITATIVE OVERLAY / v2.2**

适用范围：后续奇门学习、解盘、技能调用、案例复盘、前瞻验证。本文件用于约束旧版《奇门遁甲知识库》与尚未完全迁移的 `qclaw` 内容。

> 这不是新的“圣经”。它是一组当前有效、可被反例修改/缩窄/废弃的认识论约束。

## 一、为什么需要这一层

旧知识库和技能文件经历过多轮快速学习与修补，其中部分规则由单一案例、少量复盘或书本断语直接升级而来。随着 `QM-SRC-0016` 与 `QM-SRC-0001` 全书 Evidence / Book Distillate 完成，以及 gexia/gongpan runtime migration 深查，已确认至少有五类污染：

1. **书证污染**：把“书里这么说”误写成“现实中已经成立”；
2. **后见污染**：一次失败后形成补丁，再扩张成全局规律；
3. **自由度污染**：多种用神、格局、起局法、时间族、八神体系、旺衰算法、外应可在结果出来后任意切换；
4. **执行漂移**：反省日志已改，workflow/skill 仍按旧规则执行；
5. **类型污染**：把结构、象意、状态、Role、时间配置、方法专用规则压成同一“吉凶词典”。

旧资料仍保留为历史知识与 SOURCE 层，但不得越过本约束层直接获得“已验证真理”地位。

## 二、四层强制分离

每个关键判断必须区分：

- **SOURCE**：某书、某门派、某作者明确提出的规则或案例；
- **INFERENCE**：项目基于当前问题作出的情境转译、关系推演或抽象；
- **EMPIRICAL_SUPPORT**：反馈前冻结、结果后可核验的独立支持；
- **CONTAMINATION**：新闻、既知结果、求测者背景、外貌、外应、其他术数、搜索资料等可能帮助答案但妨碍归因的信息。

书证再多，只能提高 Source Fidelity；除非经过独立验证，否则不能自动提高 Empirical Support。

## 三、当前已撤销的全局硬规则

### 1. 固定全局优先级
旧：`开门 > 值符 > 生门 > 星神`

现：**DEPRECATED AS GLOBAL RULE**。优先级必须绑定问题类型、方法族、盘式、角色与任务；若某方法族确有顺序，必须反馈前冻结并只在其适用域测试。

### 2. 逢空固定翻译
旧：`逢空 = 方向待定`

现：**CANDIDATE / CONTEXT_REQUIRED**。空亡先作为状态特征，不把“逢空必凶”换成新的“逢空必待定”。

### 3. 凶格固定计分与相乘
旧：`凶格叠加相乘，>=3 分直接断大凶`

现：**DEPRECATED AS OPERATIONAL RULE / UNVERIFIED HEURISTIC**。如未来研究量化模型，须定义独立特征、权重、基线、校准方式并前瞻检验，且避免同一底层结构重复计票。

### 4. 旺衰固定折扣
旧：`旺相=全额，休囚=减半，四害自动打折/加重`

现：**REJECT FIXED COEFFICIENT SEMANTICS**。旺衰、空、墓、刑、迫仍可做 feature，但作用方向与强度必须绑定具体方法族、状态系统、事类与对象。

### 5. “三次即验证”
旧：`>=3 次独立真验证 = 已验证`

现：`>=3` 只是一项进入 **PROVISIONAL** 的最低信号之一；还必须检查预注册、独立性、基础概率、失败样本、选择偏差、污染、负对照与适用域外表现。

### 6. 强制先读三条新闻
旧：`确认对象存在 -> 查>=3条宏观新闻 -> 再看盘`

现：对象存在属于 Reality Baseline；新闻属于 **AUXILIARY CHANNEL**。研究奇门本体贡献时，应先 method-only freeze，再加入背景并记录 delta。

## 四、Method-Layer Gate：先确定“在用哪一种奇门”

新案例必须先冻结一个主层：

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

一个方法层的 miss 不得由另一个层结果后救援。需要 A/B 时，反馈前并行冻结并分别计分。`RITUAL_AUXILIARY` 默认不进入 empirical scoring。

## 五、起局、盘式、时间与八神体系是一等变量

至少显式记录：

```text
method_layer
method_family
setup_method
setup_calibration = PINGQI | DINGQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU | CHAOSHEN | ZHIRUN | JIEQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
time_family = YEAR | MONTH | DAY | HOUR | NOT_APPLICABLE
layout_method
deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
hour_omen_family
ritual_layer
bureau_table_source
```

未知项不得根据结果挑值。若该变量对模型必要却未解决，模型应停在 `CONTEXT_REQUIRED`，而不是继续出可评分预测。

### 八神体系

梁书使用勾陈/朱雀体系，现代资料常见白虎/玄武体系。当前平行保存：

- 不静默改名；
- 不在一盘互借象意；
- 未经来源/版本/布局拆解，不假设天然同义；
- 比较时采用反馈前冻结的独立模型。

## 六、State-System Gate：旺相休囚算法本身也必须冻结

深查旧 `qimen-gongpan` 发现，同一文件对天蓬状态出现互相相反的示例：一处“旺亥子、相寅卯”，另一处“旺寅卯、相亥子”。这证明“旺衰”不能继续被假设为一个无需声明的统一算法。

正式模型新增：

```text
star_state_system
door_state_system
```

规则：

- 使用九星/八门季节状态时，必须在结果未知时绑定明确 source/method system；
- 不使用时写 `NOT_APPLICABLE`；
- 可评分的 `FROZEN/RESOLVED` 模型不得保留 `CONTEXT_REQUIRED`；
- 若存在竞争系统，应建立独立 A/B case，而不是结果后选择较贴合的一套；
- state-system change after feedback 不能修补原 score。

这只是反后见约束，不表示任何一套旺衰算法已经被证明正确。

## 七、从模板解盘改为受约束情境推演

当前流程：

`Reality Baseline`
→ `Question Domain`
→ `Method-Layer Freeze`
→ `Time Family + Setup Calibration + Seasonal Alignment Freeze`
→ `Deity-System / Layout Context Freeze`
→ `State-System Freeze`
→ `Role Map Freeze`
→ `Bureau / Structural Lookup`
→ `Eligible Feature Set`
→ `Component / Relation Analysis`
→ `Pattern Registry`
→ `Competing Interpretation Branches`
→ `Timing Freeze`
→ `Frozen Prediction`
→ `Prospective Registry`
→ `Optional Auxiliary Context Ablation`
→ `Outcome Audit`
→ `Rule Lifecycle Update`

关键差异：情境化不等于自由发挥；推演越灵活越需要反馈前冻结；叙事越漂亮越不能把叙事本身当证据。

## 八、星门神奇仪宫的使用原则

星、门、神、奇仪、宫位、旺衰、生克、空墓刑迫、伏吟反吟、格局均先视为候选信息层。

至少问：

1. 当前问题域中它代表谁或什么？
2. 角色映射是 SOURCE_DEFINED、METHOD_DEFINED 还是 CONTEXT_INFERRED？
3. 它是结构、状态、来源象意，还是项目推演？
4. 与其他信号是独立证据还是同一底层结构的重复包装？
5. 若移除该特征，结论是否改变？
6. 什么结果会证明当前解释错了？

九星、门、神等固定“吉/凶”标签最多作为传统 prior，不能直接输出现实 verdict。

## 九、Pattern / Component 先分类，再谈象意

`qimen-gexia` 当前至少区分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

`qimen-gongpan` 当前至少区分：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

类型不明时，不能通过“查更多象意”填空。不同格名若共享同一底层结构，不得多重计票。

## 十、Lookup Determinism 不等于 Predictive Validity

十八局等机械查表结构可以降低排盘自由度，但必须分开：

`Source Fidelity != Lookup Determinism != Empirical Support`

- Source Fidelity：是否忠实复刻来源；
- Lookup Determinism：同一输入是否稳定得到同一结构；
- Empirical Support：是否在未知结果前瞻测试中优于合理基线。

fixture / regression / runtime-contract PASS 都不得表述为“预测法已经验证”。

## 十一、叙事与多重解释

允许多个合理解释，但必须反馈前保存竞争分支，记录前提、主导证据、区分观察与失败条件。反馈后只能评分，不能新造分支再算原预测命中。

`叙事连贯性` 只评价解释质量，不等于经验支持。

## 十二、书本案例、仪式材料与高风险象意

书本案例主要用于理解作者选择信息、找适用边界、暴露自由度、生成假设与发现失败模式。没有反馈前记录/独立结果的案例不能证明准确率。

符咒、步斗、禁敌、博奕等可作为 SOURCE / ritual-history 研究，默认不进入普通预测评分。

传统犯罪、牢狱、死亡、癌症、心脑血管等星门神宫类象属于 `HIGH_RISK_SOURCE_SYMBOLISM`，不得作为事实分类器、医学诊断或专业结论。

## 十三、Reality Baseline 与现实常理

“结合实际”不是拿现实信息替盘面圆结果，而是确认对象、时间、地点、事件定义正确；区分已知与未知；记录基础概率；高风险领域不以术数替代专业判断。

Reality Baseline 先于玄学解释，但 method validation 中必须与 auxiliary attribution 分离。

## 十四、Prospective Case Registry

正式未知结果测试遵循：

`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`

并登记：

`knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

反馈后不得覆盖原 case 的冻结字段，包括：

- 起局/校准；
- 方法层/时间族；
- 八神体系；
- `star_state_system / door_state_system`；
- Role Map；
- eligible features / patterns；
- 竞争分支、应期；
- auxiliary policy。

改变这些内容必须创建新模型版本/`case_id`。污染案例保留。

## 十五、规则生命周期

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

允许反向：

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`

渐进式迭代不是“旧规则只加不删”，而是修改有版本、删除有证据、边界有记录。

## 十六、Prediction Protocol Freeze != Theory Freeze

单次预测必须冻结协议；跨书、跨案例、跨版本的理论必须保持可推翻。Method-Layer Gate、State-System Gate、四层认识论乃至整个流程都可以在更强证据下被 `NARROW / REVISE / SPLIT / DEPRECATE / REJECT`。

## 十七、当前待验证核心假设

仍不是定论：

- Method-Family-Specific Priority 是否优于固定全局优先级；
- Method-Layer Gate 是否显著减少事后救援；
- 平气/定气、正授/超神/置闰/接气是否存在稳定前瞻差异；
- 勾陈朱雀 vs 白虎玄武是否有可重复增量；
- 不同九星/八门 state systems 是否产生稳定、可区分的预测差异；
- 九星固定标签是否劣于条件化模型；
- 九星十二时辰应克是否优于基础概率与 shuffled controls；
- 年/月/日/时传统层级是否存在；
- Role Map Freeze、多分支预注册、辅助信息消融是否真正改善可复现性与校准。

这些问题由后续文献与前瞻实验推进，不以“大师说法”裁决。

## 十八、执行优先级

发生冲突时：

`K2 Evidence / Book Distillate / Method Delta / Pre-Book Retrospective`
→ `CURRENT_METHOD_CONSTRAINTS.md`
→ `K2 Prospective Case / Source Fixture Protocols`
→ `当前版本理论草案`
→ `qclaw 技能与旧知识库`
→ `更早修炼日志`

这里的“优先”是项目运行约束优先级，不是玄学规则真值等级。
