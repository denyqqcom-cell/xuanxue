# WINDOW CONTINUITY PROTOCOL — ChatGPT Web 换窗提示

目的：降低 ChatGPT Web 窗口突然达到上下文/产品限制后无法继续工作的风险。

## 1. 重要限制

当前项目没有一个可审计接口可以读取 ChatGPT Web 的“剩余 token 百分比”“剩余消息数”或“距离窗口满还有多少轮”。因此：

- 禁止输出伪精度百分比；
- 禁止承诺“还能稳定工作 N 轮”；
- 改用可解释的连续性风险状态。

## 2. 每次完成工作都必须报告

每个 completed work cycle 最终回复末尾必须包含：

```text
PROGRESS_SYNC=PASS | PROGRESS_SYNC_BLOCKED
WINDOW_CONTINUITY=CONTINUE | PREPARE_SWITCH | SWITCH_NOW
HANDOFF_READY=YES | NO
```

并给出一句自然语言说明。

## 3. 状态定义

### CONTINUE

满足大部分条件：

- 当前任务的关键 GitHub/Moto/Knowledge 事实已 fresh verify；
- 不依赖已经丢失的旧聊天细节；
- 当前工作可以从仓库 checkpoint 直接恢复；
- 没有出现明显的上下文截断或自相矛盾；
- 下一项任务规模适中。

用户提示：`当前窗口可继续；项目进度已落盘，即使意外中断也可从 checkpoint 恢复。`

### PREPARE_SWITCH

出现任一明显风险即可使用：

- 当前窗口已经经历多个大型 work cycle / 大量工具结果；
- active branch/head 在本窗口内多次快速漂移；
- 即将进入一个长时间、多阶段或高风险任务；
- 需要频繁回溯较早的细节才能继续；
- 当前回答已经需要大量 handoff/context 重建；
- 为保证下一阶段完整闭环，换窗成本已低于继续堆积上下文的风险。

动作：

1. 当前 cycle 完成并同步；
2. 不再开启新的大型 cycle；
3. 更新最终 handoff；
4. 给用户可直接复制的新窗口启动提示。

用户提示：`建议在下一个自然 checkpoint 更换窗口；当前状态已可无损续接。`

### SWITCH_NOW

出现任一强触发：

- 关键历史上下文已经不可访问/明显截断；
- 继续工作需要猜测旧状态；
- 当前窗口无法再可靠完成 fresh verification；
- 用户明确报告窗口已满、即将失效或要求换窗；
- 工具/项目状态已经需要重新在新窗口恢复，继续留在旧窗口没有收益。

动作：停止新实现，只做最后 fresh verify + continuity checkpoint + handoff prompt。

用户提示：`请现在更换窗口；不要在本窗口再开启新工作。`

## 4. HANDOFF_READY

- `YES`：最近一次 `CURRENT_STATE.*` + `WORK_LOG.jsonl` 已同步，重要 Decision Memory 已更新，下一 AI 的 first action 明确。
- `NO`：进度同步受阻或当前状态仍存在未解析漂移；必须先说明缺口。

## 5. 新窗口最小启动提示

当状态为 `PREPARE_SWITCH` 或 `SWITCH_NOW` 时，旧 AI 应给用户以下形式的可复制提示，动态 SHA 不必手抄进提示词，因为新 AI 必须 fresh verify：

```text
@GitHub @Moto X30 Pro

继续 denyqqcom-cell/xuanxue 项目。
先读取仓库根目录 PROJECT_HANDOFF.md，再按 project-handoff/EXECUTION_PLAYBOOK.md 做 Fresh Verification。
不要把旧聊天中的 SHA/CI/Physical 当当前事实；先重新核对 active PR/head、CI、Knowledge 和可用时的 Moto。
读取 project-handoff/CURRENT_STATE.json、CURRENT_STATE.md、WORK_LOG.jsonl 最近 checkpoint、DECISION_MEMORY.md。
验真后输出 HANDOFF_VERIFIED / HANDOFF_DRIFTED / HANDOFF_NOT_VERIFIED，再从 CURRENT_STATE 的 next action 继续。
未授权不要 Merge，不要创建真实 Batch/Freeze/Outcome，不要 destructive sync。
每完成一次工作都必须更新 CURRENT_STATE.* + WORK_LOG，并在回复末尾报告 WINDOW_CONTINUITY。
```

## 6. 目标

最终目标不是预测窗口什么时候“刚好满”，而是让任何一个自然 checkpoint 都已经具备可恢复性，使窗口突然结束只造成会话中断，不造成项目状态丢失。
