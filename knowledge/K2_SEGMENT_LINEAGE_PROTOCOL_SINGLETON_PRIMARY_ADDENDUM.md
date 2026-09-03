# K2 Segment-Aware Work Lineage Protocol — singleton primary segment addendum

适用阶段：K2B / Deep Closure  
目的：补足现行 validator 与既有协议之间的实现缺口，不改变旧 WORK_PART family 的语义。

## A. 新增可表达对象：PRIMARY_WORK_IN_COMPOSITE

当完整 VISUAL_PAGE 阅读已经证明一个 composite carrier 的某一 reviewed segment 本身是一部完整、可区分的 embedded primary work，而不是另一作品的上/中/下册或章节 part 时，允许建立一个 **singleton segment-aware work family**。

它的合法形态必须同时满足：

- `member_kind = SEGMENT`
- `relation = PRIMARY_WORK_IN_COMPOSITE`
- reviewed `K2_SOURCE_SEGMENTS` 中同一 `segment_id` 的 relation 也必须是 `PRIMARY_WORK_IN_COMPOSITE`
- `independence_class = PRIMARY_CANDIDATE`
- `part_label = null`（不是 WORK_PART，不制造“卷一/卷二”）
- `credit_scope = SEGMENT_ONLY`
- `independent_vote_key = work_family_key`
- family 当前恰有 1 个 member
- domain_routes 不得超过 reviewed segment 的 domain_routes
- 作者如果只有载本内部题名页、编后语或编辑性归属，只能使用 `author_basis = SOURCE_INTERNAL_ATTRIBUTION`，不得升级成外部历史作者已验证。

## B. 与既有 WORK_PART family 的隔离

原有 WORK_PART family 规则保持不变：

- `relation = WORK_PART`
- `independence_class = SAME_WORK_NOT_INDEPENDENT`
- 至少 2 个 members
- 每个 member 必须有非空且不重复的 `part_label`
- members 共享 work title / domain routing，并继续执行同 work family single-vote policy。

不得把两个互相独立的 embedded works 为了满足“family 至少两成员”的旧 validator 条件，伪造成同一本书的上下册。

## C. Credit 边界

`PRIMARY_CANDIDATE` 只表示 segment-aware work identity 已足够支持“作为独立作品候选继续归一化”；它不等于：

- 外部作者学已经验证；
- 与同载体其他作品统计独立；
- method validity；
- empirical validity；
- Claim ready。

因此仍保持：

`LINEAGE CREDIT != METHOD CREDIT != EMPIRICAL CREDIT != TRUTH`

## D. Wave1 迁移边界

singleton primary segment family 可以进入 `K2_SEGMENT_EVIDENCE.jsonl`，因为现有 Segment-Bound Evidence Protocol 已支持：

`source_id + segment_id + work_family_key + locator`

但在 legacy Wave1 Reading/Book Distillate 仍强制一 source_id→一 work_id 时：

- 不伪造 source-level `work_id`；
- 不据此把 composite carrier 直接记为 Wave1 COMPLETE；
- 不自动增加 legacy Wave1 Evidence 计数；
- 先保留 segment Evidence / work identity，等待 composite-aware completion aggregation。

本补丁是 schema-follow-facts 的修正，不是为了增加完成率。
