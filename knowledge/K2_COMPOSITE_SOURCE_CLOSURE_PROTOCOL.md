# K2 Composite Source Closure Protocol

版本：2026-09-03
阶段：K2B / Deep Closure
状态：ACTIVE_CONTRACT

## 1. 目的

现有 K2 同时要求：

1. Wave1 legacy Reading / Evidence / Book Distillate 继续保持 source-level 语义；
2. composite carrier 不得为了迁就旧 `source_id -> work_id` 模型而伪造成单一作品；
3. `K2_DEEP_READING_LEDGER` 可以记录真实的 carrier-level 全页视觉阅读，但 Reading Credit 本身不等于 Evidence、Distillate 或 Claim。

因此需要一个显式、可失败的执行闭环，使“已经完整读完、完成 segment/work 归一化的 composite carrier”能够退出 actionable execution queue，同时不污染 legacy Wave1 COMPLETE 计数。

新增注册表：

`knowledge/K2_COMPOSITE_SOURCE_CLOSURES.jsonl`

它记录的是 **composite carrier execution resolution**，不是新的 legacy Reading Ledger。

## 2. 信用边界

合法 closure 必须固定：

- `legacy_wave1_credit = NONE`
- `carrier_independent_vote_credit = NONE`
- `empirical_credit = NONE`
- `claim_extraction_blocked = true`

因此：

`COMPOSITE EXECUTION CLOSED != LEGACY WAVE1 COMPLETE != EMPIRICAL VALIDATION != TRUTH`

退出执行队列不增加传统理论的真实性信用，也不增加一个新的 independent evidence vote。

## 3. 必需依赖链

一个 composite source 只有在以下链路全部存在并通过 validator 后才能声明 `queue_resolution=RESOLVED`：

`canonical source`
→ `K2_SOURCE_SEGMENTS`
→ `K2_DEEP_READING_LEDGER (SEGMENTED_CARRIER / COMPLETE / VISUAL_PAGE)`
→ `K2_SEGMENT_LINEAGE`
→ `K2_SEGMENT_EVIDENCE`
→ `K2_WORK_FAMILY_DISTILLATES`
→ `K2_COMPOSITE_SOURCE_CLOSURES`

仅有 100% Deep Reading 不足以产生 closure；仅有 segmentation 也不足以产生 closure。

## 4. Hard gate

`tools/validate_k2_composite_source_closures.py` 必须至少验证：

- source canonical SHA 与 K1/K2 source registry 一致；
- Deep Reading 覆盖固定 PDF 的 `p1-pN`，并且是 `COMPLETE / REVIEWED / VISUAL_PAGE / SEGMENTED_CARRIER`；
- Deep Reading 的 `segment_ids` 与当前 reviewed segmentation 精确一致；
- 每个 governed work-bearing segment 恰有一个 segment→work binding；
- 每个 governed domain route 至少有一条 Segment Evidence；
- `NON_WORK` segment 不得产生 Segment Evidence；
- 每个 work family 恰有一个 REVIEWED Work-Family Distillate；
- distillate 必须引用同一 carrier Deep Reading，并精确覆盖该 family 当前 Segment Evidence；
- 同 source 不得同时获得 terminal legacy Wave1 Reading、legacy Evidence 或 legacy Book Distillate；
- closure 不得泄漏 empirical credit、Claim authorization、carrier-level independent vote 或本地文件路径。

任一条件不满足，closure 必须 fail closed。

## 5. Queue 语义

Legacy Wave1 terminal set 的定义保持不变：

`legacy_terminal = Reading Ledger 中 COMPLETE 或 BLOCKED 的 source`

Execution queue 的 resolved set 扩展为：

`execution_resolved = legacy_terminal ∪ validated_composite_execution_closures`

因此 actionable queue 为：

`expected_sources - execution_resolved`

必须分别报告：

- legacy terminal / legacy COMPLETE 计数；
- composite execution closure 计数；
- execution-resolved 计数。

禁止把 `execution_resolved` 偷换成 legacy Wave1 COMPLETE。

## 6. Deep Reading reuse 不等于完成

Execution queue 仍允许 `deep_reading_reusable=true` 来避免重复阅读，但不能直接从 `_deep_complete()` 推导 source 已完成。

原因：

`Reading Credit != Attribution Credit != Evidence Credit != Distillation Credit != Execution Closure`

只有显式 closure registry 通过 hard gate 后，composite source 才能离开 actionable queue。

## 7. 与 per-book aggregate 的关系

`tools/validate_k2_per_book_completion.py` 继续以 legacy Wave1 aggregate 计算 `complete / partial / blocked`，不得把 composite closure 混入这些数字。

同一 gate 另外验证 composite closure registry，并单独输出 `composite_execution_closed=N`。

这样同时保留：

- 旧 Wave1 会计语义的连续性；
- composite source 的真实 execution progress；
- 不为 schema 整齐而补造 source-level work identity。

## 8. 经验验证边界

本协议解决的是 provenance、reading、normalization 与 queue semantics。

它不回答：

- 书中规则是否现实有效；
- 某派理论是否正确；
- 某案例是否具有预测力；
- 某 work family 是否优于其他方法。

所有这些问题仍需要独立、反馈前冻结、允许失败的 prospective testing。
