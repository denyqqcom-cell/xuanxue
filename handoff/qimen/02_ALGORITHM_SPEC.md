# Qimen algorithm spec (encodable only)

Anything not in this file is not an algorithm.  
If a step needs a school choice, it is written as a parameter, not as “the” method.

Timezone default for this project: **Asia/Shanghai (UTC+8, no DST)**.  
Do not use the machine local zone.  
True solar time: **not specified** — leave `useTrueSolarTime=false` until a sourced algorithm exists.

---

## ALG-CAL-01  Sexagenary day index

**Inputs:** civil date `Y-M-D` in Asia/Shanghai.  
**Preconditions:** Gregorian date after 1900-01-01 is enough for this App.  
**Steps:**

1. Convert the civil date to a Julian Day Number (or equivalent continuous day count).  
2. Map to 60-jiazi. Two anchors already used in user verification (do not hardcode a single magic day without documenting it):
   - 1900-01-01 = 甲戌  
   - 2000-01-01 = 戊午  
3. Both anchors must agree. If they disagree, fail the build.

**Boundary:** date at 00:00 belongs to that civil date. Whether 23:00 still belongs to that **qimen day** is ALG-CAL-03, not this function.

**Output:** `dayStem`, `dayBranch`, `jiaziIndex` 1–60.

**Sources:** N01 交叉验证 2026-08-07 (two-anchor check).  
**Versions:** none.  
**Default:** two-anchor agreement required.  
**implementation_ready:** YES for civil day.  
**Not ready:** lunar date (not required for 时家起局).

---

## ALG-CAL-02  Hour pillar (五鼠遁)

**Inputs:** `dayStem`, `hourBranch` (子丑寅卯辰巳午未申酉戌亥).  
**Steps:**

Song used in notes (do not treat the poem as copyrighted modern prose):

- 甲己 → 甲  
- 乙庚 → 丙  
- 丙辛 → 戊  
- 丁壬 → 庚  
- 戊癸 → 壬  

Then walk the 12 branches from 子.

**Output:** `hourStem`, `hourBranch`.

**Sources:** N02 qimen-qiju §11; N05 script. Multi-source traditional.  
**implementation_ready:** YES.

**Table (rewrite, not a book facsimile):**

| day stem | stem at 子 |
|---|---|
| 甲 / 己 | 甲 |
| 乙 / 庚 | 丙 |
| 丙 / 辛 | 戊 |
| 丁 / 壬 | 庚 |
| 戊 / 癸 | 壬 |

---

## ALG-CAL-03  Early / late 子时

**Inputs:** local clock `HH:mm` in Asia/Shanghai.  
**Recommended default (B, notes disagree — see 04_CONFLICTS):**

| clock | branch | day adjustment |
|---|---|---|
| 00:00–00:59 | 早子 | same civil date |
| 01:00–02:59 | 丑 | same |
| … 2-hour slots … | | |
| 23:00–23:59 | 晚子 | **qimen day = next civil date** (then recompute day pillar) |

**Do not encode** “20:00–23:00 = 晚子” as default. It appears in one note heading and contradicts the 13-label list used by the Ziwei app (`早子 00–01` … `晚子 23–00`).

**implementation_ready:** YES for the 13-slot table; day-change at 23:00 is a **config flag** `lateZiRollsToNextDay` default true.  
**Sources:** N01/N02 mixed; Ziwei `SHICHEN_LABELS` in `xuanxue` app (same household convention, not a qimen book).

---

## ALG-CAL-04  Solar terms (jieqi)

**Inputs:** instant + timezone.  
**Required:** use a tested astronomy/calendar implementation with second-level jieqi boundaries.  
**Forbidden as encoder:** the rounded table “立春2.4 / 立秋8.7” in N01 §2.5. That table is a memory aid, not a boundary.

**Current implementation:** `JieqiClock` wraps the repository's existing MIT dependency `cn.6tail:lunar:1.7.7`. v1 intentionally supports only `Asia/Shanghai`, because the wrapped API has no explicit `ZoneId` parameter and the project must not pretend to offer timezone semantics it has not verified.

**Output:** current jieqi name, `yinYangDun` (`YANG` if jieqi is in 冬至…芒种 inclusive set; `YIN` if 夏至…大雪), seconds-since-jieqi-start, civil-day-index-in-jieqi 1-based.

**Boundary:** the new jieqi takes effect at the exact jieqi instant. The civil-day index is metadata; it is **not** the default yuan resolver.

**Tests:** second-level boundaries include lunar-java's published 2022 立春 / 立秋 values.  
**implementation_ready:** YES for `Asia/Shanghai`; other zones remain unsupported.  
**Sources:** N01 §2.5 approximate memory table (rejected for boundary code); direct source review recorded in `10_SOURCE_REVIEW_CORRECTION.md`; lunar-java v1.7.7 tests for exact boundaries.

