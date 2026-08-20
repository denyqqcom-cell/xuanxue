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
| `qimen-gongpan` | Component / Relation Registry：结构、象意、状态、Role、关系分层；八神/旺衰系统需冻结 |
| `qimen-shengke` | 宫间关系与主客候选，不跨方法族自动执行 |
| `qimen-yingqi` | 应期方法族；禁止结果后挑应期 |
| `qimen-gexia` | Pattern Registry：结构/来源/适用域/经验支持分离；格名不是自动结论 |
| `qimen-qiju` | 起局候选体系；仍有 P2 migration debt |
| `qimen-cases` | 案例用于理解方法与失败模式，不直接证明准确率 |
| `qimen-yange` | 歌诀/传统文本来源层 |

---

## 二、当前学习/执行顺序

```text
基础结构
→ 问题域
→ Method Layer / Method Family
→ 起局校准 + 盘式 + 时间族 + 八神体系
→ State-System Freeze（若使用九星/八门旺衰）
→ Role Map
→ Structural Lookup
→ Eligible Feature Set
→ Component / Relation Analysis
→ Pattern Registry
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
- 哪些算法本身存在版本/来源冲突；
- 哪些真正有前瞻经验支持；
- 哪些规则应该被删掉。

---

## 三、文献引用、查表与经验支持必须分开

```text
SOURCE CONSENSUS != EMPIRICAL SUPPORT
SOURCE FIDELITY != LOOKUP DETERMINISM != EMPIRICAL SUPPORT
```

引用次数、作者名气、古籍年代、程序复刻成功都不能替代未知结果的前瞻验证。

---

## 四、旧“速查表”的降级

旧版直接写过：求财=生门、击刑=大凶、青龙回首=大吉、吉星+吉门+吉神=大吉等。

当前统一改读为：

**“某些传统体系中的 Role / Feature / Pattern / Symbolism 候选”。**

`qimen-gexia` 进一步拆成：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

`qimen-gongpan` 进一步拆成：

`STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`

同一底层结构不得因为挂了多个格名或多个象意标签就重复计票。

---

## 五、Method / Deity / State-System Gates

当前至少冻结：

- `method_layer`
- `setup_calibration`
- `seasonal_alignment`
- `time_family`
- `layout_method`
- `deity_system`
- `star_state_system`
- `door_state_system`
- `hour_omen_family`
- `ritual_layer`
- `bureau_table_source`

一个方法层的 miss 不得由另一个层结果后救援。

梁书勾陈/朱雀与现代常见白虎/玄武体系作平行 `deity_system`，不得静默混合。

旧 gongpan 对天蓬旺相状态在同一文件中出现互相矛盾的两套示例，因此 `star_state_system` 也必须像起局法一样事前冻结；不能结果后选择更贴合的一套。

---

## 六、内外盘当前校正版

| 盘别 | 内盘 | 外盘 |
|---|---|---|
| 阳遁 | **1、8、3、4** | **9、2、7、6** |
| 阴遁 | **9、2、7、6** | **1、8、3、4** |

传统“内快外慢”仍只是候选语义，不是固定时间系数。

---

## 七、冲突裁决

```text
先查 object / layer / method family / setup / layout / time family / deity system / state system / application context
→ 不同：CONTEXT_SPLIT_REQUIRED
→ 相同且冲突：CONFLICT_CANDIDATE
→ 建立反馈前可区分的竞争假设
→ Outcome Audit 决定 KEEP / NARROW / REVISE / DEPRECATE / REJECT
```

任何 Agent、作者或古籍都没有身份上的天然真值权限。

已保留的真实 legacy 冲突包括：

- gexia：朱雀投江两套干对；小格两套干对；
- gongpan：天蓬旺相状态两套相反示例；
- deity system：勾陈/朱雀 vs 白虎/玄武。

---

## 八、当前验证等级

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

可逆：

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`

`>=3` 只是一项最低信号，不是验证魔数。

---

## 九、当前原创方法论

见：`奇门/理论创新_受约束情境推演法_v0.2-alpha.md`

当前最可辩护的增量不是“已经更准”，而是：

**更少允许反馈后换轨，更容易暴露模型真正失败。**

---

## 十、当前工程阶段

已完成：

- `QM-SRC-0001` canonical 57/57 `VISUAL_PAGE`；
- 32 条 REVIEWED Atomic Evidence；
- REVIEWED Book Distillate；
- Method Delta + Prospective Test Plan；
- 十八局 source fixture index；
- Prospective Case Registry；
- `qimen-gexia` Pattern Registry migration；
- `qimen-gongpan` Component / Relation Registry migration；
- gexia/gongpan runtime-contract CI gates。

尚未完成：

- 十八局 `ANCHORS_VERIFIED`；
- 十八局 `IMPLEMENTATION_CHECKED`；
- `qimen-qiju` P2 migration；
- old cases reclassification；
- Test A-G 的真实前瞻实验；
- 任何经验有效性结论。

---

## 十一、Prospective Registry

未知结果正式测试使用：

- `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`
- `knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

详细私人 case packet 留在 Git 外；Git 保存冻结元数据与 hashes。

结果后改变 setup、method layer、time family、deity system、state system、Role Map、feature、分支、应期或 auxiliary policy，都必须新建模型版本/`case_id`。

污染案例保留，不得删掉以美化命中率。

---

## 十二、执行底线

- 不因书名权威而盲信；
- 不因案例像就称验证；
- 不因叙事连贯就称预测正确；
- 不因单次失败造全局补丁；
- 不因单次成功升级规则；
- 不在反馈后换盘、校准、方法层、时间族、八神体系、旺衰系统、用神、格局、应期；
- 不把 source fixture / runtime contract 通过当成预测有效；
- 不把传统犯罪/疾病象意当真实人物或医学事实；
- 不在高风险领域把术数当专业结论。

---

*QClaw Index v2.1 | 2026-08-21 | Method-Layer / Prospective Registry / Pattern Registry / Component-Relation Registry aligned*
