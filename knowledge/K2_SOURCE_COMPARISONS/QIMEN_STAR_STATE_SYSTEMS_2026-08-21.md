# 九星旺相休囚系统对照 — AQ-005 第一轮

Status: `SOURCE_COMPARISON / PARTIAL_AQ005 / NO_EMPIRICAL_CREDIT / NO_RUNTIME_WEIGHT_CHANGE`

Date: 2026-08-21

目标不是找一张“标准旺衰表”，而是检验旧项目是否把来源级状态分类过早压成了统一、可直接加权的运行规则。

本轮只比较两个已经正式完成 K2 Reading 的来源：

- `QM-SRC-0001 / WORK-000217 / 梁湘润《奇门遁甲入门》` — `COMPLETE / VISUAL_PAGE`；
- `QM-SRC-0028 / WORK-000018 / 善天道《奇门遁甲讲义71页》` — `COMPLETE / TEXT_LAYER_FULL`，相关页已有 supplemental original-page visual check。

因此本次比较不新增 Reading credit，只增加 source-comparison 层的认识。

---

## 1. 梁湘润 p18：九星不是简单套“地上五行旺相休囚死”

PDF p18 原页有两组相邻表格。

一组以五行 `木 / 金 / 土 / 火 / 水` 为对象，列 `旺 / 相 / 休 / 囚` 等季节关系；另一组直接以九星为对象，列出：

`旺 / 相 / 废 / 休 / 囚`

并按月份分配状态。

例如天蓬水星一行可见：

- 亥、子月列入 `旺`；
- 寅、卯月列入 `相`；
- 申、酉月列入 `废`；
- 巳、午月列入 `休`；
- 辰、戌、丑、未月列入 `囚`。

关键不是某一行数字，而是结构本身：**九星表使用“废”而不是“死”，且状态映射不是简单把星的五行当作地上五行直接套季节旺衰。**

当前分类：

`SOURCE_DEFINED_STAR_STATE_SYSTEM / WANG_XIANG_FEI_XIU_QIU`

这只证明梁书如何组织九星状态，不证明这些状态具有预测增量。

---

## 2. 善天道 71 页 p8-p9：作者先承认古籍分歧，再明确选一套解释

PDF p8 原页直接指出：九星旺相休囚的古籍说法并不一致，有的按五行旺相休囚理解，有的认为不同。

该讲义随后明确选择《烟波钓叟歌》一系解释，并给出关系规则：

- 九星所生的月令五行为 `旺`；
- 与九星同五行为 `相`；
- 月令生九星为 `废`；
- 九星克月令为 `休`；
- 月令克九星为 `囚`。

p9 再用天蓬水星、天芮土星举例说明这一套状态系统，并明确把地上五行的 `旺 / 相 / 休 / 囚 / 死` 与九星的 `旺 / 相 / 休 / 囚 / 废` 区分开。

当前分类：

`SOURCE_DEFINED_STAR_STATE_SYSTEM / WANG_XIANG_FEI_XIU_QIU`

同时还有一条非常重要的 source-critical Evidence：

`SOURCE_REPORTS_INTERNAL_TRADITION_DISAGREEMENT`

即这本现代讲义自己就告诉读者：这里不是“古籍从来只有一套标准答案”。

---

## 3. 两书目前在结构上高度一致，但不能直接叫“独立双重验证”

梁书 p18 的九星月份表与善天道 p8-p9 所解释的 `旺 / 相 / 废 / 休 / 囚` 关系，在可核对部分高度一致。

如果只追求“多书一致”，很容易立刻写成：

`两本书都这么说 -> 规则得到双重验证`

这是当前项目必须禁止的推理。

原因至少有三层：

1. 两书一致首先只提高 `Source Consensus`；
2. 善天道明确把自己的算法追溯到《烟波钓叟歌》，梁书本身也收录烟波钓叟相关传统材料，两者存在 `POSSIBLE_SHARED_LINEAGE`，未必是统计意义上的独立来源；
3. 即使历史来源完全独立，也仍不能自动提高现实预测的 `Empirical Support`。

