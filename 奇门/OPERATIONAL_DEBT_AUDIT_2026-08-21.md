# 奇门运行知识债务审计 — 2026-08-21

状态：ACTIVE REVIEW / runtime migration in progress

目的：记录已经迁移的旧确定性规则与仍未处理的运行债务，防止“方法论文件升级了”被误认为“整个执行系统已经升级”。

## 一、已完成迁移

### OD-01 固定八步法强制确定性
已迁移为 Reality Baseline → Method/Setup/Role/Feature Freeze → Competing Branches → Frozen Prediction → Outcome Audit。

### OD-02 古籍/师傅身份权威链
已废弃。SOURCE provenance 与现实真值分离；冲突按 object/layer/method/context 拆分。

### OD-03 内外盘旧错误
当前 baseline：阳遁内 `1、8、3、4`，外 `9、2、7、6`；阴遁反转。传统“内快外慢”仍是候选语义。

### OD-04 基础五行与六十甲子逻辑错误
`qimen-basics / qimen-shengke` 已纠正基础结构，传统象意与结构事实分层。

### OD-05 前五/后五与干支阴阳混名
运行层改为 `FIRST_FIVE_GROUP / LAST_FIVE_GROUP`；原书旧术语保留时标 `TERMINOLOGY_CONFLICT`。

### OD-06 四害/四避开混用
`qimen-sihai` 已改为状态特征识别，不再自动打折/放大。

### OD-07 入墓来源内部不一致
不静默统一；当前结构 baseline 与 source-specific 变体分开。

### OD-08 固定用神表
已改为 `Role Map Freeze`，竞争 Role Map 必须反馈前保存。

### OD-09 应期方法超市
已改为 timing method family / eligible features / window / tolerance feedback-before freeze。

### OD-10 全局优先级、凶格计分、旺衰固定折扣
已从 operational authority 撤销。

### OD-11 qimen-bigpicture 固定伏吟/反吟行动命令
已迁移为 structural feature + context candidate，高风险古断退出自动运行。

### OD-12 VISUAL_REQUIRED 只有阻塞没有真读路径
已实现 canonical hash → render → main-review visual inspection → page accounting → Evidence；`QM-SRC-0001` 已完成 57/57 一例闭环。

### OD-13 qimen-gexia 混合吉格/凶格/时间状态/十干克应
已迁移为 Pattern Registry：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

十干克应保留 `(天盘干, 地盘干)` 有序方向；旧固定凶格计分退出运行；来源冲突显式保存。

### OD-14 qimen-gongpan 把结构、象意、状态、Role 与高风险现实事件混成一层
已迁移为 Component / Relation Registry：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

并新增 `star_state_system / door_state_system` feedback-before freeze。人体/疾病/犯罪/灾害降为 `HIGH_RISK_SOURCE_SYMBOLISM`。

### OD-15 qimen-qiju 起局定义与时间边界漂移
legacy 深查发现：

- 超神/接气方向前后反转；
- 拆补“固定5+5+5”与“残元+补元”两套描述；
- 拆补/茅山定义重叠；
- 子时边界冲突；
- 宫号顺序与顺/逆时针语义混用。

已迁移为 Setup Method Registry，并将以下字段加入全链冻结：

`setup_method / setup_calibration / seasonal_alignment / time_boundary_system / time_family / layout_method`

不同算法若生成不同盘，必须反馈前 A/B，不能结果后挑盘。

### OD-16 qimen-cases 把书本复盘、直断和真实预测混成“经验”
legacy 文件出现“预测有约八成准确率”等无可审计分母的数字，并把“玄武=假冒伪劣”“惊门凶格=必有官司”等来源断语放在可直接调用层。

当前迁移为 Case Classification：

- `SOURCE_RETROSPECTIVE_CASE`
- `PROJECT_RETROSPECTIVE_REANALYSIS`
- `PROSPECTIVE_FROZEN_CASE`
- `CONTAMINATED_CASE`
- `IMPLEMENTATION_FAILURE_CASE`
- `UNSCORABLE_ANECDOTE`

只有满足 Prospective Registry、结果未知、反馈前冻结且可评分的 `PROSPECTIVE_FROZEN_CASE` 才可能贡献 Empirical Support。

旧“约八成准确率”标 `UNSUPPORTED_ACCURACY_CLAIM`；项目不在样本不足时显示总体准确率。

## 二、当前仍未完成的主要债务

### P2 — qimen-yange

需要重做 provenance：

- 歌诀版本/异文来源；
- 口诀中的操作规则绑定哪个 method/setup；
- 不用“多处一致”替代原典版本差异；
- 口诀若进入运行，必须经过 source lineage / applicability / prospective eligibility 审查。

### P2 — 旧《奇门遁甲知识库.md》monolith

仍保留历史规则、摘记、失败补丁与已废弃断法。当前不无差别重写，以免抹掉历史证据；运行时由 `CURRENT_METHOD_CONSTRAINTS.md` authoritative overlay 压住，逐技能迁移。

### P1 research — 梁书十八局 sparse anchors

Reading 57/57 已完成，但 `ANCHORS_VERIFIED / IMPLEMENTATION_CHECKED` 尚未全部闭环。fixture/CI 通过只能证明 source fidelity / execution integrity，不代表 predictive validity。

### P1 research — Test A-G prospective trials

尚未取得足够正式未知结果样本。Prospective Registry 允许为空；不得为了“有验证数据”制造案例。

## 三、这轮自省的新结论

### 1. 隐藏模型变量比“口诀错一个字”更危险

起局法、日界、八神体系、旺衰算法若不显式冻结，就会在结果后成为无穷救援空间。因此它们必须和用神/feature/应期一样成为一等 protocol fields。

### 2. 案例库最容易制造伪经验支持

书本复盘、作者自述“实践验证”、项目结果已知后的重新解释，都可以帮助理解方法，但不能与结果未知的前瞻预测共享同一个“应验率”分母。

### 3. runtime contract 是防复发装置，不是预测验证

CI 应检查旧确定性断法是否悄悄恢复、必要冻结字段是否缺失、污染案例是否可被删除等工程性质问题。CI 绿不等于术数有效。

### 4. 新理论当前最可辩护的增量仍是减少结果后自由度

如果未来前瞻数据表明这些约束没有提高可复现性、校准或相对 baseline 表现，这套理论本身也应被 NARROW / REVISE / DEPRECATE。

## 四、下一顺序

`exact-head CI`
→ `qimen-yange provenance migration`
→ `十八局 sparse anchors 主审复核 / implementation check`
→ `开始真实 unknown-outcome prospective trials`
→ `按 outcome audit 更新 Rule Lifecycle`

任何 source fixture、runtime contract、案例复盘或 CI 通过，都不得写成“奇门预测已经验证”。
