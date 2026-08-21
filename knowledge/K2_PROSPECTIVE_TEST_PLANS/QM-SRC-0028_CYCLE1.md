# QM-SRC-0028 Cycle 1 — Test Plan

Status: TEST_A_A2_IMPLEMENTED / TEST_B-D_OPEN / NO EMPIRICAL CREDIT

Date: 2026-08-21

Source: `QM-SRC-0028 / WORK-000018 / 善天道《奇门遁甲讲义71页》`

Purpose: convert the full visual re-audit into tests that can fail. This plan does not validate the book, the project theory, or divination efficacy.

## Test A — Worked-plate implementation fidelity

Question: does an explicit source-defined implementation reproduce the source's p21-p22 worked plate structures beyond chief identity, while materially outperforming wrong or permuted structural inputs?

Before running, freeze:

- source-defined setup method;
- solar-term/yuan interpretation;
- time boundary;
- yin/yang bureau;
- star/door/deity system;
- center-host rule;
- expected palace-level star/door/deity placements transcribed independently from original-page review.

Positive controls: the two source worked plates.

Negative-control families:

- wrong bureau / shifted bureau;
- wrong hour while keeping the same bureau;
- wrong time-boundary variant **only when a genuine boundary witness exists**;
- permuted star/door/deity placements;
- alternative center-host assumption;
- broader shuffled full-chart controls.

Pass condition: correct source configuration must match independently reviewed expected structure and materially outperform negative controls. A test that only confirms an identity derived by the same implementation path is insufficient.

Failure classes: `PAIPAN_ERROR / SETUP_METHOD_ERROR / TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / ORACLE_ASSOCIATION_ERROR / REPRESENTATION_ERROR`.

## Test A result — milestone A1

Implementation commit:

`fb54b40f25d96ec97c29d45e2227121db664c29f`

Exact-head CI:

`Knowledge Engine V1 CI #294 = completed / success`.

What changed:

- production exposes `SHANTI_DAO_71_P21_P22` while retaining `LEGACY_EXPERIMENTAL` as the A/B baseline;
- source profile uses the book's five-day甲/己符头元 logic rather than silently replacing legacy `yuanOf()`;
- `PALACE_NUMBER_SEQUENCE` and `OUTER_ROTATION_RING` became different executable objects;
- `天禽` is represented as rotating with `天芮` in this profile;
- value-door target is calculated by xun-hour offset with Yang forward / Yin reverse through 1..9, then the eight-door wheel is aligned on the outer ring;
- deity movement starts from the chief-star destination and follows Yang-forward / Yin-reverse outer-ring motion.

Positive comparison covers sparse, non-Jiazi star/door/deity anchors from:

- p21 `1995-06-11 09:30 / 丁巳 / 芒种中元 / 阳遁三局`;
- p21-p22 `1995-08-13 20:00 / 戊戌 / 立秋下元 / 阴遁八局`.

A deliberate wrong-bureau control is rejected.

## Test A result — milestone A2

Negative controls were expanded in later commits.

### A2.1 Hidden-Jia representation failure

CI #298 exposed a real implementation defect while exercising a center-door fail-closed case: literal `甲` was searched directly in the earth-plate map even though the earth plate stores the current xun's hidden `遁干`.

Classification:

`HIDDEN_JIA_REPRESENTATION_ERROR`.

Fix:

`甲时 -> 当前旬遁干表示 -> 地盘宫位`.

Commit:

`6decd61a7ed14741736a9b4668a7fe95cb1ebde0`

CI #299: `completed / success`.

This adds **Representation-Object Type Safety** alongside Sequence-Object Type Safety:

`linguistic token != stored plate token != movement object`.

### A2.2 Wrong-hour control

Commit:

`de6caab23aeada99fb682c495518e6fed0122cec`

For the p21 Yang-3 plate, the source configuration `丁巳` is compared with a deliberately wrong `丙辰` while keeping Yang-3 fixed.

The independently reviewed sparse oracle scores star/door/deity anchors. The correct hour must score strictly higher than the wrong hour.

This is a **wrong-time input** control. It is not a `wrong-time-boundary` control.

### A2.3 Permuted-layer control

The same commit deterministically shifts star, door and deity labels by different offsets on the outer ring. The permuted layers must score below the correct sparse visual oracle.

This checks that the test is not merely satisfied by any plausible-looking rotation.

### A2.4 Exact-head evidence

Exact head for A2:

`de6caab23aeada99fb682c495518e6fed0122cec`

`Knowledge Engine V1 CI #301 = completed / success`.

The run includes:

- knowledge/runtime contracts;
- `:ziwei-core:test`;
- `:app:compileDebugKotlin`;
- Windows K2 helper portability.

Implementation fidelity credit from Test A still does not create predictive Empirical Support.

## Test A scope boundary

This is **not** full closure.

Still open:

- genuine wrong-`time_boundary_system` controls around an actual boundary witness;
- broader shuffled-full-chart controls beyond deterministic outer-ring label shifts;
- alternative center-host assumptions backed by explicit source variants;
- cross-source comparison of the same non-Jiazi full-rotation object;
- whether the legacy profile should ever be deprecated.

If source-defined value-door counting lands exactly on center 5, current p21-p22 evidence does not independently settle a complete door wheel. The source profile therefore returns:

`SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED`

and leaves the door layer blank rather than inventing a host rule.

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

Current source-comparison result:

`UNRESOLVED / NO-OP`.

The comparison preserves at least these competing hypotheses:

- `ALIAS_WITH_CONTEXT`;
- `LAYERED_HIDDEN_DEITY`;
- `YIN_YANG_SUBSTITUTION`;
- `EDITORIAL_SYNTHESIS / MULTIPLE_METHOD_LAYERS`.

No runtime taxonomy change is justified yet. Existing deity-system labels remain anti-post-hoc freeze labels, not a solved historical lineage claim.

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

The strongest current innovation remains constraint of interpretive degrees of freedom plus executable object/representation discipline, not expansion of symbolic vocabulary.
