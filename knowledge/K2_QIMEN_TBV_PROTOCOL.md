# K2 奇门 TBV 反向重析协议 v1.2

TBV = Theory — Boundary — Validation（理论—边界—验证）。

状态：`ACTIVE / PARTIAL`  
阶段：K2B Cognitive Reconstruction  
Claim Extraction：`BLOCKED`  
Empirical Credit：`NONE`

## 1. 目的

TBV 用于对已经完成 Deep Visual Review 的奇门材料做第二遍反向阅读。第一遍回答“来源实际写了什么、作品/章节/方法结构怎样”，第二遍强制拆成：

`THEORY -> BOUNDARY -> VALIDATION`

只有三层都被显式记录，source-local 方法才可能进入后续 SCRM 候选 operator；即使进入，也不获得现实有效性信用。

## 2. THEORY

TBV 不把规则列表、页数或表项数量等同理论。优先提炼：对象定义、问题域、角色模型、盘层、时间模型、关系配置、生成规则、程序优先级、多观察通道、修正规则与作者自己的方法批判。

若一个 carrier 含多个 segment/work/method layer，必须分开表示。物理同册不等于同一作品、同一作者声音、同一理论或同一独立证据票。

## 3. BOUNDARY

每条理论至少反查：question domain、method layer、role frame、plate/symbol instance、temporal model、source/school context、prerequisite、exclusion 与 stop/failure condition。

统一执行：

`SOURCE CONTAINS RULE != RULE IS UNIVERSAL`

`SOURCE ENDORSES RULE != RULE IS EMPIRICALLY VALID`

边界不清时保留 `CONTEXT_REQUIRED / HOLD`，不得替来源补成“奇门通用真理”。

## 4. VALIDATION

信用必须分账：

- source_credit：来源是否完整视觉核验；
- structure_credit：结构能否稳定重建；
- method_credit：能否明确还原来源怎样使用；
- empirical_credit：未知结果条件下是否经过前瞻验证。

本阶段所有 TBV 条目：

`empirical_credit = NONE`

古籍年代、作者名气、案例数量、表项数量、来源自我主张、来源自我批判、现代作者强调实践，都不能越级成为 empirical credit。

## 5. Universalization Gate

所有 TBV review：

`universalization_status = BLOCKED`

跨来源规则在 Claim Extraction 正式开放前，不做“多数书都这么说所以是真的”的归并。先检查 work/course dependence、术语同名异义、role frame、plate layer、temporal model、method layer 与前置条件。

## 6. 与 SCRM / QCIC 的接口

流程：

`SOURCE -> Deep Reading -> TBV -> QCIC eligibility -> SCRM scenario mapping/operator -> prospective validation`

TBV 可以给出 source-local candidate、boundary-only、mixed-stance hold、historical-only 或 hold；不能给出无边界万能口诀、已验证现实规律或高风险现实操作建议。

## 7. Wave A / Wave B 当前状态

Wave A 已覆盖：QM-SRC-0015、0017、0019、0020、0021 与 WF-QM-JIADUN-ZHENSHOU-001。

Wave B 已覆盖：WF-QM-SANYUAN-QIMEN-001、WF-QM-JINHAN-YUJING-001，以及 QM-SRC-0009、0024、0027、0028、0029。

其中：

- QM-SRC-0009 已完成 535/535 原页视觉复核。它是现代白话图解载体，内部至少要分传统原文/古注、现代白话提要、现代图解与出版社说明等 voice；方法上同时包含确定性排局、静态象意、条件关系、派生格局、回顾性案例与法术/仪式层。下部 QM-SRC-0010 尚未做双边视觉身份确认，因此本轮只关闭 0009 的 source-level semantic/TBV，不提前闭合上下部 work lineage，也不创建依赖 work_id 的 deep-source distillate；
- QM-SRC-0024 是 composite carrier，QIMEN primary work content 必须按 SEG-002 / SEG-004 分段绑定，不能把共同装订当成统一理论；
- QM-SRC-0027 / 0028 / 0029 虽分别做 source-level TBV，以保存 synopsis / foundation / advanced-extension 的独特边界，但三者属于 `COURSE-QM-SHANTIADAO-001`，独立性继续执行 `COURSE_FAMILY_SINGLE_VOTE`；三个 TBV source rows 不是三张 empirical/corroboration 票；
- 已完成 visual deep review 的 17 个奇门来源，目前 `effective_deep_source_coverage = 17/17`。

但全项目仍有：

`global_unknown_textual_backlog = 92`

因此：

`full_reviewed_material_tbv_coverage = false`

`status = PARTIAL`

**Deep-reviewed layer 的 TBV 17/17 只代表已深读层没有 TBV gap，不代表全语料库掌握完成。**

统一执行：

`DEEP_REVIEW_TBV_COVERAGE != FULL_CORPUS_COMPLETION`

## 8. 覆盖与独立性

`COVERAGE CREDIT != INDEPENDENT EVIDENCE VOTE`

work-family review 可以覆盖多个 member source，但仍只是一条 family-level provenance unit；同理，同一 course family 中的独立 work 为保存各自 theory/boundary 可分别接受 TBV review，却不能因此重复增加独立 corroboration。

TBV registry 可使用 aggregate 与 `knowledge/K2_QIMEN_TBV_REVIEW_REGISTRY.d/*.jsonl` shards。shard 只是存储方式，不绕过 duplicate unit、source identity、coverage 与 fail-closed gate。

## 9. Known-outcome training 与评价隔离

`KNOWN_OUTCOME_TRAINING != PROSPECTIVE_EVALUATION`

