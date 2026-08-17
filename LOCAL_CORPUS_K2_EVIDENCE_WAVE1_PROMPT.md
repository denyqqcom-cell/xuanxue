# LOCAL AI PROMPT — K2B Evidence Extraction Wave 1

你现在负责 Xuanxue Knowledge Engine v1 的 **K2_EVIDENCE_EXTRACTION / WAVE 1**。

K1 已关闭，K2A Source Lineage 已由项目端正式验收为 COMPLETE。

本轮是第一次真正逐书阅读本地资料，但仍然：

**严禁 Claim Extraction。**

Evidence ≠ Claim。

────────────────────
## 一、同步正确分支
────────────────────

执行：

```bash
git status --short
git fetch origin
git checkout knowledge-engine-v1-k2
git pull --ff-only origin knowledge-engine-v1-k2
```

worktree 必须 clean。

确认存在：

- `knowledge/K2A_FINAL_ACCEPTANCE.md`
- `knowledge/K2_EVIDENCE_PROTOCOL.md`
- `knowledge/K2_EVIDENCE_STATE.json`
- `knowledge/schema/evidence.schema.json`
- `knowledge/schema/reading_coverage.schema.json`
- `tools/plan_k2_evidence_wave1.py`
- `tools/sanitize_k2_evidence.py`
- `tools/validate_k2_evidence.py`
- `tools/test_k2_evidence.py`

如果有未知改动，STOP。

禁止 `reset --hard` / `clean -fd`。

────────────────────
## 二、先生成官方 Wave 1 阅读计划
────────────────────

执行：

```bash
python3 tools/plan_k2_evidence_wave1.py \
  --output /home/joe/knowledge-intake/K2_WAVE1_PLAN.jsonl
```

必须成功。

不要自行挑书替代官方计划。

Wave 1 的选择逻辑已经写死：

1. 六术所有 P0 unique-coverage textual work；
2. 只要一个 P0 source 属于某 work_id，就展开该 work 的全部 PRIMARY_WORK / WORK_PART unique coverage；
3. 六爻、大六壬属于薄 corpus，本轮把其全部 governed unique textual coverage读完；
4. SAME_WORK_VARIANT 只作为备份载体，不增加独立票；
5. NOTE / CODE / AUX 不进入传统文本阅读。

────────────────────
## 三、本轮必须真正“读”，不是搜索关键词
────────────────────

对 `K2_WAVE1_PLAN.jsonl` 每一条 selected reading unit：

- 读取完整文件 coverage；
- PDF 已知页数时，从 pdf 第 1 页检查到最后一页；
- 不得只看目录；
- 不得只检索关键词；
- 不得只摘几条“看起来重要”的内容后标 COMPLETE；
- 不得把 TEXT_OK 等同 READ；
- 不得把 OCR 输出等同原书。

TEXT_OK：可以用文字层提高效率，但 evidence 必须能回到具体页。

SCAN / OCR_WEAK：以页面视觉核验为准。OCR 只能辅助定位，不得盲信；任何进入 Evidence 的内容必须回看原页确认。

遇到无法辨认页：

`read_status=BLOCKED`

写简短 blocker_reason，不能假装 COMPLETE。

────────────────────
## 四、Reading Ledger
────────────────────

本机输出：

`/home/joe/knowledge-intake/K2_WAVE1_READING_LEDGER.jsonl`

每个 Wave1 selected source_id 恰好一行。

字段只能：

```text
reading_id
source_id
work_id
relation
coverage_mode
page_ranges
pages_reviewed_count
read_status
evidence_count
blocker_reason
review_status
```

建议：

```text
reading_id = READ-<source_id>
```

PDF 示例：

```json
{
  "reading_id":"READ-ZW-SRC-0001",
  "source_id":"ZW-SRC-0001",
  "work_id":"WORK-000001",
  "relation":"PRIMARY_WORK",
  "coverage_mode":"PDF_PAGES",
  "page_ranges":[{"start":1,"end":55}],
  "pages_reviewed_count":55,
  "read_status":"COMPLETE",
  "evidence_count":12,
  "blocker_reason":null,
  "review_status":"REVIEWED"
}
```

如果 K1 `pages=55`，COMPLETE 必须覆盖 pdf 1–55。

不能用“读了大部分”冒充 COMPLETE。

────────────────────
## 五、Evidence 输出
────────────────────

本机输出：

`/home/joe/knowledge-intake/K2_WAVE1_EVIDENCE.jsonl`

Evidence 是**一个来源位置明确支持的一条原子事实/规则/案例信息**。

字段只能：

```text
evidence_id
domain
source_id
work_id
source_location
evidence_type
scope
topic
normalized_fact
extraction_basis
claim_readiness
school_ids
verbatim_quote
review_status
copyright_class
notes
```

