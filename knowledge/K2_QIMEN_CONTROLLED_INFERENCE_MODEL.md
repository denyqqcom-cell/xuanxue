# 奇门受控推演链 QCIC v0.5

版本：0.5  
状态：CANDIDATE_UNTESTED  
阶段：K2B / Deep Closure  
empirical_credit：NONE  
claim_extraction_blocked：true

## 0. v0.5 迭代来源

v0.1 由善天道 0027/0028/0029 的完整阅读形成，重点控制角色切换、修正规则与同课重复计票。

v0.2 由 QM-SRC-0015 完整阅读加入 Rule Table Density Gate、Rule Search Entropy 与 post-acceptance lineage correction。

v0.3 由 QM-SRC-0019 完整阅读加入 Reality Evidence Gate、Symbol Specificity Ceiling、Temporal Input Sensitivity 与 Self-Fulfilling Action Guard。

v0.4 由 QM-SRC-0020 完整阅读加入 Method Layer Router、Role Frame Registry 与 Cross-Layer Rule Leakage 约束。

继续完整视觉阅读 QM-SRC-0021《奇门遁甲预测学》285/285 页后，项目发现：**规则冻结仍然不足以冻结解释自由度**。

来源第五章明确允许“全盘看、外应看、特殊情况看”，并强调在一些情况下不能拘于常理；第六章虽然给出相对程序化的应期顺序，最后仍允许其他断法、外应与灵活机动；下编还保留了一个明确断错后再重新分析原盘的案例。

因此 v0.5 新增四项控制：

- Observation Channel Registry；
- Exception Override Budget；
- Retrospective Error Ledger；
- Procedure Precedence Graph。

## 1. 核心目标

QCIC 的控制对象不再只是“用了什么规则”，而是整个解释路径：

> 在结果出现之前，固定允许进入系统的信息通道、方法层、角色坐标、规则集合、规则执行顺序、修正与例外权限；在结果出现之后，保留原预测原貌，只允许追加评分和复盘，不允许逆向改写。

QCIC 是项目自己的工程化候选框架，不是古籍原说，也不因“自创”获得额外信用。

## 2. 十三层推演链

### L0 Provenance Gate — 来源独立性

先确定：

`canonical source -> raw lineage -> correction overlay -> effective work identity -> course provenance -> voice/source dependence`

文件名不是 work identity；传承/引录 voice 不自动算作者独立证据。

### L1 Reality Evidence Gate — 现实证据门

记录：

- `direct_evidence_available`；
- `direct_action_available`；
- `professional_method_available`；
- `why_symbolic_layer_is_still_needed`。

现实事实、调查、测量、诊断、法律程序、财务数据与安全流程优先。

### L2 Question Topology — 问题拓扑

冻结问题域、所问对象、主体/客体/第三方，以及所问属于时间、位置、状态、关系还是选择问题。

### L3 Observation Channel Registry — 观察输入通道注册

正式推演先声明哪些输入可以进入模型，例如：

- `PLATE_INTERNAL`：盘内结构；
- `QUERY_CONTEXT`：求测者在反馈前明确提供的上下文；
- `PRE_REGISTERED_EXTERNAL_OBSERVATION`：事先定义类别与时间窗的外部观察；
- `REALITY_EVIDENCE`：可核实现实资料。

默认禁止：

- 结果后才出现的信息；
- 未登记的“外应”；
- 看见结果后才被解释为有意义的环境细节；
- 无时间戳、无分类标准、不可复核的偶发输入。

记录：

`observation_channels + channel_event_taxonomy + observation_cutoff_time`

### L4 Method Layer Router — 方法层路由

每条候选规则先归入 method layer：

- `CALCULATION`；
- `DIVINATION`；
- `SELECTION_STRATEGY`；
- `MILITARY_OPERATIONAL`；
- `RITUAL_ESOTERIC`；
- `TRANSMITTED_REFERENCE`。

默认：

`cross_layer_rule_count = 0`

跨层桥接必须反馈前注册：

`from_layer + to_layer + bridge_rule + reason + failure_condition`

### L5 Role Frame Registry + Role Candidate Library — 角色坐标系与候选库

角色记录：

`role_label + role_frame_type + actor_mapping + directionality + plate_layer`

至少区分：

- `ACTOR_RELATION`；
- `INITIATIVE_DIRECTION`；
- `PLATE_LAYER`；
- `TASK_DOMAIN`。

之后再由：

