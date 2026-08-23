# K2 Enumeration Compression Protocol

版本：v1  
状态：ACTIVE  
适用阶段：K2B Deep Closure  
Claim Extraction：BLOCKED

## 1. 目的

解决大型定局表、状态表、组合表造成的伪证据膨胀：

`enumeration size != evidence sample size`

如果成百上千个表项可以由同一生成规则和输入空间机械重建，那么它们增加的是查询覆盖与结构展开，不是成百上千个独立经验样本。

## 2. Derived Enumeration Collapse

凡符合以下条件的表项，执行：

`DERIVED_ENUMERATION_COLLAPSE`

条件：

- 同一来源；
- 同一方法层；
- 同一生成机制或候选生成机制；
- 表项主要由输入状态变化而展开；
- 完整视觉阅读确认其属于系统性枚举而非互不相干的独立案例。

压缩后：

- `collapsed_structure_units = 1`；
- `empirical_evidence_units = 0`；
- `source_credit = SOURCE_STRUCTURE_ONLY`；
- `empirical_credit = NONE`。

## 3. reconstruction_test_status

压缩并不等于已经证明我们能正确重建原表。

必须显式记录：

- `UNTESTED`：已经识别为生成式枚举，但尚未实现独立重建测试；
- `PASS`：预先定义的重建测试通过；
- `FAIL`：重建失败，说明压缩模型不完整或错误。

在状态为 UNTESTED 时，禁止写成“算法已验证”。

## 4. generative_rule_id

`generative_rule_id` 是知识工程中的结构标识，不等于传统规则已经现实有效。

它用于回答：

> 哪一组表项应被视为一个生成机制的展开？

而不是：

> 这个生成机制是否预测准确？

后者只能由 prospective validation 回答。

## 5. 初始落地：QM-SRC-0017

《奇门遁甲新述》完整阅读显示：

- 卷五、卷六分别展开时家阳遁540定局与阴遁540定局；
- 卷八、卷九分别展开日家阳遁60定局与阴遁60定局。

因此初始 registry 把：

- 1080个时家定局；
- 120个日家定局；

分别压缩为两个 source-structure unit。

当前 reconstruction status 保持 UNTESTED；本次只关闭“条目数=证据数”的错误，不虚报重建算法已经完成。

## 6. 与 Evidence / Claim 的边界

Enumeration Compression 只处理知识结构和证据独立性。

它不能：

- 提升 empirical credit；
- 自动产生 Claim；
- 证明某定局表现实有效；
- 用页数或条目量替代前瞻样本。

## 7. Fail-closed

以下任一情况必须失败：

- enumerated_entries_count < 2；
- collapsed_structure_units != 1；
- empirical_evidence_units != 0；
- empirical_credit 不为 NONE；
- source_credit 不为 SOURCE_STRUCTURE_ONLY；
- compression_policy 不是 DERIVED_ENUMERATION_COLLAPSE；
- evidence locator 超出 COMPLETE VISUAL_PAGE 阅读范围；
- source SHA 或 work_id 不匹配；
- 本地路径泄漏进知识树。
