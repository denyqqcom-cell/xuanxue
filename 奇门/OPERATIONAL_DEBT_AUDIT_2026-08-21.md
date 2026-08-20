# 奇门运行知识债务审计 — 2026-08-21

状态：ACTIVE REVIEW

目的：记录“已经认识到的问题”和“尚未完成迁移的旧知识”，防止因为入口层升级就误以为整个奇门知识库已经完成纠偏。

## 一、本轮已确认并处理的高优先级问题

### OD-01 固定八步法强制确定性

旧：QClaw 每步必须给明确一句话，最终必须给成败与具体应期。

风险：证据不足也会被格式逼着造答案；多流派规则无限叠加。

处理：`_AGENT_INSTRUCTIONS.md` / `WORKFLOW.md` 已迁移为受约束情境推演 + Frozen Prediction + Outcome Audit。

状态：MIGRATED。

### OD-02 “古籍核查者天然更权威”

旧：师傅有古籍依据则以师傅为准。

风险：把 provenance 当 truth；后一层只因引用古书就可以覆盖前一层。

处理：`qclaw/INDEX.md` 已废弃身份权威链，改成 contextual conflict decomposition + prospective comparison。

状态：MIGRATED。

### OD-03 阳遁内外盘事实性错误

旧 `qimen-overview`、`qimen-yingqi`、`qimen-basics` 曾残留阳遁内盘 `1、3、4、9` 等错误。

当前校正版：

- 阳遁内 `1、8、3、4`，外 `9、2、7、6`；
- 阴遁反转。

处理：overview / yingqi / basics 已修正；bigpicture 保留同一校正版。

状态：CORRECTED。

### OD-04 生克技能基础五行错误

旧 `qimen-shengke` 把九宫数字顺序写成“相生递进”，并出现“离火克艮土”“坎水克坤/艮”等错误。

处理：重写基础关系表，恢复 `木→火→土→金→水→木` 和标准五行相克；生克只作为关系结构，不自动吉凶。

状态：CORRECTED。

### OD-05 “前五/后五”与基础天干阴阳混名

旧资料把 `甲乙丙丁戊` 称“五阳”，`己庚辛壬癸` 称“五阴”，容易与基础干支阴阳 `甲丙戊庚壬 / 乙丁己辛癸` 混淆。

处理：当前统一称 `FIRST_FIVE_GROUP / LAST_FIVE_GROUP`，作为特定主客方法分组；若原书确实使用“五阳/五阴”则保留原词并标 `TERMINOLOGY_CONFLICT`。

状态：CORRECTED / SOURCE WORDING STILL TO VERIFY PAGE-VISUALLY WHEN REVISITED。

### OD-06 “四害”与“四个避开”混用

旧 `qimen-sihai` 将空亡、入墓、击刑、门迫称“四害”，同时引用善天道“四个避开”作为直接来源。

历史 8/7 自查已确认两者不是同一概念。

处理：技能改为状态特征识别；五不遇时等择时避开规则单列。

状态：CORRECTED。

### OD-07 入墓表内部自相矛盾

旧 `qimen-sihai` 中表格与歌诀对庚、辛、壬、癸墓位存在互相不一致；验证标准本身不稳定。

处理：当前采用 `qimen-basics` 十干十二状态表作为 structural baseline，同时明确这是当前项目 baseline，不把其他流派差异静默覆盖。

状态：CORRECTED WITH CONTEXT CAVEAT。

### OD-08 固定用神表导致反馈后换角色

旧 `qimen-yongshen`：日干“任何时候都用”、年命“更精确”、十大事项固定主用神。

处理：改成 `Role Map Freeze`，所有角色记录 SOURCE_DEFINED / METHOD_DEFINED / CONTEXT_INFERRED；多解预注册竞争 Role Map。

状态：MIGRATED。

### OD-09 应期“方法超市”

旧：空亡、马星、墓库、冲合、值使数字、地盘干、外应都可调用。

风险：结果后总能挑一个最接近日期的规则。

处理：`qimen-yingqi` 改为 timing method family freeze + frozen window + alternatives + scoring tolerance。

状态：MIGRATED。

### OD-10 固定全局优先级、凶格计分、旺衰折扣

