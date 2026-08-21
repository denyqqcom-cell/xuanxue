# Book Cycle 1 Entry — 善天道《奇门遁甲讲义71页》

状态：ACTIVE ENTRY / STRUCTURAL_SURVEY_ONLY / READING_CREDIT=0

日期：2026-08-21

## 1. Canonical K1 identity

本轮第一版 Entry 曾写 `PENDING_K1_INTAKE`。回查现有 K1 `knowledge/domains/qimen/sources.jsonl` 后确认，这是主 Agent 自己的状态查询遗漏；该源早已完成 K1 sanitized intake。

正确身份：

- source_id：`QM-SRC-0028`
- title：`善天道-奇门遁甲讲义71页`
- author：`善天道`（K1 `author_basis=FILENAME`，不是作者页独立验证）
- source_type：`COURSE`
- SHA256：`bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243`
- PDF page count：71
- pages_basis：`PDF_PAGE_COUNT`
- readability：`TEXT_OK`
- copyright：`FORBIDDEN_TO_PACKAGE`
- K1 status：`INDEXED`

本地 canonical candidate 的 hash/page count 与 `QM-SRC-0028` 完全一致。

历史《精读笔记_善天道》另有独立 K1 身份：`QM-SRC-0036 / NOTE / SECONDARY_NOTE`，不能替代 `QM-SRC-0028` 原书。

当前只完成 71/71 render + structural survey + targeted page inspection，整书 `READING_CREDIT=0`。

下一步不是重复 K1 intake，而是建立 K2 work/reading packet，并从 canonical source 原页重新读。

## 2. Why this book enters now

进入 Cycle 1 的原因不是静态课程表，而是当前真实 implementation debt：

1. `QimenEngine` 刚暴露过 center-palace chief-door gap；
2. 36 个梁书甲子 sparse anchors 只验证 chief identity，full star/door/deity rotation 仍未验证；
3. 需要独立来源攻击当前对天禽/天芮寄宫、值符值使和八神体系的理解；
4. 旧 `QM-SRC-0036` 二手笔记本身已经暴露 source-map 与 operational-promotion 问题，必须回原书重做。

因此本书属于问题驱动 source selection。

## 3. Prior-model audit before fresh reading

Cycle 1 不假装“第一次接触善天道”。项目已经有旧二手笔记，所以必须先冻结旧认知，再检查它哪里错。

前置审计：

`奇门/学习笔记/审计_精读笔记_善天道_Cycle1_2026-08-21.md`

已发现：

- 旧笔记明写来源为 `_txt` 提取，却使用“精读”命名；
- 71 页结构地图实际上只覆盖到 p15，漏掉大半正文；
- “讲义=飞宫法、精华=排宫法”的八神归类与 canonical p27“本书用的是排宫法”冲突；
- 同一 71 页源 p3、p19-p20、p31 本身存在不同八神列表/命名关系，不能粗暴归入一个 enum；
- “最实用/核心资产/更系统化/可合并”属于旧项目判断，不是经验支持；
- 疾病死亡、刑事等高风险断语被过度提升为 operational knowledge。

本轮新读必须优先寻找旧笔记的反例和遗漏页，而不是继续确认旧笔记。

## 4. Pre-reading attack questions

### Q1 — Center host / star-door rotation

当前工作假设：

- 中五宫没有独立门位；
- 五宫 chief identity 可得到天禽 / 死门；
- 但完整 star/door rotation 与 Tian-Qin/Tian-Rui hosting 仍未验证。

本书 p19-p22 结构上直接涉及值符、值使、天禽/天芮和星门转动。

要找的是反例、例外与完整算法，不是只找“支持死门”的句子。

### Q2 — Deity-system relationship

当前项目把 `GOUCHEN_ZHUQUE` 与 `BAIHU_XUANWU` 作为独立冻结体系，目的是防止结果后静默替换；这个工程约束本身不等于历史谱系已经搞清。

canonical source 的 targeted review 目前显示：

- p3 列 `九神煞`：真符、腾蛇、太阴、六合、勾陈、太常、朱雀、九地、九天；
- p19-p20 采用白虎（勾陈）、玄武（朱雀）的括号关系，并记载小值符运转有两说；
- p27 明确写“本书用的是排宫法”；
- p31 又讨论阳遁/阴遁中勾陈、朱雀与玄武、白虎的转换。

待验证问题不是“谁等于谁”，而是：

- 作者是否在同书介绍多个体系？
- 括号是 alias、替代名，还是特定遁法下的转换？
- p3 的九神煞与 p19-p31 的八神是否属于不同方法层？
- 是否存在教材拼接/传本差异？

