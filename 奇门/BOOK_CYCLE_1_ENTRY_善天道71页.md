# Book Cycle 1 Entry — 善天道《奇门遁甲讲义71页》

状态：ACTIVE READING / PARTIAL 22/71 / K2 EVIDENCE 12 REVIEWED

日期：2026-08-21

## 1. Canonical K1 identity

本轮第一版 Entry 曾写 `PENDING_K1_INTAKE`。回查现有 K1 `knowledge/domains/qimen/sources.jsonl` 后确认，这是主 Agent 自己的状态查询遗漏；该源早已完成 K1 sanitized intake。

正确身份：

- source_id：`QM-SRC-0028`
- work_id：`WORK-000018`
- relation：`PRIMARY_WORK`
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

历史《精读笔记_善天道》另有独立 K1 身份：`QM-SRC-0036 / WORK-000232 / NOTE / SECONDARY_NOTE`，不能替代 `QM-SRC-0028` 原书。

### K2 reading state

已逐页主审原页：`p1-p22`。

- reading_id：`K2R-W1-QM-SRC-0028`
- execution_lane：`TEXT_DIRECT`
- verification_mode：`VISUAL_PAGE`
- reviewed coverage：22/71
- read_status：`PARTIAL`
- Atomic Evidence：12 rows / REVIEWED or CONFLICTED
- p23-p71：**尚未获得 Reading credit**

71/71 render、contact-sheet/text-layer navigation 不能替代尚未完成的逐页 Reading credit。

## 2. Why this book enters now

进入 Cycle 1 的原因不是静态课程表，而是当前真实 implementation debt：

1. `QimenEngine` 刚暴露过 center-palace chief-door gap；
2. 36 个梁书甲子 sparse anchors 只验证 chief identity，full star/door/deity rotation 仍未验证；
3. 需要独立来源攻击当前对天禽/天芮寄宫、值符值使和八神体系的理解；
4. 旧 `QM-SRC-0036` 二手笔记本身已经暴露 source-map 与 operational-promotion 问题，必须回原书重做。

因此本书属于问题驱动 source selection。

## 3. Prior-model audit before fresh reading

Cycle 1 不假装“第一次接触善天道”。项目已经有旧二手笔记，所以先冻结旧认知，再检查它哪里错。

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

## 4. p1-p22 主审后的第一批 Source Findings

这些只表示“本书在这些页面怎么说”，不直接改变 Empirical Support。

### 4.1 书本自己已经反对部分机械直断

p4-p5 在讲阴阳时与行动取向后，明确提醒出行不能只由时辰一项决定，旧传歌诀仅供参考。

p5-p7 一面给八门传统吉凶与行动象意，一面又提醒不能一般化地把“生=吉、克=凶”当充分判断，仍需看具体条件。

这说明：把善天道简单理解成“更果断、更多直断”也不完整；来源内部本身已有情境限制。

### 4.2 九星旺相休囚不是一个无争议系统

p7-p9 明确承认旧说存在差异，作者选择其中一套解释，并把九星状态循环与通常按季节讲的五行旺相休囚区别开。

因此当前登记为 `CONFLICT_CANDIDATE`，不能因为课程选了某一说就直接成为 runtime truth。

### 4.3 拆补法的“实践更准”只能先保留为 source claim

p15-p18 用符头定上中下元，并讲拆补法跨节气处理；p18 对置闰表达批评，并以学员多次实践认为信息较多、准确性较高作为理由。

当前页段没有提供可审计分母、连续失败记录、matched control 或 preregistration，所以：

`作者经验主张 != 项目 Empirical Support`

对应 Evidence 使用 `NOT_CLAIM`，不把“实践很多”折算验证次数。

### 4.4 center-host 方向得到新的 source witness，但 full rotation 仍未闭环

p18-p19 把盘面分为地、天、人、神四层，并描述九星、八门、值符值使转动；门位说明把坤二天芮与中五天禽共同关联到死门结构。

p21-p22 又给出阳遁三局、阴遁八局完整示例。阴八例中，中五天禽参与值符结构并与死门值使关系同现。

这支持继续设计 `QimenEngine` 的非甲子/full-rotation source comparison，但不能从两例直接宣布完整星门神盘已正确。

### 4.5 八神问题比项目现有二分更复杂

p19-p20 把白虎/勾陈、玄武/朱雀以括注或隐含关系并列，同时记录小值符运转存在至少两种说法。

这说明现有 `GOUCHEN_ZHUQUE vs BAIHU_XUANWU` 冻结字段对防止 post-hoc switching 有工程价值，但未必已经准确表达历史 lineage。

当前动作：登记 `CONFLICT_CANDIDATE`，**不扩 schema、不改 enum、不静默同义化**。

### 4.6 “快速起局法”是作者教学工作流，不应倒推成古典通行法

