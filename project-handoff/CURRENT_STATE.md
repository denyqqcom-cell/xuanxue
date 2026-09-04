# CURRENT STATE — Snapshot at 2026-09-05

> 这是**可审计快照**，不是永远有效的“当前真相”。任何新 AI 必须先按 `EXECUTION_PLAYBOOK.md` fresh verify。

## 1. Snapshot identity

- captured_local_time: `2026-09-05T01:05:00+08:00`
- repository: `denyqqcom-cell/xuanxue`
- snapshot_parent_branch: `ci/qimen-ui-provenance-v1`
- snapshot_parent_head: `ff1a3389b90e854bd81d17b9cf1c54218e1074b3`
- active PR at capture: `#45 Product carrier: separate Qimen provenance classes`
- PR #45: `OPEN / DRAFT / UNMERGED / MERGEABLE`
- PR #45 base: `ci/qimen-world-model-before-symbols-v1@426300ad914d18a71163c2aac5aa4e16e50aeb73`
- no merge authorization is implied by this snapshot.

## 2. Current product/core work

PR #45 当前已经不只是 fail-first：branch exact head `ff1a3389...` 包含奇门产品层四类 provenance UI 分区：

1. 盘面事实 `CHART_FACT`
2. 来源规则 `SOURCE_RULE`
3. 项目推论 `PROJECT_INFERENCE`
4. 未经验证假设 `UNVERIFIED_HYPOTHESIS`

用户现实输入保持在四类之外。该设计用于防止“用户事实 / 盘面字段 / 书中规则 / 项目推论 / 未验证候选”在 UI 上被呈现成同一可信度。

上游 PR #44 已建立 `WORLD_MODEL_BEFORE_SYMBOLS` M0–M4 Core contract；这属于认知治理/结构信用，不是预测有效性。

## 3. Knowledge Engine

Current repository state declares:

- phase: `K2_EVIDENCE_EXTRACTION`
- K1 acceptance: `PROJECT_VERIFIED`
- source lineage: `COMPLETE`
- evidence extraction: open
- claim extraction: `BLOCKED`
- execution owner: `PROJECT_MAIN_AGENT`
- local AI role: `EXECUTION_HELPER_ONLY`
- source identity authority: canonical file SHA-256

### Formal Wave1

Current exact tree contains six formal COMPLETE Reading rows:

- Qimen: `QM-SRC-0001`, `QM-SRC-0003`, `QM-SRC-0016`, `QM-SRC-0021`, `QM-SRC-0028` = **5/5 Qimen Wave1**
- Ziwei: `ZW-SRC-0002` = **1 formal COMPLETE unit**

Aggregate formal Wave1:

- `6 / 37 COMPLETE` = **16.2%**
- `31 / 37` are not formal legacy COMPLETE
- Atomic Evidence: **694**
- Claim Extraction: **BLOCKED**
- UNKNOWN textual backlog: **91**

Important: composite execution closure and historical deep-reading records are separate credit types. Do not infer actionable queue size from `37 - 6` without running the current queue aggregator.

### Registry vs real reading

- K1 Source Registry / Lineage coverage is structurally mature (historically 515 sources / 515 lineage rows), but this is **not** corpus mastery.
- “登记 515 个来源”不得写成“学完 515 本”。
- Corpus mastery reports must use Reading/Evidence/Distillate state, not registry count.

## 4. Empirical state

Current project boundary remains:

```text
REAL_BATCH = NONE
FREEZE = NONE
OUTCOME = NONE
EMPIRICAL_CREDIT = NONE
CLAIM_EXTRACTION = BLOCKED
```

Repository contains substantial preregistration, paired-comparator, batch-review, replication-credit, sample provenance and canonical identity infrastructure. Those gates control hindsight/provenance degrees of freedom; they do not create empirical evidence by themselves.

## 5. CI state at snapshot

For parent head `ff1a3389...`:

- `K2 World Model Before Symbols #11` — SUCCESS
- `K2 QCIC v0.6 Machine Gates #435` — SUCCESS
- `Knowledge Engine V1 CI #979` — IN_PROGRESS at capture
  - knowledge steps through local-AI/device-contract checks had completed successfully;
  - Windows `k2-helper-portability` had completed SUCCESS;
  - stable `:ziwei-core:test` step was still running at capture.

Do not preserve `IN_PROGRESS` as a permanent conclusion. Fresh read the workflow by exact head.

## 6. Physical / Moto state

This session attempted fresh Moto X30 Pro host access and received:

```text
FORBIDDEN: This conversation does not support developer MCPs
```

Therefore:

```text
CURRENT_SESSION_PHYSICAL_STATE = NOT_VERIFIED
```

This does **not** mean the phone, ADB, AgentDock or prior physical evidence failed. It only means this session could not independently verify them. Any physical PASS must be bound to an exact source head and fresh execution evidence; binary equivalence may be recorded as `INHERITED`, not exact-head physical PASS.

## 7. Current strategic diagnosis

The project is unevenly mature:

- governance / experiment infrastructure: high
- Qimen first-wave corpus: closed for its selected 5 units
- whole six-domain Wave1 corpus: still early (`6/37` formal COMPLETE)
- engine structural verification: partial; full Qimen golden-board closure is still not established
- contextual reasoning architecture: actively improving (`WORLD_MODEL_BEFORE_SYMBOLS`)
- product cognition UX: active in PR #45
- real prospective evidence: zero

Next work should not be measured by number of new validators. Prefer source completion, adversarial theory review, source-grounded fixtures, real scenario reasoning, exact-head product/physical acceptance, then prospective testing.
