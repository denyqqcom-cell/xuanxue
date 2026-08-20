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
| FUTOU_ZHIRUN | 符头定元，正授/超神/接气，必要时置闰 | SOURCE_REVIEW_REQUIRED | 超神/接气定义在 legacy file 内反转 |
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

Status:

`SOURCE_INCONSISTENCY / TERMINOLOGY_DIRECTION_CONFLICT`.

Required resolution: page-level verification per source, retaining source-specific terminology if authors genuinely differ.

## 4. Conflict QJ-02 — 拆补算法描述不一致

Legacy simple model:

`节气1-5日上元 / 6-10日中元 / 11-15日下元`.

Legacy detailed model:

`残上→中→下→补上` or `残下→上→中→补下`.

These are not automatically the same algorithm.

Status:

`SOURCE_INCONSISTENCY / ALGORITHM_VARIANT_REQUIRED`.

## 5. Conflict QJ-03 — 拆补与茅山定义重叠

Legacy descriptions for both methods emphasize actual solar-term arrival and no ordinary futou adjustment. The file does not give enough distinct executable rules.

Status:

`DEFINITION_OVERLAP_UNRESOLVED`.

Do not create artificial A/B variants until source definitions are sufficiently distinct.

## 6. Conflict QJ-04 — 子时 / day-boundary rule

Legacy file contains:

- “20点~23点为晚子时”;
- “23-24点为晚子时算次日”.

Status:

`INTERNAL_TIME_BOUNDARY_CONFLICT`.

Operational response: introduce `time_boundary_system`; no scored case may switch it after outcome.

## 7. Conflict QJ-05 — palace order vs clockwise language

Legacy file describes the fixed nine-palace number list as both clockwise and counter-clockwise depending on yin/yang, and describes stem distribution using “顺时针/逆时针” without defining the exact sequence.

Status:

`IMPLEMENTATION_AMBIGUITY`.

Required decomposition:

- `PALACE_NUMBER_ORDER`
- `GEOMETRIC_ROTATION_ORDER`
- `SOURCE_DEFINED_SEQUENCE`

No implementation should infer one from another.

## 8. Conflict QJ-06 — 值使落宫 vs 八门门序

Legacy file says both:

- 值使门随时支按阳顺阴逆运转；
- 八门永远顺时针转排，不论阴阳遁。

This may describe different layers, but the old wording does not prove that distinction.

Status:

`SEMANTIC_LAYER_AMBIGUITY`.

Future algorithm spec separates:

`chief_door_position_rule / door_sequence_rule / rotation_direction_rule`.

## 9. Provenance correction

Legacy `《奇门遁甲应用学》佚名` is corrected at runtime to **王云鹏** based on K2 verified metadata.

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

## 11. Prospective implication

A clean prospective model must freeze at least:

- `setup_method`
- `setup_calibration`
- `seasonal_alignment`
- `time_boundary_system`
- `time_family`
- `layout_method`

If two choices lead to different plates, both models must be registered before feedback if compared.

## 12. Experimental priorities

1. source-faithful executable specs for setup variants;
2. boundary timestamps around solar-term transitions and day boundaries;
3. setup divergence rate;
4. downstream prediction divergence rate;
5. wrong-setup / permuted structural controls;
6. only later compare outcome calibration.

*Migration audit v1 | 2026-08-21*
