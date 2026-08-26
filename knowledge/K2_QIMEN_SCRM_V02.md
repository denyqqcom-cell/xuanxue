# SCRM v0.2：奇门场景条件关系模型——信息顺序版

英文：Scenario-Conditioned Relational Model  
简称：SCRM  
版本：`v0.2`  
状态：`CANDIDATE_UNTESTED`  
Empirical Credit：`NONE`  
Claim Extraction：`BLOCKED`

## 0. 与 v0.1 的关系

SCRM-v0.2 不是推翻 v0.1，而是针对 v0.1 暴露出的隐藏自由度做增量修正。

v0.1 已建立：Scenario State Graph、Reality Anchor、Symbolic Mapping Hypotheses、Eligible Rule Operators、Competing Explanations、Counterfactual Stress Test、Sensitivity Analysis、Confidence Components 与 Abstention。

v0.2 新增四个核心控制：

- `WORLD MODEL BEFORE SYMBOLS`；
- `COMPARATOR INFORMATION PARITY`；
- `MODEL VERSION FREEZE`；
- `ABSTENTION IS ACCOUNTED`。

总体链条改为：

`REALITY INPUT -> WORLD FREEZE -> REALITY BASELINE -> MODEL FREEZE -> SYMBOLIC REVEAL -> QCIC ELIGIBILITY -> SCRM INFERENCE -> COUNTERFACTUAL/SENSITIVITY -> FROZEN OUTPUT -> OUTCOME`

## 1. Scenario State Graph 仍是核心，但必须先于符号解释

现实问题先建成状态图：

- actor；
- resource；
- process；
- constraint；
- action；
- event；
- observable state variable；
- hidden state；
- outcome definition；
- time horizon。

v0.2 的关键变化是：正式 FROZEN 案例中，这个 world model 必须在 symbolic mapping 之前冻结。

原因很简单：如果盘面已经告诉解释者“哪里有冲突、哪里有阻力”，再回头挑现实变量，场景模型可能只是更高级的事后叙事。

因此：

`WORLD MODEL BEFORE SYMBOLS`

不是说现实世界与盘面完全隔离，而是要求先建立一个不依赖盘面也说得通的现实问题模型，然后再测试符号模型到底新增了什么。

## 2. Information Order Contract

每个正式案例新增 `information_order`。

至少记录：

- `world_model_freeze_status`；
- `symbolic_inputs_hidden_until_world_freeze`；
- `outcome_known_at_freeze`；
- `information_cutoff`；
- `contamination_status`。

### CLEAN prospective case

正式 prospective freeze 需要：

- world model 已冻结；
- symbolic input 在 world freeze 前未用于建模；
- outcome 未知；
- contamination = CLEAN。

### CONTAMINATED retrospective case

如果结果已知、盘面已被看过、或现实节点是看盘后才补出来，必须标记 contamination。

这类案例仍可用于：

- source/method learning；
- hypothesis generation；
- error analysis。

但不能当作干净的 empirical evaluation。

## 3. Reality Anchor

Reality Anchor 保持三层：

1. Direct Evidence；
2. Base-Rate Context；
3. Actionable Reality Checks。

任何能直接查证的现实事实优先于符号推演。

如果一个电话、合同、物流单、公开公告或实际流程状态已经足以回答问题，SCRM 不应该为了输出而覆盖现实证据。

## 4. COMPARATOR INFORMATION PARITY

v0.1 要求 Competing Explanations，但没有把 comparator 的信息预算锁死。

v0.2 要求：

`COMPARATOR INFORMATION PARITY`

即 H0 与 SCRM 共享：

- 相同 known facts；
- 相同 reality anchor；
- 相同 information cutoff；
- 相同 time horizon；
- 相同 outcome definition。

唯一允许隔离的增量是 symbolic channel 及其通过 QCIC 后的规则。

否则不能判断性能差异来自奇门模型，还是来自 SCRM 获得了更多现实信息。

每个案例新增 `comparator_parity`：

- `shared_reality_information = true`；
- `shared_information_cutoff`；
- `symbolic_increment_isolated = true`；
- `freeze_status`。

## 5. Symbolic Mapping Hypotheses

只有 world model 冻结后才允许 mapping 进入。

每条 mapping 仍写成：

`world_variable -> candidate_symbolic_role -> source/method basis -> alternatives -> boundary -> failure_condition`

关键变化：mapping 不得反过来新增现实节点，除非明确记录为 post-freeze hypothesis，并且不得改变原预测分数。

如果多个 mapping 合法且无法事前区分：

- 并行保留；
- 使用冻结 tie-break；或
- ABSTAIN。

不能结果后才决定哪个用神“其实更对”。

## 6. QCIC 接口

QCIC 继续负责控制：

- provenance；
- source stance；
- method layer；
- role/rule eligibility；
- observation channel；
- procedure precedence；
- exception budget；
- hindsight control。

SCRM 不绕过这些 gate。

v0.2 的新职责分工：

`SCRM 先冻结现实世界模型`  
`QCIC 再冻结允许进入的符号/规则通道`

两层都冻结后才进入关系推演。

## 7. Eligible Rule Operators

