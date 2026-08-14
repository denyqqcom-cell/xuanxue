# Qimen algorithm spec — current encodable contract

Status date: 2026-08-14

This file is the canonical **engineering** specification for `qimen-core`. It records only rules that are either implemented with executable tests or explicitly blocked. It is a rewrite, not a transcription of modern teaching material.

Rules:

- If a method differs by school, encode the school/method id instead of pretending there is one universal rule.
- Source examples validate only the layout/calculation fact they reproduce; later outcome claims in a case are not engine evidence.
- An online paipan site is never ground truth.
- A source gap produces an explicit unsupported/locked state, not a guess.
- Default timezone for the current core is `Asia/Shanghai`.

---

## ALG-CAL-01 — civil day pillar

**Input:** Gregorian civil date used by the current Qimen day.

**Contract:** map the date to the sexagenary cycle using a continuous day count. Regression anchors include 1900-01-01 = 甲戌 and 2000-01-01 = 戊午; both anchors must agree with the same mapping.

**State:** implemented and tested.

---

## ALG-CAL-02 — hour pillar / 五鼠遁

**Input:** day stem + hour branch.

Stem at 子:

- 甲/己 -> 甲
- 乙/庚 -> 丙
- 丙/辛 -> 戊
- 丁/壬 -> 庚
- 戊/癸 -> 壬

Advance one stem for each branch from 子.

**State:** implemented and tested.

---

## ALG-CAL-03 — 13 clock slots and late 子

Current supported convention:

- 00:00–00:59 = 早子, same civil date.
- 01:00–22:59 = ordinary two-hour branches.
- 23:00–23:59 = 晚子; when `lateZiRollsToNextDay=true`, Qimen day rolls to the next civil date before recomputing day/hour pillars.

A stray note describing 20:00–23:00 as late 子 is not a supported school.

**State:** implemented as a configurable late-Zi day-roll policy; tested.

---

## ALG-CAL-04 — exact jieqi boundary

**Input:** instant + zone.

`JieqiClock` uses the repository's existing `cn.6tail:lunar:1.7.7` dependency to obtain second-level solar-term boundaries. Rounded memory dates such as “2/4 = 立春” are never used as the boundary algorithm.

Current v1 deliberately supports only `Asia/Shanghai`; other zones and true-solar-time semantics are rejected until sourced and tested.

The new jieqi takes effect at its exact boundary instant. A civil-day index inside the term may be exposed as metadata, but it is not the current yuan resolver.

**State:** implemented; second-level boundary tests include 2022 立春 / 立秋 values from the dependency's own tested data.

---

## ALG-JU-01 — current 拆补 method: `CHAI_BU_FUTOU`

**Input:** exact current jieqi + current day pillar.

1. Crossing the exact jieqi instant switches to the new term.
2. Resolve the nearest previous day whose stem is 甲 or 己; this is the five-day 符头.
3. Yuan from the branch of that 符头:
   - 子/午/卯/酉 -> 上
   - 寅/申/巳/亥 -> 中
   - 辰/戌/丑/未 -> 下
4. Resolve `{jieqi, yuan}` through the 24-term ju table.

The earlier `CHAI_BU_DAYCOUNT` handoff assumption is retained as an id but is unsupported; it is not silently aliased to the current method.

**State:** implemented and source-reviewed. See `10_SOURCE_REVIEW_CORRECTION.md`.

---

## ALG-JU-02 — 置闰 and other ju schools

`ZHI_RUN` and other alternate ju methods are not implemented merely from outline notes. They require independent worked fixtures for edge cases such as 超神/接气/闰局.

**State:** blocked / unsupported.

---

## ALG-JU-TABLE — 24 jieqi × three yuan

Current triples in `{上,中,下}` order:

Yang terms:

- 冬至 1/7/4; 小寒 2/8/5; 大寒 3/9/6
- 立春 8/5/2; 雨水 9/6/3; 惊蛰 1/7/4
- 春分 3/9/6; 清明 4/1/7; 谷雨 5/2/8
- 立夏 4/1/7; 小满 5/2/8; 芒种 6/3/9

Yin terms:

- 夏至 9/3/6; 小暑 8/2/5; 大暑 7/1/4
- 立秋 2/5/8; 处暑 1/4/7; 白露 9/3/6
- 秋分 7/1/4; 寒露 6/9/3; 霜降 5/8/2
- 立冬 6/9/3; 小雪 5/8/2; 大雪 4/7/1

Each triple is protected by range/structure tests. Historical-lineage confidence is still lower than executable confidence because the actual B22 scan remains difficult to compare directly.

**State:** implemented; historical-source cross-check remains open.

---

## ALG-PLATE-01 — earth plate / 地盘九仪

**Input:** `{dun, ju}`.

Fixed sequence:

