# Engineering handoff standard

`handoff/` is the boundary between local research material and shippable App logic. One module per folder; do not mix systems.

The goal is not to copy books into Git. The goal is to turn locally reviewed material into a traceable engineering contract that another developer/AI can implement **without access to the original PDFs** and without silently inventing missing rules.

## Current module status

| folder | module | status |
|---|---|---|
| `qimen/` | 奇门遁甲 | first full handoff pack; full 九宫 golden boards still = 0 |
| `bazi/` | 八字 | handoff still required |
| `liuyao/` | 六爻 | handoff still required |
| `liuren/` | 大六壬 | handoff still required |

紫微 currently follows a different provenance path: Kotlin implementation parity against iztro fixtures + upstream notices.

Start qimen review at `qimen/HANDOFF_SUMMARY.md`, then `qimen/08_IMPLEMENTATION_HANDOFF.md` and `qimen/07_COPYRIGHT_GATE.md`.

## Required files for every new handoff module

A module is not allowed to upgrade its App maturity merely because code compiles or one book example matches. The local-corpus pass should produce:

1. `00_CORPUS_MANIFEST.md` — unique sources, duplicates, version/era, page/text-layer status, local-only paths and copyright status.
2. `01_SYSTEM_MAP.md` — system layers, terminology, school boundaries and dependency graph.
3. `02_ALGORITHM_SPEC.md` — only computable procedures; every step exposes inputs, outputs, conditions and school id.
4. `03_RULES.jsonl` — structured rules with `rule_id`, conditions, source ids, confidence, conflicts and `implementation_ready`.
5. `04_CONFLICTS.md` — unresolved school/source conflicts; do not average them into one fake consensus.
6. `05_FIXTURES.jsonl` — reproducible inputs + expected structural outputs + source + whether the case is retrospective.
7. `06_CASES.md` — retrospective / half-blind / blind cases separated; known-answer interpretation must not be reported as predictive accuracy.
8. `07_COPYRIGHT_GATE.md` — `ALLOW_IN_APP` / `RESEARCH_ONLY` / `FORBIDDEN_TO_PACKAGE`.
9. `08_IMPLEMENTATION_HANDOFF.md` — Kotlin packages, public API, config enums, unsupported-school behavior, errors and tests.
10. `09_OPEN_QUESTIONS.md` — missing evidence and unresolved implementation blockers.
11. `HANDOFF_SUMMARY.md` — counts, readiness, largest conflicts, copyright risk and next engineering tasks.

## Minimum release gates

A rule can enter an App core only when all of the following are true:

- provenance is explicit;
- the rule is independently rewritten as a procedure/data fact rather than copied modern prose;
- school/method is explicit where alternatives exist;
- inputs and outputs are executable;
- conflicts are either resolved by evidence or represented as configuration/unsupported state;
- at least one reproducible fixture exists for the exact algorithm path;
- no `MODEL_KNOWLEDGE_ONLY` item is used as a formal algorithm or golden fixture;
- `07_COPYRIGHT_GATE.md` marks the content as allowed in App.

A judgement/interpretation rule has an additional gate: it must state the **question/subject conditions** under which it applies. Generic symbol → generic conclusion rules are not implementation-ready merely because they are traditional.

## App integration rule

The App may expose three different layers, but they must never be conflated:

1. **Structure** — calendar/chart/hexagram/course fields produced by deterministic code.
2. **Selection** — 用神 / 类神 / subject-object choice, which depends on the concrete question and school.
3. **Interpretation** — scenario reasoning, counter-evidence, timing and confidence.

The current App has a `ReadingContext` gate for 奇门 / 六爻 / 大六壬. User-provided question and known facts are explicitly tagged as user context; they constrain the scenario but do not upgrade evidence maturity.

If a handoff only validates layer 1, the UI must stay at layer 1. Missing layer 2/3 evidence is not permission for the model to fill gaps from memory.

## Copyright boundary

Never commit/package original scans, full OCR, complete modern tables, long modern translations/annotations, commercial app copy, screenshots, fonts or artwork unless a separate license explicitly allows redistribution.

Ancient source text and a modern edition are not the same copyright object. Public-domain underlying text does not automatically make a modern scan, punctuation, translation, commentary, diagram or typesetting public domain.
