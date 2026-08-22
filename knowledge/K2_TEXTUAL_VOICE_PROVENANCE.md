# K2 Textual Voice Provenance：文本声音、署名与传承归属分层

版本：2026-08-22
阶段：K2B / Deep Closure
状态：ACTIVE / SOURCE-DRIVEN REFINEMENT
Claim Extraction：BLOCKED
Empirical Credit：NONE

## 1. 为什么新增这一层

Deep Closure 已经通过 QM-SRC-0023、QM-SRC-0024 证明：

`one PDF != one work != one author != one domain`

继续视觉阅读 QM-SRC-0025《金函玉镜奇门遁甲秘笈全书(上)》后，又暴露出更细的 provenance 问题：**即使已经把 carrier 与 work 分开，同一页、同一卷内部仍可能同时存在多个“说话者”。**

截至当前已完成 `pdf:p1-p200` 连续视觉复核，因此以下结论只具有 PARTIAL SOURCE CREDIT，不构成整部作品闭合结论。

已直接看到：

- `pdf:p3` 题名页列“诸葛亮等著”，并另列“刘伯温点校”“陈管明注评”；这只能证明本版的题名页署名结构，不能自动证明历史作者真实性；
- `pdf:p4` 是现代出版信息页，显示中州古籍出版社及 1996 年版本信息；它属于 carrier/editorial provenance，不属于古代正文作者层；
- `pdf:p5` 序文用“相传”为张子房、诸葛武侯所著来叙述来源；“相传”本身是传统归属声明，不是经过项目验证的历史作者事实；
- `pdf:p7-p9`《奇门遁甲总序》包含黄帝、蚩尤、风后等起源叙事，这类内容首先只能获得 HISTORY/TRADITIONAL_CLAIM credit；
- `pdf:p30` 起进入《烟波钓叟歌》正文；随后多页同时出现原歌诀与明确标记的 `[白话译释]`，说明 base text 与现代解释在同一 carrier、甚至同一页并存；
- `pdf:p33-p58` 反复出现“原文/歌诀或规则 + 白话译释”的混合结构；
- `pdf:p59-p66`《十干克应诀》系统使用“天盘某干加地盘某干”的有层级、有方向组合，说明 page locator 之外还必须保留 operand 的盘层身份；
- `pdf:p68-p89` 进入九星条目，正文与白话译释持续交错，并按时序、方向及所见外应组织大量条件分支；
- `pdf:p90` 起卷四进入“三奇到宫克应吉凶”，`pdf:p94` 后又见“十干克应捷法”“八门克应总诀”等；
- `pdf:p113` 起卷五“九遁变化法”，`pdf:p126` 起卷六“奇门主客占验论”，`pdf:p144` 起卷七转入大量具体占类；
- `pdf:p151-p194` 继续按“占书馆、占访人、占出行、占囚禁、占诉讼、占疾病、占失物、占捕盗、占选妃、占求财、占婚姻”等具体场景组织规则，并持续夹有 `[白话译释]`；不同场景会改换“以何为主”、主客、门星、干支与宫位组合，不能把同一个用神优先级表套遍所有问题；
- `pdf:p195` 起进入卷十“千金诀”，`pdf:p196-p200` 又出现“三甲开阖图”“禹罡图”“兵占”等另一组方法材料，说明本 carrier 内部还存在显著章节/材料类型转换，最终 segmentation 必须等上册 383 页全读完再裁决。

因此，仅靠 `source_id + page locator` 不足以保证 Evidence 的声音归属正确；仅靠“符号名”也不足以唯一确定关系参与者，必须额外保留盘层/位置实例。

## 2. 旧模型暴露出的隐性假设

过去的 Evidence 管线仍可能默认：

`source_id -> one textual voice`

或：

`page locator -> one authorial voice`

这两个假设在注评本、校本、白话译本、汇编本中都不成立。

如果不拆 voice layer，会发生：

1. 把现代注评者的解释误算成古代原文；
2. 把题名页的“署名”误算成历史作者已经验证；
3. 把“相传”型传承叙事误算成 provenance fact；
4. 把出版者、点校者、注评者、原作者混成一个 author 字段；
5. 同一现代解释在多个古籍 carrier 中重复出现时，被错误当作独立传统共识；
6. 后续模型在不知不觉中学习的其实是现代注家的框架，而不是原始文本结构。

## 3. 新的最小 Provenance Voice 模型

今后遇到混合文本来源，至少区分以下 textual voice：

`BASE_TEXT`
- 当前被研究作品的正文、歌诀、原始条文。

`COMMENTARY`
- 注、疏、评、释、按语、解释性扩写。

`TRANSLATION_PARAPHRASE`
- 白话译释、现代转述、意译。

`EDITORIAL_FRONT_MATTER`
- 序跋、出版说明、编者说明、目录性说明。

`TITLE_PAGE_ATTRIBUTION`
- 题名页、封面所列作者/点校/注评署名；仅证明 edition attribution。

