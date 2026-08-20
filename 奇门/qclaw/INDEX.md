# 奇门 QClaw 知识体系索引 v2.0

> **执行前必读**：
>
> 1. `奇门/CURRENT_METHOD_CONSTRAINTS.md`
> 2. `qclaw/_AGENT_INSTRUCTIONS.md`
> 3. `qclaw/qimen-overview/SKILL.md`
>
> QClaw 已从“固定八步查表解盘”迁移为“受约束情境推演”。旧技能继续保存文献、象意和历史方法，但不再拥有自动真值地位。

## 一、当前技能角色

| 技能 | 当前定位 |
|---|---|
| `qimen-overview` | 运行入口：Reality Baseline、方法族、冻结、竞争解释、Outcome Audit |
| `qimen-basics` | 基础概念与传统结构来源 |
| `qimen-datum` | 问题分类候选，不是最终 taxonomy |
| `qimen-bigpicture` | 伏吟/反吟、日时、内外盘等 SOURCE/CANDIDATE |
| `qimen-yongshen` | Role Map 候选来源；反馈前冻结 |
| `qimen-sihai` | 空亡/入墓/击刑/门迫结构识别，不自动吉凶打折 |
| `qimen-gongpan` | 星门神奇仪宫资料与关系候选 |
| `qimen-shengke` | 宫间关系与主客候选，不跨方法族自动执行 |
| `qimen-yingqi` | 应期方法族；已修正内外盘事实错误，禁止结果后挑应期 |
| `qimen-gexia` | 格局来源库；格名不是自动结论 |
| `qimen-qiju` | 起局候选体系；起局/盘式必须反馈前冻结 |
| `qimen-cases` | 案例用于理解方法与失败模式，不直接证明准确率 |
| `qimen-yange` | 歌诀/传统文本来源层 |

---

## 二、当前学习顺序

```text
基础结构
→ 起局与盘式差异
→ 问题/方法族
→ Role Map
→ Eligible Feature Set
→ 关系推演
→ 竞争解释
→ 应期冻结
→ 前瞻预测
→ Outcome Audit
```

学习目标不是把每个技能背熟，而是知道：

- 哪些是某本书的说法；
- 哪些是不同流派共享结构；
- 哪些只是项目推演；
- 哪些真正有前瞻经验支持；
- 哪些规则应该被删掉。

---

## 三、文献引用的正确含义

引用次数、古籍年代、作者名气都不等于现实有效性。

多个来源同意一条规则时，只能先说：

`SOURCE CONSENSUS ↑`

不能直接写：

`EMPIRICAL SUPPORT ↑`

后者需要独立、结果未知、反馈前冻结的验证。

---

## 四、旧“速查表”的降级

旧版索引曾直接写：

- 求财=生门；
- 健康=天芮/死门；
- 官讼=惊门/庚；
- 空亡=事情不实；
- 入墓=停滞；
- 击刑=大凶；
- 门迫=吉门不吉、凶门更凶；
- 青龙回首=大吉等。

这些现在统一改读为：

**“某些传统体系常用的 Role / Feature / Pattern 候选”**。

真实解盘必须结合问题域、方法族、Role Map、关系、适用边界和竞争证据，不能直接从速查表跳到结论。

---

## 五、内外盘当前校正版

| 盘别 | 内盘 | 外盘 |
|---|---|---|
| 阳遁 | **1、8、3、4** | **9、2、7、6** |
| 阴遁 | **9、2、7、6** | **1、8、3、4** |

历史技能中出现过阳遁内盘 `1、3、4、9` 的错误；`qimen-overview` 与 `qimen-yingqi` 已在 2026-08-21 修正。

传统“内快外慢”语义仍是待验证候选，不代表固定时间系数。

---

## 六、冲突裁决已废弃旧权威链

旧版：

`徒弟分析 -> 师傅古籍核查 -> 师傅有古籍依据则以师傅为准`

这个规则现已**DEPRECATED**。

原因：古籍只能证明“古籍这样写”，不能因为是古籍就自动推翻另一个方法或现实结果。

当前冲突处理：

```text
先查是否同一 object / layer / method family / setup / layout / time family / application context
→ 若不同：CONTEXT_SPLIT_REQUIRED
→ 若相同且冲突：CONFLICT_CANDIDATE
→ 形成可前瞻区分的竞争假设
→ 用结果审计决定 KEEP/NARROW/REVISE/DEPRECATE/REJECT
```

任何 Agent 都没有“身份更高，所以结论天然更真”的权限。

---

## 七、当前验证等级

统一生命周期：

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

可逆：

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`

`>=3` 独立前瞻案例只是一项进入 PROVISIONAL 的最低信号，不再称“已验证门槛”。

同时检查：

- 是否预注册；
- 是否独立；
- 基础概率；
- 失败样本；
- 选择偏差；
- 新闻/背景污染；
- 负对照；
- 适用域外表现。

---

## 八、当前原创方法论

见：

`奇门/理论创新_受约束情境推演法_v0.2-alpha.md`

核心不是创造更多吉凶表，而是：

**先限制解释自由度，再允许情境推演。**

这套理论整体仍是未验证 alpha。梁湘润及后续文献的任务之一，就是主动攻击它，而不是寻找赞同它的句子。

---

## 九、当前单书学习目标

下一本：

`QM-SRC-0001 / WORK-000217 / 梁湘润《奇门遁甲入门》`

该源为 `SCAN / VISUAL_REQUIRED`，必须 57/57 原页视觉阅读。

阅读前已完成 Pre-Book Retrospective；阅读时重点关注：

- 信息层选择机制；
- 用神自由度；
- 起局/盘式/时间体系；
- 旺衰空墓刑迫的结构角色；
- 是否存在降低后见自由度的约束；
- 是否有反例迫使当前理论缩窄或废弃。

---

## 十、执行底线

- 不因书名权威而盲信；
- 不因案例“很像”就称验证；
- 不因叙事连贯就称预测正确；
- 不因一个失败就造全局补丁；
- 不因一个成功就升级规则；
- 不在反馈后换盘、换用神、换格局、换应期；
- 不把现实新闻的贡献算回奇门本体；
- 不在高风险领域把术数当专业结论。

---

*QClaw Index v2.0 | 2026-08-21 | 与 K2 Evidence / Pre-Book Retrospective / CURRENT_METHOD_CONSTRAINTS 对齐。*
