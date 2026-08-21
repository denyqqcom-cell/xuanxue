# 奇门运行知识债务审计 — 2026-08-21

状态：ACTIVE REVIEW / runtime migration in progress

目的：记录已经迁移的旧确定性规则与仍未处理的研究债务，防止“方法论升级”被误认为“整个执行系统已验证”。

## 一、已完成的主要 runtime migration

### OD-01 固定模板与身份权威链
固定八步强制结论、古籍/师傅身份优先已废弃。当前使用 Reality Baseline → Method/Setup/Role/Feature Freeze → Competing Branches → Frozen Prediction → Outcome Audit。

### OD-02 基础结构错误与旧全局硬规则
已处理：内外盘旧错误、基础五行错误、前五/后五命名混乱、四害/四避开混用、固定全局优先级、固定凶格计分、旺衰固定折扣、`>=3=已验证` 等。

### OD-03 qimen-bigpicture / yongshen / yingqi
已分别迁移为 Big Picture Feature Map、Role Map Freeze、Timing Method Freeze。结果后换用神/应期不得修补原预测。

### OD-04 VISUAL_REQUIRED 阅读链
已实现 canonical hash → render → 主审 visual inspection → page accounting → Evidence；`QM-SRC-0001` 已完成 57/57 一例闭环。

### OD-05 qimen-gexia
已迁移为 Pattern Registry：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

十干克应保留 `(天盘干, 地盘干)` 有序方向；来源冲突显式保存；固定凶格计分退出运行。

### OD-06 qimen-gongpan
已迁移为 Component / Relation Registry：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

新增 `star_state_system / door_state_system` feedback-before freeze；高风险人体/疾病/犯罪/灾害类象降为 `HIGH_RISK_SOURCE_SYMBOLISM`。

### OD-07 qimen-qiju
legacy 深查发现超神/接气方向冲突、拆补算法描述冲突、拆补/茅山重叠、子时边界冲突、宫号顺序与旋转语义混用。

已迁移为 Setup Method Registry，并将：

`setup_method / setup_calibration / seasonal_alignment / time_boundary_system / time_family / layout_method`

加入全链冻结。不同算法生成不同盘时必须反馈前 A/B。

### OD-08 qimen-cases / cases-v2
旧案例库把书本复盘、直断条目、项目复盘与真实前瞻混在同一“应验率”语义中，并存在“预测有约八成准确率”等无可审计分母的数字。

已迁移为 Case Classification：

- `SOURCE_RETROSPECTIVE_CASE`
- `PROJECT_RETROSPECTIVE_REANALYSIS`
- `PROSPECTIVE_FROZEN_CASE`
- `CONTAMINATED_CASE`
- `IMPLEMENTATION_FAILURE_CASE`
- `UNSCORABLE_ANECDOTE`

只有符合 Prospective Registry、结果未知、反馈前冻结且可评分的 `PROSPECTIVE_FROZEN_CASE` 才可能贡献 Empirical Support。旧总体准确率标 `UNSUPPORTED_ACCURACY_CLAIM`。

### OD-09 qimen-yange
legacy “烟波钓叟歌详解”把古籍归因、现代解释、教学口诀、速查表、格局星级和项目释义混成一层，并用统一“经典/文献来源”语气展示。

已迁移为 Verse / Formula Provenance Registry：

`PRIMARY_TEXT / COMMENTARY_TEXT / MODERN_PARAPHRASE / TEACHING_MNEMONIC / PROJECT_GLOSS`

并区分：

`PAGE_VERIFIED / LEGACY_ATTRIBUTION / ATTRIBUTION_UNRESOLVED / SOURCE_INCONSISTENCY / CROSS_SOURCE_VARIANT`

操作口诀必须路由到 `qimen-qiju` 绑定 method/setup；格局干对冲突路由到 `qimen-gexia` lineage review。旧 skill 的引用不得反向证明原典。

### OD-10 梁书十八局 source fixture 主审纠错

第一次主审把同一 scan spread 的右侧局图标题错误配给左侧表体，造成 one-bureau shift；validator/CI 因共享错误 expected mapping 仍然 PASS。

重新按 printed-page topology + table-internal Jiazi structure 复核后已纠正：

- 18/18 table bodies visible；
- 18/18 fixtures = `ANCHORS_VERIFIED`；
- 36 sparse anchors；
- p35/p36 scan order swap 已显式保留；
- former shifted mapping / Yin1→p49 已成为 negative controls。

