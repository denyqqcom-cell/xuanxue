# qimen-qiju Setup Method Registry Migration Audit

Status: ACTIVE / RUNTIME-MIGRATED / SOURCE-REVIEW-INCOMPLETE

Purpose: preserve legacy setup knowledge while separating algorithm identity, solar-term calibration, seasonal alignment, time boundary, layout sequence and empirical validity.

## 1. Registry contract

A setup model is not identified by one label. Minimum identity:

```text
setup_method
setup_calibration
seasonal_alignment
time_boundary_system
time_family
layout_method
bureau_table_source
implementation_version
```

`SETUP REPRODUCIBLE != PREDICTION VALIDATED`.

## 2. Current setup-method candidates

| setup_method | Legacy description | Current status | Main unresolved point |
|---|---|---|---|
| FUTOU_ZHIRUN | 符头定元，正授/超神/接气，必要时置闰 | SOURCE_REVIEW_REQUIRED | 超神/接气已获得一条 source-specific 方向证据，但另一反向 legacy 定义来源仍未定位 |
| CHAIBU_SOLAR_TERM | 节气交接后拆补三元 | SOURCE_REVIEW_REQUIRED | “固定5+5+5”与“残元+补元”两套描述 |
| MAOSHAN_SOLAR_TERM | 完全按实际节气，不参考符头 | DEFINITION_OVERLAP_UNRESOLVED | 与 legacy 简化拆补描述高度重叠 |
| SOURCE_DEFINED_OTHER | 其他来源算法 | CONTEXT_REQUIRED | 必须给 source/version |

没有默认“推荐法”。

## 3. Conflict QJ-01 — 超神/接气方向反转

Legacy section 2:

- 超神 = 节气先到、旬首未到；
- 接气 = 旬首先到、节气未到。

Legacy section 9:

- 超神 = 上元符头在节气前；
- 接气 = 节气在前、符头在后。

原始状态：

`SOURCE_INCONSISTENCY / TERMINOLOGY_DIRECTION_CONFLICT`.

### 3.1 QM-SRC-0027 source-specific witness

`QM-SRC-0027 / WORK-000228 / 善天道《奇门遁甲精华培训教材》` PDF p4 已做原页核验。

该页明确支持：

- 超神 = 上元符头在前，节气在后；
- 接气 = 节气在前，上元符头在后；
- 置闰 = 上元符头超过节气九天。

因此当前从“纯 legacy 内部冲突”推进为：

`SOURCE_SPECIFIC_SUPPORT_ADDED / GLOBAL_CONFLICT_UNRESOLVED`。

这条证据只说明 `QM-SRC-0027` 的术语方向，不能反向证明另一套 legacy 定义必然错误，也不能宣布所有流派统一如此。

详细记录：

`knowledge/K2_SOURCE_COMPARISONS/QM-SRC-0027_SETUP_BOUNDARY.md`

Required resolution: continue page-level verification per source, retaining source-specific terminology if authors genuinely differ.

## 4. Conflict QJ-02 — 拆补算法描述不一致

Legacy simple model:

`节气1-5日上元 / 6-10日中元 / 11-15日下元`.

Legacy detailed model:

`残上→中→下→补上` or `残下→上→中→补下`.

These are not automatically the same algorithm.

Status:

`SOURCE_INCONSISTENCY / ALGORITHM_VARIANT_REQUIRED`.

`QM-SRC-0027 p4` 虽写“不置闰—拆补法（推荐方法）”，但仍没有给出足够 executable detail 去裁决上述两种算法。因此这条 source preference 不关闭 QJ-02，也不恢复任何“默认推荐法”。

## 5. Conflict QJ-03 — 拆补与茅山定义重叠

Legacy descriptions for both methods emphasize actual solar-term arrival and no ordinary futou adjustment. The file does not give enough distinct executable rules.

Status:

`DEFINITION_OVERLAP_UNRESOLVED`.

Do not create artificial A/B variants until source definitions are sufficiently distinct.

## 6. Conflict QJ-04 — 子时 / day-boundary rule

Legacy file contains:

- “20点~23点为晚子时”;
- “23-24点为晚子时算次日”.

原始状态：

`INTERNAL_TIME_BOUNDARY_CONFLICT`.

### 6.1 QM-SRC-0027 p3：真正的 split-zi witness

PDF p3 原页把时辰表明确拆成：

- `0:00-1:00` = 早子时；
- `21:00-23:00` = 亥时；
- `23:00-24:00` = 晚子时。

更有判别力的是时干表：同一“日干组”栏中，晚子时使用的子时干已经切换到下一日干组对应的五子遁结果。例如 `甲己日` 栏的早子时为 `甲子`，晚子时为 `丙子`。

当前最窄分类：

`SHANTI_DAO_JINGHUA_P3_SPLIT_ZI_HOUR_STEM_BASIS`

这是真实 source boundary witness，但它只直接约束**时干推定的 day-basis**。它尚不足以单独证明：

- 23:00 后完整日柱统一换日；
- civil date 必须整体前移；
- 所有奇门 setup 都采用 `ZI_START_23`；
- 23:00 边界后的完整星门神盘式。

因此正式模型若采用这一路径，当前更适合冻结为：

`time_boundary_system = SOURCE_DEFINED_OTHER`

并附 source/version：

