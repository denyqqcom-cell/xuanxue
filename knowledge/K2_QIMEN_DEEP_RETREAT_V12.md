# K2 奇门深度闭关 v1.2：从认知重构到信息顺序纪律

状态：`OPEN`  
模式：`COGNITIVE_RECONSTRUCTION`  
当前原创候选：`SCRM-v0.2`  
框架状态：`CANDIDATE_UNTESTED`  
Claim Extraction：`BLOCKED`  
Empirical Credit：`NONE`

## 0. 阶段定义

深度闭关不是停止吸收资料，而是改变“资料在认知体系中的权力”。

文献继续承担三项基础职责：

1. 告诉我们某一来源实际说了什么；
2. 暴露方法的预设、边界、冲突和自我限制；
3. 提供可重建、可比较、可转化为测试假设的结构。

文献不能自动承担第四项职责：证明现实世界必然如此。

因此本阶段的总路径是：

`全覆盖阅读 -> 理论—边界—验证 -> 场景世界模型 -> 信息顺序冻结 -> 竞争解释 -> 前瞻测试 -> 渐进迭代`

只要 machine-derived UNKNOWN backlog 非零：

`full_corpus_mastery_claim = false`

动态覆盖状态不得抄进叙事成为固定数字：

`DYNAMIC STATE = MACHINE_DERIVED`

认知重构不等于理论已验证。工程严谨、全书读完、结构重建完成，都不能代替 prospective empirical credit。

## 1. 第一轮反审得到的旧误区

v1.1 已经确认并记录：carrier/work/voice 混同、文件数当独立票、source contains 当 source endorses、枚举数量当证据数量、跨 method layer 混用、外应与例外未冻结、复盘洗白失败、复杂度崇拜、重点深读误当全库掌握、CI 严格误当现实有效、QCIC 控制壳误当场景模型等问题。

这些修正仍然保留，不因为进入 v1.2 就删除历史错误。

## 2. v1.2 新发现：场景模型本身也可能事后拟合

SCRM-v0.1 虽然要求 Scenario State Graph、Reality Anchor、Competing Explanations、Counterfactual、Sensitivity 与 Abstention，但它仍留下四个重要自由度。

### 2.1 盘面反向塑造世界模型

如果先看到盘，再决定“现实里真正重要的变量是什么”，Scenario State Graph 本身就可能被盘面诱导。

例如先看到某宫受制，随后才把“审批人”或“资金”补成关键节点，形式上虽然是场景建模，本质仍可能是 symbol-first hindsight search。

所以 v1.2 新增：

`WORLD MODEL BEFORE SYMBOLS`

正式冻结案例中，question definition、known facts、actors、constraints、reality anchor、scenario graph 与主要 state variables 必须先冻结，之后才允许 symbolic mapping 进入。

若结果已知或盘面已经参与了世界模型构造，则 contamination 必须如实记录；这种案例可用于方法学习，不能冒充干净 prospective evaluation。

### 2.2 Comparator 信息不对称

仅仅“有 H0 baseline”仍不够。如果 SCRM 看到了完整现实信息，而 baseline 只得到一句问题摘要，SCRM 的优势可能来自信息量，而不是符号模型。

所以新增：

`COMPARATOR INFORMATION PARITY`

H0 与 SCRM 必须共享同一 reality information cutoff。符号信息必须作为被隔离的增量通道，才能测试“加入奇门信息后到底增加了什么”。

### 2.3 理论版本后选

如果结果出来后可以在 SCRM-v0.1、v0.2、不同 QCIC 版本、不同排盘/四化/用神变体之间选择最合适的版本，就会产生 model-version shopping。

所以新增：

`MODEL VERSION FREEZE`

每个正式案例在结果未知时冻结 SCRM 版本、QCIC 版本、method variants 与 tie-break。新版本只能影响未来案例，不能回写旧案例原分数。

### 2.4 ABSTAIN 也可能成为逃生门

弃权是必要能力，但若模型只在容易的案例预测、困难案例全部弃权，就可能获得看似漂亮的命中率。

所以新增：

`ABSTENTION IS ACCOUNTED`

abstention trigger 必须结果前冻结；所有弃权进入 coverage accounting。评价不能只看“已回答案例准确率”，还要同时看 coverage、selective risk 与弃权质量。

## 3. 理论—边界—验证：从阅读协议升级为推演协议

任何进入候选理论的知识单元必须回答：

### THEORY

- 它描述什么对象？
- 使用什么符号关系？
- 是计算程序、关系规则、经验口诀、案例归纳、历史叙述还是作者评论？

### BOUNDARY

- question domain；
- role frame；
- method layer；
- temporal model；
- school/source context；
- prerequisites；
- exclusions；
- failure/stop condition。

