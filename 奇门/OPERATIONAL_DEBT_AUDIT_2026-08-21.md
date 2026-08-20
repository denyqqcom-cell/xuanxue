# 奇门运行知识债务审计 — 2026-08-21

状态：ACTIVE REVIEW

目的：记录已经认识到的问题与尚未迁移的旧知识，防止因为入口层升级就误以为整个知识库已完成纠偏。

## 一、已确认并处理的高优先级问题

### OD-01 固定八步法强制确定性
处理：`_AGENT_INSTRUCTIONS.md` / `WORKFLOW.md` 迁移为受约束情境推演 + Frozen Prediction + Outcome Audit。
状态：MIGRATED。

### OD-02 “古籍核查者天然更权威”
处理：废弃身份权威链，改 contextual conflict decomposition + prospective comparison。
状态：MIGRATED。

### OD-03 阳遁内外盘事实性错误
当前：阳遁内 `1、8、3、4`、外 `9、2、7、6`；阴遁反转。
状态：CORRECTED。

### OD-04 生克技能基础五行错误
处理：恢复标准五行生克；生克只作关系结构，不自动吉凶。
状态：CORRECTED。

### OD-05 “前五/后五”与基础天干阴阳混名
处理：运行层改称 `FIRST_FIVE_GROUP / LAST_FIVE_GROUP`；原书若用“五阳/五阴”保留并标术语冲突。
状态：CORRECTED / SOURCE WORDING TO VERIFY WHEN REVISITED。

### OD-06 “四害”与“四个避开”混用
处理：`qimen-sihai` 改状态结构识别；五不遇时等另列。
状态：CORRECTED。

### OD-07 入墓表内部自相矛盾
处理：使用当前 structural baseline，同时保留来源/流派上下文。
状态：CORRECTED WITH CONTEXT CAVEAT。

### OD-08 固定用神表导致反馈后换角色
处理：Role Map Freeze + 竞争 Role Map。
状态：MIGRATED。

### OD-09 应期“方法超市”
处理：timing method freeze + frozen window + alternatives + tolerance。
状态：MIGRATED。

### OD-10 固定全局优先级、凶格计分、旺衰折扣
旧：`开门>值符>生门>星神`、凶格>=3分、相乘、旺相全额/休囚减半、逢空=方向待定。
处理：全局降级/废弃。
状态：OVERRIDDEN；legacy monolith remains historical debt。

### OD-11 基础技能混淆结构事实与传统象意
发现六十甲子成因、生克、十二长生现实映射、八神高风险象意、人体医学、“神助”因果等问题。
处理：`qimen-basics` 三层化：STRUCTURE / SOURCE TRADITION / CURRENT PROJECT CONSTRAINT。
状态：MIGRATED + CORRECTED。

### OD-12 qimen-bigpicture 固定行动命令
处理：迁移为 Big Picture Feature Map；伏吟反吟等先识别结构，再绑定方法/角色/事类。
状态：MIGRATED。

### OD-13 VISUAL_REQUIRED 只有诚实阻塞、没有真读通路
处理：canonical PDF → render → main visual review → page accounting → Evidence；QM-SRC-0001 已 57/57 完成。
状态：IMPLEMENTED + PROVEN IN QM-SRC-0001 WORKFLOW。

### OD-14 qimen-gexia 把不同类型结构压成“吉格/凶格”
深查发现：朱雀投江两套干对、小格两套干对、三吉门/三奇会聚定义不清，且旧有固定分数/相乘。
处理：Pattern Registry；强制 `PATTERN_TYPE / STRUCTURE / SOURCE_PROVENANCE / APPLICABILITY / EMPIRICAL_SUPPORT / OPERATIONAL_STATUS`；十干克应保留有序方向；冲突不静默修正；固定凶格计分退出运行层。
状态：MIGRATED / SOURCE-SPECIFIC LINEAGE REVIEW OPEN。

### OD-15 qimen-gongpan 把结构、象意、状态、Role、高风险应事与风水规则混成词典
深查发现：固定星门神加总、固定五层优先级、人体/疾病/犯罪类象越界、风水专用规则泛化、白虎玄武与勾陈朱雀未分流，以及天蓬旺相两套相反示例。
处理：Component / Relation Registry；新增 `star_state_system / door_state_system`；八神先冻结 `deity_system`；高风险类象 SOURCE-only；runtime contract。
状态：MIGRATED / SOURCE-SPECIFIC STATE-SYSTEM REVIEW OPEN。

### OD-16 qimen-qiju 把起局法、节气处理、日界与宫序写成单一“标准流程”
深查发现：