p20 把快速起局法说明为为纸上起局、保留预测和积累经验而设计的操作流程。

因此其 provenance 先绑定作者/课程。工作流是否更方便与是否提高预测能力是两个问题。

## 5. Pre-reading attack questions

### Q1 — Center host / star-door rotation

当前工作假设：

- 中五宫没有独立门位；
- 五宫 chief identity 可得到天禽 / 死门；
- 但完整 star/door rotation 与 Tian-Qin/Tian-Rui hosting 仍未验证。

p19-p22 已产生候选 source witness；后续要从完整上下文和错误输入继续攻击，不只寻找支持句。

### Q2 — Deity-system relationship

当前项目把 `GOUCHEN_ZHUQUE` 与 `BAIHU_XUANWU` 作为独立冻结体系，目的是防止结果后静默替换；这个工程约束本身不等于历史谱系已经搞清。

已读 p19-p20 已显示名称关系与小值符运转异说；待 p23-p32 尤其 p27/p31 完整主审后再决定 lineage map 是否需要修改。

### Q3 — Setup / solar-term / yuan semantics

p15-p18 已确认课程使用符头与拆补法语境。下一步要将其与当前 engine 的 JieQi selection、`yuanOf`、setup method/time-boundary assumptions 做 source-defined comparison，而不是先把 production 改成书的版本。

### Q4 — Deterministic pattern claims

p33-p49 尚未逐页主审。任务不是背规则，而要拆成：

`SOURCE_PATTERN -> APPLICABILITY CLAIM -> TESTABLE CONSEQUENCE`

### Q5 — Method-layer shift around p50

p50-p71 尚未逐页主审。需要判断暗藏飞干及后续应用内容是同一排宫法扩展、另一算法层、资料拼接，还是只改变解释层。

### Q6 — Applied/high-risk layer

p51-p71 尚未逐页主审。即使原书明确写疾病、死亡、刑事、犯罪等断语，也只能先做 source fidelity / research classification，不直接 operationalize 为现实事实判断。

## 6. Anti-confirmation rule for this cycle

本书此前已有 p19/p21-p22 targeted secondary inspection，用来协助理解 center-host implementation gap；另外旧 `QM-SRC-0036` 已把部分善天道规则评价成“最实用/核心资产”。

因此完整阅读必须：

- 优先找当前实现/旧笔记的冲突页；
- 支持与冲突分开记录；
- source 内部冲突不能多数表决；
- 不因为代码已修过，就把书解释成支持现状；
- 不因为旧笔记写过“核心资产”，就优先给这些规则 operational credit。

## 7. First sprint execution order

- [x] K1 identity：`QM-SRC-0028 / WORK-000018`。
- [x] 旧笔记 correction overlay，冻结 prior model。
- [x] p1-p22 逐页视觉主审；12 条 Atomic Evidence。
- [ ] p23-p32：象意/八神/九宫层，继续查 deity lineage 与 source symbolism。
- [ ] p33-p49：pattern/provenance，标记强确定性断语与内部冲突。
- [ ] p50-p71：method-layer/lineage shift + 应用/高风险隔离。
- [ ] 完整 Book Distillate（只在 71/71 COMPLETE 后生成 final distillate）。
- [ ] 把真正改变实现或可验证模型的问题送入 implementation/prospective tests。
- [ ] Book Close 输出 `KEEP / REVISE / DELETE / NO-OP`。

## 8. Local AI packet scope

本地 AI 仍仅作为 `EXECUTION_HELPER_ONLY`：

- verify `QM-SRC-0028` SHA256/page count；
- 300 DPI+ render；
- 建 page/section map；
- 生成可追溯 visual/candidate packet；
- text extraction/OCR 仅 navigation；
- 跑 QimenEngine full-rotation raw output / wrong-input controls；
- 保存本地 artifacts / hashes / logs。

默认禁止 Reading/Evidence/Empirical Support credit、tracked edits、commit/push/merge、根据结果选择支持页、把高风险 source claim 当现实事实，以及用旧 `QM-SRC-0036` 笔记代替 `QM-SRC-0028` 原页。

## 9. Exit / switch conditions

正常关闭必须满足现行 `BOOK_ROTATION_CYCLE.md`，并且：

- 至少找到一个真正攻击当前实现/理论/旧笔记的 source point，或诚实记录 `NO_ATTACK_FOUND`；
- 至少一个 implementation/prospective test hook；
- 不以“71 页看完”单独作为完成条件；
- 不因为时间盒结束虚标 COMPLETE。

## 10. Theory-version discipline

本 Cycle 不预设会产生 v0.4。

只有新 source conflict / implementation failure / negative control / clean prospective evidence 真正改变 operational claim，才考虑理论版本升级。

读得更多，不等于理论自动更新。
