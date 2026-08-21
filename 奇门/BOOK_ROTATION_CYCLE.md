# 奇门项目书籍轮换周期

状态：ACTIVE / v1.0 / 2026-08-21

目的：防止“无限堆书 = 持续学习”的假进步。书籍轮换既要保证读透，也要强制留下验证、反证和压缩时间。

## 1. 基本原则

项目同时最多：

- 1 本 `PRIMARY_ACTIVE_BOOK`；
- 1 本 `SECONDARY_REFERENCE`。

Secondary 只能用于定向交叉查看；没有独立完成 intake / reading / evidence 流程，不获得完整 Reading/Book credit。

切换书籍不是“看完页数就换”，而是：

`问题 -> 选书 -> 原页阅读 -> Evidence/Distillate -> 攻击当前理论 -> Test Hook -> 自省压缩 -> 切换`

## 2. 周期单位

以 7 天为一个 `BOOK_SPRINT`，并按 verified PDF page count 分配默认时间盒：

- `S`：1-100 页 -> 1 sprint / 7 天；最大 14 天。
- `M`：101-250 页 -> 2 sprints / 14 天；最大 21 天。
- `L`：251-500 页 -> 3 sprints / 21 天；最大 28 天。
- `XL`：>500 页或结构复杂的大型卷册 -> 4 sprints / 28 天；最大 42 天。
- 多卷本：**按卷单独建 cycle**，不得把“上中下三册”一次性写成一个 COMPLETE。

这里的“天数”是项目时间盒，不是完成度承诺。到期没有读完，正确状态是 `PARTIAL / BLOCKED`，不是为了换书而虚标 COMPLETE。

## 3. 每个 Book Sprint 的内部比例

默认：

- 10%：Pre-Book Retrospective + canonical intake；
- 45%：原页阅读 / visual review；
- 20%：Atomic Evidence + Book Distillate；
- 10%：Conflict / Applicability / attack current theory；
- 10%：implementation / prospective test hook；
- 5%：self-audit + Model Compression。

若某本书只产生大量摘录、没有 conflict/test hook/self-audit，不算健康闭环。

## 4. 正常换书 Gate

一本 primary book 在正常切换前至少满足：

1. canonical identity 已锁：filename 不算，至少有 SHA256 + verified page count；
2. Reading Ledger 诚实：`COMPLETE / PARTIAL / BLOCKED` 与实际一致；
3. 已读范围有 Atomic Evidence / Distillate，不用模糊“我已经懂了”代替；
4. 明确记录 source 与 project inference 的边界；
5. 至少提出一个“这本书如何攻击当前模型”的问题，或明确 `NO_METHOD_DELTA`；
6. 至少产生一个 testable implementation/prospective hook，若确实不适用写 `NOT_APPLICABLE`；
7. 记录 unresolved conflict / ambiguity debt；
8. 做一次 compression review：本轮有没有东西应该删、并、降级；
9. exact-head CI/索引状态若受影响，已同步或明确记录 pending。

满足这些后才可 `CLOSED -> next PRIMARY`。

## 5. 提前换书与强制轮换

### 可以提前结束

在 target timebox 前完成全部换书 Gate，并完成至少一次独立反证/negative-control review，可提前关闭。

“我读得快”不是提前结束理由。

### 必须强制轮换

发生以下任一情况，可在记录状态后切换：

- 达到该 size class 最大时间盒仍无法闭环；
- source inaccessible / scan corruption 导致连续 2 个 research session 无法推进；
- 连续 3 个 research session 没有新增 Evidence、Conflict、Test Hook 或 correction，只在重复摘录；
- 与最近一本同 lineage 内容高度重复，新增信息主要是 wording 而不是方法差异；
- 当前更高优先级的 implementation/prospective failure 明确要求转查另一来源。

强制轮换时，原书保留 `PARTIAL / BLOCKED / RETURN_LATER`，不得伪装“读完”。

## 6. 防止同门派回音室

默认采用三类轮换：

- `A — PRIMARY / EARLY TEXT`：古籍、早期文本、原典 witness；
- `B — INDEPENDENT SYSTEM`：现代系统著作、独立理论框架；
- `C — PRACTICE / CASE / LECTURE`：实战讲义、案例、操作体系。

默认不连续超过 2 个 cycle 使用同一作者/同一 lineage。

若需要连续读多卷同一系列，必须在每卷之间做一次 cross-lineage challenge；若没有新的方法差异，可暂停系列而不是为了“全集读完”继续。

## 7. 选下一本书的算法

每次换书先列当前 TOP 3 unresolved questions，再给候选书打“研究价值”，不是打“权威分”：

