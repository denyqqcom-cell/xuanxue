# 奇门场景化推演协议

状态：ACTIVE RESEARCH PROTOCOL / v0.1 / NO EMPIRICAL CREDIT

日期：2026-08-21

目的：专门修正当前解盘“过度书本化”和另一极端“情境越多越能自由发挥”的问题。

本协议不是新的断语词典，不提供固定吉凶。它规定如何把现实问题转成可审计的 Role/Relation model，并要求情境越具体，解释空间越窄。

---

## 1. 两个都要拒绝的极端

### 极端 A：背书式

`惊门 -> 口舌`

`开门 -> 工作/事业`

`天芮 -> 疾病`

然后直接把标签翻成现实结论。

问题：同一个符号跨情境机械复用，忽略实际角色、对象、时间和行动条件。

### 极端 B：自由情境式

`用户给了很多背景 -> 从所有象意里挑最贴合的解释`

问题：context leakage、narrative rescue、结果导向解释。

当前只允许第三条路：

`Context defines the problem space; it does not authorize arbitrary symbol meanings.`

---

## 2. Context Compression Invariant

核心不变量：

> **加入更具体的现实情境后，合法解释空间原则上应缩小，而不是扩大。**

用研究语言表示：

```text
eligible_meanings(context_richer) <= eligible_meanings(context_poorer)
branch_count(context_richer) <= branch_count(context_poorer)
role_map_alternatives(context_richer) <= role_map_alternatives(context_poorer)
```

这不是严格数学定理，而是当前模型的反后见约束。

如果实际发生相反情况，标：

`CONTEXT_EXPANSION_FLAG`

并检查：

- 是否把新的现实事实当成了新象意入口；
- 是否为了适配结果增加了第二/第三解释；
- 是否 Role Map 本来就没冻结；
- 是否 question framing 发生了变化。

---

## 3. 场景输入必须先结构化，而不是直接丢进象意库

一个具体问题至少拆成：

```text
QUESTION_DOMAIN
ACTORS
TARGET
TIME_HORIZON
DECISION_OR_OUTCOME_SPACE
KNOWN_CONSTRAINTS
NEUTRAL_SETUP_FACTS
PREDICTIVE_AUXILIARY_FACTS
```

### QUESTION_DOMAIN

问的是什么类型的问题，不是为了机械决定用神，而是限定可观察结果空间。

### ACTORS

现实中的参与者：本人、对方、团队、公司、竞争者、合同方等。

### TARGET

真正要判断的对象或事件。

### TIME_HORIZON

例如未来三个月、下一周、签约日前。没有时间窗口，就不能结果后随意移动应期。

### DECISION_OR_OUTCOME_SPACE

最好预先有限化：

- A / B / 不行动；
- 成 / 不成；
- 上升 / 横盘 / 下降；
- 在窗口内发生 / 未发生。

若结果空间无法定义，应先 `UNSCORABLE`，不急着解盘。

### KNOWN_CONSTRAINTS

现实中已经确定、会限制行动的条件，例如预算、地点、截止日期、必须满足的制度约束。

它们用于限定可行分支，不直接替奇门预测。

### PREDICTIVE_AUXILIARY_FACTS

已经对结果有明显预测力的现实线索必须单独隔离，走 Baseline Firewall。

---

## 4. Role Map 不是“问题类别查表”

Role Map 至少记录：

```text
role
real_world_referent
qimen_feature_candidate
mapping_basis
alternatives
freeze_status
```

`mapping_basis` 只能明确标为：

- `SOURCE_DEFINED`
- `METHOD_DEFINED`
- `CONTEXT_INFERRED`

不能写“通常如此”作为未追踪依据。

### Role Map 决策顺序

1. 先确定现实角色，不先看盘；
2. 再列可用 source/method mapping；
3. 若有两个合理映射，反馈前保留有限 A/B；
4. 不因为哪一个更贴合盘面就临时选哪一个；
5. 若 mapping freedom 过大，允许退回 `CONTEXT_REQUIRED` 或用更简单 fixed-role family。

---

## 5. 星门神奇仪宫只作为候选特征

每一个被使用的盘面因素必须经过：

```text
FEATURE
-> OBJECT TYPE
-> SOURCE/METHOD BASIS
-> STATE
-> ROLE RELATION
-> CONTEXTUAL PROPOSITION
-> DISCRIMINATING OBSERVATION
```

例如不是：

`惊门 = 争吵`

而是先问：

- 惊门落在谁的角色上？
- 它在这个 method family 中被允许表示哪些 communication / disturbance 类候选？
- 当前还有没有其他同底层结构的重复标签？
- 它与对方角色、门宫关系、时间条件构成什么关系？
- 这条关系若是真的，未来什么观察应该更常出现？
- 什么结果会证明这次解释错？

没有最后两问，就还只是叙事。

---

## 6. 从“象意”到“关系命题”

推荐输出不是断语，而是 `RELATION PROPOSITION`。

模板：

```text
[角色A]
在[结构/状态特征]条件下
相对[角色B/目标]
表现出[方向关系]
因此提高/降低[有限结果分支]的相对支持
前提是[现实约束]
若出现[反证观察]则此解释失败
```