---

## ALG-JU-01  拆补 ju (default school: 符头定元)

**Inputs:** exact current jieqi, yin/yang dun, current day pillar.  
**Steps:**

1. When the exact jieqi instant is crossed, switch to the new jieqi immediately.  
2. Find the nearest previous day whose stem is 甲 or 己; this is the current five-day 符头.  
3. Determine yuan by the **branch of that 甲/己符头**:
   - 子午卯酉 → 上元
   - 寅申巳亥 → 中元
   - 辰戌丑未 → 下元
4. Look up the ju number in ALG-JU-TABLE using `{jieqi, yuan}`.
5. Return `{dun, ju, yuan, method=CHAI_BU_FUTOU}`.

**Important correction:** the earlier handoff elevated a simple “jieqi day 1–5 / 6–10 / 11–15” reading to the default. Direct rereading of two currently accessible sources supports immediate jieqi switching **plus** 甲/己符头定元 instead. The historical `CHAI_BU_DAYCOUNT` id is retained as unsupported so the earlier assumption cannot silently disappear.

**Sources:** direct review of B01 《奇门遁甲预测学》 and 善天道《奇门遁甲讲义》, recorded in `10_SOURCE_REVIEW_CORRECTION.md`.  
**implementation_ready:** YES for `CHAI_BU_FUTOU`.

---

## ALG-JU-02  置闰 ju (alternate school)

**Inputs:** day pillar 符头, jieqi, days between 上元符头 and jieqi.  
**Steps (as rewritten from notes, not coded this pass):**

1. 符头 days: 上元 子午卯酉; 中元 寅申巳亥; 下元 辰戌丑未. First day of a yuan is 甲 or 己.  
2. 超神: 符头 before jieqi. 接气: jieqi before 符头. 正授: they coincide.  
3. 置闰 only at 芒种 and 大雪; if 超神 > 9 days, insert a 60-day intercalation.  

**implementation_ready:** NO. No independent worked example was recomputed this pass.  
**Sources:** N01 §3.2; N02 §2.3 / §9; B01 pp.66–67.

---

## ALG-JU-TABLE  24 jieqi × 3 yuan

Rewrite of the mnemonic table in N01 §2.7. User checked “宫组” 1-4-7 / 2-5-8 / 3-6-9.  
**confidence B.** Origin claimed: 烟波钓叟歌 lineage + web cross-check (百度百科 / ctext). **B22 PDF was not read this pass**, so this table is **not A** as historical-source evidence, even though the code table has internal invariants and executable tests.

阳遁:

| jieqi | 上 | 中 | 下 |
|---|---:|---:|---:|
| 冬至, 惊蛰 | 1 | 7 | 4 |
| 小寒 | 2 | 8 | 5 |
| 大寒, 春分 | 3 | 9 | 6 |
| 立春 | 8 | 5 | 2 |
| 雨水 | 9 | 6 | 3 |
| 清明, 立夏 | 4 | 1 | 7 |
| 谷雨, 小满 | 5 | 2 | 8 |
| 芒种 | 6 | 3 | 9 |

阴遁:

| jieqi | 上 | 中 | 下 |
|---|---:|---:|---:|
| 夏至, 白露 | 9 | 3 | 6 |
| 小暑 | 8 | 2 | 5 |
| 大暑, 秋分 | 7 | 1 | 4 |
| 立秋 | 2 | 5 | 8 |
| 处暑 | 1 | 4 | 7 |
| 寒露, 立冬 | 6 | 9 | 3 |
| 霜降, 小雪 | 5 | 8 | 2 |
| 大雪 | 4 | 7 | 1 |

Invariant: each row is a rotation of one 宫组. Use this as a unit test on the table itself, not as proof of historical lineage.

---

## ALG-PLATE-01  Earth plate (地盘)

**Inputs:** `{dun, ju}`.  
**Steps:**

1. Palace numbers: 1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离.  
2. Fixed 九仪 sequence: 戊己庚辛壬癸丁丙乙.  
3. Place 戊 on palace `ju`; that is the operational meaning of “几局”.  
4. YANG: place the remaining sequence by **numeric palace order +1**, wrapping `9 → 1`.  
5. YIN: place the remaining sequence by **numeric palace order -1**, wrapping `1 → 9`.  
6. 中5 is a normal earth-plate location for a 奇/仪. 天禽寄宫 is a later sky-star rule and must not be used to skip palace 5 here.

**Direct source check:**

- 善天道《奇门遁甲讲义》 directly gives the fixed sequence and “阳遁顺布、阴遁逆布”.
- 《奇门遁甲预测学》 directly explains numeric-palace walking and supplies complete worked examples:
  - 阳遁三局: `3-4-5-6-7-8-9-1-2`
  - 阴遁三局: `3-2-1-9-8-7-6-5-4`

