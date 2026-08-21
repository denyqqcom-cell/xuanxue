---
name: qimen-gexia
description: >
  奇门格局 / 十干克应 Pattern Registry 入口。用于识别结构、记录来源、适用域与冲突，
  不把格名或传统吉凶标签直接升级为现实结论。调用时必须服从 CURRENT_METHOD_CONSTRAINTS.md。
---

# 奇门格局：Pattern Registry 运行版 v2.1

> **上位约束**：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`qimen-overview/SKILL.md`、`_AGENT_INSTRUCTIONS.md`。
>
> **当前定位**：格局是 SOURCE / METHOD 层的结构候选，不是自动吉凶裁决器。
>
> **禁止恢复**：固定“吉格=吉、凶格=凶”、多凶格叠加自动相乘、`>=3分直接大凶`、旺相/休囚固定百分比折扣。

---

## 一、为什么从“格局详解”改成 Pattern Registry

旧技能把很多性质不同的东西都装进“吉格/凶格”两类：

- 天盘干 + 地盘干的有序组合；
- 星、门、神、奇仪的复合结构；
- 伏吟、反吟、门迫、入墓、击刑等状态结构；
- 五不遇时、天显时格等时间配置；
- 某些来源特有的遁格、口诀与传统应事。

这些不是同一种对象。若全部压成一个“吉凶格局表”，会产生至少三种错误：

1. **类型错误**：把状态、时间配置、天盘/地盘有序对当成同类格局；
2. **来源错误**：同名异义、异名同义、上下盘方向差异被静默合并；
3. **推理错误**：从格名直接跳到现实成败，绕过 Role Map、事类、旺衰状态、相反证据与方法族。

因此当前使用 Pattern Registry 六字段：

```text
PATTERN_TYPE
STRUCTURE
SOURCE_PROVENANCE
APPLICABILITY
EMPIRICAL_SUPPORT
OPERATIONAL_STATUS
```

需要时再附：`TRADITIONAL_LABEL / CONFLICTS / NOTES`。

---

## 二、Pattern Type

### 2.1 `STEM_PAIR_PATTERN`

天盘干与地盘干的**有序对**：

```text
ORDERED_PAIR = (HEAVEN_STEM, EARTH_STEM)
```

`戊加丙` 与 `丙加戊` 不是同一结构。不得只写成无方向的“戊丙组合”。

代表性传统名称包括：青龙返首、飞鸟跌穴、青龙逃走、白虎猖狂、太白入荧、荧入太白、大格等。

### 2.2 `COMPOSITE_PATTERN`

由星 / 门 / 神 / 奇仪 / 宫位等多个条件共同构成，如“三奇得使”“玉女守门”等。

必须记录完整条件，不能只保留格名。

### 2.3 `STRUCTURAL_STATE`

伏吟、反吟、门迫、入墓、击刑等首先是结构或状态特征。它们已有专门技能负责结构识别：

- 伏吟/反吟 → `qimen-bigpicture`
- 空墓刑迫 → `qimen-sihai`

本技能只保存其作为传统 Pattern 名称的 provenance，不再重复制造固定吉凶。

### 2.4 `TIME_CONFIGURATION`

五不遇时、天显时格等属于时间/起局配置，不应与十干克应混成一个“凶格表”。

需要同时绑定 `time_family / setup / source context`。

### 2.5 `METHOD_SPECIFIC_PATTERN`

某一来源或流派定义的遁格、组合规则。若结构定义尚未完成 K2 source verification，则保持 `SOURCE_REVIEW_REQUIRED`。

---

## 三、结构层硬约束

### 3.1 天盘/地盘方向不可丢

所有十干克应先写成：

```text
天盘 X 加 地盘 Y
```

若来源没有明确上下盘方向，标：

`DIRECTION_UNRESOLVED`

不得为了套上熟悉格名自行补方向。

### 3.2 “甲”不能被当作普通显式天盘/地盘干随意配对

标准遁甲盘中“甲”通常遁于六仪之下。旧技能写“庚+甲（任何组合）=最凶”，若理解为普通显式 stem pair，会造成结构误导。

当前处理：

- “庚克甲”保留为传统统帅/克甲概念候选；
- 真正进入盘面时必须说明甲遁何仪、当前方法怎样表达；
- 不允许把它注册成一个无上下文的 `STEM_PAIR_PATTERN(庚,甲)`。

### 3.3 普通八门布局下，一宫只能有一个值班门

旧技能出现“开+休+生三吉门同宫”的定义。对普通标准八门布局而言，三个不同门同时占同一宫与基本排布结构冲突。

因此“三吉门会聚同宫”当前状态：

`DEFINITION_UNRESOLVED / STRUCTURAL_CONFLICT`

除非找到明确的特殊盘式/“会聚”定义，否则不得运行。

