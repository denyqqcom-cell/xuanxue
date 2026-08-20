---
name: qimen-overview
description: >
  奇门遁甲受约束情境推演入口。用于定义问题、方法层/方法族、起局校准、盘式/时间体系、
  八神体系、旺衰状态体系、Role Map、结构查表、Component/Pattern、竞争解释、冻结预测与结果审计。
  调用时必须服从 CURRENT_METHOD_CONSTRAINTS.md 与 K2_PROSPECTIVE_CASE_PROTOCOL.md。
---

# 奇门解盘总览：受约束情境推演入口 v2.2

> **当前约束**：先读 `奇门/CURRENT_METHOD_CONSTRAINTS.md`。正式未知结果前瞻验证同时读取 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`。传统规则属于 SOURCE / CANDIDATE，查表一致与叙事自洽都不等于预测有效。

## 一、当前运行流程

```text
0. Reality Baseline
1. Question Domain
2. Method-Layer / Method-Family Freeze
3. Setup Calibration + Seasonal Alignment + Layout + Time Family + Deity-System Freeze
4. State-System Freeze
5. Role Map Freeze
6. Bureau / Structural Lookup
7. Eligible Feature Set
8. Component / Relation Analysis
9. Pattern Registry
10. Competing Interpretation Branches
11. Timing Freeze
12. Frozen Prediction
13. Prospective Registry
14. Optional Auxiliary Context Ablation
15. Outcome Audit
16. Rule Lifecycle Update
```

旧“明确问题→看大局→取用神→查四害→析宫盘→看生克→定应期”只保留为历史检查清单，不是通用宇宙法则。

## 二、Reality Baseline

开始前确认对象/事件/时间/地点、已知与未知、时间范围、基础概率、高风险边界以及是否 `PRE_EXPOSED`。

现实背景可以进入实际决策，但评估奇门本体时必须与 method-only 结果分离。

## 三、Question Domain + Method-Layer Freeze

先定义问题，再定义本次使用哪一个方法层：

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

一个层 miss 不得由另一层结果后救援；A/B 必须反馈前独立冻结。`RITUAL_AUXILIARY` 默认不评分。

## 四、Setup / Time / Deity Freeze

反馈前至少记录：

```text
setup_method
setup_calibration = PINGQI | DINGQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU | CHAOSHEN | ZHIRUN | JIEQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
yin_yang_dun
ju_number
layout_method
time_family = YEAR | MONTH | DAY | HOUR | NOT_APPLICABLE
deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
hour_omen_family
ritual_layer
bureau_table_source
school_context
```

梁湘潤《奇門遁甲入門》使用勾陈/朱雀，现代资料常见白虎/玄武。当前按平行 `deity_system` 保存，不静默改名、不互借象意、不结果后切换。

## 五、State-System Freeze

`qimen-gongpan` legacy 深查发现，同一文件对天蓬出现两套相反状态示例：`旺亥子/相寅卯` 与 `旺寅卯/相亥子`。

所以正式模型新增：

```text
star_state_system
door_state_system
```

- 使用旺相休囚时写明确 source/method identifier；
- 不使用写 `NOT_APPLICABLE`；
- 可评分 FROZEN model 不得留 `CONTEXT_REQUIRED`；
- 竞争系统用独立 A/B case；
- 结果后切换 state system 不能修补原预测。

## 六、Role Map Freeze

每个角色记录：

- `SOURCE_DEFINED`
- `METHOD_DEFINED`
- `CONTEXT_INFERRED`

同一对象有多个合理用神时，反馈前保存竞争 Role Map，不能结果后换用神。

## 七、Bureau / Structural Lookup

把排盘执行正确与解释有效分开：阴阳遁、局数、值符值使、星门神位置、旬空马星、source-defined bureau lookup 等只先作为结构输入。

```text
Source Fidelity != Lookup Determinism != Empirical Support
```

梁书十八局 fixture 通过只能证明来源复刻/执行完整性。

## 八、Eligible Feature Set

按方法族预先选择 IN / OUT。候选包括日时年命、事项用神、九星、八门、八神、九宫、奇仪、状态、空墓刑迫、伏吟反吟、内外盘、马星、Pattern 等。

没有全局 `开门 > 值符 > 生门 > 星神`。未进入 IN 的信息反馈后不能补入救援。

## 九、Component / Relation Analysis

`qimen-gongpan` 当前先分：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

九宫方位/五行、实际落宫等可做结构；盗贼、疾病、丧事、犯罪、死亡等传统映射属于 SOURCE symbolism，不是现实事实。

宫盘关系至少检查：

- 哪个组件绑定哪个 Role；
- 同宫/对宫/生克/比和；
- state feature 作用到谁；
- 有无相反证据；
- 去掉局部象是否改变结论；
- 是否只是把多个来源词串成故事。

取消固定 `九星→八门→八神→八卦→十干` 全局顺序，也取消“吉星+吉门+吉神=大吉”式机械加总。

## 十、Pattern Registry

`qimen-gexia` 当前区分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

十干克应保留 `(HEAVEN_STEM, EARTH_STEM)` 有序方向。格名本身不是结论；同一底层结构不能多个格名重复计票。

已有 legacy 冲突（例如朱雀投江、小格）保持 `CONFLICT_CANDIDATE`，定义不清保持 `DEFINITION_UNRESOLVED`。

## 十一、伏吟反吟、空墓刑迫

- 伏吟/反吟先识别结构，传统静/动/主客语义为 SOURCE candidate；
- 空亡、入墓、击刑、门迫先识别状态与作用对象；
- 不使用固定凶吉、百分比折扣或自动放大。

## 十二、主客、急缓与其他传统 protocol

五阳/五阴、天地盘主客、急从神/缓从门等只在对应 method family 中作为候选 protocol；必须反馈前定义和冻结，不能结果后切换。

## 十三、Competing Branches

遇到一象多义、信号冲突、流派分歧时保存 H1/H2：前提、主导证据、区分观察、失败条件。叙事连贯性只评价解释质量。

## 十四、Timing Freeze

先冻结应期方法族、eligible features、主窗口、容许度和竞争窗口。禁止结果后从空/墓/马/值使/地盘干/外应中任选一个对得上的。

内外盘结构：

- 阳遁内 `1、8、3、4`；外 `9、2、7、6`；
- 阴遁内 `9、2、7、6`；外 `1、8、3、4`。

“内快外慢”仍是待验证候选语义。

## 十五、Frozen Prediction

反馈前至少冻结：

```text
case_id
question_fingerprint_sha256
question_domain
method_family
method_layer
setup_calibration
seasonal_alignment
layout_method
time_family
deity_system
star_state_system
door_state_system
hour_omen_family
ritual_layer
bureau_table_source
role_map_sha256
eligible_features_sha256
competing_branches_sha256
timing_protocol_sha256
auxiliary_information_policy
主结论 / 竞争结论
observable success/failure criteria
freeze_timestamp
outcome_unknown_at_freeze
```

正式前瞻案例同步 `K2_PROSPECTIVE_CASE_REGISTRY.jsonl`。

允许 `INSUFFICIENT_EVIDENCE / UNSCORABLE / OUT_OF_SCOPE`。

## 十六、Auxiliary Ablation

推荐：

`method-only -> freeze -> context-augmented -> record delta`

新闻、背景、外应、其他术数的增益不能倒算给奇门本体。

## 十七、HOUR_OMEN / Ritual 隔离

九星十二时辰应克属于 `HOUR_OMEN`，需要独立预注册事件类别、时间窗、基准率与负对照。

符咒、反闭、步斗、六戊、禁敌、博奕等属于 SOURCE / ritual-history，默认不进入普通预测评分。

## 十八、高风险类象边界

传统人体/疾病、犯罪、牢狱、死亡、灾害类象可用于文献研究，但不能替代医学诊断、法律事实、金融判断或对真实人物的严重指控。

## 十九、Outcome Audit + Rule Lifecycle

错误至少区分：

`INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR / METHOD_LAYER_ERROR / SETUP_CALIBRATION_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE`

Outcome：`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`。

规则：`KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT`。

成功案例讨论基础概率与污染；失败案例不能自动用“体系天花板”解释；污染案例不能删除。

## 二十、快速导航

| 任务 | 技能 |
|---|---|
| 起局 | `qimen-qiju` |
| 取用神 | `qimen-yongshen` |
| 空墓刑迫 | `qimen-sihai` |
| 宫盘组件/关系 | `qimen-gongpan` |
| 主客生克 | `qimen-shengke` |
| 应期 | `qimen-yingqi` |
| Pattern/格局 | `qimen-gexia` |
| 基础 | `qimen-basics` |

---

*Overview v2.2 | 2026-08-21 | State-System / Component-Relation / Pattern Registry Gate 对齐*
