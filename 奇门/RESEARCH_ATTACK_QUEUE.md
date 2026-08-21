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

当前问题：`勾陈/朱雀` 与 `白虎/玄武` 的现代整理已经出现互不等价的 alias / hidden-layer / yin-yang-substitution 解释。目标不是再找一本书替其中一方背书，而是查更早 witness 是否本来就存在不同结构。

攻击目标：优先早期/独立来源，不优先现代摘要；需要同时观察名称、排列、阴阳遁、天/地神层、运动方向或 worked plate。

会改变当前观点的结果：

- 早期 witness 明确支持其中一种关系且上下文完整 -> 只提高该 lineage hypothesis 的 Source/Lineage confidence，不自动改 runtime 全局 enum；
- 早期 witness 与现代隐藏神说法冲突 -> 保留历史分叉，禁止普遍等号；
- 出现现代四假设之外的结构 -> 扩大 source-lineage model，但不为了整齐强行归并；
- 只有名称列表没有运动上下文 -> `NO-OP` 于 executable mapping。

初始候选：

- 《甲遁真授秘录》：先做结构/关键词导航，但 OCR 命中只当线索；
- 《笺元遁甲句解烟波钓叟歌》：用于更早文本/口诀谱系，不假定其能回答八神运动；
- 其他古籍只有下一轮重新开启 AQ-003 时才考虑，不因本轮出现漂亮结果立刻追加。

停止条件：**本轮最多深挖 2 个独立早期 source probes。完成后无论结果漂亮与否，先停止 source accumulation，整合再说。**

### Probe 1 — QM-SRC-0024 / 《笺元遁甲句解烟波钓叟歌》

已做 canonical p1-p12 targeted original-page provenance review。

结果：

- p5 `PAGE_VERIFIED` 书名 witness；
- p5 `PAGE_VERIFIED_WITNESS_ATTRIBUTION` 到赵普归因语境；
- 赵普历史作者身份不能由该页单独证明；
- `明刊本` 版本判断仍 `EDITION_UNRESOLVED`；
- p1-p12 本轮没有足够的八神名称顺序、运动层或 worked-plate context。

AQ-003 结果：

`PROVENANCE_IMPROVED / DEITY_LINEAGE_NO-OP`。

不冒充全书 Reading COMPLETE，也不为了让 probe “有成果”强行生成八神结论。

### Probe 2 — QM-SRC-0022 / 《甲遁真授秘录》上册 carrier

最初 OCR 对 `朱雀 / 白虎 / 玄武 / 九地 / 九天` 的命中非常嘈杂，因此只作为 navigation clue。继续回原页后，找到了真正处在 Qimen algorithm context 的 witness：

- PDF p21-p22 周边明确出现六甲遁仪、八门、九星、直符、阴阳顺逆飞遁；
- p22 原页写到 `天乙隨六甲加時干，是以名直符`；
- 同一段随后给出八位置序列，原页缩写为：
  `直符 / 蛇 / 陰 / 六合 / 朱 / 白 / 九地 / 九天`；
- 紧接着有 `順逆飛遁 / 陰陽二至分順逆` 的 movement context；
- PDF p37 又把八神中的五吉神明确列为：
  `天乙 / 太陰 / 六合 / 九地 / 九天`。

这不是在已有四种现代解释里“选中一个”。它反而形成一个新的 source-specific witness：

`ZHU_BAI_DUAL_POSITION_WITNESS`

即：在这个原页 Qimen context 中，`朱` 与 `白` 同时占据八位置中的两个不同位置。

因此：

- universal `白虎=勾陈 / 玄武=朱雀` 更不能直接成立；
- universal yin/yang pair substitution 也不能拿来吞并这个 witness；
- 不把 p22 的单字缩写偷偷展开成现代 enum；
- 不因为它看起来“更古”就宣布它更真、更准或更标准。

另一个重要反例在 PDF p44：OCR 同样命中 `白虎` 等词，但原页局部其实进入 `天将阴阳干支所属` / 十二将类语境，并不是 p22 那个 Qimen 八位置对象。

由此得到阅读纪律：

`same token != same method object`

工作名：`Semantic-Object Type Safety`。

详细记录：

`knowledge/K2_VISUAL_REVIEW_SESSIONS/QM-SRC-0022_TARGETED_DEITY_LINEAGE.md`。

### AQ-003 本轮停止

两个预先限定的 early-source probes 已完成：

1. QM-SRC-0024 -> deity lineage `NO-OP`；
2. QM-SRC-0022 -> `ZHU_BAI_DUAL_POSITION_WITNESS`。

**现在停止 AQ-003 本轮继续找第三本古籍。**

原因不是“已经证明了什么”，而是遵守事先的 `STOPPING_DOF` 约束：出现有趣结果后立刻继续搜更多支持材料，同样是一种 favourable stopping / selection bias 的反面形式。

下一轮若重新开启 AQ-003，必须先写新的攻击问题，例如：

- QM-SRC-0022 的 `朱/白` 在同源其他页是否有全称解释？
- 独立早期 witness 是复现 `朱/白` 双位置，还是给出另一套结构？
- movement rule 是否也是同一对象？

本轮不再扩源。

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
