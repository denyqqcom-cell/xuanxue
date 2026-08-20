# 奇门当前方法约束层（2026-08-21）

状态：**ACTIVE / AUTHORITATIVE OVERLAY / v2.1**

适用范围：在后续奇门学习、解盘、技能调用、案例复盘、前瞻验证中，本文件用于约束旧版《奇门遁甲知识库》与 `qclaw` 技能中尚未完成迁移的确定性表述。

> 这不是新的“圣经”。它是一组当前有效的认识论约束；后续新书、强反例和前瞻验证可以修改、缩窄或废弃它。

## 一、为什么需要这一层

旧知识库和技能文件经历过多轮快速学习与修补，其中部分规则由单一案例、少量复盘或书本断语直接升级而来。随着 `QM-SRC-0016` 与 `QM-SRC-0001` 全书 Evidence / Book Distillate 完成，已确认若继续让这些旧表述直接作为运行规则，会出现四类污染：

1. **书证污染**：把“书里这么说”误写成“现实中已经成立”；
2. **后见污染**：一次失败后形成补丁，再把补丁扩张成全局规律；
3. **自由度污染**：多种用神、格局、起局法、时间族、八神体系、外应可在结果出来后任意切换；
4. **执行漂移**：反省日志已经改正，但真正运行的 workflow/skill 仍按旧规则执行。

因此，从本文件生效起，旧资料仍保留为历史知识与 SOURCE 层，但不得越过本约束层直接获得“已验证真理”地位。

## 二、四层强制分离

每个关键判断必须能区分：

- **SOURCE**：某书、某门派、某作者明确提出的规则或案例；
- **INFERENCE**：项目基于当前问题作出的情境转译、关系推演或抽象；
- **EMPIRICAL_SUPPORT**：反馈前冻结、结果后可核验的独立支持；
- **CONTAMINATION**：新闻、既知结果、求测者背景、外貌、外应、其他术数、搜索资料等可能帮助答案但妨碍归因的信息。

书证再多，只能提高 Source Fidelity。除非经过独立验证，否则不能自动提高 Empirical Support。

## 三、当前已撤销的“全局硬规则”

### 1. 固定全局优先级

旧：`开门 > 值符 > 生门 > 星神`

现：**DEPRECATED AS GLOBAL RULE**。

信息层优先级必须绑定问题类型、方法族、盘式、角色与具体任务。若某一方法族确有固定顺序，应在预测前声明并冻结，只在该适用域内测试。

### 2. 逢空固定翻译

旧：`逢空 = 方向待定`

现：**CANDIDATE / CONTEXT_REQUIRED**。

空亡只先记录为状态特征。它可能在不同事类中对应延迟、落空、未定、脱离、暂缺、失效或其他含义；不得把旧的“逢空必凶”换成新的“逢空必待定”。

### 3. 凶格固定计分与相乘

旧：`凶格叠加相乘，>=3 分直接断大凶`

现：**UNVERIFIED HEURISTIC**。

可保留作研究变量，不得作为硬裁决器。若要保留计分模型，必须先定义每一项权重、适用域、基线、校准方式，并通过前瞻数据检验。

### 4. 旺衰固定折扣

旧：`旺相=全额，休囚=减半，四害自动打折/加重`

现：**REJECT FIXED COEFFICIENT SEMANTICS**。

旺衰、空、墓、刑、迫等仍是候选 feature，但其作用方向与强度必须由方法族、事类和组合关系决定；不得使用未经校准的百分比或固定折扣。

### 5. “三次即验证”

旧：`>=3 次独立真验证 = 已验证`

现：`>=3` 只作为进入 **PROVISIONAL** 的最低信号之一。

还必须检查：预注册、案例独立性、基础概率、失败样本、选择偏差、信息污染、竞争方法、负对照以及适用域外表现。

### 6. 强制先读三条新闻

旧：`确认对象存在 -> 查>=3条宏观新闻 -> 再看盘`

现：对象是否存在仍是必要 Reality Baseline；新闻属于 **AUXILIARY CHANNEL**。

