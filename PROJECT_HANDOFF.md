# PROJECT HANDOFF — 项目级 AI 续接入口

> **所有接手 `denyqqcom-cell/xuanxue` 的 AI，请先读这里。**

本文件只负责把你导向项目级续接包。术数模块自己的工程 handoff 仍在 `handoff/`；项目总体进度、路线、当前权威快照、执行纪律与跨窗口记忆统一放在：

- `project-handoff/README.md`
- `project-handoff/CURRENT_STATE.md`
- `project-handoff/CURRENT_STATE.json`
- `project-handoff/WORK_LOG.jsonl`
- `project-handoff/WINDOW_CONTINUITY_PROTOCOL.md`
- `project-handoff/ROADMAP.md`
- `project-handoff/EXECUTION_PLAYBOOK.md`
- `project-handoff/ACCEPTANCE_AND_EPISTEMIC_RULES.md`
- `project-handoff/DECISION_MEMORY.md`
- `project-handoff/HANDOFF_TEMPLATE.md`

## 最重要的规则

1. **快照不是当前真相。** 新窗口必须 fresh read GitHub / PR / CI / Knowledge Engine；需要真机事实时 fresh read Moto。若动态事实漂移，输出 `HANDOFF_DRIFTED` 并重建状态。
2. **不得把聊天记忆当仓库事实。** 权威顺序：live GitHub / exact commit repository records / current CI / current physical evidence > 本目录快照 > 旧聊天。
3. **Evidence != Truth != Claim。** CI、fixture、source agreement、工程实现都不能自动升级为现实预测有效。
4. **未获用户明确授权不得 Merge。** 不得为了“同步”粗暴 `reset --hard`、删除 local-only commits、stash/clean 未授权文件。
5. **项目状态必须分轨报告。** Corpus / Cognitive / Engine / Product / Empirical 不得压成一个“总完成度”。
6. **完成一次工作，就必须完成一次 Continuity Checkpoint。** 在向用户宣告该工作完成前，fresh verify 动态事实，更新 `CURRENT_STATE.md` + `CURRENT_STATE.json`，并向 `WORK_LOG.jsonl` 追加一条记录；若无法写入，必须明确报告 `PROGRESS_SYNC_BLOCKED`，不能静默跳过。
7. **ChatGPT Web 每次工作完成都要报告窗口续接状态。** 使用 `CONTINUE / PREPARE_SWITCH / SWITCH_NOW`，不得伪造“剩余 token 百分比”；具体规则见 `WINDOW_CONTINUITY_PROTOCOL.md`。

接手后第一步：执行 `project-handoff/EXECUTION_PLAYBOOK.md` 的 Fresh Verification，然后再继续开发。
