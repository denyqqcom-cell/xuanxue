# 奇门项目工作清单

状态：ACTIVE / 2026-08-21

适用分支：`k2-qm0001-liang-retrospective`

本清单只管理“下一步做什么”，不把完成度、CI 绿色或读书数量当成预测有效性。

## 0. 当前基线

- PR #9：Draft / open / unmerged。
- 梁湘润《奇门遁甲入门》阅读/蒸馏已 CLOSED。
- 梁书十八局：18/18 fixture 已到 `IMPLEMENTATION_CHECKED`，但范围仅限 36 个 tracked `甲子` sparse anchors。
- 善天道《奇门遁甲讲义71页》：aggregate K2 早已 `COMPLETE / 71/71 / TEXT_LAYER_FULL / 50 Evidence`；Cycle 1 又完成 supplemental visual fidelity re-audit 71/71，不重复 Reading/Evidence credit。
- `QimenEngine` 已修正 `CENTER_CHIEF_DOOR_IDENTITY`、sequence-object conflation、以及 `HIDDEN_JIA_REPRESENTATION_ERROR`。
- explicit `SHANTI_DAO_71_P21_P22` source-defined profile 与 `LEGACY_EXPERIMENTAL` 并存，不静默覆盖。
- p21-p22 两个 non-Jiazi worked plates 已有 sparse star/door/deity positive comparison。
- full-layer negative controls 已覆盖 Yang3/Yin8 wrong-bureau、Yang3 wrong-hour、以及 deterministic permuted star/door/deity labels。
- source-profile 的“值使计时正落中五宫”完整门盘仍明确 unresolved；实现返回 `SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED`，不猜测填满。
- Method Freeze 已推进到 Engine -> App -> Interpreter；K2 CI 同时跑 `:ziwei-core:test` 与 `:app:compileDebugKotlin`。
- exact head `de6caab23aeada99fb682c495518e6fed0122cec` / CI #301 = completed / success。
- 当前原创理论：`反证情境压缩法 v0.3-alpha`，状态仍为 `PROVISIONAL / UNVALIDATED / OPEN TO REJECTION`。

## 1. 工作优先级

### P0-A — 继续打穿实现边界

已完成的窄里程碑：

- [x] 梁书 18 局甲子 chief identity：36 sparse anchors + wrong-bureau/permuted controls。
- [x] 善天道 p21-p22：非甲子 full star/door/deity sparse source comparison。
- [x] 善天道 p21-p22：阳3、阴8两个 worked plates 的 source-defined `元 / 星 / 门 / 神`实现路径。
- [x] Yang3 / Yin8 wrong-bureau controls。
- [x] Yang3 wrong-hour control：保持局数，`丁巳` 对 `丙辰`，错误时辰必须丢失 sparse visual oracle 分数。
- [x] deterministic permuted star/door/deity label control：错误转位不得与正确 oracle 打平。
- [x] `PALACE_NUMBER_SEQUENCE` 与 `OUTER_ROTATION_RING` 成为不同 executable objects。
- [x] `甲时 -> 当前旬遁干 -> 地盘宫位` 的 representation transform 显式化。
- [x] App 方法选择显式化，unresolved warnings 进入 UI/Interpreter；K2 CI 增加 App compile gate。

仍未完成：

- [ ] 值使计时目标落中五宫时的 source-defined full door plate；没有独立 witness 前继续 fail closed。
- [ ] 真正的 wrong-`time_boundary_system` control；只在存在子时/午夜/节气交界的独立 source witness 时做，不拿普通时刻伪装边界实验。
- [ ] broader shuffled-full-chart controls，超出当前 outer-ring deterministic label shifts。
- [ ] alternative center-host assumption control；必须先有明确 source variant，不能凭想象造第二套算法。
- [ ] 另一独立来源对同一 non-Jiazi full-rotation 对象的交叉 implementation comparison。
- [ ] 检查更多 source-defined 时刻，避免只拟合 p21-p22 两张 worked plate。
- [ ] 每一个 PASS 继续写明 scope，不允许 sparse pass 外推 full-chart correctness。

阶段性退出条件“至少有一个非甲子、非 chief-identity 的 source-defined positive comparison，且错误输入会明确 FAIL”已达到；P0-A 本身仍未关闭。

### P0-B — 启动 clean unknown-outcome prospective pilot

第一阶段不是“证明准确率”，而是测试冻结流程能否真实运行。

- [ ] 建立首批 6 个 `PROSPECTIVE_FROZEN_CASE` protocol pilot。
- [ ] 每个 case 在反馈前完成 Baseline Firewall、method/setup/time/deity/state、Role Map、Eligible Features、primary branch/weights、失败条件、timing、auxiliary policy 冻结。
- [ ] 只选结果可公开核验、低风险、结果定义清楚的目标。
- [ ] `PREDICTIVE_AUXILIARY_FACTS` 若已看见，必须标 `PRE_EXPOSED`，不得冒充 clean method-only。
- [ ] 6-case pilot 只用于发现 protocol/implementation 漏洞，不得据此宣布理论有效。
- [ ] pilot 稳定后，再扩到至少 20 个 matched unknown-outcome cases，才开始做有意义的模型比较；20 也不是自动“验证门槛”。

当前 registry 继续允许为空。没有真实结果未知 case 时，**不为凑 6 条制造伪前瞻**。

退出条件：首批 6 个真实 case 能在不改写原预测的情况下完成 outcome audit；任何 miss 都保留。

### P0-C — Outcome-to-Rule Firewall

