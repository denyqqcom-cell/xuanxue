# 奇门当前方法约束层（2026-08-21）

状态：**ACTIVE / AUTHORITATIVE OVERLAY / v2.3**

适用范围：后续奇门学习、解盘、技能调用、案例复盘与前瞻验证。本文件约束旧版《奇门遁甲知识库》及尚未完全迁移的 `qclaw` 内容。

> 这不是新的“圣经”。它是一组当前有效、可被反例修改、缩窄或废弃的认识论与执行约束。

## 一、认识论分层

每个关键判断必须区分：

- **SOURCE**：某书、某门派、某作者明确提出的规则或案例；
- **INFERENCE**：项目基于当前问题作出的情境转译、关系推演或抽象；
- **EMPIRICAL_SUPPORT**：结果未知时已冻结、结果后可核验的独立支持；
- **CONTAMINATION**：新闻、既知结果、求测者背景、外应、其他术数、搜索资料等可能帮助答案但妨碍归因的信息。

`Source Fidelity != Lookup Determinism != Empirical Support`。

书证再多，只能提高 Source Fidelity；fixture、回归测试或 runtime contract 通过，只说明来源复刻/执行约束更可靠，不代表预测现实有效。

## 二、已撤销的全局硬规则

以下旧规则不得再直接运行：

- 固定 `开门 > 值符 > 生门 > 星神`；
- `逢空 = 方向待定` 或其他单一固定翻译；
- `凶格>=3分直接大凶`、凶格相乘；
- `旺相=全额 / 休囚=减半 / 四害自动折扣`；
- `>=3次独立案例 = 已验证`；
- 强制先查若干新闻再把结论归因于奇门本体。

这些旧规则若仍有研究价值，只能作为 `CANDIDATE / UNVERIFIED_HEURISTIC`，必须另行预注册测试。

## 三、Method-Layer Gate

新案例先冻结主方法层：

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

一个方法层的 miss 不得由另一个层结果后救援。需要比较时，反馈前并行建立独立 A/B case。`RITUAL_AUXILIARY` 默认 `eligible_for_scoring=false`。

## 四、Setup / Time / Layout / Deity Gate

起局不是一个“局数”字段，而是一组会改变结构结果的模型选择。至少显式记录：

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

若某变量对模型必要但未解决，必须停在 `CONTEXT_REQUIRED`；不使用时写 `NOT_APPLICABLE`。可评分的 `FROZEN / RESOLVED` 模型不得把必要字段留为 `CONTEXT_REQUIRED`。

### 4.1 Setup Method Gate

旧 `qimen-qiju` 已发现：

- 超神/接气在同一 legacy 文件前后存在方向反转；
- 拆补存在“固定5+5+5”和“残元+补元”两种描述；
- 拆补/茅山定义高度重叠；
- 宫号顺序与顺/逆时针旋转语言混用。

因此不得默认某一 setup “天然正确”。若不同算法产生不同盘，必须绑定 source/version 或反馈前做平行 A/B。

### 4.2 Time-Boundary Gate

日界/子时规则是模型变量。旧资料曾同时出现“20点~23点为晚子时”和“23-24点算次日”等冲突记录。当前只允许显式绑定 `time_boundary_system`；结果后切换日界不能修补原预测。

### 4.3 Deity-System Gate

梁书勾陈/朱雀体系与现代常见白虎/玄武体系平行保存：

- 不静默改名；
- 不互借象意；
- 不假设天然同义；
- 比较时反馈前独立冻结。

## 五、State-System Gate

正式模型新增：

```text
star_state_system
door_state_system
```

旧 `qimen-gongpan` 同一文件对天蓬状态曾出现 `旺亥子/相寅卯` 与 `旺寅卯/相亥子` 两套相反示例。使用九星/八门旺相休囚时必须绑定明确 source/method system；不使用写 `NOT_APPLICABLE`；竞争系统必须 A/B 预注册；结果后切换 state system 不能修补原 score。

这只是反后见约束，不表示任何一套旺衰算法已被证明正确。

## 六、受约束情境推演流程

当前运行链：

`Reality Baseline`
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
→ `Timing Freeze`
→ `Frozen Prediction`
→ `Prospective Registry`
→ `Optional Auxiliary Context Ablation`
→ `Outcome Audit`
→ `Rule Lifecycle Update`

情境化不等于自由发挥。推演越灵活，越需要反馈前冻结；叙事越漂亮，越不能拿叙事本身当证据。

## 七、Role Map / Component / Pattern

Role Map 必须标明角色来源：

- `SOURCE_DEFINED`
- `METHOD_DEFINED`
- `CONTEXT_INFERRED`

多个合理用神反馈前保存竞争 Role Map；结果后换用神只能算模型修改。

`qimen-gongpan` 当前至少区分：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

`qimen-gexia` 当前至少区分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

