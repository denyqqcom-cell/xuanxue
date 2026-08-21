# QM-SRC-0028 Cycle 1 — 八神谱系对照审计

Status: TEST_C_SOURCE_COMPARISON / UNRESOLVED / NO_RUNTIME_CHANGE / NO_EMPIRICAL_CREDIT

Date: 2026-08-21

Purpose: test whether the current project can legitimately collapse `勾陈/朱雀` and `白虎/玄武` into aliases, yin/yang substitutions, hidden layers, or separate systems. The answer is currently **no**.

## 1. Witnesses are not equal

### A. QM-SRC-0001 / 梁湘润《奇门遁甲入门》

Verification: `VISUAL_PAGE`, full-book review complete.

The source-level deity list uses:

`值符 / 螣蛇 / 太阴 / 六合 / 勾陈 / 朱雀 / 九地 / 九天`.

This is a direct witness for a `勾陈/朱雀` naming family. It does not explain whether later `白虎/玄武` usage is aliasing, substitution or another layer.

### B. QM-SRC-0028 / 善天道《奇门遁甲讲义71页》 p19-p20

Verification: base TEXT_LAYER evidence + supplemental original-page visual re-audit.

The plate-building section associates the modern eight-deity sequence with `白虎/玄武` while parenthetically/structurally connecting them to `勾陈/朱雀`. The same section also records more than one small-chief movement doctrine.

This supports a relationship between the name pairs, but not a unique relationship type.

### C. QM-SRC-0028 p31

Verification: supplemental original-page visual re-audit.

This page says yin- and yang-escape deity ordering differs and further states that the yang-side `勾陈/朱雀` become `玄武/白虎` on the yin side. But the printed yang sequence on the same page is visibly incomplete despite the prose speaking about eight deities.

Classification:

`SOURCE_INTERNAL_CONFLICT / CORRUPTED_OR_INCOMPLETE_SEQUENCE`.

This page cannot by itself establish a clean executable mapping.

### D. QM-SRC-0028 p55

Verification: supplemental original-page visual re-audit.

A later teaching layer lists the eight deities as `值符、腾蛇、太阴、六合、白虎、玄武、九地、九天` and describes `勾陈` as beneath/within the White-Tiger position and `朱雀` beneath/within the Black-Tortoise position.

That wording is not the same model as the simple p31 statement “yang name becomes yin name”.

### E. QM-SRC-0021 / 幺学声《奇门遁甲预测学》（现代应用技术）

Verification now has two layers:

- existing aggregate K2: `TEXT_LAYER_FULL`;
- targeted supplemental original-page review: PDF p54, p57, p69-p72 = `VISUAL_PAGE` for these inspected pages only.

Canonical PDF SHA256 was rechecked before visual review:

`e804e292b446821e40965caa012e51d256f9eb9317f8b9519bbf4baebdbf4dd9`.

The original pages visually confirm:

- a visible `白虎/玄武` sequence with `勾陈/朱雀` described as hidden/subordinate relations at those positions;
- fixed deity order with Yang clockwise / Yin counter-clockwise movement;
- separation of faster heaven-plate deity movement from a slower earth-plate deity cadence/application layer;
- a worked Yang-8 plate where the chief deity follows the chief-star destination and the remaining deities occupy the same outer-ring order used by the current implementation.

This is now a **visual** independent modern witness for the layered-hidden-deity hypothesis and for movement-layer/cadence separation.

It is stronger than the previous text-layer-only support, but it still does not prove that Liang's direct `勾陈/朱雀` list is merely an alias of the same historical system.

Detailed supplemental record:

`knowledge/K2_VISUAL_REVIEW_SESSIONS/QM-SRC-0021_TARGETED_ROTATION.md`.

## 2. Competing lineage hypotheses

The current evidence still permits at least four materially different models.

### H1 — ALIAS_WITH_CONTEXT

`白虎 ≈ 勾陈`, `玄武 ≈ 朱雀`, with naming selected by context.

Problem: p31 ordering/substitution language and p55 / QM-SRC-0021 hidden-layer language are not identical claims.

### H2 — LAYERED_HIDDEN_DEITY

`白虎` and `玄武` are visible deity positions while `勾陈` and `朱雀` are hidden/subordinate layers.

Support is now stronger because both Shantiandao p55 and visually reviewed QM-SRC-0021 p54/p57 use a layered formulation.

Problem: this still does not automatically explain Liang's direct `勾陈/朱雀` eight-deity list or Shantiandao p31's yin/yang substitution wording.

### H3 — YIN_YANG_SUBSTITUTION

The name pair changes with yin/yang escape.

Support: the explicit Shantiandao p31 statement.

Problem: the same p31 sequence is visibly incomplete/corrupted, while p55 and QM-SRC-0021 give a different relationship description.

### H4 — EDITORIAL_SYNTHESIS / MULTIPLE_METHOD_LAYERS

The 71-page carrier combines teaching material from more than one naming/movement lineage, so no single mapping should be inferred from the whole book.

Support: broader Cycle-1 evidence of duplicated chapters, method-layer shifts, source corruption and mixed symbolic material.

Problem: this is still a source-composition hypothesis, not demonstrated historical provenance.

## 3. Current decision

Result of Test C remains:

`UNRESOLVED`.

No runtime enum change is justified.

The existing project fields `GOUCHEN_ZHUQUE` and `BAIHU_XUANWU` remain useful **only as anti-post-hoc freeze labels**. They must not be described as a solved historical taxonomy.

No silent rules such as the following are allowed:

`白虎 = 勾陈` universally;

`玄武 = 朱雀` universally;

or

`阳遁必用勾陈朱雀、阴遁必用玄武白虎` universally.

## 4. Why stronger evidence still yields NO-OP

This round did produce a genuine evidence upgrade: one modern independent witness moved from text-layer-only support to targeted original-page visual support.

But evidence strength and hypothesis resolution are different questions.

The new pages strengthen H2; they do not eliminate H1/H3/H4 or explain Liang's direct naming family. Promoting H2 to universal runtime truth would therefore still be a post-source synthesis rather than a source-demonstrated conclusion.

The correct update remains a deliberate `NO-OP` on runtime taxonomy.

This is model-compression discipline in practice: stronger evidence may narrow uncertainty without forcing a new enum or rule.

## 5. New implementation value from the same visual review

QM-SRC-0021 p70-p72 also provides an independent worked plate for `2004-05-29 午时` with a displayed Yang-8 configuration and sparse palace placements.

That witness is now used separately as a cross-source implementation test. This is more discriminating than mere terminology agreement because it constrains:

`timestamp + bureau + xun leader + chief star/door + center host + outer rotation + deity positions`.

A pass can increase selected cross-source implementation confidence, but not predictive Empirical Support and not deity-lineage resolution.

## 6. Next discriminating evidence

Priority is now more specific. Another modern summary repeating `白虎/玄武` is low value. Useful next evidence should be:

1. an earlier/independent source with page-level verification and an explicit deity sequence **plus movement object**;
2. context showing whether names change by yin/yang, heaven/earth deity layer, or method family;
3. a worked plate from a genuinely different lineage where the disputed name pair has an unambiguous position;
4. provenance evidence strong enough to distinguish historical inheritance from later editorial synthesis.

Until such evidence exists, Test C remains open.

`Source Consensus != Lineage Resolution != Empirical Support`.