建议 evidence_id：

```text
EV-<source_id>-0001
EV-<source_id>-0002
...
```

────────────────────
## 六、Evidence 可以抽什么
────────────────────

只抽来源直接支持的内容：

- 明确规则 / 定义；
- 排盘、计算、安置、起例程序；
- 表格中的结构映射；
- 图中的明确结构信息；
- 用神 / 参数选择条件；
- 象意 / 判断规则；
- 旺衰、格局、宫位、星门神、六亲、三传等明确规则；
- 应期/时间规则；
- 完整 worked example 的关键输入、步骤、输出；
- 案例记录；
- 作者明确表达的方法论、限制、伦理、主客、急缓、取参原则；
- 历史起源、人物归属等说法，但必须标 HISTORICAL_CLAIM / HISTORY，不能当技术真值。

不需要把纯广告、致谢、重复目录、无知识信息的闲文变 Evidence。

但“没有 Evidence”不代表没读；Reading Ledger 才证明 coverage。

────────────────────
## 七、严禁在 K2B 做的事
────────────────────

严禁：

- 把两本书的内容合成一个新规则；
- 用模型常识补齐书中没说的条件；
- 看到明显疑似错误就自行改正；
- 判断 A 派比 B 派正确；
- 把多数书一致当成真理；
- 把同一本书的不同版本算多票；
- 把 WORK_PART 当独立来源投票；
- 把 COMMENTARY 当原典独立票；
- 把项目 CODE 当传统理论证据；
- 从 NOTE 抽传统术理 Evidence；
- 创建任何 claims 文件；
- 修改 App/算法。

如果发现冲突：

两边各自形成 Evidence，`claim_readiness=CONFLICT_CANDIDATE`。

不要解决冲突。

────────────────────
## 八、normalized_fact 规则
────────────────────

必须自己重述，不长抄原文。

每条尽量只表达一个命题或一个程序步骤。

必须保留：

- 条件；
- 例外；
- 顺逆；
- 阴阳；
- 时间/空间前提；
- 所属流派（仅当来源明确）；
- 原文使用的关键术语。

禁止把：

“可能 / 宜 / 可参考”

改写成：

“必然 / 一定”。

────────────────────
## 九、source_location 必须可反查
────────────────────

使用：

```text
pdf:p12
pdf:p12-p13
printed:p35|pdf:p41
chapter:卷二/第三节|pdf:p88
```

禁止写：

`/home/...`
`/mnt/...`
`E:\...`

Evidence 必须回得去真实页面。

────────────────────
## 十、extraction_basis
────────────────────

只能：

```text
TEXT_LAYER
VISUAL_PAGE
TABLE_READ
DIAGRAM_READ
MANUAL_TRANSCRIPTION
```

SCAN/OCR_WEAK 的最终 evidence，如果是看原页确认，优先写 VISUAL_PAGE / TABLE_READ / DIAGRAM_READ，而不是把 OCR 当证据。

────────────────────
## 十一、scope
────────────────────

只能：

```text
STRUCTURE
ALGORITHM
SYMBOLISM
SELECTION
INTERPRETATION
TIMING
CASE
HISTORY
META_METHOD
```

不要因为 scope=INTERPRETATION 就开始综合解盘。

这里仍只是“这本书说了什么”。

────────────────────
## 十二、claim_readiness
────────────────────

只能：

```text
READY
CONTEXT_REQUIRED
CONFLICT_CANDIDATE
NOT_CLAIM
```

READY ≠ 已经是正确 Claim。

只表示后面 K2C 可以拿来做 Claim synthesis 候选。

────────────────────
## 十三、版权
────────────────────

默认：

```text
verbatim_quote = null
copyright_class = DERIVED_FACT_SAFE
```

现代书、现代扫描、研究资料：禁止把原句、整段、整表复制进 Git。

即使本机 OCR 出来，也只能用于研究和核验，不能把长文本提交仓库。

────────────────────
## 十四、WORK_PART 与 SAME_WORK_VARIANT
────────────────────

Wave1 计划只要求 unique coverage。

WORK_PART：必须读，因为有独特 coverage。

SAME_WORK_VARIANT：不是独立阅读义务。

如果 PRIMARY/WORK_PART 页面损坏，而 variant 更清楚：可以本地参考 variant 进行视觉核验，但不能把它算成另一份支持票。

如果必须从 variant 才能确认某页且无法诚实引用 primary/part 的页位置，先标 BLOCKED 并回报，不要自己创造 provenance 规则。

────────────────────
## 十五、多领域 source
────────────────────

一个 source 的 `knowledge_domains` 可能有多个正式 domain。

