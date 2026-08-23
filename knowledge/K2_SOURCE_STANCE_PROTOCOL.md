# K2 Source Stance Registry Protocol

版本：v1.1  
状态：ACTIVE  
适用阶段：K2B Deep Closure  
Claim Extraction：BLOCKED

## 1. 目的

解决完整阅读后暴露的错误：

`SOURCE_CONTAINS(rule) != SOURCE_ENDORSES(rule)`

同一作品可能同时包含传统转述、作者采用、后文否定以及作者自己仍存疑的内容。不能把“在书中出现过”自动升级成“作者支持”。

## 2. 四种 source stance

### SOURCE_REPORTS

来源只是记录、转述、引用或整理某一说法。默认不得进入作者本人方法池。

### SOURCE_ENDORSES

来源有明确文本证据表明作者采用、主张或认可。即使如此，也只获得 source-local author-method credit，不获得 empirical credit。

### SOURCE_REJECTS

来源明确否定、批判、要求删除或判为不可采。必须从作者本人方法池排除。

### SOURCE_UNCERTAIN

完整阅读后仍无法确定作者最终立场，或者作者明确表示仍需进一步研究。按 fail-closed 处理，不进入作者本人方法池。

## 3. Precedence 与唯一 effective leaf

如果同一来源、同一 topic 在不同位置出现不同 stance，通过：

`stance_precedence + supersedes_stance_ids`

显式记录后出的作者立场。

允许 supersede 的前提：

- source_id 相同；
- topic_key 相同；
- 新 stance 的 precedence 严格高于旧 stance；
- evidence locator 均位于 COMPLETE 的视觉精读范围内。

此外必须满足：

> 每一个 `source_id + topic_key` 最终恰好只有一个未被 supersede 的 effective stance leaf。

两个 individually-valid 但都未被 supersede 的 stance 仍属于歧义，必须 fail closed；下游不得自行选取较高 precedence、较新页码或较方便的一条。

## 4. author_method_pool_eligible

这是“作者方法归属”字段，不是“现实有效”字段。

硬规则：

- SOURCE_REPORTS -> false；
- SOURCE_REJECTS -> false；
- SOURCE_UNCERTAIN -> false；
- SOURCE_ENDORSES -> 可以 true，也可以因其只是边界/元方法信息继续 false。

即使 true：

`empirical_credit = NONE`

也不代表规则可用于现实高风险决策。

## 5. 证据要求

每一条 stance 必须绑定：

- canonical source SHA；
- effective K2 work_id；
- topic_key；
- PDF page locator；
- COMPLETE VISUAL_PAGE deep reading；
- REVIEWED 状态。

本协议不允许只凭文件名、目录名或模型常识推断作者立场。

## 6. 当前落地

当前 gate state 已覆盖：

- QM-SRC-0015：预测可靠性存疑、现实数据优先；
- QM-SRC-0017：神化起源/偶然动应/符咒的明确否定，以及剩余科学性存疑；
- QM-SRC-0019：传统权威不足以证明有效、现实行动优先以及内部理论冲突/科学性存疑。

这些记录只表达完整阅读能够定位的来源立场，不代表项目已经验证其结论。

## 7. Fail-closed

以下任一情况必须失败：

- REJECTS / REPORTS / UNCERTAIN 被标为 author_method_pool_eligible=true；
- empirical_credit 不为 NONE；
- evidence locator 超出完整视觉阅读页；
- source SHA 或 effective work_id 不匹配；
- supersedes 指向不同来源或不同 topic；
- superseding precedence 不高于被覆盖记录；
- 同 source/topic 最终存在多个 effective leaves；
- mandatory target 的 registry rows 被删除；
- 本地路径泄漏进知识树。
