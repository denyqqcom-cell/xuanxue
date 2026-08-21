# 奇门 QClaw 知识体系索引 v2.3

> **执行前必读**：
> 1. `奇门/CURRENT_METHOD_CONSTRAINTS.md`
> 2. `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`
> 3. `qclaw/_AGENT_INSTRUCTIONS.md`
> 4. `qclaw/qimen-overview/SKILL.md`

QClaw 当前定位：**受约束情境推演 + 前瞻冻结登记**。旧技能继续保存 SOURCE / history，但不拥有自动真值地位。

## 一、当前技能角色

| 技能 | 当前定位 |
|---|---|
| `qimen-overview` | 运行入口：Method/Setup/Time/Deity/State/Role/Pattern 冻结与 Outcome Audit |
| `qimen-basics` | 基础结构与传统来源层 |
| `qimen-datum` | 问题分类候选，不是最终 taxonomy |
| `qimen-bigpicture` | 伏吟反吟、日时、内外盘 Feature Map |
| `qimen-yongshen` | Role Map 候选；反馈前冻结 |
| `qimen-sihai` | 空亡/入墓/击刑/门迫结构识别 |
| `qimen-gongpan` | Component / Relation Registry；结构、象意、状态、Role、关系分层 |
| `qimen-shengke` | 宫间关系与主客候选 |
| `qimen-yingqi` | Timing Method Registry；禁止结果后挑应期 |
| `qimen-gexia` | Pattern Registry；格名不是自动结论 |
| `qimen-qiju` | Setup Method Registry；拆补/置闰/茅山、日界、宫序等必须 source-specific freeze |
| `qimen-cases` | 旧案例待重新分类，不直接证明准确率 |
| `qimen-yange` | 歌诀/传统文本来源层，仍需 provenance migration |

## 二、当前执行顺序

```text
Reality Baseline
→ Question Domain
→ Method Layer / Family
→ Setup Method + Calibration + Seasonal Alignment
→ Time Boundary + Time Family + Layout + Deity System
→ Star/Door State Systems
→ Role Map
→ Structural Lookup
→ Eligible Feature Set
→ Component / Relation Analysis
→ Pattern Registry
→ Competing Branches
→ Timing Freeze
→ Frozen Prediction
→ Prospective Registry
→ Auxiliary Ablation
→ Outcome Audit
→ Rule Lifecycle
```

## 三、三个必须分离的验证维度

```text
SOURCE CONSENSUS != EMPIRICAL SUPPORT
SOURCE FIDELITY != LOOKUP DETERMINISM != EMPIRICAL SUPPORT
RUNTIME CONTRACT PASS != PREDICTION VALIDATED
```

## 四、当前关键冻结字段

正式可评分模型至少明确：

```text
method_layer
method_family
setup_method
setup_calibration
seasonal_alignment
time_boundary_system
time_family
layout_method
deity_system
star_state_system
door_state_system
hour_omen_family
ritual_layer
bureau_table_source
Role Map
Eligible Feature Set
Competing Branches
Timing Protocol
Auxiliary Policy
```

结果后改变任何关键字段只能新建模型版本/`case_id`。

## 五、当前已确认的真实 legacy 冲突

- gexia：朱雀投江两套干对；小格两套干对；三吉门/三奇会聚定义不清；
- gongpan：天蓬旺相状态出现两套相反示例；
- deity system：勾陈/朱雀 vs 白虎/玄武；
- qiju：超神/接气定义方向反转；拆补两套算法描述；拆补/茅山重叠；子时 20-23 vs 23-24；宫号序列与“顺逆时针”混写。

这些冲突是研究资产，不静默修成一套“统一古法”。

## 六、旧速查/硬规则降级

以下均不再是跨场景真理：

- `开门 > 值符 > 生门 > 星神`；
- 逢空固定待定；
- 凶格>=3分/相乘；
- 旺相全额、休囚减半；
- 吉星+吉门+吉神=大吉；
- 伏吟=守成、反吟=出击；
- “拆补法推荐/最准/最常用”作为选择依据；
- 任何传统疾病、犯罪、死亡类象直接当事实。

## 七、当前验证生命周期

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

允许反向：

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`

`>=3` 不是验证魔数。

## 八、当前原创方法论

`奇门/理论创新_受约束情境推演法_v0.2-alpha.md`

当前最可辩护的价值不是“已经更准”，而是：**更少允许反馈后换轨，更容易让模型真正失败。**

## 九、QM-SRC-0001 当前完成状态

已完成：

- canonical 57/57 `VISUAL_PAGE`；
- 32 REVIEWED Atomic Evidence；
- REVIEWED Book Distillate；
- Method Delta + Prospective Test Plan；
- 十八局 p32-p49 source fixture index；
- Prospective Case Registry；
- gexia Pattern Registry migration；
- gongpan Component / Relation Registry migration；
- qiju Setup Method Registry migration；
- execution/gexia/gongpan/qiju runtime-contract CI gates。

尚未完成：

- 十八局 `ANCHORS_VERIFIED`；
- 十八局 `IMPLEMENTATION_CHECKED`；
- old cases reclassification；
- yange provenance migration；
- Test A-G 真实前瞻实验；
- 任何经验有效性结论。

## 十、Prospective Registry

正式未知结果测试使用：

- `knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`
- `knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

Git 保存冻结元数据/hashes，详细私人 case packet 留在 Git 外。污染案例保留，不得为了命中率删除。

## 十一、执行底线

- 不因书名/作者/古籍权威盲信；
- 不因案例“像”就称验证；
- 不因叙事连贯就称正确；
- 不在结果后换 setup、日界、method layer、time family、deity/state system、Role Map、Pattern、应期；
- 不把 fixture/runtime contract PASS 当预测有效；
- 不把传统高风险象意当专业结论；
- 不用辅助信息倒算奇门本体能力。

---

*QClaw Index v2.3 | 2026-08-21 | Setup / Time-Boundary / State-System / Pattern / Component Registry aligned*