Evidence 的 `domain` 必须是 K1 已支持的其中一个。

同一页如果真的分别支持两个体系的不同事实，可以建两条 Evidence，但不能为了增加数量重复同一事实。

────────────────────
## 十六、六术平衡
────────────────────

禁止按：

奇门 → 全读完 → 紫微 → 全读完 → ...

执行。

建议循环：

```text
紫微一 work
八字一 work
奇门一 work
六爻一 work
六壬一 work
风水一 work
再下一轮
```

六爻 / 六壬因为 corpus 薄，本 Wave 直接完成其 governed unique textual coverage。

────────────────────
## 十七、96 条 semantic UNKNOWN 本轮不要乱认领
────────────────────

K2A 还有 96 条 TEXTUAL_SOURCE：

`knowledge_domains=["UNKNOWN"]`

本 Wave 1 的正式 Evidence lane 不从它们抽六术 Evidence。

它们没有被丢弃。

项目已登记：

`unknown_textual_resolution_backlog = 96`

后续 K2B 会有独立 Discovery Reading 波次，打开真实内容判断：

- 属于哪一术；
- OUT_OF_SCOPE；
- 或读后仍应 UNKNOWN。

本轮禁止为了“全部吸收”提前猜。

────────────────────
## 十八、完成本机草稿后使用官方 sanitizer
────────────────────

执行：

```bash
python3 tools/sanitize_k2_evidence.py \
  --ledger /home/joe/knowledge-intake/K2_WAVE1_READING_LEDGER.jsonl \
  --evidence /home/joe/knowledge-intake/K2_WAVE1_EVIDENCE.jsonl \
  --repo-root .
```

必须：

```text
k2-evidence-sanitize: PASS
```

生成：

- `knowledge/K2_READING_LEDGER_WAVE1.jsonl`
- `knowledge/K2_EVIDENCE_WAVE1.jsonl`

禁止手工复制作为最终产物。

────────────────────
## 十九、机器验收
────────────────────

运行：

```bash
python3 tools/test_k2_evidence.py
python3 tools/validate_k2_evidence.py --force
python3 tools/validate_k2_lineage_integrity.py
python3 tools/validate_knowledge.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

目标：

- Evidence/ledger 数据 issues=0；
- selected reading units 无缺漏；
- Claim Extraction 仍 blocked；
- lineage integrity 不退化；
- App stable core 不退化。

注意：

K2_EVIDENCE_STATE 仍保持 `WAVE1_OPEN`。

本地 AI 不得自行改成 WAVE1_COMPLETE。

项目端会二次审核 Evidence 质量后再决定。

────────────────────
## 二十、提交边界
────────────────────

本轮只允许提交：

```text
knowledge/K2_READING_LEDGER_WAVE1.jsonl
knowledge/K2_EVIDENCE_WAVE1.jsonl
```

禁止提交：

- `/home/joe/knowledge-intake/`
- PDF / 扫描页 / 截图 / OCR 全文
- K1 registry
- K2 lineage
- PROJECT_STATE
- K2_EVIDENCE_STATE
- claims / conflicts / fixtures / interpretation
- App / engine / algorithm
- validator / tests

push：

`origin/knowledge-engine-v1-k2`

然后 STOP。

严禁开始 K2C Claim Extraction。

────────────────────
## 二十一、最终回报
────────────────────

只回报：

1. commit SHA
2. official Wave1 selected reading units 数
3. 六术 selected source 数与 distinct work_id 数
4. Reading Ledger rows
5. COMPLETE / BLOCKED 数
6. 总已复核页数
7. 各术已复核页数
8. Evidence 总数
9. Evidence 按六术数量
10. evidence_type 分布
11. scope 分布
12. claim_readiness 分布
13. extraction_basis 分布
14. 每个 source evidence_count 与 ledger 是否一致
15. 发现的 suspected source/OCR issue 数，只给 source_id + page + 简短说明
16. 发现的 conflict candidate 数，只给 evidence_id / source_id / topic，不解决
17. COMMENTARY_DERIVATIVE evidence 数
18. 是否有从 NOTE/CODE/AUX 抽 traditional Evidence：必须 0
19. 是否有从 semantic UNKNOWN 抽六术 Evidence：必须 0
20. 非 PUBLIC_DOMAIN source 的 verbatim_quote 非 null 数：必须 0
21. `test_k2_evidence.py`
22. `validate_k2_evidence.py --force`
23. `validate_k2_lineage_integrity.py`
24. `validate_knowledge.py`
25. `generate_knowledge_status.py --check`
26. `:ziwei-core:test`
27. git status 是否 clean
28. commit 文件列表

不要开始 Claim Extraction。
