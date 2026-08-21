# QClaw 奇门执行指令 v2.3 — 受约束情境推演

> **定位**：QClaw 是方法执行器，不是“查表后必须下吉凶定论”的模板机。
>
> **上位约束**：执行前读取 `奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`、`qimen-overview/SKILL.md`。

## 第零步：执行前检查

必须确认：问题对象/时间/地点、排盘来源、前瞻或复盘、辅助信息政策、高风险边界，以及本次 `method_layer`。

若起局依赖具体算法，还必须确认：

```text
setup_method
setup_calibration
seasonal_alignment
time_boundary_system
time_family
layout_method
deity_system
star_state_system
door_state_system
```

影响模型的字段未解决时，不得猜一个能解释结果的值。

## 一、Reality Baseline

先确认对象是否存在、哪些是已知事实、真正未知目标、时间尺度、基础概率与专业安全边界。新闻/背景不是 Reality Baseline 本身；评价奇门本体时属于 auxiliary channel。

## 二、Question / Method-Layer Freeze

冻结：

```text
question_domain
method_family
method_layer = STANDARD_PLATE / TIME_FAMILY_VARIANT / HOUR_OMEN / RITUAL_AUXILIARY
```

- `RITUAL_AUXILIARY` 默认不评分；
- 一个 method layer 的 miss 不得由另一层结果后救援；
- A/B 必须反馈前独立建立 `case_id`。

## 三、Setup / Time / Deity / State-System Freeze

正式记录：

```text
setup_method = FUTOU_ZHIRUN / CHAIBU_SOLAR_TERM / MAOSHAN_SOLAR_TERM / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
setup_method_version/source
setup_calibration = PINGQI / DINGQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU / CHAOSHEN / ZHIRUN / JIEQI / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
time_boundary_system = CIVIL_MIDNIGHT / ZI_START_23 / SOURCE_DEFINED_OTHER / NOT_APPLICABLE
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
solar_term_timestamp_source
input_timezone
plate_self_check
```

### 起局红线

- 拆补、置闰、茅山不能结果后切换；
- 超神/接气旧资料存在方向冲突，未绑定具体 source algorithm 时不得自选；
- 日界/子时规则会改变干支时，不得结果后换 `time_boundary_system`；
- “顺时针/逆时针”不能替代明确宫序/旋转序列。

### 八神红线

勾陈/朱雀与白虎/玄武不得静默混用、互借象意或反馈后切换。

### 旺衰系统红线

旧 corpus 已发现九星旺相算法内部冲突：

- 使用状态时必须明确 `star_state_system / door_state_system`；
- 不使用写 `NOT_APPLICABLE`；
- 可评分 FROZEN model 不得留下 `CONTEXT_REQUIRED`；
- 竞争系统必须 A/B 预注册。

## 四、Role Map Freeze

每个角色记录 `SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED` 与理由。多个合理用神反馈前全部保存，结果后换用神只能算模型修改。

## 五、Structural Lookup

只处理机械结构：局数、值符值使、星门神落宫、旬空马星、source-defined bureau table 等。

`Source Fidelity != Lookup Determinism != Predictive Validity`。

盘程序稳定不代表预测现实有效。

## 六、Eligible Feature Set

预先确定 IN / OUT。禁止固定全局 `开门 > 值符 > 生门 > 星神`。未进入 IN 的信息结果后不得补入。仪式、符咒、博奕、禁敌默认 OUT。

## 七、Component / Relation Analysis

使用 `qimen-gongpan` 时先拆：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

不做固定星门神加总，不用旺衰当通用乘数，不把传统犯罪/疾病/死亡类象当现实事实。

## 八、Pattern Registry

使用 `qimen-gexia` 时先分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

十干克应保留 `(天盘干, 地盘干)` 有序方向。同一底层结构不得多个格名重复计票。来源内部冲突不结果后选优。

## 九、Competing Branches

多义/冲突时保存 H1/H2 的前提、主导证据、预期观察与失败条件。叙事自洽不等于经验支持。

## 十、Timing Freeze

冻结 timing method family、eligible timing features、主窗口、容许度、竞争窗口。禁止结果后从空/墓/马/值使/外应中挑命中的一个。

## 十一、Frozen Prediction

任何反馈/辅助信息加入前，至少冻结：

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
observable_success_criteria
observable_failure_criteria
freeze_timestamp
outcome_unknown_at_freeze
```

正式未知结果测试登记到 `K2_PROSPECTIVE_CASE_REGISTRY.jsonl`。

## 十二、Auxiliary Context Ablation

先 freeze method-only，再加入新闻/背景/外应/其他术数，记录 augmentation delta。外部信息带来的改善不能倒算给奇门-only。

## 十三、Outcome Audit

错误分类至少包括：

`INPUT_ERROR / PAIPAN_ERROR / ROLE_MAP_ERROR / METHOD_FAMILY_ERROR / METHOD_LAYER_ERROR / SETUP_METHOD_ERROR / SETUP_CALIBRATION_ERROR / TIME_BOUNDARY_ERROR / DEITY_SYSTEM_ERROR / STATE_SYSTEM_ERROR / FEATURE_SELECTION_ERROR / INTERPRETATION_ERROR / TIMING_ERROR / BASE_RATE_ERROR / AUXILIARY_CONTAMINATION / UNSPECIFIED_MODEL_FAILURE`

反馈后检查是否发生：

- setup method / calibration switch；
- time boundary switch；
- method layer / time family switch；
- deity / star-state / door-state switch；
- Role Map / factor / Pattern switch；
- timing-rule switch；
- external information added。

Outcome：`HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED`。污染案例不能删除。

## 十四、知识来源标注

重要结论拆成：

```text
SOURCE
INFERENCE
EMPIRICAL_SUPPORT
CONTAMINATION
```

古籍/名家/多书一致都不自动等于现实真值。

## 十五、clean-hit 红线

以下反馈后发生，本次不得计 clean hit：

1. 换 setup method / 节气校准；
2. 换日界/子时规则；
3. 换 method layer / time family；
4. 换 deity system；
5. 换 star/door state system；
6. 换 Role Map；
7. 补入未预注册 feature/Pattern；
8. 从多个应期法挑中者；
9. 借已知新闻/结果再归因奇门；
10. 排盘错误后追认；
11. 书本复盘当真实前瞻；
12. `>=3` 自动升级“已验证”；
13. HOUR_OMEN / 其他时间族 / ritual 事后救标准盘；
14. 高风险领域把术数当专业结论。

## 十六、不确定性输出

证据足够给方向；多解给竞争分支；不足可 `INSUFFICIENT_EVIDENCE`；无法评分 `UNSCORABLE`；方法不适用 `OUT_OF_SCOPE`。

不知道不是失败，结果后换轨才是方法污染。

## 十七、学习关系

`SOURCE READER -> METHOD EXECUTOR -> ADVERSARIAL REVIEW -> PROSPECTIVE REGISTRY -> OUTCOME AUDIT`

不同书、Agent、流派用于暴露盲点，不建立身份权威链。

---

*版本 v2.3 | 2026-08-21 | Setup Method / Time-Boundary / State-System 全链冻结*
