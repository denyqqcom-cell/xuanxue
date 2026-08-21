# 奇门运行知识债务审计 — 2026-08-21

状态：ACTIVE REVIEW / implementation-integrity milestone reached

目的：记录已经迁移的旧确定性规则与仍未处理的研究债务，防止“方法论升级”被误认为“整个执行系统已验证”。

## 一、已完成的主要 runtime migration

### OD-01 固定模板与身份权威链
固定八步强制结论、古籍/师傅身份优先已废弃。当前运行受 `CURRENT_METHOD_CONSTRAINTS.md` 约束。

### OD-02 基础结构错误与旧全局硬规则
已处理：内外盘旧错误、基础五行错误、前五/后五命名混乱、四害/四避开混用、固定全局优先级、固定凶格计分、旺衰固定折扣、`>=3=已验证` 等。

### OD-03 qimen-bigpicture / yongshen / yingqi
已分别迁移为 Big Picture Feature Map、Role Map Freeze、Timing Method Freeze。结果后换用神/应期不得修补原预测。

### OD-04 VISUAL_REQUIRED 阅读链
已实现 canonical hash → render → 主审 visual inspection → page accounting → Evidence；`QM-SRC-0001` 已完成 57/57 阅读/蒸馏闭环。

### OD-05 qimen-gexia
已迁移为 Pattern Registry：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

固定凶格计分退出运行；来源冲突显式保存。

### OD-06 qimen-gongpan
已迁移为 Component / Relation Registry，并把 `star_state_system / door_state_system` 提升为 feedback-before freeze 变量。高风险人体/疾病/犯罪/灾害类象降为 `HIGH_RISK_SOURCE_SYMBOLISM`。

### OD-07 qimen-qiju
legacy 深查发现超神/接气方向冲突、拆补算法冲突、拆补/茅山重叠、子时边界冲突、宫序/旋转语义混用。已迁移为 Setup Method Registry，并冻结 setup/time/layout 等关键分叉。

### OD-08 qimen-cases / cases-v2
书本复盘、项目复盘、前瞻、污染、实现错误与不可评分故事已拆开。无可审计分母的“约八成准确率”等标为 `UNSUPPORTED_ACCURACY_CLAIM`。

### OD-09 qimen-yange
已迁移为 Verse / Formula Provenance Registry，区分原文、注释、现代改写、教学口诀和项目释义；旧技能引用不得反向证明原典。

### OD-10 梁书十八局 Source-Topology 纠错

第一次主审把 spread 右侧标题错误配给左侧表体，造成 one-bureau shift；validator/CI 因共享错误 expected mapping 仍 PASS。

重新按 printed-page topology + table-internal Jiazi structure 复核后：

- 18/18 table bodies visible；
- 36 sparse anchors main-reviewed；
- former shifted mapping / p35-p36 scan-order swap / Yin1→p49 已成为 fail-closed controls；
- 新增 `Visual Presence != Semantic Association` 与 Validation Independence。

### OD-11 梁书十八局 Jiazi sparse implementation integrity

Production path：`ziwei-core/src/main/kotlin/com/xuanxue/qimen/QimenEngine.kt`。

对 18 个局、36 个 tracked Jiazi anchors 做了直接 implementation comparison。预修正结果：

- chief star：18/18 matched；
- chief door：16/18 matched；
- Yang-5 / Yin-5 暴露 `CENTER_CHIEF_DOOR_IDENTITY`：中五宫时 production 返回空值，source oracle 为 `死`。

按 source-bounded 范围修正 chief identity：中五宫 `天禽 / 死门`。没有把完整门盘旋转一起宣布正确。

Test commit：`86e0b37d31549c0b2c16154ab1b8b81d83ebe454`

Exact-head CI #282：`completed / success`，其中 stable core `:ziwei-core:test` 通过：

- 18 bureau positive controls；
- wrong-bureau controls；
- permuted star/door controls；
- bureau-5 regression。

因此 18 fixtures 可在后续 status commit 中升级 `IMPLEMENTATION_CHECKED`，但该状态只覆盖 36 个 tracked Jiazi sparse anchors。

## 二、当前仍未完成的主要研究债务

### P1 — Full-plate implementation debt

Sparse chief-identity milestone 不能向上继承为完整九宫正确。

仍需验证：

- non-Jiazi source-table cells；
- full star rotation；
- full eight-door rotation / center-host semantics；
- Tian-Qin/Tian-Rui hosting across times；
- deity-system-specific rotation；
- setup/time-boundary timestamp branches；
- wrong-time / shuffled full-chart negative controls。

在这些完成前，应用 UI 对完整九宫继续应标“实验盘/未黄金夹具核验”。

### P1 — clean unknown-outcome prospective trials

Prospective Registry 仍缺足够正式未知结果样本。这项债务现在不能再长期排在“继续读更多书/继续加更多 Gate”之后。

禁止：

- contaminated case 折算“半次真验证”；
- outcome-known retrospective 计 Empirical Support；
- 单个 HIT/MISS 直接改全局规则。

### P2 — 旧《奇门遁甲知识库.md》monolith

仍保留历史规则、摘记、失败补丁与已废弃断法。当前不无差别重写，以免抹掉历史证据；运行时由 authoritative overlay 压住。

### P2 — source-specific lineage deep review

仍需逐来源回查：

- gexia 格名/干对/方向；
- gongpan 九星/八门 state systems；
- qiju 拆补/置闰/茅山与时间边界；
- yange 原典 witness、异文、现代转述。

但不得把“读完所有书”设成开始前瞻验证的前置条件。

### P2 — protocol / introspection complexity debt

K2 已有较多 protocol、Gate、registry 和 runtime contracts。它们解决真实旧债，但本身也可能成为复杂度债务。

后续持续检查：

- 哪些 context key 长期不改变输出；
- 哪些 Gate 重复表达同一约束；
- 哪些反省只有提醒价值，不值得再转 schema；
- 是否能用更少字段维持同等 reproducibility/discrimination。

## 三、当前方法论认识

### 1. 显式化不是终点
隐藏变量必须显式，否则会成为结果后救援空间；但字段一旦进入 protocol，也不获得永久存在权。

### 2. 反省与 CI 都可能制造伪进步
“我又发现很多误区”“CI 又多了几个 Gate”不能直接提高预测能力。Validator PASS 甚至可能与错误 oracle 一起共错。

### 3. 从结果学习必须隔离
单个 outcome 先生成 `CASE_LESSON_CANDIDATE`：

`Outcome -> Case Lesson -> Testable Hypothesis -> Prospective Discrimination -> Rule Update`

### 4. 当前原创方向：反证 + 压缩

`FRAME -> FREEZE -> RELATE -> DISCRIMINATE -> FALSIFY -> COMPRESS`

理论价值看未知结果下的区分、校准、baseline delta 与删减能力，不看规则数量。

## 四、下一顺序

`fixture status/audit exact-head CI`
→ `启动 clean unknown-outcome prospective trials`
→ `并行小范围 full-plate negative-control research`
→ `由真实 failure exposure 选择下一轮 source-specific reading`
→ `Outcome Audit / Rule Lifecycle / Model Compression`

文献继续学，但不再采用“下一本接下一本”的被动堆书模式。

任何 source fixture、runtime contract、案例复盘、歌诀 provenance、理论创新或 CI 通过，都不得写成“奇门预测已经验证”。
