# QM-SRC-0028 p21-p22 Worked Plate → QimenEngine Implementation Audit

Status: IMPLEMENTATION_PATCH_CANDIDATE / SOURCE-BOUNDED / NO EMPIRICAL CREDIT

Date: 2026-08-21

Source: `QM-SRC-0028 / WORK-000018 / 善天道《奇门遁甲讲义71页》`

Scope: only the two visually re-audited worked plates on p21-p22 and the source-defined operations required to reproduce their sparse structural anchors. This is **not** a claim that the whole book is internally consistent, nor that this profile predicts reality.

## 1. Why this audit was necessary

The previous `QimenEngine` had already passed Liang Jiazi chief-identity anchors, but that scope did not test non-Jiazi full star/door/deity movement. The Cycle-1 source review supplied two worked plates that expose exactly those degrees of freedom:

- p21: 1995-06-11 09:30, source says `丁巳 / 芒种中元 / 阳遁三局`;
- p21-p22: 1995-08-13 20:00, source says `戊戌 / 立秋下元 / 阴遁八局`.

Both are non-Jiazi and therefore cannot be rescued by the earlier `甲子 -> 戊落局数宫 -> chief identity` shortcut.

## 2. Pre-patch implementation mismatches

Static comparison against the existing production path found five independent object/sequence conflations.

### A. 元的对象错了

Legacy `yuanOf()` grouped the day by the ten-day sexagenary xun base.

The source worked example instead takes the previous `甲/己` day as符头 and groups five-day元 by that符头地支. For `癸酉`, legacy and source-defined logic diverge:

- legacy ten-day xun chunk -> 上元;
- source p21 previous符头 `己巳` -> 中元.

Classification: `SETUP_METHOD_OBJECT_MISMATCH`.

### B. 九星旋转把“飞布数序”当成“外八宫转盘序”

Legacy star movement shifted all 9 stars over `1..9`.

p21-p22 instead rotate the outer eight-palace wheel in geometric order:

`1 -> 8 -> 3 -> 4 -> 9 -> 2 -> 7 -> 6 -> 1`

while `天禽` is carried with `天芮` through坤二.

Classification: `ROTATION_SEQUENCE_OBJECT_MISMATCH`.

### C. 值使落宫把“时支所属宫”当成“旬内时序计宫”

Legacy door movement used `zhiPalace(hour branch)` as the target.

The source counts the hour offset from the xun leader through nine palace numbers:

- 阳遁 forward;
- 阴遁 reverse.

Example p21: `甲寅`在8宫，卯9、辰1、巳2，因此 `丁巳` 的值使生门落2宫.

Example p22: `甲午`在5宫，阴遁逆数，未4、申3、酉2、戌1，因此 `戊戌` 的值使死门落1宫.

Classification: `DOOR_TARGET_OBJECT_MISMATCH`.

### D. 天禽被当成独立第九颗转星

Legacy code rotated `STAR_HOME[5]=天禽` as an independent ninth position.

The source p21-p22 explicitly places `天禽` together with `天芮` in the rotating star layer.

Classification: `CENTER_HOST_REPRESENTATION_GAP`.

### E. 八神使用了另一套宫序

Legacy deity movement used ad-hoc palace lists.

The worked examples put小值符 at the large chief-star destination and then:

- 阳遁沿外八宫顺行;
- 阴遁沿外八宫逆行.

Classification: `DEITY_ROTATION_SEQUENCE_MISMATCH`.

## 3. Patch strategy: do not replace one dogma with another

This audit does **not** silently replace the existing engine with “善天道真法”.

Instead production exposes two explicit profiles:

- `LEGACY_EXPERIMENTAL`
- `SHANTI_DAO_71_P21_P22`

The old default remains available as the A/B baseline. The new profile is narrowly bound to the operations supported by p15-p22 and the two worked plates.

This preserves:

`method disagreement -> explicit profile`

rather than:

`new book found -> overwrite old method`.

## 4. Source-profile mechanics implemented

The source-defined profile separates three different sequences:

1. `1..9` flying-number sequence for ground-plate placement and the value-door hour count;
2. outer-ring geometric sequence `1,8,3,4,9,2,7,6` for star/door rotation;
3. deity sequence, starting from the chief-star destination, Yang forward / Yin reverse on the outer ring.

It also represents the rotating center host as:

`天芮/天禽`

instead of inventing a ninth outer ring position.

### Explicit unresolved case

If the source-defined value-door hour count lands exactly on center 5, p21-p22 do not provide an independently auditable full-door worked plate. The new profile therefore returns an empty door layer plus:

`SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED`

It does **not** silently guess a host rule merely to keep the UI visually full.

## 5. Independent sparse visual anchors used by tests

Only a small non-substantial subset is hard-coded.

### p21 阳遁三局

Expected setup/identity:

`芒种 / 中元 / 阳3 / 丁巳 / 甲寅遁癸 / 天任 / 生门`

Sparse full-layer anchors include:

- 9宫：天任 / 休门 / 值符;
- 2宫：天冲 / 生门 / 腾蛇;
- 1宫：天芮/天禽 / 景门 / 白虎.

### p21-p22 阴遁八局

Expected setup/identity:

`立秋 / 下元 / 阴8 / 戊戌 / 甲午遁辛 / 天禽 / 死门`

Sparse anchors include:

- 8宫：天芮/天禽 / 惊门 / 值符;
- 1宫：天英 / 死门 / 腾蛇;
- 9宫：天蓬 / 生门 / 玄武;
- 3宫：天柱 / 开门 / 九天.

These are implementation witnesses, not prediction outcomes.

## 6. Negative control

A deliberate wrong-bureau control rebuilds the same `丁巳` hour with阳4 instead of source阳3.

Pass condition:

- correct bureau reproduces the registered sparse star/door anchors;
- wrong bureau must not reproduce them.

If both correct and wrong bureau can pass, the test has no discrimination value.

## 7. What this milestone can and cannot claim

If exact-head CI passes, the new credit is:

> an explicit `SHANTI_DAO_71_P21_P22` implementation path reproduces selected non-Jiazi source-defined star/door/deity anchors and rejects the defined wrong-bureau control.

It does **not** mean:

- `LEGACY_EXPERIMENTAL` is now wrong in every school;
- the whole 71-page carrier is coherent;
- p31/p55 deity lineage has been resolved;
- center-door target 5 has been solved;
- setup/time-boundary alternatives are settled;
- any prediction claim has empirical support.

## 8. Self-audit lesson

The deeper error family is not merely “the code used the wrong order”.

It is:

`same integer labels -> assumed same semantic sequence`

The project already saw this with palace-number order vs geometric rotation order in `qimen-qiju`. The production code independently reproduced the same cognitive mistake.

New engineering discipline:

**Sequence-Object Type Safety**

Whenever an algorithm says “顺/逆/转/飞/移”, first name the object being traversed:

`PALACE_NUMBER_SEQUENCE / OUTER_ROTATION_RING / HOUR_OFFSET_SEQUENCE / DEITY_ORDER / SOURCE_DEFINED_OTHER`.

A direction word without an object is not executable knowledge.

No theory version bump is granted by this implementation correction.
