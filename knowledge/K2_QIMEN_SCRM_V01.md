# SCRM v0.1：奇门场景条件关系模型

英文：Scenario-Conditioned Relational Model  
简称：SCRM  
状态：`CANDIDATE_UNTESTED`  
Empirical Credit：`NONE`  
Claim Extraction：`BLOCKED`

## 0. 为什么建立 SCRM

QCIC v0.6 已经能显著约束来源、角色、规则、外应、程序顺序、例外与事后找补，但它的核心仍然是一套 **推演控制协议**。

控制协议解决的是：

> 哪些解释不应该被允许。

它没有完全解决：

> 面对一个具体而非标准化的现实场景，应该怎样组织事实、未知量、参与者、约束、行动与多种解释，再决定奇门材料到底能贡献什么。

SCRM 因此不是替代 QCIC，而是补上“场景模型”这一层。

总体架构：

`REAL WORLD -> SCRM SCENARIO CORE -> QCIC CONTROL/ELIGIBILITY -> FROZEN INTERPRETATION -> PROSPECTIVE VALIDATION`

实际执行时 QCIC 与 SCRM 互相约束：SCRM 不能绕过 QCIC 的来源与反馈冻结；QCIC 也不能把“合规地用了很多规则”误当成已经理解具体场景。

## 1. 核心认识论

### 1.1 盘不是现实本身

盘面只是一组符号与关系结构。

真实世界还包含：

- actor；
- resource；
- institution；
- incentive；
- observable fact；
- hidden state；
- time window；
- constraint；
- action；
- feedback；
- outcome definition。

所以：

`plate structure != world state`

必须通过显式 mapping hypothesis 才能把二者联系起来。

### 1.2 映射是候选解释，不是事实

例如某个门、星、神、干或宫位被映射为“对方意愿”“资金”“程序阻力”，在 SCRM 中首先是：

`symbolic_mapping_hypothesis`

它必须说明：

- 为什么这样映射；
- 来自哪个 source/method tradition；
- 适用什么 question topology；
- 有什么竞争映射；
- 哪些事实会使该映射失效。

### 1.3 理论必须对场景做信息压缩

一个好的场景模型不是解释更多，而是用较少、事前确定的状态变量解释更多可观察差异。

如果每个新案例都需要增加新的象意、例外、外应和特殊口诀，则模型没有真正压缩信息，只是在扩大解释词典。

## 2. Scenario State Graph

每个正式案例先建立状态图，而不是先看吉凶词典。

### 2.1 Nodes

节点至少可以包括：

- `ACTOR`：主体、客体、第三方；
- `RESOURCE`：资金、权限、信息、时间、物资；
- `PROCESS`：审批、谈判、寻找、治疗流程、交易流程；
- `EVENT`：可观察未来事件；
- `CONSTRAINT`：制度、物理、时间、法律、现实条件；
- `ACTION`：当事人可以执行的动作。

### 2.2 Relations

关系不是单纯“五行生克”的替代品，而是先保存现实关系，再决定盘面关系是否能提供额外假设。

例如：

- controls；
- depends_on；
- competes_with；
- enables；
- blocks；
- transfers_to；
- delays；
- observes；
- acts_on。

### 2.3 State Variables

每个问题必须把真正决定结果的状态变量列出来。

例如“合作能否签成”不能只写一个 `success/fail`，可能至少包含：

- 对方意愿；
- 我方资源；
- 决策权限；
- 第三方竞争；
- 合同条件差距；
- 截止时间；
- 审批进度。

如果这些变量完全未知，模型必须承认自己不是在解释一个充分定义的场景。

## 3. Reality Anchor

SCRM 在任何符号层之前建立三类现实锚点。

### 3.1 Direct Evidence

当前已经可以核实的事实。

例如聊天记录、物流状态、公开公告、实际库存、合同条款、考试日期、航班状态等。

这些事实优先于术数解释。

### 3.2 Base-Rate Context

如果有可用的普通现实基准，就登记。

例如某种流程通常需要多久、某类审批的一般失败原因、已知市场波动范围等。

这里的 base rate 不一定总能获得，但不能因为没有数据就假装奇门自然拥有更高先验权重。

### 3.3 Actionable Reality Checks

