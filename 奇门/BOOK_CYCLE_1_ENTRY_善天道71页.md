# Book Cycle 1 Entry — 善天道《奇门遁甲讲义71页》

状态：ACTIVE ENTRY / STRUCTURAL_SURVEY_ONLY / READING_CREDIT=0

日期：2026-08-21

## 1. Candidate identity

文件：善天道《奇门遁甲讲义71页》

- candidate SHA256：`bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243`
- verified PDF page count：71
- renderer：PDF render 已成功完成 71/71 页结构巡检
- source_id / work_id：`PENDING_K1_INTAKE`

文件名不是 provenance。只有 K1 intake 完成后才分配/确认正式 source identity。

当前没有因为 contact sheet、text layer 或 targeted page inspection 给整书 Reading credit。

## 2. Why this book enters now

进入 Cycle 1 的原因不是静态课程表，而是当前真实 implementation debt：

1. `QimenEngine` 刚暴露过 center-palace chief-door gap；
2. 36 个梁书甲子 sparse anchors 只验证 chief identity，full star/door/deity rotation 仍未验证；
3. 需要独立来源攻击当前对天禽/天芮寄宫、值符值使和八神体系的理解。

因此本书属于问题驱动 source selection。

## 3. Pre-reading attack questions

### Q1 — Center host / star-door rotation

当前工作假设：

- 中五宫没有独立门位；
- 五宫 chief identity 可得到天禽 / 死门；
- 但完整 star/door rotation 与 Tian-Qin/Tian-Rui hosting 仍未验证。

本书 p19-p22 结构上直接涉及值符、值使、天禽/天芮和星门转动。

要找的是反例、例外与完整算法，不是只找“支持死门”的句子。

### Q2 — Deity-system relationship

当前项目把 `GOUCHEN_ZHUQUE` 与 `BAIHU_XUANWU` 作为独立冻结体系，防止结果后静默替换。

本书 p19-p20 的可见说明把白虎后括注勾陈、玄武后括注朱雀，并讨论不同八神运转说法。

待验证问题：

- 这是作者主张的同义替代？
- 是 lineage alias？
- 是教学层合并？
- 还是不同上下文的混合写法？

完整阅读前，不得把括号关系升级成项目等价规则，也不得立即修改 registry enum。

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

### Q5 — Applied/high-risk layer

p51-p71 涵盖词讼、疾病、求财、阳宅、刑事等实际事项，并出现死亡、犯罪、病理等高风险判断。

处理原则：

- source fidelity 可以学习；
- 高风险断语只保留为 source claim / research candidate；
- 不直接用于现实医疗、法律、犯罪事实判断；
- 若产生研究价值，转成低风险、可评分的结构问题，而不是照搬结论。

## 4. Anti-confirmation rule for this cycle

本书此前已有 p19/p21-p22 targeted secondary inspection，用来协助理解 center-host implementation gap。

因此这轮完整阅读必须主动防止 selection bias：

- 先找与当前实现冲突的页；
- 再找支持页；
- 支持与冲突分开计数；
- source 内部冲突不能由“多数页支持”自动抹平；
- 不因为当前代码已经修过，就把书解释成支持现状。

## 5. First sprint execution order

1. 完成 K1 intake：canonical identity / source_id / lane / copyright metadata；
2. p1-p22 逐页视觉主审：先攻 setup + value-chief + rotation；
3. p23-p32：象意层，区分 source symbolism 与 operational feature；
4. p33-p49：pattern/provenance，标记确定性断语与内部冲突；
5. p50-p71：判断是否发生 method-layer/lineage shift，隔离应用与高风险内容；
6. 形成 Atomic Evidence / Book Distillate；
7. 只把真正改变实现或可验证模型的问题送入 implementation/prospective tests；
8. Book Close 时必须输出 `KEEP / REVISE / DELETE / NO-OP`。

## 6. Local AI packet scope

本地 AI 仅作为 `EXECUTION_HELPER_ONLY`：

- verify SHA256/page count；
- 300 DPI+ render；
- 建 chapter/page map；
- 对 p15-p22、p33-p49、p50-p71 生成可追溯 crop packet；
- text extraction/OCR 仅 navigation；
- 跑 QimenEngine full-rotation raw output / wrong-input controls；
- 保存本地 artifacts / hashes / logs。

默认禁止：

- Reading/Evidence/Empirical Support credit；
- tracked edits；
- commit/push/merge；
- 根据结果选择支持页；
- 把 source deterministic claim 当现实事实。

## 7. Exit / switch conditions

正常关闭必须满足现行 `BOOK_ROTATION_CYCLE.md`。

额外要求：

- 至少找到一个真正攻击当前实现/理论的 source point，或明确记录 `NO_ATTACK_FOUND`；
- 至少一个 implementation/prospective test hook；
- 不以“71 页看完”单独作为完成条件；
- 不因为时间盒结束虚标 COMPLETE。

## 8. Theory-version discipline

本 Cycle 不预设会产生 v0.4。

只有新 source conflict / implementation failure / negative control / clean prospective evidence 真正改变 operational claim，才考虑理论版本升级。

读得更多，不等于理论自动更新。
