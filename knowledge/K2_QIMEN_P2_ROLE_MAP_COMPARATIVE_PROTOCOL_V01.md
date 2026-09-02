# K2 Qimen P2 Role-Map Comparative Protocol v0.1

状态：`DESIGN_READY / UNTESTED / NO_BATCH / NO_FREEZE / NO_OUTCOME`

Hypothesis：`QRM-H1`
Plan：`K2PV-QRM-001`
Empirical Credit：`NONE`
Claim Extraction：`BLOCKED`

## 0. 研究问题

本协议只回答一个被现有 H-JD-001 留空的问题：在同一问题、同一现实事实、同一 Scenario Graph、同一 Engine/plate、同一 source role catalog、同一 eligible rule pool 与同一 Outcome 定义下，**问题拓扑驱动、且在读取当前盘面具体符号值之前冻结的 Role Map / Layer Priority**，是否比忠实保留来源角色目录并使用固定全局信息层优先级的 baseline 更稳定、更可复现、更可校准。

这不是对“场景化推演”理念的确认。若 candidate 不胜，必须接受增加 question-topology 自由度可能只是增加解释空间而非信息增量。

## 1. 来源边界：为什么不能造一个弱 baseline

### QM-SRC-0003

- `K2E-W1-QM-0003-0065 @ pdf:p37`：来源明确给出固定全局判断顺序：`奇仪 -> 八门 -> 八神 -> 九星`。
- 但同一来源并非“完全无场景角色”。例如 `K2E-W1-QM-0003-0009` 已按单位问题设置上级/同级/下级角色，`K2E-W1-QM-0003-0063` 的失物用神会随物品类别变化，`K2E-W1-QM-0003-0068` 又要求单位风水抓主要环境、领导与财务负责人等重点。

因此 comparator 必须保留这些已经存在的 domain-specific role catalog；禁止把它降格成“任何问题永远只看同一个用神”的稻草人。

### QM-SRC-0016

`K2D-W1-QM-SRC-0016` 明确把问题分成静态、动态、九宫拟象、综合等方法族，并要求不同问题子场景重建角色，同时也暴露反馈后换用神、换起局、误局继续解释、外应和跨术数确认等自由度风险。该来源给的是 **candidate-method support**，不是现实有效性信用。

### QM-SRC-0021

`K2DS-QM-SRC-0021` 与其 Evidence 显示问题域/asked object 会改变主要用神或观察层，例如 `K2E-W1-QM-0021-0239` 的工作角色表、`-0327` 的父母多种取法、`-0330` 的工作社会角色层级。来源同时允许多观察通道、外应、特殊情况与事后重析，因此这些材料只能支持“存在 topology-conditioned candidate”，不能证明 candidate 更准。

## 2. 核心识别：把两个自由度拆开

简单 A/B 会把两个变化绑在一起：

1. Role Binding 是否由 question topology 决定；
2. Layer Priority 是否由 question topology 决定。

因此必须使用三条 lane。

### Lane A — `GLOBAL_PRIORITY_CATALOG_ROLE_BASELINE_V01`

- 角色只能从反馈前冻结的 `source_role_catalog` 选取；
- catalog 必须忠实保留 QM-SRC-0003 等来源已经存在的 domain-specific 角色，不得删除以制造弱 baseline；
- 信息层优先级固定为：`奇仪 -> 八门 -> 八神 -> 九星`；
- 角色选择只能使用 question domain / asked object 与 observation-cutoff 前现实事实；不得读取 current plate values 来挑角色。

### Lane A' — `GLOBAL_PRIORITY_TOPOLOGY_ROLE_ABLATION_V01`

- 允许根据 Reality Anchor、Scenario Graph、question topology 绑定 world variable -> symbolic role；
- 仍固定 `奇仪 -> 八门 -> 八神 -> 九星`；
- 这是强制 bridge ablation，用来单独识别 topology role binding 的增量。

### Lane B — `TOPOLOGY_CONDITIONED_ROLE_PRIORITY_V01`

- Role Map 由 question topology 生成；
- primary/secondary layer priority 也由 question topology 生成；
- 两者都必须在 current plate symbol values、strength/auspiciousness、prediction 与 Outcome 可见之前冻结。

## 3. Attribution Contrasts

必须分别计分，不得用 combined win 偷换组件信用：

- `P2-C1 = A' - A`：只允许归因给 **topology role binding**。
- `P2-C2 = B - A'`：只允许归因给 **topology-conditioned layer priority**。
- `P2-C3 = B - A`：只表示 **full bundle** 的联合增量，不能单独证明 Role Map 或 Layer Priority。

