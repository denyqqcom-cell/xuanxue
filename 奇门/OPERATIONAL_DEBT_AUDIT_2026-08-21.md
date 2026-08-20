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

旧 `qimen-overview`、`qimen-yingqi`：阳遁内盘写成 `1、3、4、9`，外盘 `2、6、7、8`。

项目已校正版：

- 阳遁内 `1、8、3、4`，外 `9、2、7、6`；
- 阴遁反转。

处理：两技能已直接修正。

状态：CORRECTED。

### OD-04 生克技能基础五行错误

旧 `qimen-shengke` 把九宫数字顺序写成“相生递进”，并出现“离火克艮土”“坎水克坤/艮”等错误。

处理：重写基础关系表，恢复 `木→火→土→金→水→木` 和标准五行相克；生克只作为关系结构，不自动吉凶。

状态：CORRECTED。

### OD-05 善天道“前五/后五”与基础天干阴阳混名

旧：把 `甲乙丙丁戊` 称“五阳干”，`己庚辛壬癸` 称“五阴干”。

风险：与基础天干阴阳 `甲丙戊庚壬 / 乙丁己辛癸` 混淆。

处理：将前五/后五保留为善天道特定主客分组，并标 `TERMINOLOGY_CONFLICT`，不再冒充基础干支阴阳事实。

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

### OD-10 固定全局优先级、凶格计分、旺衰折扣等

旧：`开门>值符>生门>星神`、凶格>=3分、大凶相乘、旺相全额/休囚减半、逢空=方向待定。

处理：`CURRENT_METHOD_CONSTRAINTS.md` 全局降级/废弃；`qimen-overview` 执行入口同步迁移。

状态：OVERRIDDEN；legacy KB remains historical debt。

---

## 二、尚未逐文件迁移的知识债务

以下文件仍可能含确定性古断、未验证吉凶、旧 Role Map 或高风险现实推断。入口层已通过 `CURRENT_METHOD_CONSTRAINTS.md` 约束它们，但文件本体尚未全部重写。

### P1 — qimen-basics

已观察风险：

- 传统天干合化象意直接写成人格/婚恋现实结论；
- 十二状态直接映射“外遇、事业兴旺、老年旺极而折”等；
- “前五/后五”主客术语与基础阴阳潜在混淆；
- 五脏等传统映射容易被误当医学事实。

处理计划：保留基础结构，所有象意改 SOURCE；高风险现实结论增加非经验支持边界。

### P1 — qimen-bigpicture

已观察风险：

- 伏吟“利主”、反吟“利客”等写成固定动作建议；
- 星门俱伏吟“极凶”等传统标签可越过事类；
- 健康/婚姻等场景存在直接高风险断语。

处理计划：改为大局 feature map，不自动行动策略。

### P1 — qimen-gexia

预期风险：

- 吉格/凶格等级表容易被直接裁决；
- 十干克应在不同来源中可能有名词、方向、上下盘差异；
- 同一格名的 source lineage 需要重新核查。

处理计划：Pattern Registry 化：结构、来源、适用域、传统断语、empirical support 分列。

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

本轮选择**不直接重写整份 monolith**，原因：

1. 它同时承担历史记录、来源摘记、错误修正轨迹；
2. 大规模无差别重写容易丢失 provenance；
3. 当前更安全的方式是建立 authoritative overlay，并逐技能迁移。

因此，运行时以 `CURRENT_METHOD_CONSTRAINTS.md` 为上位约束；旧知识库继续作为历史 SOURCE / migration backlog。

这不是“问题解决了”，而是“问题被隔离并进入显式债务队列”。

---

## 四、本轮方法论上的新认识

### 1. 自省不能只写日志，要下沉到执行层

过去多次在修炼日志里已经认识到“不要盲信、不要机械”，但 QClaw 的 Agent Instruction 仍要求固定八步、明确吉凶、古籍师傅优先。

这说明：

**认知升级而运行协议不升级 = 实际上没有升级。**

### 2. 纠错不能只纠“玄学知识”，还要纠普通逻辑和基础事实

本轮最值得警惕的不是某个门派口诀，而是：

- 九宫数字顺序被当成五行相生；
- 火土关系写错；
- 内外盘宫位已经在日志纠正，却在两个运行技能继续错。

这说明旧系统存在“修炼日志修过，执行文件没同步”的长期结构病。

### 3. 新理论的首要创新不是更会断，而是更难作弊

`受约束情境推演法 v0.2-alpha` 当前最大的价值不是提高准确率——这还没有证据——而是减少：

- 反馈后换用神；
- 反馈后换方法；
- 反馈后选应期；
- 叙事后见；
- 外部信息倒算。

如果未来实验表明这些约束并不能带来更好或更可校准的预测，该理论也应被降级。

---

## 五、下一步顺序

在梁湘润 `QM-SRC-0001` 原始视觉页尚未进入当前执行环境时，不得伪造 57/57 Reading Credit。

等待视觉源期间，正确的内部顺序是：

`高优先级运行债务清理 -> CI -> 梁书视觉源可达 -> 57/57 Visual Reading -> Atomic Evidence -> Book Distillate -> Method Delta -> Prospective Tests`

本文件会随下一轮运行债务清理继续更新，不因本轮修了几个入口文件就宣布“旧系统已全部纠正”。
