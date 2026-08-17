# Knowledge Engine Status — K1_SANITIZED_IMPORT

| Domain | Engine level | Local K1 sources | K1 index | K2 readiness | Claims | Fixtures verified | Next gate |
|---|---|---:|---|---|---:|---:|---|
| 紫微 | L0_SOURCE_ONLY | 148 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K1_SANITIZED_IMPORT |
| 八字 | L0_SOURCE_ONLY | 168 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K1_SANITIZED_IMPORT |
| 奇门 | L2_CLAIM_EXTRACTED | 154 | PASS | READY_FOR_EXTRACTION | 36 | 17 | K1_SANITIZED_IMPORT |
| 六爻 | L0_SOURCE_ONLY | 7 | PASS | THIN_CORPUS | 0 | 0 | K1_SANITIZED_IMPORT |
| 大六壬 | L0_SOURCE_ONLY | 10 | PASS | THIN_CORPUS | 0 | 0 | K1_SANITIZED_IMPORT |
| 风水 | L0_SOURCE_ONLY | 28 | PASS | READING_REQUIRED | 0 | 0 | K1_SANITIZED_IMPORT |

本地 K1 Source Index 已通过项目 validator 的机器验收并完成 accounting 对账；当前剩余 Gate 是 **sanitized metadata import**。在 `knowledge/domains/*/sources.jsonl` 被导入并通过仓库端验证以前，不把本地 source 数直接冒充为仓库已吸收的 `L1_INDEXED`。

`ENGINE_MATURITY_IMBALANCE` 仍然存在：奇门已有 legacy claim/fixture，而其他领域尚未进入同等 claim maturity。这不允许用模型知识补齐，也不允许绕过六域共同 Gate。

六爻/大六壬的 `THIN_CORPUS` 与风水的 `READING_REQUIRED` 是 K2 readiness 风险，不否定其 K1 索引完整性，但会限制后续交叉验证与解释层开放。

紫微现有 iztro fixture 属于实现 parity 证据，不计为独立传统术理真值。

Generated from `knowledge/domains/*/status.json`, `knowledge/K1_LOCAL_VALIDATION.json` and `knowledge/PROJECT_STATE.json`; balance gate = `ENFORCE`.