因此当前只能记：

`SOURCE_CONVERGENCE / POSSIBLE_SHARED_LINEAGE / EMPIRICAL_SUPPORT_UNCHANGED`

而不是：

`VALIDATED STAR WEIGHTING RULE`。

---

## 4. 这次对旧理论真正造成的修正：状态分类 != 固定效果倍率

旧 `情境推演法 v0.1` 曾经把旺衰状态直接转成运行倍率：

- 旺相 -> 断语“全额生效”；
- 休囚 -> 吉凶“减半”；
- 四害再固定加减。

这一步在当前证据下没有来源依据，也没有 prospective evidence。

梁书和善天道能支持的是：

`某 source 如何分类 star state`

它们**不能支持**：

`旺 = 1.0 倍 / 休囚 = 0.5 倍`

更不能支持：

`某状态跨疾病、求财、天气、市场等所有问题都具有相同数值影响`。

因此旧固定倍率继续保持 `DEPRECATED / NOT_OPERATIONAL`。

这不是“反对古书”，而是把两个不同问题拆开：

`state classification` 与 `predictive effect size`。

---

## 5. “因局制宜”在这里该怎么落地

如果未来在解盘中使用九星旺衰，不能直接写：

`天蓬旺 -> 凶更凶`

或：

`天辅囚 -> 吉减半`

更稳妥的关系链应该是：

`source-specific star-state -> 当前 Method Family 是否允许该变量 -> 当前角色/事项中该星承担什么关系 -> 该状态是否改变可观察预测 -> 与不使用该状态的模型比较`

如果删除 star-state 后冻结预测完全不变，它可能只是解释性装饰。

如果加入 star-state 后只让故事更丰富，却没有改善 discrimination / calibration，就应该压缩甚至删除其 operational influence。

这才是“活法”与“随意解释”的分界。

---

## 6. AQ-005 当前结论

本轮第一组 source comparison 得到：

`SOURCE_CONVERGENCE`

但不是：

`EMPIRICAL_VALIDATION`。

并且进一步暴露：

`STAR_STATE_OBJECT != FIVE-ELEMENT_STATE_OBJECT != EFFECT-SIZE WEIGHT`

这是继：

- Sequence-Object Type Safety；
- Representation-Object Type Safety；
- Semantic-Object Type Safety；

之后的同类对象分离问题。当前先记为方法论观察，不新增顶层 schema。

### KEEP

保留 `star_state_system` 作为反馈前冻结字段，因为不同 source system 仍可能产生不同状态。

### NARROW

把当前可用 claim 缩窄为“来源级分类系统”，不把它当固定吉凶倍率。

### DELETE

继续删除“旺相全效 / 休囚半效”这类数值化旧遗产。

### TEST

未来 clean prospective 中做 matched ablation：

`STAR_STATE_ON` vs `STAR_STATE_OFF`

必须使用同一 setup、Role Map、feature set、auxiliary policy 与评分协议。

若长期不增加 discrimination / calibration，考虑删除该变量的 operational influence。

---

## 7. AQ-005 尚未关闭

AQ-005 原目标还包括八门状态系统。

九星这一轮已经说明：即使两书表面一致，也要继续问 lineage independence 与 effect-size evidence。

下一步不急着再找第三本九星表，而应转向：

- 八门旺相休囚是否也有 source-specific algorithm；
- 是否与九星使用同一“状态对象”；
- 不同来源是否把门的季节状态用于吉凶方向、幅度、应期，还是仅作描述。

在完成两个 method-context 清楚的门状态来源比较前，AQ-005 保持 `PARTIAL / OPEN`。

一句话：

> **两本书写出同一张表，最多先说明一种传统被重复保存；它离“现实中应该给多少权重”还隔着完整的一层验证。**
