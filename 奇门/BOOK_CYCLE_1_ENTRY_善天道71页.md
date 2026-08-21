# Book Cycle 1 Entry — 善天道《奇门遁甲讲义71页》

状态：ACTIVE DISTILLATION / SUPPLEMENTAL VISUAL RE-AUDIT 71/71 / BASE K2 READING REMAINS COMPLETE(TEXT_LAYER_FULL)

日期：2026-08-21

## 1. Canonical identity and corrected K2 state

- source_id：`QM-SRC-0028`
- work_id：`WORK-000018`
- relation：`PRIMARY_WORK`
- title：`善天道-奇门遁甲讲义71页`
- author：`善天道`（K1 `author_basis=FILENAME`，不是作者页独立验证）
- source_type：`COURSE`
- SHA256：`bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243`
- PDF pages：71
- readability：`TEXT_OK`
- copyright：`FORBIDDEN_TO_PACKAGE`

本 Cycle 曾先后暴露两次状态认知错误，均保留为失败史：

1. 第一版 Entry 曾误写 `PENDING_K1_INTAKE`，实际该源早已完成 K1 intake；
2. commit `10ad742f...` 又把 p1-p22 的视觉复核新建成 `PARTIAL` Reading/Evidence shard，但 aggregate K2 中 `QM-SRC-0028` 早已是 `COMPLETE / 71/71 / TEXT_LAYER_FULL / 50 Evidence`。CI #287 因重复 Reading source fail-closed。

因此本轮不再伪造第二份 Reading。正确语义是：

`BASE K2 COMPLETE(TEXT_LAYER_FULL) + SUPPLEMENTAL VISUAL_FIDELITY_REAUDIT(71/71)`

而不是：

`旧 COMPLETE 被重置为 PARTIAL`。

重复 shard 已删除。视觉复核结果进入独立 Visual Review / Correction Overlay，不重复计 Reading Credit，也不把同一来源重复算作独立 Evidence。

历史《精读笔记_善天道》另有 K1 身份 `QM-SRC-0036 / WORK-000232 / NOTE / SECONDARY_NOTE`，继续只作为 prior model，不替代原书。

## 2. Why this source is being reopened

这不是为了“再读一本书”刷进度，而是为了攻击真实 debt：center host / full rotation、八神谱系、setup/time-boundary 差异、旧二手笔记的 source-map 错误，以及大量象意词典带来的 narrative flexibility。

本轮核心目标从“补阅读覆盖率”修正为：

`验证旧 TEXT_LAYER Evidence 的 Source Fidelity -> 找视觉层错误/内部冲突 -> 判断哪些只是纸面规则 -> 形成可证伪 test hooks`。

## 3. Full visual re-audit result

原页视觉复核已覆盖 p1-p71。详细记录：

`knowledge/K2_VISUAL_REVIEW_SESSIONS/QM-SRC-0028_CYCLE1.md`

该 71/71 指的是本 Cycle 的 supplemental visual fidelity audit，不改变 aggregate Reading Ledger 中既有 `COMPLETE / TEXT_LAYER_FULL` 状态。

### 3.1 书本自身并不支持单因素机械直断

p4-p7 一面给五阴五阳、八门传统吉凶等规则，一面明确提醒出行不能只靠时辰歌诀、门宫生克不能简单等同吉凶。p25 又把三奇六仪、八门、九星、八神、九宫视作相互关联的信息符号。

这支持“组合/情境分析是来源内部已有的限制条件”，但不证明项目当前模型有效。

### 3.2 视觉层暴露了 TEXT_LAYER 很难看出的 source corruption

本书并不是一份可以无损转成规则库的干净教材。视觉复核发现多处印刷/编辑/拼接问题，例如：

- p27 “两面三刀种体系”等明显文本损坏；八门表头/五行字段亦有异常；
- p29 正文出现“天星”而表格列“天英”；
- p35 同段的三奇升殿命名有自相矛盾；
- p33 称“四十格”，p46 又列“第四十一 门迫与宫迫”；
- p53-p55 的地支、五行、节令材料存在明显错字/错配候选；
- p55 出现日期与节气名称不相容的教学例。

这些都必须保留为 `SOURCE_TEXT_CORRUPTION / SOURCE_INCONSISTENCY`，不能由模型按照常识静默修正。

### 3.3 八神不是一个可以强行压成单一 enum 的干净系统

p31 与 p55 对勾陈/朱雀、白虎/玄武的关系给出互相冲突的映射线索；p31 的阳遁八神序列本身还出现“称八神但列项不足”的不完整文本。

因此现有 `GOUCHEN_ZHUQUE` 与 `BAIHU_XUANWU` 冻结字段继续作为 anti-post-hoc 工程约束，但**不得被解释为历史谱系已经解决**。

当前分类：

`SOURCE_INTERNAL_CONFLICT / DEITY_LINEAGE_UNRESOLVED / CONTEXT_REQUIRED`

不改 runtime enum，不静默同义化。

### 3.4 格局不是“看到两个字就套一句话”

