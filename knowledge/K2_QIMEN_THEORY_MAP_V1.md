# K2 奇门理论地图 v1.0

状态：`SOURCE_GROUNDED_MAP / CANDIDATE_MODEL / NO_EMPIRICAL_CREDIT`  
Claim Extraction：`BLOCKED`  
用途：把已经完成深读/蒸馏的奇门材料从“按书存放”重组为“理论问题—候选模型—边界—冲突—验证”的研究地图。  
非用途：本文件不是新的奇门教科书，不把多来源共现等同于真理，不授予任何规则现实预测信用。

## 0. 为什么需要理论地图，而不是继续堆规则

当前 K2 已经证明：按书完成阅读、形成 Evidence 和 Distillate，只解决“来源说了什么、怎样说、在哪个上下文说”的问题，并不自动解决“哪套理论更好”。

如果继续沿着：

```text
source -> rule -> rule -> rule -> bigger rule set
```

扩张，系统会重新回到两个旧误区：

1. **静态词典膨胀**：条目越多，结果后越容易找到一个能解释结果的规则；
2. **来源票数幻觉**：同一作品、同一课程变体或互相承袭的说法，被误当成多个独立证据票。

因此 v1.0 改用：

```text
SOURCE / VOICE
      ↓
THEORY PROBLEM
      ↓
CANDIDATE MODEL(S)
      ↓
BOUNDARY / CONFLICT
      ↓
DISCRIMINATING TEST
      ↓
RETAIN / SPLIT / CONSTRAIN / DOWNGRADE / REMOVE
```

本地图只组织**当前已经有 source-grounded distillate 的认识**。没有来源支持的空白保持空白，不用常识补齐。

---

# 1. 理论层级总图

当前奇门知识不应压成一张“符号=意义”表，而至少分成七层：

```text
L0  Provenance / Voice / Carrier
L1  Temporal Setup / Ju Method
L2  Layout / Ontology / Plate State
L3  Question Topology / Role Mapping
L4  Conditional Symbolic Operators
L5  Relational Configuration / State Transition
L6  Auxiliary Information / Cross-Method Inputs
L7  Outcome / Prospective Validation
```

任何规则如果不知道自己属于哪一层，就不允许进入统一解释池。

一个来源在某层可靠，不代表它在其他层也可靠。例如：

- 一个来源可以提供可复现的排盘结构，但其吉凶断语仍然没有现实验证；
- 一个案例可以很好地展示作者怎样取用神，却不能证明该取用神方法现实上优于竞争方案；
- 一个古籍可以完整记录 source-local 八神体系，但不能因此定义所有流派的统一八神 ontology。

---

# 2. L0 — Provenance / Voice / Carrier：先回答“这句话是谁在什么载体里说的”

## 2.1 当前得到的核心结论

### 候选原则 L0-P1

`CARRIER != WORK != VOICE != CLAIM`

来源文件、作品、作者声部、转引传统、现代译释和后期编辑必须分离。

当前 source-grounded 支持：

- `QM-SRC-0001` 的 voice-qualified pilot 已明确区分：传统起源转录、结构正文、方法边界评论；三者不能共享作者信用或操作信用；
- `WF-QM-JIADUN-ZHENSHOU-001` 已显示同一 composite carrier 可包含不同作品 segment；
- work-family distillation 已明确上下册/同作品不同 carrier 只能增加 coverage，不能重复增加 independent vote。

## 2.2 当前边界

这是一条**知识工程/来源治理规则**，不是奇门预测理论。

它可以减少：

- 作者归属污染；
- 版本污染；
- 同源重复计票；
- 译释声部被误当 base text。

它不能直接提高现实预测准确率。

## 2.3 当前状态

`RETAIN_AS_INFRASTRUCTURE`

---

# 3. L1 — Temporal Setup / Ju Method：先把“怎样生成盘”与“怎样解释盘”彻底分开

## 3.1 当前候选模型

目前来源中至少存在或提及：

- 拆补 / 符头；
- 置闰；
- 不拆不闰；
- 灵机/其他起局路径；
- 年家、月家、日家、时家等不同 temporal family。

`QM-SRC-0016` 与 `QM-SRC-0021/0028` 都提示：不同起局/时间模型不能在结果出现后自由切换。

