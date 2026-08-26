# K2B Per-Book Distillation Protocol

Every fully reviewed book/source carrier must be distilled. Reading coverage and Atomic Evidence are necessary but not sufficient for project acceptance.

This protocol is additive to `K2_EVIDENCE_PROTOCOL.md`. It does **not** unlock Claim Extraction and does not replace Atomic Evidence.

## 1. Why distillation exists

Atomic Evidence preserves what a source says. A book distillate records what the project learned **from reviewing that source as a whole** without promoting the source to truth.

The goal is to prevent two opposite failures:

- accumulating hundreds of disconnected rules without understanding the source's method structure;
- compressing a book into a confident doctrine that erases conditions, conflicts, failure modes, or source limitations.

A distillate is therefore a constrained synthesis layer between Evidence and later Claim work.

## 2. Hard gate: every COMPLETE book is distilled

For every Wave1 Reading Ledger row with `read_status=COMPLETE`, there must be exactly one row in:

`knowledge/K2_BOOK_DISTILLATES_WAVE1.jsonl`

A source may not be treated as fully closed/accepted if its complete reading has no reviewed distillate.

`PARTIAL`, `NOT_STARTED`, and `BLOCKED` rows must not receive a final book distillate.

## 3. Distillation is not Claim extraction

A distillate may summarize:

- the source's core structure;
- the method families it actually uses;
- applicability constraints and exceptions;
- internal tensions and cross-source conflict candidates already visible at Evidence level;
- source-quality limitations;
- anti-patterns exposed by the source or by case methodology;
- changes the source forces in the project's own reasoning model;
- hypotheses worth prospective testing;
- material that must stay excluded from operational use.

A distillate must not:

- assert that a traditional rule is empirically true merely because the book states it;
- convert author self-validation into project validation;
- count same-work variants as independent support;
- silently reconcile conflicting schools;
- rewrite a failed case into a success;
- use feedback-after-the-fact reinterpretation as evidence of predictive validity;
- unlock medical, death, legal, criminal, financial, election, war, or other high-risk predictions merely because the source contains them.

## 4. Required compression questions

Every reviewed source distillate must answer these questions in structured form:

1. **Essence** — what is the smallest set of ideas needed to understand this source?
2. **Method map** — how does the source actually move from question/setup to interpretation?
3. **Applicability** — where do its rules apply, and where do they stop applying?
4. **Source limitations** — what prevents this source from being treated as truth?
5. **Conflicts/tensions** — what internal or cross-source disagreements must remain unresolved for now?
6. **Anti-patterns** — what reasoning behavior should the project explicitly avoid learning from this source?
7. **Model updates** — what did this source force the project to change in its own method?
8. **Testable hypotheses** — what can later be prospectively tested with a frozen protocol?
9. **Operational exclusions** — what content must remain non-operational/high-risk despite being present in the book?

## 5. Evidence anchoring

Each distillate records:

- the source's accepted `evidence_count`;
- one or more `evidence_anchor_refs` belonging to that same source.

Anchor references are not a substitute for the full Evidence set. They are provenance handles showing that the distillate is downstream of reviewed Atomic Evidence rather than an unaudited free-form summary.

The validator requires the distillate `evidence_count` to match both the Reading Ledger and the actual Atomic Evidence count for that source.

## 6. Original-method learning rule

The project must not merely learn the books; it must learn from its own errors while reading them.

A book may therefore produce a `model_updates` item even when the update is negative, for example:

- reject a previously assumed global priority order;
- narrow a rule to a specific question topology;
- split two schools that had been wrongly merged;
- add a fail-closed gate against post-feedback role switching;
- downgrade a source-supported rule from operational use to a testable hypothesis.

This is deliberate. Distillation is the mechanism that converts source reading into gradual self-correction rather than passive accumulation.

## 7. Validation and later promotion

During K2B:

`Evidence != Distillate != Claim != Truth`

A distillate can propose `testable_hypotheses`, but empirical confidence can increase only through later prospective validation where setup, role map, eligible rule set, prediction, alternatives, and falsification conditions are frozen before outcome feedback.

Cross-source agreement raises textual support only. It does not by itself raise empirical validity.

## 8. Copyright boundary

Book distillates contain only independent project synthesis and short source/evidence identifiers. They do not package original pages, OCR text, long quotations, screenshots, or copyrighted source wording.

`copyright_class` is fixed to `DERIVED_SYNTHESIS_SAFE`.