- 是否直接回答当前 implementation/prospective failure；
- 是否与上一来源独立，能形成冲突而非重复背书；
- 是否有清楚 provenance / 可做 source fidelity；
- 是否包含可转成 testable structure 的内容；
- 是否可能攻击当前 v0.3-alpha，而不只是支持它；
- 当前文件是否可稳定访问和视觉复核。

优先选“最可能暴露我们错在哪里”的书，而不是“最像现在理论”的书。

## 8. 当前默认轮换序列

这是默认队列，不是不可打断的课程表。若真实 implementation/prospective failure 指向其他来源，可覆盖，但必须记录 override reason。

### Cycle 0 — 梁湘润《奇门遁甲入门》

状态：Reading/Distillation CLOSED；36 Jiazi sparse-anchor implementation scope CLOSED；Empirical validity OPEN。

### Cycle 1 — 善天道《奇门遁甲讲义71页》

类型：C / small practical lecture。

默认周期：S = 7 天，最大 14 天。

为什么排前：当前 implementation debt 正好集中在中宫寄宫、值符值使、星门完整转动；此前只做过 p19/p21-p22 targeted secondary cross-check，尚未给整书 Reading credit。完整阅读可以检查 targeted selection 是否有偏见。

主要攻击面：

- center host 是否只有 chief identity，还是完整门星寄宫规则；
- 当前 `QimenEngine` rotation 与本书是否一致；
- 本书的断法是否存在“单符号直断”与过度确定性。

### Cycle 2 — 《笺元遁甲句解烟波钓叟歌》

类型：A / early-text witness。

周期：在 K1 intake 后按 verified page count 决定。

主要攻击面：

- yange/provenance；
- 起局口诀与后世现代转述的差异；
- 当前 qimen-yange registry 的 attribution 是否站得住。

### Cycle 3 — 《奇门遁甲新述》费秉勋

类型：B / independent modern system。

周期：按 verified page count。

主要攻击面：

- 是否提供不同于“秘传/讲义”的理论组织方式；
- Role Map / 方法族 / 旺衰是否可减少当前模型字段；
- 是否存在能直接反驳 v0.3 的更简单模型。

### Cycle 4 — 善天道《奇门遁甲高级研修班讲义294页》

类型：C / applied lecture。

文件名已指示约 294 页，但正式周期仍以 K1 verified page count 为准；若为 251-500 页，默认 L = 21 天，最大 28 天。

主要攻击面：

- 解盘流程是否会诱发模板化；
- 用神/格局/四害的具体适用域；
- 将讲义规则转成 matched prospective A/B，而不是照抄成 runtime truth。

### Cycle 5 — 《甲遁真授秘录》上册

类型：A / historical source。

周期：按 verified page count。

主要攻击面：

- setup/time/layout 的历史变体；
- 后世“标准转盘”的哪些部分其实是 later synthesis；
- 当前 source lineage 是否把现代术语倒投古籍。

### Cycle 6 — 曾子南《三元奇门遁甲讲义》上

类型：B/C / independent school。

按“单卷一个 cycle”。上卷完成后不自动进入中卷：先比较与当前体系是否真的产生新的 method family；若只重复，先轮换其他 lineage。

### 后续候选池

- 《金函玉镜奇门遁甲秘笈全书》上/下；
- 《奇门遁甲秘传》姜春龙；
- 《奇门遁甲吉凶占断教程》；
- 《奇门遁甲白话精解》；
- 曾子南中/下；
- 善天道《奇门遁甲精华》；
- 《奇门遁甲预测学》；
- 其他已 intake 来源。

候选池不是优先级真值；每次换书重新按 unresolved questions 排序。

## 9. 书与实验的比例上限

为了避免“读书替代验证”：

- 任意连续 2 个 book sprint 内，至少必须有 1 个 implementation negative-control milestone 或 1 个 prospective pilot milestone；
- 如果没有，下一 sprint 暂停新 primary book，先做验证；
- 任意一本书产生的规则，在没有独立结果数据前只能改变 Source Map / Candidate Hypothesis，不能直接改变 Empirical Support。

## 10. 每轮闭书必须问的五句话

1. 这本书真正教会了什么，而不是“说了什么”？
2. 哪些内容只是 source tradition，尚未证明现实有效？
3. 哪一点最可能推翻当前自己的理论？
4. 哪条规则可以设计成失败得很清楚的测试？
5. 学完以后，我们删掉了什么，还是又只增加了一层？

如果第五问长期回答“什么都没删”，优先怀疑项目仍在知识累积，而不是理论成长。
