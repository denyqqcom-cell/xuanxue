# 奇门运行知识债务审计 — 2026-08-21

状态：ACTIVE REVIEW

目的：记录“已经认识到的问题”和“尚未完成迁移的旧知识”，防止因为入口层升级就误以为整个奇门知识库已经完成纠偏。

## 一、本轮已确认并处理的高优先级问题

### OD-01 固定八步法强制确定性

旧：QClaw 每步必须给明确一句话，最终必须给成败与具体应期。

处理：`_AGENT_INSTRUCTIONS.md` / `WORKFLOW.md` 已迁移为受约束情境推演 + Frozen Prediction + Outcome Audit。

状态：MIGRATED。

### OD-02 “古籍核查者天然更权威”

旧：师傅有古籍依据则以师傅为准。

风险：把 provenance 当 truth。

处理：`qclaw/INDEX.md` 已废弃身份权威链，改成 contextual conflict decomposition + prospective comparison。

状态：MIGRATED。

### OD-03 阳遁内外盘事实性错误

旧 `qimen-overview`、`qimen-yingqi`、`qimen-basics` 曾残留阳遁内盘 `1、3、4、9` 等错误。

当前校正版：

- 阳遁内 `1、8、3、4`，外 `9、2、7、6`；
- 阴遁反转。

状态：CORRECTED。

### OD-04 生克技能基础五行错误

旧 `qimen-shengke` 把九宫数字顺序写成“相生递进”，并出现错误五行克制关系。

处理：恢复标准五行生克；生克只作为关系结构，不自动吉凶。

状态：CORRECTED。

### OD-05 “前五/后五”与基础天干阴阳混名

旧资料把 `甲乙丙丁戊` / `己庚辛壬癸` 称“五阳/五阴”，容易与基础干支阴阳混淆。

处理：当前统一称 `FIRST_FIVE_GROUP / LAST_FIVE_GROUP`，原书若使用旧词则标 `TERMINOLOGY_CONFLICT`。

状态：CORRECTED / SOURCE WORDING STILL TO VERIFY WHEN REVISITED。

### OD-06 “四害”与“四个避开”混用

处理：`qimen-sihai` 改为状态特征识别；五不遇时等择时避开规则单列。

状态：CORRECTED。

### OD-07 入墓表内部自相矛盾

旧 `qimen-sihai` 表格与歌诀对部分墓位互相不一致。

处理：采用当前 structural baseline，同时保留流派/来源上下文，不静默覆盖。

状态：CORRECTED WITH CONTEXT CAVEAT。

### OD-08 固定用神表导致反馈后换角色

处理：改成 `Role Map Freeze`；多解预注册竞争 Role Map。

状态：MIGRATED。

### OD-09 应期“方法超市”

处理：`qimen-yingqi` 改为 timing method family freeze + frozen window + alternatives + scoring tolerance。

状态：MIGRATED。

### OD-10 固定全局优先级、凶格计分、旺衰折扣

旧：`开门>值符>生门>星神`、凶格>=3分、大凶相乘、旺相全额/休囚减半、逢空=方向待定。

处理：`CURRENT_METHOD_CONSTRAINTS.md` 全局降级/废弃；运行入口同步迁移。

状态：OVERRIDDEN；legacy monolith remains historical debt。

### OD-11 基础技能混淆“结构事实”与“传统象意”

发现六十甲子成因、生克规则、十二长生现实映射、八神高风险象意、人体医学类象、“神助”因果等问题。

处理：`qimen-basics` 重写成 `STRUCTURE / SOURCE TRADITION / CURRENT PROJECT CONSTRAINT` 三层。

状态：MIGRATED + CORRECTED。

### OD-12 “看大局”技能仍在发固定行动命令

旧 `qimen-bigpicture` 把伏吟/反吟直接翻译成守成、出击、极凶等，并含高风险古断。

处理：迁移为 Big Picture Feature Map；先识别结构，再绑定方法/角色/事类。

状态：MIGRATED。

### OD-13 VISUAL_REQUIRED 以前只有诚实阻塞，没有真正视觉交接

处理：新增 canonical PDF 原页渲染 helper 与视觉交接协议；`QM-SRC-0001` 已完成 57/57 `VISUAL_PAGE` 主审阅读，Windows renderer CI 已通过。

状态：IMPLEMENTED + PROVEN IN QM-SRC-0001 WORKFLOW。

### OD-14 qimen-gexia 把不同类型结构压成“吉格/凶格”并保留固定凶格计分

旧文件混合十干克应有序干对、复合格、结构状态、时间配置和单次失败后的量化补丁。

深查发现：

- `朱雀投江` 同文件出现 `丁+丙临坤离` 与 `丁+癸`；
- `小格` 同文件出现 `庚+壬` 与 `庚+己`；
- “三吉门会聚同宫”“三奇会聚同宫或相邻”等定义存在结构/几何上下文不清。

处理：迁移为 Pattern Registry，新增 `PATTERN_TYPE / STRUCTURE / SOURCE_PROVENANCE / APPLICABILITY / EMPIRICAL_SUPPORT / OPERATIONAL_STATUS`；十干克应保留 `(天盘干, 地盘干)` 有序方向；固定凶格计分和相乘语义退出运行层；CI 加 runtime contract。