假设事件、已经知道结果的历史事件、书中反馈案例和复盘盘例可用于训练算法、检查方法重建、发现表示错误与冲突，但只能取得 `TRAINING / METHOD RECONSTRUCTION` 信用。

真正 prospective evaluation 必须使用结果未知、反馈前冻结的 clean holdout；已用于训练/复盘的案例及语义近重复不得重新包装成盲测。若发生 leakage，该批只能降为方法研究材料。

## 10. QM-SRC-0009 反审新增约束

完整阅读 0009 后新增以下机器应保留的认知边界：

`PREDEFINED PROCEDURAL BRANCHING != POST-HOC INTERPRETIVE SEARCH`

复杂规则并不自动等于 hindsight freedom。反馈前由历法、局式、盘层和已冻结条件机械决定的分叉，与结果后才选择用神、格局、象意或方法层必须分开审计。

`CALCULATION CONSISTENCY != REAL-WORLD VALIDITY`

来源内部的定局、超神、接气、置闰和错误检点可以证明算法内部可重建，不等于现实预测有效。

`TEXTUAL PRECISION != EMPIRICAL VALIDATION`

九星临十二时辰等条目即使给出非常具体的人物、事件、方向和期限，也不能凭文字具体程度升级经验信用。

`NAMED PATTERN = DERIVED FEATURE`

若一个“格”完全由底层干、门、星、神、宫或盘层实例决定，其格名不能与构成变量重复作为独立证据。

`EDITORIAL REPETITION != INDEPENDENT CORROBORATION`

同一规则在原文、白话、表格、图解和后续章节中反复出现，只增加该编辑体系中的覆盖和重要性，不增加独立来源票。

`SOURCE PROHIBITION != EPISTEMIC ABSTENTION`

五不遇时等来源禁忌是 source-local operator；SCRM 因映射不稳、信息不足或模型冲突而 ABSTAIN 是认识论机制，二者不得偷换。

`TRANSMISSION PRESTIGE != EVIDENCE QUALITY`

秘传、师承、只传贤德等传承伦理与身份叙事不能增加 empirical credit。

0009 的现代白话提要在玉女反闭部分明确指出其说法“玄而又玄”且“没有什么理论依据”，但仍因属于奇门传统而介绍。因此继续执行：

`SOURCE CONTAINS METHOD != SOURCE ENDORSES METHOD`

并将法术、咒式、军事仪式层与一般排盘/占断 operator 分离。

## 11. 善天道课程家族的 TBV 边界

QM-SRC-0027 主要提供高压缩 role-candidate 索引；QM-SRC-0028 主要提供基础排盘、组合解释与方法冲突；QM-SRC-0029 主要提供高级程序化断局、宫内/宫际关系、角色竞争与修正层。

三册共同强化的不是“某符号固定等于某结果”，而是：

`问题域 -> 候选角色 -> 反馈前冻结 -> 盘面状态 -> 宫内关系 -> 宫际关系 -> 受控修正 -> 应期/输出`

其中年命/日干、拆补/置闰、九星旺衰、马星冲墓/空等都存在选择或竞争空间。它们必须被显式冻结或并行测试，不得结果后任选命中路径。

## 12. Composite-carrier 边界

对 QM-SRC-0024 这类复合载体：

`CARRIER -> SEGMENT -> WORK -> METHOD/VOICE`

是最低必要路径。共同装订、文件名或目录不能建立跨 work 的默认桥接。若以后发现来源自己明确给出桥接规则，应登记为新证据，而不是由项目事先补造。

## 13. 当前认知结果

到当前阶段，更值得工程化保留的不是孤立“吉凶词典”，而是：

`对象定义 + 问题域 + 角色坐标 + symbol instance/layer + 时间模型 + 方法层 + 条件关系 + 程序顺序 + 修正边界 + 现实锚点`

同时，0009 强迫项目再增加一项自我约束：场景模型不能因为字段更多就自称更高级。SCRM 若只是把传统的门星神干自由度换成 actor、constraint、rival、sensitivity 等现代字段，却没有降低实际可选解释路径，则只是换了一套复杂语言。

因此后续比较必须关注 `NET DEGREES OF FREEDOM`：新结构应减少结果后可选路径并改善复现、错误定位、弃权或前瞻表现，否则删除或降级。

这与 SCRM 的 scenario-conditioned relational 路线相容，但“相容”不等于 SCRM 已被验证。

## 14. TBV 自身的失败条件

若后续实际来源复核或前瞻实践发现：

- 当前提炼遗漏关键前提；
- 所谓关系模型只是项目现代化重写；
- context split 实际是不可调和矛盾；
- 来源确实将某规则明确写成无条件规则；
- SCRM/QCIC 增加结构却没有改善复现、校准、错误定位或弃权质量；

则必须修改/降级 TBV 与模型，不能修改来源或事后加例外保护模型。

## 15. 下一阶段

Deep-visual TBV gap 已关闭，下一主线转为：

1. 对 92 个 semantic UNKNOWN textual sources 继续真实 content access / review，禁止按文件名或目录批量清零；
2. 优先视觉核验 QM-SRC-0010 的题名、版权、目录和全文，再决定与 0009 的正式 work lineage；
3. 将已完成 TBV 的 source-local 方法投入低风险实战/前瞻练习，用冻结预测、失败保留、mapping drift 与净自由度审计持续反向校正模型；
4. Claim Extraction 保持 BLOCKED，Empirical Credit 保持 NONE，直到其各自机器门槛真正满足。
