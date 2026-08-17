# Knowledge Engine Status — K1_SEMANTIC_ROUTING_PRECISION_REVIEW

| Domain | Engine level | Local K1 sources | K1 index | K2 readiness | Claims | Fixtures verified | Next gate |
|---|---|---:|---|---|---:|---:|---|
| 紫微 | L0_SOURCE_ONLY | 148 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K1_SEMANTIC_ROUTING_REVIEW |
| 八字 | L0_SOURCE_ONLY | 168 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K1_SEMANTIC_ROUTING_REVIEW |
| 奇门 | L2_CLAIM_EXTRACTED | 154 | PASS | READY_FOR_EXTRACTION | 36 | 17 | K1_SEMANTIC_ROUTING_REVIEW |
| 六爻 | L0_SOURCE_ONLY | 7 | PASS | THIN_CORPUS | 0 | 0 | K1_SEMANTIC_ROUTING_REVIEW |
| 大六壬 | L0_SOURCE_ONLY | 10 | PASS | THIN_CORPUS | 0 | 0 | K1_SEMANTIC_ROUTING_REVIEW |
| 风水 | L0_SOURCE_ONLY | 28 | PASS | READING_REQUIRED | 0 | 0 | K1_SEMANTIC_ROUTING_REVIEW |

本地 K1 Source Index、515 条 sanitized metadata 的结构/隐私 Gate 以及 attribution/source-quality Gate 已通过；项目端最终精度复验进一步发现 **TITLE_FILENAME 路由可能被作者姓名中的术数词误触发**（典型为“紫微杨/紫微扬”），当前仍有少量高风险 source 需要回到真实文件或更强证据重新判定。当前 Gate 为 `K1_SEMANTIC_ROUTING_REVIEW`，K2 继续锁定。

`ENGINE_MATURITY_IMBALANCE` 仍然存在：奇门已有 legacy claim/fixture，而其他领域尚未进入同等 claim maturity。这不允许用模型知识补齐，也不允许绕过六域共同 Gate。

六爻/大六壬的 `THIN_CORPUS` 与风水的 `READING_REQUIRED` 是 K2 readiness 风险，不否定其 K1 索引完整性，但会限制后续交叉验证与解释层开放。

紫微现有 iztro fixture 属于实现 parity 证据，不计为独立传统术理真值。

Generated from `knowledge/domains/*/status.json`, `knowledge/K1_LOCAL_VALIDATION.json` and `knowledge/PROJECT_STATE.json`; balance gate = `ENFORCE`.
