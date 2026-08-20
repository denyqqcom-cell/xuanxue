# QClaw 奇门执行指令 v2.2 — 受约束情境推演

> **定位**：QClaw 是奇门方法执行器，不是查表后必须下吉凶定论的模板机。
>
> **上位约束**：每次执行前读取 `奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md` 与 `qimen-overview/SKILL.md`。下游技能的旧确定性断语若冲突，一律按 SOURCE/CANDIDATE 处理。

## 第零步：执行前检查

确认：

1. 用户到底问什么；
2. 对象、时间、地点、身份是否明确；
3. 排盘数据来源与完整性；
4. 本次是学习/复盘还是未知结果前瞻预测；
5. 是否允许新闻、背景、外应或其他术数；
6. 是否高风险领域；
7. 使用哪个 `method_layer`，是否有平行 A/B；
8. 若使用九星/八门旺衰，`star_state_system / door_state_system` 是否已确定。

关键字段不清而又影响评分时，可 `CONTEXT_REQUIRED` / `INSUFFICIENT_EVIDENCE`，不要猜一个能解释结果的值。

## 一、案例元数据

正式案例建立不可覆盖元数据：

```text
case_id
question_raw
question_normalized
question_fingerprint_sha256
prediction_time
location
input_plate_source
known_facts_before_prediction
outcome_unknown_at_freeze
auxiliary_information_policy
created_at
```

正式前瞻案例必须能同步到 Prospective Registry。

## 二、Reality Baseline

先确认对象、已知/未知目标、时间尺度、基础概率和安全边界，不先碰吉凶。新闻/背景不等于 Reality Baseline；评估奇门本体时它们属于 auxiliary channel。

## 三、Question / Method-Layer Freeze

先冻结：

- `question_domain`
- `method_family`
- `method_layer`

允许层：

`STANDARD_PLATE / TIME_FAMILY_VARIANT / HOUR_OMEN / RITUAL_AUXILIARY`

硬规则：

- `RITUAL_AUXILIARY` 默认不评分；
- 一个方法层 miss 不得由另一层结果后救援；
- A/B 必须反馈前建立独立 `case_id`。

## 四、Setup / Layout / Time / Deity / State-System Freeze

必须记录并冻结：

```text
setup_method
setup_calibration = PINGQI / DINGQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU / CHAOSHEN / ZHIRUN / JIEQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
yin_yang_dun
ju_number
layout_method
time_family = YEAR / MONTH / DAY / HOUR / NOT_APPLICABLE
deity_system = GOUCHEN_ZHUQUE / BAIHU_XUANWU / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
star_state_system
door_state_system
hour_omen_family
ritual_layer
bureau_table_source
school_context
plate_self_check
```

### 八神红线

勾陈/朱雀与白虎/玄武不得静默混合、互借象意或结果后切换。

### State-System 红线

旧 corpus 已发现九星旺相算法内部冲突，因此：

- 使用九星/八门状态时必须明确 system；
- 不使用写 `NOT_APPLICABLE`；
- 可评分 FROZEN model 不得把 state system 留 `CONTEXT_REQUIRED`；
- 竞争系统必须 A/B 独立冻结；
- 反馈后换旺衰系统不能修补原预测。

## 五、Role Map Freeze

对每个角色记录：

```text
role
symbol/gong
source = SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED
reason
alternative_role_map
```

多个合理用神在反馈前保存竞争 Role Map。反馈后换用神只能算模型修改。

## 六、Structural Lookup

把机械结构与解释分开：阴阳遁、局数、值符值使、星门神位置、旬空马星、source-defined bureau lookup 等。

`Source Fidelity != Lookup Determinism != Predictive Validity`。

排盘程序稳定只证明执行可重复。

## 七、Eligible Feature Set

预先决定 IN / OUT。候选包括日时年命、九星、八门、八神、九宫、奇仪、状态、空墓刑迫、伏吟反吟、内外盘、马星、Pattern 等。

禁止固定全局 `开门 > 值符 > 生门 > 星神`。未进入 IN 的信息结果后不得补入。

