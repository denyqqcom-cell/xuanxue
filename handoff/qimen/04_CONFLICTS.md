# Qimen conflicts

Do not reconcile these in code unless a direct source review plus reproducible fixture has resolved the specific conflict. Unresolved alternatives must remain explicit as `school`, `flag`, or blocked capability.

---

## C-JU-CHAIBU-INTERNAL — RESOLVED FOR CURRENT DEFAULT

**Earlier issue:** old notes made B01 (幺学声《预测学》) look as if 拆补 had two incompatible defaults:

- **A:** exact jieqi switching + 甲/己符头定上中下元.  
- **B:** exact jieqi switching + simple day-count 1–5 / 6–10 / 11–15 as yuan.

**2026-08-14 direct source review:** rereading B01 and 善天道《奇门遁甲讲义》 supports A as the current project default: crossing the exact jieqi instant changes the jieqi, while yuan remains determined by the nearest 甲/己符头 branch group. The earlier day-count reading is retained as a historical handoff assumption, not silently erased.

**App:** `JuMethod.CHAI_BU_FUTOU` is the default. `CHAI_BU_DAYCOUNT` remains an id but is unsupported until an independent source + worked fixture justifies it. See `10_SOURCE_REVIEW_CORRECTION.md`.

---

## C-ZI-LATE

**What:** 晚子时 clock span and whether it rolls the qimen day.

- **A:** 23:00–00:00 = 晚子, next qimen day (qiju §6 table; household 13-slot list).  
- **B:** one note heading says “用20点~23点为晚子时” (qiju §3.1).

**Effect:** four hours of charts would attach to the wrong day pillar / xun.  
**App:** implement A; keep B as a rejected note inconsistency, not a school.

---

## C-GATE-ROTATION

**What:** 人盘 direction.

- **A:** B01 directly states 值使随时支按“阳顺阴逆”运行 and gives an 阳遁八局 worked sequence.  
- **B:** an older extracted note also contains “八门永远顺时针转排，不论阴阳遁”.

**Effect:** entire 人盘 can mirror on 阴遁.  
**App:** the 阳遁 worked sequence may become a fixture; do not ship the 阴遁 gate rotation until a named 阴遁 worked board is reproduced.

---

## C-PLATE-WALK — RESOLVED

**Earlier issue:** `学习资料/tools/paipan_core.py` used an unsourced hard-coded walk, while the old handoff only had “阳顺阴逆”; this was insufficient to decide whether the path meant numeric palace order or another 洛书 adjacency.

**2026-08-14 direct source review:**

- 善天道《奇门遁甲讲义》 gives the fixed sequence `戊己庚辛壬癸丁丙乙` and 阳顺阴逆.
- 《奇门遁甲预测学》 explicitly states numeric palace walking and supplies complete examples:
  - 阳三局 `3-4-5-6-7-8-9-1-2`
  - 阴三局 `3-2-1-9-8-7-6-5-4`

The printed heading of the second example contains a typo, but its prose says 阴遁逆排 and all nine placements agree with the reverse numeric sequence.

**App:** earth plate is now implemented by `EarthPlateBuilder`, protected by complete 阳三/阴三 fixtures and 18-ju invariants. The old N05 script is still not treated as a source. See `11_EARTH_PLATE_AND_AI_INTERPRETATION.md`.

---

## C-YONGSHEN-PERSON

**What:** who is “the person”.

- **A 幺学声:** 日干 = 求测者.  
- **B 善天道:** prefer 年命 in some question types / teaching contexts.

**Effect:** different 用神 palace.  
**App:** do not collapse this into a universal hard rule. `PersonToken.DAY_STEM` remains the conservative engine default; `YEAR_PILLAR` requires question-type context and later interpretation-layer handling.

---

## C-PRIORITY-VS-URGENCY

**What:** what to read first.

- **A:** 开门 > 值符 > 生门 > 星神 (user 6/15 failure analysis).  
- **B 善天道:** 急则从神 / 缓则从门.

**Effect:** opposite first-look on 急事.  
**App:** judgement UI / AI interpretation policy only; never use it to change plate math.

---

## C-KONG-MEANING

**What:** 逢空.

- **A book:** B01 p.76 “逢空则不吉” (as cited).  
- **B book:** 《最新实例解析》 p.81 “方向未定” (as cited in notes).  
- **C practice:** 2026-06-15 空 + 大涨 → user rewrote as “方向待定”.

**Effect:** interpretation, not plate math.  
**App:** do not implement A as a hard fail. AI output must identify this as a school/contextual interpretation when relevant.

---

## C-SI-MEN-WANG

**What:** 死门旺季.

- **A 善天道精华 p.9:** 死门旺于秋.  
- **B common 五行:** 土旺于四季月.

**App:** store as source-specific interpretation data, not as physics or engine invariant.

---

## C-HIT-XING-OLD

**What:** older user files once had 壬击刑亥 / 癸击刑子. Current notes correct to 巽4 / 巽4.  
**App:** only ship the current map; keep the old pair in this file so nobody “restores” it.

---

## C-QINGLONG-NAMING

**What:** 青龙返首 vs 龙回首 vs 甲加丙.

Notes 2026-08-08: treated as one pattern (天盘甲/戊加地盘丙), not two.  
**Risk:** another author may split them.  
**App:** one pattern id with aliases only after the full plate exists; do not invent a second pattern without a fixture.

---

## C-FEIGONG-GOD-NAMES

**What:** 转盘 白虎/玄武 vs 飞宫 勾陈/太常/朱雀 (+ 中门).  
**App:** different `BoardSchool`. Do not alias 白虎=勾陈 in one object.

---

## Method problems (not school forks)

| id | issue |
|---|---|
| M-POSTHOC | Book cases and “9/9 100%” are 回溯. They may illustrate a method but cannot establish predictive accuracy. |
| M-ONLINE-ORACLE | Online paipan sites are comparison tools, **not** ground truth sources. |
| M-MEMORY-TABLE | A table recalled from memory must never be promoted to engine truth without reopening a source. |
| M-N05 | `paipan_core.py` is a diary/prototype, not a source. Even where later code matches it, the justification must come from direct source + fixtures. |
| M-AI-RECALC | An LLM must not recalculate or silently “correct” engine facts. AI receives an evidence packet and is only an interpretation layer. |
