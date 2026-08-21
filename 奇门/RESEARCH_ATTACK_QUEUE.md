# 奇门 Research Attack Queue

状态：ACTIVE / LIGHTWEIGHT / NOT_A_SCOREBOARD

日期：2026-08-21

目的：减少 `SELECTION_DOF / STOPPING_DOF`，防止每个 case 都冻结得很严格，却只挑容易支持当前模型的问题、来源和负对照。

这不是新的 Empirical Registry，不增加 Reading/Evidence credit，不按完成率评价学习进度。如果它不能实际减少 cherry-picking，应删除而不是升级成更重的流程。

## 使用规则

1. 在看到目标来源/测试结果之前，先登记“为什么这个对象值得攻击当前模型”。
2. 每条必须写出至少一个会迫使当前观点 `NARROW / REVISE / DELETE / NO-OP` 的结果。
3. `PASS / FAIL / NO-OP / UNRESOLVED` 全部保留，不只记录漂亮结果。
4. 不把同一谱系的重复支持当成独立 cross-source corroboration。
5. 若是 matched prospective/model comparison，开始前冻结样本数、时间窗或停止条件；不能赢了就停、输了就加样本直到好看。
6. Queue 只决定“先攻击哪里”，不替代 Source Review、Prediction Freeze 或 Outcome Audit。

---

## AQ-001 — Cross-source full rotation：主动找反例，不继续只找支持

当前问题：`SHANTI_DAO_71_P21_P22` 已能复现善天道 p21-p22 sparse worked-plate anchors，并在 `QM-SRC-0021` 的一组独立现代 worked plate 上得到 selected cross-source implementation agreement。

攻击目标：找**不同来源、不同实例**的 non-Jiazi full-rotation plate，优先选择可能采用不同中宫寄法、值使移动或八神运动的来源。

会改变当前观点的结果：

- 同一明确 method context 下，星/门/神的结构与当前 profile 系统性冲突 -> `NARROW` source profile，不得解释为“书错了”直接跳过；
- 只有星一致、门或神不一致 -> 把 full-profile 再拆对象，而不是继续整体冠名；
- 来源自身无法确定 method context -> `UNRESOLVED / NO-OP`，不硬算支持或反对。

停止条件：至少得到 2 个新的独立、原页可审的 worked-plate witnesses，或遇到足以证明 method context 不可比的 lineage blocker。之后先复盘，不无限找第三本支持材料。

---

## AQ-002 — 中五值使：专门攻击当前 fail-closed 空白

当前问题：值使时序目标落中五宫时，当前 source profile 返回：

`SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED`

攻击目标：找原页明确给出“值使计时结果落五宫”且完整八门落位可核对的 worked plate / algorithm witness。

会改变当前观点的结果：

- 独立来源给出明确寄宫/门轮处理 -> 建立 source-specific variant，先做 implementation comparison；
- 不同来源给出互相冲突的中宫处理 -> 保持多 profile，不选“最顺眼”者；
- 只有口诀没有 worked plate -> 增加 Source Fidelity，不足以关闭 implementation gap。

停止条件：找到 1 个可完整复核的 source-defined center-target worked plate，或明确证明现有可访问资料只给规则不提供足够 oracle。

---

## AQ-003 — 八神谱系：寻找早期且带运动对象的 witness

当前问题：`勾陈/朱雀` 与 `白虎/玄武` 已存在至少四种竞争解释，Test C 当前 `UNRESOLVED / NO-OP`。

攻击目标：优先早期/独立来源，不优先现代摘要；需要同时观察名称、排列、阴阳遁、天/地神层、运动方向或 worked plate。

会改变当前观点的结果：

- 早期 witness 明确支持其中一种关系且上下文完整 -> 只提高该 lineage hypothesis 的 Source/Lineage confidence，不自动改 runtime 全局 enum；
- 早期 witness 与现代隐藏神说法冲突 -> 保留历史分叉，禁止普遍等号；
- 只有名称列表没有运动上下文 -> `NO-OP` 于 executable mapping。

初始候选：

- 《甲遁真授秘录》：先做结构/关键词导航，但 OCR 命中只当线索；
- 《笺元遁甲句解烟波钓叟歌》：用于更早文本/口诀谱系，不假定其能回答八神运动；
- 其他古籍由实际页级证据再加入。

停止条件：本轮最多深挖 2 个独立早期 witnesses；如果都不能回答运动对象，转向别的问题，不以“再找一本”拖延。

### First probe — 2026-08-21

`QM-SRC-0024 / 《笺元遁甲句解烟波钓叟歌》` 已做 canonical p1-p12 targeted original-page provenance review。

得到的不是“八神谱系答案”，而是一个更窄的 provenance 结果：

