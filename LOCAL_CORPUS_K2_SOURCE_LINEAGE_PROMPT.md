# LOCAL AI PROMPT — K2 Source Lineage

你现在负责 Xuanxue Knowledge Engine v1 的 **K2_SOURCE_LINEAGE**。

K1 已由项目端正式关闭。现在开始 K2，但**本轮仍禁止 Claim Extraction**。

你的唯一任务是：对 K1 的 515 条 canonical source 建立工作谱系 / 版本关系 / 派生关系，避免以后把同一本书的不同扫描、版本、笔记和代码误当成多个独立来源。

## 一、先同步仓库

执行：

```bash
git status --short
git fetch origin
git checkout knowledge-engine-v1
git pull --ff-only origin knowledge-engine-v1
```

必须 clean。若有未知改动，STOP。禁止 reset --hard / clean -fd。

确认存在：

- `knowledge/K1_FINAL_ACCEPTANCE.md`
- `knowledge/K2_SOURCE_LINEAGE_PROTOCOL.md`
- `knowledge/schema/source_lineage.schema.json`
- `tools/sanitize_k2_lineage.py`
- `tools/validate_k2_source_lineage.py`
- `tools/test_k2_source_lineage.py`

## 二、严格禁止

本轮禁止：

- 抽取任何术数规则 Claim；
- 总结整本书；
- 判断哪本书“更真”；
- 修改 App / 排盘算法 / Interpreter；
- 修改 validator 来迁就数据；
- 把 PDF、扫描页、OCR 全文、现代长文本提交 Git；
- 把 `knowledge-intake/` 提交 Git；
- 因为作者相同就假定两本书是同一 work；
- 因为标题相似就自动合并 work；
- 因为 SHA 不同就把两本版本当成独立证据。

## 三、输入

公开 sanitized registry：

- `knowledge/domains/ziwei/sources.jsonl`
- `knowledge/domains/bazi/sources.jsonl`
- `knowledge/domains/qimen/sources.jsonl`
- `knowledge/domains/liuyao/sources.jsonl`
- `knowledge/domains/liuren/sources.jsonl`
- `knowledge/domains/fengshui/sources.jsonl`

共 515 条，source_id 不得增删或重编号。

真实文件仍在本机 corpus；只有在 lineage 无法通过标题/已知元数据判断时，才打开标题页、版权页、目录或少量必要页面核验。不要做全文 OCR。

## 四、输出位置

先在本机生成：

`/home/joe/knowledge-intake/K2_SOURCE_LINEAGE_DRAFT.jsonl`

一条 canonical source 恰好一行，共 515 行。

字段只能：

```text
source_id
work_id
relation
parent_work_ids
independence_class
lineage_basis
lineage_evidence
k2_eligible
read_priority
review_status
```

禁止写 local_path、用户名、盘符、原文段落。

## 五、relation 定义

只能使用：

- `PRIMARY_WORK`：目前作为该 underlying work 的主记录；
- `SAME_WORK_VARIANT`：同一 underlying work 的另一扫描、排版、版本、整洁版等；
- `COMMENTARY_DERIVATIVE`：明确是对另一 work 的注、解、评、今注等派生作品；
- `SECONDARY_NOTE`：用户笔记 / AI 笔记 / 学习笔记；
- `IMPLEMENTATION`：项目代码/测试/实现；
- `AUXILIARY_INDEX`：目录、digest、索引等；
- `OUT_OF_SCOPE`：K1 已确认六术之外；
- `UNKNOWN`：无法可靠判断。

## 六、work_id 规则

全局格式：

`WORK-000001`

递增即可，但必须稳定、唯一。

同一个 underlying work 的不同版本必须使用同一个 `work_id`。

例如：

- 《某书》扫描版
- 《某书》整洁版
- 《某书》另一出版社排印版

如果经过标题页/目录确认只是同一作品不同载体，应共享 work_id。

但是：

- 《滴天髓》原典
- 《滴天髓今注》

不能仅因为名字接近就用同一个 work_id。今注若是独立现代著作，应有自己的 work_id，并用 `COMMENTARY_DERIVATIVE` + `parent_work_ids` 指向原 work。

如果 parent work 在当前 515 条里不存在，也不要编造不存在的 source；可以暂时使用一个独立 work_id 代表可确认的 parent work 概念，但必须 `lineage_basis=CONTENT_VERIFIED/MANUAL_VERIFIED`，否则 UNKNOWN。

## 七、independence_class

只能：

- `PRIMARY_CANDIDATE`
- `SAME_WORK_NOT_INDEPENDENT`
- `DERIVATIVE_REVIEW_REQUIRED`
- `IMPLEMENTATION_ONLY`
- `NOT_ELIGIBLE`
- `UNKNOWN`

规则：

`PRIMARY_WORK` 通常为 `PRIMARY_CANDIDATE`。

同一个 work_id 最多只能一条 `PRIMARY_CANDIDATE`。

`SAME_WORK_VARIANT` 必须为 `SAME_WORK_NOT_INDEPENDENT`。

`COMMENTARY_DERIVATIVE` 必须为 `DERIVATIVE_REVIEW_REQUIRED`，因为以后要在 claim 级别判断它是在复述 parent 还是提出独立解释。

`IMPLEMENTATION` 必须为 `IMPLEMENTATION_ONLY`。

`OUT_OF_SCOPE / AUXILIARY_INDEX` 必须为 `NOT_ELIGIBLE`。

`UNKNOWN` 使用 `UNKNOWN`。

## 八、evidence_role 映射硬规则

公开 Source Registry 中：

`SECONDARY_NOTE` → relation 必须 SECONDARY_NOTE，不能 PRIMARY_WORK。

`IMPLEMENTATION_EVIDENCE` → IMPLEMENTATION + IMPLEMENTATION_ONLY。

