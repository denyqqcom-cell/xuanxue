# K2 奇门文献全覆盖总计划

状态：ACTIVE / LONG-HORIZON / AUDITABLE / v1.1

日期：2026-08-21

目标：把“库中文献尽数研习、熟稔于心”落实成可审计的长期工程，而不是口头宣称掌握。全覆盖解决的是 **Corpus Coverage**；它不自动解决 **Truth / Applicability / Empirical Support**。

---

## 0. 先纠正一个刚发生的指标误读

v1.0 曾把 CI 输出：

```text
expected_reading_units = 37
complete = 5
not_started = 32
```

直接写成“奇门剩余 32 unit”。

这是错误的 metric scope。

`validate_k2_evidence.py` 的 `expected_reading_units=37` 是 **六领域当前 Wave1 selection 的 aggregate 指标**，不是奇门 corpus 总数。

因此：

`GLOBAL WAVE1 METRIC != QIMEN CORPUS COVERAGE`

这个错误很典型：即使数字来自 CI，也必须先确认 denominator 的语义对象。否则“精确数字”只会让错误显得更可靠。

本文件从 v1.1 起不再用 37/32 代表奇门全覆盖进度。

---

## 1. 当前奇门 corpus 的真实 scope

`knowledge/domains/qimen/sources.jsonl` 当前有 `QM-SRC-0001 ... QM-SRC-0035` 共 35 个登记 source rows。

结合 `K2_SOURCE_LINEAGE.jsonl`，当前可分：

### A. K2-eligible textual carriers：25

这些 carrier 当前 `k2_eligible=true`，属于 `PRIMARY_WORK / WORK_PART`，覆盖 19 个 unique works：

```text
QM-SRC-0001
QM-SRC-0002
QM-SRC-0003
QM-SRC-0004
QM-SRC-0005
QM-SRC-0008
QM-SRC-0011
QM-SRC-0012
QM-SRC-0013
QM-SRC-0014
QM-SRC-0015
QM-SRC-0016
QM-SRC-0017
QM-SRC-0018
QM-SRC-0019
QM-SRC-0020
QM-SRC-0021
QM-SRC-0025
QM-SRC-0026
QM-SRC-0027
QM-SRC-0028
QM-SRC-0029
QM-SRC-0032
QM-SRC-0033
QM-SRC-0034
```

多卷/多部 carrier 不能因为共享 `work_id` 就只读其中一册；full file coverage 仍需逐 carrier 覆盖，但 source-consensus 统计不能把同一 work 的多卷当独立来源。

### B. Textual carriers 但 lineage/domain 尚未准入：5

```text
QM-SRC-0009
QM-SRC-0010
QM-SRC-0022
QM-SRC-0023
QM-SRC-0024
```

这些不是“可以忽略”，而是必须先解决：

`domain / work identity / lineage / eligibility`

之后才能决定进入哪种正式 Reading lane。

其中 `QM-SRC-0022 / 0024` 已有 targeted visual witness，但 targeted review 不等于 eligibility 已解决。

### C. 非 textual-reading target：5

当前包括 auxiliary indexes / project notes 等：

`QM-SRC-0006 / 0007 / 0030 / 0031 / 0035`

它们可用于导航、历史审计或项目记录，但不应为了“35/35”被伪装成 textual source reading。

### 当前正式 COMPLETE textual carriers：5

- `QM-SRC-0001 / WORK-000217 / 梁湘润《奇门遁甲入门》` — `VISUAL_PAGE / 57/57`
- `QM-SRC-0003 / WORK-000028 /《奇门直断》` — `VISUAL_PAGE / 45/45`
- `QM-SRC-0016 / WORK-000026 / 王云鹏《奇门遁甲应用学》` — `TEXT_LAYER_FULL / 415/415`
- `QM-SRC-0021 / WORK-000027 / 幺学声《奇门遁甲预测学》` — `TEXT_LAYER_FULL / 285/285`
- `QM-SRC-0028 / WORK-000018 / 善天道《奇门遁甲讲义71页》` — `TEXT_LAYER_FULL / 71/71`

