# HANDOFF TEMPLATE — 跨窗口/跨 AI 最终交接模板

> 旧窗口在准备交接前 fresh verify 后填写。不要复制隐藏思维链，不要复制 secrets，不要把旧 SHA 当成当前事实。

## 1. Handoff result

```text
HANDOFF_VERIFIED | HANDOFF_DRIFTED | HANDOFF_NOT_VERIFIED
```

原因：

## 2. Exact repository state

```text
repository:
active_branch:
active_head_sha:
active_pr:
pr_state:
pr_base:
pr_base_sha:
merge_authorized: false/true
```

## 3. Current CI

```text
workflow_name / run_number / conclusion / exact_head
...
```

Cancelled / in-progress 不能写 SUCCESS。

## 4. Knowledge state

```text
phase:
registry_sources:
lineage_rows:
formal_wave1_complete:
formal_wave1_total:
atomic_evidence_rows:
actionable_queue_remaining:
unknown_backlog:
claim_extraction:
```

注明哪些数字是 fresh aggregate，哪些只是 inherited snapshot。

## 5. Cognitive state

```text
active_framework:
world_model_before_symbols:
active_hypotheses:
known_conflicts:
known_counterexamples:
open belief revisions:
```

## 6. Engine state

```text
core_exact_head:
source-grounded fixtures:
full-board/global claims explicitly NOT made:
known unsupported paths:
```

## 7. Product state

```text
current product cycle:
core:
knowledge:
product/ui:
emulator:
physical:
```

若 physical 未 exact-head 重跑，必须写 `INHERITED / NOT_RUN / BLOCKED`，不能写 PASS。

## 8. Empirical state

```text
real_batch:
freeze:
outcome:
batch_review:
replication_review:
empirical_credit:
```

## 9. Moto / local host state

```text
connector_available:
local_repo_path:
local_head:
local_branch:
tracked_worktree:
untracked:
ahead_behind_remote:
local_only_commits_preserved:
physical_device:
```

若无法 fresh verify：

```text
PHYSICAL_NOT_VERIFIED
LOCAL_REPO_NOT_VERIFIED
```

不要从旧聊天补值。

## 10. Changes completed in this window

- 

## 11. Things explicitly NOT done

- no merge unless authorized
- no real Batch unless authorized
- no hidden rule/metric change
- no destructive local sync
- other:

## 12. Failures / rejected approaches

- 

这些内容同步追加到 `project-handoff/DECISION_MEMORY.md`（若属于长期有价值的教训）。

## 13. Next work

按优先级列最多 5 项：

1. 
2. 
3. 
4. 
5. 

## 14. Next AI first action

必须是一个可验证、低风险、read-only 起手动作，例如：

```text
Fresh read active PR + exact branch head + current CI + CURRENT_STATE.json；
如 Moto connector 可用，再 read-only 检查 local repo，不做 reset/pull。
```

## 15. Required non-claims

至少确认：

```text
Evidence != Truth != Claim
CI PASS != predictive validity
REAL_BATCH/FREEZE/OUTCOME state is stated explicitly
EMPIRICAL_CREDIT state is stated explicitly
```