p33-p42 多个格局依赖旬别、天地盘次序、门、奇、神、宫等组合条件。青龙返首、飞鸟跌穴本书自己就限定旬条件，说明平面化的 `stem pair -> verdict` 会损失定义条件。

这支持现有 Pattern Registry 的方向：先冻结对象、层、顺序、触发条件，再谈格局解释。

### 3.5 p49 以后出现明显 method / editorial layer shift

同一本书出现重复“第五章”、暗藏飞干、一般五行/八字式节令材料、`万物类象（新）`、现代职业/机构象意，以及后段再度重复占事规则。

这更像一个多层教学汇编，而不是一条完全一致的单一算法链。

当前必须拆为至少：

`STANDARD_PLATE / HIDDEN_FLYING_STEM_AUX / SYMBOLIC_LEXICON / APPLIED_ROLE_MAP / HIGH_RISK_SOURCE_CLAIMS`

不能笼统叫“善天道体系”然后全部互通。

### 3.6 “象意翻译”解决死模板，也会制造新的自由度

p59 以后明确把奇门视为庞大的意象符号系统，强调像翻译一样依赖记忆与想象。这对摆脱单符号模板有启发，但同时暴露新的危险：一个符号可以拥有大量人物、疾病、物品、机构、事件含义，事后几乎总能挑到一个贴合现实的解释。

因此项目不能从“死背条文”滑向“无限联想”。

当前新增的方法论约束候选：

`Semantic Expansion Penalty / 语义自由度预算`

只有在结果未知前被冻结的 Role Map、eligible symbolic meanings、pattern family 与 competing branches 才可进入评分；越宽泛的象意词典，越需要更强的预冻结和 negative control。

这只是 v0.3-alpha 内部 refinement，不升级理论版本。

### 3.7 高风险具体断语继续隔离

p51-p71 大量疾病、死亡、刑事、犯罪、诉讼、癌症、凶器、罪犯方向等断语可以作为 Source Fidelity 研究对象，但没有资格直接用于现实医疗、法律或犯罪事实判断。

统一：`HIGH_RISK_SOURCE_CLAIM / RESEARCH_ONLY / NOT_EMPIRICAL_SUPPORT`。

### 3.8 同书重复不是独立 corroboration

p49-p52 与 p68-p71 等段存在明显规则重复。重复出现只能说明同一载体反复编排，不能增加独立来源数或经验置信度。

新增纪律：

`INTRA_SOURCE_REPETITION != INDEPENDENT_SUPPORT`。

## 4. Correction of the old “精读笔记”

前置审计继续有效，但现在需要再加一层修正：过去的问题不仅是旧笔记来自 `_txt`，更是项目曾经把“TEXT_LAYER 已完整抽取”与“Source Fidelity 已经充分核验”混成同一件事。

新的区分：

`TEXT_LAYER_COMPLETE != VISUAL_FIDELITY_AUDITED != EMPIRICALLY_SUPPORTED`。

三者分别回答：文本是否读完、原载体是否核对、现实效力是否有证据。

## 5. Current theory impact

不升级 v0.4。

本书目前真正改变的是约束，而不是准确率：

- 保留 Context / Role Map / Pattern Registry；
- 强化 Source-Internal-Conflict Gate；
- 强化 Method-Layer separation；
- 引入 `Semantic Expansion Penalty` 候选；
- 将“想象力”视为可能的叙事自由度，而不是天然优点；
- 同书重复不计独立支持；
- 任何可在结果后替换的 deity alias、用神、象意词、格局条件、应期，都必须冻结或 A/B。

因此当前最接近自己的理论路线仍是：

`受约束的情境推演 + 反证优先 + 自由度预算 + 结果前冻结 + 负对照`。

它仍是研究中的 v0.3-alpha，不是已证实理论。

## 6. Next tests — attack, not confirmation

下一阶段不再继续摘录更多“象意”。优先做四类可失败测试：

1. 用 p21-p22 worked plates 检查非甲子 full star/door/deity rotation 与 center hosting；
2. 做 wrong-bureau / wrong-setup / wrong-boundary / permuted-role-map negative controls；
3. 对宽象意词典做 shuffled-symbol / restricted-lexicon 对照，测试错误映射是否仍能生成“很像”的解释；
4. 八神 p31 vs p55 只做 lineage/context 拆解，不以结果命中率倒推采用哪套映射。

若错误盘、错用神或打乱象意仍能被解释得很有说服力，这不是“模型灵活”，而是自由度过高的反证。

## 7. Book-close discipline

当前先不把“71/71 visual audit”自动等于 Book Close。关闭前仍需完成：

- visual correction overlay 固化；
- 既有 50 条 TEXT_LAYER Evidence 的受影响项核对清单；
- implementation / negative-control hooks 至少落一个；
- 输出 `KEEP / REVISE / DELETE / NO-OP`；
- 明确哪些内容只停留在纸面、哪些进入可测试候选、哪些被排除。

读完不是通过；能指出自己之前为什么会读错、哪里不能用、怎样可能被证伪，才算这一轮有增量。
