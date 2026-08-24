# Reference App Audit

Status: ACTIVE / DRAFT

This document records what may be learned from user-provided or user-authorized reference apps while keeping implementation provenance clean.

## 1. Reference discipline

Reference apps may be used to study:

- information hierarchy;
- screen flow and interaction density;
- which chart layers experienced users expect to see;
- field naming and grouping;
- black-box output comparison for the same input;
- regression fixtures when an output can be independently validated.

Reference apps must **not** be treated as proof that an occult rule is correct. Their proprietary source code, packaged assets, fonts, artwork, paid text, or other copyrighted implementation material are not imported into this repository.

The intended flow is:

`reference behavior -> observed requirement -> independent implementation -> source/fixture verification -> acceptance`

not:

`decompile -> copy implementation`.

## 2. Static reference already inspected

User-provided APK:

- `紫微斗數_6.1.7.apk`

Static inspection of its packaged string/data surface shows a mature Ziwei information architecture containing concepts such as:

- 先天命盤;
- 专业盘 / 排盘设置;
- 四化盘;
- 飞星盘;
- 大限 / 大限流年;
- 流年 / 流月 / 流日;
- 命主 / 身主;
- 十二长生.

Its packaged `XingYaoDescription.json` also organizes Ziwei around the twelve palaces, body palace, stars and transit layers. That material is used only to identify expected information layers, not copied into the app's interpretation corpus.

## 3. Current xuanxue coverage after PR #12 work

### Ziwei

Current implementation already exposes an independent natal-chart surface with:

- 12-palace chart around a center summary;
- heavenly stem / earthly branch per palace;
- major, minor and adjective stars;
- brightness and four-transform markers when present in the core model;
- decadal ranges and age lists;
- Changsheng / Boshi / Suiqian / Jiangqian layers in detail;
- soul/body and soul/body palace summary.

Current core does **not** yet expose independently verified annual/monthly/daily transit chart generation equivalent to mature apps' 流年 / 流月 / 流日 screens. Those modes must not be faked in the UI before the model and fixtures exist.

### Qimen

The chart-first 3x3 Luo Shu surface is restored. In the next correction pass the baseline analysis layer is being separated from still-unverified rotation logic:

- day void and hour void are preserved separately;
- horse star is derived from the **hour branch**, not the day branch;
- the source example `2016-12-02 17:48` is locked as a regression fixture for 戊午日 / 辛酉时 / 子丑日空时空 / 亥马星;
- star/gate/deity rotation still requires fuller golden-chart verification.

## 4. Moto X30 Pro reference capture plan

The user's Moto X30 Pro contains installed reference apps for Ziwei, Bazi, Qimen, almanac/calendar, Liuyao and Fengshui. When the phone control connector is available, capture should proceed per app as a black-box audit:

1. inventory user-installed packages and resolve app labels;
2. record package/version metadata;
3. launch the app without logging into private accounts unless explicitly authorized;
4. capture the home screen and primary chart entry flow;
5. for a fixed public test input, capture the resulting chart screen;
6. collect UI hierarchy/text labels when technically available;
7. record the visible information layers and interactions;
8. compare those observations with xuanxue's screen/model coverage;
9. only when needed, pull the installed base APK for static structure inspection;
10. never import proprietary code/assets into xuanxue.

For each domain the result should be a `reference -> current -> gap -> independently implemented fix -> fixture/CI -> physical-device acceptance` chain.

## 5. Priority order

1. Qimen correctness blockers that can already be source-locked.
2. Ziwei professional-chart information hierarchy and missing transit model boundaries.
3. Bazi chart density, hidden stems / ten gods / luck-cycle presentation.
4. Liuyao six-line chart structure and moving-line information hierarchy.
5. Huangli / calendar date-navigation and day-detail structure.
6. Fengshui only after its domain model and evidence boundary are explicit.

## 6. Acceptance rule

A reference app can tell us **what a mature product exposes**. It cannot, by itself, tell us **what is true**.

A change is accepted only when the implementation is ours, the underlying calculation has an auditable source or fixture, automated checks pass, and the Moto X30 Pro visual/interaction check passes when the change is UI-facing.
