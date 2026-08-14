# Qimen full-plate + AI closed-loop record

Date: 2026-08-14

This note records only rules that were re-opened in readable source material and then reproduced by tests. It is deliberately a rewrite/engineering record, not a transcription of modern books. No scanned pages, long prose, omen tables, or case-analysis passages are copied into the runtime code or this note.

## 1. Development rule used in this cycle

Every capability follows the same gate:

`source fact -> minimal algorithm -> source fixture -> negative/edge test -> CI -> capability state`

A feature is not called complete merely because the implementation compiles. When a source gap appears, the code must return an explicit lock/error instead of filling the gap from model memory or an online paipan site.

## 2. Value star / value gate anchor and movement

Readable sources used this cycle:

- B01: 幺学声《奇门遁甲预测学（奇门遁甲现代应用技术）》, especially the worked 2004-05-29 case.
- B02: 《善天道奇门遁甲讲义》, especially the complete Yang/Yin worked boards around the qiju chapter.

Engineering result:

1. Find the hidden Yi of the current xun on the earth plate.
2. The home star of that palace is the value star.
3. The home gate of that palace is the value gate.
4. The value star follows the hour stem's earth-palace location; a Jia hour uses the xun's hidden Yi.
5. The value gate starts from the xun hidden-Yi palace and advances one numeric palace per hour branch: Yang increasing, Yin decreasing, wrapping 1..9.

Source fixtures:

- 2004-05-29 Wu-Shen day, Wu-Wu hour, Yang 8: Jia-Yin xun; Tian-Fu / Du anchor at 4; both current positions are 8.
- A printed Yin 7 case: Jia-Chen xun; Tian-Chong anchor at 3 moves to 6, Shang gate moves to 7.

### Self-correction: center palace

The first implementation intentionally left a center-palace gate anchor unresolved. That was safer than guessing, but a later direct source review found a complete Yin 8 worked example:

- Yi-Hai year, Jia-Shen month, Bing-Zi day, Wu-Xu hour, Jia-Wu xun, Yin 8.
- Hidden Xin is in center 5.
- The source identifies Tian-Qin as value star and Death gate as value gate; center uses Kun-2 as the gate's home/host source.
- Crucially, the value gate's time movement still starts from actual palace 5: at Wu branch it is at 5, then Yin reverse to 4,3,2,1 by Xu.

Therefore the code was revised from "center unresolved" to `CENTER_PALACE_HOSTED_KUN2`, while retaining `dunYiPalace=5` as the movement anchor. Regression tests protect this distinction.

## 3. Human plate: apparent direction conflict resolved by separating two motions

Old notes appeared contradictory:

- value messenger moves "Yang forward / Yin reverse";
- all eight gates keep a fixed clockwise adjacency.

The complete Yang and Yin boards show that these statements refer to different operations, not competing full-board algorithms:

1. **Current value-gate palace**: numeric 1..9 movement, Yang +, Yin -.
2. **Full eight-gate placement after the current palace is known**: fixed gate adjacency around the eight outer palaces.

Current outer clockwise ring:

`1 -> 8 -> 3 -> 4 -> 9 -> 2 -> 7 -> 6 -> 1`

Gate cycle:

`Xiu -> Sheng -> Shang -> Du -> Jing(scener y) -> Si -> Jing(alarm) -> Kai -> Xiu`

(`QimenGate` uses distinct enum names internally for the two Chinese homophone/transliteration cases.)

Validated full boards:

- 2004 Yang 8, Wu-Wu: full printed eight-gate board reproduced.
- Yin 8, Wu-Xu: full printed eight-gate board reproduced.

Remaining guard: if the **current value gate itself** is at center 5, there is not yet a sufficiently clear complete eight-gate board for that exact moment. `HumanPlateBuilder` therefore returns `CenterValueGateUnverified` rather than inventing a layout.

## 4. Sky plate: stars plus carried stems

The rotating unit is not only a star label. The readable worked examples show that a star carries the earth-palace Yi/Qi from its original home position.

The engine therefore stores `SkyStarPlacement(star, carriedStem, homePalace)`.

The outer-ring star groups are represented as eight rotating groups; Tian-Rui (home 2) and Tian-Qin (home 5) travel together under the supported center-host rule, while retaining their separate carried stems.

Golden reproduction from B02:

1995-06-11 09:30, Gui-You day / Ding-Si hour, Jia-Yin xun, Yang 3:

