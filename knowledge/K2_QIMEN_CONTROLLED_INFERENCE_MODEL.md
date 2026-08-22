# 奇门受控推演链 QCIC v0.4

版本：0.4  
状态：CANDIDATE_UNTESTED  
阶段：K2B / Deep Closure  
empirical_credit：NONE  
claim_extraction_blocked：true

## 0. v0.4 迭代来源

v0.1 由善天道 0027/0028/0029 的完整阅读形成，重点控制角色切换、修正规则与同课重复计票。

v0.2 由 QM-SRC-0015 完整阅读加入 Rule Table Density Gate、Rule Search Entropy 与 post-acceptance lineage correction。

v0.3 由 QM-SRC-0019《奇门遁甲白话精解》完整阅读加入 Reality Evidence Gate、Symbol Specificity Ceiling、Temporal Input Sensitivity 与 Self-Fulfilling Action Guard。

继续完整视觉阅读 QM-SRC-0020 canonical carrier 125/125 页后，项目发现两个仍未被充分控制的问题：

1. **Method Layer Leakage**：同一本奇门资料可以同时包含排盘、占验、择用、军事、仪式、神煞和传承材料；“来自同一本书”不等于“属于同一种方法”。
2. **Role Frame Collision**：同一个“主/客”标签可以指现实行动主体、主动/被动方向、天地盘层关系等不同坐标系；只冻结角色名仍可能冻结错的 frame。

因此 v0.4 新增：

- Method Layer Router；
- Role Frame Registry；
- Cross-Layer Rule Leakage 约束。

## 1. 核心目标

QCIC 的目标继续收紧：

> 先让现实证据拥有优先权，再确认当前问题属于哪一种方法层与角色坐标系；只有在此之后，规则才有资格被筛选、冻结和推演。

QCIC 是项目自己的工程化候选框架，不是古籍原说，也不因“自创”获得额外信用。

## 2. 十二层推演链

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

### L3 Method Layer Router — 方法层路由

每条候选规则先归入 method layer：

- `CALCULATION`：排盘、定局、盘层算法；
- `DIVINATION`：占验与关系判断；
- `SELECTION_STRATEGY`：择时、择方、行动策略；
- `MILITARY_OPERATIONAL`：用兵、行军、阵势等；
- `RITUAL_ESOTERIC`：布斗、仪式、神煞操作等；
- `TRANSMITTED_REFERENCE`：前贤、引录、汇编传统材料。

当前问题只允许预先授权的方法层进入后续流程。

默认：

`cross_layer_rule_count = 0`

任何跨层桥接必须在反馈前注册：

`from_layer + to_layer + bridge_rule + reason + failure_condition`

### L4 Role Frame Registry + Role Candidate Library — 角色坐标系与候选库

角色记录不再只有一个 label，而是：

`role_label + role_frame_type + actor_mapping + directionality + plate_layer`

至少允许区分：

- `ACTOR_RELATION`；
- `INITIATIVE_DIRECTION`；
- `PLATE_LAYER`；
- `TASK_DOMAIN`。

同名“主/客”“我/他”不因字面相同自动合并。

之后再从：

`Question Domain -> Candidate Roles`

冻结本题可参与角色。

### L5 Rule Table Density Gate — 规则表密度门

记录：

- `candidate_rules_count`；
- `eligible_rules_count`；
- `rule_reduction_ratio`；
- `rule_selection_basis`。

规则存在于来源不等于本题有资格调用。

### L6 Eligible Rule Set Freeze — 合格规则集冻结

反馈前固定：

- 已激活 role frame 与角色；
- 可调用门、星、神、干、宫、格局与克应；
- competing school/model；
- 明确禁止的规则与方法层。

### L7 Base Plate Annotation — 基础盘面标注

只记录预先允许的基础状态，例如年/月/日/时、月令、空亡、击刑、入墓、马星、伏吟反吟等，不先为了结果决定吉凶。

### L8 Relational Inference + Symbol Specificity Ceiling — 关系推演与具体化上限

Micro：主要角色所在宫内部的门、星、神、奇仪、旺衰及组合。

Macro：不同角色落宫之间的生克、主客与相互作用。

同时执行 `SYMBOL_SPECIFICITY_CEILING`：抽象符号默认只表达类别、关系与状态候选；没有独立现实证据或预注册关系规则时，不得直接跳到唯一具体人物、事件、病因、罪责或交易结论。