The second worked example has a heading typo in the printed text but its prose says “阴遁逆排” and all nine placements match the reverse sequence; the fixture is based on the explicit rule + complete palace assignment, not the mistaken heading.

**Executable fixtures:** complete 阳三局, complete 阴三局, and all 18-ju structural invariants.  
**implementation_ready:** YES. Implemented as `EarthPlateBuilder`.  
**Correction record:** `11_EARTH_PLATE_AND_AI_INTERPRETATION.md`.

---

## ALG-PLATE-02  旬首 / 值符 / 值使 initial anchors

**Inputs:** hour pillar + verified earth plate.  
**Steps supported by current sources:**

1. 旬首 of hour: 甲子戊, 甲戌己, 甲申庚, 甲午辛, 甲辰壬, 甲寅癸.  
2. 旬空: the two branches not in that 10-day xun (戌亥 / 申酉 / 午未 / 辰巳 / 寅卯 / 子丑).  
3. Find which earth palace holds that 旬首遁仪.  
4. The home star of that palace is the 值符星. The corresponding home gate is the 值使门.

Home stars:  
1天蓬 2天芮 3天冲 4天辅 5天禽 6天心 7天柱 8天任 9天英.

Home gates:  
1休 2死 3伤 4杜 6开 7惊 8生 9景.

**Current caution:** palace 5 has no ordinary eight-gate home position. Do **not** invent a gate-5 rule from memory; resolve the 中五/寄宫 case from a direct worked source before making the API total.

**implementation_ready:** PARTIAL. 旬首/遁仪/旬空 are implemented; value-star/value-gate anchoring is the next code milestone.

---

## ALG-PLATE-03  Sky / gate / spirit rotation

**Inputs:** earth plate, 值符星, 值使门, hour stem, hour branch, dun.  
**Intended steps (source review still incomplete):**

1. Sky: move 值符星 to the palace associated with the current hour stem under the verified earth plate / later heavenly-plate rule; preserve the star order. 中五天禽寄宫 still needs direct worked-source verification.  
2. Gates: B01 directly gives “值使随时支，阳顺阴逆” and a worked 阳八局 sequence. An older note also contained a contradictory “八门永远顺时针” sentence, so 阴遁 still needs a named worked fixture before shipping.  
3. Spirits: source review and fixtures still required; do not infer from mnemonic order alone.

**implementation_ready:** NO for complete four-plate generation.

---

## ALG-REL-01  六仪击刑 map (data, not a story)

| yi | hidden branch | 刑 | palace |
|---|---|---|---|
| 戊 | 子 | 卯 | 3 |
| 己 | 戌 | 未 | 2 |
| 庚 | 申 | 寅 | 8 |
| 辛 | 午 | 午 | 9 |
| 壬 | 辰 | 辰 | 4 |
| 癸 | 寅 | 巳 | 4 |

**Sources:** N01 交叉验证 + claimed B01 p.92.  
**implementation_ready:** YES as a static map.  
**confidence:** B (two note-internal derivations; book page not reopened this pass).

---

## ALG-REL-02  五不遇时 generator

**Rule rewrite:** hour stem overcomes day stem, same yin/yang, stems 5 apart in the 10-cycle.  
Enumerate 60 days × 12 hours.  

Book table (善天道精华 pp.25–26 per notes) lists 10 pairs. Independent generation adds 己日乙亥, 庚日丙戌.  
**Default for App:** expose **generator output** (12 pairs), show book-10 only as a printed-table comparison, not as engine truth.

**implementation_ready:** YES for the generator.  
**Sources:** N01 验证1.

---

## AI interpretation boundary (engineering contract, not a traditional rule)

AI is an **interpretation layer**, never an alternative plate calculator.

- Core provides a structured evidence packet containing only engine-produced facts.
- `FULL_PLATE` interpretation stays locked until all four plates are independently verified.
- Remote AI requires explicit per-request consent; core itself stores no API key and sends no network request.
- AI may explain, compare and perform scenario reasoning, but may not silently recalculate pillars, ju, stars, gates or spirits and overwrite core output.
- `ENGINE_VERIFIED` means “produced by current tested engine”, not “scientifically validated metaphysical conclusion”.

See `11_EARTH_PLATE_AND_AI_INTERPRETATION.md`.

---

## What not to encode yet

- Any money / score / weather numeric formula  
- 90 十干克应 omen strings as hard logic  
- 年家/月家/日家  
- 飞宫  
- True solar time  
- Unverified 天盘九星 / 人盘八门 / 神盘八神 rotation  
- Full-plate AI interpretation
