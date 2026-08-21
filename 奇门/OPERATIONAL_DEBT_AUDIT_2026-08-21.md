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

2026-08-21 又发现：视觉看过原页仍可能因跨页拓扑误判而把标题配错表体。因此新增认识：

`Visual Presence != Semantic Association`

VISUAL_REQUIRED 后续还需关注 printed-page/spread topology 与表内结构校验。

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

legacy “烟波钓叟歌详解”已迁移为 Verse / Formula Provenance Registry：

`PRIMARY_TEXT / COMMENTARY_TEXT / MODERN_PARAPHRASE / TEACHING_MNEMONIC / PROJECT_GLOSS`

并区分：

`PAGE_VERIFIED / LEGACY_ATTRIBUTION / ATTRIBUTION_UNRESOLVED / SOURCE_INCONSISTENCY / CROSS_SOURCE_VARIANT`

操作口诀路由到 `qimen-qiju`；格局干对冲突路由到 `qimen-gexia`。旧 skill 的引用不得反向证明原典。

### OD-10 梁书十八局 sparse-anchor 主审

第一次主审把 spread 同一 raster 的右侧标题误配给左侧表体，导致一局位移和假的 `YIN-01/p49 missing table`。

第二次按 printed-page topology + 表内甲子结构纠正：

- Yang1-9 table bodies: p31,p32,p33,p34,p36,p35,p37,p38,p39
- Yin9-1 table bodies: p40-p48
- p35/p36 PDF scan order 与实体印刷页序交换
- all 18 tables visible
- all 18 fixtures: `ANCHORS_VERIFIED`
- 2 Jiazi anchors each, total 36

该错误记录为 `MAIN_REVIEWER_SEMANTIC_ASSOCIATION_ERROR`，不是 source anomaly。

## 二、当前仍未完成的主要研究债务

### P1 — 梁书十八局 `IMPLEMENTATION_CHECKED`

18 局的 sparse anchors 已完成主审，但代码尚未全部与 36 anchors 做正式比较。

下一 Gate 必须包含：

- correct-bureau positive controls;
- wrong-bureau controls;
- superseded shifted-page mapping control;
- permuted-anchor controls;
- bureau-5 center palace / 值使处理专项检查。

只有区分正确/错误输入的实现测试通过后，才能把对应 fixture 升为 `IMPLEMENTATION_CHECKED`。

### P1 — Test A-G prospective trials

尚未取得足够正式未知结果样本。Prospective Registry 允许为空；不得为了“有验证数据”制造案例。

### P2 — 旧《奇门遁甲知识库.md》monolith

仍保留历史规则、摘记、失败补丁与已废弃断法。当前不无差别重写，以免抹掉历史证据；运行时由 `CURRENT_METHOD_CONSTRAINTS.md` authoritative overlay 压住。

### P2 — source-specific lineage deep review

仍需逐来源回查：

- gexia 的格名/干对/天盘地盘方向；
- gongpan 的九星/八门 state systems；
- qiju 的拆补/置闰/茅山和时间边界；
- yange 的原典 witness、异文、现代转述与口诀来源。

### P2 — Evidence locator normalization

梁书 Evidence 0022/0023 的旧粗粒度 page range 来自第一次表体索引，应由本次 source correction overlay 解释并在后续 Evidence maintenance 中规范成 corrected table-body ranges。不得让旧 locator 反过来推翻已重新视觉核验的 body mapping。

## 三、当前方法论认识

### 1. 隐藏模型变量必须变成冻结字段

起局法、日界、八神体系、旺衰系统若不显式记录，就会成为结果后救援空间。

### 2. 案例库、歌诀库和“绿色 CI”都可能制造伪权威

“作者说实践验证”“多本书都引用”“validator/CI PASS”分别只能证明有限维度。若共享的 expected value 本身写错，CI 会稳定地验证错误。

### 3. runtime contract 是防复发装置

CI 负责阻止旧确定性断法、隐藏字段、无支持准确率等重新进入运行；CI 绿不等于术数有效，也不保证 reviewer 的 source model 正确。

### 4. 新理论当前最可辩护的价值仍是减少后见自由度

如果未来 prospective data 不改善可复现性、校准或相对 baseline 表现，理论本身也必须 NARROW / REVISE / DEPRECATE。

### 5. 约束本身也要接受压缩

每新增一个 context key、branch 或 Gate，都应有未来可以删除/合并它的条件。研究系统不能只增不减。

## 四、下一顺序

`source-mapping correction CI`
→ `十八局 implementation comparison`
→ `wrong-bureau / shifted-page / permuted controls`
→ `source-specific lineage deep review`
→ `真实 unknown-outcome prospective trials`
→ `Outcome Audit / Rule Lifecycle / Model Compression`

任何 source fixture、runtime contract、案例复盘、歌诀 provenance 或 CI 通过，都不得写成“奇门预测已经验证”。