- Tian-Ren carrying Gui -> 9
- Tian-Chong carrying Wu -> 2
- Tian-Fu carrying Ji -> 7
- Tian-Ying carrying Ding -> 6
- Tian-Rui carrying Yi + Tian-Qin carrying Geng -> 1
- Tian-Zhu carrying Ren -> 8
- Tian-Xin carrying Xin -> 3
- Tian-Peng carrying Bing -> 4

The test checks these placements as data, not by reproducing the source page or its prose.

Remaining guard: value star current target = center 5 is still locked for the complete sky representation.

## 5. Spirit plate: school conflict kept explicit

Readable material contains at least two spirit-movement methods:

- small value symbol follows the big value star each hour;
- another method moves a ground-spirit layer once per xun.

The project does not merge them.

`SpiritMethod.FOLLOW_VALUE_STAR` is the only currently enabled method. The fixed spirit cycle starts at the value symbol; Yang uses the outer ring clockwise, Yin counterclockwise.

`SpiritMethod.PER_XUN_GROUND_SPIRITS` exists only as an explicit method id and returns `UnsupportedMethod` until a separate reproducible fixture set is established.

Fixtures reproduce the printed 2004 Yang board and the printed Yin-8 reverse board.

## 6. First end-to-end four-layer golden chart

`QimenFullBoardGoldenTest` starts from civil time rather than manually injecting a ju or xun:

`1995-06-11 09:30 Asia/Shanghai`

The deterministic engine must reproduce, in sequence:

- Gui-You day;
- Ding-Si hour;
- Jia-Yin xun;
- Yang 3;
- Tian-Ren value star at 9;
- Sheng value gate at 2;
- the source-matching sky star/stem placements;
- the source-matching human gates;
- the source-matching spirit sequence.

This is the first branch fixture that validates the chain from civil datetime through all four plate layers for the currently supported turning-board method.

## 7. Conditional full-plate state

A complete board is no longer globally "unverified". It is conditionally resolved:

- `FULL_PLATE_RESOLVED_SUPPORTED_METHOD`: all current builders can produce the four layers under the supported method.
- `FULL_PLATE_LOCKED_CENTER_TARGET`: value star and/or value gate currently targets center 5, where a complete target-state source fixture is still missing.

`FullPlateResolver` returns either `Resolved(FullPlate)` or `Locked(reasons)`. There is no fallback that silently manufactures the missing center representation.

A real locked datetime is also used for acceptance testing: 1995-08-13 at noon is derived from the source's Bing-Zi / Yin-8 day; Bing day noon is Jia-Wu, whose hidden Xin sits in center 5 in Yin 8. The engine must therefore lock both current value-star and value-gate center targets.

## 8. AI interpretation boundary after full-plate work

AI remains an interpretation layer, not a paipan oracle.

`FULL_PLATE` evidence is allowed only when `QimenEngine.fullPlate` is `Resolved`. If the engine returns a center-target lock, `AiInterpretationGate` must reject full-plate interpretation with `ScopeLocked`.

For a resolved chart the evidence packet may contain:

- calendar / xun / ju facts;
- earth plate;
- value star and value gate runtime facts;
- sky placements including each carried stem;
- human gates;
- spirits.

The model is not asked to rebuild those layers. Remote mode still requires explicit consent on the individual request before the evidence packet may be handed to a network adapter. `qimen-core` itself contains no provider SDK, HTTP client, or API key storage.

## 9. Acceptance matrix

Closed-loop CI runs completed during this feature chain:

- Duty engine integration: `31815923659` PASS
- AI duty evidence: `31816139108` PASS
- Center-host correction: `31816479622` PASS
- Human plate: `31816694450` PASS
- Initial sky plate: `31816919261` PASS
- Spirit plate: `31817200791` PASS
- Sky carried-stem upgrade: `31817498953` PASS
- First four-layer golden case: `31817686178` PASS
- Conditional full-plate engine resolution: `31817994318` PASS

The AI full-plate gate is accepted only after its latest real locked-chart / resolved-chart / consent tests also pass CI. Record that final run here only after GitHub Actions completes successfully.

## 10. What remains intentionally unresolved

- complete sky/human/spirit representation when the **current** value star or value gate lands at center 5;
- alternate per-xun ground-spirit method;
- Zhi-Run, Mao-Shan, Fei-Gong and true-solar-time variants;
- independent readable second-source reproduction of the same full civil-time golden chart;
- interpretation-layer question classification, Yong-Shen policy, competing priority rules, and falsification protocol.

A conditionally complete four-layer board is not the same claim as "all Qimen schools are solved". The implementation state must continue to make that distinction visible.