列出不需要预测、直接就能缩小不确定性的动作。

如果一个电话、查件、体检、查合同、问主管就能回答关键问题，应优先做现实核验。

## 4. Question Decomposition

同一句自然语言问题可能混合多个子问题。

SCRM 先拆：

`decision objective -> observable outcome -> state variables -> time horizon`

例如“他还会不会找我”至少要区别：

- 是否主动联系；
- 是否恢复关系；
- 联系发生在什么时间窗；
- 当事人是否采取主动行动；
- 什么行为算“联系”。

若 outcome definition 不清，后续任何“命中”都可能依赖事后重定义。

## 5. Symbolic Mapping Hypotheses

在 Scenario Graph 完成后，才允许奇门角色映射进入。

每条映射至少记录：

`world_variable -> candidate_symbolic_role -> source/method basis -> alternatives -> boundary -> failure_condition`

同一个现实变量可以存在多个合法候选映射。

但正式预测前必须：

- 选择一个；或
- 明确并行保留 competing mappings；或
- 因无法区分而 ABSTAIN。

不能结果后才决定“其实这个才是用神”。

## 6. Eligible Rule Operators

SCRM 不把古籍规则视为直接事实，而把通过 QCIC Gate 的规则看成条件算子：

`IF scenario/mapping conditions THEN symbolic relational implication`

每条 operator 必须有：

- source stance；
- method layer；
- role frame；
- preconditions；
- effect；
- boundary；
- incompatibility；
- precedence；
- failure condition。

规则只在前置条件满足时进入，不因为“它很著名”或“书里有一条像当前结果”就调用。

## 7. Competing Explanations

SCRM 强制至少保留两个有真实竞争力的解释。

最低配置通常是：

- `H1`: 当前奇门关系模型；
- `H0`: 不依赖奇门的现实/统计/直接过程 baseline。

若存在多个奇门流派或 role mapping，也可以加入 H2/H3。

禁止把 comparator 设计成明显不可能成功的稻草人。

每个 explanation 都必须说明：

- 它预测什么；
- 它解释哪些已知事实；
- 它无法解释什么；
- 未来哪种观察更支持它；
- 哪种观察使它失败。

## 8. Relational Inference

在映射和规则冻结以后，才进入盘面关系推演。

### Micro

分析某个节点内部或直接邻接关系：

- 门、星、神、奇仪；
- 旺衰；
- 空亡、入墓、击刑等；
- source-local combinations。

### Macro

分析不同 scenario nodes 对应角色之间：

- 生克；
- 主客；
- 动静；
- temporal transition；
- enable/block/transfer 等现实关系假设。

关键区别：

盘面关系最后必须回到 Scenario Graph 中一个明确 state variable，而不是停在“吉”“凶”“有阻力”这种无法评分的抽象话术。

## 9. Counterfactual Stress Test

任何主解释都必须回答：

> 如果相反解释是真的，盘面与现实里应该看到什么？

以及：

> 当前有哪些观察真正区分 H1 与 H0，而不是两个模型都能解释？

每次至少登记一个 counterfactual check：

`assumption_changed -> expected_effect -> discriminating_observation`

若无法提出任何会推翻主解释的观察，则当前解释不可证伪，应降级为 narrative-only 或 ABSTAIN。

## 10. Sensitivity Analysis

机械套书的一个典型问题是：换一个时间边界、换一个角色映射、换一个学校规则，结论可能完全翻转，却不报告这种脆弱性。

SCRM 强制检查至少一类敏感性：

- temporal boundary sensitivity；
- role mapping sensitivity；
- school/model sensitivity；
- missing-context sensitivity；
- exception/correction sensitivity；
- observation-channel sensitivity。

若小幅合法变动就使结论翻转：

`input_sensitivity = high`

则 overall confidence 必须下降，必要时 ABSTAIN。

## 11. Confidence Components

SCRM 不允许直接把“感觉很明显”转换成高置信。

v0.1 暂用五个研究性分量：

- `reality_evidence_strength`；
- `source_support_strength`；
- `model_agreement`；
- `input_sensitivity`；
- `overall_confidence`。

所有值当前只是 0-1 normalized research score，不具有已校准概率意义。

特别是：