所以当前更诚实的 corpus 描述是：

```text
Qimen registered rows = 35
K2-eligible textual carriers = 25
K2-eligible unique works = 19
formal COMPLETE textual carriers = 5
eligible textual carriers not COMPLETE = 20
textual carriers awaiting lineage/domain resolution = 5
non-textual/secondary rows = 5
```

这才是当前“全覆盖”分母。

---

## 2. 当前 K2 Gate 与长期全覆盖不是同一个集合

现有 `validate_k2_evidence.py` 的 Wave1 selection 不是“所有 K2-eligible 奇门 P1/P2 source”。它只接受当前 selection policy 选中的 reading units。

因此像 `QM-SRC-0017` 这样的 `P2 PRIMARY_CANDIDATE`，即使现在开始正式 visual study，也**不能为了体现进度就强塞进当前 Wave1 aggregate ledger**，否则 validator 会把它视为不在 selected set。

处理原则：

1. 研究可以按用户目标继续；
2. visual session / pre-book / source comparison 可以诚实落盘；
3. 不伪造 Wave1 Reading Credit；
4. 当 corpus expansion 进入正式阶段时，先演进 selection/protocol，再迁移这些已审页面；
5. 迁移时保留原始 review 时间和范围，不把 earlier partial exposure 重写成“当时已 COMPLETE”。

`Protocol scope must expand before credit scope expands.`

---

## 3. 全覆盖的定义

每个 eligible textual carrier 最终必须有诚实状态：

`COMPLETE / PARTIAL / BLOCKED`

每个 unresolved textual carrier 最终必须先有：

`ELIGIBLE / NOT_ELIGIBLE / DERIVATIVE / WORK_PART / BLOCKED_LINEAGE`

不得长期靠“我大概看过”悬空。

一个 `COMPLETE` source 至少要有：

1. canonical source identity：SHA256 + page count；
2. honest reading coverage；
3. Atomic Evidence；
4. Book Distillate；
5. provenance / lineage status；
6. source-internal conflict；
7. applicability boundary；
8. high-risk / ritual / deterministic claim isolation；
9. Method Delta 或明确 `NO_METHOD_DELTA`；
10. 至少一个 test hook、implementation question、negative-control question或明确 `NOT_APPLICABLE`；
11. compression review：新增、缩窄、合并、删除还是 NO-OP；
12. affected runtime/CI state honest sync。

少任何一项，不用“页数读完”替代。

---

## 4. 三条并行学习轨道

### Track A — Source Mastery

把来源本身读对：题名、作者/署名、版本、页序、方法对象、规则、图表拓扑、内部矛盾、术语变体、历史谱系。

主要提高：`Source Fidelity / Lineage Confidence`。

### Track B — Executable Knowledge

把能执行的内容变成可复算、可失败对象：起局、时间边界、星门神运动、中宫寄法、state system、Role Map、worked plate、negative controls。

主要提高：`Implementation Fidelity`。

### Track C — Reality Validation

用 clean unknown-outcome、baseline、matched model、calibration、ablation、misses 检验 operational claim。

只有这一轨才可能增加：`Empirical Support`。

三轨不得互相代领 credit。

---

## 5. 剩余 corpus 的问题驱动 Wave

### Wave A — 排盘基础对象与历史分叉

- 符头 / 超神 / 接气 / 置闰 / 拆补 / 茅山；
- 平气/定气；
- 子时日界；
- 中宫寄宫；
- 星门神 movement object；
- 早期 deity set 与现代 enum。

### Wave B — State / Pattern / Role Map

- 九星旺相休囚；
- 八门旺衰；
- 宫迫/击刑/空墓等结构与 effect 是否混写；
- 十干克应方向；
- source-fixed / method-defined / context-inferred Role Map；
- 多格名是否重复包装同一结构。

### Wave C — Case / Application / High-risk isolation

