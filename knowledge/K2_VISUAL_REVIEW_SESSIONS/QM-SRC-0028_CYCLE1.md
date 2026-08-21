# QM-SRC-0028 Cycle 1 Supplemental Visual Review

Status: VISUAL_FIDELITY_REAUDIT_COMPLETE / 71_OF_71 / NO_DUPLICATE_READING_CREDIT / EMPIRICAL_OPEN

Date: 2026-08-21

## Source lock

- source_id: `QM-SRC-0028`
- work_id: `WORK-000018`
- title: `善天道-奇门遁甲讲义71页`
- registered pages: `71`
- readability: `TEXT_OK`
- canonical SHA256: `bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243`
- copyright boundary: `FORBIDDEN_TO_PACKAGE`

Canonical local bytes were hash/page-count checked against K1 before this review.

## Why this is a supplemental audit, not a second K2 Reading

Aggregate K2 already records this source as:

- `COMPLETE`
- `71/71`
- `TEXT_LAYER_FULL`
- `50` Evidence rows

Cycle 1 initially attempted to create a new `PARTIAL 22/71` shard after original-page inspection. CI #287 correctly rejected that architecture because the same source would exist in both aggregate base and per-book shard.

The failed attempt is retained as an audit lesson:

`TEXT_LAYER_COMPLETE != VISUAL_FIDELITY_AUDITED`

but also:

`SUPPLEMENTAL_VISUAL_AUDIT != SECOND_READING_VOTE`.

The duplicate Reading/Evidence shards were removed. This file records the visual correction layer without double-counting coverage or evidence independence.

## Review integrity

- original-page visual inspection: DONE p1-p71
- text extraction: navigation/comparison aid only during this supplemental audit
- old secondary note used as source substitute: NO
- raw copyrighted page reproduction committed: NO
- source typo silently repaired: NO
- Empirical Support added from source repetition or author anecdotes: NO
- runtime deity/setup/state choice changed because of this source: NO

## Full visual findings

### A. Source-internal anti-template statements are real but limited

p4-p7 explicitly restrict single-factor use of time labels and simple生克吉凶. p25 describes the symbols as an interacting information system. These are source-level arguments for contextual combination, not evidence that any particular contextual model predicts reality.

### B. The carrier contains visible corruption/editorial defects

Original-page review exposes several problems that a clean text extraction can hide or normalize psychologically:

- p27 contains a visibly corrupted phrase around the number of Qimen systems; its eight-door table also has anomalous header/element entries;
- p29 prose/table naming around 天英 is inconsistent;
- p35 a 三奇升殿 example is mislabeled relative to the same paragraph's own classification;
- p33 calls the catalogue 四十格 while p46 adds 第四十一;
- p53-p55 contain damaged/mismatched branch, element and solar-term teaching material;
- p55 contains a date/solar-term example that is internally incompatible.

Classification: `SOURCE_TEXT_CORRUPTION / SOURCE_INCONSISTENCY`.

Policy: preserve the printed anomaly and, where needed, separately record a correction hypothesis. Do not silently rewrite the source into the expected traditional form.

### C. Deity lineage is internally contradictory

p31 and p55 do not yield one clean mapping between 勾陈/朱雀 and 白虎/玄武. p31 also presents an incomplete 阳遁 sequence despite speaking of 八神.

The project may continue to freeze `deity_system` before prediction to stop post-outcome switching, but the source does not justify treating the present enum split as a solved historical taxonomy.

Status: `SOURCE_INTERNAL_CONFLICT / DEITY_LINEAGE_UNRESOLVED`.

### D. Pattern definitions are conditional structures, not flat phrases

p33-p42 repeatedly require旬别, ordered heaven/earth stems, gate, deity and palace conditions. 青龙返首 and 飞鸟跌穴 are explicit examples where a superficial stem-pair match is insufficient.

This supports the engineering direction of Pattern Registry + ordered relation + context fields. It still does not validate the predicted worldly outcome attached to the pattern.

### E. The book has multiple editorial/method layers

Signals include:

- duplicate chapter numbering around p46/p49;
- p49-p50 introduction of 暗藏飞干 after the earlier plate-building chain;
- p52-p55 insertion of generic五行/节令/十二长生 material;
- p55 onward `万物类象（新）` with modern institutions/objects;
- p68-p71 repetition of earlier占事 material.

Therefore the source should not be flattened into one homogeneous “善天道体系”. Candidate layers:

`STANDARD_PLATE / HIDDEN_FLYING_STEM_AUX / SYMBOLIC_LEXICON / APPLIED_ROLE_MAP / HIGH_RISK_SOURCE_CLAIMS`.

### F. Symbolic richness creates a falsifiability problem

p59 onward explicitly treats Qimen as a large image-symbol language and emphasizes memory plus imagination in interpretation. This is useful evidence against rigid single-symbol templates, but it also creates a large post-hoc search space: one symbol can be mapped to many people, objects, organs, institutions and events.

Research consequence:

`contextual interpretation` must not mean `unbounded narrative freedom`.

Candidate refinement: `Semantic Expansion Penalty / Symbolic Degrees-of-Freedom Budget`.

Only meanings/roles/features frozen before outcome feedback can enter scoring. Broad lexicons should face stronger negative controls and complexity penalties, not higher confidence.

### G. High-risk claims are source evidence only

p51-p71 includes medical diagnosis/prognosis, death, litigation, criminal identification, guilt, weapon, direction and other high-risk deterministic claims.

Classification:

`HIGH_RISK_SOURCE_CLAIM / RESEARCH_ONLY / NOT_EMPIRICAL_SUPPORT`.

They are not used for real-world medical, legal or criminal factual decisions.

### H. Repetition inside the same book is not corroboration

Later sections repeat earlier role maps and predictions. Same-source repetition does not create an independent vote and must not increase evidence strength.

Rule:

`INTRA_SOURCE_REPETITION != INDEPENDENT_SUPPORT`.

## Existing Evidence rows requiring visual caution

The base 50-row TEXT_LAYER evidence remains the canonical K2 Evidence set. The visual audit does not create duplicate rows. Instead, the following classes need caution when used downstream:

- deity naming/movement rows: preserve p31/p55 conflict and do not normalize aliases;
- fixed pattern rows: require all printed trigger conditions, not keyword matching;
- 五不遇时 / 门迫宫迫 rows: retain source-specific wording and cross-source conflict status;
- symbolic lexicon/applied role-map rows: candidate semantics only, no independent empirical support;
- high-risk disease/crime/legal rows: research-only;
- repeated late-book rules: no additional source weight.

A future correction pass may amend individual base Evidence notes/status where the visual anomaly materially changes the normalized fact. That pass must preserve evidence IDs and audit history rather than replacing the source silently.

## Self-audit lessons

### 1. Completion semantics were too coarse

The old contract correctly meant “full TEXT_LAYER review completed”, but in practice the label `COMPLETE` encouraged a stronger mental inference: “this book's source fidelity is fully settled.” That inference was wrong.

We now keep the contractual Reading state while explicitly tracking visual fidelity as a distinct audit dimension.

### 2. Flexibility can overfit just as easily as rigidity

Earlier project mistakes included mechanical `symbol -> verdict`. The opposite mistake is `symbol -> unlimited associations -> persuasive story`.

Both are failures. The desired path is constrained contextual inference with frozen degrees of freedom.

### 3. A source can teach a useful reasoning discipline while containing unreliable content

The book's warnings against single-factor judgment and its relation-based examples are methodologically useful. Its typographical corruption, internally conflicting deity mappings and unsupported concrete predictions show why usefulness must be decomposed into:

`Source Fidelity / Structural Usefulness / Applicability / Empirical Support`.

No one dimension substitutes for another.

## Test obligations generated by this audit

1. non-Jiazi full star/door/deity rotation against p21-p22 worked plates;
2. wrong-bureau / wrong-setup / wrong-boundary controls;
3. shuffled Role Map and shuffled symbolic-lexicon controls;
4. restricted-lexicon vs broad-lexicon comparison to measure narrative rescue capacity;
5. deity p31 vs p55 lineage/context analysis without outcome-based selection.

If wrong structures still produce equally persuasive narratives, that is evidence of excessive interpretive degrees of freedom, not model strength.

## Theory status

No version bump.

Current contribution is a constraint refinement inside v0.3-alpha:

`context -> frozen role/features -> relation/pattern -> competing branches -> semantic DoF budget -> prediction -> negative control -> outcome audit`.

No accuracy gain is claimed.

## Close condition

Visual fidelity audit is complete. Cycle 1 itself remains in distillation/testing until affected Evidence notes are triaged and at least one generated implementation/negative-control obligation is executed.