需要研究奇门本体贡献时，应先完成 `method-only` 判断并冻结，再加入新闻/现实背景形成 `context-augmented` 判断，单独记录增量。

## 四、Method-Layer Gate：先确定“在用哪一种奇门”

`QM-SRC-0001` 证明，同一本入门书已经同时包含多个性质不同的方法层。新案例必须先冻结一个主层：

- `STANDARD_PLATE`：标准三元/时家排局与盘面解释；
- `TIME_FAMILY_VARIANT`：YEAR / MONTH / DAY / HOUR 各自独立算法；
- `HOUR_OMEN`：如九星十二时辰应克，单独计分；
- `RITUAL_AUXILIARY`：符咒、反闭、步斗、六戊、禁敌等，默认 `eligible=false`。

一个方法层的 miss 不得由另一个层在结果后救援。若要 A/B 比较，必须在反馈前并行冻结，并分别计分。

## 五、起局与上下文必须成为一等变量

标准盘至少显式记录：

```text
method_layer
method_family
setup_calibration = PINGQI | DINGQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
seasonal_alignment = ZHENGSHOU | CHAOSHEN | ZHIRUN | JIEQI | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
time_family = YEAR | MONTH | DAY | HOUR | NOT_APPLICABLE
layout_method
deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER | NOT_APPLICABLE
hour_omen_family
ritual_layer
bureau_table_source
```

未知项必须标 `CONTEXT_REQUIRED` 或 `NOT_APPLICABLE`，不能根据结果挑最合适的值。

### 八神体系

梁书使用勾陈、朱雀体系，而现代资料常见白虎、玄武体系。两者暂按 `deity_system` 平行保存：

- 不静默改名；
- 不在一盘内借用两套象意；
- 未经来源/版本/布局拆解，不视为天然同义；
- 若要比较，采用反馈前冻结的平行模型。

## 六、从“模板解盘”改为“受约束情境推演”

当前推荐流程升级为：

`Reality Baseline`
→ `Question Domain`
→ `Method-Layer Freeze`
→ `Time Family + Setup Calibration + Seasonal Alignment Freeze`
→ `Deity-System / Layout Context Freeze`
→ `Role Map Freeze`
→ `Bureau / Structural Lookup`
→ `Eligible Feature Set`
→ `Contextual Relations`
→ `Competing Interpretation Branches`
→ `Frozen Prediction`
→ `Optional Auxiliary Context Ablation`
→ `Outcome Audit`
→ `Rule Lifecycle Update`

关键差异：

- **情境化不等于自由发挥**；
- **推演越灵活，越需要反馈前冻结**；
- **叙事越漂亮，越不能拿叙事本身当证据**；
- **方法越丰富，越不能允许结果后的层级切换。**

## 七、星门神奇仪宫的使用原则

星、门、神、奇仪、宫位、旺衰、生克、空墓刑迫、伏吟反吟、格局等均先视为候选信息层，而非自动结论。

对任一关键特征至少问：

1. 当前问题域中它代表谁或什么？
2. 这个角色映射是书本固定、方法族规定，还是本次推演？
3. 它与其他用神是主关系、辅助关系还是局部背景？
4. 若移除该特征，结论会不会改变？
5. 什么结果会证明当前解释错了？

九星等固定“吉/凶”标签最多作为传统粗粒度 prior。即使来源给固定标签，也必须经过季节、事项、状态、角色与竞争信号后才可形成情境判断。

## 八、Lookup Determinism 不等于 Predictive Validity

十八局表等机械查表结构有重要价值：它们能够降低排盘阶段自由度并帮助发现实现漂移。

但必须分开：

`Source Fidelity != Lookup Determinism != Empirical Support`

- Source Fidelity：代码是否忠实复刻来源规定；
- Lookup Determinism：同一输入是否稳定得到同一结构；
- Empirical Support：该方法是否在未知结果的前瞻测试中优于合理基线。

通过 fixture / regression test 不得被表述为“预测法已经验证”。

## 九、叙事与多重解释的约束

允许一个盘存在多个合理解释，但必须在反馈前保存竞争分支。