即使 P2-C3 显著为正，只要 P2-C1 不支持 role-binding 增量，就不得宣称“场景化用神已验证”。

## 4. Mapping Input Boundary

三条 lane 在映射阶段只允许读取：

- question definition / asked object；
- observation-cutoff 前 Reality Anchor；
- Scenario Graph / object graph / state variables；
- setup_method / school_context / time_family / layout_method；
- source_role_catalog 与预注册 eligible rule pool；
- outcome definition（只能定义评分目标，不得包含结果值）。

映射阶段明确禁止：

- current plate symbol values；
- 当前盘旺衰、吉凶、格局强弱；
- 已生成 prediction；
- Outcome / feedback；
- 未注册外应或事后新增现实信息。

执行顺序必须为：

`Question + Reality -> Scenario Graph -> three Role/Layer Maps FREEZE -> current plate value access -> same rule pool -> three predictions -> future Outcome`

`mapping_before_plate_value_access=true`

`plate_value_access_before_mapping=false`

如果不能机器或审计记录这一顺序，该 case 为污染或 `UNEVALUABLE`。

## 5. Shared Controls

三条 lane 必须共享：

- question definition / asked object；
- Reality Anchor / Scenario Graph / observation cutoff；
- Engine commit、plate identity、setup/method context；
- source role catalog；
- eligible rule pool；
- Outcome definition / scoring rule；
- prediction cutoff；
- paired abstention policy。

除 attribution 所规定的 Role Binding / Layer Priority 差异外，不得给某条 lane 单独增加规则、外应、第二套盘或额外现实信息。

## 6. Competing Mappings 与 Abstention

如果一个关键 world variable 存在多个来源允许的 mapping，且事前规则无法唯一选择：

- 并行冻结 competing mappings；或
- `ABSTAIN / UNEVALUABLE`。

结果出来后选中命中的 mapping，计为 contamination，不重算原 prediction。

## 7. Future Batch 必须再冻结的对象

本 v0.1 只是 protocol，不是 Batch preregistration。未来任何 Batch 在第一条 case 之前仍必须原子冻结：

- source_role_catalog 的确切版本/hash；
- comparator / bridge / candidate mapping generator；
- topology features 与允许输入 manifest；
- global 与 topology-conditioned layer-priority policy；
- interpreter protocol 与跨解读者分配；
- primary metric / calibration metric / selective-risk metric；
- decision threshold；
- sampling / stopping rule；
- minimum information floor；
- contamination ledger 与 exclusion policy。

当前：`BATCH=NONE / FREEZE=NONE / OUTCOME=NONE`。

## 8. 评价指标

预注册 Batch 至少记录：

- P2-C1 / P2-C2 / P2-C3 paired primary metric delta；
- calibration 或 discrimination delta；
- abstention / selective-risk delta；
- cross-interpreter Role Map reproducibility；
- cross-interpreter prediction reproducibility；
- pre-outcome mapping instability rate；
- post-feedback role-switch attempt rate；
- post-feedback rule/layer-priority edit rate。

跨解读者一致性只能用于测可复现性，不能用多数票事后选赢的 mapping。

## 9. 成功、失败与信用边界

`QRM-H1` 只有在未知 Outcome 的未来 Batch 中，按事前冻结的统计与停止规则达到门槛，且无 post-feedback repair，才可进入 Batch Review。

失败条件包括：

- candidate 对 comparator 无稳定增量；
- 增量只在看过 current plate values 后改 mapping 才出现；
- 增量只在 Outcome 后换 Role Map / Layer Priority / Rule / Interpretation Path 才出现；
- 跨解读者无法按同一输入重建 mapping；
- P2-C3 胜出但 P2-C1/P2-C2 无法分离对应组件增量。

任何失败、弃权、不可判定和 repair attempt 都必须保留。

## 10. 高风险边界

`RESEARCH_ONLY`。只允许低风险、未来结果可客观核验的研究案例。医疗、法律、金融、人身安全、重大关系、犯罪归责等问题不得进入现实行动建议或经验晋级样本。

## 11. 当前状态

```text
PROTOCOL = DESIGN_READY
QRM-H1 = UNTESTED
BATCH = NONE
FREEZE = NONE
OUTCOME = NONE
EMPIRICAL_CREDIT = NONE
CLAIM_EXTRACTION = BLOCKED
```

CI / validator 通过只表示合同结构可审计，不表示任何 lane 获得现实预测信用。
