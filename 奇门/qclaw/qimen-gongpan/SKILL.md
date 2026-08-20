---
name: qimen-gongpan
description: >
  奇门宫盘 Component / Relation Registry。用于识别九宫、九星、八门、八神、奇仪等结构与来源象意，
  再绑定 Role Map、状态与关系形成受约束推演；不使用固定“星门神吉凶相加”裁决。
---

# 析宫盘：Component / Relation Registry v2.1

> **上位约束**：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`qimen-overview/SKILL.md`、`_AGENT_INSTRUCTIONS.md`。
>
> **当前定位**：宫盘分析不是把“九星词典 + 八门词典 + 八神词典”逐项相加，而是把结构、来源象意、状态、角色和关系分层后推演。

---

## 一、先拆六层，禁止“词典直译现实”

宫盘信息统一拆成：

```text
STRUCTURAL_METADATA
SOURCE_SYMBOLISM
STATE_FEATURE
ROLE_BINDING
RELATION
CONTEXTUAL_INFERENCE
```

### 1.1 STRUCTURAL_METADATA

可机械核对的盘面信息，例如：

- 宫号 / 卦 / 五行 / 后天方位；
- 某星、门、神、天盘干、地盘干实际落宫；
- 同宫、对宫、生克、比和等关系；
- 已冻结方法下的旺衰/状态计算结果。

### 1.2 SOURCE_SYMBOLISM

书中给出的传统类象、吉凶词、人物/事物映射。

这些只说明“某来源这样解释”，不自动成为现实事实。

### 1.3 STATE_FEATURE

旺相休囚、空墓刑迫、伏吟反吟等状态。它们不能用固定百分比给星门神“加减分”。

### 1.4 ROLE_BINDING

当前问题里谁代表求测者、事件、对方、财、职位、文书等，必须先由 Role Map 冻结。

### 1.5 RELATION

宫内和宫间真正进入推演的是关系，例如：

- 某 Role 所在宫被另一 Role 生/克；
- 同一宫内星门神是否提供同向或反向候选语义；
- 某状态具体作用到谁。

### 1.6 CONTEXTUAL_INFERENCE

项目根据问题域作出的当前推演。必须和 SOURCE 分开，并保留竞争分支与失败条件。

---

## 二、九宫：结构信息与传统象意分开

当前结构层保留：

| 宫 | 卦 | 五行 | 后天方位 |
|---|---|---|---|
| 1 | 坎 | 水 | 北 |
| 2 | 坤 | 土 | 西南 |
| 3 | 震 | 木 | 东 |
| 4 | 巽 | 木 | 东南 |
| 5 | 中 | 土 | 中央 |
| 6 | 乾 | 金 | 西北 |
| 7 | 兑 | 金 | 西 |
| 8 | 艮 | 土 | 东北 |
| 9 | 离 | 火 | 南 |

“盗贼、丧事、坟墓、疾病、车祸、聪明”等不是九宫本身的结构事实。若某来源给出这类映射，归入 `SOURCE_SYMBOLISM`。

### 九宫象意使用 Gate

调用某宫传统象意前至少问：

- 本次用的是哪一来源/方法族？
- 它在当前题里绑定哪个 Role/Object？
- 是空间象、人物象、物象还是事件象？
- 有没有其他同样合理的类象？
- 什么结果能区分这些竞争解释？

不能因为“坤宫传统上有病符/丧象”就直接断现实疾病或丧事。

---

## 三、九星：身份结构、来源标签、季节状态三件事分开

### 3.1 基础结构索引

当前只把以下作为常见结构索引保存；吉凶等级属于来源层：

| 星 | 常见本宫 | 五行 |
|---|---|---|
| 天蓬 | 坎一 | 水 |
| 天芮 | 坤二 | 土 |
| 天冲 | 震三 | 木 |
| 天辅 | 巽四 | 木 |
| 天禽 | 中五 | 土 |
| 天心 | 乾六 | 金 |
| 天柱 | 兑七 | 金 |
| 天任 | 艮八 | 土 |
| 天英 | 离九 | 火 |

旧技能中的“天蓬=凶、天禽=大吉、天心=大吉、天柱=凶”等可作为 `TRADITIONAL_LABEL` 保留，但不再直接决定现实成败。

### 3.2 人物/事件类象是 SOURCE lexicon

旧资料把某些九星直接列成“杀人犯、黑社会、贩毒走私、车祸、疾病”等人物/事件类别。

当前处理：

- 只作为来源中的传统联想词；
- 不得用来判断真实人物是罪犯、骗子或有某疾病；
- 不得单独用于高风险事实判断；
- 若进入解释，应说明为什么当前问题域允许该类象，并同时保留更普通的竞争解释。

