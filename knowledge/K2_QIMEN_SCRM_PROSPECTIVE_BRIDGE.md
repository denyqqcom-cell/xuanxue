# K2 SCRM-v0.2 Prospective Bridge

状态：`DESIGN_READY`  
框架：`SCRM-v0.2 / CANDIDATE_UNTESTED`  
Claim Extraction：`BLOCKED`  
Empirical Credit：`NONE`

## 1. 目的

本桥接层把 SCRM-v0.2 的 H6-H9 从理论文档中的候选假设，接入既有：

`HYPOTHESIS -> TEST PLAN -> BATCH PREREGISTRATION -> CASE FREEZE -> OUTCOME -> BATCH REVIEW`

链路。

桥接完成只表示“已经可以被严格测试”，不表示理论已被验证。

## 2. 假设来源不再假定只能来自 work family

旧 prospective validator 默认所有 hypothesis 都来自 `K2_WORK_FAMILY_DISTILLATES.jsonl`，因此 plan 使用 `work_family_key` 绑定来源。

这对文献衍生假设成立，但对项目自建框架不成立。若为了兼容字段而把 SCRM 伪装成一个 work family，会污染 provenance。

因此 plan provenance 升级为：

- `hypothesis_scope_type`
- `hypothesis_scope_ref`

允许两类来源：

- `WORK_FAMILY`：来源于已审计文献 work family；
- `FRAMEWORK`：来源于项目自建、仍未验证的框架假设。

SCRM-v0.2 的 H6-H9 使用：

`hypothesis_scope_type = FRAMEWORK`  
`hypothesis_scope_ref = SCRM-v0.2`

其机器权威登记文件为：

`knowledge/K2_QIMEN_SCRM_PROSPECTIVE_HYPOTHESES.jsonl`

不得把框架作者身份、GitHub CI 成功或“原创”本身转换成 empirical credit。

## 3. SCRM-v0.2 Freeze 必须携带四个结构

所有 `hypothesis_scope_ref = SCRM-v0.2` 的 TEST PLAN，除既有 mandatory freeze fields 外，还必须包含：

- `information_order`
- `comparator_parity`
- `model_freeze`
- `abstention_policy`

缺少任一字段，plan 不得进入有效 prospective freeze。

### 3.1 information_order

正式 prospective case 必须满足：

- world model 已 `FROZEN`；
- symbolic input 在 world freeze 前未参与建模；
- outcome 在 freeze 时未知；
- information cutoff 明确；
- contamination status 为 `CLEAN`。

### 3.2 comparator_parity

必须满足：

- H0/H1 共享 reality information；
- shared information cutoff 与 world-model cutoff 完全一致；
- symbolic increment 被隔离；
- comparator contract 已冻结。

因此不能用“给 SCRM 更多普通现实资料、给 baseline 更少资料”的方式制造增量。

### 3.3 model_freeze

必须冻结：

- `scrm_version = SCRM-v0.2`；
- QCIC version；
- method variants；
- freeze status。

结果出现后不得切换版本重算旧案例。

### 3.4 abstention_policy

必须在反馈前冻结：

- trigger conditions；
- decision rule；
- freeze status；
- `coverage_accounting = true`。

ABSTAIN / UNEVALUABLE 不能从 coverage 分母消失。

## 4. 当前四个 DESIGN_READY 计划

### H6 — WORLD MODEL BEFORE SYMBOLS

研究问题：world-first freeze 是否降低 scenario node / mapping churn。

主要失败条件：没有降低后验修改，或优势仅来自大幅降低 coverage。

### H7 — COMPARATOR INFORMATION PARITY

研究问题：H0/H1 在相同 reality information cutoff 下，symbolic increment 是否仍有稳定增量。

主要失败条件：信息对齐后优势消失或反转。

### H8 — MODEL VERSION FREEZE

研究问题：冻结 SCRM/QCIC/method variant 是否减少 outcome 后 model switching。

主要失败条件：仍需反馈后切换版本才能维持解释。

### H9 — ABSTENTION ACCOUNTABILITY

研究问题：将弃权计入 coverage/selective risk 后，是否能在合理覆盖率下稳定降低错误。

主要失败条件：所谓提升完全由大量弃权造成，或弃权无法事前识别高错误风险案例。

## 5. 当前不创建真实 Batch

本提交只把 H6-H9 提升到 `DESIGN_READY`，不伪造：

- preregistered batch；
- case freeze；
- outcome；
- empirical score。

真实 Batch 必须等到存在符合条件的低风险、结果未知案例与明确 sampling/stopping/exclusion rule 后再建立。

## 6. 认知纪律

这一步本身也必须接受反审：

- 计划更多，不等于证据更多；
- schema 更严格，不等于奇门更有效；
- H6-H9 全部可以失败；
- 若未来 ablation 显示某组件无增量价值，删除或降级；
- 若 H7 在 information parity 下失败，必须直接缩小“symbolic increment”主张，而不是给 SCRM 额外现实信息补强；
- 未经 Batch Review，`empirical_credit = NONE` 永久保持。
