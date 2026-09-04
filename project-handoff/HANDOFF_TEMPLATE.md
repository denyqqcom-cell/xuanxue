# HANDOFF TEMPLATE — 跨窗口/跨 AI 最终交接模板

> 旧窗口在准备交接前 fresh verify 后填写。不要复制隐藏思维链，不要复制 secrets，不要把旧 SHA 当成当前事实。

## 1. Handoff result

```text
HANDOFF_VERIFIED | HANDOFF_DRIFTED | HANDOFF_NOT_VERIFIED
PROGRESS_SYNC=PASS | PROGRESS_SYNC_BLOCKED
WINDOW_CONTINUITY=CONTINUE | PREPARE_SWITCH | SWITCH_NOW
HANDOFF_READY=YES | NO
```

原因：

## 2. Continuity checkpoint

```text
checkpoint_id:
continuity_branch:
continuity_commit_sha:
work_log_latest_checkpoint:
current_state_freshness:
```

若 `PROGRESS_SYNC_BLOCKED`，必须说明哪个文件/写入动作失败，并在本交接正文中完整保留临时状态。

## 3. Exact repository state

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

## 4. Current CI

```text
workflow_name / run_number / conclusion / exact_head
...
```

Cancelled / in-progress 不能写 SUCCESS。

## 5. Knowledge state

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

## 6. Cognitive state

```text
active_framework:
world_model_before_symbols:
active_hypotheses:
known_conflicts:
known_counterexamples:
open belief revisions:
```

## 7. Engine state

```text
core_exact_head:
source-grounded fixtures:
full-board/global claims explicitly NOT made:
known unsupported paths:
```

## 8. Product state

```text
current product cycle:
core:
knowledge:
product/ui:
emulator:
physical:
```

若 physical 未 exact-head 重跑，必须写 `INHERITED / NOT_RUN / BLOCKED`，不能写 PASS。

## 9. Empirical state

```text
real_batch:
freeze:
outcome:
batch_review:
replication_review:
empirical_credit:
```

## 10. Moto / local host state

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

## 11. Changes completed in this window

- 

每个真正完成的 work cycle 应能在 `project-handoff/WORK_LOG.jsonl` 找到对应 checkpoint。

## 12. Things explicitly NOT done

- no merge unless authorized
- no real Batch unless authorized
- no hidden rule/metric change
- no destructive local sync
- other:

## 13. Failures / rejected approaches

- 

这些内容同步追加到 `project-handoff/DECISION_MEMORY.md`（若属于长期有价值的教训）。

## 14. Next work

按优先级列最多 5 项：

1. 
2. 
3. 
4. 
5. 

## 15. Next AI first action

必须是一个可验证、低风险、read-only 起手动作，例如：

```text
Fresh read active PR + exact branch head + current CI + CURRENT_STATE.json + WORK_LOG latest checkpoint；
如 Moto connector 可用，再 read-only 检查 local repo，不做 reset/pull。
```

## 16. Required non-claims

至少确认：

```text
Evidence != Truth != Claim
CI PASS != predictive validity
REAL_BATCH/FREEZE/OUTCOME state is stated explicitly
EMPIRICAL_CREDIT state is stated explicitly
```

## 17. ChatGPT Web 换窗提示

如果 `WINDOW_CONTINUITY=PREPARE_SWITCH` 或 `SWITCH_NOW`，附上可直接复制的新窗口启动提示词。不要要求用户手工复制当前 SHA；新 AI 必须 fresh verify。

推荐最小提示：

```text
@GitHub @Moto X30 Pro
继续 denyqqcom-cell/xuanxue 项目。先读取 PROJECT_HANDOFF.md，并按 project-handoff/EXECUTION_PLAYBOOK.md Fresh Verification。
读取 CURRENT_STATE.json / CURRENT_STATE.md / WORK_LOG.jsonl 最近 checkpoint / DECISION_MEMORY.md。
不要把旧聊天 SHA/CI/Physical 当当前事实。验真后输出 HANDOFF_VERIFIED / HANDOFF_DRIFTED / HANDOFF_NOT_VERIFIED，再继续 next action。
未授权不要 Merge，不要创建真实 Batch/Freeze/Outcome；每完成一次工作都更新 CURRENT_STATE.* + WORK_LOG，并报告 WINDOW_CONTINUITY。
```