`TRADITIONAL_ATTRIBUTION_CLAIM`
- “相传某人所著”“传自某人”等传统来源说法；属于历史声明，不等于已验证作者身份。

`PUBLISHER_METADATA`
- ISBN、出版社、版次、印次、现代版权页信息。

`UNKNOWN_VOICE`
- 无法在当前阅读范围内可靠判定说话者时使用；不得强行归入 BASE_TEXT。

## 4. 作者与署名必须拆成不同问题

以后不再用一个模糊问题“这是谁写的”覆盖所有层次，而是分别问：

1. `carrier_attribution`：当前这个版本封面/题名页写了谁？
2. `segment_internal_signature`：具体 work/segment 内部是否有署名？
3. `commentary_author`：注、译、评由谁承担？
4. `traditional_authorship_claim`：来源自己声称或相传归给谁？
5. `historical_authorship_verified`：项目是否有足够独立证据确认历史作者？

只有第 5 项才允许被表述为“历史作者已验证”。前四项都不能偷换成第五项。

因此 QM-SRC-0025 当前只能说：

- 本版题名页：`诸葛亮等著 / 刘伯温点校 / 陈管明注评`；
- 序文存在“相传为张子房、诸葛武侯所著”的传统归属说法；
- **历史作者真实性：当前未验证。**

## 5. Evidence 级约束

在后续正式从 QM-SRC-0025/0026 提取 Atomic Evidence 前，必须做到：

`CARRIER -> SEGMENT/WORK -> PAGE -> VOICE_LAYER -> ATTRIBUTION -> EVIDENCE`

同一页允许产生不同 voice layer 的 Evidence，但必须分别标记，不能共享默认作者身份。

特别是：

- `[白话译释]` 不得作为 `BASE_TEXT`；
- `TITLE_PAGE_ATTRIBUTION` 不得升级为 `historical_authorship_verified`；
- `TRADITIONAL_ATTRIBUTION_CLAIM` 的 claim_readiness 默认应为 `NOT_CLAIM` 或 `CONTEXT_REQUIRED`；
- COMMENTARY / TRANSLATION_PARAPHRASE 若形成方法性解释，只能先获得该注评层的 METHOD/SOURCE credit；
- 同一注评者对多个古籍文本的重复解释不得增加 independent traditional vote；
- page locator 不足以唯一定位声音时，应增加局部段落/标签说明，或暂缓正式 Evidence；
- 对“天盘 X 加地盘 Y”这类规则，Evidence 必须保留 operand layer，不能只存 `{X,Y}`。

## 6. 对现有系统的影响

当前 K2 Evidence schema 尚未全局强制 `voice_layer` 字段。此缺口已经被真实来源暴露，因此在 schema 迁移完成前：

1. QM-SRC-0025/0026 不进入正式 Atomic Evidence；
2. 继续逐页视觉阅读可以进行，但 Reading Credit 与 Evidence Credit 分离；
3. 不因为旧 `K2_SOURCE_LINEAGE` 将二者标成 `WORK-000016 / WORK_PART`，就假设内部只有一个作品声音；
4. 完成上、下册全覆盖后，再决定是否需要 segment-level work decomposition 与 lineage 重写；
5. Claim Extraction 继续保持 BLOCKED。

## 7. 对“法—道—术”的认知修正

这次暴露的问题说明：所谓“书上写的法”，首先还要问**是谁在这一段说话**，以及**同一个符号此刻到底处于哪一盘层、哪一位置。**

如果连声音层和实例层都没有分清，就谈不上从“法”抽象“道”。

因此当前顺序应是：

`辨载体`
→ `辨作品`
→ `辨声音`
→ `辨署名性质`
→ `辨对象实例/盘层`
→ `辨规则对象与边界`
→ `辨关系结构`
→ `再谈底层约束`
→ `最后才进入场景验证`

“道”不是把不同声音、不同盘层的同名符号强行揉成一个统一口诀，而是找出在明确 provenance、对象实例、边界和情境下仍能保持稳定的约束结构。

## 8. 当前阅读状态

QM-SRC-0025：

- canonical SHA256：`08a715a13df8ff61060a15b709794732a5ab8d564965559af3c03e4b729d3016`
- canonical pages：383
- 已连续视觉复核：`pdf:p1-p200`
- 当前状态：`PARTIAL`
- Reading Credit：仅 p1-p200
- Formal Atomic Evidence：暂不生成，等待 voice provenance schema 收紧及更完整 work segmentation
- Empirical Credit：NONE

QM-SRC-0026 尚未开始语义阅读。

## 9. 可证伪/可撤销条件

本模型不是因为“分层看起来更专业”而成立。

如果后续全册阅读证明：

- `[白话译释]` 与原文不存在可稳定区分的边界；或
- 当前 carrier 实际并非多声音结构；或
- voice layer 对 Evidence 归属、冲突判断、模型复现没有任何实质影响；

则本模型应被简化。

反之，如果不区分 voice layer 会持续导致作者错配、规则时代错配、现代解释冒充古代原文或独立证据票数膨胀，则该层应升级为 fail-closed provenance gate。
