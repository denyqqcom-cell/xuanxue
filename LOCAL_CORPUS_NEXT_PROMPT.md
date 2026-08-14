# Local corpus next-pass prompt

Copy the block below to the AI that can access the local books. Run it **three separate times** for `bazi`, `liuyao`, and `liuren`. Do not combine modules.

---

你现在负责把我本地书籍/笔记转成可供 Android/Kotlin 工程使用的“可验证 handoff”，不是写教程，也不是把书 OCR 后搬进 Git。

目标模块：`<bazi | liuyao | liuren>`（每次只做一个）
输出目录：`handoff/<module>/`

必须遵守：

1. 先完整盘点本模块本地资料：书名、作者、时代/版本、本机路径、页数/大小、是否有文本层、是否重复、是否现代出版物。古籍原文与现代整理/翻译/图解分开判断版权。
2. 禁止提交/输出整本 PDF、扫描页、全文 OCR、整章、长段现代译注、完整现代作者独创表格/图解。必要短引文必须带来源位置；主体必须是独立重写的结构化规则。
3. 严格拆成三层：
   - Structure：历法/排盘/装卦/起课等确定性结构；
   - Selection：取用神/类神/主客等，必须写明事体条件和流派；
   - Interpretation：情境推演、反证、应期与置信边界。
   不允许把“看到某符号”直接写成固定现实结论。
4. 不同流派/书本冲突不得强行合并。必须记录冲突输入、两种规则、来源、会影响哪些输出，以及 App 应采用 config、UnsupportedSchool 还是继续阻断。
5. 每条正式规则必须有 `rule_id`、conditions、inputs、outputs、school、source_ids、source_location、confidence(A/B/C/D)、conflicts_with、implementation_ready、notes。
6. `MODEL_KNOWLEDGE_ONLY` 只能作为待核验提示，禁止进入正式算法、黄金夹具和 release-ready 规则。
7. 案例必须区分 retrospective / half-blind / blind；已知答案后解释不得统计成预测准确率。
8. 已有本地脚本只能当候选实现。必须先确认来源/许可，再用独立资料或标准案例交叉核对；“能运行”不等于“规则正确”。
9. 现代出版物中的长断语、案例叙事、独特译注/编排默认 `RESEARCH_ONLY`；能进入 App 的优先是传统事实关系、独立重写的程序化规则、短 UI 说明和可复现 fixture。
10. 如果资料不足以决定某算法，明确写 `NOT_READY`，不要用模型常识补齐。

必须生成以下文件：

- `00_CORPUS_MANIFEST.md`
- `01_SYSTEM_MAP.md`
- `02_ALGORITHM_SPEC.md`
- `03_RULES.jsonl`
- `04_CONFLICTS.md`
- `05_FIXTURES.jsonl`
- `06_CASES.md`
- `07_COPYRIGHT_GATE.md`
- `08_IMPLEMENTATION_HANDOFF.md`
- `09_OPEN_QUESTIONS.md`
- `HANDOFF_SUMMARY.md`

`05_FIXTURES.jsonl` 每条至少包含：raw_input、expected_structural_output、source_ids、source_location、school、retrospective(boolean)、notes。优先建立真正能锁死算法边界的 fixture，而不是只测试“字段不为空”。

`07_COPYRIGHT_GATE.md` 必须把候选内容逐类分成：
- `ALLOW_IN_APP`
- `RESEARCH_ONLY`
- `FORBIDDEN_TO_PACKAGE`

`08_IMPLEMENTATION_HANDOFF.md` 必须给出：建议 Kotlin package、data classes、public API、method/school enums、Unsupported/invalid errors、测试清单、哪些字段允许 UI 展示、哪些解释尚未开放。

`HANDOFF_SUMMARY.md` 最后必须汇总：
- 唯一资料数 / 重复数 / 实际精读数 / 无法读取数；
- A/B/C/D 规则数量；
- implementation_ready 数量；
- fixture 数量和覆盖层级；
- 最大流派冲突；
- 最大版权风险；
- 当前能做到 Structure / Selection / Interpretation 哪一层；
- 接下来给 Kotlin AI 的 3 个具体任务。

完成后不要声称“模块已验证完成”。只按证据给出 READY / PARTIAL / NOT_READY。

---
