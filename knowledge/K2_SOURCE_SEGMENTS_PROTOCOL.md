# K2 Composite Carrier Segmentation Protocol

版本：2026-08-27
阶段：K2B / Deep Closure
状态：ACTIVE

## 1. 为什么需要这一层

项目此前隐含了一个过强假设：`一个 canonical source_id / PDF = 一个 work = 一个 author = 一个 domain`。

QM-SRC-0023 的 185 页连续视觉复核推翻了这个假设。该载体实际包含：

- `pdf:p1-p67`：《甲遁真授秘錄（下）》/ 页内异题《甲遁真授秘集》，属于奇门 work family；
- `pdf:p68-p104`：《瑞應圖記》，独立附载作品；
- `pdf:p105-p177`：《乾坤變異錄》，独立附载作品；
- `pdf:p178-p185`：现代出版目录、版权及书目资料，不属于古籍正文作品。

因此，carrier 是物理/数字载体，work 是知识作品，两者不得再强制一一对应。

## 2. 强制分层

对已确认 composite carrier，归属顺序改为：

`CARRIER -> SEGMENT -> WORK RELATION -> AUTHOR / DOMAIN -> EVIDENCE`

禁止反向从文件名、封面总题名或 K1 单行元数据，把一个作者、领域或 work_id 自动传播到整个载体。

## 3. 数据文件

`knowledge/K2_SOURCE_SEGMENTS.jsonl`

每一行是一个经完整视觉复核后确定的、页码闭合的 carrier segment。一个 source_id 一旦进入该文件：

- 必须至少有两个 segment；
- 所有 segment 页码必须不重叠、无缺口，并完整覆盖 canonical source 的 `1..pages`；
- locator 必须落在该 segment 自己的页码范围内；
- `source_credit_scope` 固定为 `SEGMENT_ONLY`；
- 未知作者必须保持 UNKNOWN，不得从 carrier 文件名继承；
- 非六术正文可路由为 `OUT_OF_SCOPE`；出版目录等载体性材料路由为 `CARRIER_MATTER`。

## 4. 与既有 K2 Source Lineage 的关系

`K2_SOURCE_LINEAGE.jsonl` 当前是 canonical source 级的一源一 work 模型。对于 composite carrier，这个模型不足以表达真实结构。

因此：

1. segment 数据是更细粒度的事实层；
2. 在 segment-aware lineage/evidence 合同完成前，不得为了让旧 schema 通过而把整个 composite carrier 强塞给某一个 work_id；
3. QM-SRC-0023 的 source-level lineage 保持 UNKNOWN，比错误地宣称“全 185 页都是《甲遁真授秘錄》”更诚实；
4. 《甲遁真授秘錄（下）》segment 与 QM-SRC-0022 的同 work-family 关系可以在 segment 层先被记录，待 lineage schema 升级后再升格为正式 work_id 关系。

## 5. 与 Reading / Evidence 的关系

本文件记录的是**载体结构复核**，不是 Atomic Evidence，也不是 Claim。

- segment `REVIEWED` 不自动等于 Wave1 Reading Ledger `COMPLETE`；
- 在 legacy Evidence schema 仍要求 `source_id -> one work_id` 时，composite carrier 不得产生会跨 segment 错配 work/domain 的正式 Evidence；
- 后续 Evidence 必须能绑定 `segment_id` 或等价的页段归属，才可从 composite carrier 进入正式 Evidence 集；
- `Evidence != Truth != Claim` 继续成立。

## 6. 认知纪律

遇到载体结构与旧 schema 冲突时，优先修改 schema，不修改事实。

不能因为工程结构已经存在，就把新读到的材料压扁成旧结构需要的样子。

## 7. 作者归属的认识论边界

2026-08-27 对已经接受的 segment 做反向复核后，确认旧字段 `author_basis=CONTENT_VERIFIED` 容易产生一个语义越级：

> “载体内可以看到作者署名/编者归属说明”被下游误读成“历史作者身份已经得到独立验证”。

两者必须拆开：

`SOURCE INTERNAL ATTRIBUTION != HISTORICAL AUTHORSHIP VERIFICATION`

因此新增：

`knowledge/K2_SEGMENT_AUTHORSHIP_STATUS.jsonl`

作为 post-acceptance epistemic overlay。历史 `K2_SOURCE_SEGMENTS.jsonl` 不静默重写，effective segment view 在验证阶段叠加 `author_claim_status`。

当前状态定义：

- `SOURCE_INTERNAL_ATTRIBUTION`：题名页、正文署名、编者说明等只证明**这个载体如何归属作者**；
- `EXTERNALLY_VERIFIED`：保留给未来具有独立外部作者核验引用的状态；当前没有任何 accepted segment 获得该状态；
- `UNKNOWN`：没有可靠作者归属证据。

当前 fail-closed 规则：

1. `CONTENT_VERIFIED` 只能得到 `SOURCE_INTERNAL_ATTRIBUTION`；
2. `TITLE_PAGE` 也只能得到 `SOURCE_INTERNAL_ATTRIBUTION`；
3. `UNKNOWN` 不得被 overlay 提升为来源内部作者归属；
4. `EXTERNALLY_VERIFIED` 必须携带独立 `external_evidence_refs`，且不能仅依赖 `CONTENT_VERIFIED/TITLE_PAGE`；
5. 一个名字在载体里出现、一本现代汇编说“某人撰”、文件名标某作者，都不能单独解决历史真伪问题。

本轮对三条历史已接受记录做 effective 降格而非删改：

- `QM-SRC-0023#SEG-001`：薛凤祚 → `SOURCE_INTERNAL_ATTRIBUTION`；
- `QM-SRC-0024#SEG-002`：趙普 → `SOURCE_INTERNAL_ATTRIBUTION`；
- `QM-SRC-0013#SEG-002`：程道生 → `SOURCE_INTERNAL_ATTRIBUTION`。

这里“降格”只针对**作者身份信用层级**，不否定载体确实包含这些署名/归属陈述，也不改变 segment 页码、作品边界或 domain route。
