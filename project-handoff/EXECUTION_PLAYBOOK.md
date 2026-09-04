# EXECUTION PLAYBOOK — 新 AI 接手与实施流程

本文件规定“接手项目后怎么做”，防止新窗口从旧聊天直接继续写代码。

## A. Fresh Verification — 先验真

### A1. GitHub

至少重新读取：

- repository / default branch；
- active open Draft PRs；
- 当前任务对应 PR 的 `base / base_sha / head / head_sha / draft / merged / mergeable`；
- branch exact head；
- exact-head workflow runs / job steps；
- 与任务相关的 repository state files。

禁止仅根据 PR body 的“Current head”判断，因为 body 可能落后于 branch。

### A2. Knowledge Engine

对于 corpus / evidence / claim 状态，优先运行或读取当前 exact tree 的正式 aggregator/validator：

```bash
python3 tools/validate_knowledge.py
python3 tools/validate_k2_evidence.py
python3 tools/validate_k2_per_book_completion.py
python3 tools/validate_k2_claim_extraction_readiness.py
```

若仓库已经新增/替换 authoritative aggregate contract，应以当前 CI 调用为准。

必须区分：

```text
Source Registry
Source Lineage
Deep Reading
Formal Wave1 Reading
Atomic Evidence
Composite Execution Closure
Claim Readiness
Prospective Empirical Credit
```

不得互相代替。

### A3. Moto / local host

如果当前会话支持 Moto connector，第一轮只做 read-only：

```bash
git rev-parse --show-toplevel
git status --short --branch
git rev-parse HEAD
git branch -vv
git fetch --all --prune
git rev-list --left-right --count HEAD...origin/<target-branch>
```

如果发现 local-only commits、diverged history 或 untracked 文件：先报告并建立安全策略；**不得自动 reset/stash/clean/delete**。

如果 connector 返回 `FORBIDDEN`/无权限：记录 `PHYSICAL_NOT_VERIFIED`，不要推断手机断线。

## B. Handoff decision

验真后输出：

- `HANDOFF_VERIFIED`：关键动态事实匹配；
- `HANDOFF_DRIFTED`：事实变化，重建 current state/plan；
- `HANDOFF_NOT_VERIFIED`：缺权限或缺证据。

若只有 Moto 不可验证，可写：

```text
HANDOFF_VERIFIED_GITHUB
PHYSICAL_NOT_VERIFIED
```

但绝不把旧 physical PASS 复制到新 exact head。

## C. 任务实施纪律 — 11 steps

每个独立 cycle 使用：

```text
1 DEFINE
2 BASELINE
3 FAIL-FIRST
4 IMPLEMENT
5 UNIT VERIFY
6 SYSTEM VERIFY
7 PRODUCT VERIFY
8 PHYSICAL VERIFY
9 EPISTEMIC VERIFY
10 CHECKPOINT
11 ONLY THEN CONTINUE
```

不是每个改动都需要 App/Physical；不适用时明确写 `NOT_APPLICABLE`，而不是伪造 PASS。

### DEFINE

写清：目标、非目标、权威输入、允许修改范围、禁止事项、成功/失败条件。

### BASELINE

记录 exact base SHA、相关测试现状、当前 bug/缺口的可复现证据。

### FAIL-FIRST

能够 test-first 的工程缺口应先证明旧系统真的会失败。理论/资料工作则用明确反例、冲突或缺证据状态，不为了形式制造无意义红灯。

### IMPLEMENT

最小修改，不同时偷偷扩大理论、产品和 empirical scope。

### UNIT / SYSTEM

跑对应核心测试和 Knowledge contracts；失败必须解释，不得把 cancelled/in-progress 冒充成功。

### PRODUCT

涉及 App/UX 时检查用户实际看到的 provenance、边界、错误恢复，不只是编译成功。

### PHYSICAL

只有 exact-head 真机执行才能记 `PHYSICAL=PASS`。相同 binary/tree 可以记 `INHERITED`，不能升级为 exact-head PASS。

### EPISTEMIC

每轮回答：
- 这次增加的是 source / structure / method / product / empirical 哪一种 credit？
- 什么仍然没有被证明？
- 有没有把 CI/fixture/来源一致性错写成现实有效？

### CHECKPOINT

更新：
- PR body/comment；
- `project-handoff/CURRENT_STATE.*`；
- 必要时 `DECISION_MEMORY.md`；
- exact head / CI / acceptance matrix。

## D. Git/PR 治理

- 用户没有明确说“Merge”时，不 merge；
- stacked PR 不独立 merge；
- 创建新工作优先独立 branch / Draft PR，避免污染正在验收的 cycle；
- force update / reset / rebase 只有在明确审查并授权后做；
- remote authority 与 local worktree 不一致时，先 preserve local-only commits；
- old SHA/PR/CI evidence 不得覆盖新的 exact-head evidence。

## E. 资料阅读治理

逐书工作必须从 canonical source identity 开始：

```text
SHA256 identity
→ carrier/work/segment identity
→ page review
→ Reading Ledger
→ Atomic Evidence
→ conflict/applicability
→ distillate
```

`TEXT_DIRECT` 与 `VISUAL_REQUIRED` 按 current routing contract 执行。SCAN/视觉页不能用 OCR 文本“冒充看过原页”。

Evidence 只保存来源支持的事实，不补写模型常识。来源内部错误保留为 inconsistency/conflict candidate。

## F. 实验治理

没有用户明确授权时，不创建真实 production Batch。

即使用户授权，也要先确认：
- exact hypothesis/context/content binding；
- model/engine version；
- comparator parity；
- fixed N / scoring / decision rule；
- sample identity/provenance；
- outcome route；
- no known outcome leakage；
- current experiment-specific source/fixture sufficiency。

Wave1 全库百分比不是单一 Qimen experiment 的自动门槛；同样，工程 gate 全绿也不是 Batch 启动理由。

## G. 交接前最后一步

窗口接近上限或准备换 AI 时：

1. 停止开启新大任务；
2. fresh read exact head / PR / CI / Knowledge / Physical；
3. 更新 `CURRENT_STATE.md` 与 `CURRENT_STATE.json`；
4. 把重要决定/失败追加到 `DECISION_MEMORY.md`；
5. 用 `HANDOFF_TEMPLATE.md` 生成最后交接摘要；
6. 明确下一 AI 的第一条 read-only 动作。