完整上下文读完前，不改 runtime enum，不静默互借象意。

### Q3 — Setup / solar-term / yuan semantics

p15-p18 集中讨论节气定局、上中下元、符头以及跨节气时辰切换。

需要对照当前 engine 的：

- JieQi selection；
- yuanOf；
- setup_method；
- time-boundary assumptions。

若算法不同，先记录 source-defined variant，不先改 production。

### Q4 — Deterministic pattern claims

p33-p49 大量格局、九遁、十干克应写法带有强确定性现实断语。

任务不是背下来，而是拆成：

`SOURCE_PATTERN -> APPLICABILITY CLAIM -> TESTABLE CONSEQUENCE`

没有 prospective support 的现实断语不能进入 Empirical Support。

### Q5 — Method-layer shift around p50

p50 起出现“暗藏飞干”等内容，随后进入大量占法。

必须判断：

- 这是前述排宫法的扩展？
- 另一算法层？
- 不同资料拼接？
- 只是解释层变化而不改盘？

在完成上下文核验前标 `METHOD_LAYER_REVIEW_REQUIRED`，不把全书自动压成一个统一“善天道体系”。

### Q6 — Applied/high-risk layer

p51-p71 涵盖词讼、疾病、求财、阳宅、刑事等实际事项，并出现死亡、犯罪、病理等高风险判断。

处理原则：

- source fidelity 可以学习；
- 高风险断语只保留为 source claim / research candidate；
- 不直接用于现实医疗、法律、犯罪事实判断；
- 若产生研究价值，转成低风险、可评分的结构问题，而不是照搬结论。

## 5. Anti-confirmation rule for this cycle

本书此前已有 p19/p21-p22 targeted secondary inspection，用来协助理解 center-host implementation gap；另外旧 `QM-SRC-0036` 已经把部分善天道规则评价成“最实用/核心资产”。

因此这轮完整阅读必须主动防止 selection bias：

- 先找与当前实现/旧笔记冲突的页；
- 再找支持页；
- 支持与冲突分开记录；
- source 内部冲突不能由“多数页支持”自动抹平；
- 不因为当前代码已经修过，就把书解释成支持现状；
- 不因为旧笔记已写“核心资产”，就优先给这些规则 credit。

## 6. First sprint execution order

1. K1 identity 已确认：`QM-SRC-0028`；建立 K2 work/reading packet，不重复 intake；
2. 先完成旧笔记 correction overlay，冻结 prior model；
3. p1-p22 逐页视觉主审：先攻 setup + value-chief + rotation；
4. p23-p32：象意层，区分 source symbolism 与 operational feature；
5. p33-p49：pattern/provenance，标记确定性断语与内部冲突；
6. p50-p71：判断 method-layer/lineage shift，隔离应用与高风险内容；
7. 形成 Atomic Evidence / Book Distillate；
8. 只把真正改变实现或可验证模型的问题送入 implementation/prospective tests；
9. Book Close 时必须输出 `KEEP / REVISE / DELETE / NO-OP`。

## 7. Local AI packet scope

本地 AI 仅作为 `EXECUTION_HELPER_ONLY`：

- verify `QM-SRC-0028` SHA256/page count；
- 300 DPI+ render；
- 建 page/section map；
- 对 p1-p22、p23-p32、p33-p49、p50-p71 生成可追溯 visual packet；
- text extraction/OCR 仅 navigation；
- 跑 QimenEngine full-rotation raw output / wrong-input controls；
- 保存本地 artifacts / hashes / logs。

默认禁止：

- Reading/Evidence/Empirical Support credit；
- tracked edits；
- commit/push/merge；
- 根据结果选择支持页；
- 把 source deterministic claim 当现实事实；
- 用旧 `QM-SRC-0036` 笔记代替 `QM-SRC-0028` 原页。

## 8. Exit / switch conditions

正常关闭必须满足现行 `BOOK_ROTATION_CYCLE.md`。

额外要求：

- 至少找到一个真正攻击当前实现/理论/旧笔记的 source point，或明确记录 `NO_ATTACK_FOUND`；
- 至少一个 implementation/prospective test hook；
- 不以“71 页看完”单独作为完成条件；
- 不因为时间盒结束虚标 COMPLETE。

## 9. Theory-version discipline

本 Cycle 不预设会产生 v0.4。

只有新 source conflict / implementation failure / negative control / clean prospective evidence 真正改变 operational claim，才考虑理论版本升级。

读得更多，不等于理论自动更新。
