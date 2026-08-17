# Local Corpus K1 Master Prompt — 六术统一书籍盘点

把下面整段一次性转发给能访问本机书籍/笔记/脚本的 AI。它必须按域串行执行，不能把六术混在同一份规则或输出文件里。

---

你现在负责 Xuanxue Knowledge Engine v1 的 **K1_CORPUS_INDEX**。你有本机磁盘访问能力。你的任务不是写术数教程，不是总结书，不是把 OCR 搬进 Git，而是把六术所有本地学习资料建立成可追溯、可去重、可继续工程化的 Source Registry。

必须处理且只能处理这六个正式术数域，按顺序逐域完成并逐域自验收：

1. `ziwei` — 紫微斗数
2. `bazi` — 八字
3. `qimen` — 奇门遁甲
4. `liuyao` — 六爻
5. `liuren` — 大六壬
6. `fengshui` — 风水

**禁止把六个领域合成一个 sources.jsonl。每个领域必须独立输出、独立去重、独立统计、独立 PASS/PARTIAL/BLOCKED。**

## 总原则

- 主动遍历所有可访问磁盘、资料目录和项目研究目录；不要只读现有 Markdown 笔记。
- 书籍、古籍、课程讲义、案例集、研究笔记、脚本和既有提取物都要发现，但必须区分 `BOOK / COURSE / ANCIENT_TEXT / ARTICLE / NOTE / CODE / CASE_COLLECTION / OTHER`。
- 对同名、异名、不同盘符复制件执行 SHA256 或可靠字节级去重；同一文件只建立一个 canonical source。
- 每个 canonical source 记录真实可核验元数据：标题、作者/署名、时代、版次/出版社（能确认才填）、本地路径、SHA256、页数、大小、文本层、扫描/OCR 状态、抽查情况、候选流派、版权状态。
- 禁止用模型记忆补作者、版次、页码、流派或内容。不能确认写 `UNKNOWN`。
- 未真正读取的资料不得标记 `READ`。扫描件、乱码 OCR、打不开的文件要分别标记。
- 古籍底文与现代扫描、标点、校注、翻译、图解、排版分开判断版权。
- 现代 PDF、扫描页、整书/整章 OCR、长段现代译注、完整现代作者独创表格或图解不得进入交付文本。
- 本阶段只做 Source Registry；看到规则可以记“候选冲突/候选主题”，但不得提前宣称算法正确、fixture 已验证或 Interpretation 已成熟。
- `MODEL_KNOWLEDGE_ONLY` 不是来源。

## Readability / Status 固定枚举

`readability` 只能使用：
`TEXT_OK | SCAN | OCR_WEAK | OCR_FAIL | UNOPENED | METADATA_ONLY`

`status` 只能使用：
`DISCOVERED | INDEXED | PARTIALLY_READ | READ | DUPLICATE | BLOCKED`

## 六域特别审计点

### ziwei
至少识别：三合、飞星、钦天、四化体系、安星规则、历法/时辰边界、宫位与限运体系。现有 iztro/代码只能算候选实现来源，不得当作传统术理唯一真值。

### bazi
至少识别：扶抑、格局、调候、从格/专旺、旺衰、子初换日、真太阳时、起运顺逆与起运岁数算法等体系差异。

### qimen
至少识别：拆补、置闰、转盘、飞盘、三元、年家/月家/日家/时家。必须重新审计仓库既有 `handoff/qimen`，不得默认旧 manifest/规则全部正确；已存在的统计只能作为待复核线索。

### liuyao
至少识别：纳甲、八宫、世应、六亲、六神、旺衰、伏神/飞神、进退神、应期等体系差异。

### liuren
至少识别：月将、昼夜贵人、天地盘、四课、九宗门、涉害、三传、十二天将、类神等体系差异。

### fengshui
至少拆开：形势、八宅、玄空飞星、三元、三合、罗盘/坐向基础。禁止把不同体系混成一个“住宅吉凶总分”。同时记录资料是否依赖空间测量、坐向度数、建造/入伙/大修时间等输入。

## 输出位置：本机临时目录，禁止提交 Git

每个领域输出到：

`knowledge-intake/<domain>/`

该目录是 **local-only**。不要执行 `git add`、`git commit`、`git push`。真实本机路径只允许存在于这个 intake；未来进入公开 `knowledge/` 的 sanitized registry 必须删除或泛化用户名、盘符、私有目录等无必要信息。

每个领域必须生成 6 个文件：

1. `sources.jsonl`
   每个唯一 canonical source 一行，至少字段：
   `source_id, domain, title, author, source_type, era, edition, local_path, file_sha256, pages, size_bytes, readability, school_ids, copyright, local_only, status, duplicate_of, sampled_locations, notes`

2. `duplicates.jsonl`
   每个重复路径/文件对应 canonical source，并写去重依据。

3. `unread_queue.jsonl`
   所有 `SCAN / OCR_WEAK / OCR_FAIL / UNOPENED / METADATA_ONLY` 中仍值得继续读取的资料，给 `priority`、`reason`、`next_action`。

4. `cross_domain.jsonl`
   明显属于另一术数或公共基础的资料，只登记，不强行吸收到当前领域。

5. `K1_REPORT.md`
   汇总：唯一 source 数、duplicate 数、TEXT_OK/SCAN/OCR_FAIL/UNOPENED 数、READ/PARTIALLY_READ 数、现代版权高风险数、school/system 候选、最大资料缺口、下一阶段读取优先级。

6. `K1_SELF_AUDIT.md`
   必须随机反查至少 5 个 canonical source：实际文件路径、SHA256、页数/大小、readability、duplicate 判断；同时检查是否凭模型记忆补信息、是否误把扫描/OCR 当成 READ、是否误复制现代长文本。

## Source ID 固定前缀

- 紫微：`ZW-SRC-####`
- 八字：`BZ-SRC-####`
- 奇门：`QM-SRC-####`
- 六爻：`LY-SRC-####`
- 六壬：`LR-SRC-####`
- 风水：`FS-SRC-####`

duplicate 不获得新的 canonical ID。

## 单域完成 Gate

一个领域只有全部满足以下要求才能报告 `PASS`：

- 已遍历本地可发现资料位置；
- 每个唯一文件有 source 或明确排除理由；
- duplicate 有 hash/字节证据；
- 未读资料没有冒充 READ；
- 至少 5 个 source 完成反查自验收；
- 没有现代全文、扫描页、长现代文本进入 intake 输出；
- 没有模型知识冒充来源；
- 没有把 intake 目录提交 Git；
- 结果足以让后续工程知道“有什么资料、读到什么程度、哪些流派、缺什么”，但不能据此重构原书全文。

不满足则报告 `PARTIAL` 或 `BLOCKED`，列出 blocker。禁止用“差不多完成”替代 Gate。

## 六域总收口

六个领域都执行完后，再生成本机文件：

`knowledge-intake/K1_MASTER_REPORT.md`

只汇总每域：`PASS/PARTIAL/BLOCKED`、unique sources、duplicates、readability 分布、最大 blocker、版权风险、下一动作。

**不得因为某一个领域资料多就提前开始 K2。只有六域全部至少完成可接受的 K1 source index，并经过项目端二次验收后，才进入 K2 Claim Extraction。**

执行完成后，把 `K1_MASTER_REPORT.md` 和六个领域的 `K1_REPORT.md / K1_SELF_AUDIT.md` 内容回报给我；不要上传原书、扫描、OCR 全文。

---