### L9 Correction Rule Registry — 修正规则注册表

空、墓、马冲、旺衰、伏反吟等修正必须预先拥有：

`trigger + scope + precedence + effect + incompatible_rules + failure_condition`

### L10 Timing & Temporal Input Sensitivity — 应期与时间输入敏感性

记录：

- `temporal_granularity`；
- `calendar_model`；
- `boundary_policy`；
- `competing_temporal_models_count`。

合法竞争时间模型全部保留；禁止结果后只留下命中的模型。

### L11 Prospective Validation + Intervention Guard — 前瞻验证与干预标记

只有这一层可以提升 empirical credit。

反馈前冻结 role map、role frame、method layer、eligible rules、correction registry、competing models、预测、alternatives 与 falsification conditions。

若预测改变了当事人行为，记录 `intervention_after_prediction=true`，该样本不得当作纯自然结果的独立命中证据。

## 3. Interpretation Degrees-of-Freedom Budget

每次推演至少记录：

- candidate_roles_count；
- activated_roles_count；
- role_frame_count；
- active_role_frame；
- active_method_layers；
- cross_layer_rule_count；
- candidate_rules_count；
- eligible_rules_count；
- correction_rules_count；
- competing_models_count；
- competing_temporal_models_count；
- symbol_specificity_level；
- direct_evidence_available；
- direct_action_available；
- intervention_after_prediction；
- `post_feedback_changes = 0`（正式测试必须为0）。

**Rule Search Entropy**：可搜索规则路径越多，事后解释机会越高。

**Reality Override Principle**：现实证据足够时，不因术数叙事更完整而覆盖事实。

**Method-Layer Isolation Principle**：文本共存不等于方法同层；跨层调用是例外，不是默认。

## 4. 当前候选假设

### QCIC-H1 角色冻结

冻结问题域与 role candidate set 后，跨解读者角色切换率应下降。

失败：复现率不改善或校准明显恶化。

### QCIC-H2 修正注册

把“马冲墓/空”等自由修正改为预注册 correction rule，应减少事后解释路径。

失败：自由度没有下降，或需要不断新增例外维持表现。

### QCIC-H3 低自由度优先

competing models 表现接近时，更低 interpretation degrees-of-freedom 的模型应具有更高复现性与样本外稳定性。

失败：自由度与复现/样本外表现不存在稳定关系。

### QCIC-H4 规则密度门

高规则密度来源先压缩成冻结 eligible set，应比开放式全表搜索具有更低 hindsight fit 和更高一致性。

失败：冻结后自由度、复现或校准没有改善。

### QCIC-H5 现实证据门

已有可核实资料或可直接行动时先执行 Reality Evidence Gate，应减少现实冲突与无必要术数介入。

失败：错误确定性与现实冲突没有下降，或任务质量显著恶化。

### QCIC-H6 符号具体化上限

限制抽象符号只输出类别/关系候选，应降低从单一符号直接断唯一具体事实的假确定性。

失败：校准、复现和错误具体化率均无改善。

### QCIC-H7 时间输入敏感性

预先保留多个合法时间模型并记录敏感性，应减少结果后挑选最有利时间模型。

失败：无法降低模型切换率，也无法识别稳定性差异。

### QCIC-H8 方法层路由

先固定 method layer 再选规则，应降低占验、策略、军事与仪式规则的跨层污染。

失败：cross-layer leakage 与事后规则切换没有下降，或只能靠重新开放跨层搜索维持表现。

### QCIC-H9 角色坐标系注册

显式记录 role frame 应比只记录“主/客”等标签提高跨解读者一致性。

失败：角色冲突、frame 切换与输出分歧均无改善。

以上全部：`UNTESTED`。

## 5. 明确拒绝的旧习惯

- 已有现实证据却让术数覆盖事实；
- 可以直接调查、测量、行动，却用预测替代现实处理；
- 因为规则都出自“奇门”就把占验、军事、仪式、择用混成同一规则池；
- 只记录“主/客”而不记录其 role frame；
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

QCIC v0.4 仍只是由完整阅读和项目自身错误反省逐步长出的候选架构：

`method-structure credit = CANDIDATE`

不是：

`empirical_credit = VALIDATED`

只有经过预注册、可失败、反馈前冻结，并显式记录现实证据、method layer、role frame 与干预的测试，才允许继续升级。