`QM-SRC-0027_P3_SPLIT_ZI_HOUR_STEM`

而不是把它偷换成未经证明的全局 `ZI_START_23` truth。

### 6.2 AQ-004 状态

`SOURCE_BOUNDARY_WITNESS_FOUND / EXECUTABLE_FULL_PLATE_CONTROL_NOT_READY`

原因：目前还缺一个发生在 23:00 / 00:00 边界、且能核对完整日柱/局/星门神的 worked plate oracle。

在此之前不制造伪 `wrong-time-boundary` control。

Operational response remains: `time_boundary_system` 必须反馈前冻结；no scored case may switch it after outcome.

## 7. Conflict QJ-05 — palace order vs clockwise language

Legacy file describes the fixed nine-palace number list as both clockwise and counter-clockwise depending on yin/yang, and describes stem distribution using “顺时针/逆时针” without defining the exact sequence.

Status:

`IMPLEMENTATION_AMBIGUITY`.

Required decomposition:

- `PALACE_NUMBER_ORDER`
- `GEOMETRIC_ROTATION_ORDER`
- `SOURCE_DEFINED_SEQUENCE`

No implementation should infer one from another.

### 7.1 2026-08-21 implementation recurrence

The p21-p22 `QM-SRC-0028` worked-plate audit found that production `QimenEngine` had independently reproduced this exact conceptual error:

- the legacy star layer used the numeric `1..9` flying sequence as if it were the outer rotating-star ring;
- the legacy door layer used `zhiPalace(hour branch)` as if it were the source's xun-hour value-door count;
- the deity layer used another ad-hoc palace order;
- `天禽` was rotated as an independent ninth outer star although the worked plates carry it with `天芮`.

This is important because the **written registry already warned about QJ-05 before the implementation audit**. Written knowledge did not automatically constrain executable knowledge.

Current correction adds an explicit source-bounded profile:

`SHANTI_DAO_71_P21_P22`

with separate executable objects:

- `PALACE_NUMBER_SEQUENCE = 1..9`
- `OUTER_ROTATION_RING = 1,8,3,4,9,2,7,6`
- `HOUR_OFFSET_SEQUENCE`
- `DEITY_ORDER`

The legacy profile remains `LEGACY_EXPERIMENTAL` for A/B and backward compatibility; this correction does not declare the new profile universally true.

New engineering discipline:

**Sequence-Object Type Safety**

Any rule containing “顺 / 逆 / 飞 / 转 / 移” is incomplete until it names the sequence object being traversed. A direction word without an object is not executable knowledge.

Exact implementation audit:

`knowledge/K2_IMPLEMENTATION_AUDITS/QM-SRC-0028_SHANTI_WORKED_PLATES.md`

## 8. Conflict QJ-06 — 值使落宫 vs 八门门序

Legacy file says both:

- 值使门随时支按阳顺阴逆运转；
- 八门永远顺时针转排，不论阴阳遁。

This may describe different layers, but the old wording does not prove that distinction.

Status:

`SEMANTIC_LAYER_AMBIGUITY`.

Future algorithm spec separates:

`chief_door_position_rule / door_sequence_rule / rotation_direction_rule`.

The Shantiandao p21-p22 source-profile implementation now demonstrates why this decomposition matters: “值使随时宫”的 target calculation and “八门固定顺序”的 outer-ring rotation are two different operations.

## 9. Provenance correction

Legacy `《奇门遁甲应用学》佚名` is corrected at runtime to **王云鹏** based on K2 verified metadata.

`QM-SRC-0027` 也暴露了 filename attribution 风险：文件名含“善天道”，但 p1 页眉实际可见题名为 `善天道奇门遁甲精华培训教材`，另列 `山枫道人` 标识。当前不能直接把“善天道”或“山枫道人”静默升级成 author identity。

Other source mentions without page-level K2 review remain:

`LEGACY_SOURCE_NOTE`.

Sogou/Zhihu explanations remain:

`LEGACY_WEB_NOTE`.

They may aid source discovery but do not settle the algorithm.

## 10. Deprecated authority statements

Removed from runtime authority:

- “拆补法（推荐使用）”;
- “拆补法应用最广”;
- “置闰法严格遵古” as a reason to prefer it;
- any claim that one setup is more accurate without matched prospective comparison.

Source books may still contain these preferences. They are preserved as `SOURCE_TEACHING_PREFERENCE`, not project defaults.

## 11. Prospective implication

A clean prospective model must freeze at least:

- `setup_method`
- `setup_calibration`
- `seasonal_alignment`
- `time_boundary_system`
- `time_family`
- `layout_method`

If two choices lead to different plates, both models must be registered before feedback if compared.

`layout_method` must identify the sequence objects it actually uses; a label such as “顺转” alone is not enough for reproducibility.

For split-zi sources, the frozen packet must also preserve the exact source/version semantics in notes; `SOURCE_DEFINED_OTHER` is not permission to leave the algorithm vague.

## 12. Experimental priorities

1. source-faithful executable specs for setup variants;
2. boundary timestamps around solar-term transitions and day boundaries;
3. find a 23:00/00:00 worked plate so a deliberate wrong-boundary model can actually lose;
4. setup divergence rate;
5. downstream prediction divergence rate;
6. wrong-setup / permuted structural controls;
7. only later compare outcome calibration.

*Migration audit v1.2 | 2026-08-21*
