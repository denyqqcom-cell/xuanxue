# qimen-gexia Pattern Registry Migration Audit

Status: ACTIVE / RUNTIME-MIGRATED / SOURCE-REVIEW-INCOMPLETE

Purpose: preserve legacy格局 knowledge while separating structure, source provenance, applicability and empirical support. This is a migration artifact, not K2 Evidence and not a claim of predictive validity.

## 1. Registry contract

Each retained pattern should be interpretable through:

- `PATTERN_TYPE`
- `STRUCTURE`
- `SOURCE_PROVENANCE`
- `TRADITIONAL_LABEL`
- `APPLICABILITY`
- `EMPIRICAL_SUPPORT`
- `OPERATIONAL_STATUS`
- `CONFLICTS`

Allowed operational statuses in this migration file:

- `SOURCE_CANDIDATE`
- `METHOD_CANDIDATE`
- `STRUCTURE_DELEGATED`
- `SOURCE_REVIEW_REQUIRED`
- `CONFLICT_CANDIDATE`
- `DEFINITION_UNRESOLVED`
- `DEPRECATED_AS_GLOBAL_RULE`

None of these means `SUPPORTED`.

## 2. Legacy entries retained as source candidates

| Legacy name | PATTERN_TYPE | STRUCTURE currently preserved | SOURCE_PROVENANCE | OPERATIONAL_STATUS | Notes |
|---|---|---|---|---|---|
| 青龙返首 / 青龙回首 | STEM_PAIR_PATTERN | 天盘戊加地盘丙 | legacy《奇门遁甲预测学》等记录 | SOURCE_CANDIDATE | 只保留有序对与传统名；不同事类解释需另审 |
| 飞鸟跌穴 | STEM_PAIR_PATTERN | 天盘丙加地盘戊 | legacy《奇门遁甲预测学》等记录 | SOURCE_CANDIDATE | 与青龙返首方向不可互换 |
| 青龙逃走 | STEM_PAIR_PATTERN | 天盘乙加地盘辛 | legacy source note | SOURCE_CANDIDATE | 不自动等于破财/失败 |
| 白虎猖狂 | STEM_PAIR_PATTERN | 天盘辛加地盘乙 | legacy source note | SOURCE_CANDIDATE | 高风险应事必须降级为传统象意 |
| 螣蛇夭矫 / 妖娇 | STEM_PAIR_PATTERN | 天盘癸加地盘丁 | legacy source note | SOURCE_CANDIDATE | 名称字形/版本待 provenance 拆解 |
| 太白入荧 | STEM_PAIR_PATTERN | 旧技能登记天盘庚加地盘丙 | legacy source note | SOURCE_REVIEW_REQUIRED | 不把“盗贼必来”等应事当事实 |
| 荧入太白 | STEM_PAIR_PATTERN | 旧技能登记天盘丙加地盘庚 | legacy source note | SOURCE_REVIEW_REQUIRED | 方向与太白入荧必须分开 |
| 大格 | STEM_PAIR_PATTERN | 旧技能登记天盘庚加地盘癸 | legacy source note | SOURCE_REVIEW_REQUIRED | 名称、适用域与应事待逐源核验 |
| 三奇得使 | COMPOSITE_PATTERN | 三奇与值使关系 | 多 legacy sources | SOURCE_REVIEW_REQUIRED | “临值使门/同宫”等具体定义需逐源确认 |
| 玉女守门 | COMPOSITE_PATTERN | 丁奇与值使关系 | 多 legacy sources | SOURCE_REVIEW_REQUIRED | 不直接推出婚姻/宴会吉 |
| 天遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy《奇门遁甲预测学》note | SOURCE_REVIEW_REQUIRED | 需完整来源/盘式上下文 |
| 地遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |
| 人遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |
| 神遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |
| 鬼遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |
| 风遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |
| 云遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |
| 龙遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |
| 虎遁 | METHOD_SPECIFIC_PATTERN | legacy composite definition | legacy source note | SOURCE_REVIEW_REQUIRED | 同上 |

## 3. Entries reclassified out of the generic “吉凶格” bucket