### 3.3 九星旺相休囚存在 legacy 内部冲突

旧技能同一文件对天蓬季节状态出现了互相不一致的写法：

- 一处示例写成：天蓬“旺于亥子、相于寅卯”；
- 后一处“应用学体系”又写成：天蓬“旺于寅卯、相于亥子”。

这不是可以靠“理解大意”略过的小差异，因为它会直接改变状态判断。

当前状态：

`SOURCE_INCONSISTENCY / STAR_STATE_SYSTEM_REQUIRED`

因此：

```text
star_state_system = SOURCE_DEFINED / CONTEXT_REQUIRED
```

在未冻结具体来源的九星状态算法前，不得输出“某星旺/相/休/囚，因此吉凶增强多少”。

---

## 四、八门：本宫/五行可做结构索引，吉凶与事类是候选语义

| 门 | 常见本宫 | 五行 |
|---|---|---|
| 开 | 乾六 | 金 |
| 休 | 坎一 | 水 |
| 生 | 艮八 | 土 |
| 伤 | 震三 | 木 |
| 杜 | 巽四 | 木 |
| 景 | 离九 | 火 |
| 死 | 坤二 | 土 |
| 惊 | 兑七 | 金 |

传统常把开、休、生列为吉门，把伤、死、惊列为凶门，并赋予求财、官讼、出行、丧葬等事类语义。

当前使用方式：

`门 = task/process candidate feature`

而不是：

`门名 = 现实结论`

例如：

- 生门可以是求财问题中的来源候选 Role/Feature，但“见生门=一定赚钱”禁止；
- 死门可在某来源中表示结束、停滞、土地、丧葬等，但“死门=死亡”禁止；
- 惊门可与口舌/惊恐类象相关，但不能单独推出官司、事故或精神状态。

### 八门旺衰

旧技能保存了一套门的旺相休囚死季节表。当前不删除该 SOURCE 资料，但运行时必须绑定具体 `door_state_system`；不再默认它是所有流派共用算法。

---

## 五、八神：必须先冻结 deity_system

梁湘潤 `QM-SRC-0001` 使用勾陈 / 朱雀体系，而旧 `qimen-gongpan` 主要保存白虎 / 玄武体系。

所以调用八神前必须已有：

```text
deity_system = GOUCHEN_ZHUQUE | BAIHU_XUANWU | SOURCE_DEFINED_OTHER
```

禁止：

- 在同一预测里把白虎/玄武的象意借给勾陈/朱雀；
- 因为两个体系都有八个位置就认为天然同义；
- 结果后切换体系寻找更贴合解释。

### 传统八神类象的地位

“值符贵、白虎凶、玄武盗、九天利出击、九地利固守”等是来源候选语义。

运行时必须继续经过：

`Role/Object -> task -> state -> relation -> contrary evidence`

不能直接从神名下行动命令。

---

## 六、宫内分析不再使用固定“五层优先级”

旧技能规定：

`九星 -> 八门 -> 八神 -> 八卦 -> 十干`

并把它当成固定宫内五层顺序。

当前改为：

`METHOD-FAMILY-SPECIFIC FEATURE ORDER`

也就是说：

- 问题域和方法族先决定哪些层 eligible；
- 若某来源规定内部优先级，反馈前冻结；
- 没有来源/测试支持时，不因为“以前一直这么排”而赋固定权重。

### 推荐关系图

```text
Frozen Role Map
  ↓
Relevant Palace(s)
  ↓
Eligible Components (star / door / deity / stems / palace)
  ↓
State Features
  ↓
Within-palace + cross-palace relations
  ↓
Contrary evidence
  ↓
Competing branches
```

---

## 七、撤销“星门神吉凶相加”表

旧技能存在类似：

- 吉星 + 吉门 + 吉神 = 大吉；
- 凶星 + 凶门 = 大凶；
- 吉神自动化解部分凶性；
- 凶神自动加重凶性。

这类表把来源标签当成可直接相加的数值，容易造成重复计票和机械裁决。

当前不再运行。

如果多个组件同向，只能先记录：

`CONVERGENT_SOURCE_SIGNALS`

然后检查：

- 是否来自同一个底层结构；
- 是否作用于同一个 Role；
- 是否是独立信息还是同义重复；
- 反向证据是否存在；
- 当前事项是否真的匹配这些来源语义。

“多个标签一致”不自动等于高 Empirical Support。

---

## 八、撤销固定“能量增强/减弱”系数语义

旧技能把旺、相、休、囚、死写成统一强弱，并进一步写“吉星旺则大吉、凶星旺则大凶”。

当前改成：

