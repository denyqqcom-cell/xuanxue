# QM-SRC-0019 Deep Reading Closure

版本：2026-08-23  
状态：SOURCE_REVIEW_ACCEPTED  
Claim Extraction：BLOCKED  
Empirical credit：NONE

## 1. Canonical identity

Source：QM-SRC-0019  
K1 label：《奇门遁甲白话精解》奇行+着  
SHA256：`120a3b64b004e92e5d2acb8df5f46b5877eb70a833603aa1fca6040eb6a554bb`  
PDF coverage：114/114，VISUAL_PAGE，COMPLETE。

完整视觉页证同时修正 K1 的弱元数据：

- PDF p2 题名页：`奇门遁甲白话精解`；
- PDF p2：`奇行 编著`；
- PDF p114 版权页：广西民族出版社，1991年12月第1版。

本轮不直接覆写 K1 sanitized source registry，而通过 `K2_VERIFIED_SOURCE_METADATA.jsonl` 保存 verified overlay。

## 2. 这是一部完整独立作品

与 QM0015 不同，本书从封面、题名页、前言、目录、正文到版权页完整闭合；正文印刷页码从前言后进入第1页，至 PDF p113 的印刷 p210 标注“全文完”，PDF p114 为版权页。

现有 K2 lineage 的：

`PRIMARY_WORK / WORK-000226`

没有被视觉阅读推翻，因此本轮不创建 lineage correction。

## 3. 全书结构

目录与正文一致，主要分五章：

1. 奇门遁甲及其源流；
2. 奇门遁甲的根本观念；
3. 玄奥的奇门精典——《烟波钓叟赋》；
4. 奇门遁甲的具体预测方法；
5. 中国古代预测术评析。

前四章承担“整理、解释、排盘、应用”的教材功能，第五章则从内部对传统预测术进行批判性反思。

## 4. 本书最大的价值在第五章，而不是又增加一套口诀

PDF p109-p113 的第五章明确提出多项限制：

- 现代社会的信息、交通与技术条件变化，会使古代某些具体预测法失去现实适用性；
- 如果预测准确，才说明该方法有继续研究价值；若测不准，不应因为传统权威而继续相信；
- “尽人事”优先，不能明知可以通过努力或现实行动解决，却把预测当作替代行动的工具；
- 八卦等符号首先是抽象类别，并不天然等于某个唯一具体事物；
- 年、月、日、时输入的选择本身存在分歧，时间粒度会改变信息结构；
- 奇门内部存在不同派别、理论冲突与不合理解释，不应假装已经统一。

这些内容对项目的重要性高于继续积累更多静态吉凶条目。

## 5. 对项目旧误区的修正

前几轮阅读仍隐含一个倾向：

> 只要把角色、规则、修正项冻结，就可以开始讨论“奇门预测是否有效”。

QM0019 迫使项目再加一层更前置的限制：**现实证据和直接行动必须拥有更高优先级。**

如果一个问题已经存在可核实资料、直接观察、专业调查或可执行行动，项目不应先用术数制造一个替代答案。

因此 QCIC 从 v0.2 迭代到 v0.3。

## 6. QCIC v0.3 新增四个约束

### REALITY_EVIDENCE_GATE

先回答：

- 是否已经有可核实事实？
- 是否有可以直接采取的现实行动？
- 是否存在专业调查/测量/诊断手段？

若有，现实层先行；术数最多只能进入受控参考层。

### SYMBOL_SPECIFICITY_CEILING

八卦、门、星、神、干支默认只能生成类别、关系、状态候选。

不得从抽象符号直接跳到：

`唯一人物 / 唯一事件 / 唯一病因 / 唯一罪责 / 唯一交易结论`

具体化必须有独立现实证据或预注册关系规则。

### TEMPORAL_INPUT_SENSITIVITY

所有年/月/日/时、历法算法、边界处理与 competing timing model 必须反馈前登记，并保留并行结果。

不能事后只留下最贴近结果的那一个时间模型。

### SELF_FULFILLING_ACTION_GUARD

若预测输出改变了人的行为，后续结果就已经受到干预。

此类样本不能再当作“纯预测命中”，必须标记 intervention。

## 7. 元数据学习机制也被修正

旧 `K2_VERIFIED_SOURCE_METADATA` 只接受 Wave1 Reading Ledger 作为验证基础，这在 Deep Closure 阶段已经不合理。

QM0019 的作者与题名来自完整 VISUAL_PAGE deep reading，因此 validator 本轮升级：

`Wave1 COMPLETE` 或 `Deep Reading COMPLETE + VISUAL_PAGE`

均可作为 verified metadata 的受控来源。

这避免为了修正一个作者名而伪造 Wave1 reading credit。

## 8. 不能从本书获得的信用

本书仍然没有提供：

- 现代前瞻盲测；
- 完整失败样本；
- 对照组；
- 校准曲线；
- 可独立复现的准确率。

作者在第五章提出“应当实践、调查、检验”的方向，本身是方法论建议，不等于已经完成了这些验证。

因此：

`source_credit = FULL_SOURCE_VISUAL_REVIEWED`

但仍然：

`empirical_credit = NONE`

## 9. Closure

**QM0019_DEEP_READING_COMPLETE**  
**QM0019_VERIFIED_AUTHOR_TITLE_ACCEPTED**  
**QM0019_DEEP_SOURCE_BOOK_REVIEW_ACCEPTED**  
**QCIC_v0.3_CANDIDATE_UNTESTED**

仍然不是：

`QM0019_RULES_VALIDATED`  
`QIMEN_EMPIRICALLY_VALIDATED`  
`CLAIM_EXTRACTION_OPEN`
