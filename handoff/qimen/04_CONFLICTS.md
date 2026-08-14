# Qimen conflicts

Do not reconcile these in code. Expose them as `school` or `flag`.

---

## C-JU-CHAIBU-INTERNAL

**What:** B01 (幺学声《预测学》) describes 拆补 in two incompatible ways.

- **A:** 拆补 still uses 甲己 符头 to set 上中下元 (notes: B01 pp.66–67).  
- **B:** As soon as the jieqi instant arrives, use that jieqi’s ju; yuan from day-count inside the jieqi (notes: B01 p.68; 善天道 / 应用学 practice).

**Effect:** On 交节 day and on days when 符头 yuan ≠ day-count yuan, the two methods yield different `{dun, ju}`. User example: 2026-08-07 立秋 癸丑.

**Cases:** note-level only; no third-party printed chart recomputed this pass.  
**Judgeable now?** No.  
**App:** `JuMethod.CHAI_BU_DAYCOUNT` (default, labeled “拆补·日数分段”) vs `CHAI_BU_FUTOU` vs `ZHI_RUN`. Never name both A and B “拆补” without a suffix.

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

- **A:** “阳顺阴逆随时支” (qiju §10.3 quoting B01 p.70–71).  
- **B:** same note, next sentence: “八门永远顺时针转排，不论阴阳遁”.

**Effect:** entire 人盘 mirrored on 阴遁.  
**App:** do not ship 人盘 until a fixture board from a named book is reproduced both ways.

---

## C-PLATE-WALK

**What:** how 九仪 walk 洛书 after 戊 sits on ju.

N05 uses `fly = [5,6,7,8,9,1,2,3,4]` without a citation. Notes only say 阳顺阴逆.  
**Effect:** every palace’s 仪 can change.  
**App:** block release of 地盘 until two independent worked ju diagrams match.

---

## C-YONGSHEN-PERSON

**What:** who is “the person”.

- **A 幺学声:** 日干 = 求测者.  
- **B 善天道:** prefer 年命.

**Effect:** different 用神 palace.  
**App:** `PersonToken.DAY_STEM` default; `YEAR_PILLAR` experimental.

---

## C-PRIORITY-VS-URGENCY

**What:** what to read first.

- **A:** 开门 > 值符 > 生门 > 星神 (user 6/15 failure analysis).  
- **B 善天道:** 急则从神 / 缓则从门.

**Effect:** opposite first-look on 急事.  
**App:** judgement UI only; never auto-pick.

---

## C-KONG-MEANING

**What:** 逢空.

- **A book:** B01 p.76 “逢空则不吉” (as cited).  
- **B book:** 《最新实例解析》 p.81 “方向未定” (as cited in notes).  
- **C practice:** 2026-06-15 空 + 大涨 → user rewrote as “方向待定”.

**Effect:** omen text, not plate math.  
**App:** do not implement A as a hard fail.

---

## C-SI-MEN-WANG

**What:** 死门旺季.

- **A 善天道精华 p.9:** 死门旺于秋.  
- **B common 五行:** 土旺于四季月.

**App:** store as 善天道 table, not as physics.

---

## C-HIT-XING-OLD

**What:** older user files once had 壬击刑亥 / 癸击刑子. Current notes correct to 巽4 / 巽4.  
**App:** only ship the current map; keep the old pair in this file so nobody “restores” it.

---

## C-QINGLONG-NAMING

**What:** 青龙返首 vs 龙回首 vs 甲加丙.

Notes 2026-08-08: treated as one pattern (天盘甲/戊加地盘丙), not two.  
**Risk:** another author may split them.  
**App:** one `PatternId.QINGLONG_FANSHOU` with aliases listed; do not invent a second pattern without a fixture.

---

## C-FEIGONG-GOD-NAMES

**What:** 转盘 白虎/玄武 vs 飞宫 勾陈/太常/朱雀 (+ 中门).  
**App:** different `BoardSchool`. Do not alias 白虎=勾陈 in one object.

---

## Method problems (not school forks)

| id | issue |
|---|---|
| M-POSTHOC | Book cases and “9/9 100%” are 回溯. User protocol 6/28 already bans counting them as accuracy. |
| M-ONLINE-ORACLE | User sometimes adjudicated ju by “在线排盘”. Those sites are **not** sources. |
| M-MEMORY-TABLE | User once filled 立秋二九六 from memory; self-caught. Any table without a book reopen is B/D. |
| M-N05 | `paipan_core.py` hardcodes 8/7=癸丑 and 立秋=8/7. Useful as a diary, illegal as an engine. |