旧：`开门>值符>生门>星神`、凶格>=3分、大凶相乘、旺相全额/休囚减半、逢空=方向待定。

处理：`CURRENT_METHOD_CONSTRAINTS.md` 全局降级/废弃；`qimen-overview` 执行入口同步迁移。

状态：OVERRIDDEN；legacy monolith remains historical debt。

### OD-11 基础技能混淆“结构事实”与“传统象意”

继续深查 `qimen-basics` 又发现：

- 把天干相生写成仅“阴生阳/阳生阴”、相克写成“阳克阳/阴克阴”，若作完整生克规则则错误；
- 把“10天干 × 12地支 = 60种组合”当作六十甲子成因，混淆笛卡尔积与干支同步循环；
- 十二长生直接映射外遇、疾病、老年旺极而折；
- 地支刑冲合害直接翻译固定吉凶；
- 八神类象直接贴车祸、死亡、盗窃等现实事件；
- 五脏/人体类象容易被误当医学事实；
- “神助”层写得像客观因果机制。

处理：`qimen-basics` 已重写成 `STRUCTURE / SOURCE TRADITION / CURRENT PROJECT CONSTRAINT` 三层，修复六十甲子与生克基础表述，把人体、人格、吉凶类象降回 SOURCE/CANDIDATE。

状态：MIGRATED + CORRECTED。

### OD-12 “看大局”技能仍在发固定行动命令

旧 `qimen-bigpicture`：

- 伏吟=利主/守成；
- 反吟=利客/出击；
- 星门俱伏吟=极凶；
- 天显时格可把伏吟直接反转为吉；
- 反吟婚姻破裂、久病逢之死等高风险古断可直接进入运行；
- 日干/时干生克未先绑定 Role Map。

处理：改为 Big Picture Feature Map。伏吟/反吟只先识别结构；主客、动静、快慢、天显例外均作为 METHOD/SOURCE 候选；高风险断语失去直接运行资格。

状态：MIGRATED。

### OD-13 VISUAL_REQUIRED 的执行瓶颈以前只有“诚实阻塞”，没有可用视觉交接

旧本地 helper 能正确对 VISUAL_REQUIRED 返回 `VISION_UNAVAILABLE`，但无法把 canonical SCAN 转成主审可逐页查看的图像，因此“不可假读”做到了，“如何真读”还没打通。

处理：新增 `build_k2_visual_page_packet.py`、独立依赖与 Windows fail-closed 测试；只渲染 canonical PDF 原页，不 OCR，不赋 Reading Credit；新增 `K2_VISUAL_PAGE_HANDOFF_PROTOCOL.md`。`QM-SRC-0001` 已按 canonical SHA 完成 57/57 `VISUAL_PAGE` 主审阅读，且 Windows visual renderer CI 已通过。

状态：IMPLEMENTED + PROVEN IN QM-SRC-0001 WORKFLOW。

### OD-14 qimen-gexia 把不同类型结构压成“吉格/凶格”并保留固定凶格计分

旧 `qimen-gexia` 同时混入：

- 十干克应有序干对；
- 三奇/门/神复合格；
- 伏吟、反吟、门迫、入墓、击刑等结构状态；
- 五不遇时、天显时格等时间配置；
- 多来源传统断语；
- `>=3分直接大凶`、`>=5分极凶`、凶格叠加相乘等单次失败后形成的量化补丁。

深查还发现至少三类内部问题：

1. `朱雀投江` 同文件出现 `丁+丙临坤离` 与 `丁+癸` 两种定义；
2. `小格` 同文件出现 `庚+壬` 与 `庚+己` 两种组合；
3. “三吉门会聚同宫”“三奇会聚同宫或相邻”等定义与普通标准盘结构或几何条件不清，不能直接运行。

处理：`qimen-gexia` 迁移为 Pattern Registry。新增 `PATTERN_TYPE / STRUCTURE / SOURCE_PROVENANCE / APPLICABILITY / EMPIRICAL_SUPPORT / OPERATIONAL_STATUS`；十干克应强制保留 `(天盘干, 地盘干)` 有序方向；伏吟/反吟、空墓刑迫、五不遇时等路由回专门结构技能；内部冲突保留为 `CONFLICT_CANDIDATE / DEFINITION_UNRESOLVED`；固定凶格计分和相乘语义退出运行层。