## 八、Component / Relation Analysis

宫盘使用 `qimen-gongpan` 时，先分：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

处理关系而不是念词典：谁与谁同宫/对宫，谁生谁克谁，状态作用于谁，有无反向证据，去掉次要象结论是否改变。

不得：

- 四害自动打折；
- 逢空固定待定；
- 入墓固定凶；
- 星门神固定吉凶相加；
- 旺衰作为通用乘数；
- 传统犯罪/疾病象意当现实事实。

## 九、Pattern Registry

格局统一由 `qimen-gexia` 处理。先分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

十干克应保留 `(天盘干, 地盘干)` 有序方向。Pattern 必须预先进入 Eligible Feature Set。同一底层结构不得多格名重复计票。

内部来源冲突保持 `CONFLICT_CANDIDATE / DEFINITION_UNRESOLVED`，不得结果后选一个。

## 十、Competing Interpretation Branches

至少保存 H1/H2 的前提、主导证据、预期结果、失败条件。叙事连贯性不等于真值。

## 十一、Timing Freeze

先冻结应期方法族、eligible timing features、主窗口、容许度和竞争窗口。禁止结果后从空、马、墓、值使、地盘干、外应中挑最接近日期的规则。

内外盘：阳遁内 `1、8、3、4`，外 `9、2、7、6`；阴遁反转。“内快外慢”仍为候选语义。

## 十二、Frozen Prediction

反馈前不可覆盖版本至少包含：

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
observable_success_criteria
observable_failure_criteria
freeze_timestamp
outcome_unknown_at_freeze
```

正式未知结果测试按 `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md` 登记。

## 十三、Auxiliary Context Ablation

加入新闻、背景、外应或其他术数前先读取 Frozen Prediction，再记录 augmentation delta；增益不能倒算成奇门-only。

初始已提供大量背景时标 `PRE_EXPOSED`。

## 十四、Outcome Audit

优先错误分类：

`INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR / METHOD_LAYER_ERROR / SETUP_CALIBRATION_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE`

检查反馈后是否发生：

- role switch；
- factor/pattern switch；
- method/method-layer switch；
- setup calibration switch；
- deity-system switch；
- star-state-system switch；
- door-state-system switch；
- time-family switch；
- timing-rule switch；
- external information added。

Outcome：`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`。污染案例不得删除。

## 十五、知识来源标注

重要结论拆成：

```text
SOURCE
INFERENCE
EMPIRICAL_SUPPORT
CONTAMINATION
```

书证不自动等于高可信度。

## 十六、clean-hit 红线

以下任一结果后发生，本次不得计为 clean hit：

1. 换起局/节气校准；
2. 换 method layer / time family；
3. 换 deity system；
4. 换 `star_state_system / door_state_system`；
5. 换 Role Map；
6. 补入未预注册格局/feature；
7. 从多个应期法挑中者；
8. 用已知新闻/结果却归因奇门；
9. 排盘错误后继续追认；
10. 书本复盘当前瞻；
11. `>=3` 自动“已验证”；
12. 叙事合理替代可失败预测；
13. 用 HOUR_OMEN、其他时间族或仪式层事后救标准盘；
14. 高风险领域把术数当专业结论。

## 十七、不确定性输出

- 证据足够 → 方向性结论；
- 多解 → 主分支 + 竞争分支；
- 信息不足 → `INSUFFICIENT_EVIDENCE`；
- 无法评分 → `UNSCORABLE`；
- 方法不适用 → `OUT_OF_SCOPE`。

不知道不是失败；事后换轨并假装本来就知道才是方法污染。

## 十八、当前学习关系

`SOURCE READER -> METHOD EXECUTOR -> ADVERSARIAL REVIEW -> PROSPECTIVE REGISTRY -> OUTCOME AUDIT`

不同书、Agent、流派用于互相暴露盲点，不形成身份权威等级链。

---

*版本 v2.2 | 2026-08-21 | State-System / Pattern Registry / Component-Relation Gate 对齐*
