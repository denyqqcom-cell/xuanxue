# K2 Qimen Epistemic Debt Protocol v1

Status: `ACTIVE / FAIL_CLOSED`

Purpose: turn past self-reflection into enforceable cognitive controls. This layer does **not** add divination rules, does not grant empirical credit, and does not reinterpret old learning logs as if they were prospective evidence. It asks a narrower question: **when a bias was already recognized, did the same epistemic failure later reappear under new wording or a new theory layer?**

## 1. Why this layer exists

The project already has provenance, lineage, Evidence, TBV, cognitive-error, scenario, counterfactual, sensitivity and prospective-validation controls. That is necessary but not sufficient.

A learning system can correctly describe its own bias and still repeat it later. A reflection note is therefore not proof that a bias has been corrected. The missing unit is **recurrence debt**: a machine-readable record linking an earlier known error to a later reappearance and blocking theory promotion until the debt is discharged under unknown-outcome tests.

The old learning logs remain historical artifacts. They are not silently rewritten. New controls supersede their promotion rules without erasing the record of how the earlier reasoning was formed.

## 2. Non-negotiable invariants

```text
SOURCE_FIDELITY != EMPIRICAL_VALIDITY
SELF_GENERATED_INFERENCE != EPISTEMIC_PRIVILEGE
KNOWN_OUTCOME_REPAIR != VALIDATION
CASE_COUNT != INDEPENDENCE
THREE_SUCCESSES != VALIDATION
UNCALIBRATED_WEIGHT != MODEL
TRADITIONAL_STATUS != IMMUNITY_FROM_FALSIFICATION
REFLECTION_RECORD != CORRECTION
RECURRENT_BIAS => PROMOTION_BLOCKED
NEGATIVE_EVIDENCE_IS_FIRST_CLASS
BASELINE_OR_COUNTERFACTUAL_REQUIRED
```

Interpretation:

- A rule can be faithfully attributed to a book while still having zero demonstrated real-world validity.
- An inference does not become more trustworthy merely because it was generated independently rather than copied from a source.
- A known-outcome failure may generate a new hypothesis; it cannot validate the repair proposed after seeing the result.
- A raw count such as three apparent successes says nothing by itself about independence, base rate, target difficulty, stopping rule, selection, contamination, or calibration.
- Numeric weights, half-discounts, priority scores and additive/multiplicative severity rules are parameters. They require predefined tests, baselines and ablation/counterfactual analysis; they are not upgraded by narrative plausibility.
- Traditional longevity is a provenance fact, not immunity from falsification. Gradual iteration may preserve a rule as a hypothesis, but a repeatedly failing rule must be downgradable or removable.
- Writing a self-critique does not close the issue. Closure requires a control that can detect recurrence and a prospective test that can fail.

## 3. Epistemic debt unit

Every row in `K2_QIMEN_EPISTEMIC_DEBT.jsonl` represents a second-order problem:

```text
known earlier bias
    -> later recurrence in a learning/theory artifact
    -> explanation of why the prior reflection failed to prevent recurrence
    -> promotion blocked
    -> explicit release requirements
```

A debt row is **not** an occult claim and has `empirical_credit = NONE`.

## 4. Release gate

No debt may move out of `PROMOTION_BLOCKED` merely because additional examples agree with it. Release requires all of the following to be designed before outcome access:

1. `predefined_protocol = true`
2. `unknown_outcome = true`
3. `independence_assessment = true`
4. `baseline_or_counterfactual = true`
5. `negative_evidence = true`
6. an explicit falsification rule
7. a sample-adequacy rule based on information quality, independence, target difficulty and stopping discipline rather than a magic case count
8. a theory-impact action specifying what will be downgraded, rewritten or removed if the test fails

For parameterized or weighted rules, an ablation or counterfactual must ask whether the proposed weight/component improves a predefined metric beyond a simpler baseline. If removing the component produces no meaningful deterioration, the component has not earned a place in the model.

## 5. Evidence-credit separation

The following credits must remain distinct. In particular, **source fidelity** means only that the source has been represented faithfully; it is not a synonym for empirical validity.

```text
SOURCE CREDIT
= we read and represented the source correctly

METHOD CREDIT
= we can reproduce the stated method/procedure

STRUCTURE CREDIT
= the model is internally specified and auditable

EMPIRICAL CREDIT
= unknown-outcome performance survived a predefined test
```

Only the last category can support empirical promotion, and this protocol grants none.

## 6. Negative evidence

A failed prediction, abstention failure, calibration miss, unstable mapping, non-improvement versus baseline, or failed ablation is not an embarrassment to be explained away. It is first-class model information.

Post-hoc reinterpretation is stored separately as hypothesis generation. It cannot overwrite the frozen prediction or original score.

## 7. Self-generated theory discipline

The project's long-term goal may include an internally generated theory. Internal generation does not lower the evidential bar; it raises it.

A new theory component must answer:

- What observation would make this component wrong?
- What simpler baseline does it beat?
- What changes when the component is removed?
- Which boundary conditions make it inapplicable?
- Which negative cases are retained rather than discarded?
- Does the same result survive an unknown-outcome, frozen procedure?

If these questions are unanswered, the component remains a hypothesis regardless of elegance, tradition, source count, or author confidence.

## 8. Relationship to existing controls

This protocol complements rather than replaces:

- `K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl`
- `K2_QIMEN_TBV_PROTOCOL.md`
- `K2_QIMEN_SCRM_V01.md`
- `K2_PROSPECTIVE_VALIDATION_PROTOCOL.md`
- `K2_QIMEN_PRACTICE_INPUT_INTEGRITY_PROTOCOL.md`

The cognitive-error ledger records *what kinds of errors exist*. The epistemic-debt ledger records *where a known error resurfaced after it had already been recognized*.

## 9. Current status

All current debt rows are blocked from theory promotion. `empirical_credit = NONE` remains mandatory. This protocol is an epistemic control shell, not evidence that Qimen has predictive validity.
