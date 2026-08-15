# Knowledge Engine Status — K1_CORPUS_INDEX

| Domain | Level | Sources | Claims | Fixtures verified | Next gate |
|---|---|---:|---:|---:|---|
| 紫微 | L0_SOURCE_ONLY | 0 | 0 | 0 | K1_CORPUS_INDEX |
| 八字 | L0_SOURCE_ONLY | 0 | 0 | 0 | K1_CORPUS_INDEX |
| 奇门 | L2_CLAIM_EXTRACTED | 30 | 36 | 17 | K1_CORPUS_REAUDIT |
| 六爻 | L0_SOURCE_ONLY | 0 | 0 | 0 | K1_CORPUS_INDEX |
| 大六壬 | L0_SOURCE_ONLY | 0 | 0 | 0 | K1_CORPUS_INDEX |
| 风水 | L0_SOURCE_ONLY | 0 | 0 | 0 | K1_CORPUS_INDEX |

`DOMAIN_IMBALANCE` 当前是预期状态，不代表允许继续只强化奇门。K1 的目标是六域全部达到 `L1_INDEXED`；在此之前不新增任何领域的 Interpretation production rule。

紫微现有 iztro fixture 属于实现 parity 证据，不计为本 Knowledge Engine 的独立来源吸收率。

Generated from `knowledge/domains/*/status.json`; balance gate = `ENFORCE`.