- 案例是 source demonstration 还是 prospective evidence；
- 哪些规则能转成 low-risk testable hypothesis；
- 疾病、死亡、刑事、法律等高风险断语只做 source study，不作现实验证目标。

### Wave D — Closure sweep

- eligible carriers 一个不漏；
- unresolved carriers 逐一解决 lineage/domain；
- derivative/multipart 不重复计算 independent support；
- scan/OCR 不可可靠阅读则 `BLOCKED / RETURN_LATER`；
- auxiliary/note 不虚构 reading credit。

---

## 6. 每本书的固定研究模板

### Before Reading

必须先有 `Pre-Book Retrospective`，写：

- 当前模型最可能错在哪里；
- legacy assumption；
- 什么结果会 `NARROW / REVISE / DELETE / NO-OP`；
- stopping condition。

### During Reading

标：

`METHOD_OBJECT / SOURCE_RULE / CONFLICT / APPLICATION_CONTEXT / DETERMINISTIC_CLAIM / HIGH_RISK / IMPLEMENTATION_HOOK / TEST_HOOK`

### After Reading

必须回答：

1. 真正增加了什么 source knowledge？
2. 哪些只是重复 lineage？
3. 哪个旧观点被缩窄/删除？
4. 哪个新观点最容易被反驳？
5. 什么不能进 runtime？
6. 什么不能进 Empirical Support？
7. 是否值得修改理论？若只是更懂来源，`NO-OP`。

---

## 7. 全覆盖与换书节奏

- 同时最多 1 本 `PRIMARY_ACTIVE_BOOK`；
- 最多 1 本 `SECONDARY_REFERENCE`；
- targeted Secondary 不自动领取 full-book credit；
- 连续最多 2 cycle 使用同作者/同 lineage；
- 每 2 book sprints 至少出现一个 implementation negative-control 或 prospective milestone；
- 连续两个 sprint 只有摘录，没有 conflict/test/compression，暂停开新书。

剩余 20 个 eligible carriers + 5 个 unresolved textual carriers 是长期任务，不给虚假的“几天全部学完”承诺。

---

## 8. Coverage 不能驱动虚假速度

禁止：

- 批量改 COMPLETE；
- OCR 替代 VISUAL_REQUIRED；
- targeted review 追认 full reading；
- 目录/摘要代替全书；
- 为漂亮百分比跳过 conflict review；
- Evidence 数量机械变 active rules；
- 把 global Wave1 的 `37` 当 Qimen corpus denominator；
- 把 corpus 完成包装成“奇门已验证”。

---

## 9. 当前 PRIMARY_ACTIVE_BOOK

`QM-SRC-0017 / WORK-000224 / 费秉勋《奇门遁甲新述》`

在 full content inspection 前已完成 source-specific Pre-Book Retrospective：

`knowledge/K2_PRE_BOOK_RETROSPECTIVES/QM-SRC-0017.md`

canonical identity：

- SHA256 `f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`
- 419 PDF pages
- SCAN / VISUAL_REQUIRED

当前本轮已完成 p1-p80 原页视觉阅读；这是真实 study progress，但由于当前 Wave1 selection 不覆盖该 P2 source，暂不冒充现有 aggregate Reading Ledger credit。

初步发现进入 separate source-review artifact，不在全书未读完前生成 final Book Distillate。

---

## 10. 全覆盖最终验收

奇门 corpus-level closure 至少要求：

```text
all 25 currently eligible textual carriers -> COMPLETE | PARTIAL | BLOCKED
all 5 unresolved textual carriers -> lineage/domain resolved or explicitly blocked
all COMPLETE sources have distillates
all source-specific conflicts traceable
all provenance uncertainty explicit
no targeted review masquerades as full credit
no unsupported accuracy claim promoted
```

之后才做 corpus-level compression：

- shared lineage；
- genuine method families；
- object unification vs variants；
- research-only symbolism；
- operational candidates worth prospective testing。

`Corpus Closure -> Model Compression`，不是 `Corpus Closure -> Declare Truth`。