方向关系可以是：

- support / constrain
- approach / separate
- expose / conceal
- accelerate / delay
- compete / cooperate
- stable / volatile
- available / blocked

这些也是项目推断语言，不是古籍原词，不得伪装成 SOURCE。

---

## 7. 个性化适配到底适配什么

允许个性化的是：

- 现实角色；
- 目标；
- 时间窗口；
- 可行动选项；
- 现实约束；
- Role Map 的 context basis；
- 哪些 source meanings 与当前对象相关；
- 结果评分口径。

不允许个性化的是：

- 结果后换起局法；
- 结果后换日界；
- 结果后换八神体系；
- 结果后扩大象意；
- 因用户背景“很像某解释”就提升其证据等级；
- 因用户希望某结果而调权重。

一句话：

> **适配现实问题，不适配期待答案。**

---

## 8. 书本规则进入场景的三步翻译

### Step A — Source Statement

只写来源实际说什么。

### Step B — Applicability Filter

问：

- 同一 method family 吗？
- 同一 time family 吗？
- 同一 object 吗？
- 同一 question class 吗？
- 是否有 source-specific prerequisite？

不满足时不要硬搬。

### Step C — Contextual Proposition

只有通过 A/B 后，才能形成项目侧关系命题。

必须标 `INFERENCE`，不能把现代场景翻译倒写成“古书本意”。

---

## 9. Branch 控制

允许多个分支，但必须有限。

每个 branch：

```text
branch_id
prerequisites
supporting_relations
primary_or_secondary
observable_outcome
failure_condition
```

禁止：

- 正面一个分支、反面一个分支、再加“先坏后好”第三分支，最后无论什么都算命中；
- 结果出来以后才把 secondary branch 升 primary；
- 用“玄学多义性”解释 branch 不可区分。

若分支不可区分，合并或 `UNSCORABLE`。

---

## 10. Context 与 auxiliary facts 必须做消融

当现实信息本身很强时，至少概念上拆成：

`M0 = baseline only`

`M1 = qimen method-only`

`M2 = qimen + frozen neutral context`

`M3 = qimen + predictive auxiliary context`

研究时问的是：

- M1 比 M0 增加什么？
- M2 是否只是让表达更具体，还是增加 discrimination？
- M3 的收益来自奇门还是 auxiliary information？

不得把 M3 的漂亮结果倒算成 M1 的能力。

---

## 11. 当前最关键的 A/B 研究

未来 clean prospective pilot 优先比较：

### Model S — SOURCE_RESTRICTED

只用窄 source-bound meanings + fixed/frozen Role Map。

### Model C — CONTEXT_FROZEN_RELATIONAL

加入本协议的 actors/target/horizon/action-space/constraints 和关系推演，但不扩大 source meaning set。

### Model B — BROAD_CONTEXT

允许宽象意与更多现实背景，用于测 narrative rescue capacity，不默认是更强模型。

### Negative Controls

- `SHUFFLED_ROLE_MAP`
- `SHUFFLED_SYMBOL`
- `WRONG_BUREAU / WRONG_TIME`（若 implementation object 适用）

主要比较：

- discrimination；
- calibration；
- abstention；
- branch count；
- eligible meaning count；
- analyst agreement；
- baseline delta。

如果 Model C 不优于更简单的 Model S，本协议应缩窄，不得因为“更像真人解盘”保留复杂度。

---

## 12. 解盘输出顺序

正式场景化输出建议固定为：

1. **事体定义**：我理解你在问什么；
2. **现实约束**：哪些是已知事实，哪些可能污染预测；
3. **方法冻结**：当前盘用什么 method/setup/time/deity/state；
4. **Role Map**：谁对应什么，依据是什么；
5. **结构事实**：盘上实际出现什么；
6. **关系推演**：因素如何在当前情境中相互作用；
7. **主分支**：当前最支持哪一个有限结果；
8. **反分支**：什么条件会改变判断；
9. **时间/行动边界**：仅在有合法依据时给；
10. **置信与不知道**：什么地方 unresolved；
11. **现实建议**：必须区分“由盘产生”与“一般风险管理建议”。

这样避免把十几个书本标签堆成“专业感”。

---

## 13. 何时必须停止解盘

出现以下任一情况，应优先 abstain/追问，而不是继续套书：

- 问题对象不清；
- 结果窗口不清；
- Role Map 有多个不可区分候选；
- method/setup/time boundary 会改变盘但未冻结；
- 使用的 source rule object 不明确；
- context facts 已经直接泄露结果，无法做 method-only attribution；
- 为了继续解释必须不断增加新的象意或分支。

“能说很多”不是继续的理由。

---

## 14. 本协议的失败条件

若未来 matched prospective tests 发现：

- Context Relational model 不比 Source Restricted baseline 更可复现；
- branch count 没减少；
- shuffled role map 仍同样能解释/预测；
- calibration 没改善；
- context 只提高叙事满意度而不提高 discrimination；

则应：

`NARROW / MERGE / DELETE`

而不是继续添加 context schema。

本协议没有“因为更符合活断理念”就必须存在的特权。
