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

For source work **started on or after 2026-08-21**, a book may be declared `COMPLETE / CLOSED / ACCEPTED` only when all applicable gates are closed:

`canonical bytes -> Pre-Book Retrospective -> source-appropriate full reading -> Atomic Evidence -> Book Distillate -> conflict/anti-pattern review -> Method Delta -> prospective test plan -> provenance corrections -> aggregate validators/tests -> CI -> project acceptance`

For `VISUAL_REQUIRED`, “source-appropriate full reading” specifically means original-page visual review. A local render packet may precede that review, but packet creation is transport, not Reading Credit.

Earlier accepted books remain valid accepted history and are not retroactively invalidated solely because the Pre-Book Retrospective gate did not yet exist.

A packet that is READY is not a read book. A read book without Evidence is not normalized. Evidence without a Book Distillate is not distilled. A distilled book with a known stale source identity is not fully closed. A new book that was read without first auditing inherited assumptions is not methodologically closed under the post-2026-08-21 protocol.

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
- high-risk material excluded from direct operational use.

The purpose is not to make the corpus smaller. It is to make accumulated knowledge **more constrained, auditable and falsifiable** as the corpus grows.

## 7. Pre-Book Retrospective gate

`knowledge/K2_PRE_BOOK_RETROSPECTIVE_PROTOCOL.md` defines the required self-correction gate for every new book start after 2026-08-21.

Before full reading begins, the project must create one source-specific retrospective record under:

`knowledge/K2_PRE_BOOK_RETROSPECTIVES/<SOURCE_ID>.md`

The retrospective must review relevant historical failures, theory drafts, prospective validations and recent Book Distillates, then identify:

- inherited assumptions at risk;
- recurrent historical mistakes;
- rules that must be demoted or narrowed before the next source is consumed;
- hypotheses to watch for without predicting what the book will say;
- criteria that would force a theory change;
- criteria that are insufficient to force a theory change.

This gate exists to prevent K2 from becoming passive rule accumulation. It does not weaken source fidelity or Evidence requirements, and it does not allow project inference to be rewritten as source Evidence.

## 8. VISUAL_REQUIRED handoff gate

`knowledge/K2_VISUAL_PAGE_HANDOFF_PROTOCOL.md` governs SCAN / VISUAL_REQUIRED transport.

`tools/build_k2_visual_page_packet.py` may resolve canonical local bytes and render every PDF page to local-only PNG images. A successful result is only `READY_FOR_VISUAL_REVIEW` and must record `review_credit_granted=false`.

Rendered pages, original PDFs and visual packets remain outside the repository. The main reviewer must still inspect every registered page before `pages_reviewed_count` can reach the source page count or Reading can become COMPLETE.

For VISUAL_REQUIRED, the expanded closure segment is:

`canonical bytes -> local visual packet -> main-reviewer page-by-page visual review -> Atomic Evidence`

Rendering removes an access bottleneck; it does not lower the epistemic bar.
