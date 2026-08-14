# Qimen conflicts

Do not reconcile these in code unless direct source review plus reproducible fixtures resolve the specific issue. Unresolved alternatives must remain explicit as `school`, `method`, `flag`, or blocked capability.

---

## C-JU-CHAIBU-INTERNAL — RESOLVED FOR CURRENT DEFAULT

**Earlier issue:** old notes made B01 (幺学声《预测学》) look as if 拆补 had two incompatible defaults:

- **A:** exact jieqi switching + 甲/己符头定上中下元.
- **B:** exact jieqi switching + simple day-count 1–5 / 6–10 / 11–15 as yuan.

**2026-08-14 direct source review:** rereading B01 and 善天道《奇门遁甲讲义》 supports A as the current project default: crossing the exact jieqi instant changes the jieqi, while yuan remains determined by the nearest 甲/己符头 branch group. The earlier day-count reading is retained as a historical handoff assumption, not silently erased.

**App:** `JuMethod.CHAI_BU_FUTOU` is the default. `CHAI_BU_DAYCOUNT` remains an id but is unsupported until an independent source + worked fixture justifies it. See `10_SOURCE_REVIEW_CORRECTION.md`.

---

## C-ZI-LATE

**What:** 晚子时 clock span and whether it rolls the Qimen day.

- **A:** 23:00–00:00 = 晚子, next Qimen day.
- **B:** one note heading says 20:00–23:00 is 晚子.

**Effect:** several clock hours would attach to a different day pillar / xun.
**App:** implement A; keep B as a rejected note inconsistency, not a school.

---

## C-GATE-ROTATION — RESOLVED BY SEPARATING TWO OPERATIONS

**Earlier appearance of conflict:**

- one rule says the value gate follows the hour branch, Yang forward / Yin reverse;
- another sentence says the eight gates always keep clockwise placement regardless of Yin/Yang.

**Direct worked-board review:** the two statements describe different stages.

1. **Value-gate current palace** moves through numeric palaces 1..9 from the xun anchor: Yang `+1`, Yin `-1` per branch step.
2. **Full eight-gate arrangement** after that current outer palace is known preserves the fixed gate adjacency on the outer clockwise palace ring.

A Yang-8 printed board and a complete Yin-8 printed board both reproduce this decomposition.

**App:** implemented separately as `DutyMovementResolver` + `HumanPlateBuilder`. Do not collapse them back into one direction flag.

**Remaining boundary:** if the value gate's current target is center 5, the full eight-gate representation remains locked until a complete source board for that exact center-target state is found.

---

## C-CENTER-HOST — PARTIALLY RESOLVED

**Resolved:** a complete Yin-8 worked source shows that when the xun hidden Yi is at center 5, Tian-Qin is the value star and the value gate is sourced from Kun-2's Death gate. The value gate's time movement still starts at actual palace 5.

**Not resolved:** this does not automatically prove how to draw every full sky/human/spirit layer when the **current target** of a value star or value gate is center 5. Those states remain explicitly locked.

**App:** `CENTER_PALACE_HOSTED_KUN2` is an anchor rule, not a blanket "redirect all center targets to palace 2" rule.

---

## C-SPIRIT-METHOD — UNRESOLVED SCHOOL FORK

Readable material contains two movement descriptions:

- **FOLLOW_VALUE_STAR:** small value symbol follows the big value star; Yang clockwise and Yin counterclockwise around the outer ring.
- **PER_XUN_GROUND_SPIRITS:** another described method moves a ground-spirit layer once per xun.

**Effect:** the eight spirits can occupy different palaces.

**App:** only `SpiritMethod.FOLLOW_VALUE_STAR` is enabled because complete Yang and Yin fixtures reproduce it. `PER_XUN_GROUND_SPIRITS` exists as an explicit method id and returns `UnsupportedMethod`; it is not aliased into the supported method.

---

## C-PLATE-WALK — RESOLVED

**Earlier issue:** `学习资料/tools/paipan_core.py` used an unsourced hard-coded walk, while the old handoff only had “阳顺阴逆”; this was insufficient to decide numeric order versus another adjacency.

**Direct source review:**

- 善天道《奇门遁甲讲义》 gives the fixed sequence `戊己庚辛壬癸丁丙乙` and 阳顺阴逆.
- 《奇门遁甲预测学》 explicitly states numeric palace walking and supplies complete Yang/Yin placements.

**App:** `EarthPlateBuilder`, complete Yang-3/Yin-3 fixtures and all-18-ju invariants. The old prototype script is not a source.

---

## C-YONGSHEN-PERSON

**What:** who represents the person.

- **A 幺学声:** day stem is commonly the querent.
- **B 善天道:** year-life / day stem selection varies with teaching context and question type.

**Effect:** different Yong-Shen palace and therefore different interpretation.

**App:** do not collapse this into plate mathematics or one universal rule. It belongs to a later question-aware interpretation policy.

---

## C-PRIORITY-VS-URGENCY

**What:** which symbol or layer to read first.

- one prior practice rule prioritized work-related tokens such as Kai gate / value symbol / Sheng gate;
- 善天道 also teaches urgency-dependent reading such as 急则从神 / 缓则从门.

**Effect:** different interpretation priority, not a different board.

**App:** judgement UI / AI policy only. Never change deterministic plate math.

---

## C-KONG-MEANING

**What:** meaning of 逢空.

Different materials/practice records range from hard-negative readings to “not settled / not manifest yet”.

**Effect:** interpretation only.

**App:** no universal hard fail. AI output must identify the source/policy if a specific Kong interpretation is used and allow counter-evidence.

---

## C-SI-MEN-WANG

**What:** seasonal strength of Death gate.

One source-specific teaching table and generic five-element reasoning are not identical.

**App:** source-specific interpretation data, not engine invariant.

---

## C-HIT-XING-OLD

Older user files once contained a wrong pair for Ren/Gui six-instrument punishment. Current project data uses the corrected palace mapping and keeps the old pair only as an anti-regression warning.

---

## C-QINGLONG-NAMING

**What:** Qinglong-return / Dragon-return / Jia-over-Bing naming.

Some notes treat aliases as one pattern; another author may split terminology.

**App:** do not create duplicate pattern IDs from names alone. A pattern engine requires direct formula review + fixtures after the full-board structure is stable.

---

## C-FEIGONG-GOD-NAMES

**What:** rotating-board Bai-Hu/Xuan-Wu terminology versus flying-board Gou-Chen/Tai-Chang/Zhu-Que and possible center-door structures.

**App:** different board schools. Never alias them inside one object merely to make APIs line up.

---

## Method problems (not school forks)

| id | issue |
|---|---|
| M-POSTHOC | Book outcome stories may illustrate how an author applied a rule, but cannot establish predictive accuracy. |
| M-ONLINE-ORACLE | Online paipan sites are comparison tools, not ground truth. |
| M-MEMORY-TABLE | A table recalled from memory cannot become engine truth without reopening a source. |
| M-N05 | `paipan_core.py` is a diary/prototype, not a source. Matching it is not validation. |
| M-AI-RECALC | An LLM may not recalculate or silently correct engine facts; it receives a structured evidence packet. |
| M-LAYER-LEAK | A host rule verified for one layer/stage must not be generalized to another layer/stage without a source fixture. The center-5 work is the canonical regression example. |

See `12_FULL_PLATE_AI_CLOSED_LOOP.md` for the latest resolved/locked boundary.
