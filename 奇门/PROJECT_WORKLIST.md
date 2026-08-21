# 奇门项目工作清单

状态：ACTIVE / 2026-08-21

适用分支：`k2-qm0001-liang-retrospective`

本清单只管理“下一步做什么”，不把完成度、CI 绿色、读书数量或理论版本号当成预测有效性。

## 0. 当前基线

- PR #9：Draft / open / unmerged。
- 梁湘润《奇门遁甲入门》阅读/蒸馏已 CLOSED。
- 梁书十八局：18/18 fixture 已到 `IMPLEMENTATION_CHECKED`，但范围仅限 tracked `甲子` sparse anchors，不外推 full-chart correctness。
- 善天道《奇门遁甲讲义71页》：aggregate K2 早已 `COMPLETE / 71/71 / TEXT_LAYER_FULL / 50 Evidence`；Cycle 1 又完成 supplemental visual fidelity re-audit 71/71，不重复 Reading/Evidence credit。
- `QimenEngine` 已修正 `CENTER_CHIEF_DOOR_IDENTITY`、sequence-object conflation、以及 `HIDDEN_JIA_REPRESENTATION_ERROR`。
- explicit `SHANTI_DAO_71_P21_P22` source-defined profile 与 `LEGACY_EXPERIMENTAL` 并存，不静默覆盖。
- p21-p22 两个 non-Jiazi worked plates 已有 sparse star/door/deity positive comparison。
- full-layer negative controls 已覆盖 Yang3/Yin8 wrong-bureau、Yang3 wrong-hour、以及 deterministic permuted star/door/deity labels。
- `QM-SRC-0021 / 幺学声《奇门遁甲预测学》` p54/p57/p69-p72 已做 targeted original-page visual review；其中一组 2004-05-29 午时 worked plate 已作为独立 cross-source sparse implementation witness。
- cross-source test 进入 `ziwei-core`；verified implementation milestone `12e124aa51419030a7f9d07864c2d5e5ce497091` / Knowledge Engine V1 CI #304 = completed / success。
- 这只增加 `SELECTED_CROSS_SOURCE_IMPLEMENTATION_AGREEMENT`，不增加 Empirical Support。
- source-profile 的“值使计时正落中五宫”完整门盘仍明确 unresolved；实现返回 `SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED`，不猜测填满。
- Method Freeze 已推进到 Engine -> App -> Interpreter；K2 CI 同时跑 `:ziwei-core:test` 与 `:app:compileDebugKotlin`。
- 当前原创理论：`反证情境压缩法 v0.3-alpha`，状态仍为 `PROVISIONAL / UNVALIDATED / OPEN TO REJECTION`。
- 新增闭关校准：`情境不是答案`；研究自由度拆为 `MODEL_DOF / SELECTION_DOF / STOPPING_DOF`；旧规则执行 `No Grandfathering`。
- `RESEARCH_ATTACK_QUEUE.md` 作为轻量选择偏差实验，不是新评分表；如果不能减少 cherry-picking，应删除。

## 1. 工作优先级

### P0-A — 继续打穿实现边界

已完成的窄里程碑：

- [x] 梁书 18 局甲子 chief identity：sparse anchors + wrong-bureau/permuted controls。
- [x] 善天道 p21-p22：非甲子 full star/door/deity sparse source comparison。
- [x] 善天道 p21-p22：阳3、阴8两个 worked plates 的 source-defined `元 / 星 / 门 / 神`实现路径。
- [x] Yang3 / Yin8 wrong-bureau controls。
- [x] Yang3 wrong-hour control：保持局数，`丁巳` 对 `丙辰`，错误时辰必须丢失 sparse visual oracle 分数。
- [x] deterministic permuted star/door/deity label control：错误转位不得与正确 oracle 打平。
- [x] `PALACE_NUMBER_SEQUENCE` 与 `OUTER_ROTATION_RING` 成为不同 executable objects。
- [x] `甲时 -> 当前旬遁干 -> 地盘宫位` 的 representation transform 显式化。
- [x] App 方法选择显式化，unresolved warnings 进入 UI/Interpreter；K2 CI 增加 App compile gate。
- [x] `QM-SRC-0021` targeted visual witness：不修改善天道 profile 算法的前提下，对独立现代 worked plate 做 sparse cross-source implementation comparison。

仍未完成：

- [ ] 值使计时目标落中五宫时的 source-defined full door plate；没有独立 witness 前继续 fail closed。
- [ ] 真正的 wrong-`time_boundary_system` control；只在存在子时/午夜/节气交界的独立 source witness 时做，不拿普通时刻伪装边界实验。
- [ ] broader shuffled-full-chart controls，超出当前 outer-ring deterministic label shifts。
- [ ] alternative center-host assumption control；必须先有明确 source variant，不能凭想象造第二套算法。
- [ ] 再找至少 1 个可能**反对**而不只是支持当前 full-rotation profile 的独立 worked-plate witness。
- [ ] 检查更多 source-defined 时刻，避免只拟合少数 worked plates。
- [ ] 每一个 PASS 继续写明 scope，不允许 sparse pass 外推 full-chart correctness。