`Question Domain -> Candidate Roles`

冻结本题可参与角色。

### L6 Rule Table Density Gate — 规则表密度门

记录：

- `candidate_rules_count`；
- `eligible_rules_count`；
- `rule_reduction_ratio`；
- `rule_selection_basis`。

规则存在于来源不等于当前案例有资格使用。

### L7 Eligible Rule Set Freeze — 合格规则集冻结

反馈前固定：

- 已激活 role frame 与角色；
- 可调用门、星、神、干、宫、格局与克应；
- competing school/model；
- 明确禁止的规则与方法层。

### L8 Procedure Precedence Graph — 程序优先级图

仅冻结规则集合仍不够；如果规则执行顺序可以结果后改变，同样可以制造解释自由度。

程序型方法需要登记：

`node + trigger + next_if_true + next_if_false + precedence + stop_condition`

例如应期候选可以把“事件分类 -> 伏反吟/内外盘 -> 空亡 -> 马星 -> 墓库/刑冲合 -> 生旺墓绝 -> 值使门/其他方法”作为一个待验证的 source-local precedence graph。

结果后不得重排优先级，除非原协议已注册分支条件。

### L9 Base Plate Annotation — 基础盘面标注

只记录预先允许的基础状态，例如年/月/日/时、月令、空亡、击刑、入墓、马星、伏吟反吟等，不先为了结果决定吉凶。

### L10 Relational Inference + Symbol Specificity Ceiling — 关系推演与具体化上限

Micro：主要角色所在宫内部的门、星、神、奇仪、旺衰及组合。

Macro：不同角色落宫之间的生克、主客与相互作用。

同时执行 `SYMBOL_SPECIFICITY_CEILING`：抽象符号默认只表达类别、关系与状态候选；没有独立现实证据或预注册关系规则时，不得直接跳到唯一具体人物、事件、病因、罪责或交易结论。

### L11 Correction Rule Registry + Exception Override Budget — 修正规则与例外预算

普通 correction rule 必须拥有：

`trigger + scope + precedence + effect + incompatible_rules + failure_condition`

“特殊情况”“不能拘于常理”不再是无限豁免权。任何 exception 必须在反馈前登记：

`exception_id + trigger + scope + effect + precedence + expiry + failure_condition`

并记录：

- `exception_override_count`；
- `max_exception_overrides`。

结果后新增的特殊情况一律计入 `post_feedback_changes`。

### L12 Timing & Temporal Input Sensitivity — 应期与时间输入敏感性

记录：

- `temporal_granularity`；
- `calendar_model`；
- `boundary_policy`；
- `competing_temporal_models_count`；
- `active_timing_precedence_graph`。

合法竞争时间模型全部保留；禁止结果后只留下命中的模型或重新排列规则优先级。

### L13 Prospective Validation + Intervention Guard + Retrospective Error Ledger — 前瞻验证、干预与失败账本

只有这一层可以提升 empirical credit。

反馈前冻结 observation channels、role map、role frame、method layer、eligible rules、procedure graph、correction/exception registry、competing models、预测、alternatives 与 falsification conditions。

若预测改变了当事人行为，记录：

`intervention_after_prediction = true`

该样本不得当作纯自然结果的独立命中证据。

所有案例都必须保留：

- `original_prediction`；
- `original_rule_path`；
- `original_alternatives`；
- `outcome`；
- `original_score`；
- `posthoc_reanalysis`；
- `posthoc_changes_count`。

事后重析只能生成下一轮 hypothesis，不允许覆盖 original prediction，也不允许反向提升原案例分数。

## 3. Interpretation Degrees-of-Freedom Budget

每次推演至少记录：

- observation_channel_count；
- unregistered_observation_count；
- candidate_roles_count；
- activated_roles_count；
- role_frame_count；
- active_role_frame；
- active_method_layers；
- cross_layer_rule_count；
- candidate_rules_count；
- eligible_rules_count；
- procedure_nodes_count；
- procedure_branch_count；
- correction_rules_count；
- exception_override_count；
- max_exception_overrides；
- competing_models_count；
- competing_temporal_models_count；
- symbol_specificity_level；
- direct_evidence_available；
- direct_action_available；
- intervention_after_prediction；
- posthoc_changes_count；
- `post_feedback_changes = 0`（正式测试必须为0）。

**Rule Search Entropy**：可搜索规则路径越多，事后解释机会越高。