每个重要分支至少记录：

- 前提条件；
- 主导证据；
- 与竞争分支的区别；
- 可观察的区分结果；
- 失败条件。

反馈后只能评分，不能新造分支再算“原预测命中”。

`叙事连贯性` 仅用于评估解释是否自洽，不等于经验支持。

## 十、书本案例与仪式材料的地位

书本案例主要用于：

- 理解作者实际怎样选信息；
- 找规则的适用边界；
- 暴露方法自由度；
- 生成待检验假设；
- 找失败模式与内部矛盾。

除非案例具有反馈前记录、独立结果和可核验流程，否则不得用于证明作者方法准确率。

符咒、步斗、禁敌、博奕等材料可作为历史/仪式 SOURCE 研究，但默认不进入普通预测评分，也不得因为“书中有记载”升级为现实因果证据。

## 十一、Reality Baseline 与现实常理

“结合实际”不是拿现实信息强行替盘面圆结果，而是先确认：

- 预测对象真实存在；
- 时间、地点、事件定义没有错误；
- 已知事实与待预测事实被严格分开；
- 常识性基础概率被记录；
- 高风险领域不把术数判断替代专业判断。

Reality Baseline 先于玄学解释，但在方法验证中必须与辅助信息归因分离。

## 十二、Prospective Case Registry

未知结果的正式前瞻测试必须遵循：

`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`

并在：

`knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl`

保存机器可审计的冻结元数据。详细问题、私人背景和本地 case packet 可留在 Git 外，通过 SHA256 与 registry 绑定。

任何以下变化发生在反馈后，都不得覆盖原 case：

- 起局/校准改变；
- 方法层改变；
- 时间族改变；
- 八神体系改变；
- Role Map 改变；
- eligible feature 改变；
- 竞争分支或应期方法改变；
- 辅助信息政策改变。

## 十三、规则生命周期

当前统一使用：

`CANDIDATE -> TESTABLE -> PROVISIONAL -> SUPPORTED`

允许反向变化：

`SUPPORTED/PROVISIONAL -> NARROWED -> DEPRECATED -> REJECTED`

“渐进式迭代”不再解释为“旧规则全部保留，只加新层”。真正的渐进是：修改有版本、删除有证据、边界有记录。

## 十四、Prediction Protocol Freeze != Theory Freeze

单次预测必须冻结协议，防止反馈后换方法、换用神、换格局、换解释。

跨案例、跨书、跨版本的理论则必须保持可推翻。若后续文献或前瞻实验给出更强反例，当前 Method-Layer Gate、四分法甚至整个流程本身都可以被 `NARROW / REVISE / SPLIT / DEPRECATE / REJECT`。

## 十五、当前待验证核心假设

以下仍不是定论：

- Method-Family-Specific Priority 是否优于固定全局优先级；
- Method-Layer Gate 是否显著减少事后救援；
- 平气/定气、正授/超神/置闰/接气是否存在稳定前瞻差异；
- 勾陈朱雀 vs 白虎玄武是否有可重复的增量价值；
- 九星固定标签是否劣于季节/事项/状态条件化模型；
- 九星十二时辰应克是否优于基础概率与 shuffled controls；
- 年/月/日/时的传统层级是否真实存在，还是应拆成不同对象；
- Role Map Freeze 能否显著减少反馈后换用神；
- 多分支预注册能否降低叙事后见偏差；
- 外部信息消融能否分离奇门本体贡献。

这些问题由后续文献与前瞻实验共同推进，不以“某大师说法”直接裁决。

## 十六、执行优先级

发生冲突时，当前项目读取顺序为：

`K2 Evidence / Book Distillate / Method Delta / Pre-Book Retrospective`
→ `CURRENT_METHOD_CONSTRAINTS.md`
→ `K2 Prospective Case / Source Fixture Protocols`
→ `当前版本理论草案`
→ `qclaw 技能与旧知识库`
→ `更早修炼日志`

这里的“优先”是**项目运行约束优先级**，不是判断某条玄学规则真假的证据等级。
