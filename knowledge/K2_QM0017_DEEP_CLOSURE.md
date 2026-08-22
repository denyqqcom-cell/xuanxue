# QM-SRC-0017 Deep Reading Closure

版本：2026-08-23  
状态：SOURCE_REVIEW_ACCEPTED  
Claim Extraction：BLOCKED  
Empirical credit：NONE

## 1. Canonical identity

Source：QM-SRC-0017  
题名：《奇门遁甲新述》  
作者：费秉勋  
SHA256：`f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`  
PDF coverage：419/419，VISUAL_PAGE，COMPLETE。

PDF p3 的版本页直接列出“奇门遁甲新述 费秉勋 著”，并显示时代文艺出版社、1991年3月第1版。目录 p8-p9 连续列出十卷，卷十正文 p414-p418 完整收束，因此本 carrier 可确认是独立完整作品；原 K2 lineage `PRIMARY_WORK / WORK-000224` 不需要修正。

## 2. 十卷结构不是十套同权规则

全书结构大致为：

1. 卷一“时家奇门十讲”：从定局、超神接气/置闰、九宫六仪三奇、八门九星八神、时辰干支、直符直使和活盘转法，到八门诸格、吉凶断要和占法举隅；
2. 卷二：《烟波钓叟歌》白话新注；
3. 卷三：十干、八门、九星、三奇到宫等克应；
4. 卷四：阴阳遁十八局活盘图及各时辰直符直使表；
5. 卷五：时家奇门阳遁五百四十定局；
6. 卷六：时家奇门阴遁五百四十定局；
7. 卷七：年、月、日家奇门；
8. 卷八：日家奇门阳遁六十定局；
9. 卷九：日家奇门阴遁六十定局；
10. 卷十：“奇门遁甲批判”。

这里出现了一个此前项目还没有独立建模的问题：**大量页面只是同一生成体系的枚举展开。**

从 PDF p114 的十八局活盘，到 p151、p209 开始的阳遁/阴遁五百四十定局，再到 p294、p354 的日家阳遁/阴遁六十定局，页面数量很大，但它们不能按“一个表项=一条独立证据”计算。

如果某个表项可以由确定的排布算法和输入机械重建，那么它增加的是 lookup coverage，而不是独立 empirical evidence。

因此：

`enumeration size != evidence sample size`

## 3. 本书最重要的页恰恰在最后：作者主动批判自己整理的传统

PDF p414 开始卷十“奇门遁甲批判”。作者并没有把前九卷整理过的所有传统材料都继续当成可信规则。

PDF p415 对奇门神化起源提出明确质疑，认为把奇门追溯到黄帝、九天玄女等神话缺乏可靠史料依据。

PDF p416 直接提出：

`唯心构拟的“动应”应当删除`

并列举一些偶然遇人、动物、声音等所谓“应验”条目，认为这些现象被牵强解释成“失发”“致败”“吉”“凶”等，缺乏真正依据。

PDF p417 进一步说，这些内容在奇门发展过程中被人为加入，应从奇门原理中删除；随后又单列“奇门中的符咒应当批判”。

PDF p418 总结说，本书已经删除许多荒诞迷信内容，但仍可能残留迷信或唯心崇拜色彩；即使是纯粹以时空数理进行客观推理的部分，其科学性达到什么程度，作者也认为仍须继续深入研究，最可靠的办法是通过实践检验真伪。

这意味着：

`SOURCE_CONTAINS(rule) != SOURCE_ENDORSES(rule)`

## 4. 新的知识工程错误：把“收录”误当“认可”

此前我们已经处理过 mixed voice、传承引录和 method layer，但还存在一个更细的错误：

一本现代作者可能为了整理传统而完整转述旧说，随后在后文明确否定其中一部分。如果数据库只记录“规则在哪一页出现”，就会把作者已经拒绝的规则重新当成作者证据。

所以本轮新增：

### Source Stance Registry

每类规则至少区分：

