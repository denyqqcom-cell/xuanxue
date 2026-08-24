# Knowledge Engine Status — K2_EVIDENCE_EXTRACTION

| Domain | Engine level | Local K1 sources | K1 index | K2 readiness | Claims | Fixtures verified | Next gate |
|---|---|---:|---|---|---:|---:|---|
| 紫微 | L1_INDEXED | 148 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K2_EVIDENCE_WAVE1 |
| 八字 | L1_INDEXED | 168 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K2_EVIDENCE_WAVE1 |
| 奇门 | L1_INDEXED | 154 | PASS | READY_FOR_EXTRACTION | 0 | 0 | K2_EVIDENCE_WAVE1 |
| 六爻 | L1_INDEXED | 7 | PASS | THIN_CORPUS | 0 | 0 | K2_EVIDENCE_WAVE1 |
| 大六壬 | L1_INDEXED | 10 | PASS | THIN_CORPUS | 0 | 0 | K2_EVIDENCE_WAVE1 |
| 风水 | L1_INDEXED | 28 | PASS | READING_REQUIRED | 0 | 0 | K2_EVIDENCE_WAVE1 |

K1 已完成项目端闭环：本地 accounting、515 条 sanitized registry、attribution/source-quality、semantic routing precision、版权二进制边界与 stable core 回归均通过。六术当前统一从 `L1_INDEXED` 起跑。

K2A Source Lineage 已由项目端验收为 `COMPLETE`。当前进入 `K2_EVIDENCE_EXTRACTION`：开始逐页/逐段读取本地文本，形成页级 Evidence 与 Reading Ledger，但仍禁止把多个 Evidence 合成为 Claim。

K2B 工程执行权由项目主 Agent 持有；本地 AI 仅负责 GitHub→本地 fast-forward 同步，以及 canonical 本地资料/page packet 的定位、SHA256/页数/完整性校验和明确点名的单文件发布。它不运行测试/Gradle/instrumentation，不写代码或知识树，不做工程判断，也不 commit/push。

Wave 1 execution lanes：TEXT_DIRECT = 21；VISUAL_REQUIRED = 16；ACCESS_REVIEW = 0。SCAN/OCR_WEAK/OCR_FAIL 没有原页视觉能力时必须诚实 BLOCKED，不得用 OCR 冒充视觉核验。

Windows/WSL/Linux 的 source 定位不再依赖固定 private intake 路径；允许在显式 corpus roots 中按 official canonical SHA256 查找完全相同的源字节。文件名相似不能替代 hash identity。

Wave 1 按 work coverage 而不是文件数排程：所有 P0 work family 展开到完整 PRIMARY_WORK/WORK_PART coverage；六爻与大六壬薄 corpus 的全部 governed unique textual coverage同步进入。`claim_extraction_blocked=true` 保持。

当前 K2B 账面：unique textual coverage units = 103；semantic UNKNOWN textual backlog = 91。UNKNOWN 不会被遗忘，后续必须经过 content review 后路由或保留有依据的 UNKNOWN。

六个正式术数域当前成熟度一致；Balance Gate 已从‘限制失衡’转为‘保持同步推进’。

六爻/大六壬的 `THIN_CORPUS` 与风水的 `READING_REQUIRED` 是 K2 readiness 风险，不否定其 K1 索引完整性，但会限制后续交叉验证与解释层开放。

奇门既有 36 claims / 17 fixtures 被保留为 legacy pending re-audit，不再因为旧 handoff 自动占据高于其他五域的当前成熟度。

紫微现有 iztro fixture 属于实现 parity 证据，不计为独立传统术理真值。

Generated from `knowledge/domains/*/status.json`, `knowledge/K1_LOCAL_VALIDATION.json`, `knowledge/K2_SOURCE_LINEAGE_STATE.json`, `knowledge/K2_EVIDENCE_STATE.json` and `knowledge/PROJECT_STATE.json`; balance gate = `ENFORCE`.
