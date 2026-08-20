# 📚 奇门遁甲文献库

> 统一收纳奇门遁甲相关文献、知识记录、方法约束、技能与生成内容。

## ⚠️ 当前运行入口（2026-08-21 起）

旧知识库与 `qclaw` 技能保留大量历史书证、案例和早期规则，但其中仍有部分“书证=真值”、固定优先级、单案例过度泛化和旧版机械断法。

后续学习与解盘必须先读取：

1. `奇门/CURRENT_METHOD_CONSTRAINTS.md` —— 当前**权威运行约束层**；
2. `奇门/理论创新_受约束情境推演法_v0.2-alpha.md` —— 当前原创方法论草案，**未验证、可推翻**；
3. K2 `Atomic Evidence / Book Distillate / Pre-Book Retrospective` —— 用于来源、冲突、适用域与方法更新；
4. 再调用 `qclaw` 与《奇门遁甲知识库》作为历史知识/来源层。

发生冲突时，不得因为旧文件写得更肯定就自动采用旧规则。书本与技能中的确定性断语首先按 SOURCE / CANDIDATE 处理，再看适用域和经验支持。

`Prediction Protocol Freeze != Theory Freeze`：单次预测冻结以防后见修改；跨书、跨案例的理论必须允许被反例缩窄、修改或废弃。

---

## 📁 目录结构

```text
F:\奇门遁甲\
├── 📖 PDF文献/               ← 本地研究原件，不随仓库打包
├── 📊 qimen_catalog.md       ← 文献目录分类
├── 🧠 CURRENT_METHOD_CONSTRAINTS.md
├── 🧪 理论创新_受约束情境推演法_v0.2-alpha.md
├── 🔧 qclaw/                 ← 历史/运行技能，逐步迁移到新约束
└── 🖼️ 生成内容/
```

---

## 📖 文献速查

### 🏛️ 核心教材

- 《图解奇门遁甲大全》第1部 吉凶占断
- 《图解奇门遁甲大全》第2部 阳遁540局
- 《图解奇门遁甲大全》第3部 阴遁540局
- 《奇门遁甲应用学》
- 《奇门遁甲预测学》

### 🔮 秘传/进阶

- 《奇门枢要》上、下集
- 《奇门遁甲秘传》姜春龙
- 《图解遁甲演义》上、下部

### 🧭 断局技法

- 善天道《奇门遁甲高级研修班讲义294页》
- 善天道《奇门遁甲精华》
- 善天道《奇门遁甲讲义71页》
- 《奇门遁甲吉凶占断教程》
- 《奇门直断》

### 🏛️ 经典古籍

- 《金函玉镜奇门遁甲秘笈全书》上、下
- 《笺元遁甲句解烟波钓叟歌》
- 《甲遁真授秘录》
- 《奇门統宗大全》
- 《奇门精粹：奇门遁甲典籍大全》

### 📊 实例与流派

- 《奇门遁甲最新实例解析》
- 曾子南《三元奇门遁甲讲义》上、中、下
- 梁湘润《奇门遁甲入门》（K2 target `QM-SRC-0001 / WORK-000217`，57页，SCAN / VISUAL_REQUIRED）

### 📗 其他

- 《奇门遁甲白话精解》
- 《奇门遁甲新述》费秉勋
- 日家奇门相关资料

> 文件名、作者、版本与页数以 K1/K2 verified metadata 为准；本页仅作导航，不替代 provenance。

---

## 🎯 当前解盘不是固定“九步模板”

旧版：

`明确问题 → 起局排盘 → 看大局 → 取用神 → 查四害 → 析宫盘 → 看生克 → 定应期 → 综合结论`

仍可作为**检查清单**，但不再视为所有方法族必须使用同一固定顺序的真理。

当前受约束流程：

```text
Reality Baseline
→ Question / Method Family
→ Setup + Layout + Time Family Freeze
→ Role Map Freeze
→ Eligible Feature Set
→ Contextual Relations
→ Competing Interpretation Branches
→ Frozen Prediction
→ Optional Auxiliary Context Ablation
→ Outcome Audit
→ Rule Lifecycle Update
```

重点不在于解释更多符号，而在于：**预测前限制自由度，结果后禁止改写原路径。**

---

## 🔬 当前验证纪律

- SOURCE ≠ INFERENCE ≠ EMPIRICAL_SUPPORT ≠ CONTAMINATION。
- 书本案例默认用于理解方法、发现边界与生成假设，不直接证明准确率。
- `>=3` 个独立前瞻案例只够形成 provisional signal，不等于“已验证”。
- 新闻、人物背景、外应和其他术数属于辅助通道；验证时必须与 method-only 输出分离。
- 任何“必吉、必凶、必发财、必伤灾”等断语，除非明确限定为“原书断语”，否则不得作为项目事实直接输出。
- 高风险领域不得以术数替代专业判断。

---

## 🔧 工具与技能

`qclaw/` 中的技能是持续迁移中的历史资产。调用前必须遵守 `CURRENT_METHOD_CONSTRAINTS.md`，不能因为某个 `SKILL.md` 使用“严格优先级”“大凶”“必”等措辞，就绕过 K2 的证据与适用域约束。

已知旧技能中的事实性错误应直接修正；属于流派差异或未验证理论的内容则保留来源，但降级为 SOURCE/CANDIDATE，而不是静默改成另一家说法。

---

## 📌 下一单书

`QM-SRC-0001 / WORK-000217 / 梁湘润《奇门遁甲入门》`

闭环：

`Pre-Book Retrospective → 57/57 原页视觉阅读 → Atomic Evidence → Book Distillate → Conflict/Anti-pattern → Method Delta → Prospective Test Plan → Validators/CI → CLOSED`

该书是 SCAN / VISUAL_REQUIRED。没有原始视觉页时，OCR、文本转录、旧笔记或网络摘要均不能替代 Reading Credit。

---

*最后更新：2026-08-21*