同一底层结构不得因多个格名重复计票。来源内部冲突保留为 `SOURCE_INCONSISTENCY / CONFLICT_CANDIDATE`，不能结果后选最贴合的一条。

## 八、星门神奇仪宫的使用原则

星、门、神、奇仪、宫位、旺衰、生克、空墓刑迫、伏吟反吟、格局都先视为候选信息层，而非自动 verdict。

至少检查：

1. 当前问题域中它代表谁或什么；
2. 角色映射依据；
3. 它是结构、状态、来源象意还是项目推演；
4. 是否与其他信号重复包装同一底层结构；
5. 若移除该特征，结论是否改变；
6. 什么结果会证明当前解释错了。

九星、门、神固定“吉/凶”标签最多是传统 prior，不得直接输出犯罪、死亡、疾病等现实事实。

## 九、书本案例与案例证据

书本案例主要用于：

- 重建作者实际如何选信息；
- 找适用边界；
- 暴露方法自由度；
- 生成待检验假设；
- 发现失败模式、内部矛盾和实现漂移。

案例必须先分类：

- `SOURCE_RETROSPECTIVE_CASE`
- `PROJECT_RETROSPECTIVE_REANALYSIS`
- `PROSPECTIVE_FROZEN_CASE`
- `CONTAMINATED_CASE`
- `IMPLEMENTATION_FAILURE_CASE`
- `UNSCORABLE_ANECDOTE`

只有满足 Prospective Registry、结果未知、反馈前冻结且可评分的 `PROSPECTIVE_FROZEN_CASE` 才可能贡献 Empirical Support。书本复盘吻合、直断条目、多位作者声称“实践验证”都不能替代这一条件。

任何“约八成准确率”等总体准确率数字，如果没有可审计分母、连续样本、失败记录、基线和污染控制，统一标 `UNSUPPORTED_ACCURACY_CLAIM`，不得进入运行层。

## 十、Reality Baseline / Auxiliary / 高风险边界

Reality Baseline 用于确认对象、时间、地点、事件定义、已知/未知与基础概率。新闻、背景、外应、其他术数若加入，必须走：

`method-only -> freeze -> context-augmented -> record delta`

外部信息带来的改善不得倒算给奇门本体。

传统人体、疾病、犯罪、牢狱、死亡、灾害等类象属于 `HIGH_RISK_SOURCE_SYMBOLISM`，不能替代医学、法律、金融或事实调查。

## 十一、Prospective Case Registry

正式未知结果测试遵循：

`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`

并登记：

`knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

反馈后不得覆盖原 case 的冻结字段，包括：

- method layer / family；
- setup method / calibration / seasonal alignment；
- `time_boundary_system` / time family / layout；
- deity system；
- `star_state_system / door_state_system`；
- Role Map；
- eligible features / patterns；
- competing branches / timing protocol；
- auxiliary policy。

任何改变必须创建新模型版本/`case_id`。污染案例保留，不能为了提高命中率删除。

## 十二、Outcome Audit

错误至少区分：

`INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR / METHOD_LAYER_ERROR / SETUP_METHOD_ERROR / SETUP_CALIBRATION_ERROR / TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE`

Outcome：

`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`

结果后只允许评分和模型更新，不允许重写原冻结版本。

## 十三、规则生命周期

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

允许反向：

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`

“渐进迭代”不是旧规则只加不删，而是修改有版本、删除有证据、边界有记录。

## 十四、Prediction Protocol Freeze != Theory Freeze

单次预测协议必须冻结；跨书、跨案例、跨版本理论必须保持可推翻。Method-Layer Gate、Setup/Time-Boundary Gate、State-System Gate、四层认识论乃至整个流程本身，都可以在更强证据下被 `NARROW / REVISE / SPLIT / DEPRECATE / REJECT`。

## 十五、当前待验证问题

仍不是定论：

- Method-Family-Specific Priority 是否优于固定全局优先级；
- Method-Layer Gate 是否显著减少事后救援；
- 拆补/置闰/茅山、平气/定气、正授/超神/置闰/接气是否有稳定前瞻差异；
- 不同 `time_boundary_system` 是否产生可重复差异；
- 勾陈朱雀 vs 白虎玄武是否有可重复增量；
- 不同 star/door state systems 是否产生稳定区分；
- 九星固定标签是否劣于条件化模型；
- 九星十二时辰应克是否优于基础概率与 shuffled controls；
- Role Map Freeze、多分支预注册、辅助信息消融是否改善可复现性和校准。

## 十六、执行优先级

发生冲突时：

`K2 Evidence / Book Distillate / Method Delta / Pre-Book Retrospective`
→ `CURRENT_METHOD_CONSTRAINTS.md`
→ `K2 Prospective Case / Source Fixture Protocols`
→ `当前版本理论草案`
→ `qclaw 技能与旧知识库`
→ `更早修炼日志`

这里的“优先”是项目运行约束优先级，不是玄学规则真值等级。