`戊 -> 己 -> 庚 -> 辛 -> 壬 -> 癸 -> 丁 -> 丙 -> 乙`

1. Put 戊 in palace `ju`.
2. Yang: remaining sequence follows numeric palace `+1`, wrapping 9 -> 1.
3. Yin: remaining sequence follows numeric palace `-1`, wrapping 1 -> 9.
4. Center 5 is a normal earth-plate location; do not apply later Tian-Qin hosting rules here.

**Evidence:** complete Yang-3 and Yin-3 source boards plus all-18-ju invariants.

**State:** implemented as `EarthPlateBuilder` and closed by CI.

---

## ALG-PLATE-02 — xun hidden Yi, value star and value gate anchor

Hidden-Yi mapping:

- 甲子 -> 戊
- 甲戌 -> 己
- 甲申 -> 庚
- 甲午 -> 辛
- 甲辰 -> 壬
- 甲寅 -> 癸

Home stars:

`1蓬 2芮 3冲 4辅 5禽 6心 7柱 8任 9英`

Ordinary home gates:

`1休 2死 3伤 4杜 6开 7惊 8生 9景`

Algorithm:

1. Find the earth palace holding the xun hidden Yi.
2. Its home star is the value star.
3. For an outer palace, the same palace's home gate is the value gate.
4. If the hidden Yi is in center 5, the currently supported turning-board source rule uses Tian-Qin as value star and Kun-2's Death gate as the value gate's home source. Record `gateHomePalace=2`, but keep `dunYiPalace=5` as the actual time-movement anchor.

**Important boundary:** `CENTER_PALACE_HOSTED_KUN2` is an anchor rule, not permission to redirect every later center target to palace 2.

**State:** implemented as `DutyAnchorResolver`; Yang and center-hosted Yin fixtures pass.

---

## ALG-PLATE-03 — current value star / value gate positions

### Value star

- Normally follows the current hour stem's earth-palace location.
- If the hour stem is 甲, use the xun hidden Yi as the effective stem.

### Value gate

1. Start from the xun hidden-Yi **actual** earth palace, including center 5.
2. Compute branch steps from xun-head branch to current hour branch; valid steps within the xun are 0..9.
3. Yang: numeric palace `+steps` over 1..9.
4. Yin: numeric palace `-steps` over 1..9.

**Fixtures:**

- 2004-05-29 Wu-Wu, Yang 8: Tian-Fu / Du from 4 -> current 8/8.
- printed Yin-7 example: Tian-Chong current 6, Shang gate current 7.
- printed center-hosted Yin-8 example: Tian-Qin current 8; Death gate starts at center 5 and reaches 1 at Xu.

**State:** implemented as `DutyMovementResolver` and closed by CI.

---

## ALG-PLATE-04 — human plate / 人盘八门

Two operations must remain separate.

### A. Value-gate movement

Already resolved by ALG-PLATE-03: Yang numeric forward, Yin numeric reverse through 1..9.

### B. Full eight-gate arrangement

Once the current value gate is on an outer palace, preserve the gate cycle along the clockwise outer-palace ring.

Outer clockwise ring:

`1 -> 8 -> 3 -> 4 -> 9 -> 2 -> 7 -> 6 -> 1`

Gate cycle:

`休 -> 生 -> 伤 -> 杜 -> 景 -> 死 -> 惊 -> 开 -> 休`

This separation resolves the earlier apparent conflict between “阳顺阴逆” and “八门固定顺时针相邻”.

**Hard lock:** if the value gate's **current target** is center 5, full human-plate layout returns `CenterValueGateUnverified`. No host rule is borrowed from another stage.

**Evidence:** complete Yang-8 and Yin-8 source boards.

**State:** implemented as `HumanPlateBuilder`; source fixtures and center-negative test pass.

---

## ALG-PLATE-05 — sky plate / 天盘九星 + carried stems

The supported turning-board model rotates eight outer groups.

Outer clockwise ring:

`1 -> 8 -> 3 -> 4 -> 9 -> 2 -> 7 -> 6`

Home groups in that ring order:

- 1: Tian-Peng
- 8: Tian-Ren
- 3: Tian-Chong
- 4: Tian-Fu
- 9: Tian-Ying
- 2+5 hosted group: Tian-Rui + Tian-Qin
- 7: Tian-Zhu
- 6: Tian-Xin

Each star carries the earth-plate stem from its own home palace. Tian-Rui and Tian-Qin therefore share one target palace but can carry different stems from homes 2 and 5.

Algorithm:

1. ALG-PLATE-03 supplies the current value-star target.
2. Place the value star's rotating group on that outer target.
3. Place remaining groups in fixed order around the outer clockwise ring.
4. Preserve each `homePalace` and `carriedStem` in `SkyStarPlacement`.

**Hard lock:** current value-star target = center 5 -> `CenterValueStarUnverified`.

**Evidence:**