阶段性退出条件“至少有一个非甲子、非 chief-identity 的 source-defined positive comparison，且错误输入会明确 FAIL”已达到；P0-A 本身仍未关闭。

### P0-B — 启动 clean unknown-outcome prospective pilot

第一阶段不是“证明准确率”，而是测试冻结流程能否真实运行。

- [ ] 建立首批 6 个 `PROSPECTIVE_FROZEN_CASE` protocol pilot。
- [ ] 每个 case 在反馈前完成 Baseline Firewall、method/setup/time/deity/state、Role Map、Eligible Features、primary branch/weights、失败条件、timing、auxiliary policy 冻结。
- [ ] 只选结果可公开核验、低风险、结果定义清楚的目标。
- [ ] `PREDICTIVE_AUXILIARY_FACTS` 若已看见，必须标 `PRE_EXPOSED`，不得冒充 clean method-only。
- [ ] 6-case pilot 只用于发现 protocol/implementation 漏洞，不得据此宣布理论有效。
- [ ] pilot 稳定后，再扩到 matched unknown-outcome cases 才做模型比较；样本数/时间窗/停止条件必须开始前声明，不能赢了就停、输了就无限追加。

当前 registry 继续允许为空。没有真实结果未知 case 时，**不为凑 6 条制造伪前瞻**。

退出条件：首批真实 case 能在不改写原预测的情况下完成 outcome audit；任何 miss 都保留。

### P0-C — Outcome-to-Rule Firewall

- [ ] 单个 HIT/MISS 只生成 `CASE_LESSON_CANDIDATE`。
- [ ] 禁止再出现“这次错了，所以以后全局 X>Y”的即时规则升级。
- [ ] 禁止 contaminated/retrospective 折算“0.5 次真验证”。
- [ ] `PARTIAL` 只按预注册评分，不换算 fractional validation credit。
- [ ] 每个候选规则必须先写：什么数据会支持、什么数据会推翻、什么条件下删除。

### P0-D — Research Selection / Stopping Freedom

目标：防止“每个 case 内都守规矩，但研究组合本身 cherry-pick”。

- [ ] 试运行 `RESEARCH_ATTACK_QUEUE.md`：查来源/做测试前先写攻击理由，而不是看到结果后补动机。
- [ ] PASS / FAIL / NO-OP / UNRESOLVED 都保留。
- [ ] source selection 优先找能证明当前模型错的页/实例，不连续只读支持材料。
- [ ] matched comparison 在开始前声明停止条件；禁止 favourable stopping。
- [ ] 一轮后复盘 Attack Queue 是否真的减少选择偏差；若只是新增 paperwork，直接 `DELETE / NO-OP`，不升级成 Gate。

### P1-A — Source-specific lineage deep review

按真实 implementation/prospective failure 来决定查哪一来源，而不是按书名排队堆知识。

优先问题：

- [ ] 中宫寄宫、值符/值使、完整星门转动的来源差异。
- [ ] 拆补 / 置闰 / 茅山 / 平气定气 / 子时日界分叉。
- [ ] `勾陈/朱雀` 与 `白虎/玄武` source lineage：当前 Test C `UNRESOLVED / NO-OP`；下一步优先更早/独立且能明确运动对象的 witness，而不是再收现代摘要。
- [ ] 九星/八门旺相休囚算法冲突。
- [ ] 十干克应天盘/地盘方向、格名异文。
- [ ] 所有“顺/逆/飞/转/移”规则必须先命名 sequence object，落实 `Sequence-Object Type Safety`。
- [ ] 所有“甲/旬首/遁干”等语言 token 到盘中 token 的转换必须显式，落实 `Representation-Object Type Safety`。
- [ ] 古籍 OCR 仅可做导航：关键词命中必须回原页确认，不能把 OCR 伪命中直接当 lineage evidence。

### P1-B — 反证情境压缩法 v0.3-alpha

- [ ] 用 matched prospective cases 比较“背书式”与“受约束情境推演”，不能再用 outcome-known retrospective 宣布优越。
- [ ] 把“情境给答案”彻底废弃：情境只冻结角色、对象和语义边界；情境越具体，允许的解释空间应该越窄而不是越宽。
- [ ] 检查 Role Map Freeze 是否提高分析者一致性。
- [ ] 检查 Branch-Discrimination 是否减少“任一分支命中”。
- [ ] 做 feature/context ablation：删除某象、某 Gate、某 context key 后，结论/校准是否变化。
- [ ] 做 `RESTRICTED vs CONTEXT_FROZEN_RELATIONAL vs BROAD_CONTEXT vs SHUFFLED_SYMBOL / SHUFFLED_ROLE_MAP`，直接测情境转译与宽象意的 narrative-rescue capacity。
- [ ] 每次模型版本评审至少提出一个 `DELETE / MERGE / NO-OP` 候选，而不只提出新增项。
- [ ] 不因本轮闭关自省升级 v0.4；只有独立 source conflict、implementation failure、negative-control 或 clean prospective result 真正改变 operational claim 才考虑升版。

