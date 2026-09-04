# xuanxue Project Continuity Pack

版本：2026-09-05.1

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
5. `project-handoff/ACCEPTANCE_AND_EPISTEMIC_RULES.md`
6. `project-handoff/ROADMAP.md`
7. `project-handoff/DECISION_MEMORY.md`
8. `project-handoff/EXECUTION_PLAYBOOK.md`
9. 与当前任务相关的 `knowledge/`、`handoff/<domain>/`、PR body、CI logs

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

## 与现有目录的关系

- `knowledge/`：六术统一 Source / Lineage / Reading / Evidence / Claim / Prospective contracts 的正式知识治理层；
- `handoff/`：各术数模块从研究材料进入可实现逻辑的工程交付层；
- `project-handoff/`：项目总体开发/认知/实证/产品路线及跨 AI 续接层；
- `DEVICE_ACCEPTANCE.md`：设备验收合同；
- `LOCAL_AI_EXECUTION_BOUNDARY.json`：本地执行助手边界。

本目录**不得复制现代书籍全文、扫描件、秘密、私有绝对路径、真实身份材料或 HMAC secret**。

## 更新时机

以下事件发生后应更新 `CURRENT_STATE.*`：

- active PR / exact head 改变；
- Wave1 COMPLETE / Evidence / queue 变化；
- Engine/UX 阶段进入新 checkpoint；
- Emulator / Physical exact-head acceptance 变化；
- 创建真实 Batch / Freeze / Outcome；
- empirical credit 状态变化；
- 发现重要分支分叉、回归、理论降级或路线改变。

重要设计选择、失败教训、废弃路径更新到 `DECISION_MEMORY.md`，不要只覆盖掉旧状态。
