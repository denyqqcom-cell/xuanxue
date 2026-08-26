# K2 Deep Source Per-Book / Per-Part Distillation Protocol

版本：2026-08-23  
阶段：K2B / Deep Closure  
状态：ACTIVE

## 1. 适用范围

本层用于已经进入 `K2_DEEP_READING_LEDGER.jsonl`、完成 canonical carrier 全页 `VISUAL_PAGE` 复核，但不属于 `K2_SEGMENT_LINEAGE` 多载体 work-family 的 source unit。

source unit 可以是：

- `DEEP_SOURCE_BOOK`：effective lineage 为完整独立作品；
- `DEEP_SOURCE_PART`：Deep Reading 后由 lineage correction 证明 canonical carrier 只是更大作品的完整篇/卷/节录。

因此真正的闭环是：

`DEEP_READING -> EFFECTIVE_LINEAGE -> DEEP_SOURCE_DISTILLATE -> SOURCE_REVIEW_ACCEPTANCE`

它仍然不是 Claim Extraction。

## 2. 数据文件与分片

- `knowledge/K2_DEEP_SOURCE_DISTILLATION_STATE.json`
- `knowledge/K2_DEEP_SOURCE_DISTILLATES.jsonl`
- `knowledge/K2_DEEP_SOURCE_DISTILLATES.d/*.jsonl`
- `knowledge/schema/deep_source_distillate.schema.json`

主文件与 shard 聚合后，每个 target source 只能有一条 deep-source distillate。

## 3. Effective Lineage 优先于历史 Raw Lineage

K2A 接受的 `K2_SOURCE_LINEAGE.jsonl` 是历史基线。若后续完整视觉阅读产生 `K2_LINEAGE_CORRECTIONS.jsonl`，本层必须使用 correction overlay 后的 effective lineage。

- effective `PRIMARY_WORK` -> `DEEP_SOURCE_BOOK`；
- effective `WORK_PART` -> `DEEP_SOURCE_PART`；
- effective `WORK_PART` 必须 `WORK_FAMILY_SINGLE_VOTE`，不能把篇章节录当成完整独立作品投票。

## 4. 与其他 Distillate 层的关系

### 4.1 已有 Wave1 distillate

若 source 以前已有 `K2_BOOK_DISTILLATES_WAVE1*`，deep closure 不删除或篡改旧 distillate；必须通过 `prior_distillate_refs` 明确承接。

### 4.2 Segment/work-family source

只要 source 已进入 `K2_SEGMENT_LINEAGE.jsonl`，就不得再走本层；它应由 `K2_WORK_FAMILY_DISTILLATES*` 关闭，避免 PDF-centric 与 family-centric 两套信用重复。

### 4.3 Course provenance

若 source 已进入 `K2_COURSE_LINEAGE.jsonl` 且 `independent_vote_allowed=false`：

- 必须记录相同 `course_family_id` / `course_role`；
- `independence_policy=COURSE_FAMILY_SINGLE_VOTE`；
- per-book 完整阅读可以增加 unique coverage，但不能增加第二、第三张独立来源票。

## 5. Acceptance 的含义

`K2B_SOURCE_REVIEW_ACCEPTED` 只表示：

- canonical source 身份已锁定；
- p1-pN 已完整视觉复核；
- effective lineage 已纳入；
- 整本/整篇结构、限制、冲突与项目学习已经 distill；
- 课程依赖、旧 distillate、re-audit 等关系已接入。

它不表示书中规则真实、案例已验证、可以高风险操作或 Claim Extraction 已解锁。

固定信用：

`source_credit = FULL_SOURCE_VISUAL_REVIEWED`  
`empirical_credit = NONE`

## 6. Source anchors

source-level distillate 使用：

`SOURCE_ID@pdf:pN`

Anchor 只能指向同一 canonical carrier 的合法 PDF 页。对 work part，anchor 仍使用 carrier 页码；parent work 的印刷页码只能在 synthesis 文本中作为视觉事实记录，不能伪装成 canonical locator。

## 7. Evidence re-audit 接入

如果 source 已是 `K2_EVIDENCE_REAUDIT_STATE.json` target，deep-source distillate 必须准确声明当前 coverage。旧 Evidence 与项目后来学会的降权/NOT_CLAIM 必须并存。

## 8. 自我迭代纪律

每条 distillate 必须回答：

1. 这一个 source unit 真正增加了什么？
2. 它的推演/解释流程是什么？
3. 哪些只是规则表、作者偏好或 retrospective case？
4. 哪些矛盾不能被项目偷偷修掉？
5. 哪些结构会扩大 hindsight freedom？
6. 完整阅读是否反过来推翻了早期 metadata/lineage 判断？
7. 项目自己的模型因此发生了什么可审计变化？
8. 哪些候选理论可以反馈前冻结并真正允许失败？

新理论全部保持 `UNTESTED`，不能因为是项目自己的创新就获得更高信用。
