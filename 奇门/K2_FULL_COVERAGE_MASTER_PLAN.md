# K2 奇门文献全覆盖总计划

状态：ACTIVE / LONG-HORIZON / AUDITABLE

日期：2026-08-21

目标：把“库中文献尽数研习、熟稔于心”落实成可审计的长期工程，而不是口头宣称掌握。全覆盖解决的是 **Corpus Coverage**；它不自动解决 **Truth / Applicability / Empirical Support**。

---

## 1. 当前真实覆盖率

以 Knowledge Engine V1 CI #323 的 aggregate per-book gate 为基线：

```text
expected_reading_units = 37
complete = 5
partial = 0
blocked = 0
not_started = 32
aggregate_evidence_rows = 718
prospective_scored_rows = 0
```

当前 5 个正式 COMPLETE reading units：

- `QM-SRC-0001 / WORK-000217 / 梁湘润《奇门遁甲入门》` — `VISUAL_PAGE / 57/57`
- `QM-SRC-0003 / WORK-000028` — `VISUAL_PAGE / 45/45`
- `QM-SRC-0016 / WORK-000026 / 王云鹏《奇门遁甲应用学》` — `TEXT_LAYER_FULL / 415/415`
- `QM-SRC-0021 / WORK-000027 /《奇门遁甲预测学》` — `TEXT_LAYER_FULL / 285/285`
- `QM-SRC-0028 / WORK-000018 / 善天道《奇门遁甲讲义71页》` — `TEXT_LAYER_FULL / 71/71`

注意：

- supplemental targeted visual review 不重复计算 COMPLETE；
- 看过某页不等于该书 COMPLETE；
- `QM-SRC-0027` 本轮虽浏览过全书 text layer，但因为 Pre-Book gate 被研究好奇心绕过，**不追认 COMPLETE credit**；
- COMPLETE 只表示按当前 Reading Protocol 完成该 reading unit，不表示书中内容真实有效。

---

## 2. 全覆盖的定义

每个 expected reading unit 最终必须落入且只能落入：

`COMPLETE / PARTIAL / BLOCKED`

不得长期靠“我大概看过”悬空。

一个 `COMPLETE` unit 至少要有：

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
11. compression review：本书让当前模型新增、缩窄、合并、删除还是 NO-OP；
12. affected runtime/CI state honest sync。

少任何一项，不用“页数读完”替代。

---

## 3. 三条并行学习轨道

为了避免 32 本剩余资料变成纯摘录队列，后续同时维护三条轨道。

### Track A — Source Mastery

目标：把来源本身读对。

重点：

- 题名、作者/署名、版本、页序；
- 方法对象；
- 原文规则；
- 图表/跨页语义关联；
- 内部矛盾；
- 术语变体；
- 早期文本与后世转述。

输出主要提高 `Source Fidelity / Lineage Confidence`。

### Track B — Executable Knowledge

目标：把能执行的部分变成可复算、可失败算法。

重点：

- 起局；
- 时间边界；
- 阴阳遁/局数；
- 星门神运动；
- 中宫寄法；
- 旺相休囚；
- Role Map；
- 格局方向对象；
- worked plate fixture；
- wrong/permuted/shuffled controls。

输出主要提高 `Implementation Fidelity`。

### Track C — Reality Validation

目标：检验某些 operational claims 是否对未知现实结果有增量。

重点：

- clean unknown-outcome；
- baseline；
- frozen context；
- matched model comparison；
- calibration；
- abstention；
- misses；
- auxiliary ablation。

只有这一轨才可能增加 `Empirical Support`。

三轨不得互相代领 credit。

---

## 4. 剩余 32 unit 的推进策略

不按“从书架第一本读到最后一本”机械排队，而按**问题簇 + lineage rotation**推进，同时保证最终没有遗漏。

### Wave A — 排盘基础对象与历史分叉

优先回答：

- 符头 / 超神 / 接气 / 置闰 / 拆补 / 茅山；
- 平气/定气；
- 子时日界；
- 中宫寄宫；
- 九星/八门/八神运动对象；
- 早期 deity set 与后世 enum 关系。

优先来源类型：

`EARLY TEXT -> INDEPENDENT MODERN SYSTEM -> PRACTICE LECTURE`

目的：防止只沿善天道/现代讲义一条 lineage 自证。

### Wave B — State / Pattern / Role Map

优先回答：

- 九星旺相休囚不同算法；
- 八门旺衰；
- 宫迫、击刑、门迫、空墓等结构与效应是否混写；
- 十干克应的天地盘方向；
- 用神/Role Map 是 source-fixed、method-defined 还是 context-inferred；
- 多个格名是否重复包装一个结构。

