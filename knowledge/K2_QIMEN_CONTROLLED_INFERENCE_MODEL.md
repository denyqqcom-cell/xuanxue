# 奇门受控推演链 QCIC v0.2

版本：0.2  
状态：CANDIDATE_UNTESTED  
阶段：K2B / Deep Closure  
empirical_credit：NONE  
claim_extraction_blocked：true

## 0. v0.2 迭代来源

v0.1 由善天道 0027/0028/0029 的完整阅读形成，重点控制角色切换、修正规则与同课重复计票。

继续完整视觉阅读 QM-SRC-0015 后，项目发现另一个误区：**规则表密度本身就是解释自由度来源**。该 carrier 的第四章连续展开十干、八门、八卦、奇仪、格局等大量克应，随后第五章又把规则扩展到许多现实问题域；但来源自己同时强调人物、事情、环境不同应具体分析，并在后文提醒预测不能完全相信、只能参考。

因此 v0.2 新增：

- Post-Acceptance Lineage Correction；
- Rule Table Density Gate；
- Rule Search Entropy；
- candidate_rules_count -> eligible_rules_count 的压缩记录。

## 1. 核心目标

项目不再把“记住更多规则”视为推演能力，而把重点转向：

> 在反馈出现之前，控制解释者到底被允许调用哪些来源、角色、规则、修正项与竞争模型，并预先写清楚什么结果算失败。

QCIC 是项目自己的工程化候选框架，不是古籍原说，也不因“自创”获得额外信用。

## 2. 九层推演链

### L0 Provenance Gate — 来源独立性

先确定：

`canonical source -> raw lineage -> correction overlay -> effective work identity -> course provenance -> voice/source dependence`

文件名不是 work identity。完整视觉阅读若证明 carrier 只是篇/卷，必须允许反向纠正旧 lineage。

### L1 Question Topology — 问题拓扑

先定义问题域、对象、主体/客体/第三方，以及所问属于时间、位置、状态、关系还是选择问题。没有问题拓扑，不允许直接从整库调用用神。

### L2 Role Candidate Library — 角色候选库

速查材料只提供：

`Question Domain -> Candidate Roles`

候选不等于激活。反馈前冻结本题允许参与的角色。

### L3 Rule Table Density Gate — 规则表密度门

教材中出现的全部克应、格局、应象与应用条目先进入 candidate pool，而不是自动进入本题规则集。

必须记录：

- `candidate_rules_count`；
- `eligible_rules_count`；
- `rule_reduction_ratio`；
- `rule_selection_basis`。

规则表越密集，越需要更强的冻结；否则事后总能搜索到一个“看起来命中”的条目。

### L4 Eligible Rule Set Freeze — 合格规则集冻结

反馈前固定：

- 已激活角色；
- 可调用门、星、神、干、宫、格局与克应；
- competing school/model；
- 本题明确禁止调用的规则。

数据库里“存在”不等于当前案例“有资格使用”。

### L5 Base Plate Annotation — 基础盘面标注

只记录预先允许的基础状态，例如年/月/日/时、月令、空亡、击刑、入墓、马星、伏吟反吟等，不先为了结果决定吉凶。

### L6 Relational Inference — 关系推演

分两个尺度：

- Micro：主要角色所在宫内部的门、星、神、奇仪、旺衰及组合；
- Macro：不同角色落宫之间的五行生克、主客与相互作用。

静态表只提供局部特征；最终解释必须经过关系层。

### L7 Correction Rule Registry — 修正规则注册表

空、墓、马冲、旺衰、伏反吟等修正必须预先拥有：

`trigger + scope + precedence + effect + incompatible_rules + failure_condition`

修正规则不能在看到结果后临时充当解释补丁。

### L8 Timing & Uncertainty — 应期与不确定性

输出主要时间候选、竞争 timing model、不确定范围；不能判断时明确 UNKNOWN。禁止只留下最终命中的数字而删除其他事前候选。

### L9 Prospective Validation — 前瞻验证

只有这一层可以提升 empirical credit。反馈前冻结 role map、eligible rules、correction registry、competing models、预测、alternatives 与 falsification conditions；反馈后只评分，不重写路径。

## 3. Interpretation Degrees-of-Freedom Budget

每次推演至少记录：

- candidate_roles_count；
- activated_roles_count；
- candidate_rules_count；
- eligible_rules_count；
- correction_rules_count；
- competing_models_count；
- `post_feedback_changes = 0`（正式测试必须为0）。

新增 **Rule Search Entropy**：在反馈前可合法搜索的规则路径越多，事后解释成功的机会越高。未来应比较在预测质量相近时，低自由度模型是否更稳定。

## 4. 当前候选假设

### QCIC-H1 角色冻结

冻结问题域与 role candidate set 后，跨解读者角色切换率应下降。

失败：复现率不改善或校准明显恶化。

### QCIC-H2 修正注册

把“马冲墓/空”等从自由修正改为预注册 correction rule，应减少事后解释路径。

失败：自由度没有下降，或需要不断新增例外维持表现。

### QCIC-H3 低自由度优先

competing models 表现接近时，更低 interpretation degrees-of-freedom 的模型应具有更高复现性与样本外稳定性。

失败：自由度与复现/样本外表现不存在稳定关系。

### QCIC-H4 规则密度门

高规则密度来源若先把 candidate rules 压缩成冻结的 eligible set，应比开放式全表搜索具有更低 hindsight fit 和更高跨解读者一致性。

失败：冻结后自由度、复现或校准没有改善，或优势只能靠结果后重新放宽规则集获得。

以上全部：`UNTESTED`。

## 5. 明确拒绝的旧习惯

- 看到结果后换用神；
- 看到不利规则后临时换规则“解掉”；
- 把整本克应表默认全部开放给当前案例；
- 文件名像一本书就直接判为独立 work；
- 同一课程多本讲义一致就算多票；
- 用作者案例数量代替预测准确率；
- 把 UNKNOWN 强行补成确定答案；
- 为了让盘合理而静默修正文献；
- 医疗、法律、刑事、金融、战争、选举等高风险领域因资料多就自动开放操作。

## 6. 当前定位

QCIC v0.2 仍只是由完整阅读和项目自身错误反省逐步长出来的候选架构：

`method-structure credit = CANDIDATE`

不是：

`empirical_credit = VALIDATED`

只有经过预注册、可失败、反馈前冻结的案例测试，才允许继续升级。