边界被识别，只意味着“知道它声称在哪里适用”，不意味着“已经证明它在那里有效”。

### VALIDATION

信用继续分账：

- Source Credit；
- Structure Credit；
- Method Credit；
- Empirical Credit。

前三者再强，也不能自动变成第四者。

## 4. 全覆盖学习如何与认知重构并行

全覆盖仍然是硬前提，但不再用“读完页数”衡量唯一进度。

必须同时追踪：

- work family coverage；
- source/school coverage；
- era/material-type coverage；
- independent/derivative dependence；
- TEXT_DIRECT 与 VISUAL_REQUIRED 的可达性偏差；
- unresolved conflict coverage；
- historical success-only case bias。

特别注意：可提取文本更容易处理，不能因此让现代排版资料在模型中获得结构性过度代表。视觉资料的不可达性必须作为 coverage limitation，而不是静默消失。

## 5. 场景化推演的新执行顺序

SCRM-v0.2 的正式顺序：

1. 定义 decision objective 与可评分 outcome；
2. 冻结现实 information cutoff；
3. 只用现实信息建立 Scenario State Graph；
4. 建立 reality-only comparator；
5. 冻结 SCRM/QCIC/method version；
6. 才揭示/进入 symbolic mapping；
7. 通过 QCIC 取得 eligible rule operators；
8. 形成至少两个 competing explanations；
9. 做 counterfactual stress test；
10. 做 sensitivity analysis；
11. 执行冻结的 tie-break / abstention policy；
12. 输出 prediction 或 ABSTAIN；
13. 结果出现后只记录 outcome，不改变 original path；
14. batch review 后才讨论下一版理论。

这条链的核心不是“更复杂”，而是减少信息顺序与模型选择上的后验自由度。

## 6. 对原创理论的新要求

原创理论不靠命名取得地位。SCRM-v0.2 只有在以下条件下才有继续存在的理由：

- 相比 QCIC-only baseline，有更高的预注册复现性或更好的校准；
- 相比 reality-only baseline，符号增量在相同信息预算下有可测价值；
- 在保持合理 coverage 的同时，abstention 能降低错误而不是只逃避难题；
- world-first freeze 能减少 mapping churn 与 post-hoc scenario edits；
- 新组件经 ablation 后确有增量价值。

如果没有增量价值，就删除组件、回退版本或缩小理论范围。

## 7. 新增的五类认知风险

v1.2 把以下问题加入永久错误账本：

1. **Symbol-first scenario construction**：盘面先决定现实模型；
2. **Comparator information asymmetry**：baseline 被故意或无意饿信息；
3. **Abstention escape hatch**：只答容易题造成选择性漂亮；
4. **Model-version shopping**：结果后选择理论版本或方法变体；
5. **Dynamic-state narrative drift**：机器状态变化后，旧文档仍拿固定数字当当前事实。

这些风险当前都不能标记为“完全解决”，必须保留 residual risk 与 next test。

## 8. 退出条件

深度闭关不以“写出一套新理论”作为退出条件，而以可失败能力作为退出条件。

### Coverage

- UNKNOWN backlog 清零或全部进入有证据的保留状态；
- 不再有未声明的 selection bias；
- 关键 work family 与冲突体系覆盖可审计。

### Cognitive Audit

- 所有历史 bias 永久保留；
- OPEN/PARTIALLY_CORRECTED 必须有 next test；
- 动态状态全部 machine-derived。

### Scenario

- 正式 FROZEN 案例满足 WORLD MODEL BEFORE SYMBOLS；
- comparator parity 通过；
- model version 通过 freeze；
- abstention 被 coverage accounting。

### Validation

- prospective sampling/stopping/exclusion 预注册；
- H0/H1 使用相同现实信息；
- FAIL、ABSTAIN、UNEVALUABLE 全部保留；
- 未完成 batch review 前 `empirical_credit = NONE`。

### Theory Iteration

- 新组件必须做 ablation；
- 新版本不得回写旧结果；
- 没有增量价值就删，不因传统权威或原创情结保留。

## 9. 当前定位

v1.2 不是宣布已经找到“更准的奇门”。它只是比 v1.1 更进一步发现：

> 不仅规则选择会事后拟合，连场景定义、对照组信息量、理论版本和弃权本身都可能成为隐藏自由度。

因此现在的目标不是让解释听起来更完整，而是让每一步都更难在结果出现后改写。

`范式遵循者 -> 规则审计者 -> 场景建模者 -> 信息顺序控制者 -> 可证伪理论建构者`

这条路径继续保持渐进式迭代；SCRM-v0.2 未来同样可以被数据否决。
