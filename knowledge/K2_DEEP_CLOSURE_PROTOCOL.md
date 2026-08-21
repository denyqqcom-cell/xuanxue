# K2 Deep Closure Protocol：从知识接收转向认知重构

版本：2026-08-21
阶段：K2B / Deep Closure
状态：ACTIVE

## 1. 目标

本阶段不再以“增加多少条 Evidence”为主要进度指标，而以以下四件事为核心：

1. 反向审查旧方法：识别因历史代码、旧 handoff、固定口诀和既有解释路径形成的路径依赖；
2. 全覆盖学习：对进入项目知识边界的来源逐页完成真实阅读，并把“来源说了什么”与“项目相信什么”彻底分开；
3. 场景化验证：任何规则都必须明确对象、问题域、适用前提、触发条件、观察层与停止条件；
4. 渐进建模：只有在多来源结构被充分吸收、冲突被显式保留、场景测试形成反馈后，才逐步形成原创模型。

Deep Closure 不等于重新发明一套术数。它首先是对旧知识管线进行约束化、可审计化和可证伪化改造。

## 2. 当前事实基线

当前分支：`knowledge-engine-v1-k2`

当前 exact HEAD：`6fb69fffb72d7f0146e09d7dc52905b1ac452fca`

最近一次针对该 exact HEAD 的 Knowledge Engine V1 CI：run #236，结论 `success`。

PR #6 保持 Draft，Claim Extraction 继续锁定。

本文件不授权自行合并 PR，也不解除 Claim Gate。

## 3. 第一阶段：历史路径反向校验

### 3.1 已确认的旧路径依赖

旧版 qimen handoff 的事实非常关键：当时盘面工程是在没有逐书重新阅读的条件下建立的。2026-08-14 handoff 明确记载：30 unique books 被盘点，但本轮独立重新阅读 PDF 的数量为 0；可用文本主要来自用户笔记，规则 36 条、fixtures 17 条，而且 full 九宫 golden board 为 0。

这意味着过去的主要风险不是“少看了一条口诀”，而是：

- 用用户笔记替代原书；
- 用规则清单替代作品内部方法结构；
- 用日历/表格 fixture 的正确性替代整个排盘系统的验证；
- 在没有完整 source reading 的情况下就试图确定地盘、天盘、门盘、神盘等 movement 规则。

### 3.2 第一类认知误区：实现先于来源

旧路径容易形成：

`代码现状 -> 寻找书证 -> 为代码找依据`

Deep Closure 改为：

`原始来源 -> Atomic Evidence -> 方法结构 -> 适用边界 -> 假设 -> 实现`

任何现有代码都只是一个待审查的历史假设，不具备来源优先权。

### 3.3 第二类误区：符号字典替代理论

旧式做法容易把：

`门/星/神/奇仪 -> 固定吉凶`

当成核心模型。

现阶段明确降级为候选特征。项目必须优先识别：

`问题域 -> 对象 -> 角色 -> 主要观察层 -> 修正条件 -> 组合关系 -> 时间/方位 -> 结论边界`

### 3.4 第三类误区：文本一致性冒充现实有效性

一本书内部说得通，只能得到“来源内部一致性”；多个来源重复，也只能增加“传统共现支持”。两者都不能直接升级成现实预测有效性。

因此以后至少分四类 credit：

- `SOURCE_CREDIT`：来源确实这样写；
- `STRUCTURAL_CREDIT`：结构/定义/算法关系经过跨页或跨源核验；
- `METHOD_CREDIT`：该方法在明确语境下具有可复述的操作逻辑；
- `EMPIRICAL_CREDIT`：经过预先冻结条件的前瞻测试后才可获得。

本阶段不允许用 `SOURCE_CREDIT` 伪装 `EMPIRICAL_CREDIT`。

### 3.5 第四类误区：案例命中替代前瞻验证

案例是来源记录，不是独立实验。任何案例都必须保留：信息是否事前、是否存在反馈、是否存在选择性解释、失败样本是否可见。

以后所有高价值假设都进入：

`FROZEN_INTERPRETATION_PATH -> PROSPECTIVE TEST -> FAILURE LOG -> MODEL UPDATE`

### 3.6 第五类误区：把“会动”压缩成一个 movement rule

完整阅读 QM-SRC-0022 后已经看到不同时间层存在不同 cadence、不同锚点和不同对象，不能用一个“阳顺阴逆”总规则覆盖所有天盘/门盘/神盘对象。

以后 movement 必须建模为：

`movement_object × temporal_context × anchor × cadence × direction × palace_path × center_policy`

## 4. 第二阶段：理论 - 边界 - 验证范式