- p5 原页可以 `PAGE_VERIFIED` 书名 witness；
- p5 可以 `PAGE_VERIFIED_WITNESS_ATTRIBUTION` 到赵普归因语境；
- 这不能单独证明赵普的历史作者身份；
- `明刊本` 版本判断仍 `EDITION_UNRESOLVED`；
- p1-p12 本轮没有提供足够的八神名称顺序、运动层或 worked-plate context 来解决 AQ-003。

所以 AQ-003 对本次 probe 的结果是：

`PROVENANCE_IMPROVED / DEITY_LINEAGE_NO-OP`

它**不计入**“2 个独立早期 movement witnesses”的停止条件，也不把 targeted p1-p12 review 冒充成 `QM-SRC-0024` 全书 Reading COMPLETE。

`QM-SRC-0022 / 《甲遁真授秘录》上册` 的初步 OCR 关键词命中目前只保留为 navigation clue；快速视觉抽查没有形成足够清楚的 deity-system witness，因此暂不登记支持/反对结论。若继续深挖，必须回原页上下文，而不是把 OCR 词命中升级成 Evidence。

这个 `NO-OP` 被保留下来，是为了检验 Attack Queue 是否真的会记录“没有帮当前理论增加规则”的研究结果。

---

## AQ-004 — 真正的 time-boundary control

当前问题：已有 wrong-hour control，但它不是 `time_boundary_system` 实验。

攻击目标：找发生在 23:00/00:00、子时换日、或节气交接边界附近，且来源给出明确盘例/日期算法的 witness。

会改变当前观点的结果：

- `CIVIL_MIDNIGHT` 与 `ZI_START_23` 产生不同日柱/局盘，而来源能明确支持其中一套 -> 建立 source-specific boundary profile；
- 来源本身混用边界 -> 标 `SOURCE_INCONSISTENCY`，不能拿结果倒推哪套“更准”；
- 没有边界实例 -> 不制造伪 control。

停止条件：没有真实边界 witness 就保持 open；不得为了勾选任务而拿普通白天时刻代替。

---

## AQ-005 — Star/Door state systems：查冲突，不查“标准答案”

当前问题：旧知识库曾把九星/八门旺相休囚写成固定、可直接打折的运行规则；当前已冻结 `star_state_system / door_state_system`，但 lineage/algorithm 仍有债务。

攻击目标：比较至少两个有明确算法上下文的来源，重点找：

- 月令/季节对象；
- 旺相休囚死顺序；
- 门旺衰是否按五行通则或门派表；
- 是否真的进入断局权重，还是只作描述。

会改变当前观点的结果：

- 算法冲突 -> 继续 source-specific，不造统一表；
- 多书相同 -> 只记 Source Consensus，仍不自动恢复固定“全额/减半”权重；
- prospective ablation 显示 state system 不改变 discrimination -> `MERGE / DELETE` operational influence。

停止条件：完成两个 method-context 清楚的来源比较后先做压缩评审，不因表格容易整理就无限扩展。

---

## AQ-006 — 情境转译本身：它到底增加判别力，还是只增加故事？

当前问题：用户要求解盘不能照书背断语，这个方向必须保留；但旧 v0.1 曾写“情境给我答案”，暴露 context leakage 风险。

攻击目标：在真实 clean prospective pilot 到来后比较：

`SOURCE_RESTRICTED / CONTEXT_FROZEN_RELATIONAL / BROAD_CONTEXT / SHUFFLED_ROLE_MAP`

关键不是“哪个解释更像人话”，而是：

- primary outcome discrimination；
- calibration；
- abstention；
- 分析者一致性；
- shuffled role/symbol control 的差距；
- context 增加后是否只是 branch 数量变多。

会改变当前观点的结果：

- context-frozen relational model 不优于 simpler source-restricted baseline -> 缩窄“情境推演”的 operational claim；
- broad context 与 shuffled control 同样能讲通 -> 对宽象意/宽背景加更强 Semantic Expansion Penalty；
- Role Map 无法在反馈前稳定冻结 -> 允许更简单 fixed-role method family 反而胜出。

停止条件：首轮只做 protocol pilot，不用 6 个 case 宣布理论有效；matched comparison 需预先写样本/时间窗，再决定是否扩到下一阶段。

---

## No Grandfathering 检查

任何旧规则进入当前模型，都不能以“以前已经学过/写过/用过”为理由豁免攻击。

当前已明确废弃或降级的历史遗产包括：

- 固定 `开门 > 值符 > 生门 > 星神`；
- `逢空 = 方向待定`；
- 凶格固定计分/相乘；
- 旺相全额、休囚减半；
- `>=3 次 = 已验证`；
- contaminated case 折算半次验证；
- “渐进迭代 = 不推翻旧规则”。

后续若发现其他旧规则只是因为存在得久而继续运行，优先列入 `DELETE / MERGE / ABLATE`，而不是再找书给它补背书。

---

一句话：

> **不只冻结我怎么答，也要看住我挑什么题、找什么证据、什么时候停。**
