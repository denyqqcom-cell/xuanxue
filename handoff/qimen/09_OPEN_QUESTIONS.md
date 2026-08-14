# Open questions (qimen)

## Resolved this cycle

1. **地盘九仪 walk**: direct source review now supports numeric palace walking. 阳遁 `+1` and 阴遁 `-1`, with wrap; complete 阳三/阴三 fixtures are in code. See `11_EARTH_PLATE_AND_AI_INTERPRETATION.md`.
2. **拆补 current default**: exact jieqi switching + nearest 甲/己符头定元 is the current supported method. The old day-count default is no longer treated as established. See `10_SOURCE_REVIEW_CORRECTION.md`.

## Cannot decide yet

1. **人盘阴遁方向**: B01 has a direct “阳顺阴逆” rule and an 阳遁 worked example, but an older extracted sentence conflicts. Need one named 阴遁 worked board before shipping.  
2. **中五宫值使处理**: palace 5 has 天禽 but no ordinary eight-gate home position; do not fill this from memory.  
3. **天禽寄宫** and the full 天盘九星 rotation rule: requires direct worked-source reproduction.  
4. **八神 rotation** and school-specific god names.  
5. Whether **交节时刻** should use 真太阳时 in any supported school. Current v1 uses civil `Asia/Shanghai` clock only and explicitly rejects true-solar-time mode.  
6. **置闰 / 茅山 / 飞宫** full algorithms and fixtures.  
7. Outcome of CASE-2026-08-12 Guangzhou weather — note was still waiting; do not use it as engine evidence.  
8. Author identity on several filenames (“佚名” vs title-page attribution) where the uploaded filename and parsed title metadata differ.  
9. B22 《烟波钓叟歌》: current ju table vs actual scan still needs a readable direct comparison.

## Highest-conflict rules

1. 人盘阴遁 rotation.  
2. 中五 / 天禽寄宫 handling.  
3. 晚子时 20–23 vs 23–24 (currently treat 20–23 as a bad note, not a supported school).  
4. Interpretation-layer 用神 priority across question types; this must not leak into plate math.

## Missing evidence

- No independently rebuilt **complete four-plate** 九宫 from two readable sources for the same datetime.  
- No independently licensed qimen engine in the corpus that should be treated as ground truth.  
- 24 jieqi ju table not yet checked against the actual B22 scan.  
- Several older scans are image-heavy / low-text and still need targeted human-readable page review rather than blind OCR.

## Next source work

1. Use B01's already located value-star/value-messenger chapter to encode only the **initial anchor** that can be directly reproduced.  
2. Find one printed **阴遁** value-messenger example before deciding the human-plate direction.  
3. Find one complete 天盘九星 example including a 中五/天禽 case or a source that explicitly states the host rule.  
4. Only after those pass, add 八神 and seek one single datetime whose 地/天/人/神 four layers all reproduce.

## AI interpretation gate

AI integration may proceed in parallel only as infrastructure:

- default disabled;
- local-model and user-configured remote modes are distinct;
- remote mode requires explicit per-request consent;
- core performs no network request and stores no API key;
- AI receives only structured engine evidence;
- `FULL_PLATE` interpretation stays locked until the four-plate engine is verified.

The AI may assist with explanation and scenario reasoning, but it is **not** an alternate paipan oracle.

## Blind tests to run

1. Freeze `QimenRequest` inputs before checking any external calculator; compare only the specific layer under test.  
2. Do not use A-share, weather, or book outcomes to validate engine mathematics.  
3. If a website disagrees, log it as `UNTRUSTED_ORACLE`, not ground truth.  
4. For interpretation tests, separate `ENGINE_FACT` from `INTERPRETATION` and require a falsification / uncertainty field before counting a case as useful evidence.
