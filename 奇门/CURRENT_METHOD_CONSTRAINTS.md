# 奇门当前方法约束层（2026-08-21）

状态：**ACTIVE / AUTHORITATIVE OVERLAY / v2.4**

适用范围：后续奇门学习、解盘、技能调用、案例复盘与前瞻验证。本文件约束旧版《奇门遁甲知识库》及尚未完全迁移的 `qclaw` 内容。

> 这不是新的“圣经”。它是一组当前有效、可被反例修改、缩窄、压缩或废弃的认识论与执行约束。

## 一、认识论分层

每个关键判断必须区分：

- **SOURCE**：某书、某门派、某作者明确提出的规则或案例；
- **INFERENCE**：项目基于当前问题作出的情境转译、关系推演或抽象；
- **EMPIRICAL_SUPPORT**：结果未知时已冻结、结果后可核验的独立支持；
- **CONTAMINATION**：新闻、既知结果、求测者背景、外应、其他术数、搜索资料等可能帮助答案但妨碍归因的信息。

`Source Fidelity != Lookup Determinism != Applicability != Empirical Support`

书证再多，只提高来源可追溯/共识；fixture、回归测试或 runtime contract 通过，只说明对应的来源复刻或执行约束更可靠，不代表预测现实有效。

## 二、已撤销的全局硬规则

以下旧规则不得再直接运行：

- 固定 `开门 > 值符 > 生门 > 星神`；
- `逢空 = 方向待定` 或其他单一固定翻译；
- `凶格>=3分直接大凶`、凶格相乘；
- `旺相=全额 / 休囚=减半 / 四害自动折扣`；
- `>=3次独立案例 = 已验证`；
- 强制先查若干新闻再把结论归因于奇门本体。

若仍有研究价值，只能作为 `CANDIDATE / UNVERIFIED_HEURISTIC`，另行预注册测试。

## 三、Method-Layer Gate

新案例先冻结主方法层：

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

一个方法层的 miss 不得由另一个层结果后救援。需要比较时，反馈前并行建立独立 A/B case。`RITUAL_AUXILIARY` 默认 `eligible_for_scoring=false`。

## 四、Setup / Time / Layout / Deity Gate

起局是一组会改变结构结果的模型选择。至少显式记录：

```text
method_layer
method_family
setup_method = FUTOU_ZHIRUN | CHAIBU_SOLAR_TERM | MAOSHAN_SOLAR_TERM | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
setup_calibration = PINGQI | DINGQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU | CHAOSHEN | ZHIRUN | JIEQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
time_boundary_system = CIVIL_MIDNIGHT | ZI_START_23 | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
time_family = YEAR | MONTH | DAY | HOUR | NOT_APPLICABLE
layout_method
deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
hour_omen_family
ritual_layer
bureau_table_source
```

若某变量对模型必要但未解决，必须停在 `CONTEXT_REQUIRED`；不使用写 `NOT_APPLICABLE`。可评分的 `FROZEN / RESOLVED` 模型不得把必要字段留为 `CONTEXT_REQUIRED`。

### 4.1 Setup Method Gate

旧 `qimen-qiju` 已发现超神/接气方向冲突、拆补算法描述冲突、拆补/茅山定义重叠、宫号顺序与旋转语言混用。因此不得默认某一 setup “天然正确”。不同算法若生成不同盘，反馈前 A/B。

### 4.2 Time-Boundary Gate

日界/子时规则是模型变量。结果后切换日界不能修补原预测。

### 4.3 Deity-System Gate

梁书勾陈/朱雀体系与现代常见白虎/玄武体系平行保存：

- 不静默改名；
- 不互借象意；
- 不假设天然同义；
- 比较时反馈前独立冻结。

## 五、State-System Gate

正式模型记录：

```text
star_state_system
door_state_system
```

旧 `qimen-gongpan` 同一文件对天蓬状态曾出现相反示例。使用九星/八门旺相休囚时必须绑定明确 source/method system；不使用写 `NOT_APPLICABLE`；竞争系统反馈前 A/B。结果后切换 state system 不能修补原 score。

