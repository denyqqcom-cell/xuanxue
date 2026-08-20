# 奇门 QClaw 知识体系索引 v2.1

> **执行前必读**：
>
> 1. `奇门/CURRENT_METHOD_CONSTRAINTS.md`
> 2. `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`
> 3. `qclaw/_AGENT_INSTRUCTIONS.md`
> 4. `qclaw/qimen-overview/SKILL.md`
>
> QClaw 已从“固定八步查表解盘”迁移为“受约束情境推演 + 前瞻冻结登记”。旧技能继续保存文献、象意和历史方法，但不再拥有自动真值地位。

## 一、当前技能角色

| 技能 | 当前定位 |
|---|---|
| `qimen-overview` | 运行入口：Reality Baseline、Method-Layer、起局/八神/时间冻结、竞争解释、Outcome Audit |
| `qimen-basics` | 基础概念与传统结构来源 |
| `qimen-datum` | 问题分类候选，不是最终 taxonomy |
| `qimen-bigpicture` | 伏吟/反吟、日时、内外盘等 SOURCE/CANDIDATE |
| `qimen-yongshen` | Role Map 候选来源；反馈前冻结 |
| `qimen-sihai` | 空亡/入墓/击刑/门迫结构识别，不自动吉凶打折 |
| `qimen-gongpan` | 星门神奇仪宫资料与关系候选 |
| `qimen-shengke` | 宫间关系与主客候选，不跨方法族自动执行 |
| `qimen-yingqi` | 应期方法族；禁止结果后挑应期 |
| `qimen-gexia` | 格局来源库；格名不是自动结论 |
| `qimen-qiju` | 起局候选体系；校准/盘式/时间族必须反馈前冻结 |
| `qimen-cases` | 案例用于理解方法与失败模式，不直接证明准确率 |
| `qimen-yange` | 歌诀/传统文本来源层 |

---

## 二、当前学习/执行顺序

```text
基础结构
→ 问题域
→ Method Layer / Method Family
→ 起局校准 + 盘式 + 时间族 + 八神体系
→ Role Map
→ Structural Lookup
→ Eligible Feature Set
→ 关系推演
→ 竞争解释
→ 应期冻结
→ Frozen Prediction
→ Prospective Registry
→ Outcome Audit
→ Rule Lifecycle
```

学习目标不是把每个技能背熟，而是知道：

- 哪些是某本书的说法；
- 哪些是不同流派共享结构；
- 哪些只是项目推演；
- 哪些只是可重复查表；
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

同时再加一条：

`SOURCE FIDELITY / LOOKUP DETERMINISM != EMPIRICAL SUPPORT`

代码把十八局表复刻得再准确，也不能替代现实前瞻验证。

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

真实解盘必须结合问题域、方法层、方法族、Role Map、关系、适用边界和竞争证据，不能直接从速查表跳到结论。

---

## 五、Method-Layer Gate

当前至少区分：

- `STANDARD_PLATE`
- `TIME_FAMILY_VARIANT`
- `HOUR_OMEN`
- `RITUAL_AUXILIARY`

一个层的 miss 不得由另一个层结果后救援。

同时显式记录：

- `setup_calibration`
- `seasonal_alignment`
- `time_family`
- `layout_method`
- `deity_system`
- `hour_omen_family`
- `ritual_layer`
- `bureau_table_source`

梁书勾陈/朱雀与现代常见白虎/玄武体系暂作平行 `deity_system`，不得静默混合。

---

## 六、内外盘当前校正版

| 盘别 | 内盘 | 外盘 |
|---|---|---|
| 阳遁 | **1、8、3、4** | **9、2、7、6** |
| 阴遁 | **9、2、7、6** | **1、8、3、4** |

历史技能中出现过阳遁内盘 `1、3、4、9` 的错误；当前已修正。

传统“内快外慢”语义仍是待验证候选，不代表固定时间系数。

---

## 七、冲突裁决已废弃旧权威链

旧版：

`徒弟分析 -> 师傅古籍核查 -> 师傅有古籍依据则以师傅为准`

这个规则现已 **DEPRECATED**。

当前冲突处理：

```text
先查是否同一 object / layer / method family / setup / layout / time family / deity system / application context
→ 若不同：CONTEXT_SPLIT_REQUIRED
→ 若相同且冲突：CONFLICT_CANDIDATE
→ 形成可前瞻区分的竞争假设
→ 用结果审计决定 KEEP/NARROW/REVISE/DEPRECATE/REJECT
```

任何 Agent 都没有“身份更高，所以结论天然更真”的权限。

---

## 八、当前验证等级

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

## 九、当前原创方法论

见：

`奇门/理论创新_受约束情境推演法_v0.2-alpha.md`

当前核心不是创造更多吉凶表，而是：

**先压缩结果后的解释自由度，再允许情境推演。**

梁湘潤《奇門遁甲入門》的 57/57 视觉阅读已经完成，并推动了 Method-Layer Gate、setup calibration、deity-system context、source fixture 与 prospective registry。它不是终点，也没有被当成新圣经。

---

## 十、当前工程阶段

`QM-SRC-0001 / WORK-000217` 当前已完成：

- canonical 57/57 `VISUAL_PAGE` review；
- 32 条 REVIEWED Atomic Evidence；
- REVIEWED Book Distillate；
- Method Delta；
- Prospective Test Plan；
- 十八局 p32-p49 source fixture index；
- 作者/题名页内 provenance；
- QClaw v2.1 Method-Layer / Prospective Registry 对齐。

当前尚未完成、也不得虚标完成：

- 十八局 sparse anchors 的 `ANCHORS_VERIFIED`；
- 十八局实现对照的 `IMPLEMENTATION_CHECKED`；
- Test A-G 的真实前瞻实验；
- 任何经验有效性结论。

---

## 十一、Prospective Registry

未知结果的正式测试使用：

- `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`
- `knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

Git 只保存冻结协议元数据与 hashes；详细私人 case packet 留在 Git 外。

结果后换起局、校准、方法层、时间族、八神体系、Role Map、feature、竞争分支、应期或 auxiliary policy，必须新建模型版本/`case_id`，不得覆盖原记录。

污染案例保留，不得为了命中率删除。

---

## 十二、执行底线

- 不因书名权威而盲信；
- 不因案例“很像”就称验证；
- 不因叙事连贯就称预测正确；
- 不因一个失败就造全局补丁；
- 不因一个成功就升级规则；
- 不在反馈后换盘、校准、方法层、用神、八神体系、时间族、格局、应期；
- 不把现实新闻的贡献算回奇门本体；
- 不用 HOUR_OMEN / 仪式材料事后救标准盘；
- 不把 source fixture 通过当成预测有效；
- 不在高风险领域把术数当专业结论。

---

*QClaw Index v2.1 | 2026-08-21 | 与 QM-SRC-0001 Method Delta / Source Fixture Gate / Prospective Case Gate 对齐。*
