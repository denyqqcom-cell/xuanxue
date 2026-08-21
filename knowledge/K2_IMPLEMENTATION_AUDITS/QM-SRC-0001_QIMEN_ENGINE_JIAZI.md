# QM-SRC-0001 -> QimenEngine Implementation Comparison

Status: PASS / `IMPLEMENTATION_CHECKED` SCOPE = 36 TRACKED JIAZI SPARSE ANCHORS

Date: 2026-08-21

Implementation test commit: `86e0b37d31549c0b2c16154ab1b8b81d83ebe454`

Exact-head CI: Knowledge Engine V1 CI `#282` = `completed / success`

Scope: only the 36 tracked `甲子` anchors in `LIANG_18_BUREAU`. This is **not** a full-nine-palace validation and is not predictive validation.

## 1. Independent source inputs

Primary fixture witness:

- 梁湘润《奇门遁甲入门》
- source_id: `QM-SRC-0001`
- 18/18 bureau table bodies visually reviewed
- 18/18 fixtures previously `ANCHORS_VERIFIED`
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

- 善天道《奇门遁甲讲义》p19 visibly places center-5 / Tian-Qin in the Kun-2 hosting relation and associates that structure with Death Gate;
- p21-p22 visibly give center-5 examples where Tian-Qin is chief star and Death Gate is chief door.

This secondary source only corroborates the center chief-identity relationship. It does not promote the broader 善天道 system or its predictive claims.

## 2. Production implementation inspected

Production path:

`ziwei-core/src/main/kotlin/com/xuanxue/qimen/QimenEngine.kt`

Before the fix, the relevant logic was:

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

It was not classified as a source error.

## 4. Narrow implementation correction

The production change does **not** declare the full center-hosting algorithm verified.

It only changes chief identity resolution:

- palace 5 chief star -> 天禽
- palace 5 chief door -> 死门

The production `GATE_HOME` still has no independent fifth door seat.

Full eight-door rotation, full star rotation, deity rotation and non-Jiazi bureau-table cells remain experimental/unverified.

The code comments preserve this boundary explicitly.

## 5. Validation Independence design

The Kotlin regression test does not duplicate the fixture values in a second hard-coded oracle table.

It reads the tracked JSONL fixture directly and performs only narrow text normalization:

- `天衝 -> 天冲`
- `天輔 -> 天辅`
- traditional one-character door names -> production `X门` spelling

Production code under test and fixture oracle therefore remain separate artifacts.

Exact-head CI #282 ran `./gradlew --no-daemon :ziwei-core:test` and passed the tests covering:

1. all 18 Yang/Yin bureau rows positive comparison;
2. wrong-bureau negative control;
3. permuted star/door anchor negative control;
4. explicit bureau-5 `天禽/死门` regression.

The Windows K2 helper/visual portability job also passed in the same workflow run.

## 6. Why the fixture rows may now enter `IMPLEMENTATION_CHECKED`

Lifecycle evidence is now complete for the **tracked sparse-anchor scope**:

`source witness`
-> `main visual recheck`
-> `36 sparse anchors`
-> `ANCHORS_VERIFIED`
-> `production comparison`
-> `wrong-bureau/permuted negative controls`
-> `exact-head stable-core PASS`
-> `IMPLEMENTATION_CHECKED`

This upgrade means only:

> The production ground-plate/chief-identity path reproduces the 36 tracked Jiazi sparse anchors and rejects the defined wrong-bureau/permuted controls.

It does **not** mean:

- all cells of all 18 tables are implemented;
- the current door/star/deity rotation algorithm is source-correct;
- setup-method/time-boundary choices are correct;
- the Qimen chart predicts reality.

`Source Fidelity / Implementation Integrity != Predictive Validity`.

## 7. Remaining implementation debt

Even after the sparse rows are upgraded:

- complete door-wheel rotation semantics, especially center-host handling;
- complete Tian-Qin/Tian-Rui hosting across non-Jiazi times;
- full star rotation against source-defined cells;
- deity-system-specific rotation;
- boundary timestamp/setup-method A/B;
- wrong-time / shuffled full-chart controls.

These must not be silently granted by the sparse-anchor PASS.

## 8. Self-audit note

The most important Test F result was not that 36 anchors can pass. It was that the process first exposed two different failure modes:

1. reviewer/oracle error — the earlier one-bureau shifted source mapping;
2. implementation error — the center-palace chief door returned empty.

Keeping these failures separate is more valuable than reporting a single “100% correct” number. The project therefore records the error history and narrow scope instead of converting this result into a global Qimen-engine accuracy claim.
