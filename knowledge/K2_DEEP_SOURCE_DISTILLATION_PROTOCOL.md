# K2 Deep Source Per-Book Distillation Protocol

版本：2026-08-23  
阶段：K2B / Deep Closure  
状态：ACTIVE

## 1. 适用范围

本层用于已经进入 `K2_DEEP_READING_LEDGER.jsonl`、完成整本 `VISUAL_PAGE` 复核，但不属于 `K2_SEGMENT_LINEAGE` 多载体 work-family 的独立 source book。

它解决一个此前尚未关闭的空档：

- Wave1 `K2_BOOK_DISTILLATES_WAVE1*` 只覆盖 Wave1 Reading Ledger；
- `K2_WORK_FAMILY_DISTILLATES*` 只覆盖上下册/分卷/composite segment work family；
- 课程体系中的单本基础讲义、高级讲义、摘要汇编虽然已经完整阅读，却没有正式的 per-book deep closure。

因此新增：

`DEEP_READING -> DEEP_SOURCE_DISTILLATE -> SOURCE_REVIEW_ACCEPTANCE`

这仍然不是 Claim Extraction。

## 2. 数据文件

- `knowledge/K2_DEEP_SOURCE_DISTILLATION_STATE.json`
- `knowledge/K2_DEEP_SOURCE_DISTILLATES.jsonl`
- `knowledge/schema/deep_source_distillate.schema.json`

每个目标 source 只能有一条 deep-source distillate。

## 3. 与其他 Distillate 层的关系

### 3.1 已有 Wave1 distillate

若 source 以前已有 `K2_BOOK_DISTILLATES_WAVE1*`，deep closure 不删除或篡改旧 distillate；必须通过 `prior_distillate_refs` 明确承接。

这允许完整视觉重读、course provenance、Evidence re-audit 后对项目理解做二次修正，同时保留原始审计链。

### 3.2 Work-family source

只要 source 已进入 `K2_SEGMENT_LINEAGE.jsonl`，就不得再走本层；它应由 `K2_WORK_FAMILY_DISTILLATES*` 关闭，避免 PDF-centric 与 family-centric 两套信用重复。

### 3.3 Course provenance

若 source 已进入 `K2_COURSE_LINEAGE.jsonl` 且 `independent_vote_allowed=false`：

- deep-source distillate 必须记录相同 `course_family_id` / `course_role`；
- `independence_policy=COURSE_FAMILY_SINGLE_VOTE`；
- per-book 完整阅读可以增加 unique coverage，但不能变成第二、第三张独立来源票。

## 4. Acceptance 的含义

`K2B_SOURCE_REVIEW_ACCEPTED` 只表示：

- canonical source 身份已锁定；
- p1-pN 已完整视觉复核；
- 整本结构、限制、冲突与项目学习已经完成 distillation；
- 课程依赖、旧 distillate、re-audit 等下游关系已被接入。

它**不**表示：

- 书中规则真实；
- 作者案例已经验证；
- 同课多本可独立互证；
- 可以进入医疗、金融、法律、刑事、选举、战争等现实高风险操作；
- Claim Extraction 已解锁。

固定信用：

`source_credit = FULL_SOURCE_VISUAL_REVIEWED`  
`empirical_credit = NONE`

## 5. Deep-source 压缩问题

每条 distillate 必须回答：

1. 这一本书作为单独作品真正增加了什么？
2. 它的断局/取用/解释流程是什么？
3. 哪些内容只是 quick-reference、作者偏好或 retrospective case？
4. 哪些规则必须带问题域、角色、盘层、旺衰、关系与时序条件？
5. 哪些矛盾不能被项目偷偷修掉？
6. 哪些推演自由度会造成 hindsight fitting？
7. 项目自己的模型因此发生了什么可审计变化？
8. 哪些候选理论可以在反馈前冻结并真正允许失败？

## 6. Source anchors

因为 Deep Closure 并不要求把整本书再次拆成大量 Atomic Evidence，source-level distillate 使用：

`SOURCE_ID@pdf:pN`

作为整书视觉阅读的 provenance handle。

Anchor 只能指向同一 canonical source 的合法页码；不能引用另一册同课讲义来替本书作证。

## 7. Evidence re-audit 接入

如果某 source 已是 `K2_EVIDENCE_REAUDIT_STATE.json` 的 target，deep-source distillate 必须准确声明该 target 当前 coverage。

因此旧 Evidence 的“来源事实”和项目后来学会的“降权/冻结/NOT_CLAIM”会同时进入 per-book closure，而不是彼此覆盖。

## 8. 自我迭代纪律

Deep-source distillation 允许项目提出自己的模型更新，但必须满足：

- 新理论从阅读中的可观察问题长出来；
- 状态保持 `UNTESTED`；
- 写明反馈前冻结条件；
- 写明明确失败条件；
- 不能因为是项目自己的创新就获得更高信用。

本层的目标不是把书读得越来越多，而是让“读完一本书之后，项目本身也必须变得更难自欺”。