1. 超神/接气在同一文件前后定义方向相反；
2. 拆补一处写固定 `1-5 / 6-10 / 11-15`，另一处写 `残元→中→下→补元`；
3. 拆补与茅山在旧定义下高度重叠，缺少可执行差异；
4. 子时边界一处写 `20-23`，另一处写 `23-24`；
5. 固定九宫编号被误写成“顺时针/逆时针排列”，容易让实现把宫号顺序、几何旋转、来源序列混为一谈；
6. 值使随时支“阳顺阴逆”与“八门永远顺时针转排”未拆清对象层；
7. “拆补法推荐使用/应用最广、置闰严格遵古”等权威式推荐没有经验比较依据。

处理：`qimen-qiju` 迁移为 Setup Method Registry；新增 `setup_method / time_boundary_system`；把 `setup_calibration / seasonal_alignment / time_family / layout / deity / state systems` 与 setup method 分开；冲突标 `SOURCE_INCONSISTENCY / ALGORITHM_VARIANT_REQUIRED / IMPLEMENTATION_AMBIGUITY`；Prospective Registry v1.2 纳入 `setup_method + time_boundary_system`；新增 qiju runtime contract。

状态：MIGRATED / SOURCE-SPECIFIC ALGORITHM REVIEW OPEN。

---

## 二、尚未逐文件迁移的知识债务

### P2 — qimen-cases / qimen-cases-v2

旧案例需要重新分类：

- `RETROSPECTIVE_TEACHING`
- `PROSPECTIVE_FROZEN`
- `CONTAMINATED`
- `UNSCORABLE_ANECDOTE`
- `IMPLEMENTATION_FAILURE`

不得用“复盘吻合”支持准确率；旧 success-only 选例也不能直接进入 empirical support。

### P2 — qimen-yange

歌诀文本需要 provenance/version awareness；不能用“多处一致”代替原典版本差异。涉及可执行规则的歌词必须回连 K2 source lineage。

---

## 三、旧《奇门遁甲知识库.md》仍是历史债务

仍保留固定全局优先级、三次即验证、凶格计分、逢空固定翻译、先读新闻及若干确定性断语。

不无差别重写 monolith，因为它还承担历史记录、来源摘记与错误轨迹。当前策略仍是 authoritative overlay + 逐技能迁移。

运行时以 `CURRENT_METHOD_CONSTRAINTS.md` 为上位约束；旧知识库是历史 SOURCE / migration backlog。

## 四、本轮方法论新认识

### 1. 自省必须下沉到执行层和机器 Gate

认知升级而 workflow/skill/validator 不升级，等于没有真正升级。gexia/gongpan/qiju 的旧错误都已进入 runtime-contract CI，防止后续提交悄悄恢复。

### 2. Pattern / Component / Setup 都必须先分类

有名字不等于同一类型。格局、宫盘组件、起局算法都必须先拆结构和上下文，否则“知识更丰富”只会扩大事后自由度。

### 3. 旺衰与日界都可能是模型变量

以前默认“旺衰算法”和“子时规则”是背景常识。本轮从 legacy 内部冲突证明，它们会直接改变结构或解释，所以也必须反馈前冻结。

### 4. 起局可复算比“哪法最正宗”更优先

当前首要问题不是裁决拆补/置闰/茅山谁最准，而是让每套方法变成 source-specific、可执行、可复算、可比较的算法。否则所谓准确率比较没有稳定输入。

### 5. 新理论当前最大的价值仍是减少作弊自由度

当前可辩护增量是减少：反馈后换用神、方法、setup、日界、应期、格局、八神体系、旺衰系统；减少同一结构重复计票；隔离外部信息与高风险象意。

若未来前瞻实验不改善可复现性、校准或基线表现，这套理论仍应降级。

### 6. “不可假读”到“可真读”的工程闭环已打通一例

QM-SRC-0001 已证明 canonical hash → render → visual review → page accounting → Evidence 可行。后续 VISUAL_REQUIRED 继续复用。

---

## 五、下一步顺序

`exact-head CI`
→ `十八局 sparse anchors 主审复核 / IMPLEMENTATION_CHECKED`
→ `qimen-cases / cases-v2 reclassification`
→ `qimen-yange provenance migration`
→ `真实未知结果 prospective trials`

并行 source research：逐页核验超神/接气、拆补/置闰/茅山算法差异，以及九星/八门 state systems。

任何 fixture、runtime contract 或 CI 通过都只说明知识/执行约束更可靠，不得表述为“奇门预测已经验证”。