每一条候选规则必须形成三联件：

### Theory

说明来源到底主张什么，使用来源自身术语，不能自动现代化改写。

### Boundary

至少回答：

- 对象是谁；
- 在哪个问题域；
- 哪个时间层；
- 需要哪些前置条件；
- 哪些情况不适用；
- 是否存在同源内部例外；
- 是否存在流派竞争规则。

### Validation

至少回答：

- 能否形成可执行的冻结规则；
- 能否在结果发生前记录解释路径；
- 什么算命中；
- 什么算失败；
- 能否避免反馈污染；
- 是否存在对照规则或竞争假设。

缺任一项，不得把规则提升为项目通用方法。

## 5. 第三阶段：场景化推演模型

Deep Closure 的候选总流程：

`QUESTION DOMAIN`
→ `ASKED OBJECT`
→ `OBJECT GRAPH`
→ `ROLE MAP`
→ `ELIGIBLE RULE SET FREEZE`
→ `PRIMARY / SECONDARY / CROSS-CHECK LAYERS`
→ `PALACE / STAR / DOOR / SPIRIT / QI-YI RELATIONS`
→ `WANGSHUAI / SHENGKE / EMPTY / GRAVE / XIANGCHONG 等修正`
→ `TIMING / DIRECTION / MOVEMENT CONTEXT`
→ `CONFLICT GRAPH`
→ `BOUNDARY GATE`
→ `SCENARIO CONCLUSION`

这里的核心不是让模型变得更复杂，而是禁止在结果出现后再自由选择解释路径。

## 6. Dynamic Role Map

继续沿用但正式升级为项目级一等结构：

`Question Domain -> Asked Object -> Query Order -> Primary Role -> Secondary Role -> Cross-check Role`

不同问题不能共享一个固定用神优先级表。

至少要求：

- 人事问题先确定“谁是对象”；
- 财务问题先确定“钱、主体、来源、结果”的对象关系；
- 风水问题先区分环境、空间、使用者和目标结果；
- 失物问题先确定失物与搜索行为，而不是直接读取“凶门”；
- 时间问题必须把“何时发生”与“事情吉凶”分开。

这些都是候选架构，不是已证明的预测真理。

## 7. Eligible Rule Set Freeze

来源库有一条规则，不代表当前盘有资格调用它。

每次解盘前必须冻结：

1. 本题问题域；
2. 允许使用的方法族；
3. 主信息层；
4. 辅助信息层；
5. 禁止调用的规则族；
6. 反馈后不得新增的解释通道。

禁止“先看到结果，再搜索最像的口诀”。

## 8. 八神 ontology 重构规则

不得把所有包含“神”的对象扁平化成一个集合。

至少保持以下层级独立：

- 八神；
- 九头神；
- 神煞系统；
- 神遁/鬼遁等方法名称中的“神”；
- 来源中特定功能身份，如天乙与值符的关系。

来源明确使用什么名称，就保留什么名称。跨来源建立同义/功能映射时必须保存原始术语，不允许静默标准化。

## 9. 中宫重构规则

“存在中宫”与“所有对象都经过中宫”是两个不同命题。

当前只允许建立：

`CENTER_PALACE_EXISTS`
`CENTER_NUMBER_RELATION`
`CENTER_FIVE_EARTH_RELATION`

具体的寄宫、转入、停留、排布经过规则必须逐来源确认。

在没有足够来源证据前，不得把单一流派的中五寄宫方式升级成全局规则。

## 10. Movement Ontology

所有 movement 规则必须拆成：

- `object`
- `temporal_context`
- `anchor`
- `cadence`
- `direction`
- `path`
- `center_policy`
- `school_context`

特别注意：

`YEAR_QI / MONTH_QI / DAY_QI / HOUR_QI`

可能具有不同的移动节律。一个对象“会移动”并不足以定义其移动算法。

## 11. 学习覆盖策略

K2B 的“全覆盖”必须理解为：

`所有纳入项目知识边界的 K2-eligible unique work families，都必须最终得到真实阅读状态。`

不是：

`Evidence 条数越多越好。`

优先级：

1. 原始/早期文本；
2. 同一作品的完整上下册/中册；
3. 能揭示排布结构和方法差异的来源；
4. 现代系统化教材；
5. 案例汇编与直断材料。

案例型现代书可以提供场景拓扑，但不能替代基础文本。

## 12. 当前书籍替换政策

当前不建议立刻替换现有 Wave1 书目。

原因：现有库已经包含古典文本、现代教材、案例型材料以及不同阶段的系统讲义，当前主要问题是“尚未完成全覆盖与重新校验”，不是“书不够多”。