同理，“乙丙丁三奇齐聚同宫或相邻”的“三奇会聚格”定义也需要 source/layout 重核；不能因为名称听起来熟悉就视为已确认结构。

---

## 四、当前迁移后的代表性 Registry

完整迁移审计见同目录 `PATTERN_REGISTRY.md`。本节只保留运行时需要的代表项。

| Pattern | Type | STRUCTURE | SOURCE_PROVENANCE | OPERATIONAL_STATUS |
|---|---|---|---|---|
| 青龙返首 | STEM_PAIR_PATTERN | 天盘戊 + 地盘丙 | legacy sources；需按具体 source 绑定 | SOURCE_CANDIDATE |
| 飞鸟跌穴 | STEM_PAIR_PATTERN | 天盘丙 + 地盘戊 | legacy sources；需按具体 source 绑定 | SOURCE_CANDIDATE |
| 青龙逃走 | STEM_PAIR_PATTERN | 天盘乙 + 地盘辛 | legacy sources | SOURCE_CANDIDATE |
| 白虎猖狂 | STEM_PAIR_PATTERN | 天盘辛 + 地盘乙 | legacy sources | SOURCE_CANDIDATE |
| 螣蛇夭矫/妖娇 | STEM_PAIR_PATTERN | 天盘癸 + 地盘丁（名称/字形依来源） | legacy sources | SOURCE_CANDIDATE |
| 大格 | STEM_PAIR_PATTERN | 旧技能登记为天盘庚 + 地盘癸 | lineage 待逐源复核 | SOURCE_REVIEW_REQUIRED |
| 朱雀投江 | STEM_PAIR_PATTERN / SOURCE_CONFLICT | 旧技能同时出现 `丁+丙临坤离` 与 `丁+癸` | 内部冲突 | CONFLICT_CANDIDATE |
| 小格 | STEM_PAIR_PATTERN / SOURCE_CONFLICT | 旧技能同时出现 `庚+壬` 与 `庚+己` | 内部冲突 | CONFLICT_CANDIDATE |
| 三奇得使 | COMPOSITE_PATTERN | 三奇与值使关系，具体结构按来源 | provenance 待拆 | SOURCE_REVIEW_REQUIRED |
| 玉女守门 | COMPOSITE_PATTERN | 丁奇与值使关系，具体结构按来源 | provenance 待拆 | SOURCE_REVIEW_REQUIRED |
| 天显时格 | TIME_CONFIGURATION | 六甲旬首值班相关配置 | method/time context required | METHOD_CANDIDATE |
| 五不遇时 | TIME_CONFIGURATION | 具体干配/时间条件由专门结构规则确认 | defer to qiju/sihai | STRUCTURE_DELEGATED |
| 门迫 | STRUCTURAL_STATE | 门克宫等结构定义按当前结构技能 | defer to qimen-sihai | STRUCTURE_DELEGATED |
| 入墓 / 击刑 | STRUCTURAL_STATE | 先准确识别结构 | defer to qimen-sihai | STRUCTURE_DELEGATED |
| 伏吟 / 反吟 | STRUCTURAL_STATE | 先识别盘面结构 | defer to qimen-bigpicture | STRUCTURE_DELEGATED |
| 三奇会聚 | COMPOSITE_PATTERN | 旧定义“同宫或相邻” | layout/source 未解决 | DEFINITION_UNRESOLVED |
| 三吉门会聚 | COMPOSITE_PATTERN | 旧定义“开休生同宫或相近” | 标准布局存在结构冲突 | DEFINITION_UNRESOLVED |

这些状态**不是预测结果等级**。

---

## 五、格局进入一次真实解盘的 Gate

一个 Pattern 只有同时通过下面问题，才可进入 `Eligible Feature Set`：

1. **STRUCTURE**：盘上结构是否真的成立？
2. **PATTERN_TYPE**：它究竟是有序干对、复合结构、状态还是时间配置？
3. **SOURCE_PROVENANCE**：本次采用的是哪一本书/哪一版本/哪一流派定义？
4. **METHOD CONTEXT**：当前 method_layer / method_family / layout / time_family 是否允许使用？
5. **ROLE / OBJECT**：这个 Pattern 作用到哪个角色或事项？
6. **APPLICABILITY**：来源是否限定事类、季节、旺衰、门星神或其他条件？
7. **CONTRARY EVIDENCE**：有没有同层级反向信号？
8. **EMPIRICAL_SUPPORT**：有没有独立前瞻支持？没有就明确写低/未知。

若第 1-4 项有任一不清楚：

`CONTEXT_REQUIRED / SOURCE_REVIEW_REQUIRED`

而不是继续查更多象意词把空缺填满。

---

## 六、传统吉凶标签怎样使用

“吉格 / 凶格 / 大格 / 小格 / 大吉 / 大凶”等属于来源中的传统标签时，可以保留，但必须写在：

`TRADITIONAL_LABEL`

它不能直接写入：

