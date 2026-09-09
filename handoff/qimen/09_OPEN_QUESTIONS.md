# Open questions (qimen)

## Resolved this cycle

1. **地盘九仪 walk**: direct source review supports numeric palace walking; 阳遁 `+1`, 阴遁 `-1`, wrap 1..9. Complete 阳三/阴三 fixtures and 18-ju invariants are executable.
2. **拆补 current default**: exact jieqi switching + nearest 甲/己符头定元 is the current supported method; the older day-count assumption remains unsupported.
3. **值符 / 值使初始锚点**: xun hidden Yi palace determines the value star and value gate home source.
4. **中五旬首锚点**: a complete Yin-8 worked source resolves Tian-Qin as value star and Death gate via Kun-2 host when the hidden Yi is in center 5; time movement still starts from actual palace 5.
5. **人盘“阳顺阴逆 vs 八门顺时针”**: no longer treated as one contradictory operation. Value-gate current palace moves by numeric 1..9 (Yang + / Yin -); once its current outer palace is known, all gates keep fixed adjacency on the outer clockwise ring. Complete Yang and Yin boards reproduce this separation.
6. **天盘九星 rotation / 天禽寄坤**: supported for the current turning-board method. Tian-Rui(home2)+Tian-Qin(home5) rotate as one hosted group while retaining separate carried earth stems.
7. **八神 follow-value-star method**: value spirit follows the big value star; Yang outer ring clockwise, Yin counterclockwise. Complete Yang and Yin fixtures pass.
8. **first civil-time four-layer golden chart**: 1995-06-11 09:30 Asia/Shanghai reproduces calendar, ju, duty, sky+carried stems, human gates and spirits end-to-end.
9. **AI FULL_PLATE evidence**: conditionally enabled only when core returns `FullPlateResolution.Resolved`; center-target locked charts cannot be bypassed by AI.

See `12_FULL_PLATE_AI_CLOSED_LOOP.md` for the source-to-test closure record.

## Cannot decide yet

1. **Current value star / value gate landing at center 5**: sources prove the event and resolve the xun anchor, but there is still no sufficiently clear complete board for the exact target-at-center moment. Full sky/human/spirit representation stays locked for those charts.
2. **alternate ground-spirit method**: one source describes a per-xun movement instead of the currently supported follow-value-star method. It remains `PER_XUN_GROUND_SPIRITS` + `UnsupportedMethod` until independent fixtures exist.
3. Whether **交节时刻** should use 真太阳时 in any supported school. Current v1 uses civil `Asia/Shanghai` clock only and rejects true-solar-time mode.
4. **置闰 / 茅山 / 飞宫** full algorithms and fixtures.
5. Outcome of CASE-2026-08-12 Guangzhou weather — not engine evidence.
6. Author identity where uploaded filename metadata conflicts with readable title-page attribution; e.g. the file named “佚名” parses a title page attributing 《奇门遁甲预测学》 to 幺学声.
7. B22 《烟波钓叟歌》: the current ju table still needs a readable direct comparison to the actual scan.
8. Interpretation-layer question classification, Yong-Shen selection and priority conflicts across schools / question types.

## Highest-conflict rules now

1. Center-target full-board representation.
2. Follow-value-star spirits vs per-xun ground spirits.
3. 晚子时 20–23 note vs 23–24 convention; current engine treats 20–23 as a bad note, not a supported school.
4. Interpretation-layer Yong-Shen priority. It must never change deterministic plate math.

## Missing evidence

- The branch has complete four-layer worked boards from readable material, including a civil-time end-to-end golden case, but still lacks a **second readable independent source reproducing that same full datetime**.
- No independently licensed Qimen engine in the corpus should be treated as ground truth.
- 24-jieqi ju table has not yet been checked directly against readable B22 pages.
- Several old image-heavy scans require targeted manual page review rather than blind OCR.

## Next source work

1. Find a complete worked board where the **current** value star or value gate lands at center 5; do not infer the representation from host rules used in other layers.
2. Rebuild the 1995-06-11 golden chart from one independent readable source, if available.
3. Separate and fixture the per-xun ground-spirit school if it is worth supporting.
4. Only after the deterministic board remains stable, move to interpretation policies: question taxonomy -> Yong-Shen candidates -> evidence weights -> counter-evidence / uncertainty.

## AI interpretation gate

AI infrastructure is now conditional rather than globally partial:

- default disabled;
- local-model and user-configured remote modes remain distinct;
- remote mode requires explicit consent for each request;
- core performs no network request and stores no API key;
- AI receives only structured engine evidence;
- `FULL_PLATE` is allowed only for `FullPlateResolution.Resolved` charts;
- center-target `Locked` charts get only the lower verified scope and cannot ask the model to invent the missing plate.

AI may assist with explanation and scenario reasoning, but it is not an alternate paipan oracle.

## Blind / regression discipline

1. Freeze `QimenRequest` before checking any external calculator; external calculators are comparison signals, not ground truth.
2. Validate plate mathematics with source diagrams and invariants, not outcome stories such as stock, weather, health or court results.
3. A source case may validate a **layout rule** without validating the predictive claims made later in that case.
4. For interpretation experiments, keep `ENGINE_FACT`, `SOURCE_RULE`, `INFERENCE`, `COUNTER_EVIDENCE` and `UNCERTAINTY` separate.
5. Every capability change must end with a targeted regression test plus the branch CI before its state is upgraded.
