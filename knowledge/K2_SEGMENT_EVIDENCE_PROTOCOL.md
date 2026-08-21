# K2 Segment-Bound Evidence Protocol

版本：2026-08-22
阶段：K2B / Deep Closure
状态：ACTIVE

## 1. 为什么不能继续只用 source_id

对 composite carrier，仅记录 `source_id` 会丢失作品归属：同一 PDF 的不同页段可能属于不同作者、不同 work、不同领域。

因此，来自 composite carrier 的正式归一化证据必须至少绑定：

`source_id + segment_id + work_family_key + locator`

Evidence 的归属粒度必须不粗于真实作品边界。

## 2. 数据文件

`knowledge/K2_SEGMENT_EVIDENCE.jsonl`

它记录已经经过完整视觉复核、并能落到已审定 segment 的 Atomic Evidence。当前它是 legacy Wave1 Evidence schema 的补充层，不通过伪造 source-level work_id 来冒充旧格式。

## 3. Credit 分层

每条记录强制区分：

- `source_credit = SUPPORTED`：原书确实支持这个来源描述；
- `empirical_credit = NONE`：K2 阅读本身不能证明现实有效；
- `claim_readiness`：只表示未来是否值得进入 Claim/Conflict/Test 阶段，不代表真伪。

因此：

`SOURCE SUPPORT != EMPIRICAL VALIDITY != TRUTH`

作者权威、年代、重复记载、案例数量都不能在本层提升 empirical credit。

## 4. Context discipline

如果一条规则依赖具体对象、宫位、五行、生克、时序、正卦/互卦/变卦或其他上下文，必须在 `normalized_fact` 中保留这种条件结构，不能压缩成固定吉凶词典。

看到“某物为吉/凶”时，优先记录它是**在什么组合下**被判吉凶，而不是把对象本身永久贴上标签。

## 5. Worked example 不是实验验证

古籍中的占例、异象例、事后记载即使叙述完整，也只证明作者如何运用自己的方法。

它们可以提供：

- METHOD CREDIT；
- APPLICATION-SCOPE CREDIT；
- HINDSIGHT-FREEDOM 风险信息。

不能直接提供：

- prospective accuracy；
- calibration；
- causal validity；
- real-world empirical credit。

## 6. Independent vote

Evidence 可以来自同一 work family 的不同 part，但 `independent_vote_key` 必须继承 segment-aware lineage 的 family key。

上下册可以增加 unique coverage，不能增加独立来源票数。

## 7. 当前迁移状态

在 legacy `K2_EVIDENCE_WAVE1.jsonl` 仍假设 source-level one-work identity 时，composite segment Evidence 先进入本文件并由独立 CI gate 验证。

未来 schema 迁移必须保留 `segment_id`、work-family vote collapse 和 empirical-credit separation；不得在迁移时重新压扁为 carrier-wide attribution。