`outcome = SUCCESS / FAILURE`

当前允许的推理链是：

```text
STRUCTURE
→ SOURCE-defined traditional label
→ applicability / state / task / Role Map
→ competing evidence
→ contextual inference
→ frozen prediction
```

禁止：

```text
格名 = 大凶
→ 现实一定失败
```

---

## 七、旺相、空墓刑迫与“叠加”

旧技能曾同时出现：

- 吉格遇空/墓“吉性大减”；
- 凶格遇空/墓“凶性大减”；
- 旺相固定增强、休囚固定减弱；
- 多凶格自动“大凶”；
- 凶格叠加相乘；
- 固定分数到阈值直接裁决。

这些都不再是当前运行规则。

现行处理：

- 旺相、空、墓、刑、迫分别作为 state features；
- 是否增强、削弱、转义取决于 method family、作用对象与来源；
- 多个 Pattern 同时出现时先检查是否**真正独立**，避免同一底层结构重复计数；
- 如要建立量化权重，必须另建可校准模型并接受前瞻验证。

没有“默认相乘”。

---

## 八、十干克应不是“完整60组真值表”

旧技能把若干十干克应整理成“完整60组”，但当前至少有四个问题：

1. 当前文件并未真正给出可核对的完整 60 个有序组合；
2. 名称与组合在文件内部已经出现冲突；
3. 不同来源可能在字名、上下盘方向、应事与适用条件上不同；
4. 即使 source table 完整，也只证明来源如何定义，不证明现实效验。

所以当前不再提供一个跨流派“统一60组真值表”。

后续正确做法：

`source-specific registry -> ordered-pair verification -> conflict decomposition -> implementation fixture -> prospective test`

而不是先合成一张看似完整的总表。

---

## 九、已发现的 legacy 内部冲突必须保留

当前至少保留以下冲突，禁止静默修掉：

### 9.1 朱雀投江

旧技能一处登记为：`丁+丙临坤、离`；另一处登记为：`丁+癸`。

状态：`SOURCE_INCONSISTENCY / CONFLICT_CANDIDATE`。

### 9.2 小格

旧技能一处“庚金克甲系列”登记 `庚+壬=小格`；另一处格局表登记 `庚+己=小格`。

状态：`SOURCE_INCONSISTENCY / CONFLICT_CANDIDATE`。

### 9.3 三奇会聚 / 三吉门会聚

旧结构定义与普通标准布局存在可疑处。

状态：`DEFINITION_UNRESOLVED`，不得运行时自行脑补。

这类冲突是研究资产，不是需要偷偷清理掉的“难看数据”。

---

## 十、来源与 provenance 修正

旧技能总标题曾写：

`《奇门遁甲应用学》佚名`

当前 K2 已页内验证该工作作者为**王云鹏**，因此运行文档不得继续把该已验证工作称“佚名”。

同时，旧技能还引用《图解奇门遁甲大全》《奇门枢要》《图解遁甲演义》等来源。若这些条目尚未进入 K2 page-level Evidence，则当前只能视为：

`LEGACY_SOURCE_NOTE`

不能因为旧文件保存了一个书名或引号，就宣称已经完成原页核验。

现代书内容在运行技能中以短摘要/结构索引为主，不再大段复制原文。

---

## 十一、高风险 Pattern

任何格局涉及以下现实结论时必须降级为传统象意，不得直接输出事实判断：

- 死亡、重病、手术必要性；
- 犯罪、牢狱、官司必败；
- 灾害必然发生；
- 投资必赚/必亏；
- 赌博胜负；
- 对第三人的严重人格/违法断言。

可以说“某来源传统上把该结构解释为……”，不能把它替代医疗、法律、金融或事实调查。

---

## 十二、运行输出模板

调用本技能时，推荐只输出与当前问题有关的 Pattern：

```markdown
### Pattern
- name:
- pattern_type:
- structure:
- structure_verified: true/false
- source_provenance:
- traditional_label:
- applicability:
- role/object affected:
- contrary_evidence:
- empirical_support:
- operational_status:
- current_inference:
```

若存在冲突：

```text
CONFLICT_CANDIDATE / CONTEXT_SPLIT_REQUIRED / SOURCE_REVIEW_REQUIRED
```

不要为了“格局详解”四个字把全盘所有格名逐条念一遍。

---

## 十三、与前瞻验证的关系

正式未知结果预测中：

- Pattern 必须在 `Eligible Feature Set` 冻结；
- 反馈后新增格局 = `POST_FEEDBACK_FACTOR_SWITCH`；
- 同一底层结构被多个格名重复包装，不得多重计分；
- Pattern 的 Source Fidelity 可单独提高，但 Empirical Support 只能来自合格 prospective case。

`PATTERN REGISTRY PASS != PREDICTION VALIDATED`。

---

*QClaw qimen-gexia v2.1 | Pattern Registry migration | 2026-08-21*
