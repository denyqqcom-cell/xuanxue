---
name: qimen-overview
description: >
  奇门遁甲受约束情境推演入口。定义问题、方法层/方法族、起局算法、时间边界、盘式/时间体系、
  八神/旺衰体系、Role Map、结构查表、Component/Pattern、竞争解释、冻结预测与结果审计。
---

# 奇门解盘总览：受约束情境推演入口 v2.3

> **当前约束**：先读 `奇门/CURRENT_METHOD_CONSTRAINTS.md`。正式未知结果前瞻同时读取 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`。SOURCE、查表一致、叙事自洽与 Empirical Support 必须分开。

## 一、当前运行流程

```text
Reality Baseline
-> Question Domain
-> Method-Layer / Method-Family Freeze
-> Setup Method + Calibration + Seasonal Alignment Freeze
-> Time-Boundary + Time-Family + Layout + Deity-System Freeze
-> State-System Freeze
-> Role Map Freeze
-> Bureau / Structural Lookup
-> Eligible Feature Set
-> Component / Relation Analysis
-> Pattern Registry
-> Competing Branches
-> Timing Freeze
-> Frozen Prediction
-> Prospective Registry
-> Auxiliary Ablation
-> Outcome Audit
-> Rule Lifecycle
```

## 二、Reality Baseline

确认对象/事件/时间/地点、已知与未知、时间范围、基础概率、高风险边界、是否 `PRE_EXPOSED`。现实背景若用于实际决策可以加入，但评价奇门本体时必须与 method-only 分开。

## 三、Question Domain + Method Layer

先定义问题，再冻结：

`STANDARD_PLATE / TIME_FAMILY_VARIANT / HOUR_OMEN / RITUAL_AUXILIARY`

一个层 miss 不得由另一层结果后救援。A/B 反馈前独立冻结。RITUAL 默认不评分。

## 四、Setup Method Gate

起局不是一个“局数”字段，而是一组算法选择。反馈前至少记录：

```text
setup_method
setup_calibration
seasonal_alignment
time_boundary_system
time_family
layout_method
bureau_table_source
```

`qimen-qiju` legacy 深查已经发现：

- 超神/接气定义在同一文件前后反转；
- 拆补存在“固定5+5+5”与“残元+补元”两套描述；
- 拆补/茅山定义高度重叠；
- 子时边界出现“20-23”与“23-24”冲突；
- 宫序与“顺时针/逆时针”语言混用。

因此当前没有默认“最正确 setup”。若这些差异影响盘，需绑定 source-specific algorithm 或并行 A/B。

## 五、Time-Boundary Gate

正式模型新增：

```text
time_boundary_system = CIVIL_MIDNIGHT / ZI_START_23 / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
```

这些只是项目上下文标签，不声明哪一个玄学上正确。结果后改变日界/子时规则不能修补原预测。

## 六、Deity-System Gate

梁湘潤书使用勾陈/朱雀，现代资料常见白虎/玄武。当前按：

`GOUCHEN_ZHUQUE / BAIHU_XUANWU / SOURCE_DEFINED_OTHER`

平行保存，不静默改名、不互借象意、不反馈后切换。

## 七、State-System Freeze

正式模型明确：

```text
star_state_system
door_state_system
```

旧 gongpan 同一文件对天蓬出现 `旺亥子/相寅卯` 与 `旺寅卯/相亥子` 两套相反示例。使用旺相休囚时必须绑定明确 source/method system；不使用写 `NOT_APPLICABLE`；可评分 FROZEN model 不得留 `CONTEXT_REQUIRED`。

## 八、Role Map Freeze

角色来源标：`SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED`。多个合理用神反馈前保存竞争 Role Map，不得结果后换用神。

## 九、Bureau / Structural Lookup

机械结构与解释分开。候选包括阴阳遁/局数、值符值使、星门神位置、旬空马星、source-defined bureau lookup。

`Source Fidelity != Lookup Determinism != Empirical Support`。

梁书十八局 fixture 即使实现全对，也不能证明预测有效。

## 十、Eligible Feature Set

按方法族预先选择 IN / OUT。没有全局 `开门 > 值符 > 生门 > 星神`。未进入 IN 的信息反馈后不能补入。

## 十一、Component / Relation Analysis

`qimen-gongpan` 先分：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

取消固定 `九星→八门→八神→八卦→十干` 顺序与“吉星+吉门+吉神=大吉”机械加总。传统犯罪、疾病、死亡、灾害类象不是现实事实分类器。

## 十二、Pattern Registry

`qimen-gexia` 先分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

十干克应保留 `(HEAVEN_STEM, EARTH_STEM)` 有序方向。同一底层结构不得多格名重复计票；来源冲突保留 `CONFLICT_CANDIDATE`。

## 十三、空墓刑迫 / 伏吟反吟

先识别结构与作用对象，不做固定凶吉、百分比折扣或自动放大。传统静/动、主客等语义属于 SOURCE candidate。

## 十四、Competing Branches

多义/流派冲突时保存 H1/H2：前提、主导证据、区分观察、失败条件。叙事连贯性不等于 Empirical Support。

## 十五、Timing Freeze

先冻结 timing method、eligible features、主窗口、容许度与竞争窗口。禁止结果后从空/墓/马/值使/外应中挑一个对得上的。

阳遁内 `1、8、3、4`、外 `9、2、7、6`；阴遁反转。“内快外慢”仍待验证。

## 十六、Frozen Prediction

至少冻结：

```text
case_id
question_fingerprint_sha256
question_domain
method_family
method_layer
setup_method
setup_calibration
seasonal_alignment
time_boundary_system
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
observable success/failure criteria
freeze_timestamp
outcome_unknown_at_freeze
```

正式前瞻同步 Prospective Registry。允许 `INSUFFICIENT_EVIDENCE / UNSCORABLE / OUT_OF_SCOPE`。

## 十七、Auxiliary / HOUR_OMEN / Ritual 隔离

推荐 `method-only -> freeze -> context-augmented -> record delta`。

HOUR_OMEN 需要独立事件类别、时间窗、基准率、负对照。符咒/步斗/禁敌/博奕等 ritual-history 默认不进入普通评分。

## 十八、高风险边界

传统人体/疾病、犯罪、牢狱、死亡、灾害类象可用于文献研究，但不能替代医学、法律、金融或事实调查。

## 十九、Outcome Audit

错误至少区分：

`INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR / METHOD_LAYER_ERROR / SETUP_METHOD_ERROR / SETUP_CALIBRATION_ERROR / TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE`

Outcome：`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`。

Rule lifecycle：`KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT`。

## 二十、快速导航

| 任务 | 技能 |
|---|---|
| 起局 / setup registry | `qimen-qiju` |
| Role Map | `qimen-yongshen` |
| 空墓刑迫 | `qimen-sihai` |
| 宫盘组件/关系 | `qimen-gongpan` |
| 主客生克 | `qimen-shengke` |
| 应期 | `qimen-yingqi` |
| Pattern/格局 | `qimen-gexia` |
| 基础 | `qimen-basics` |

---

*Overview v2.3 | 2026-08-21 | Setup Method / Time-Boundary / State-System / Pattern & Component Registry aligned*