状态：MIGRATED / SOURCE-SPECIFIC LINEAGE REVIEW STILL OPEN。

---

## 二、尚未逐文件迁移的知识债务

### P1 — qimen-gongpan

预期风险：

- 星门神传统吉凶标签可能直接映射现实事件；
- 九宫人体内容属于高风险传统医学象，必须明确非医学证据；
- 固定宫内分析顺序需要与 Method-Family Priority 对齐。

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

该文件仍保留多处旧规则，例如：

- `>=3次独立真验证=已验证门槛`；
- 固定 `开门>值符>生门>星神`；
- 凶格相乘与固定分数；
- `逢空=方向待定`；
- “查>=3条新闻再看盘”；
- 若干“必得利/大凶”等书本断语。

本轮仍选择**不直接无差别重写整份 monolith**，因为它同时承担历史记录、来源摘记与错误修正轨迹。当前更安全的方式是 authoritative overlay + 逐技能迁移。

因此，运行时以 `CURRENT_METHOD_CONSTRAINTS.md` 为上位约束；旧知识库继续作为历史 SOURCE / migration backlog。

这不是“问题解决了”，而是“问题被隔离并进入显式债务队列”。

---

## 四、本轮方法论上的新认识

### 1. 自省不能只写日志，要下沉到执行层

过去日志已经多次写“不要盲信、不要机械”，但运行协议仍会要求固定步骤、固定吉凶、古籍权威优先。

**认知升级而运行协议不升级 = 实际上没有升级。**

### 2. 纠错不能只纠玄学口诀，还要纠普通逻辑和基础事实

本轮连续抓到：

- 九宫数字顺序被当五行相生；
- 火土、水土基础关系写错；
- 10×12 被误写成 60 种干支组合；
- 内外盘已在日志校正但运行技能继续错；
- 基础天干阴阳与门派主客分组混名；
- “三个不同八门同宫”一类结构条件未经检查就被登记为格局；
- 同一文件对同名十干克应给出互相冲突的有序干对。

这说明“玄学难验证”不能成为基础逻辑错误的遮羞布。越是术数体系，越要先把普通可核对事实做对。

### 3. Pattern 必须先分类，再谈象意

旧做法把所有“有名字的东西”都叫格局，再贴一个吉凶等级。现在至少区分：

`STEM_PAIR_PATTERN / COMPOSITE_PATTERN / STRUCTURAL_STATE / TIME_CONFIGURATION / METHOD_SPECIFIC_PATTERN`

分类的价值不是美观，而是减少错误调用：状态结构不应被当成十干克应重复计分，时间配置也不应在结果后作为额外“凶格票”叠加。

### 4. 新理论当前最大的价值仍不是“更准”，而是“更难事后作弊”

`受约束情境推演法 v0.2-alpha` 目前没有资格宣称提高预测准确率。它当前真正可辩护的增量是减少：

- 反馈后换用神；
- 反馈后换方法；
- 反馈后选应期；
- 反馈后补格局；
- 同一底层结构用多个格名重复计票；
- 叙事后见；
- 外部信息倒算。

若未来实验显示这些约束并没有带来更可复现、更可校准或更优于基线的结果，该理论也应被降级。

### 5. “不可假读”之后还必须解决“怎样真读”

`QM-SRC-0001` 已证明 canonical hash → 原页渲染 → 主审逐页视觉阅读 → page accounting → Evidence 的闭环可行。

下一阶段不再把“视觉不可达”当作当前梁书 blocker，而是继续把这一套 transport/review 分权机制复用于后续 VISUAL_REQUIRED source。

---

## 五、下一步顺序

当前 `QM-SRC-0001` 已完成 57/57 阅读、Evidence、Book Distillate、Method Delta、Prospective Test Plan，并建立十八局 fixture index 与 Prospective Case Registry。

当前正确顺序：

`exact-head CI`
→ `qimen-gongpan P1 migration`
→ `十八局 sparse anchors 主审复核 / IMPLEMENTATION_CHECKED`
→ `qimen-qiju P2 migration`
→ `旧案例重新分类`
→ `真实未知结果 prospective trials`

任何 source fixture、runtime contract 或 CI 通过，都只说明知识/执行约束更可靠，不得被表述为“奇门预测已经验证”。
