# K2 奇门文献全覆盖总计划

状态：ACTIVE / LONG-HORIZON / AUDITABLE / v1.2

日期：2026-08-21

目标：把“库中文献尽数研习、熟稔于心”落实成可审计的长期工程，而不是口头宣称掌握。全覆盖解决的是 **Corpus Coverage**；它不自动解决 **Truth / Applicability / Empirical Support**。

---

## 0. 先纠正一个已经发生的指标误读

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

本文件不再用 37/32 代表奇门全覆盖进度。

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

### 当前正式受 Gate 管理的 COMPLETE textual carriers：6

Base Wave1 COMPLETE 仍为 5：

- `QM-SRC-0001 / WORK-000217 / 梁湘润《奇门遁甲入门》` — `VISUAL_PAGE / 57/57`
- `QM-SRC-0003 / WORK-000028 /《奇门直断》` — `VISUAL_PAGE / 45/45`
- `QM-SRC-0016 / WORK-000026 / 王云鹏《奇门遁甲应用学》` — `TEXT_LAYER_FULL / 415/415`
- `QM-SRC-0021 / WORK-000027 / 幺学声《奇门遁甲预测学》` — `TEXT_LAYER_FULL / 285/285`
- `QM-SRC-0028 / WORK-000018 / 善天道《奇门遁甲讲义71页》` — `TEXT_LAYER_FULL / 71/71`

Post-Wave1 corpus expansion COMPLETE：

- `QM-SRC-0017 / WORK-000224 / 费秉勋《奇门遁甲新述》` — `VISUAL_PAGE / 419/419`

`QM-SRC-0017` 的 credit 不修改 Wave1 denominator；它由独立 expansion manifest / ledger / Evidence / Distillate gate 管理。

所以当前更诚实的 corpus 描述是：

```text
Qimen registered rows = 35
K2-eligible textual carriers = 25
K2-eligible unique works = 19
base-Wave1 COMPLETE qimen carriers = 5
post-Wave1 expansion COMPLETE qimen carriers = 1
formally governed COMPLETE qimen textual carriers = 6
eligible textual carriers not COMPLETE = 19
textual carriers awaiting lineage/domain resolution = 5
non-textual/secondary rows = 5
```

这里的 `6 COMPLETE` 只表示 Reading/Distillation coverage 已通过相应 Gate，不表示 6 本书都正确，更不表示奇门预测有效。

---

## 2. Wave1 与长期 corpus expansion 是两个不同 scope

现有 `validate_k2_evidence.py` 的 Wave1 selection 不是“所有 K2-eligible 奇门 P1/P2 source”。它只接受当前 selection policy 选中的 reading units。

因此 P1/P2 source 不能为了显示进度直接塞进 Wave1 ledger。

现在正式采用第二条可审计通道：

```text
Base Wave1
  knowledge/K2_READING_LEDGER_WAVE1*
  knowledge/K2_EVIDENCE_WAVE1*
  knowledge/K2_BOOK_DISTILLATES_WAVE1*

Post-Wave1 Corpus Expansion
  knowledge/K2_EVIDENCE_EXPANSION.json
  knowledge/K2_READING_LEDGER_EXPANSION.d/
  knowledge/K2_EVIDENCE_EXPANSION.d/
  knowledge/K2_BOOK_DISTILLATES_EXPANSION.d/
```

Expansion 只能接纳：

- 已在 K2 lineage 中 `k2_eligible=true` 的 textual source；
- 不属于现有 Wave1 的 source；
- canonical identity 已确认；
- Pre-Book gate 与实际 Reading coverage 可审计；
- SCAN/OCR_WEAK source 满足 `VISUAL_PAGE`；
- Evidence / Distillate 与 reading count 一致；
- 不泄露私有文件路径或受版权保护长文本。

Expansion validator 必须拒绝：

- 与 base Wave1 重复领 credit；
- 非 eligible source；
- 不完整 coverage 冒充 COMPLETE；
- evidence locator 超出 reviewed pages；
- SCAN 只靠 text/OCR 领视觉 credit；
- distillate 与 Evidence 数量不一致。

核心原则仍然是：

`Protocol scope must expand before credit scope expands.`

但 scope 扩展不需要每次重写原 Wave1 的历史 selection；显式 Expansion lane 更能保留历史语义。

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

把来源本身读对：题名、作者/署名、版本、页序、方法对象、规则、图表拓扑、内部矛盾、术语变体、历史谱系、作者立场。

新增永久阅读纪律：

`SOURCE_CONTAINS(X) != AUTHOR_ENDORSES(X)`。

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

并检查 source-position：

`TRADITION_RECORDED / AUTHOR_EXPLANATION / AUTHOR_CRITIQUE / AUTHOR_OPERATIONAL_COMMITMENT`。

它目前是阅读纪律，不强制新增 schema 字段。

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

剩余 19 个 eligible carriers + 5 个 unresolved textual carriers 是长期任务，不给虚假的“几天全部学完”承诺。

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
- 把 Expansion COMPLETE 算回 Wave1 造成历史 denominator 漂移；
- 把 corpus 完成包装成“奇门已验证”。

---

## 9. 当前 Primary 状态

`QM-SRC-0017 / WORK-000224 / 费秉勋《奇门遁甲新述》` 已完成本轮 full-carrier closure：

- Pre-Book Retrospective：已完成；
- canonical SHA256：`f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`；
- 419/419 original-page visual coverage；
- Expansion Reading Ledger：COMPLETE；
- 18 条 derived Atomic Evidence；
- Expansion Book Distillate；
- Final Method Delta；
- Post-Reading Test Plan。

本书 closure 后不自动开启下一本 Primary。

当前 `PRIMARY_ACTIVE_BOOK = NONE / NEXT_SOURCE_ATTACK_DRIVEN`。

下一本 source 必须由真实攻击问题选择，而不是按日历自动轮换。优先选择能够区分以下至少一项的 witness：

- 23:00/00:00 day-pillar / hour-stem boundary；
- 中五值使 full-door host；
- 可能反对当前 full-rotation profile 的 worked plate；
- 八门 state system 的明确独立算法；
- 能够攻击 `SOURCE_FIXED_LOOKUP vs CONTEXT_FROZEN_RELATIONAL` 的不同 method family。

clean unknown-outcome case 若先出现，则 prospective 优先于继续开书。

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