### 候选原则 L1-P1

`SETUP_METHOD must be frozen before outcome access`

它不是“哪一派永远正确”的结论，而是最小可证伪要求。

## 3.2 已发现的具体工程错误

本轮对 `CHAI_BU_FUTOU` 审计发现：旧实现曾把：

- 十日六甲旬首；
- 五日拆补符头；

混成同一个分组。

当前 engine 已将五日符头回溯与十日旬首逻辑拆开，并保留来源盘 regression；但这只获得**结构修复信用**，不是整个 FUTOU 方法的全局真实性证明。

## 3.3 当前 unresolved conflict

`拆补 vs 置闰 vs 不拆不闰` 当前没有足够前瞻数据决定唯一优胜者。

因此禁止形成：

`一套默认法 = 传统真法 = 现实最优法`

这样的推断链。

## 3.4 验证方向

同一未来时点同时生成多个**事前冻结**的 setup models，保持 outcome definition、role map、评分一致；长期比较：

- reconstruction consistency；
- downstream prediction delta；
- method-switch rate；
- failure distribution。

## 3.5 当前状态

`MULTI_MODEL / JU_METHOD_VALIDATION_OPEN`

---

# 4. L2 — Layout / Ontology / Plate State：同名符号不必属于同一个统一模型

## 4.1 当前来源揭示的三个问题

### A. 转盘 / 飞宫不是同一 layout 的不同写法

`QM-SRC-0016` 明确暴露：转盘与飞宫在门神数量、中五处理和移动算法上存在结构差异。

因此：

`layout_method` 必须成为规则上下文，而不能把两套规则混到统一表里后再消除“矛盾”。

### B. source-local ontology 不应静默标准化

`WF-QM-JIADUN-ZHENSHOU-001` 对八神的完整阅读表明，该来源的八神枚举与部分现代常见名单不同；其中“天乙”又和“值符”存在功能联系。

因此必须区分：

```text
ontology member
functional identity
modern normalized label
```

不能看到功能相近就直接改名。

### C. 中宫规则高度依赖对象与模型层

同一来源可以支持“中心=五”的结构事实，却不支持把它无限外推为：

- 中五永远寄坤二；
- 所有门星神都必须经过中宫；
- 所有 layout 共用同一种寄宫规则。

## 4.2 候选原则 L2-P1

`SOURCE_LOCAL_ONTOLOGY + EXPLICIT_CROSS_SOURCE_RELATION`

先保存每个来源自己的 ontology，再显式建立：

- SAME_AS；
- FUNCTIONALLY_RELATED；
- VARIANT_OF；
- CONFLICTS_WITH；
- UNKNOWN_RELATION。

## 4.3 当前状态

`RETAIN_SOURCE_LOCAL / CROSS-SOURCE-NORMALIZATION_BLOCKED`

---

# 5. L3 — Question Topology / Role Mapping：当前最重要的解释分歧之一

## 5.1 两类竞争模型已经真实存在

### Model A — Fixed Global Priority

`QM-SRC-0003《奇门直断》` 倾向提供大量按问题域组织的直断条目，并出现固定信息层优先顺序倾向。

它的优势候选：

- 简洁；
- 可操作；
- 规则容易冻结。

风险：

- 规则库很大时产生结果后检索自由度；
- 固定顺序可能忽略具体问题拓扑。

### Model B — Domain/Scenario-Specific Role Map

`QM-SRC-0021` 与 `QM-SRC-0016` 更强调：不同问题域、不同 asked object 使用不同主要信息层与用神/角色映射。

其候选优势：

- 更贴合具体问题对象；
- 能把“同一符号在不同问题中角色不同”显式化。

风险：

- role mapping 自由度更高；
- 若不在反馈前冻结，会产生“结果后换用神”。

## 5.2 当前项目立场

不能因为 Model B 更符合“场景化推演”的理念，就直接宣布 B 正确。

当前只允许：

`B = stronger candidate for prospective comparison`

而不是：

`B = validated replacement`

## 5.3 现有工程化候选

SCRM 已把 mapping 表达为：

