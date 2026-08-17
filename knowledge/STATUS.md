# Knowledge Engine Status — K2_SOURCE_LINEAGE

| Domain | Engine level | Local K1 sources | K1 index | K2 readiness | Claims | Fixtures verified | Next gate |
|---|---|---:|---|---|---:|---:|---|
| 紫微 | L1_INDEXED | 148 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K2_LINEAGE_COVERAGE_REVIEW |
| 八字 | L1_INDEXED | 168 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K2_LINEAGE_COVERAGE_REVIEW |
| 奇门 | L1_INDEXED | 154 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K2_LINEAGE_COVERAGE_REVIEW |
| 六爻 | L1_INDEXED | 7 | PASS | THIN_CORPUS | 0 | 0 | K2_LINEAGE_COVERAGE_REVIEW |
| 大六壬 | L1_INDEXED | 10 | PASS | THIN_CORPUS | 0 | 0 | K2_LINEAGE_COVERAGE_REVIEW |
| 风水 | L1_INDEXED | 28 | PASS | READING_REQUIRED | 0 | 0 | K2_LINEAGE_COVERAGE_REVIEW |

K1 已完成项目端闭环：本地 accounting、515 条 sanitized registry、attribution/source-quality、semantic routing precision、版权二进制边界与 stable core 回归均通过。六术当前统一从 `L1_INDEXED` 起跑。

当前进入 `K2_SOURCE_LINEAGE`：先建立 underlying work / edition / commentary / note / implementation 的谱系，再开始 Evidence/Claim Extraction。`claim_extraction_blocked=true` 是有意的 fail-closed Gate。

同一本书的不同扫描、整洁版、排印版，以及由它派生的笔记/代码，不得按文件数计算为多个独立支持来源。

项目端复验发现第一版 lineage 把部分互补卷册/分页与真正的同内容版本都标成 `SAME_WORK_VARIANT`。当前必须完成 `K2_LINEAGE_COVERAGE_REVIEW`：互补卷册使用 `WORK_PART` 并保持可读；真正重复载体使用 `SAME_WORK_VARIANT + variant_of_source_id`。Claim Extraction 继续锁定。

六个正式术数域当前成熟度一致；Balance Gate 已从‘限制失衡’转为‘保持同步推进’。

六爻/大六壬的 `THIN_CORPUS` 与风水的 `READING_REQUIRED` 是 K2 readiness 风险，不否定其 K1 索引完整性，但会限制后续交叉验证与解释层开放。

奇门既有 36 claims / 17 fixtures 被保留为 legacy pending re-audit，不再因为旧 handoff 自动占据高于其他五域的当前成熟度。

紫微现有 iztro fixture 属于实现 parity 证据，不计为独立传统术理真值。

Generated from `knowledge/domains/*/status.json`, `knowledge/K1_LOCAL_VALIDATION.json`, `knowledge/K2_SOURCE_LINEAGE_STATE.json` and `knowledge/PROJECT_STATE.json`; balance gate = `ENFORCE`.
