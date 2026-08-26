# K2 Deep Reading Ledger Protocol

版本：2026-08-22
阶段：K2B / Deep Closure
状态：ACTIVE

## 1. 目的

Wave1 Reading Ledger 是按既有 source-level lineage/selection 规则生成的执行集合。完整研读过程中，项目可能先发现某些 source 的旧 metadata/lineage 不足以表达真实载体结构。

此时不能因为旧 schema 尚未迁移，就丢失已经真实完成的阅读，也不能反过来伪造旧 lineage 让它进入 Wave1。

因此增加：

`knowledge/K2_DEEP_READING_LEDGER.jsonl`

它只记录**项目主 Agent 已经实际完成的 carrier-level 阅读覆盖**。

## 2. Reading Credit 与 Attribution Credit 分离

Reading Ledger 只回答：

- 是否真的看过原始页；
- 看了哪些页；
- 用什么 verification mode；
- carrier 是否被识别为 composite。

它不回答：

- 整个 carrier 属于哪个作者；
- 整个 carrier 属于哪个 domain；
- 某理论是否正确；
- 是否具有 empirical validity。

因此：

`READING CREDIT != ATTRIBUTION CREDIT != EVIDENCE CREDIT != TRUTH`

## 3. Composite carrier

若 source 已进入 `K2_SOURCE_SEGMENTS.jsonl`：

- `binding_mode` 必须是 `SEGMENTED_CARRIER`；
- `segment_ids` 必须精确列出该 carrier 的全部 reviewed segments；
- source-level COMPLETE 只表示 carrier 每页均已视觉复核，不允许把某 segment 的作者/domain 传播到其他 segment。

未分段 source 使用 `binding_mode=SOURCE`，`segment_ids=[]`。

## 4. COMPLETE 的含义

对于有固定 PDF 页数的 source：

- page_start 必须为 1；
- page_end 必须等于 canonical pages；
- pages_reviewed_count 必须等于 canonical pages；
- `verification_mode=VISUAL_PAGE` 才能声明本层视觉 COMPLETE。

READY packet、OCR、摘要、旧笔记均不能产生 Reading Credit。

## 5. 与 Wave1 的关系

Deep Reading Ledger 是补充审计层，不改变 `K2_EVIDENCE_STATE.expected_wave1_reading_units`，也不把 source 自动加入 Wave1。

待 source metadata、segment lineage 和 evidence schema 完成迁移后，可显式迁入统一 Reading/Evidence 模型；迁移前保留原始 reading provenance。