通过 QCIC 的书本规则仍只是条件算子：

`IF boundary + scenario + method conditions THEN symbolic implication`

任何规则即使来源清楚，也不自动获得 universal status。

Theory—Boundary—Validation 仍分账：

- 来源确实写过；
- 结构可以重建；
- 方法使用可以复述；
- 现实是否有效。

前三项不能替代第四项。

## 8. Competing Explanations

正式案例至少保留：

- `H0`：reality-only comparator；
- `H1`：SCRM + QCIC symbolic model。

必要时加入：

- 不同 method/school variant；
- 不同 role mapping；
- 更简单的 symbolic baseline。

禁止稻草人 comparator。

真正有效的 comparator 必须有合理成功机会，并且使用相同现实信息预算。

## 9. Counterfactual Stress Test

继续要求：

> 如果主解释是错的，什么观察应该出现？

以及：

> 哪个观察真正能区分 H1 与 H0？

每个正式预测至少一个 discriminating counterfactual。

如果 H0、H1 对未来观察给出完全相同的预测，则该案例不能为 symbolic increment 提供辨识信息。

## 10. Sensitivity Analysis

至少检查一种：

- temporal boundary；
- role mapping；
- school/method variant；
- missing context；
- observation channel；
- exception use；
- reality-state uncertainty。

如果小幅合法变化使结论翻转，必须降低 overall confidence 或 ABSTAIN。

## 11. MODEL VERSION FREEZE

v0.2 新增 `model_freeze`：

- `scrm_version`；
- `qcic_version`；
- `method_variants`；
- `freeze_status`。

正式案例在 outcome 未知时冻结这些字段。

结果出现后：

- 可以提出 SCRM-v0.3；
- 可以修改 QCIC；
- 可以发现更好的 method routing；

但这些只进入未来案例。

旧案例必须保留 original model path 与 original score。

这条规则用于阻止 model-version shopping。

## 12. Decision Tie-Break

如果机械算法产生多个合法候选：

`DETERMINISTIC MULTI-OUTPUT != UNIQUE DECISION`

必须在反馈前：

- 声明候选输出；
- 声明 selection rule；
- 冻结 selected output；

或者保持 UNRESOLVED 并 ABSTAIN。

结果后不能挑命中的方向、宫位或解释。

## 13. ABSTENTION IS ACCOUNTED

Abstention 仍是正式能力，但不再是免费能力。

v0.2 将弃权从一个字符串条件升级为 `abstention_policy`：

- `trigger_conditions`；
- `decision_rule`；
- `freeze_status`；
- `coverage_accounting = true`。

因此评估必须同时看：

- answered-case performance；
- total coverage；
- abstention rate；
- selective risk；
- abstention quality。

如果模型通过大量弃权只保留“容易案例”，不能只报告剩余案例命中率。

## 14. Confidence Components

v0.2 暂时继续使用：

- `reality_evidence_strength`；
- `source_support_strength`；
- `model_agreement`；
- `input_sensitivity`；
- `overall_confidence`。

仍然只是 research score，不是已校准概率。

未来要判断是否保留这些分量，必须看 prospective calibration 与 ablation，而不是看术语是否漂亮。

## 15. SCRM-v0.2 候选假设

### SCRM-H6：World-first freeze hypothesis

如果 Scenario State Graph 在 symbolic reveal 前冻结，post-hoc node/mapping churn 应下降。

失败条件：冻结前后修改率没有改善，或模型性能明显下降且无法用减少后验自由度解释。

### SCRM-H7：Comparator parity hypothesis

在 H0/H1 使用相同 reality information cutoff 后，若 symbolic increment 仍有稳定增量，才值得继续研究其附加价值。

失败条件：信息对齐后 SCRM 优势消失。

### SCRM-H8：Version-freeze hypothesis

冻结 SCRM/QCIC/method version 应降低结果后 model switching。

失败条件：正式案例仍频繁需要 outcome 后切换版本才能维持解释。

### SCRM-H9：Abstention-accountability hypothesis

把 ABSTAIN 纳入 coverage/selective-risk 评估后，如果弃权机制有真实价值，应在合理 coverage 下减少错误，而不是单纯缩小样本。

失败条件：性能提升完全由 coverage 大幅下降造成，或弃权不能稳定识别高风险案例。

## 16. Ablation Discipline

v0.2 的每个新增组件都必须允许被删除测试：

- 去掉 world-first freeze；
- 去掉 comparator parity；
- 去掉 version freeze；
- 去掉 abstention accounting。

如果某组件对预注册指标没有增量价值，就不因为“理论完整性”而永久保留。

## 17. 当前结论

SCRM-v0.2 的原创性不在于增加更多门星神规则，而在于把四个通常隐藏在解释过程中的自由度变成可审计对象：

1. 世界模型何时建立；
2. comparator 得到多少信息；
3. 使用哪个理论/方法版本；
4. 弃权是否被计入代价。

它仍然是 `CANDIDATE_UNTESTED`。

真正的下一步不是继续扩写理论，而是用相同信息预算、结果未知、版本冻结的低风险 prospective batch 去证明或否定这些新增结构。
