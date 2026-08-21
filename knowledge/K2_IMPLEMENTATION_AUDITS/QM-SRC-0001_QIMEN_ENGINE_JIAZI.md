# QM-SRC-0001 -> QimenEngine Implementation Comparison

Status: PRE_CI / NOT_YET_IMPLEMENTATION_CHECKED

Date: 2026-08-21

Scope: only the 36 tracked sparse `甲子` anchors in `LIANG_18_BUREAU`. This is **not** a full-nine-palace validation and is not predictive validation.

## 1. Independent source inputs

Primary fixture witness:

- 梁湘润《奇门遁甲入门》
- source_id: `QM-SRC-0001`
- 18/18 bureau table bodies visually reviewed
- 18/18 fixtures `ANCHORS_VERIFIED`
- each fixture contains:
  - `MAIN_TABLE/甲子/TOP_STAR_HEADER`
  - `MAIN_TABLE/甲子/BOTTOM_DOOR_FOOTER`

Tracked bureau-specific source pairs:

- 1 -> 天蓬 / 休
- 2 -> 天芮 / 死
- 3 -> 天衝 / 傷
- 4 -> 天輔 / 杜
- 5 -> 天禽 / 死
- 6 -> 天心 / 開
- 7 -> 天柱 / 驚
- 8 -> 天任 / 生
- 9 -> 天英 / 景

Secondary targeted visual cross-check, **not granted K2 Reading/Evidence credit in this task**:

- 善天道《奇门遁甲讲义》p19 visibly states the Kun-2 relation includes center-5 / Tian-Qin and corresponds to Death Gate;
- p21-p22 visibly gives a center-5 example where Tian Qin is chief star and Death Gate is chief door.

This secondary source only corroborates the center chief-identity relationship. It does not promote the broader 善天道 system or its predictive claims.

## 2. Production implementation inspected

Production path:

`ziwei-core/src/main/kotlin/com/xuanxue/qimen/QimenEngine.kt`

Before this comparison, the relevant logic was:

- ground plate: `戊` begins at `ju` and yin/yang controls forward/reverse placement;
- `dunPalace` = palace containing the current旬首遁干;
- chief star = `STAR_HOME[dunPalace]`;
- chief door = `GATE_HOME[dunPalace]`;
- `GATE_HOME` had no palace-5 entry.

For `甲子`, `dunGan=戊`, so the sparse fixture path reduces to:

`bureau -> 戊落该宫 -> chief star/door identity`

## 3. Pre-fix comparison result

Against 18 fixture rows:

- ground-plate `戊落局数宫`: structurally consistent with current implementation;
- chief-star identity: 18/18 source anchors matched after narrow traditional/simplified typography normalization (`衝/冲`, `輔/辅`);
- chief-door identity: 16/18 matched;
- both Yang-5 and Yin-5 failed because production returned an empty chief door for center palace 5, while source anchor is `死`.

Observed mismatch class:

`IMPLEMENTATION_GAP / CENTER_CHIEF_DOOR_IDENTITY`

Not classified as source error.

## 4. Narrow implementation change under test

The proposed change does **not** declare the full center-hosting algorithm verified.

It only changes chief identity resolution:

- palace 5 chief star -> 天禽
- palace 5 chief door -> 死门

The production `GATE_HOME` still has no independent fifth door seat.

Full eight-door rotation, full star rotation, deity rotation and non-Jiazi bureau-table cells remain experimental/unverified.

The code comment explicitly preserves this boundary.

## 5. Validation Independence design

The new Kotlin test does not duplicate the fixture values in a second hard-coded oracle table.

It reads the tracked JSONL fixture directly and performs only narrow text normalization:

- `天衝 -> 天冲`
- `天輔 -> 天辅`
- traditional one-character door names -> production `X门` spelling

Production code under test and fixture oracle therefore remain separate artifacts.

Tests cover:

1. all 18 Yang/Yin bureau rows positive comparison;
2. wrong-bureau negative control;
3. permuted star/door anchor negative control;
4. explicit bureau-5 `天禽/死门` regression.

No fixture row may be upgraded to `IMPLEMENTATION_CHECKED` until the exact-head CI containing these tests succeeds.

## 6. What a PASS would mean

A PASS would mean only:

> The production ground-plate/chief-identity path reproduces the 36 tracked Jiazi sparse anchors and rejects the defined wrong-bureau/permuted controls.

It would **not** mean:

- all cells of all 18 tables are implemented;
- the current door/star/deity rotation algorithm is source-correct;
- setup-method/time-boundary choices are correct;
- the Qimen chart predicts reality.

`Source Fidelity / Implementation Integrity != Predictive Validity`.

## 7. Remaining implementation debt even after PASS

- complete door-wheel rotation semantics, especially center-host handling;
- complete Tian-Qin/Tian-Rui hosting across non-Jiazi times;
- full star rotation against source-defined cells;
- deity-system-specific rotation;
- boundary timestamp/setup-method A/B;
- wrong-time / shuffled full-chart controls.

These must not be silently granted by a sparse-anchor PASS.