- 2004 Yang-8 complete star board.
- 1995-06-11 Yang-3 complete star + carried-stem board, including separately carried stems for Tian-Rui and hosted Tian-Qin.
- printed Yin-8 complete star board.

**State:** implemented as `SkyPlateBuilder`; tests pass.

---

## ALG-PLATE-06 — spirit plate / 神盘八神

Methods are explicit:

### `FOLLOW_VALUE_STAR` — supported

Spirit cycle:

`值符 -> 螣蛇 -> 太阴 -> 六合 -> 白虎 -> 玄武 -> 九地 -> 九天`

1. Put the small value symbol in the current big-value-star palace.
2. Yang: continue on the outer ring clockwise.
3. Yin: continue on the outer ring counterclockwise.

### `PER_XUN_GROUND_SPIRITS` — unsupported

A readable source records this alternate method, but the branch does not yet have independent fixtures for it. It returns `UnsupportedMethod`; it is not merged into the supported method.

**Hard lock:** current value-star target = center 5.

**Evidence:** complete printed Yang and Yin spirit boards.

**State:** `FOLLOW_VALUE_STAR` implemented as `SpiritPlateBuilder`; alternate method blocked.

---

## ALG-PLATE-07 — conditional full four-layer plate

`FullPlateResolver` composes earth, sky, human and spirit layers.

Return states:

- `Resolved(FullPlate)` when the current supported turning-board builders can construct all four layers.
- `Locked(reasons)` when current value star and/or current value gate targets center 5.

Lock reasons:

- `VALUE_STAR_IN_CENTER`
- `VALUE_GATE_IN_CENTER`

Engine-level states:

- `FULL_PLATE_RESOLVED_SUPPORTED_METHOD`
- `FULL_PLATE_LOCKED_CENTER_TARGET`

**Golden civil-time fixture:** `1995-06-11 09:30 Asia/Shanghai` must reproduce day/hour/xun/ju and all four source layers end-to-end.

**Real center-lock acceptance:** `1995-08-13 12:00 Asia/Shanghai` resolves to the source-supported Bing-Zi / Yin-8 day and Jia-Wu hour; hidden Xin is center 5, so both center lock reasons must appear.

**State:** conditionally implemented and closed by tests/CI. This is not a claim that all Qimen schools are complete.

---

## ALG-REL-01 — 六仪击刑 static map

Current engine map:

- 戊 -> 3
- 己 -> 2
- 庚 -> 8
- 辛 -> 9
- 壬 -> 4
- 癸 -> 4

This is structured rule data only; interpretive wording is not embedded in engine logic.

**State:** implemented. Source confidence remains lower than the full-board fixtures because the claimed printed page has not been reopened in this cycle.

---

## ALG-REL-02 — 五不遇时 generator

The engine generates candidates from the stem relation rather than trusting a short printed lookup table as exhaustive. Existing tests protect the generator output and known discrepancies with one printed table.

**State:** implemented; interpretation of severity belongs outside plate math.

---

## AI-01 — interpretation evidence gate

This is an engineering contract, not a traditional Qimen rule.

Execution modes:

- `DISABLED` — default
- `LOCAL_MODEL`
- `REMOTE_USER_CONFIGURED`

Remote mode requires `explicitRemoteConsent=true` on the individual request. `qimen-core` stores no API key and performs no HTTP request.

Scopes:

- `PRE_PLATE`
- `EARTH_PLATE`
- `DUTY_RUNTIME`
- `FULL_PLATE`

`FULL_PLATE` is available only when `QimenChart.fullPlate` is `Resolved`. A center-target `Locked` chart returns `ScopeLocked`; an LLM cannot bypass the deterministic guard.

For a resolved full plate, the evidence packet can contain:

- calendar/xun/ju facts;
- earth plate;
- value-star/value-gate runtime;
- sky stars with carried stems;
- human gates;
- spirits.

The LLM receives facts to interpret; it is not asked to recalculate the plate. `ENGINE_VERIFIED` means “produced by the current tested engine”, not “scientifically validated metaphysical conclusion”.

**Acceptance:** resolved golden-chart evidence, real center-locked chart rejection, carried-stem presence and per-request remote consent are executable tests.

See `12_FULL_PLATE_AI_CLOSED_LOOP.md`.

---

## Explicitly not encoded / not globally claimed

- 置闰, 茅山, 飞宫 complete algorithms
- true solar time
- year/month/day Qimen
- alternate per-xun ground-spirit method
- full target-at-center sky/human/spirit representation
- modern-book omen prose as hard logic
- money/score/weather numeric formulas derived from retrospective cases
- universal Yong-Shen selection or reading priority across question types
- predictive accuracy claims inferred from source case outcomes

The current core is a **conditionally complete, source-fixtured turning-board implementation for its supported method**, not a universal Qimen oracle.
