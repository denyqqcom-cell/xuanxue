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
**Required:** compute 24 jieqi from **solar longitude** (or a tested astronomy library).  
**Forbidden as encoder:** the rounded table “立春2.4 / 立秋8.7” in N01 §2.5. That table is a memory aid, not a boundary.

**Output:** current jieqi name, `yinYangDun` (`YANG` if jieqi is in 冬至…芒种 inclusive set; `YIN` if 夏至…大雪), seconds-since-jieqi-start, day-index-in-jieqi 1-based.

**Boundary:** “交节当天” — user notes: 拆补 uses the new jieqi as soon as the instant passes the term. That is a school choice (拆补). 置闰 may keep 符头 logic across the term.

**implementation_ready:** calendar library YES; wiring to ju NO until jieqi tests exist.  
**Sources:** N01 §2.5 (approx, reject for code); N01/N02 拆补 “一进交接即用该节气之局”.  
**MODEL_KNOWLEDGE_ONLY:** that 24 terms are defined by 15° solar longitude. Do not put this sentence into fixtures until a library + test is added.

---

## ALG-JU-01  拆补 ju (default school)

**Inputs:** `yinYangDun`, `dayIndexInJieqi` (1–15+), jieqi name.  
**Steps:**

1. yuan = 上 if day in 1–5; 中 if 6–10; 下 if 11–15. Days 16+ (long jieqi) → treat as 下 unless a sourced rule says otherwise. **Uncertain — see 09.**  
2. Look up ju number in ALG-JU-TABLE.  
3. Return `{dun, ju, yuan, method=CHAI_BU}`.

**Must not** use 甲己 符头 to choose yuan in this method.

**Sources:** N01 §3.1; N02 qiju §2.4; B01 pp.66–68 internally contradicts this — default follows the “day-count” reading + user adjudication, labeled school `CHAI_BU_DAYCOUNT`.  
**implementation_ready:** YES once jieqi day-index is exact.

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
**confidence B.** Origin claimed: 烟波钓叟歌 lineage + web cross-check (百度百科 / ctext). **B22 PDF was not read this pass**, so this table is **not A** and not a golden fixture until checked against B22 or two printed editions.

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

Invariant: each row is a rotation of one 宫组. Use this as a unit test on the table itself, not as proof the historical song matches.

---

## ALG-PLATE-01  Earth plate (地盘)

**Inputs:** `{dun, ju}`.  
**Steps:**

1. 洛书 numbers: 1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离.  
2. Sequence of 九仪: 戊己庚辛壬癸丁丙乙.  
3. Place 戊 on palace `ju`. That is the definition of “几局”.  
4. YANG: walk the remaining 八仪 in 洛书 **forward** (notes: 顺). YIN: **backward** (逆).  
5. 中5: 天禽 / 寄坤 is a later star rule, not an earth-yi skip. Earth still has a 戊…乙 in some palace including possibly 5.

**implementation_ready:** PARTIAL. The walk order on 洛书 (numeric 1→9 vs 洛书邻格) is **not uniquely specified** in the notes I read. N05 used `fly=[5,6,7,8,9,1,2,3,4]` which is **not sourced** in that file. Do not copy N05 as truth.

**Sources:** N02 §7.1; N01 §3.3.  
**Conflicts:** see C-PLATE-WALK.

---

## ALG-PLATE-02  旬首 / 值符 / 值使

**Inputs:** hour pillar.  
**Steps:**

1. 旬首 of hour: 甲子戊, 甲戌己, 甲申庚, 甲午辛, 甲辰壬, 甲寅癸.  
2. 旬空: the two branches not in that 10-day xun (戌亥 / 申酉 / 午未 / 辰巳 / 寅卯 / 子丑).  
3. Find which earth palace holds that 遁仪.  
4. Home star of that palace = 值符星. Home gate = 值使门 (中5 has no gate — 寄, usually 坤2).  

Home stars (standard 洛书驻地, N01 §2.1):  
1天蓬 2天芮 3天冲 4天辅 5天禽 6天心 7天柱 8天任 9天英  

Home gates:  
1休 2死 3伤 4杜 6开 7惊 8生 9景  

**implementation_ready:** YES for the maps; depends on ALG-PLATE-01 for palace of 遁仪.

---

## ALG-PLATE-03  Sky / gate / spirit rotation

**Inputs:** earth plate, 值符星, 值使门, hour stem, hour branch, dun.  
**Intended steps (from notes, not independently executed):**

1. Sky: move 值符星 to the palace where **hour stem** currently sits on the earth plate; keep star cyclic order. 天禽 usually 寄坤2.  
2. Gates: 值使 follows **hour branch**; notes also say gates always rotate clockwise regardless of dun — **conflicts with “阴逆”**.  
3. Spirits: 小值符追大值符; YANG clockwise 值符→螣蛇→太阴→六合→白虎→玄武→九地→九天; YIN reverse. 飞宫 school uses 勾陈/太常/朱雀 names instead of 白虎/玄武.

**implementation_ready:** NO for this pass. N05 explicitly stopped before these plates.

**Sources:** N02 §10–11; N01 §5.3; B02 ch.12 notes on 飞宫.

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
**Default for App:** expose **generator output** (12 pairs), show book-10 as optional “printed table” school.

**implementation_ready:** YES for the generator.  
**Sources:** N01 验证1.

---

## What not to encode yet

- Any money / score / weather numeric formula  
- 90 十干克应 omen strings as logic  
- 年家/月家/日家  
- 飞宫  
- True solar time  
- N05 earth-plate walk
