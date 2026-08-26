# K2 Per-Book Completion Protocol

K2B is source-by-source work. The original Wave1 Ledger, Evidence and Book Distillate files were intentionally small at the start, but rewriting a growing monolithic JSONL file for every completed book creates avoidable transport risk and weakens review locality.

This protocol adds a **per-source shard overlay** without changing the meaning of the existing K2B contracts.

## 1. Authoritative aggregate

The authoritative K2B view is the union of:

- legacy base files:
  - `knowledge/K2_READING_LEDGER_WAVE1.jsonl`
  - `knowledge/K2_EVIDENCE_WAVE1.jsonl`
  - `knowledge/K2_BOOK_DISTILLATES_WAVE1.jsonl`
- plus sorted per-source shards:
  - `knowledge/K2_READING_LEDGER_WAVE1.d/*.jsonl`
  - `knowledge/K2_EVIDENCE_WAVE1.d/*.jsonl`
  - `knowledge/K2_BOOK_DISTILLATES_WAVE1.d/*.jsonl`

The base files remain valid accepted history. New source completions may be added as shards.

## 2. Source purity

A shard filename stem is the governed `source_id`, for example:

`knowledge/K2_EVIDENCE_WAVE1.d/QM-SRC-0016.jsonl`

Every row in that shard must have exactly the same `source_id`. A reading shard and a distillate shard contain exactly one row. Evidence shards may contain multiple atomic Evidence rows.

A source already represented by a base Reading Ledger row may not introduce a second Reading shard. Evidence IDs, Reading IDs and Distillate IDs must be globally unique across base plus shards.

## 3. Existing contracts remain binding

Shard storage does not weaken any K2 rule:

- canonical source identity is still official K1 SHA256;
- Reading Credit requires actual project-side review;
- `COMPLETE` still requires full source coverage;
- Evidence locators must remain inside reviewed coverage;
- `VISUAL_REQUIRED` still requires `VISUAL_PAGE` verification;
- modern-book text is paraphrased and `verbatim_quote=null` by default;
- CASE_RECORD is a record, not empirical validation;
- Claim Extraction remains blocked during K2B;
- every COMPLETE book requires exactly one REVIEWED Book Distillate;
- Evidence != Distillate != Claim != Truth.

## 4. Hard aggregate gate

`tools/validate_k2_per_book_completion.py` is the authoritative aggregate completion gate.

It must:

1. load base files and all sorted shards;
2. fail on shard/source mismatch, duplicate IDs, duplicate Reading source rows, or malformed shard cardinality;
3. materialize an isolated aggregate view and run the existing K2 Evidence validator with `--force` so semantic issues produce a non-zero exit code;
4. validate Book Distillates against the aggregate Reading Ledger and aggregate Evidence set;
5. preserve `claim_extraction_blocked=true`.

The explicit `--force` aggregation is important: an informational `REVIEW_REQUIRED` printout with exit code 0 is not sufficient for CI acceptance.

## 5. Per-book closure

A book may be declared `COMPLETE / CLOSED / ACCEPTED` only when all applicable gates are closed:

`canonical bytes -> full reading -> Atomic Evidence -> Book Distillate -> provenance corrections -> aggregate validators/tests -> CI -> project acceptance`

A packet that is READY is not a read book. A read book without Evidence is not normalized. Evidence without a Book Distillate is not distilled. A distilled book with a known stale source identity is not fully closed.

## 6. Distillation purpose

Every book must leave a compact record of:

- what is structurally worth retaining;
- how its method actually selects and combines information;
- where its rules apply and stop applying;
- what the source cannot establish;
- internal/cross-source tensions;
- anti-patterns that increase hindsight freedom;
- concrete updates forced on the project methodology;
- hypotheses that can be tested prospectively;
- high-risk material excluded from direct operational use。

The purpose is not to make the corpus smaller. It is to make accumulated knowledge **more constrained, auditable and falsifiable** as the corpus grows.

## 7. Composite carrier exception

“source-by-source”描述的是通常路径，不等于 `one source_id = one work` 的本体论断言。

如果完整阅读证明一个 canonical carrier 内含多个作品，则在任何 author/domain/lineage/Evidence 升格前必须先执行：

`canonical carrier -> full visual reading -> K2_SOURCE_SEGMENTS -> work-scoped attribution`

此时：

- `knowledge/K2_SOURCE_SEGMENTS.jsonl` 是页段归属的先决事实层；
- 不允许把 carrier 文件名中的作者传播到未署名的 embedded work；
- 不允许把载体路由领域传播到所有页段；
- 不允许为了满足 legacy `source_id -> work_id` schema 而把 composite carrier 强行塞入单一 work_id；
- 在 Evidence schema 尚未支持 segment binding 前，该 composite carrier 的正式 Evidence normalization 保持阻塞。

也就是说，**已读完整载体但结构被证明为 composite** 时，正确动作不是假装旧 per-source contract 足够，而是先修正知识模型。