- [ ] 单个 HIT/MISS 只生成 `CASE_LESSON_CANDIDATE`。
- [ ] 禁止再出现“这次错了，所以以后全局 X>Y”的即时规则升级。
- [ ] 禁止 contaminated/retrospective 折算“0.5 次真验证”。
- [ ] `PARTIAL` 只按预注册评分，不换算 fractional validation credit。
- [ ] 每个候选规则必须先写：什么数据会支持、什么数据会推翻、什么条件下删除。

### P1-A — Source-specific lineage deep review

按真实 implementation/prospective failure 来决定查哪一来源，而不是按书名排队堆知识。

优先问题：

- [ ] 中宫寄宫、值符/值使、完整星门转动的来源差异。
- [ ] 拆补 / 置闰 / 茅山 / 平气定气 / 子时日界分叉。
- [ ] `勾陈/朱雀` 与 `白虎/玄武` source lineage：当前 Test C 已完成一轮比较，结论 `UNRESOLVED / NO-OP`；下一步要找更早/独立且能明确运动对象的 witness，而不是再收现代摘要。
- [ ] 九星/八门旺相休囚算法冲突。
- [ ] 十干克应天盘/地盘方向、格名异文。
- [ ] 所有“顺/逆/飞/转/移”规则必须先命名 sequence object，落实 `Sequence-Object Type Safety`。
- [ ] 所有“甲/旬首/遁干”等语言 token 到盘中 token 的转换必须显式，落实 `Representation-Object Type Safety`。

### P1-B — 反证情境压缩法 v0.3-alpha

- [ ] 用 matched prospective cases 比较“背书式”与“受约束情境推演”，不能再用 outcome-known retrospective 宣布优越。
- [ ] 检查 Role Map Freeze 是否提高分析者一致性。
- [ ] 检查 Branch-Discrimination 是否减少“任一分支命中”。
- [ ] 做 feature ablation：删除某象、某 Gate、某 context key 后，结论/校准是否变化。
- [ ] 做 `RESTRICTED vs BROAD vs SHUFFLED_SYMBOL vs SHUFFLED_ROLE_MAP`，直接测宽象意词典的 narrative-rescue capacity。
- [ ] 每次模型版本评审至少提出一个 `DELETE / MERGE / NO-OP` 候选，而不只提出新增项。

### P1-C — 旧知识债务

- [ ] 旧《奇门遁甲知识库》只做问题驱动清债，不再整本重写。
- [ ] 旧“100%命中 / 92%实战能力 / 真验证覆盖率”等表述保留历史证据，但运行层禁止复活。
- [ ] 已知错误如会影响 runtime，直接修；纯历史错误只做 correction overlay，不抹历史。
- [ ] 文档已有约束但 production 未落实时，按 `Written Knowledge != Executable Knowledge` 处理。
- [ ] validator/core-test 通过但 App/实际入口没覆盖时，按 `Tested Layer != Shipped Execution Layer` 处理。

## 2. 每轮研究时间配比

默认配比，不以“读书页数最大化”为目标：

- 45%：原页阅读 / source lineage / Evidence。
- 30%：implementation / negative controls / prospective trials。
- 15%：回看旧记录、Outcome Audit、Model Compression。
- 10%：CI、索引、状态同步、本地执行助手交接。

如果连续两轮“读书+整理”超过 70% 而没有新的 implementation/prospective test，下一轮自动降读书优先级。

当前 Cycle 1 已连续产生真实 implementation failures/controls，因此下一棒优先：

`独立 source witness -> 更强 structural negative control`

或

`真实 clean prospective pilot`

而不是为了换书而换书。

## 3. 每周检查点

每 7 天或每完成一个 book sprint，主 Agent 必须回答：

1. 本周新增的是 source knowledge、implementation fidelity，还是 empirical support？不得混写。
2. 有没有一个旧观点被降级/删除/缩窄？如果没有，检查是否只在累加。
3. 有没有真实 negative control？错误输入是否真的会输？
4. 有没有 clean unknown-outcome case 在跑？如果没有，说明为什么不是在用清债回避失败。
5. 下周最重要的问题是什么？先定义问题，再决定读哪本书。

## 4. 主 Agent 与本地 AI 分工

主 Agent：

- 决定研究问题、source identity、Evidence semantics、冲突归类、理论修改、case scoring、credit、Git 归档与是否发布。
- 负责最终视觉主审；不把 OCR/本地助手候选直接当事实。
- implementation comparison 必须把 source witness、oracle、system under test、negative control 尽量分开。

本地 AI：

- 只做 `EXECUTION_HELPER_ONLY`：同步仓库、校验 hash/page count、渲染/crop、OCR navigation、运行测试、生成 raw diff/候选 packet、收集本地输出。
- 默认不得修改 tracked files、不得 commit/push、不得给 Reading/Evidence/Empirical Support credit。
- 只有收到明确 `ONE_TIME_PERMISSION` 才可进入限定 publish scope。

详细边界见：`奇门/LOCAL_AI_EXECUTION_RUNBOOK.md`。

## 5. 书籍切换

项目不采用“读完一本马上下一本”的无限堆书模式。

统一执行：`奇门/BOOK_ROTATION_CYCLE.md`。

核心原则：

`问题驱动选书 -> 原页读透 -> 生成候选 -> 负对照/前瞻 -> 复盘压缩 -> 再换书`

而不是：

`书越多 -> 规则越多 -> 默认越接近真理`。

当前善天道 Cycle 1 已完成视觉 fidelity re-audit；Test A 已进入 A2，Test C 得到 `UNRESOLVED / NO-OP`，Test B/D 等待真实 prospective。下一本书应优先回答 **中宫寄宫 / full rotation / deity lineage / time boundary** 中的一个具体开放问题，而不是按静态队列机械切换。