**Observation Search Entropy**：可随时新增的输入通道越多，越容易把随机环境细节转成命中解释。

**Precedence Search Entropy**：同一套规则若能自由改变执行顺序，也会产生大量事后路径。

**Reality Override Principle**：现实证据足够时，不因术数叙事更完整而覆盖事实。

**Method-Layer Isolation Principle**：文本共存不等于方法同层；跨层调用是例外，不是默认。

**Failure Preservation Principle**：错误样本不得通过事后重析被洗成成功样本。

## 4. 当前候选假设

### QCIC-H1 角色冻结

冻结问题域与 role candidate set 后，跨解读者角色切换率应下降。

### QCIC-H2 修正注册

预注册 correction rule 应减少事后解释路径。

### QCIC-H3 低自由度优先

competing models 表现接近时，更低 interpretation degrees-of-freedom 的模型应具有更高复现性与样本外稳定性。

### QCIC-H4 规则密度门

高规则密度来源先压缩成冻结 eligible set，应比开放式全表搜索具有更低 hindsight fit 和更高一致性。

### QCIC-H5 现实证据门

已有可核实资料或可直接行动时先执行 Reality Evidence Gate，应减少现实冲突与无必要术数介入。

### QCIC-H6 符号具体化上限

限制抽象符号只输出类别/关系候选，应降低从单一符号直接断唯一具体事实的假确定性。

### QCIC-H7 时间输入敏感性

预先保留多个合法时间模型并记录敏感性，应减少结果后挑选最有利时间模型。

### QCIC-H8 方法层路由

先固定 method layer 再选规则，应降低占验、策略、军事与仪式规则的跨层污染。

### QCIC-H9 角色坐标系注册

显式记录 role frame 应比只记录“主/客”等标签提高跨解读者一致性。

### QCIC-H10 观察通道注册

预注册 observation channels 与外部观察分类，应减少“外应”及偶发信息带来的结果后解释路径。

失败：未登记输入、结果后引入环境细节或跨解读者分歧没有下降。

### QCIC-H11 例外预算

给“特殊情况”设置预注册 trigger 和 override budget，应减少无限例外对规则冻结的绕过。

失败：例外数量、后验修正或 hindsight fit 没有下降，或模型必须不断增加例外才能维持表现。

### QCIC-H12 失败样本不可洗白

把 original prediction 与 posthoc reanalysis 永久分离，应使准确率、校准与错误模式更真实地暴露。

失败：分离后审计质量没有改善，或事后重析在未知结果条件下可稳定复现原修正路径。

### QCIC-H13 程序优先级冻结

对于应期等程序型规则，冻结 precedence graph 应比开放式多规则搜索具有更高复现性。

失败：顺序冻结不能降低时间模型切换和结果后命中，或只有重新开放优先级才能维持表现。

以上全部：`UNTESTED`。

## 5. 明确拒绝的旧习惯

- 已有现实证据却让术数覆盖事实；
- 可以直接调查、测量、行动，却用预测替代现实处理；
- 因为规则都出自“奇门”就把占验、军事、仪式、择用混成同一规则池；
- 只记录“主/客”而不记录其 role frame；
- 冻结规则后仍允许任意新增“外应”；
- 看到结果后把偶发环境细节解释成关键输入；
- 用“特殊情况”无限绕过正常判断顺序；
- 同一套应期规则结果后重新排列优先级；
- 断错后用结果重析原盘，再把新解释当成原预测命中；
- 看到结果后换用神、换 frame 或跨 method layer 找补；
- 把整本克应表默认全部开放给当前案例；
- 从抽象卦象直接跳到唯一具体事实；
- 事后只保留最像结果的时间模型；
- 预测改变行为后仍把后果算作纯预测命中；
- 文件名像一本书就直接判作者、版本或独立 work；
- 传承引录被同一作者收编后就重新算独立证据；
- 同一课程多本讲义一致就算多票；
- 用作者案例数量代替预测准确率；
- 把 UNKNOWN 强行补成确定答案；
- 为了让盘合理而静默修正文献；
- 高风险领域因资料多就自动开放操作。

## 6. 当前定位

QCIC v0.5 仍只是由完整阅读、失败样本和项目自身错误反省逐步长出的候选架构：

`method-structure credit = CANDIDATE`

不是：

`empirical_credit = VALIDATED`

下一步真正能提升信用的，不是再增加规则，而是把 observation channels、procedure precedence、exception budget 和 failure ledger 放进预注册前瞻测试。