```text
world_variable
 -> candidate_symbolic_role
 -> source/method basis
 -> alternatives
 -> boundary
 -> failure_condition
```

并要求反馈前：选择、并行保留竞争 mapping，或 ABSTAIN。

## 5.4 关键前瞻问题

`Domain-specific frozen role mapping` 是否相对 `fixed global priority`：

- 降低 post-feedback role switch；
- 降低跨解读者漂移；
- 提高 calibration/discrimination；
- 在未知 outcome 下保持优势。

## 5.5 当前状态

`COMPETING_MODELS / UNTESTED`

---

# 6. L4 — Conditional Symbolic Operators：符号不是结论，只能是条件化候选特征

## 6.1 当前已经否定的旧形态

不再接受：

```text
symbol -> fixed real-world verdict
```

例如：

- 吉门出现 = 成；
- 凶门出现 = 败；
- 某星 = 某类现实人物；
- 旺/墓/刑/空中任一标签 = 固定最终吉凶。

`QM-SRC-0016`、`QM-SRC-0021` 都明确支持：旺衰、入墓、击刑、伏吟反吟等需要回到具体问题、角色、落宫和组合条件。

## 6.2 新表示

每个 operator 至少需要：

```text
source_stance
method_layer
layout_method
question_topology
role_frame
preconditions
symbolic_effect
boundary
incompatibility
precedence
failure_condition
```

这对应 QCIC + SCRM 的接口。

## 6.3 数值权重当前全部降级

以下没有校准的全局数值/星级规则，不能获得经验权重：

- “休囚减半”；
- 凶格累计分；
- `⭐⭐⭐`；
- 固定门星神全局优先级。

它们可以作为历史方法候选存在，但必须单项 ablation。

## 6.4 当前状态

`CONDITIONAL_FEATURE_ONLY / NUMERIC_WEIGHTING_DISABLED_UNTIL_CALIBRATED`

---

# 7. L5 — Relational Configuration / Contextual State Transition：当前最值得研究、也最容易叙事过拟合的一层

## 7.1 来源支持到哪里

`WF-QM-JIADUN-ZHENSHOU-001` 的 deep distillation 支持：该 work family 的应用层不是单个符号固定吉凶，而是把对象、盘层、时间模型、五行、伏吟、卦变等放入关系网络后判断。

`QM-SRC-0021/0016` 也都支持组合条件与问题域的重要性。

这给出的是：

`RELATIONAL_METHOD_CREDIT`

不是：

`RELATIONAL_MODEL_EMPIRICALLY_TRUE`

## 7.2 当前两个候选模型

### H-JD-001 / CDAF-H3

`RELATIONAL_CONFIGURATION` 相对冻结的简单 symbolic mapping 是否有增量？

### H-JD-002

`object-specific contextual state transition` 是否比单一“阳顺阴逆”总口诀更稳定重建 movement rules？

两者均为 `UNTESTED`。

## 7.3 最大风险：Narrative Overfit

关系越多、场景越细、解释越完整，越容易产生“无论结果是什么都能讲通”的系统。

因此关系层必须同时满足：

- mapping 反馈前冻结；
- relational path 反馈前冻结；
- 至少一个真正竞争的 H0/H2；
- 给出 discriminating observation；
- 小幅合法输入变化引起结论翻转时降低 confidence 或 ABSTAIN；
- narrative layer 不得回写 prediction。

## 7.4 当前状态

`PROMISING_METHOD_STRUCTURE / EMPIRICAL_CREDIT_NONE`

---

# 8. L6 — Auxiliary Information / Cross-Method Inputs：最容易制造“奇门很准”的污染层

`QM-SRC-0016` 的案例审计已经暴露：

- 社会背景；
- 外应；
- 其他术数；
- 直觉；
- 已知年龄/身份；

都可能在真实推断里起作用。

如果最终只报告“奇门命中”，就会发生贡献归属错误。

## 8.1 候选原则 L6-P1

`AUXILIARY_INFORMATION must be declared and attributed separately`

允许使用，不等于允许混记。

正式研究至少区分：

```text
Qimen only
Reality/context baseline
Qimen + external omen
Qimen + other divination system
Qimen + social prior
```

## 8.2 当前状态