这只是反后见约束，不表示任何一套旺衰算法已被证明正确。

## 六、Baseline Firewall

Reality Baseline 不能成为“把现实答案先塞进 method-only”的入口。

基础信息必须先分：

### `NEUTRAL_SETUP_FACTS`

仅用于识别/定义待测对象，例如：对象身份、输入时间/地点/时区、问题定义、结果评分口径和必要的非预测性结构事实。

### `PREDICTIVE_AUXILIARY_FACTS`

本身可能直接提高结果预测力，例如：已发布天气预报、市场期货/赔率/盘口、重大新闻、当事人既有行为趋势、外应、其他术数或任何已经接近答案的现实线索。

这些信息必须走 `auxiliary_information_policy`，使用：

`method-only -> freeze -> context-augmented -> record delta`

若预测者在 freeze 前已接触，则标 `PRE_EXPOSED`；不得伪装成 clean method-only。

真实性不是“可以进入 baseline”的充分条件。

## 七、Role Map / Component / Pattern

Role Map 必须标明角色来源：`SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED`。多个合理用神反馈前保存竞争 Role Map；结果后换用神只能算模型修改。

`qimen-gongpan` 至少区分：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

`qimen-gexia` 至少区分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

同一底层结构不得因多个格名重复计票。来源内部冲突保留为 `SOURCE_INCONSISTENCY / CONFLICT_CANDIDATE`，不能结果后选最贴合的一条。

## 八、Branch-Discrimination Gate

“预注册很多解释”不等于可证伪。

`competing branches` 必须满足：

1. 分支数量有限，不能枚举到覆盖几乎全部结果空间；
2. 反馈前指定 `primary branch`，或冻结明确概率/权重；
3. 每条分支写可观察的区分条件；
4. 每条分支写明确失败条件；
5. 结果后只能评分各分支，不能用“任一分支命中”给整个模型记 `HIT`；
6. 若各分支无法由未来观察区分，应合并或标 `UNSCORABLE`。

多分支的目的，是暴露不确定性，不是预先占满所有答案。

## 九、Ambiguity-Debt Gate

`CONTEXT_REQUIRED` 是暂时的诚实状态，不是永久逃生门。

对影响可评分模型的未解决项，必须选择之一：

- 在反馈前拆成明确 A/B；
- 暂时移除该 feature/method layer，并写 `NOT_APPLICABLE`；
- 保留为 `AMBIGUITY_DEBT`，明确阻塞对象、需要的证据和解除条件。

不得长期把“无法选择”当成不接受失败的理由。新的来源冲突也不得直接变成永久新字段；先判断它是否真实改变模型输出。

## 十、Source-Topology Gate

2026-08-21 梁书十八局复核发现：主审曾把 spread 同一 raster 的右侧标题误配给左侧表体，validator 和 CI 因共享错误 expected mapping 而全部 PASS。

因此 VISUAL_REQUIRED 后新增：

`Visual Presence != Semantic Association`

图表/跨页资料至少检查：

`Raster Identity`
→ `Printed-Page Topology`
→ `Semantic Object Identity`
→ `Internal Structural Check`
→ `Sparse Anchor Verification`

来源异常在排除 crop、跨页错配、scan-order、printed-page sequence、table-body identity 等解释前，不得升级为 `SOURCE_INCONSISTENCY`。

## 十一、受约束情境推演流程

当前运行链：

`Reality Baseline`
→ `Baseline Firewall`
→ `Question Domain`
→ `Method-Layer Freeze`
→ `Setup Method + Calibration + Seasonal Alignment Freeze`
→ `Time-Boundary + Time-Family + Layout + Deity Freeze`
→ `State-System Freeze`
→ `Role Map Freeze`
→ `Bureau / Structural Lookup`
→ `Eligible Feature Set`
→ `Component / Relation Analysis`
→ `Pattern Registry`
→ `Competing Interpretation Branches`
→ `Branch-Discrimination Gate`
→ `Timing Freeze`
→ `Frozen Prediction`
→ `Prospective Registry`
→ `Optional Auxiliary Context Ablation`
→ `Outcome Audit`
→ `Rule Lifecycle Update`
→ `Model-Compression Review`