- 状态算法先按 source/system 冻结；
- 状态只描述当前来源定义下的强弱/作用条件；
- 状态与现实吉凶的关系仍需事类、Role 与前瞻验证；
- 不使用固定百分比或默认乘法。

特别是九星状态算法当前已有内部冲突，所以未指定 `star_state_system` 时应输出 `CONTEXT_REQUIRED`。

---

## 九、十干/格局由 qimen-gexia Pattern Registry 接管

旧 gongpan 把十干克应作为宫内“第五层”并直接接格局吉凶。

当前统一路由：

`qimen-gexia/PATTERN_REGISTRY.md`

要求：

- 保留 `(天盘干, 地盘干)` 有序方向；
- Pattern 类型与来源明确；
- 内部冲突不静默修正；
- 反馈后新增格局记 `POST_FEEDBACK_FACTOR_SWITCH`。

宫盘技能本身不再复制一份十干吉凶表。

---

## 十、人体 / 疾病映射：只允许 SOURCE 层研究

旧技能保存了：

- 九宫对应人体部位/脏腑；
- 九星、八门对应癌症、心脑血管、肝胆、脾胃等疾病；
- 某些宫象直接映射病症。

这些属于传统术数/传统医象资料，不是医学证据。

真实健康问题中：

- 可以说明“某来源传统上这样映射”；
- 不得据此诊断疾病、判断良恶性、决定手术/用药、预测生死；
- 医疗事实由专业检查与医生判断；
- 在研究 registry 中这类 feature 标 `HIGH_RISK_SOURCE_SYMBOLISM`。

---

## 十一、风水条目从宫盘全局规则降为 METHOD_SPECIFIC SOURCE

旧技能末尾存在一组风水规则，例如：

- 日干=人、时干=宅；
- 时干生日干就“风水无害”；
- 时干克日干就“不利”；
- 某些干、门直接代表梁、床、灶、坟、阳宅/阴宅。

这些不是普通宫盘的全局规则。

当前处理：

- `method_family = FENGSHUI` 时才有资格调用；
- Role Map 必须事前冻结；
- “无害/有害”不得覆盖其他现实信息；
- 具体物象属于 SOURCE lexicon，需要空间/现场信息与竞争解释；
- 不把盘面物象当作真实建筑缺陷的替代检查。

---

## 十二、来源 provenance 修正

旧技能多处写：

`《奇门遁甲应用学》佚名`

K2 已通过页内证据确认对应已审工作作者为**王云鹏**。因此当前运行层不再把这个已验证工作称为“佚名”。

同时，旧技能引用《图解奇门遁甲大全》、幺学声资料、善天道讲义等。没有进入当前 page-level K2 Evidence 的具体表格/引文，统一先标：

`LEGACY_SOURCE_NOTE`

旧文档里存在过引号，并不等于今天已经重新核过原页。

---

## 十三、当前宫盘推演流程

```text
1. Read frozen Method-Layer / Method-Family context
2. Read frozen deity_system / state-system context
3. Read frozen Role Map
4. Select relevant palace(s)
5. Verify STRUCTURAL_METADATA
6. Load only eligible SOURCE_SYMBOLISM
7. Attach STATE_FEATURES with source-specific algorithm
8. Build within-palace / cross-palace RELATIONS
9. Identify contrary evidence
10. Create competing branches
11. Freeze conclusion + failure conditions
```

任何一步出现来源/算法冲突时：

`CONTEXT_REQUIRED / SOURCE_REVIEW_REQUIRED / CONFLICT_CANDIDATE`

而不是通过增加更多象意词解决。

---

## 十四、输出模板

```markdown
### Palace Analysis
- palace:
- structural_metadata:
- role_binding:
- eligible_components:
- deity_system:
- star_state_system:
- door_state_system:

### Source Symbolism
- star:
- door:
- deity:
- stems/pattern:

### Relations
- within_palace:
- cross_palace:
- state_features:

### Contrary Evidence
- ...

### Competing Branches
- H1:
- H2:

### Epistemic Split
- SOURCE:
- INFERENCE:
- EMPIRICAL_SUPPORT:
- CONTAMINATION:
```

不要求每个宫都填满，也不要求每个符号都解释。

---

## 十五、运行底线

- 九宫、九星、八门、八神先分结构与象意；
- 不按固定“星门神吉凶表”相加；
- 不把旺衰当通用乘数；
- 不混用八神体系；
- 不从传统犯罪/疾病类象直接判断真实人物或医学事实；
- 不把风水专用 Role Map 当普通问题全局规则；
- 不因叙事细节很多就提高 Empirical Support；
- 结果后补入星门神/格局解释不得修补原预测。

---

*QClaw qimen-gongpan v2.1 | Component / Relation Registry migration | 2026-08-21*