`source_support_strength` 高，只能说明来源支持集中，不等于现实命中概率高。

在 prospective calibration 建立以前，不得把 `0.8` 解释成“80% 会发生”。

## 12. Abstention 是正式输出

SCRM 把“不知道”设计成模型能力的一部分。

以下情况应考虑 ABSTAIN：

- 问题或 outcome 无法定义；
- 关键角色无法反馈前冻结；
- competing mappings 无法区分；
- 现实证据已经足够，不需要符号推演；
- 合法模型之间结论冲突且无选择依据；
- sensitivity 太高；
- 需要未注册外应才能形成结论；
- 必须不断增加特殊例外才能维持解释。

模型如果从不弃权，反而可能说明它拥有过多解释自由度。

## 13. 与 QCIC 的接口

### QCIC -> SCRM

QCIC 提供：

- effective source identity；
- source stance；
- method layer；
- observation cutoff；
- role candidate restrictions；
- eligible rules；
- precedence；
- exception budget。

### SCRM -> QCIC

SCRM 提供：

- question topology 的现实展开；
- scenario nodes/relations；
- world-to-symbol mapping hypotheses；
- competing explanations；
- counterfactual；
- sensitivity；
- confidence decomposition。

任何 SCRM mapping 仍必须服从 QCIC 的冻结与来源边界。

## 14. 一个抽象低风险示例

问题：某个合作项目能否在两周内正式签约。

旧式模板可能直接寻找：

`日干 / 时干 / 开门 / 六合 / 生克 -> 成或不成`

SCRM 先建现实状态：

- Actor A：我方；
- Actor B：合作方；
- Actor C：审批人；
- State 1：双方商业意愿；
- State 2：条款差距；
- State 3：审批权限；
- State 4：两周期限；
- State 5：竞争方案；
- Outcome：在 T+14 日前双方完成具有明确效力的签署。

再登记现实证据：已经谈到哪一步、是否已有草案、谁有最终签字权。

之后才建立奇门 mapping hypotheses，并同时保留：

- H1：SCRM/QCIC 奇门模型；
- H0：仅根据现实流程状态的 baseline。

如果现实资料已经显示合同正在双方盖章流程，奇门不能为了制造神秘感覆盖这一事实。

如果关键审批人身份完全不清，而不同 role mapping 给出相反结论，则应降低 confidence 或 ABSTAIN，而不是结果出来以后再选命中的用神。

## 15. v0.1 候选假设

### SCRM-H1 场景图优先

先建 Scenario State Graph，再做角色映射，应比直接从盘面选用神降低“回答错问题”的比例。

状态：`UNTESTED`

### SCRM-H2 竞争解释

强制保留合理 non-symbolic baseline，应降低单一叙事 confirmation bias。

状态：`UNTESTED`

### SCRM-H3 反事实压力

要求每个主解释提供可区分的反事实观察，应降低不可证伪叙事比例。

状态：`UNTESTED`

### SCRM-H4 敏感性披露

预先测试合法 role/time/model perturbation，应提高对脆弱结论的识别并改善弃权质量。

状态：`UNTESTED`

### SCRM-H5 置信拆分

把现实证据、来源支持、模型一致与输入敏感性分开记录，应比单一主观置信更利于后续校准。

状态：`UNTESTED`

## 16. 失败条件

SCRM 必须允许被淘汰。

如果预注册比较显示：

- 相比 QCIC-only baseline 没有改善复现性；
- 相比简单现实 baseline 没有增量预测/解释价值；
- scenario graph 只增加文档复杂度；
- counterfactual 不能真正区分模型；
- sensitivity analysis 不能预测错误或弃权需要；
- confidence components 无法校准；
- 仍需大量结果后重映射才能表现良好；

则应删除、降级或拆分 SCRM，而不是继续给它增加层级来保护它。

## 17. 当前定位

SCRM 的创新点不在于创造新的门星神含义，而在于改变推演的基本单位：

旧单位：

`symbol/rule -> judgment`

候选新单位：

`scenario state -> mapping hypothesis -> relational operator -> competing explanation -> falsification test`

这只是项目当前的原创性候选方向。

是否真的更有解释力，必须由未来的前瞻、可失败比较决定。