情境化不等于自由发挥。推演越灵活，越需要反馈前冻结；叙事越漂亮，越不能拿叙事本身当证据。

## 十二、星门神奇仪宫的使用原则

星、门、神、奇仪、宫位、旺衰、生克、空墓刑迫、伏吟反吟、格局都先视为候选信息层，而非自动 verdict。

至少检查：当前问题域中它代表谁/什么、角色映射依据、结构/状态/来源象意/项目推演分类、是否重复包装同一底层结构、删掉后结论是否改变、什么结果会证明解释错。

九星、门、神固定“吉/凶”标签最多是传统 prior，不得直接输出犯罪、死亡、疾病等现实事实。

## 十三、书本案例与案例证据

案例必须先分类：

- `SOURCE_RETROSPECTIVE_CASE`
- `PROJECT_RETROSPECTIVE_REANALYSIS`
- `PROSPECTIVE_FROZEN_CASE`
- `CONTAMINATED_CASE`
- `IMPLEMENTATION_FAILURE_CASE`
- `UNSCORABLE_ANECDOTE`

只有满足 Prospective Registry、结果未知、反馈前冻结且可评分的 `PROSPECTIVE_FROZEN_CASE` 才可能贡献 Empirical Support。

无可审计分母、连续样本、失败记录、基线和污染控制的“约八成准确率”等统一标 `UNSUPPORTED_ACCURACY_CLAIM`。

## 十四、Prospective Case Registry

正式未知结果测试遵循 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`。

反馈后不得覆盖原 case 的冻结字段，包括 method/setup/time/deity/state/Role Map/features/patterns/branches/timing/auxiliary policy。任何改变必须创建新模型版本/`case_id`。污染案例保留。

## 十五、Outcome Audit

错误至少区分：

`INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR / METHOD_LAYER_ERROR / SETUP_METHOD_ERROR / SETUP_CALIBRATION_ERROR / TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE`

Outcome：`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`。

结果后只允许评分和模型更新，不允许重写原冻结版本。

## 十六、Rule Lifecycle + Model Compression

规则生命周期：

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

允许反向：

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`

现在协议字段、feature、branch 和 Gate 本身也进入相同的可删除逻辑。

每个新增模型变量原则上应写明未来的 removal/merge 条件，例如：长期不改变输出、不改善 discrimination/calibration、与另一字段高度耦合、负对照表明没有增量、或更简单模型在 prospective data 中表现相当/更好。

研究目标不是“约束越来越多”，而是在保证可复现与区分力的前提下逼近**最小充分模型**。

## 十七、Prediction Protocol Freeze != Theory Freeze

单次预测协议必须冻结；跨书、跨案例、跨版本理论必须保持可推翻。Method-Layer Gate、Baseline Firewall、Branch-Discrimination Gate、Ambiguity-Debt Gate、State-System Gate乃至整个流程，都可以在更强证据下被 `NARROW / REVISE / SPLIT / DEPRECATE / REJECT`。

## 十八、当前待验证问题

仍不是定论：

- Method-Family-Specific Priority 是否优于固定全局优先级；
- Method-Layer Gate 是否显著减少事后救援；
- setup/time-boundary/deity/state-system 分叉是否有稳定前瞻差异；
- 九星固定标签是否劣于条件化模型；
- 九星十二时辰应克是否优于基础概率与 shuffled controls；
- Role Map Freeze 是否改善可复现性；
- Branch-Discrimination 是否比“宽泛多分支”提高校准；
- Baseline Firewall 是否能减少辅助信息误归因；
- 哪些当前 context keys 可以通过 ablation 合并或删除。

## 十九、执行优先级

发生冲突时：

`K2 Evidence / Evidence Corrections / Book Distillate / Method Delta / Pre-Book Retrospective`
→ `CURRENT_METHOD_CONSTRAINTS.md`
→ `K2 Prospective Case / Source Fixture Protocols`
→ `当前版本理论草案`
→ `qclaw 技能与旧知识库`
→ `更早修炼日志`

这里的“优先”是项目运行约束优先级，不是玄学规则真值等级。