### P1-C — 旧知识债务 / No Grandfathering

- [ ] 旧《奇门遁甲知识库》只做问题驱动清债，不再整本重写。
- [ ] 旧“100%命中 / 92%实战能力 / 真验证覆盖率”等表述保留历史证据，但运行层禁止复活。
- [ ] 已知错误如会影响 runtime，直接修；纯历史错误只做 correction overlay，不抹历史。
- [ ] 文档已有约束但 production 未落实时，按 `Written Knowledge != Executable Knowledge` 处理。
- [ ] validator/core-test 通过但 App/实际入口没覆盖时，按 `Tested Layer != Shipped Execution Layer` 处理。
- [ ] 对现存 legacy rule 做 No Grandfathering audit：存在得久、曾经标✅、被多个版本继承，都不算支持证据。
- [ ] 每轮至少挑 1 个遗产规则做 `ABLATE / MERGE / NARROW / DELETE / RESEARCH_ONLY` 评审；删不掉才有资格继续占模型复杂度。

## 2. 每轮研究时间配比

默认配比，不以“读书页数最大化”为目标：

- 40%：原页阅读 / source lineage / Evidence；
- 30%：implementation / negative controls / prospective trials；
- 20%：回看旧记录、Outcome Audit、Model Compression / No Grandfathering；
- 10%：CI、索引、状态同步、本地执行助手交接。

比例不是课程表，只是防偏提醒。真实 unresolved question 可以改变本轮分配。

如果连续两轮“读书+整理”超过 70% 而没有新的 implementation/prospective test，下一轮自动降低整理优先级。

当前下一棒优先从 `RESEARCH_ATTACK_QUEUE` 选择真实攻击问题：

`独立反例型 source witness / center-target witness / boundary witness / clean prospective`

而不是为了换书而换书。

## 3. 每周检查点

每 7 天或每完成一个 book sprint，主 Agent 必须回答：

1. 本周新增的是 source knowledge、implementation fidelity，还是 empirical support？不得混写。
2. 有没有一个旧观点被降级/删除/缩窄？如果没有，检查是否只在累加。
3. 有没有真实 negative control？错误输入是否真的会输？
4. 有没有 clean unknown-outcome case 在跑？如果没有，说明为什么不是在用清债/自省回避失败。
5. 我这一周挑选研究对象的方式有没有偏向支持当前模型？有没有 FAIL/NO-OP 被忽略？
6. 下周最重要的问题是什么？先定义会改变模型的真实问题，再决定读哪本书。

## 4. 主 Agent 与本地 AI 分工

主 Agent：

- 决定研究问题、source identity、Evidence semantics、冲突归类、理论修改、case scoring、credit、Git 归档与是否发布。
- 负责最终视觉主审；不把 OCR/本地助手候选直接当事实。
- implementation comparison 必须把 source witness、oracle、system under test、negative control 尽量分开。
- 负责研究选择的自审：不把“我主动选的支持材料”误写成自然出现的独立证据。

本地 AI：

- 只做 `EXECUTION_HELPER_ONLY`：同步仓库、校验 hash/page count、渲染/crop、OCR navigation、运行测试、生成 raw diff/候选 packet、收集本地输出。
- 默认不得修改 tracked files、不得 commit/push、不得给 Reading/Evidence/Empirical Support credit。
- 只有收到明确 `ONE_TIME_PERMISSION` 才可进入限定 publish scope。

详细边界见：`奇门/LOCAL_AI_EXECUTION_RUNBOOK.md`。

## 5. 书籍切换

项目不采用“读完一本马上下一本”的无限堆书模式。

统一执行：`奇门/BOOK_ROTATION_CYCLE.md`，但时间盒只触发复盘，不是学习动力来源。

核心原则：

`问题驱动选书 -> 原页读透 -> 生成候选 -> 负对照/前瞻 -> 复盘压缩 -> 再换书`

现在再加一条：

`先登记要攻击什么 -> 再打开来源`

而不是：

`书越多 -> 支持材料越多 -> 默认越接近真理`。

当前善天道 Cycle 1 已完成视觉 fidelity re-audit；Test A 已进入跨来源 implementation comparison，Test C 得到 `UNRESOLVED / NO-OP`，Test B/D 等待真实 prospective。下一来源由 **中宫寄宫 / full rotation / deity lineage / time boundary / state-system** 中哪个攻击问题最需要独立 witness 决定。