新增：`Visual Presence != Semantic Association` 与 Validation Independence。

## 二、当前仍未完成的主要研究债务

### P1 — 梁书十八局 implementation integrity

Source side 18/18 已达到 `ANCHORS_VERIFIED`，但尚未全部 `IMPLEMENTATION_CHECKED`。

当前应直接对 production `QimenEngine` 做 comparison，并重点检查：

- bureau-specific Jiazi chief star/door；
- bureau 5 中宫/寄宫的值使处理；
- simplified/traditional normalization 是否只做文字归一、不改变结构；
- wrong-bureau / shifted / permuted negative controls 是否真的 fail。

只有 source witness、fixture oracle、production implementation 与 negative controls 形成区分链后才能升级。

### P1 — clean unknown-outcome prospective trials

Prospective Registry 仍缺足够正式未知结果样本。

这项债务现在不能再长期排在“继续读更多书/继续加更多 Gate”之后。必要 implementation integrity 完成后，应开始真实可失败 trial。

禁止：

- contaminated case 折算“半次真验证”；
- outcome-known retrospective 计 Empirical Support；
- 单个 HIT/MISS 直接改全局规则。

### P2 — 旧《奇门遁甲知识库.md》monolith

仍保留历史规则、摘记、失败补丁与已废弃断法。当前不无差别重写，以免抹掉历史证据；运行时由 `CURRENT_METHOD_CONSTRAINTS.md` authoritative overlay 压住。

### P2 — source-specific lineage deep review

仍需逐来源回查：

- gexia 的格名/干对/天盘地盘方向；
- gongpan 的九星/八门 state systems；
- qiju 的拆补/置闰/茅山和时间边界；
- yange 的原典 witness、异文、现代转述与口诀来源。

但这部分不得无限扩张成“把所有书读完以后才允许开始前瞻验证”。

### P2 — protocol / introspection complexity debt

K2 已形成较多 protocol、Gate、registry、runtime contracts。它们解决真实旧债，但本身也可能成为复杂度债务。

后续要持续检查：

- 哪些 context key 长期不改变输出；
- 哪些 Gate 只是重复表达同一约束；
- 哪些反省只有提醒价值，不值得转成 schema；
- 是否可以用更少字段保持同样的 reproducibility/discrimination。

## 三、当前方法论认识

### 1. 隐藏模型变量必须显式，但显式后也要能删除

起局法、日界、八神体系、旺衰系统若不显式记录，会成为结果后救援空间；但一个字段一旦进入 protocol，并不获得永久存在权。

### 2. 案例库和歌诀库容易制造伪权威，反省日志也会制造伪进步

“作者说实践验证”“多本书都引用”“口诀很经典”只能提高 provenance/source consensus。

同样，“我又发现了十个误区”“CI 又多了五个 Gate”也不能直接提高预测能力。

### 3. runtime contract 是防复发装置，不是效果证明

CI 负责阻止旧确定性断法、隐藏字段、无支持准确率等重新进入运行；CI 绿不等于术数有效，validator 绿也不保证 oracle 正确。

### 4. 从结果学习必须隔离

单个 outcome 只生成 `CASE_LESSON_CANDIDATE`：

`Outcome -> Case Lesson -> Testable Hypothesis -> Prospective Discrimination -> Rule Update`

禁止从一次成败直接重写全局理论。

### 5. 当前原创方向从“约束”继续走向“反证 + 压缩”

当前理论草案：

`FRAME -> FREEZE -> RELATE -> DISCRIMINATE -> FALSIFY -> COMPRESS`

理论价值不看规则数量，而看：能否在未知结果下形成区分、能否接受失败、能否删掉无增量部分。

## 四、下一顺序

`exact-head CI`
→ `QimenEngine implementation comparison / bureau-5 chief-door audit`
→ `wrong-bureau / shifted / permuted negative controls`
→ `eligible fixture rows -> IMPLEMENTATION_CHECKED`
→ `启动 clean unknown-outcome prospective trials`
→ `在真实 failure exposure 下选择下一轮 source-specific reading`
→ `Outcome Audit / Rule Lifecycle / Model Compression`

文献继续学，但不再采用“下一本接下一本”的被动堆书模式。

任何 source fixture、runtime contract、案例复盘、歌诀 provenance、理论创新或 CI 通过，都不得写成“奇门预测已经验证”。