目的：压缩旧知识库中“标签越多，结论越强”的倾向。

### Wave C — Case / Application / High-risk isolation

优先回答：

- 书中案例到底证明什么；
- 哪些只是 retrospective narrative；
- 哪些规则能转成 low-risk prospective hypothesis；
- 高风险疾病、死亡、刑事、法律等断语只做 source study，不作现实验证目标。

目的：把“会背案例”与“会预测”彻底分开。

### Wave D — Remaining corpus closure

完成前三个问题波次后，对仍未覆盖的 expected units 做 closure sweep：

- 不因“看起来重复”直接跳过；
- 若高度 derivative，仍要记录 lineage 与 `NO_METHOD_DELTA / DUPLICATIVE_SOURCE`；
- 若 scan/OCR 难以可靠阅读，标 `BLOCKED / RETURN_LATER`，不虚标 COMPLETE；
- 多卷本逐卷关闭。

最终目标：`not_started = 0`，但这不是预测有效性的 milestone。

---

## 5. 每本书的固定研究模板

### Before Reading

`Pre-Book Retrospective`

必须写：

- 当前模型最可能错在哪里；
- 当前最危险的 legacy assumption；
- 这本书什么结果会迫使模型 `NARROW / REVISE / DELETE / NO-OP`；
- 本次停止条件。

### During Reading

每页/章节不只摘内容，还标：

- `METHOD_OBJECT`
- `SOURCE_RULE`
- `CONFLICT`
- `APPLICATION_CONTEXT`
- `DETERMINISTIC_CLAIM`
- `HIGH_RISK`
- `IMPLEMENTATION_HOOK`
- `TEST_HOOK`

### After Reading

必须回答：

1. 这本书真正增加了什么 source knowledge？
2. 哪些只是重复 lineage？
3. 哪个旧观点被缩窄/删除？
4. 哪个新观点最容易被反驳？
5. 有什么不能进入 runtime？
6. 有什么不能进入 Empirical Support？
7. 是否值得修改理论？若只是更好理解，`NO-OP`。

---

## 6. 全覆盖与换书节奏

仍遵循：

- 同时最多 1 本 `PRIMARY_ACTIVE_BOOK`；
- 最多 1 本 `SECONDARY_REFERENCE`；
- Secondary targeted review 不自动领取 full-book credit；
- 连续最多 2 个 cycle 使用同作者/同 lineage；
- 每 2 个 book sprint 至少出现一个 implementation negative-control 或 prospective milestone；
- 若连续两个 sprint 只有摘录，没有 conflict/test/compression，暂停开新书。

预计剩余 32 units 是长期任务，不给“几天学完全部”的虚假承诺。

---

## 7. Coverage 不能驱动虚假速度

禁止以下行为：

- 因为用户要求“全覆盖”就批量把 Not Started 改 Complete；
- OCR 直接替代 VISUAL_REQUIRED；
- targeted review 追认 full reading；
- 读完目录/摘要就声称掌握；
- 为了提高百分比跳过 conflict review；
- 一书几十条 Evidence 机械变成几十条 active rules；
- 把“37/37 完成”包装成“奇门已经验证”。

全覆盖的价值是让模型不再只从自己偏爱的几本书学习，而不是制造一个漂亮进度条。

---

## 8. 全覆盖最终验收

Corpus 层达到阶段性 closure 时，至少要求：

```text
not_started = 0
all units = COMPLETE | PARTIAL | BLOCKED
all COMPLETE units have distillates
all source-specific conflicts traceable
all provenance uncertainty explicit
no targeted review masquerades as full credit
no unsupported accuracy claim promoted
```

然后才进行 corpus-level compression：

- 哪些规则只是同源重复；
- 哪些 source families 真正不同；
- 哪些对象可以统一；
- 哪些必须保持 variants；
- 哪些象意层应被删除或 research-only；
- 哪些 operational candidates 值得进入下一阶段 prospective testing。

`Corpus Closure -> Model Compression`，而不是 `Corpus Closure -> Declare Truth`。

---

## 9. 当前下一棒

在扩大下一本 primary book 前，优先完成：

1. `AQ-005` 八门 state-system 的第二来源比较；
2. `AQ-004` 继续寻找真正能区分 `TIME-BRANCH / HOUR-STEM DAY-BASIS / DAY-PILLAR ROLLOVER` 的边界 worked plate；
3. clean prospective pilot 有真实机会时立即进入，不因读书队列排满而延期；
4. 再根据 attack result 选择下一本 primary，而不是按旧固定书单自动切换。

这是“全覆盖”的新定义：**最终一本不漏，但每次打开一本，都要知道为什么现在读它。**
