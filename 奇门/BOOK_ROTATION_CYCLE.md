# 奇门项目书籍轮换周期

状态：ACTIVE / v1.1 / 2026-08-21

目的：保证最终文献全覆盖，同时防止“无限堆书 = 持续学习”的假进步。换书由 unresolved problem 与反证价值驱动，不由页数完成或固定书单自动驱动。

当前全覆盖总计划：`奇门/K2_FULL_COVERAGE_MASTER_PLAN.md`。

---

## 1. 当前真实基线

以 exact-head `b67e69d02ca69782f0b7b5d3af5a6e072b62b08a` / Knowledge Engine V1 CI #323 为最近完成基线：

```text
expected_reading_units = 37
complete = 5
partial = 0
blocked = 0
not_started = 32
aggregate_evidence_rows = 718
prospective_scored_rows = 0
```

正式 COMPLETE：

- `QM-SRC-0001` 梁湘润《奇门遁甲入门》；
- `QM-SRC-0003`；
- `QM-SRC-0016` 王云鹏《奇门遁甲应用学》；
- `QM-SRC-0021`《奇门遁甲预测学》；
- `QM-SRC-0028` 善天道《奇门遁甲讲义71页》。

因此旧 v1.0 中“Cycle 1 善天道71页尚未给整书 Reading credit”的描述已经过时，现已纠正。

`COMPLETE != TRUE != VALIDATED`。

---

## 2. 基本原则

项目同时最多：

- 1 本 `PRIMARY_ACTIVE_BOOK`；
- 1 本 `SECONDARY_REFERENCE`。

Secondary 只能用于定向交叉查看；没有独立完成 intake / pre-book / reading / evidence / distillate 流程，不获得完整 Reading/Book credit。

切换书籍不是：

`读完页数 -> 下一本`

而是：

`问题 -> 选书 -> Pre-Book -> 原页阅读 -> Evidence/Distillate -> 攻击当前理论 -> Test Hook -> 自省压缩 -> 切换`

最终要求一本不漏，但每一次打开一本都必须知道它当前为什么值得读。

---

## 3. 周期单位

以 7 天为一个 `BOOK_SPRINT`，按 verified PDF page count 分配默认时间盒：

- `S`：1-100 页 -> 1 sprint / 7 天；最大 14 天；
- `M`：101-250 页 -> 2 sprints / 14 天；最大 21 天；
- `L`：251-500 页 -> 3 sprints / 21 天；最大 28 天；
- `XL`：>500 页或复杂卷册 -> 4 sprints / 28 天；最大 42 天；
- 多卷本按卷单独建 cycle。

这里是时间盒，不是完成承诺。到期没读完就诚实标 `PARTIAL / BLOCKED / RETURN_LATER`。

---

## 4. 每个 Book Sprint 的内部比例

默认：

- 10%：Pre-Book Retrospective + canonical intake；
- 40%：原页阅读 / visual review；
- 20%：Atomic Evidence + Distillate；
- 10%：Conflict / Applicability / source-lineage；
- 10%：implementation / negative-control / prospective test hook；
- 10%：self-audit + Model Compression。

如果一本书只产生大量摘录，没有 conflict/test/compression，不算健康闭环。

---

## 5. 正常换书 Gate

Primary book 正常关闭前至少满足：

1. canonical identity：SHA256 + verified page count；
2. Reading Ledger 与实际一致；
3. Atomic Evidence / Distillate；
4. source 与 project inference 边界明确；
5. 至少一个 attack question，或明确 `NO_METHOD_DELTA`；
6. 至少一个 implementation/prospective hook，或 `NOT_APPLICABLE`；
7. unresolved conflict / ambiguity debt；
8. high-risk / ritual / deterministic claims 已隔离；
9. compression review：新增、缩窄、合并、删除、NO-OP 至少明确其一；
10. affected runtime/CI 状态已同步或明确 pending。

“我已经懂了”不能替代以上任何一项。

---

## 6. 流程真实性 Gate

新增纪律：

`Process performed != process credit earned`。

如果 targeted attack 过程中因为好奇心扩展成近似全书浏览，但没有事前完成 Pre-Book Retrospective：

- 保留已经看到的事实；
- 不假装没看过；
- 不事后补文档伪造时间顺序；
- targeted Evidence 可按实际 verification 记录；
- full-book COMPLETE credit 暂停；
- 若以后正式开该书，先写 `POST-EXPOSURE RETROSPECTIVE`，说明污染和已暴露内容。

`QM-SRC-0027` 当前就是这个例子。

---

## 7. 防止同门派回音室

轮换至少考虑三类来源：

- `A — PRIMARY / EARLY TEXT`
- `B — INDEPENDENT MODERN SYSTEM`
- `C — PRACTICE / CASE / LECTURE`

默认不连续超过 2 个 cycle 使用同一作者/同一 lineage。

多卷系列每卷之间至少做一次 cross-lineage challenge；若下一卷主要重复 wording 而非 method difference，可暂停系列。

