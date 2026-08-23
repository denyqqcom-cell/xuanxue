# K2 Source Stance Registry Protocol

版本：v1  
状态：ACTIVE  
适用阶段：K2B Deep Closure  
Claim Extraction：BLOCKED

## 1. 目的

解决一个在完整阅读后才暴露出来的错误：

`SOURCE_CONTAINS(rule) != SOURCE_ENDORSES(rule)`

同一作品可能同时包含：

- 对传统说法的转述；
- 作者自己的采用；
- 作者后文明确否定的旧说；
- 作者自己也保留疑问的内容。

因此以后不能再把“在某书中出现过”自动升级成“作者支持”。

## 2. 四种 source stance

### SOURCE_REPORTS

来源只是记录、转述、引用或整理某一说法。默认不得进入“作者本人方法池”。

### SOURCE_ENDORSES

来源有明确文本证据表明作者采用、主张或认可。即使如此，也只获得 source-local author-method credit，不获得 empirical credit。

### SOURCE_REJECTS

来源明确否定、批判、要求删除或判为不可采。必须从作者本人方法池排除。

### SOURCE_UNCERTAIN

完整阅读后仍无法确定作者最终立场，或者作者明确表示仍需进一步研究。按 fail-closed 处理，不进入作者本人方法池。

## 3. precedence

如果同一来源、同一 topic 在不同位置出现不同 stance，可以通过：

`stance_precedence + supersedes_stance_ids`

显式记录后出的作者立场。

允许 supersede 的前提：

- source_id 相同；
- topic_key 相同；
- 新 stance 的 precedence 严格高于旧 stance；
- evidence locator 均位于已经 COMPLETE 的视觉精读范围内。

不能通过 precedence 把不同 topic 强行合并。

## 4. author_method_pool_eligible

这是“作者方法归属”字段，不是“现实有效”字段。

硬规则：

- SOURCE_REPORTS -> false；
- SOURCE_REJECTS -> false；
- SOURCE_UNCERTAIN -> false；
- SOURCE_ENDORSES -> 可以 true，也可以因项目边界继续 false。

即使 true：

`empirical_credit = NONE`

也不代表规则可用于现实高风险决策。

## 5. 证据要求

每一条 stance 必须绑定：

- canonical source SHA；
- raw K2 work_id；
- topic_key；
- PDF page locator；
- COMPLETE deep reading；
- REVIEWED 状态。

本协议不允许只凭文件名、目录名或模型常识推断作者立场。

## 6. 初始落地：QM-SRC-0017

《奇门遁甲新述》卷十提供了第一组机器化 stance：

- 对神化起源的批判；
- 对唯心构拟“动应”的否定；
- 对符咒迷信的批判；
- 对剩余时空数理部分的科学性程度保持继续研究立场。

这些记录只表达费秉勋在该作品中的文本立场，不代表项目已经验证其结论。

## 7. Fail-closed

以下任一情况必须失败：

- REJECTS / REPORTS / UNCERTAIN 被标为 author_method_pool_eligible=true；
- empirical_credit 不为 NONE；
- evidence locator 超出完整视觉阅读页；
- source SHA 或 work_id 不匹配；
- supersedes 指向不同来源或不同 topic；
- superseding precedence 不高于被覆盖记录；
- 本地路径泄漏进知识树。
