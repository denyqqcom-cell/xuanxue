# K2 Enumeration Compression Protocol

版本：v1.3  
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

## 3. generative_rule_id 必须唯一计数

同一个生成机制即使被拆成多个不同 label，也不能得到多个 structure unit。

硬规则：

> 同一 `source_id + generative_rule_id` 只能有一条 compression row。

如果同一个生成机制横跨多个页段或多个子表，应在一条 row 的 input domain / evidence locators 中表达，而不是拆成多条增加 structure unit。

## 4. reconstruction_test_status

压缩并不等于已经证明我们能正确重建原表。

必须显式记录：

- `UNTESTED`：已经识别为生成式枚举，但尚未完成可审计重建测试；
- `PASS`：预先定义的结构重建测试通过；
- `FAIL`：结构重建测试失败，说明当前压缩模型不完整或错误。

新增硬边界：

`RECONSTRUCTION PASS != SELF-DECLARED STATUS`

registry 中单独把字符串从 `UNTESTED` 改成 `PASS` 或 `FAIL` 不构成有效测试结果。任何 PASS/FAIL 都必须有 `knowledge/K2_ENUMERATION_RECONSTRUCTION_RESULTS.jsonl` 中一条匹配、REVIEWED、可审计的 result artifact。

result artifact 必须绑定：

- source / work / canonical SHA；
- compression_id / generative_rule_id；
- algorithm spec ID + SHA256；
- fixture set ID + SHA256；
- source checkpoints；
- checked / matched state counts；
- PASS 或 FAIL；
- `scope = SOURCE_STRUCTURE_REPRODUCIBILITY_ONLY`；
- `empirical_credit = NONE`；
- `claim_extraction_blocked = true`。

PASS 必须满足所有已登记 checked states 均匹配。FAIL 必须至少有一个已检查 state 不匹配。

当前 contract 暂不允许同一 source/generative_rule_id 同时存在多个正式 result row；未来若需要保留多轮测试历史，应先增加显式 supersession/effective-leaf 机制，不能静默覆盖。

## 5. PASS 的语义上限

即使 reconstruction PASS，也只能说明：

> 在冻结的 algorithm spec 与 fixture set 下，已检查的来源结构状态可以被重现。

它不能说明：

- 传统规则具有现实预测效度；
- 书中解释文字、克应文字或应用断语都已被算法重建；
- 未检查的全部表项已无条件证明正确；
- empirical credit 可以升级；
- Claim Extraction 可以开放。

因此：

`SOURCE STRUCTURE REPRODUCIBLE != REAL-WORLD PREDICTIVE VALIDITY`

## 6. generative_rule_id 的语义

`generative_rule_id` 是知识工程中的结构标识，不等于传统规则已经现实有效。

它用于回答：

> 哪一组表项应被视为一个生成机制的展开？

而不是：

> 这个生成机制是否预测准确？

后者只能由 prospective validation 回答。

## 7. Semantic generator coverage

此前 QCIC gate 对 mandatory enumeration target 只检查 `minimum_rows`。这仍然存在 count-only false green：删除已接受的生成机制，再补入同 source 的无关 compression row，行数不变，机器门仍可能通过。

不变量：

`ROW COUNT COVERAGE != SEMANTIC GENERATOR COVERAGE`

mandatory enumeration target 必须在 gate state 中冻结：

- `required_generative_rule_ids`：当前已接受、不得被无关 generator 替代的结构身份；
- `required_generator_entry_counts`：该 generator 当前经完整阅读确认的枚举规模；
- `required_generator_method_layers`：该 generator 所属方法层。

`minimum_rows` 只作为粗粒度 sanity check。真正的覆盖由 generator identity 决定。

这样可以同时阻止三类静默漂移：

1. 用无关 generator 替换 mandatory generator，但保持行数不变；
2. 保留同一 generator id，却悄悄改变其结构规模；
3. 保留同一 generator id，却把 CALCULATION 等方法层改成另一个 layer。

如果后续完整阅读或重建测试证明原 generator identity/规模/layer 有误，应显式更新 registry 与 gate snapshot，并重新跑 fail-first / correction / exact-current acceptance，而不是为了维持绿灯偷偷改写。

## 8. 当前落地

QM-SRC-0017《奇门遁甲新述》当前冻结两个结构机制：

- `QM0017-TIME-QIMEN-1080-ENUM`：时家阳遁540 + 阴遁540，共1080，CALCULATION；
- `QM0017-DAY-QIMEN-120-ENUM`：日家阳遁60 + 阴遁60，共120，CALCULATION。

QM-SRC-0010 当前冻结：

- `QM0010-TIME-QIMEN-1080-ENUM`：1080个时辰盘状态展开，CALCULATION。

这些数字用于描述来源中的结构枚举规模，不是 empirical sample size。

当前三个 reconstruction status 均保持 UNTESTED，正式 reconstruction result registry 为空。这一状态是刻意保守的：目前只证明来源具有系统枚举结构，还没有把任一单元升级成“已完成结构重建测试”。

## 9. 与 Evidence / Claim 的边界

Enumeration Compression 只处理知识结构和证据独立性。

它不能：

- 提升 empirical credit；
- 自动产生 Claim；
- 证明某定局表现实有效；
- 用页数、条目量、compression row 数或 reconstruction PASS 替代前瞻样本。

## 10. Fail-closed

以下任一情况必须失败：

- enumerated_entries_count < 2；
- collapsed_structure_units != 1；
- empirical_evidence_units != 0；
- empirical_credit 不为 NONE；
- source_credit 不为 SOURCE_STRUCTURE_ONLY；
- compression_policy 不是 DERIVED_ENUMERATION_COLLAPSE；
- 同一 source/generative_rule_id 被重复登记；
- evidence locator 超出 COMPLETE VISUAL_PAGE 阅读范围；
- source SHA 或 effective work_id 不匹配；
- mandatory generator 被无关 generator 替换；
- mandatory generator 的枚举规模或 method layer 无显式 gate 更新而发生漂移；
- mandatory target 的 compression rows 被删除；
- registry 标为 PASS/FAIL 但缺少匹配 reviewed reconstruction result；
- reconstruction result 与 registry 的 source/work/SHA/compression/generator/status 不一致；
- PASS 存在任一未匹配 checked state；
- reconstruction artifact 获得 empirical credit 或解除 Claim blocker；
- 本地路径泄漏进知识树。
