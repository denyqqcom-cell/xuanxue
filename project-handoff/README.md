# xuanxue Project Continuity Pack

版本：2026-09-05.2

用途：让任何新的 ChatGPT / Codex / 本地执行 AI 在**不依赖旧聊天记忆**的情况下，能够恢复项目真实状态、理解路线、遵守边界并继续工作。

本目录不是聊天备份，也不是“长期不变的真相文件”。它把项目续接拆成三类内容：

- **Stable Contract**：长期目标、方法论、验收与禁止事项，低频修改；
- **Dynamic Snapshot**：某个 exact Git SHA 下的进度快照，高频更新，必须 fresh verify；
- **Decision Memory**：为什么做过某些决定、哪些路径被否定、有哪些已知认知债务，追加为主。

这种拆法用于避免两个常见失败：一是旧窗口 SHA/CI 被新窗口误当当前事实；二是项目只保存“做了什么”，却没有保存“为什么这样做、什么不能再做”。

## 新 AI 的强制阅读顺序

1. `PROJECT_HANDOFF.md`
2. `project-handoff/README.md`
3. `project-handoff/CURRENT_STATE.json`
4. `project-handoff/CURRENT_STATE.md`
5. `project-handoff/WORK_LOG.jsonl`（至少读最近 checkpoint）
6. `project-handoff/WINDOW_CONTINUITY_PROTOCOL.md`（ChatGPT Web 必读）
7. `project-handoff/ACCEPTANCE_AND_EPISTEMIC_RULES.md`
8. `project-handoff/ROADMAP.md`
9. `project-handoff/DECISION_MEMORY.md`
10. `project-handoff/EXECUTION_PLAYBOOK.md`
11. 与当前任务相关的 `knowledge/`、`handoff/<domain>/`、PR body、CI logs

## 接手状态协议

Fresh Verification 后只能输出三种项目续接状态之一：

```text
HANDOFF_VERIFIED
HANDOFF_DRIFTED
HANDOFF_NOT_VERIFIED
```

- `HANDOFF_VERIFIED`：动态 SHA / PR / Knowledge / CI 等关键事实已重新核对，和快照兼容；
- `HANDOFF_DRIFTED`：远端 HEAD、PR、Corpus、Evidence、CI、路线依赖等已变化；必须以当前事实重建计划；
- `HANDOFF_NOT_VERIFIED`：缺少必要权限/工具，不能验证；不得把旧记录冒充当前状态。

物理设备可以单独处于 `PHYSICAL_NOT_VERIFIED`，这不等于 GitHub 状态也无法验证。

## 项目五条状态链

任何状态报告都必须至少区分：

1. **Corpus Mastery**：Source Registry / Lineage / Reading / Evidence / Distillate；
2. **Cognitive Reconstruction**：Theory / assumptions / boundary / conflict / competing explanations / belief revision；
3. **Engine Structural Credit**：算法、fixture、source-grounded reproducibility；
4. **Product Acceptance**：Core / App / Emulator / Physical / UX provenance；
5. **Prospective Empirical Credit**：Preregistration / Batch / Freeze / Outcome / Review / replication。

禁止把这五条压成一个总体百分比。

## 权威顺序

动态事实优先级：

```text
Live GitHub / exact ref
> exact-commit repository records
> current CI evidence
> fresh Moto / physical evidence
> project-handoff snapshot
> PR prose / comments
> old chat / model memory
```

PR body 可能滞后于 branch head；必须比较 exact head、diff 与 workflow run。任何旧 SHA 只能是线索。

## Per-work Continuity Checkpoint：完成工作即更新进度

从 v2026-09-05.2 起，**“工作完成”与“进度同步完成”是同一个事务边界**。任何 AI 在向用户说“这轮完成了”之前必须：

1. fresh read 当前 active branch / PR / CI / Knowledge / Physical（适用时）；
2. 更新 `CURRENT_STATE.md`；
3. 更新 `CURRENT_STATE.json`；
4. 向 `WORK_LOG.jsonl` **追加**一条 checkpoint；
5. 若本轮产生长期决策、失败教训或废弃路径，再追加 `DECISION_MEMORY.md`；
6. 最终回复中回报 `PROGRESS_SYNC=PASS` 与 continuity branch exact commit；若写入失败则回报 `PROGRESS_SYNC_BLOCKED`。

这意味着未来不再“窗口快满了才补 handoff”，而是每个已完成工作周期都留下可续接点。即使浏览器窗口突然无法继续，新窗口也只需要读取最后一个已落盘 checkpoint。

**边界说明：** AI 没有在无人运行时持续监听 GitHub 的后台能力，因此这里的“实时”定义为**每个已执行工作周期在返回用户前同步**，而不是声称 24/7 daemon 式实时。若外部 actor 在两个会话之间推进分支，下一次 Fresh Verification 必须检测为 drift 并更新快照。

## ChatGPT Web 窗口续接信号

ChatGPT Web 端没有提供给本项目一个可审计的“剩余上下文百分比”接口，因此禁止报伪精度，例如“还剩 18% token”。每次完成工作后改为输出以下一个状态：

```text
CONTINUE
PREPARE_SWITCH
SWITCH_NOW
```

含义和触发器见 `WINDOW_CONTINUITY_PROTOCOL.md`。无论状态如何，最后一个 Continuity Checkpoint 都必须已经写入仓库或明确报告写入受阻。

## 与现有目录的关系

- `knowledge/`：六术统一 Source / Lineage / Reading / Evidence / Claim / Prospective contracts 的正式知识治理层；
- `handoff/`：各术数模块从研究材料进入可实现逻辑的工程交付层；
- `project-handoff/`：项目总体开发/认知/实证/产品路线及跨 AI 续接层；
- `DEVICE_ACCEPTANCE.md`：设备验收合同；
- `LOCAL_AI_EXECUTION_BOUNDARY.json`：本地执行助手边界。

本目录**不得复制现代书籍全文、扫描件、秘密、私有绝对路径、真实身份材料或 HMAC secret**。

## 更新时机

`CURRENT_STATE.*` 与 `WORK_LOG.jsonl` 的默认更新频率现在是：**每个 completed work cycle**。

此外，下列事件即使发生在一个较大工作周期内部，也应在安全 checkpoint 处尽快同步：

- active PR / exact head 改变；
- Wave1 COMPLETE / Evidence / queue 变化；
- Engine/UX 阶段进入新 checkpoint；
- Emulator / Physical exact-head acceptance 变化；
- 创建真实 Batch / Freeze / Outcome；
- empirical credit 状态变化；
- 发现重要分支分叉、回归、理论降级或路线改变。

重要设计选择、失败教训、废弃路径更新到 `DECISION_MEMORY.md`，不要只覆盖掉旧状态。
