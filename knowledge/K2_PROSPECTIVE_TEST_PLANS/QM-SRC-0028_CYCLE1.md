# QM-SRC-0028 Cycle 1 — Test Plan

Status: TEST_A_IMPLEMENTED / TEST_B-D_OPEN / NO EMPIRICAL CREDIT

Date: 2026-08-21

Source: `QM-SRC-0028 / WORK-000018 / 善天道《奇门遁甲讲义71页》`

Purpose: convert the full visual re-audit into tests that can fail. This plan does not validate the book, the project theory, or divination efficacy.

## Test A — Worked-plate implementation fidelity

Question: does an explicit source-defined implementation reproduce the source's p21-p22 worked plate structures beyond chief identity?

Before running, freeze:

- source-defined setup method;
- solar-term/yuan interpretation;
- time boundary;
- yin/yang bureau;
- star/door/deity system;
- center-host rule;
- expected palace-level star/door/deity placements transcribed independently from original-page review.

Positive controls: the two source worked plates.

Negative controls:

- wrong bureau;
- shifted bureau;
- wrong time-boundary variant where applicable;
- permuted star sequence;
- permuted door sequence;
- alternative center-host assumption.

Pass condition: correct source configuration must match independently reviewed expected structure and materially outperform negative controls. A test that only confirms an identity derived by the same implementation path is insufficient.

Failure classes: `PAIPAN_ERROR / SETUP_METHOD_ERROR / TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / ORACLE_ASSOCIATION_ERROR`.

### Test A result — milestone A1

Implementation commit:

`fb54b40f25d96ec97c29d45e2227121db664c29f`

Exact-head CI:

`Knowledge Engine V1 CI #294 = completed / success`.

What changed:

- production now exposes an explicit `SHANTI_DAO_71_P21_P22` method profile while retaining `LEGACY_EXPERIMENTAL` as the default A/B baseline;
- the source profile uses the book's five-day甲/己符头元 logic rather than silently replacing legacy `yuanOf()`;
- `PALACE_NUMBER_SEQUENCE` and `OUTER_ROTATION_RING` are different executable objects;
- `天禽` is represented as rotating with `天芮` in this profile;
- value-door target is calculated by xun-hour offset with Yang forward / Yin reverse through 1..9, then the eight-door wheel is aligned on the outer ring;
- deity movement starts from the chief-star destination and follows Yang-forward / Yin-reverse outer-ring motion.

Positive comparison now covers sparse, non-Jiazi star/door/deity anchors from:

- p21 `1995-06-11 09:30 / 丁巳 / 芒种中元 / 阳遁三局`;
- p21-p22 `1995-08-13 20:00 / 戊戌 / 立秋下元 / 阴遁八局`.

A deliberate wrong-bureau control is rejected.

### Test A scope boundary

This is **not** full closure.

Still open:

- shifted-bureau / wrong-boundary / permuted-star / permuted-door controls beyond the first wrong-bureau control;
- any case where source-defined value-door hour counting lands exactly on center 5;
- p31/p55 deity-lineage conflict;
- cross-source comparison of the same full-rotation object;
- whether the legacy profile should ever be deprecated.

The source profile deliberately returns `SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED` rather than inventing a center-door host rule that p21-p22 do not independently settle.

Implementation fidelity credit from Test A does not create predictive Empirical Support.

## Test B — Semantic Degrees-of-Freedom / narrative-rescue control

Question: can broad symbolic lexicons produce equally persuasive explanations after the symbols are wrong?

For a future clean, low-risk, unknown-outcome case, create before outcome:

1. `RESTRICTED` model: only a small source-bound lexicon and frozen Role Map;
2. `BROAD` model: broader p55-p67 style symbolic lexicon, but all eligible meanings must still be enumerated/frozen ex ante;
3. `SHUFFLED_SYMBOL` negative control: symbol labels are permuted while keeping output format constant;
4. `SHUFFLED_ROLE_MAP` negative control: role bindings are permuted before interpretation.

All branches must have finite observable failure conditions. Human-readable “persuasiveness” is not the primary score.

Primary measurements:

- preregistered outcome discrimination;
- calibration / branch scoring;
- number of eligible symbolic meanings frozen before outcome;
- proportion of predictions rescued only by secondary/tertiary meanings;
- performance gap between correct and shuffled controls.

Candidate complexity signal:

`semantic_dof = eligible_meaning_count + role_map_alternatives + branch_count + timing_alternatives`

This is not yet a canonical scoring formula. It is a measurement field for model-compression research.

Falsification signal: if shuffled/wrong-symbol controls remain comparably discriminative, the symbolic layer is not demonstrating useful structure and should be narrowed/deprecated.

## Test C — Deity lineage separation

Question: are p31 and p55 describing aliases, yin/yang substitutions, different systems, or editorial inconsistency?

This is a source-lineage test, not an outcome test.

Procedure:

- preserve p31 and p55 as separate witnesses;
- compare surrounding method objects: plate method, yin/yang context, movement rule, list order, terminology;
- compare independent sources without assuming modern enum equivalence;
- do not choose the mapping based on which one improves a retrospective case.

Possible conclusions:

`ALIAS_WITH_CONTEXT / SYSTEM_VARIANT / EDITORIAL_CORRUPTION / UNRESOLVED`.

No conclusion may increase predictive Empirical Support by itself.

## Test D — Role-map specificity vs template lookup

Question: does problem-specific role mapping add discriminative value without becoming post-hoc freedom?

Future clean cases should freeze:

- question domain;
- primary role map;
- at most a small number of explicit alternative role maps;
- observable difference between alternatives;
- failure condition for each.

Compare:

`SOURCE_FIXED_TEMPLATE` vs `CONTEXT_FROZEN_ROLE_MAP`.

A context map only earns support if selected before outcome and shows stable improvement over matched prospective cases. Retrospective elegance is zero empirical credit.

## Safety / exclusion

Do not use disease diagnosis, death, criminal guilt/identity, legal liability or similar high-risk source claims as operational validation targets. Structural method research may abstract such passages into low-risk role/relationship questions, but the concrete high-risk verdict is excluded.

## Theory impact rule

No v0.4 from Test A or this plan alone.

A theory change requires prospective or broader implementation evidence that changes an operational claim. Expected lifecycle:

`CANDIDATE -> TESTABLE -> PROVISIONAL`, with reverse movement allowed.

The strongest current innovation remains constraint of interpretive degrees of freedom, not expansion of symbolic vocabulary.