状态：MIGRATED / SOURCE-SPECIFIC LINEAGE REVIEW STILL OPEN。

### OD-15 qimen-gongpan 把结构、象意、状态、角色、高风险应事和风水规则混成一张宫盘词典

旧文件存在：

- 九宫结构与“盗贼、丧事、疾病”等现实事件直接混写；
- 九星/八门/八神固定吉凶标签可直接进入现实判断；
- 固定 `九星→八门→八神→八卦→十干` 全局顺序；
- “吉星+吉门+吉神=大吉”等机械加总；
- “吉星旺则大吉、凶星旺则大凶”等固定状态增强语义；
- 人体、癌症、心脑血管等传统医象容易越界成医学事实；
- 风水专用 `日干=人、时干=宅` 等规则被嵌入普通宫盘全局运行；
- 主要采用白虎/玄武八神体系，未与梁书勾陈/朱雀体系分离。

进一步发现同一 legacy 文件对天蓬旺相状态互相矛盾：

- 一处写 `旺亥子、相寅卯`；
- 后一处又写 `旺寅卯、相亥子`。

处理：迁移为 Component / Relation Registry，强制拆分 `STRUCTURAL_METADATA / SOURCE_SYMBOLISM / STATE_FEATURE / ROLE_BINDING / RELATION / CONTEXTUAL_INFERENCE`；新增 `star_state_system / door_state_system` 冻结概念；八神必须先冻结 `deity_system`；高风险人物/疾病映射降为 `HIGH_RISK_SOURCE_SYMBOLISM`；风水规则降为 `METHOD_SPECIFIC_SOURCE`；新增 runtime contract。

状态：MIGRATED / SOURCE-SPECIFIC STATE-SYSTEM REVIEW STILL OPEN。

---

## 二、尚未逐文件迁移的知识债务

### P2 — qimen-qiju

重点不是“哪法最正宗”，而是：

- 拆补/置闰/茅山等定义是否准确；
- 符头、节气交接、局数边界是否存在内部不一致；
- 起局法选择必须冻结，不能结果后选盘。

### P2 — qimen-cases / qimen-cases-v2

旧案例需要重新分类：

- retrospective teaching case；
- prospective prediction；
- contaminated case；
- unscorable anecdote。

不得再用“复盘吻合”支持准确率。

### P2 — qimen-yange

歌诀文本应重 provenance，不用“多处一致”代替原典版本差异；口诀中涉及操作规则的部分需要与 K2 source lineage 对照。

---

## 三、旧《奇门遁甲知识库.md》仍是历史债务，不得误称已全修

该文件仍保留多处旧规则，例如固定全局优先级、三次即验证、凶格计分、逢空固定翻译、先读新闻及若干确定性断语。

本轮仍不无差别重写整份 monolith，因为它同时承担历史记录、来源摘记与错误修正轨迹。当前更安全的方式是 authoritative overlay + 逐技能迁移。

因此，运行时以 `CURRENT_METHOD_CONSTRAINTS.md` 为上位约束；旧知识库继续作为历史 SOURCE / migration backlog。

---

## 四、本轮方法论上的新认识

### 1. 自省必须下沉到执行层和机器 Gate

认知升级而 workflow/skill/validator 不升级，等于没有真正升级。

因此本轮不只写“不要机械”，而是把 gexia/gongpan 的旧确定性行为写入 CI runtime contract，防止后续提交悄悄恢复。

### 2. Pattern 与 Component 必须先分类，再谈象意

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION` 不能混成一个吉凶表；同理宫盘中的结构、象意、状态、Role 和关系也不能混成一层。

分类的价值是减少重复计票、跨方法污染和结果后自由切换。

### 3. “旺衰”本身也可能是方法变量

以前常把旺相休囚当成已经确定的统一状态层。本轮从同一旧技能内部就发现九星旺相算法示例冲突。

因此 `state system` 也必须像起局法、八神体系一样被显式冻结；不能结果后选择“哪套旺衰解释更合理”。

### 4. 新理论当前最大的价值仍是减少作弊自由度，不是宣称更准

当前可辩护增量包括减少：

- 反馈后换用神/方法/应期；
- 反馈后补格局；
- 同一底层结构多格名重复计票；
- 混用八神体系；
- 切换旺衰算法；
- 用高风险传统类象冒充现实事实；
- 外部信息倒算。

如果前瞻实验不改善可复现性、校准或基线表现，这套约束理论仍应降级。

### 5. “不可假读”到“可真读”的工程闭环已经打通一例

`QM-SRC-0001` 已证明 canonical hash → render → visual review → page accounting → Evidence 可行。后续 VISUAL_REQUIRED 继续复用，不再把视觉不可达当长期借口。

---

## 五、下一步顺序

当前正确顺序：

`exact-head CI`
→ `把 star_state_system / door_state_system 纳入 Prospective Registry`
→ `十八局 sparse anchors 主审复核 / IMPLEMENTATION_CHECKED`
→ `qimen-qiju P2 migration`
→ `旧案例重新分类`
→ `真实未知结果 prospective trials`

任何 source fixture、runtime contract 或 CI 通过，都只说明知识/执行约束更可靠，不得被表述为“奇门预测已经验证”。