“多本都这么说”只有在 independence 确认后才有 source-consensus 意义。

---

## 8. 下一本书的选择算法

每次换书先写 TOP unresolved questions，再评候选 source 的**攻击价值**：

- 是否直接回答当前 implementation/prospective failure；
- 是否可能反对当前 model，而不是只支持；
- 与刚读来源是否 lineage 独立；
- provenance 是否可核；
- 是否含可复算 algorithm / worked plate；
- 是否能生成 negative control；
- 是否能帮助压缩现有变量；
- 当前文件是否可稳定视觉复核。

高“权威感”不是加分项。

---

## 9. 当前攻击问题优先级

### AQ-004 — 真正的 time-boundary control

当前已有：

- `QM-SRC-0027 p3`：`0-1`早子、`23-24`晚子，晚子 hour-stem day-basis 已改变；
- `QM-SRC-0021 p25`：子时写作连续 `23:00-1:00` branch interval。

但这两页没有直接裁决完整 `DAY-PILLAR ROLLOVER`。

当前对象必须分开：

`TIME-BRANCH INTERVAL != HOUR-STEM DAY-BASIS != DAY-PILLAR ROLLOVER`

下一来源优先找 23:00/00:00 worked plate，而不是再找一句“子时从几点开始”。

### AQ-005 — Star/Door state systems

九星第一轮已经得到 source convergence，但不恢复 fixed multiplier：

`STAR-STATE CLASSIFICATION != PREDICTIVE EFFECT-SIZE`

下一步优先完成八门 state-system 的第二个 method-context 清楚来源，然后先 compression review，不无限扩表。

### AQ-002 — 中五值使

仍需 source-defined center-target full-door witness。找不到就继续 fail closed。

### Clean Prospective

只要出现真实、低风险、结果未知、可核验机会，优先级可直接超过换书队列。

读书不能成为逃避未来失败的理由。

---

## 10. 当前 source 轮换候选

不是固定课程表，只是候选池。

### Early / historical challenge

- 《笺元遁甲句解烟波钓叟歌》；
- 《甲遁真授秘录》上/下；
- 《金函玉镜奇门遁甲秘笈全书》上/下。

使用目的：历史对象、术语、movement lineage、setup variant。古籍身份不等于真理优先级。

### Independent modern system

- 费秉勋《奇门遁甲新述》；
- 曾子南《三元奇门遁甲讲义》上/中/下；
- 其他 K2 eligible independent work。

使用目的：寻找真正不同的 method family，而不是现代重复背书。

### Practice / lecture

- 善天道《奇门遁甲高级研修班讲义294页》；
- 善天道《奇门遁甲精华》；
- 《奇门遁甲秘传》；
- 《奇门遁甲吉凶占断教程》；
- 《奇门遁甲白话精解》等。

使用目的：Role Map、案例、场景断法、宽象意风险与可测试结构。

---

## 11. 书与实验的比例上限

为了防止“读书替代验证”：

- 任意连续 2 个 sprint 内，至少有 1 个 implementation negative-control milestone 或 prospective milestone；
- 若没有，下一 sprint 暂停新 primary book；
- 任意一本书产生的规则，在没有独立结果数据前只能改变 Source Map / Candidate Hypothesis；
- 每个 book cycle 至少提出一个 `DELETE / MERGE / NARROW / NO-OP` 候选。

若连续两个 sprint 都只有新术语、新表格、新象意，说明项目正在重新走回知识堆积。

---

## 12. 强制轮换条件

以下任一出现，记录状态后可切换：

- 达到 size class 最大时间盒仍不能闭环；
- scan corruption / inaccessible 连续 2 个 session 阻塞；
- 连续 3 个 session 没有新增 Evidence、Conflict、Test Hook 或 correction；
- 与最近来源同 lineage 高度重复；
- 更高优先级 implementation/prospective failure 明确要求另一来源；
- 当前 source 已无法再减少不确定性，只能继续增加相似摘录。

切换不等于放弃，保留 `RETURN_LATER`。

---

## 13. 每轮闭书必须问

1. 这本书真正教会了什么，而不是只“说了什么”？
2. 哪些内容只是传统 source claim？
3. 哪一点最可能推翻当前自己的模型？
4. 哪条规则可以失败得很清楚？
5. 学完以后删掉/缩窄/合并了什么？
6. 如果什么都没删，本次新增复杂度有什么可测增量？
7. 下一本是因为研究问题需要，还是因为“该换书了”？

如果第 7 问答不清楚，就先不换。

---

## 14. 最终全覆盖目标

长期目标仍是 37 expected units 全部有诚实状态，最终 `not_started = 0`。

但项目不追求最快完成时间，而追求：

`Corpus Coverage + Source Fidelity + Executable Separation + Falsifiable Tests + Compression`

最后也只允许说：

“已系统学习全部登记文献，并知道它们在哪里一致、冲突、不可执行、待验证。”

不能因为 37/37 就说：

“奇门规则已被证明为真。”
