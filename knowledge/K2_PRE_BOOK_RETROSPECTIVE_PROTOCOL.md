# K2 Pre-Book Retrospective Protocol

Status: ACTIVE for every new per-book start after 2026-08-21.

## 1. Purpose

K2 must not become a pipeline that only reads more books and accumulates more rules. Before a new book is opened, the project must look backward at its own prediction logs, failed forecasts, previous distillates, theory drafts, implementation errors and validation records.

The objective is to detect whether the current method is already carrying stale assumptions, post-hoc repairs, over-generalized rules or source-authority bias into the next source.

This gate is deliberately separate from book reading. A new source is evidence about a model; it is not an authority that automatically replaces the model.

## 2. Required retrospective inputs

For the target domain, review at minimum:

1. the most recent complete Book Distillate(s);
2. prior self-reflection / failure-analysis records;
3. prospective validation records, including misses and unresolved cases;
4. current theory/method drafts;
5. implementation errors where the written rule and executable calculation diverged;
6. current operational rules that were promoted from only one or a few cases.

The retrospective must identify recurrent error families, not merely repeat old lists.

## 3. Mandatory questions

Before reading the next book, answer:

- Which current rules came from a single dramatic success or failure?
- Which rules confuse `source says X` with `X is empirically supported`?
- Which rules were repaired after feedback and then promoted as if pre-registered?
- Which fixed priorities are actually scenario-, layout-, time-family- or method-family-specific?
- Which interpretation devices increase narrative freedom without increasing falsifiability?
- Which external facts, news, appearance, prior history or auxiliary methods can contaminate attribution?
- Which 'validation' thresholds are merely convenient numbers rather than evidence of robustness?
- Which claimed system limitations are actually untested explanations for a miss?
- Where has implementation drifted from the documented method?

## 4. Epistemic separation

From this protocol forward, at least four layers must remain distinct:

- **SOURCE**: what a source explicitly states or demonstrates;
- **INFERENCE**: project-side interpretation, abstraction or situational translation;
- **EMPIRICAL_SUPPORT**: prospective or otherwise independently testable evidence;
- **CONTAMINATION**: information that could improve an answer while preventing clean attribution to the method being tested.

Direct support from a book raises Source Fidelity only. It does not, by itself, raise Empirical Support.

## 5. Rule lifecycle

Rules do not move directly from `BOOK -> TRUE` or `CASE -> VERIFIED`.

Use the lifecycle:

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

and allow destructive revision:

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`.

Gradual iteration means versioned, evidence-traceable change. It does **not** mean every previous rule must be preserved forever.

## 6. Prediction Protocol Freeze is not Theory Freeze

Prediction Protocol Freeze applies within one prediction episode. Before outcome feedback, freeze all applicable choices that would otherwise create hindsight freedom, including question classification, setup method, layout/time family, role map, eligible rule set, allowed auxiliary information and interpretation branches.

Theory evolution operates across books and across prospectively scored cases. Strong counter-evidence may narrow, revise, deprecate or reject frozen components for future predictions.

A frozen prediction cannot be retroactively edited into a hit. A frozen theory is not required.

## 7. Counterexample handling

A conflicting source statement or one surprising case does not immediately replace the current method.

First classify the relation:

- `SUPPORTS`
- `CONTRADICTS`
- `NARROWS`
- `ORTHOGONAL`
- `CONTEXT_SPLIT_REQUIRED`

Then test whether the apparent conflict shares the same question class, layout method, time family, role definition and auxiliary-information policy.

Only after this normalization may the conflict produce a method update or a prospective hypothesis.

## 8. Narrative control

Situational reasoning and narrative coherence may help generate hypotheses, but a coherent story is not evidence.

When multiple interpretations are plausible, record the competing branches **before** feedback. Do not select the branch that best matches the known result and then count it as a hit.

Each important branch should state:

- prerequisite assumptions;
- discriminating observations;
- failure conditions;
- what outcome would favor a rival branch.

## 9. Validation discipline

`>=3` prospective cases is only a minimum signal threshold, not proof of validity.

Promotion beyond PROVISIONAL should consider:

- pre-registration before outcome feedback;
- independence of cases;
- baseline frequency / chance performance;
- misses as well as hits;
- negative controls or deliberately wrong inputs where feasible;
- auxiliary-information contamination;
- cross-method contamination;
- whether the rule survives a different scenario within its claimed applicability range.

## 10. Auxiliary-information ablation

If real-world context such as news, social background, appearance, external omen or another divination method is allowed, its role must be frozen in advance and scored separately.

Preferred evaluation structure when feasible:

1. produce a method-only interpretation;
2. freeze it;
3. add the auxiliary channel;
4. record the delta;
5. never attribute the auxiliary gain back to the original method.

## 11. Required artifact before a new book

Create one source-specific retrospective record before full reading begins. It must contain:

- inherited assumptions at risk;
- recurrent historical mistakes;
- rules to demote/narrow before reading;
- hypotheses to watch for in the new source;
- criteria that would force a theory change;
- criteria that would **not** be enough to force a theory change.

The record is a pre-reading checkpoint, not a prediction of what the book will say.

## 12. Closure relation

For new per-book work, the methodological chain is:

`Pre-Book Retrospective -> Full Reading -> Atomic Evidence -> Book Distillate -> Conflict/Anti-pattern Review -> Method Delta -> Prospective Test Plan -> Validators/Tests -> CI -> CLOSED`

The retrospective does not replace any existing K2 Evidence gate. It adds a self-correction gate before the project consumes another source.