- `SOURCE_REPORTS`：只是记录/转述；
- `SOURCE_ENDORSES`：明确认可或采用；
- `SOURCE_REJECTS`：明确否定、批判或要求删除；
- `SOURCE_UNCERTAIN`：无法判断作者立场。

对于同一作者后出的明确批判，允许设置 `stance_precedence`。

但反过来也不能犯另一个错误：作者批判了迷信部分，并不等于剩下部分自动获得科学验证。

## 5. 大规模定局表不能制造“证据票数”

卷五、卷六各称“五百四十定局”，卷八、卷九各列六十日家定局。这种结构特别容易让知识库产生一种幻觉：

> 条目很多、图很多、页数很多，所以支持很强。

这是错的。

如果1080个时家状态是同一排布规则在1080个输入状态上的确定性展开，那么它们在方法独立性上仍然只属于同一个生成系统。

因此 QCIC v0.6 新增：

### Enumeration Compression Gate

记录：

`generative_rule_id + input_domain + enumerated_entries_count + reconstruction_test`

并执行：

`DERIVED_ENUMERATION_COLLAPSE`

只有那些无法由共同生成规则解释、真正携带新增独立假设的信息，才可能作为新的规则单元。

这也会改善未来实现：知识库不需要把数百页盘式都当作几千条“知识”，可以保存生成规则、索引键和代表性重建测试。

## 6. 来源自我批判也不是验证

《奇门遁甲新述》的卷十对项目很有价值，因为它证明传统来源内部本来就存在筛选、质疑和否定，而不是所有古说都被后人无条件接受。

但项目不能因为作者写出了“批判”二字就反向把他保留下来的部分视作科学事实。

来源自己在 p418 也没有这样声称，而是承认其科学性程度仍需继续研究，并主张通过实践检验。

因此本书获得的是：

- source-stance credit；
- method-structure credit；
- internal-critique credit；

不是：

- empirical validation credit。

## 7. 对 QCIC 的更新：v0.6

v0.6 在 v0.5 的基础上新增两个核心控制：

1. **SOURCE_STANCE_REGISTRY**：解决“书里写过”与“作者认可”的混淆；
2. **ENUMERATION_COMPRESSION_GATE**：解决“查表条目多”与“独立证据多”的混淆。

同时增加：

- `source_reported_rule_count`；
- `source_endorsed_rule_count`；
- `source_rejected_rule_count`；
- `generative_rule_count`；
- `enumerated_entries_count`。

新的原则是：

`文本覆盖度可以很高，但独立证据自由度必须被压缩到真正的生成机制与作者立场。`

## 8. 本轮自我反省

过去的学习容易有两个隐含偏差：

第一，**把书作为一个单一声音。**

事实上同一作者可以先转述、后批判；同一作品内部的 stance 会变化。如果不记录这个变化，越“完整学习”反而越可能把被作者否定的旧说重新激活。

第二，**把知识量和证据量混为一谈。**

1080个定局可以占一百多页，但如果都是一个算法的展开，它们不是1080次独立验证。

因此持续学习不应该只扩大知识库，而要不断压缩重复自由度、区分作者立场，并主动删除虚假的证据增量。

## 9. 高风险边界

卷一、卷三及定局说明中仍包含疾病、死亡、婚姻、战争、财务等传统克应。它们只能作为历史规则与候选结构研究，不能直接形成现实高风险操作结论。

卷十已经明确批判的神化起源、偶然“动应”和符咒内容，只保留传统史/文本史价值，不进入 operational rule pool。

## 10. Closure

**QM0017_DEEP_READING_COMPLETE**  
**QM0017_EFFECTIVE_LINEAGE_PRIMARY_WORK_CONFIRMED**  
**QM0017_VERIFIED_METADATA_UPGRADED**  
**QM0017_DEEP_SOURCE_BOOK_REVIEW_ACCEPTED**  
**QCIC_v0.6_CANDIDATE_UNTESTED**

仍然不是：

`QM0017_RULES_VALIDATED`  
`EMPIRICAL_CREDIT_GRANTED`  
`CLAIM_EXTRACTION_OPEN`
