# K2 Enumeration Compression Protocol

版本：v1.2  
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

- `UNTESTED`：已经识别为生成式枚举，但尚未实现独立重建测试；
- `PASS`：预先定义的重建测试通过；
- `FAIL`：重建失败，说明压缩模型不完整或错误。

在状态为 UNTESTED 时，禁止写成“算法已验证”。

下游 eligibility view 会把 FAIL 保持为 HOLD，而不是当作可用重建结构。

## 5. generative_rule_id 的语义

`generative_rule_id` 是知识工程中的结构标识，不等于传统规则已经现实有效。

它用于回答：

> 哪一组表项应被视为一个生成机制的展开？

而不是：

> 这个生成机制是否预测准确？

后者只能由 prospective validation 回答。

## 6. Semantic generator coverage

此前 QCIC gate 对 mandatory enumeration target 只检查 `minimum_rows`。这仍然存在 count-only false green：删除已接受的生成机制，再补入同 source 的无关 compression row，行数不变，机器门仍可能通过。

新增不变量：

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

## 7. 当前落地

QM-SRC-0017《奇门遁甲新述》当前冻结两个结构机制：

- `QM0017-TIME-QIMEN-1080-ENUM`：时家阳遁540 + 阴遁540，共1080，CALCULATION；
- `QM0017-DAY-QIMEN-120-ENUM`：日家阳遁60 + 阴遁60，共120，CALCULATION。

QM-SRC-0010 当前冻结：

- `QM0010-TIME-QIMEN-1080-ENUM`：1080个时辰盘状态展开，CALCULATION。

这些数字用于描述来源中的结构枚举规模，不是 empirical sample size。

当前 reconstruction status 仍保持 UNTESTED；这只关闭“条目数=证据数”和“行数=语义覆盖”的错误，不虚报重建算法已完成。

## 8. 与 Evidence / Claim 的边界

Enumeration Compression 只处理知识结构和证据独立性。

它不能：

- 提升 empirical credit；
- 自动产生 Claim；
- 证明某定局表现实有效；
- 用页数、条目量或 compression row 数替代前瞻样本。

## 9. Fail-closed

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
- 本地路径泄漏进知识树。