`CONTAMINATION-SENSITIVE / ATTRIBUTION_REQUIRED`

---

# 9. L7 — Outcome / Validation：任何理论只有在这里才可能获得 empirical credit

## 9.1 当前正式链

```text
Hypothesis
  -> Plan
  -> Batch
  -> Freeze
  -> Outcome
  -> Review
```

`SOURCE_DERIVED` 与 `PROJECT_GENERATED` 可以进入同一验证链，但 provenance 不可互相伪装。

## 9.2 当前 CDAF 的局部归因模型

```text
M0 reality-only
M1 context-structured, no Qimen
M2 frozen symbolic mapping
M3 relational Qimen
M4 narrative expression only
```

对应差分：

```text
M1-M0 = 通用问题建模增量
M2-M1 = 奇门符号增量候选
M3-M2 = 关系推演增量候选
M4-M3 = 表达/理解增量
```

任何高层模型变好，都不能替低层组件自动获得信用。

## 9.3 当前天气 pilot 带来的更深修正

weather-v0.1 的 real-calendar audit 显示：`CORE_RAIN_SIGNAL_V01` 是 civil datetime 的确定性变换，并且对节气/局状态高度不均匀。

因此即使未来 `M2 > M1`，也不能直接解释为“盘获得日历之外的新信息”。

当前必须同时比较相邻相位 calendar shams，以回答更窄的问题：

> 精确 plate alignment 是否比复杂度近似、局部时间结构保留的日历负对照更有区分力？

这就是理论地图的一个示范：**实验结果会反过来改变我们允许提出的问题，而不是只给旧理论加分。**

## 9.4 当前状态

`NO_QIMEN_THEORY_HAS_EMPIRICAL_PROMOTION_IN_THIS_MAP`

---

# 10. 当前主要冲突矩阵

## C-01 固定全局信息层 vs 问题域特定优先级

来源：`QM-SRC-0003` vs `QM-SRC-0021 / QM-SRC-0016`

状态：`UNRESOLVED / PROSPECTIVE_COMPARISON_REQUIRED`

不得通过“哪个更现代/更合理”裁决。

## C-02 拆补 vs 置闰 vs 不拆不闰

来源：`QM-SRC-0028 / QM-SRC-0016 / QM-SRC-0021` 等当前已读材料中的方法分歧。

状态：`UNRESOLVED / SETUP-METHOD-FREEZE_REQUIRED`

## C-03 静态 symbol dictionary vs relational configuration

来源：大量直断条目结构 vs `QM-SRC-0021/0016` 与 `WF-QM-JIADUN-ZHENSHOU-001` 的组合关系方法。

状态：`FORMAL HYPOTHESIS EXISTS / UNTESTED`

关联：`H-JD-001 / K2PV-JD-001`

## C-04 统一 movement 口诀 vs object-specific state transition

来源：`WF-QM-JIADUN-ZHENSHOU-001`

状态：`FORMAL HYPOTHESIS EXISTS / UNTESTED`

关联：`H-JD-002 / K2PV-JD-002`

## C-05 统一 ontology vs source-local ontology

来源：古籍 work family 与现代常用术语存在成员/功能关系差异。

状态：`DO_NOT_FORCE-RESOLVE`

当前先保存 explicit cross-source relations。

## C-06 “灵活机动” vs 可证伪性

来源：`QM-SRC-0016` 内部同时存在反机械化主张与灵机、外应、多术数、反馈后修正等高自由度路径。

状态：`KEEP_TENSION_VISIBLE`

不能把“灵活”本身升级为理论优势；必须通过 Freeze/ablation 判断哪些灵活性是真实信息增益，哪些只是事后自由度。

---

# 11. 知识信用不再用单一等级压缩

本地图不采用一个简单的 S/A/B/C 排名，因为那会再次把不同维度压成一个模糊分数。

每个理论组件至少分开记录：

```text
source_fidelity       来源是否真的这样说
structural_repro      结构/算法能否复现
applicability_clarity 适用条件是否清楚
conflict_status       是否存在未解决竞争模型
prospective_status    是否进入反馈前验证链
empirical_credit      是否真正得到前瞻结果支持
```

例如：