`AUXILIARY_INDEX` → AUXILIARY_INDEX + NOT_ELIGIBLE。

这些来源后续都不能被统计成传统书籍的独立“支持票”。

## 九、K1 semantic routing 必须尊重

如果 K1：

`knowledge_domains=["OUT_OF_SCOPE"]`

本轮必须：

```text
relation=OUT_OF_SCOPE
k2_eligible=false
read_priority=SKIP
independence_class=NOT_ELIGIBLE
```

不能重新把它塞回六术。

如果 K1 semantic domain 为 UNKNOWN，可以继续 UNKNOWN；不要为了提高覆盖率猜。

## 十、lineage_basis

只能：

- TITLE_MATCH
- CONTENT_VERIFIED
- MANUAL_VERIFIED
- HASH_PROVENANCE
- PROJECT_CODE_PATH
- UNKNOWN

标题明显相同但 SHA 不同，只能作为候选；若存在“整洁版/上中下册/出版社版”等，需要确认它们到底是同一完整 work、分册还是不同内容。

不要把作者相同当 lineage evidence。

## 十一、lineage_evidence

最多 240 字，只写独立重述的短依据，例如：

`标题页作品名相同，整洁版与扫描版目录章节一致`

不要复制现代书长段原文。

UNKNOWN：

```text
lineage_basis=UNKNOWN
lineage_evidence=null
```

## 十二、read_priority

用途是下一阶段阅读排程，不代表“这本书更正确”。

- `P0`：六术各自最基础、可读、语义明确、可能提供结构算法或完整案例的独立 textual work；
- `P1`：重要但需要扫描件定向阅读、或关键流派资料；
- `P2`：后续专题/案例/现代 commentary；
- `P3`：低优先但仍需最终吸收的合法来源；
- `SKIP`：OUT_OF_SCOPE / AUXILIARY 等当前不进入六术阅读管线。

必须六术均衡：不能把奇门全部 P0/P1，而六爻、六壬、风水全部拖后。

对于薄 corpus：六爻、大六壬的有效 textual work 应优先纳入 P0/P1，而不是因为书少降低优先级。

## 十三、不要把“版本多”当“证据多”

特别扫描：

- 同书整洁版 / 原扫描版；
- 同一古籍不同现代扫描；
- 上中下册是否是一个 work 的分卷还是三个独立作品；
- 同一内容的现代重排；
- 笔记是否由某本书直接派生；
- 项目代码是否由旧 handoff / notes 派生。

K2 后续 cross-verification 按 independent work/claim lineage 计算，不按文件数投票。

## 十四、使用 official sanitizer

完成本地 515 行 draft 后执行：

```bash
python3 tools/sanitize_k2_lineage.py \
  /home/joe/knowledge-intake/K2_SOURCE_LINEAGE_DRAFT.jsonl \
  --repo-root .
```

必须：

```text
k2-lineage-sanitize: PASS
sources=515
```

它会生成：

`knowledge/K2_SOURCE_LINEAGE.jsonl`

禁止手工复制为最终文件。

## 十五、机器验收

先保持：

`knowledge/K2_SOURCE_LINEAGE_STATE.json.status = REVIEW_REQUIRED`

运行：

```bash
python3 tools/test_k2_source_lineage.py
python3 tools/validate_k2_source_lineage.py
```

如果数据无结构错误，validator 应显示 REVIEW_REQUIRED，而不是假装 COMPLETE。

然后人工自审至少：

- 每个正式 domain 10 条（不足 10 条则全部）；
- 每个 SAME_WORK family 至少抽 1 组；
- 每个 COMMENTARY_DERIVATIVE 至少抽查 1 个 parent link；
- 所有 OUT_OF_SCOPE；
- 所有 UNKNOWN 中随机至少 10 条；
- 所有 IMPLEMENTATION / SECONDARY_NOTE 映射。

只有自审通过，才可把：

`K2_SOURCE_LINEAGE_STATE.status = COMPLETE`

但仍保持：

`claim_extraction_blocked=true`

随后执行：

```bash
python3 tools/validate_k2_source_lineage.py --force
python3 tools/validate_knowledge.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

必须全 PASS。

## 十六、提交边界

本轮允许提交：

- `knowledge/K2_SOURCE_LINEAGE.jsonl`
- `knowledge/K2_SOURCE_LINEAGE_STATE.json`

如状态文档生成需要，可提交 `knowledge/STATUS.md`，但不要修改 claims/evidence/fixtures。

禁止提交：

- `knowledge-intake/`
- PDF / EPUB / 扫描 / OCR
- App / 算法
- claims / evidence / fixtures / interpretation
- validator / tests（除非项目端另行要求）

push `origin/knowledge-engine-v1` 后停止。

## 十七、最终回报

只回报：

1. commit SHA
2. lineage rows 是否 515
3. distinct work_id 数
4. PRIMARY_WORK 数
5. SAME_WORK_VARIANT 数
6. COMMENTARY_DERIVATIVE 数
7. SECONDARY_NOTE 数
8. IMPLEMENTATION 数
9. AUXILIARY_INDEX 数
10. OUT_OF_SCOPE 数
11. UNKNOWN 数
12. independence_class 分布
13. P0/P1/P2/P3/SKIP 分布，按六术语义域拆分
14. 最大的 20 个 same-work family（work_id + source_ids）
15. commentary parent link 数及 unresolved 数
16. 自审样本结果
17. `test_k2_source_lineage.py`
18. `validate_k2_source_lineage.py --force`
19. `validate_knowledge.py`
20. `generate_knowledge_status.py --check`
21. `:ziwei-core:test`
22. git status 是否 clean
23. 实际 commit 文件列表

严禁开始 Claim Extraction。
