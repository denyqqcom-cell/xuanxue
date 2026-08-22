# QM-SRC-0020 Deep Reading Closure

版本：2026-08-23  
状态：SOURCE_REVIEW_ACCEPTED  
Claim Extraction：BLOCKED  
Empirical credit：NONE

## 1. Canonical identity

Source：QM-SRC-0020  
K1 label：《奇门遁甲秘传》姜春龙  
SHA256：`b68903c27da9ca9f8c45050ba43ecb198474e8532cd7df5e1d2a43c8c07dc7a2`  
PDF coverage：125/125，VISUAL_PAGE，COMPLETE。

本 canonical carrier 与 K1 的125页登记一致。

但完整视觉阅读发现一个必须保留的书目限制：PDF p1 直接从目录开始，正文从 PDF p10 第一章开始，PDF p125 到印刷 p230 的最后一个目录列项“五行相制法”结束；carrier 没有可见题名页、作者页或版权页。

因此本轮只接受“canonical carrier 全部正文已经读完”，**不把文件名中的作者姜春龙升级为 CONTENT_VERIFIED，也不新增 verified metadata overlay**。

## 2. 正文结构是否完整

目录从第一章到第二十三章连续闭合。关键章节包括：

- 第一章：基本认识；
- 第二章：星、门、神煞之吉凶；
- 第三章：十干克应吉凶；
- 第四章：天星值使之吉凶；
- 第五至十章：三奇九宫、门法、八门、诈遁、飞盘/换盘等；
- 第十一章：实用奇门占验分类；
- 第十二至十八章：星神门宫、格局、贵人天地将、忌法、主客、九星值时克应；
- 第十九章：用兵行军作战篇；
- 第二十章：吉凶神煞篇；
- 第二十一章：前贤妙论篇；
- 第二十二章：奇门九遁；
- 第二十三章：六甲六丁布斗篇。

PDF p125 正好结束于第二十三章目录中的最后一项“五行相制法”。所以可判断**正文 body 在本 carrier 内结构闭合**；但 bibliographic completeness 仍未知。

## 3. 这本书真正暴露的是“方法层污染”风险

该书把不同性质的方法放在同一个正文系统中：

- 排盘与算法；
- 静态吉凶/克应表；
- 一般占验；
- 主客与格局关系；
- 择用/策略；
- 用兵行军；
- 神煞、九遁；
- 六甲六丁布斗等操作/仪式内容；
- “前贤妙论”式传承材料。

如果知识工程只看到“都属于奇门”，就会把这些规则放进同一个可调用池。这样即使每一条规则都忠实抄自来源，也会形成严重的 cross-layer leakage。

所以本轮不把“全书规则更多”视为能力增加，而把它转成新的**方法层路由约束**。

## 4. 同一个“主客”也不是同一个角色

PDF p48 第十一章“奇门主客占论”非常关键。

它一方面按现实行动定义主客：别人来找我，我为主、对方为客；我去找别人，则我为客、对方为主。

另一方面，同段又使用天盘/地盘星作为彼此关系的观察层，并继续讨论我生他、他生我、我克他、他克我等关系。

这说明“主/客”至少可能同时处于不同 role frame：

- ACTOR_RELATION；
- INITIATIVE_DIRECTION；
- PLATE_LAYER。

若只记录 `role=主/客`，不同解读者很容易实际使用不同坐标系，却误以为在讨论同一规则。

## 5. 传承材料不是作者独立证据

PDF p112 起进入第二十一章“前贤妙论篇”，明确以“前贤”材料、总法天机、主客论等方式继续展开。

这些内容对研究传统方法很有价值，但它们首先是 transmission/reference evidence。

不能因为被收进这一本 carrier，就把它们重新计成一份独立的“姜春龙方法验证”。

## 6. QCIC v0.4

由此 QCIC 从 v0.3 继续迭代，新增两项核心约束。

### METHOD_LAYER_ROUTER

每条规则必须先被路由到方法层，例如：

`CALCULATION / DIVINATION / SELECTION_STRATEGY / MILITARY_OPERATIONAL / RITUAL_ESOTERIC / TRANSMITTED_REFERENCE`

本题没有授权的方法层，规则不得进入 eligible set。

默认：

`cross_layer_rule_count = 0`

如果确实需要跨层，必须在反馈前写明桥接规则、理由与失败条件。

### ROLE_FRAME_REGISTRY

角色不仅记录“是谁”，还要记录“在哪个坐标系里是谁”：

`role_label + role_frame_type + actor_mapping + directionality + plate_layer`

同名角色不因字面相同自动合并。

## 7. 本轮自我反省

之前 QCIC 已经控制：来源、现实证据、角色候选、规则密度、修正项、时间模型。

但仍潜藏一个漏洞：

> 只要规则已经被“冻结”，就默认它有资格与其他规则处在同一解释空间。

QM0020 说明这仍然不够。**冻结错误的方法层，仍然是错误。**

因此新的顺序必须是：

`PROVENANCE -> REALITY -> QUESTION -> METHOD LAYER -> ROLE FRAME -> ELIGIBLE RULES -> RELATIONAL INFERENCE`

不是先把整本奇门资料合成一个总规则池，再做筛选。

## 8. Closure

**QM0020_DEEP_READING_COMPLETE**  
**QM0020_BODY_STRUCTURE_COMPLETE_BIBLIOGRAPHY_UNVERIFIED**  
**QM0020_DEEP_SOURCE_BOOK_REVIEW_ACCEPTED**  
**QCIC_v0.4_CANDIDATE_UNTESTED**

仍然不是：

`QM0020_AUTHOR_CONTENT_VERIFIED`  
`QM0020_RULES_VALIDATED`  
`QIMEN_EMPIRICALLY_VALIDATED`  
`CLAIM_EXTRACTION_OPEN`
