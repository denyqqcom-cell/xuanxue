# K2 Post-Acceptance Lineage Correction Protocol

版本：2026-08-23  
阶段：K2B / Deep Closure  
状态：ACTIVE

## 1. 为什么不能把 K2A 当成永远不可修正

K2A 的 Source Lineage 是当时基于题名、目录、carrier 结构与已掌握内容作出的项目接受状态。Deep Reading 可能随后提供更强的页级证据，证明某个 canonical source 实际上只是更大作品的一个篇、卷、附录或节录。

此时有两个坏选择：

1. 明知旧 lineage 错了却因为“已经 acceptance”而不改；
2. 直接重写历史 K2A 数据，让后续无法知道项目曾经判断错过。

本协议采用第三种方式：

`ACCEPTED RAW LINEAGE -> REVIEWED CORRECTION OVERLAY -> EFFECTIVE LINEAGE`

历史接受数据保留；后续消费者必须读取 correction overlay 得到有效 lineage。

## 2. 数据文件

- `knowledge/K2_LINEAGE_CORRECTIONS.jsonl`
- `knowledge/schema/lineage_correction.schema.json`

每个 source 当前最多一条 active correction。未来若需要再次修正，应扩展 version/supersedes 机制，而不是静默覆盖。

## 3. 允许修正的依据

本阶段 correction 只接受 `VISUAL_PAGE`：

- canonical source 已完整进入 `K2_DEEP_READING_LEDGER.jsonl`；
- `read_status=COMPLETE`；
- `verification_mode=VISUAL_PAGE`；
- correction 的 `pdf:pN` locator 必须位于完整阅读范围内。

文件名、猜测、第三方书目列表不能单独推翻已接受 lineage。

## 4. WORK_PART 纠正

若 canonical carrier 的视觉页明确显示：

- 原书页码连续落在更大作品中间；
- 页眉/页侧/篇章标题持续标识更大作品；
- carrier 覆盖的是其中一个完整篇/卷而非独立题名作品；

则可以把 effective relation 从 `PRIMARY_WORK` 纠正为 `WORK_PART`。

这不会删除该 carrier 的 unique coverage，但会取消把它作为一部完整独立作品重复计票的资格。

## 5. QM-SRC-0015

完整视觉复核显示：

- PDF p1 的印刷页码为 257；
- PDF p53 的印刷页码为 309；
- 页侧持续标识 `第三篇 奇门遁甲吉凶占断` 与 `超级神算`；
- carrier 内部自身从第一章到第五章闭合，但它是更大作品中的完整“第三篇”。

因此原 K2A 的：

`PRIMARY_WORK / WORK-000223`

在 effective lineage 中纠正为：

`WORK_PART / WORK-000223 / 第三篇 奇门遁甲吉凶占断 / parent work title=超级神算`

这里保留原 work_id，是为了不在没有父作品 canonical carrier 的情况下制造新的、不可追溯的 work id；该 work_id 从此代表已识别的 parent-work family，而不是把 53 页节录当作独立完整作品。

## 6. 下游规则

- correction overlay 不改变 canonical file SHA；
- 不改变 source registry 的历史文件标签；
- deep-source distillation 必须使用 effective lineage；
- effective `WORK_PART` 必须使用 `DEEP_SOURCE_PART` scope；
- effective `WORK_PART` 必须使用 work-family single-vote policy；
- correction 只增加 provenance 正确性，不增加 empirical credit；
- Claim Extraction 继续 blocked。

## 7. 方法论意义

本纠正专门防止一种项目型错误：

> 因文件名像一本书，就把一个章节节录当成独立作品，再让它在跨来源验证时多投一票。

Deep Reading 不只是“把内容读完”，还必须有权反过来修正 K1/K2A 阶段根据元数据做出的过早判断。
