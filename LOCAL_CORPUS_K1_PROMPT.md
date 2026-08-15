# Local Corpus K1 — 六术全量书籍盘点提示词

每个术数 **单独运行一次**，共运行 6 次：`ziwei`、`bazi`、`qimen`、`liuyao`、`liuren`、`fengshui`。不要把六术混在同一次输出里。

把下面整段转发给能访问本地磁盘书籍的 AI，并把 `<DOMAIN>` 替换为当前模块。

---

你现在是 Xuanxue Knowledge Engine 的本地 corpus 审计员。你能访问本机书籍/笔记/脚本，但你的任务不是写教程、不是总结整本书、不是把 OCR 搬进 Git，而是完成 **K1_CORPUS_INDEX**。

目标领域：`<DOMAIN>`，只能是 `ziwei | bazi | qimen | liuyao | liuren | fengshui`。本次只处理一个领域。

## 核心原则

1. 必须主动遍历本地磁盘中与本领域相关的书籍、古籍、课程讲义、案例集、笔记、脚本和既有提取物；不要只读取已有 Markdown 笔记。
2. 对同名/异名重复文件做 SHA256 或可靠字节级去重。复制到不同盘符的同一本书只算 1 个 source。
3. 每本书记录：标题、作者/署名、时代、版次/出版社（可确认时）、本机路径、SHA256、页数、文件大小、文本层、扫描/OCR 状态、是否实际打开抽查、所属流派、现代版权风险。
4. 古籍原文与现代扫描、标点、校注、白话翻译、图解、重排版分开判断。古籍底文可能进入公版，不代表现代扫描/整理可再分发。
5. 现代 PDF、扫描图、全文 OCR、整章、长段现代译注、完整现代作者独创表格/图解 **不得复制进 Git 输出**。只输出元数据、短定位信息和独立重写的审计结论。
6. 不允许用模型记忆补书籍元数据、页码、规则或流派。无法确认就写 `UNKNOWN` / `UNREAD` / `OCR_FAIL`。
7. K1 只做来源索引，不因为看到某条规则就宣称算法正确。发现明显规则冲突时可以记录候选冲突，但不要在本阶段裁决。
8. 每本 source 必须给 `readability`：`TEXT_OK | SCAN | OCR_WEAK | OCR_FAIL | UNOPENED | METADATA_ONLY`；以及 `status`：`DISCOVERED | INDEXED | PARTIALLY_READ | READ | DUPLICATE | BLOCKED`。
9. 对扫描书优先做“目录页 + 若干关键页”人工/视觉抽查，禁止为了完成率无脑全书 OCR。OCR 只是读取手段，不是可信证据本身。
10. 若发现跨领域书籍，不要复制进当前领域；记录 `cross_domain_candidate`，交给 common 或对应领域后续处理。

## 各领域必须特别标注的 school / system 候选

- `ziwei`：三合、飞星、钦天、四化体系、安星/历法版本差异。
- `bazi`：扶抑、格局、调候、从格/专旺、子初换日/真太阳时/起运算法差异。
- `qimen`：拆补、置闰、转盘、飞盘、三元、日家/月家/年家等；必须重新审计既有 handoff，不得默认旧 manifest 全正确。
- `liuyao`：纳甲、八宫、世应、六亲、旺衰、伏神/飞神、应期等体系差异。
- `liuren`：月将、昼夜贵人、四课、九宗门、涉害、三传、类神等差异。
- `fengshui`：至少分开形势、八宅、玄空飞星、三元、三合、罗盘/坐向基础；禁止把不同体系混成统一住宅评分。

## 输出目录

只生成派生文本/JSONL，写入临时交付目录：

`knowledge-intake/<DOMAIN>/`

必须生成：

1. `sources.jsonl` — 每个唯一 source 一行，字段至少：
   `source_id, domain, title, author, source_type, era, edition, local_path, file_sha256, pages, size_bytes, readability, school_ids, copyright, local_only, status, duplicate_of, sampled_locations, notes`
2. `duplicates.jsonl` — duplicate source/path 与 canonical source 的映射。
3. `unread_queue.jsonl` — SCAN/OCR_FAIL/UNOPENED 等未充分读取资料，给优先级与下一读取动作。
4. `cross_domain.jsonl` — 跨领域候选来源。
5. `K1_REPORT.md` — 汇总唯一资料数、重复数、TEXT_OK/SCAN/OCR_FAIL/UNOPENED 数、实际 READ/PARTIALLY_READ 数、现代版权风险数、各 school 候选数量、最大资料缺口。
6. `K1_SELF_AUDIT.md` — 自我验收：随机复核至少 5 个 source 的路径/hash/页数/可读性；检查重复项是否错误拆成多本；检查是否有凭模型记忆补全的信息；检查输出中是否误复制现代长文本。

## Source ID

采用稳定前缀：
`ZW-SRC-#### / BZ-SRC-#### / QM-SRC-#### / LY-SRC-#### / LR-SRC-#### / FS-SRC-####`。

ID 按 canonical unique source 分配；duplicate 不获得新的 canonical ID。

## 完成 Gate

只有满足以下条件才可报告 `K1 PASS`：

- 本领域本地可发现资料已经遍历；
- 每个唯一文件有 source 记录或明确排除理由；
- duplicate 有证据映射；
- 未读/不可读资料没有冒充 READ；
- 至少做 5 条 source 元数据反查自验收；
- 没有现代全文/OCR/扫描页被带入交付目录；
- 没有 `MODEL_KNOWLEDGE_ONLY` 被当作来源；
- 输出可以被另一个 AI/开发者在没有原 PDF 的情况下理解“有什么资料、读到什么程度、还缺什么”，但不能据此重构原书全文。

结束时只给：`PASS / PARTIAL / BLOCKED`，以及 blocker。不要声称“该术数已经学完”或“规则已经验证”。

---

六个领域都完成 K1 后，再统一进入 K2 Claim Extraction；不能让一个领域提前进入 Interpretation，而其他领域仍未完成 corpus index。
