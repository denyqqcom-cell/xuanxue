# QM-SRC-0015 Deep Reading & Lineage Correction Closure

版本：2026-08-23  
状态：SOURCE_REVIEW_ACCEPTED  
Claim Extraction：BLOCKED  
Empirical credit：NONE

## 1. Canonical identity

Source：QM-SRC-0015  
K1 label：《奇门遁甲吉凶占断教程》  
SHA256：`fce0db0c5cf1e2b7af2701c7df59d27b2255bdaba03d14d9b42ca4243907d587`  
PDF coverage：53/53，VISUAL_PAGE，COMPLETE。

## 2. 本轮最先纠正的不是规则，而是“这到底是不是一本独立书”

旧 K2A lineage 把 QM0015 标成：

`PRIMARY_WORK / WORK-000223`

完整视觉阅读后，这个判断不能继续保留为 effective lineage。

视觉页证：

- PDF p1 的原书印刷页码为 257；
- PDF p53 的原书印刷页码为 309；
- 页侧持续出现 `第三篇 奇门遁甲吉凶占断`；
- 同一页侧持续出现 parent work 标识 `超级神算`。

因此 canonical carrier 实际是更大作品中的完整第三篇，而不是一部独立完整作品。

本轮没有直接篡改历史 K2A raw lineage，而新增 correction overlay：

`PRIMARY_WORK -> WORK_PART`

part label：`第三篇 奇门遁甲吉凶占断`  
parent work title：`超级神算`  
work_id 暂保留 `WORK-000223`，直到未来发现 parent work 的其他 canonical carrier 再做 family merge。

## 3. 53 页内容结构

该篇自身从第一章到第五章闭合：

1. 奇门遁甲入门；
2. 奇门遁甲基础知识；
3. 奇门遁甲如何排盘；
4. 奇门遁甲占断；
5. 奇门占法应用。

第四章开始给出占断总述、主客论、`急则从神缓从门`，随后大篇幅排列十干、八门、八卦、奇仪、格局等克应规则。

第五章再按问题域展开婚姻生育、工作求学、疾病、人生机遇、经营求财、刑事官司、军事体育、天气地理、失人失物等应用。

## 4. 本书最值得保留的不是静态吉凶表

PDF p22 的占断总述明确承认：人与事、自然环境和时空条件都在变化，因此不能简单把同一固定公式套到所有事情上，必须具体分析。

PDF p24 的主客论也不是单一主客口诀，而是同时列出时间、格局与天地盘生克等判断路径。

这与第四章随后密集的固定克应表形成明显张力：

> 规则很多，但来源自己也不支持无条件机械套表。

因此项目不把这 53 页转成一个更大的“吉凶字典”，而把规则表降为 candidate rule pool。

## 5. 来源自己的自我限制

第五章涉及大量现实领域，但 PDF p51 明确提醒，上述若干预测情形并不能完全相信，奇门遁甲只能作为一种预测参考，现实生活仍要依据真实资料作选择与判断。

这条自我限制比任何一个单独吉凶条目更重要，因为它直接约束 operational use。

因此本轮明确：

- 医疗/疾病：NOT OPERATIONAL；
- 婚育胎儿性别：NOT OPERATIONAL；
- 刑事嫌疑、案件归责：NOT OPERATIONAL；
- 官司诉讼：NOT OPERATIONAL；
- 军事：NOT OPERATIONAL；
- 经营求财：不得仅凭术数文本操作资金。

## 6. 对 QCIC 的新修正

QM0015 暴露出一个此前尚未独立建模的问题：**Rule Table Density**。

当一本资料连续列出大量克应与应用规则时，即使解释者完全不“改规则”，只要允许他在整个规则库中搜索，也会产生巨大的事后命中空间。

所以 QCIC 从 v0.1 迭代到 v0.2，增加：

- Rule Table Density Gate；
- Rule Search Entropy；
- `candidate_rules_count`；
- `eligible_rules_count`；
- `rule_reduction_ratio`。

即：

`书里存在的规则 != 本题允许调用的规则`

必须在反馈前完成规则资格筛选。

## 7. 本轮自我反省

前一阶段有一个明确误区：

> K1 文件名 + K2A 题名判断，一旦被 acceptance，就容易在后续被当成稳定 work identity。

QM0015 证明这是错的。Deep Reading 的职责不能只读内容，还必须具有反向修正 metadata / lineage 的权力。

所以知识链现在进一步变成：

`CANONICAL SOURCE -> RAW LINEAGE -> VISUAL DEEP READING -> LINEAGE CORRECTION OVERLAY -> EFFECTIVE LINEAGE -> DISTILLATE`

这比直接把历史数据改掉更可审计，也比“acceptance 后永不修正”更接近持续学习。

## 8. Closure

**QM0015_DEEP_READING_COMPLETE**  
**QM0015_RAW_LINEAGE_ERROR_FOUND**  
**QM0015_EFFECTIVE_LINEAGE_WORK_PART**  
**QM0015_DEEP_SOURCE_PART_REVIEW_ACCEPTED**  
**QCIC_v0.2_CANDIDATE_UNTESTED**

仍然不是：

`QM0015_RULES_VALIDATED`  
`EMPIRICAL_CREDIT_GRANTED`  
`CLAIM_EXTRACTION_OPEN`
