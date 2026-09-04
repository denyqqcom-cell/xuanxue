# ROADMAP — 项目开发 / 认知 / 实证总路线

本路线不再用单一 P0→P6 描述全部成熟度。项目同时存在认知、实证、工程产品三条主链，最后在理论重构处汇合。

## 总体目标

建立一个能够回答以下问题的玄学 Knowledge Engine / Product：

- 我为什么相信这条规则？
- 它来自什么 source / work / school / page？
- 它在什么条件下成立，哪里可能失效？
- 有哪些竞争解释、反例和冲突？
- 目前是盘面事实、来源规则、项目推论还是未验证假设？
- 什么未来证据会让我改变观点？
- 真实 prospective outcome 是否支持它？

目标不是把“书上写了”变成“系统真理”，也不是把大量 gate 当成研究成果。

## 三条主链

### A. 认知链

```text
SOURCE
→ CARRIER / LINEAGE
→ PAGE READING
→ ATOMIC EVIDENCE
→ THEORY MODEL
→ ASSUMPTION / BOUNDARY
→ CONFLICT
→ CONTEXT ACTIVATION
→ COMPETING HYPOTHESES
→ BELIEF REVISION
```

### B. 实证链

```text
HYPOTHESIS
→ COMPARATOR
→ PREREGISTRATION
→ SAMPLE IDENTITY / PROVENANCE
→ BATCH
→ FREEZE
→ OUTCOME
→ BATCH REVIEW
→ REPLICATION REVIEW
→ MANUAL EMPIRICAL CREDIT DECISION
```

### C. 工程/产品链

```text
SOURCE-GROUNDED ENGINE
→ CORE FIXTURES
→ CONTEXTUAL REASONING CONTRACT
→ PRODUCT PROVENANCE
→ APP / UX
→ EMULATOR
→ PHYSICAL DEVICE
```

## 阶段路线

### T0 — Truth Convergence

目的：任何时候只维护一个“当前候选事实树”，但保留历史 Draft/失败证据。

工作：
- fresh verify active PR stack / exact heads；
- 检查本地仓库分叉与 local-only commits；
- 不允许粗暴 reset；
- 不把 PR prose 当 exact branch truth；
- 分支整合必须先做无副作用 compare/merge-tree 审计。

退出条件：当前候选树、Knowledge 状态、CI 与任务依赖可以被一个新 AI 重现。

### C1 — Cognitive Retrospective

目的：反审过去为什么会“机械照书、符号先行、结果后解释”。

每个 active belief/hypothesis 至少回答：
- source basis；
- hidden assumptions；
- applicability boundary；
- known counterexample / conflict；
- competing explanation；
- falsifier；
- KEEP / MERGE / DOWNGRADE / SPLIT / DELETE 结果。

禁止 KPI：不强制必须 DELETE，不强制必须发现固定数量 latent factor。

### C2 — Constructive Mastery

目的：把真实逐书掌握重新变成主要研究吞吐。

当前 formal Wave1 snapshot：`6/37`。

一本阅读单元 COMPLETE 至少要求：
- carrier identity verified；
- page review complete；
- Reading Ledger complete；
- page-bound Atomic Evidence；
- intra-source contradiction review；
- cross-source conflict links；
- applicability boundaries；
- per-book/work distillate；
- unprovable claims remain unpromoted；
- Claim Extraction 仍受全局 gate 控制。

优先级由 current execution queue 决定，不能仅凭文件名或旧聊天猜下一本。

### E1 — Engine Verification

目的：只给可复现结构以 structural credit。

奇门重点矩阵：
- 阴/阳遁；
- 九局/三元/定元；
- 旬首/值符/值使；
- 中五寄宫；
- 地盘/天盘/八门/九星/八神；
- 日空/时空；
- 马星；
- 五不遇时；
- school/method variation。

任何 fixture 必须有 source/algorithm provenance。单个 fixture PASS != whole-board PASS；whole-board PASS != predictive validity。

### R1 — Scenario Reasoning

目的：从“符号→断语”转成“现实世界模型→角色/对象→符号条件化→竞争解释”。

强制顺序：

```text
M0 normalize/freeze reality input
→ M1 world model, reality only
→ M2 chart/symbol mapping enters
→ M3 freeze prediction / abstain / unevaluable
→ M4 narrative cannot rewrite M3
```

缺少具体事体时停在 Structure，不自动补造成败、吉凶或应期。

### P1 — Product Cognition UX

目的：让用户看得见 epistemic boundary。

当前 active PR #45 实现四类分析 provenance：
- 盘面事实；
- 来源规则；
- 项目推论；
- 未经验证假设。

现实输入必须单独呈现。下一步完成 exact-head Unit/System/Product/Physical/Epistemic closure，不把 UI 完成当理论验证。

### X1 — Preregistration

目的：outcome 之前冻结模型、样本身份、comparator、scoring、N、decision rule、policy content。

当前已有大量 contract infrastructure，但 `REAL_BATCH=NONE`。只有当实验自身的 source/engine/representation/comparator/outcome contract 都闭合，且用户明确授权，才创建 production Batch。

### X2 — Prospective Test

目的：让理论接受真正可能失败的现实测试。

要求：
- no outcome peeking；
- no post-hoc case replacement；
- no rule/metric shopping；
- abstain/unevaluable retained；
- same-case comparator parity；
- complete fixed-N review；
- replication before empirical credit。

### T1 — Theory Reconstruction

目的：Outcome 反向修改理论，而不是为旧理论找例外。

允许结果：
- SUPPORT；
- PARTIAL_SUPPORT；
- NO_SUPPORT；
- INSUFFICIENT_INFORMATION。

理论修订动作：KEEP / MERGE / DOWNGRADE / SPLIT / DELETE。保留失败历史和 revision rationale。

## 当前优先顺序

1. 关闭 PR #45 当前 Product/CI/Physical checkpoint；
2. 保持 `project-handoff/` 快照与 active head 同步；
3. 继续 C2 corpus mastery，而不是继续以 gate 数量为主要产出；
4. 并行做 E1 source-grounded fixture matrix 和 C1 adversarial review；
5. 把 R1 world model/competing hypotheses 进入真实用例；
6. 实验入口条件满足且用户明确授权后才进入 X1/X2；
7. 有真实 Outcome 后才允许 T1 获得 empirical revision credit。
