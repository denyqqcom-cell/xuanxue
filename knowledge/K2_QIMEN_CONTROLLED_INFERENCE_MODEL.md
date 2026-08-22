# 奇门受控推演链 QCIC v0.1

版本：0.1  
状态：CANDIDATE_UNTESTED  
阶段：K2B / Deep Closure  
empirical_credit：NONE  
claim_extraction_blocked：true

## 1. 为什么需要这套模型

完整读完善天道 0027 / 0028 / 0029 后，项目暴露出三个互相连接的问题：

1. **角色过多**：精华讲义可以为不同问题列出大量“用神/参数”，如果全部开放给解释者，结果出来后几乎总能找到某个匹配角色；
2. **修正规则过多**：高级班大量使用空、墓、马星、旺衰、伏吟反吟等二阶修正，如果 trigger 与优先级不预先固定，容易形成 hindsight fitting；
3. **来源依赖被低估**：不同 PDF、不同 work_id 仍可能来自同一课程体系，文本重复不能当成多份独立验证。

因此项目不再把“会背更多规则”视为推演能力，而把重点转向：

> 在反馈出现之前，控制一个解释者到底被允许调用哪些角色、哪些规则、按什么顺序修正，以及什么结果算失败。

这套候选模型暂名：

**Qimen Controlled Inference Chain — QCIC / 奇门受控推演链**

它是项目自己的工程化理论框架，不是古籍原说，也不因“自创”而获得额外信用。

## 2. 八层推演链

### L0 Provenance Gate — 来源独立性

先确定：

`canonical source -> work identity -> course provenance -> voice/source dependence`

同课讲义只可增加 unique coverage；重复规则最多取得一个 provenance-family credit。

### L1 Question Topology — 问题拓扑

先定义：

- 问题域；
- 所问对象；
- 主体与客体；
- 是否存在第三方；
- 是否属于时间、位置、状态、关系或选择问题。

没有问题拓扑，不允许直接从整库调用用神。

### L2 Role Candidate Library — 角色候选库

0027 这类速查材料只提供候选角色集合。

例如：

`Question Domain -> Candidate Roles`

候选不等于激活。进入下一层前必须冻结本题允许参与的角色。

### L3 Eligible Rule Set Freeze — 合格规则集冻结

反馈前固定：

- 哪些角色有资格参与；
- 哪些门、星、神、干、宫与格局规则可调用；
- 哪些 competing school/model 同时运行；
- 哪些规则本题明确禁止调用。

数据库里“存在”不等于当前案例“有资格使用”。

### L4 Base Plate Annotation — 基础盘面标注

吸收0029较清晰的程序化步骤，但只作为 source-derived candidate workflow：

- 年/月/日/时及月令；
- 日空、时空；
- 六仪击刑；
- 入墓；
- 马星；
- 伏吟/反吟及其他预先允许的基础状态。

这一层只记录状态，不先为了结果决定吉凶。

### L5 Relational Inference — 关系推演

分成两个尺度：

- **Micro / 小局**：主要角色所在宫内部的门、星、神、奇仪、旺衰及组合；
- **Macro / 大局**：不同角色落宫之间的五行生克、主客与相互作用。

静态符号词典只提供局部特征；最终解释必须经过关系层。

### L6 Correction Rule Registry — 修正规则注册表

空、墓、马冲、旺衰、伏反吟等不再是随时可加的“解释补丁”。

每个 correction rule 必须预先拥有：

`trigger + scope + precedence + effect + incompatible_rules + failure_condition`

例如“马冲墓/空”如果未来进入测试，必须先定义：

- 什么马星；
- 冲哪一宫/哪一层；
- 什么情况下可削弱而不是完全取消；
- 与旺衰、空墓同时出现时谁优先；
- 哪些结果会判它失败。

### L7 Timing & Uncertainty — 应期与不确定性

应期本身在来源中就被承认为困难且有分歧，因此必须输出：

- 主要时间候选；
- competing timing model；
- 不确定范围；
- 不能判定时明确 UNKNOWN。

禁止只留下最终命中的一个数字而删除其他事前候选。

### L8 Prospective Validation — 前瞻验证

只有这一层可以提升 empirical credit。

反馈前冻结：

- role map；
- eligible rule set；
- correction registry；
- competing models；
- 预测结果；
- alternatives；
- falsification conditions。

结果回来后只允许评分，不允许重写预测路径。

## 3. Interpretation Degrees-of-Freedom Budget

QCIC 新增一个核心概念：

**解释自由度预算**。

一个案例可用角色越多、可切换模型越多、可叠加修正越多，就越容易在事后解释成功。

因此每次推演应记录至少：

- activated_roles_count；
- eligible_rules_count；
- correction_rules_count；
- competing_models_count；
- post_feedback_changes = 0（正式测试时必须为0）。

未来可以研究：在预测质量相同的情况下，是否应优先选择解释自由度更低的模型。

## 4. 三条当前候选假设

### QCIC-H1：角色冻结

如果问题域与 role candidate set 在反馈前冻结，跨解读者角色切换率应下降。

失败条件：冻结后复现率没有改善，或准确/校准明显恶化。

### QCIC-H2：修正注册

把“马冲墓/空”等规则从自由修正改成预注册 correction rule，应减少事后解释路径数量。

失败条件：自由度没有下降，或只有不断增加例外才能维持表现。

### QCIC-H3：低自由度优先

在 competing models 表现接近时，更低 interpretation degrees-of-freedom 的模型应具有更高的可复现性与更好的样本外稳定性。

失败条件：自由度与复现/样本外表现不存在稳定关系。

以上全部状态：`UNTESTED`。

## 5. 明确拒绝的旧习惯

QCIC 当前明确拒绝：

- 看到结果后换用神；
- 看到不利规则后临时用另一规则“解掉”；
- 同一课程三本讲义一致就算三票；
- 用作者案例数量代替预测准确率；
- 把 UNKNOWN 强行补成一个确定答案；
- 为了让盘看起来合理而静默修正文献错误；
- 医疗、法律、刑事、金融、战争、选举等高风险领域因来源丰富就自动开放操作。

## 6. 当前定位

QCIC v0.1 只是一个由完整阅读与项目自身错误反省长出来的**候选推演架构**。

它目前获得的是：

`method-structure credit = CANDIDATE`

而不是：

`empirical_credit = VALIDATED`

下一步只有通过预注册、可失败、反馈前冻结的案例测试，它才有资格继续进化。