| Legacy name | New type | Current routing | Why |
|---|---|---|---|
| 伏吟 | STRUCTURAL_STATE | `qimen-bigpicture` | 先识别结构，不自动“利主/不利客” |
| 反吟 | STRUCTURAL_STATE | `qimen-bigpicture` | 先识别结构，不自动“利客/不利主” |
| 门迫 | STRUCTURAL_STATE | `qimen-sihai` | 是门宫关系状态，不应只作为凶格名 |
| 入墓 | STRUCTURAL_STATE | `qimen-sihai` | 需先确认干、墓位及当前方法定义 |
| 六仪击刑 | STRUCTURAL_STATE | `qimen-sihai` | 需要具体结构，不是“六仪受任何地支刑”这种泛化定义 |
| 五不遇时 | TIME_CONFIGURATION | `qimen-qiju` / `qimen-sihai` | 需具体时间干配，不等于泛化“时干克日干” |
| 天显时格 | TIME_CONFIGURATION | `qimen-qiju` / `qimen-bigpicture` | 是时间配置，不是能无条件反转伏吟的吉格 |
| 庚克甲 | METHOD/TRADITIONAL_CONCEPT | method context | 甲通常遁于六仪下，不注册成普通显式 `(庚,甲)` stem pair |

## 4. Internal source inconsistencies discovered in the legacy skill

These are preserved as research conflicts rather than silently corrected.

### 4.1 朱雀投江

Legacy file contains both:

- `丁+丙临坤、离`
- `丁+癸`

Status:

`SOURCE_INCONSISTENCY / CONFLICT_CANDIDATE`

Required next step: locate the original page for each claimed source and compare ordered pair, palace condition and terminology. Until then no operational definition is accepted.

### 4.2 小格

Legacy file contains both:

- `庚+壬 = 小格`
- `庚+己 = 小格`

Status:

`SOURCE_INCONSISTENCY / CONFLICT_CANDIDATE`

Required next step: source-specific verification. Do not choose the version that best explains a case.

### 4.3 三奇会聚

Legacy definition says `乙+丙+丁三奇齐聚同宫或相邻`.

Problems:

- “同宫” requires a layout explanation because ordinary plate structure does not simply place three heaven stems as one equivalent cell;
- “相邻” has no frozen geometric or method definition;
- the quoted mnemonic in the legacy file appears to refer to “三奇得使”, not necessarily the registered “三奇会聚” definition.

Status:

`DEFINITION_UNRESOLVED`.

### 4.4 三吉门会聚

Legacy definition says `开+休+生三吉门同宫或相近`.

Under ordinary eight-door placement, three distinct doors do not occupy one palace simultaneously.

Status:

`STRUCTURAL_CONFLICT / DEFINITION_UNRESOLVED`.

A special layout/source definition would be required before revival.

## 5. Provenance correction

The legacy skill repeatedly called `《奇门遁甲应用学》` “佚名”. K2 verified-source metadata now identifies the reviewed work as authored by **王云鹏**.

Therefore:

- future runtime references to that verified work use 王云鹏;
- old “佚名” wording is retained only as a historical migration note where needed;
- this correction is provenance-only and does not make its pattern claims true.

Other books named in the legacy file but not yet tied to page-level K2 Evidence remain `LEGACY_SOURCE_NOTE` until separately reviewed.

## 6. Deprecated global semantics

The following legacy rules are no longer operational:

- “吉格出现 → 事情顺利” as a universal rule;
- “凶格出现 → 事情凶” as a universal rule;
- multiple吉格 automatically become“大吉”;
- multiple凶格 automatically become“大凶”;
- `>=3` fixed score automatically means“大凶”;
- `>=5` fixed score automatically means“极凶”;
- “凶格叠加是相乘不是相加” as an established model;
- fixed旺相/休囚 coefficient semantics;
- fixed空墓 reduction semantics.

If a quantitative pattern model is studied later, it must define features, avoid duplicate counting, freeze weights before outcomes, calibrate against baselines and retain misses.

## 7. Duplicate-feature warning

Different traditional names can encode overlapping underlying structures. A model must not receive several votes merely because one structure appears under several labels.

Before combining patterns, record:

```text
underlying_structure_id
independence_assumption
shared_components
```

If two “凶格” are consequences of the same stem pair/state, counting both as independent evidence is prohibited unless a prospective model explicitly justifies it.

## 8. Runtime rule

For a real case, the registry is queried only after `Method-Layer / Setup / Time / Deity / Role Map / Eligible Feature` context is frozen.

A pattern contributes at most:

- a source-defined structural label;
- a context-conditioned candidate interpretation;
- a hypothesis that can fail.

It does not contribute automatic reality truth.

*Migration audit v1 | 2026-08-21*