当前上传来源中，后续应优先完成：

- `QM-SRC-0023`《甲遁真授秘录》下册：与 0022 同一作品，必须完成闭环；
- `QM-SRC-0024`《笺元遁甲句解烟波钓叟歌》：作为传统核心文本的独立锚点；
- `QM-SRC-0025/0026`《金函玉镜奇门遁甲秘笈全书》上下册：必须按同一 work family 读取，避免双重计票；
- 曾子南三册作为一个 work family 处理；
- 善天道系列的不同版本作为同源/同课变体处理，不得独立投票。

只有出现以下条件之一才应更换/补充书籍：

1. 来源确认是纯二手笔记而非原始文本；
2. 已确认是同一作品的重复载体；
3. 内容只提供大量静态断语，无法增加结构理解；
4. 出现更可靠、可核验的早期/原始文本，可以显著提高 lineage 或结构辨识度。

因此当前结论：**暂不要求用户换书；先完成现有核心 corpus 的闭环。**

## 13. 本地 AI 协助边界

本阶段原则不变：

`EXECUTION_HELPER_ONLY`

本地 AI 可以：

- 定位 canonical PDF；
- 核验 SHA256；
- 逐页生成 page packet；
- 提取原有文字层；
- 汇报页码/页数/视觉可用性；
- 运行项目现有 validator/test；
- 对已锁定的页区做机械分页输出。

本地 AI 不得：

- 自己总结正式 Evidence；
- 自己判断作者；
- 自己判断 lineage；
- 自己确定规则是否正确；
- 自己修改 tracked knowledge；
- 自己 commit/push；
- 用关键词搜索替代逐页阅读。

## 14. 本地 AI 深度闭关提示词

下面提示词只允许机械执行，不允许它成为最终知识判断者：

```text
你是 Xuanxue 奇门知识工程的 EXECUTION_HELPER_ONLY。

任务目标：协助 PROJECT_MAIN_AGENT 完成指定 canonical PDF 的逐页阅读准备与原始证据暴露，不做术理裁决。

硬约束：
1. 不得跳页，不得以关键词搜索替代连续阅读；
2. 不得根据旧 handoff、旧规则或代码猜测页面内容；
3. 不得自行判断作者、domain、lineage、流派归属或规则正确性；
4. 不得把自己的摘要写成正式 Atomic Evidence；
5. 不得修改 tracked knowledge，不得 commit，不得 push；
6. 每页必须保留 PDF page number；
7. 只能报告页面原文/图像中实际可见的信息；看不清必须报告 BLOCKED/UNCLEAR；
8. TEXT_DIRECT 只暴露原有文字层；VISUAL_REQUIRED 必须诚实报告视觉可用性；
9. 不得 OCR 成功即视为语义正确；
10. 不得把案例当成验证结果。

输出格式：
SOURCE_ID:
PDF_TOTAL_PAGES:
PAGE_RANGE:
EXECUTION_LANE:
TEXT_LAYER_STATUS:
VISUAL_STATUS:
CANONICAL_SHA256:

PAGE_PACKET:
- pdf:pXX
  - visible_text: ...
  - diagrams/tables: ...
  - names/titles: ...
  - uncertain: ...

END_PACKET
```

## 15. Deep Closure 出口条件

在以下条件完成前，不进入 Claim Extraction：

- Wave1 选定 coverage 完成或诚实 BLOCKED；
- 关键 qimen work families 已完成 Reading Ledger；
- 每个 COMPLETE source 有对应 Book Distillate；
- 作者、domain、lineage 的关键异常完成回溯修正；
- 八神、中宫、movement 等 ontology 不再依赖单一书本；
- 冲突由“真假二选一”升级为对象/层级/时间/流派可分解的 Conflict Graph；
- 建立至少一批冻结场景测试；
- 对测试失败的规则建立 failure log；
- 任何所谓“有效”结论都有明确的 validation basis。

## 16. 原创理论的渐进形成

当前不宣布任何“新奇门理论”已经成立。

只允许形成以下类型的研究假设：

`H1：奇门判断的基本单位不是单一符号，而是“情境中的对象关系”。`

`H2：同一符号在不同问题域、时间层和角色映射下，其解释权重并不固定。`

`H3：movement 是对象状态转移问题，而不是统一的顺逆规则。`

`H4：解释质量的关键之一是提前冻结信息选择路径，而不是事后提高象意覆盖率。`

这些只是待验证假设。

最终目标不是取代古籍，而是在完整吸收、明确边界、持续测试后，形成一个能解释“为什么在这个场景应该看这些信息、为什么那些信息此时不应参与”的约束化推演模型。