- `CHAI_BU_FUTOU` 某个 source fixture 可以有较高 structural reproduction，但 method-wide empirical credit 仍为 NONE；
- 一个古籍关系结构可以有高 source fidelity 与 method credit，但 prediction empirical credit 仍为 NONE；
- 一个自创 CDAF 设计可以有清晰 falsification contract，但因为尚无 Outcome，empirical credit 仍为 NONE。

这是为了阻止“来源很强，所以现实很准”或“工程很完整，所以理论很强”的错误压缩。

---

# 12. 解盘时怎样调用这张地图

理论地图不是让模型多背一层规则，而是减少解释自由度。

正式 reasoning 顺序：

```text
1. Define question/outcome/time horizon
2. Record reality anchors / base-rate / direct checks
3. Freeze setup model + layout context
4. Build world-variable / role candidates
5. Freeze or explicitly parallel competing mappings
6. Admit only context-eligible symbolic operators
7. Build at least one non-Qimen or competing explanation
8. Run relational inference only on frozen nodes/operators
9. Stress-test counterfactual + sensitivity
10. Produce prediction / confidence / abstention
11. Narrative may explain, never rewrite frozen prediction
12. Outcome later updates model credit, not historical record
```

若第 3–7 步无法冻结，优先 `ABSTAIN / CONTEXT_REQUIRED`，而不是扩大象意词典寻找一个答案。

---

# 13. 理论创新的准入条件

一个“新理论”只有满足以下条件才进入项目级 hypothesis registry：

1. 指出当前地图中一个明确未解决问题；
2. 相比现有模型只新增有限、可描述的变量或关系；
3. 给出至少一个竞争模型；
4. 说明什么观察会使它失败；
5. 不需要结果后改用神、改局法、改 role map 或增加新例外才能存活；
6. 可以通过 CDAF 或同等 ablation 知道增量究竟来自哪里；
7. 未验证前必须保持 `empirical_credit=NONE`。

“解释更多”“更符合直觉”“更完整”“融合更多古法”都不能单独构成创新信用。

---

# 14. v1.0 明确不做的事

- 不宣称已经统一奇门各派；
- 不裁定古籍和现代来源谁更真实；
- 不给星门神干建立全局固定现实字典；
- 不从案例命中数量推导准确率；
- 不把 CI 通过、Evidence 数量、阅读页数转成 empirical credit；
- 不把本地图自身当作原创理论验证结果；
- 不为了看起来完整而填补当前资料没有支持的空白。

---

# 15. 当前可执行优先级

本地图完成后，下一阶段不应同时扩所有层，而应按“最靠前的未闭环层会污染后续层”的原则处理：

```text
P0  carrier/source identity for critical fixtures
P1  JuMethod + plate structural validation
P2  competing role-map / priority models
P3  symbolic operator ablation
P4  relational configuration prospective tests
P5  narrative/comprehension layer
```

原因：如果起局、layout 或 role map 本身还会漂移，直接研究高级关系推演只会把底层误差包装成更复杂叙事。

---

# 16. 来源/项目锚点

本 v1.0 直接依赖当前已存在的研究产物：

- `knowledge/K2_BOOK_DISTILLATES_WAVE1.jsonl`
  - `QM-SRC-0028`
  - `QM-SRC-0021`
  - `QM-SRC-0003`
- `knowledge/K2_BOOK_DISTILLATES_WAVE1.d/QM-SRC-0001.jsonl`
- `knowledge/K2_BOOK_DISTILLATES_WAVE1.d/QM-SRC-0016.jsonl`
- `knowledge/K2_WORK_FAMILY_DISTILLATES.jsonl`
  - `WF-QM-JIADUN-ZHENSHOU-001`
  - 以及当前已登记的其他 qimen work-family distillates
- `knowledge/K2_QIMEN_SCRM_V01.md`
- `knowledge/K2_QIMEN_CONTEXTUAL_DIFFERENTIAL_ABLATION_V01.md`
- `knowledge/K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md`
- `knowledge/K2_PROSPECTIVE_VALIDATION_PROTOCOL.md`
- `knowledge/K2_QIMEN_CDAF_H2_*`

注意：本地图是这些材料的**二阶研究索引**，不是 canonical source，也不能替代任何原页复核。
