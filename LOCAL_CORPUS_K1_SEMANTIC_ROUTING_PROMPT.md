# LOCAL_CORPUS_K1_SEMANTIC_ROUTING_PROMPT

你现在负责 Xuanxue Knowledge Engine v1 的 `K1_SEMANTIC_ROUTING_REVIEW`。

严禁开始 K2 Claim Extraction。严禁修改 App/排盘算法/Interpretation。严禁修改 validator 来迁就数据。严禁提交 `knowledge-intake/`、原书、扫描页、OCR 全文。

## 当前已通过

- K1 local index: PASS
- 911 scanned / 542 distinct SHA / 515 canonical / 345 duplicates / 51 excluded
- K1 attribution/source-quality: PASS, issues=0
- sanitized registry structure/privacy: PASS

## 项目端复验发现的新问题

此前 `domain` 实际上同时承担了“文件在哪个本地资料目录被发现”和“这份资料真正属于哪个术数领域”两个含义。这会污染 K2。

已确认例子：

- `BZ-SRC-0114/0115` 是 `梅花心易实战详解`，不能因为文件位于八字资料目录就送入八字 Claim Extraction。
- `BZ-SRC-0122` 是 `火珠林密本（古本）`，必须重新确认实际 semantic domain；不能按八字目录归类。
- `FS-SRC-0011` 是 `周易變占法引論`，不能因为位于风水资料目录就自动归入风水。
- `FS-SRC-0012` 是 `揭露铁板神数之内幕`，不得自动归入风水。
- `LR-SRC-0001/0002` 文件名明确区分 `袁树珊撰 / 谢路军主编 / 邓同校`；`主编/校者` 不能一起写入 `author`。

## 新字段

对全部 515 条 private intake source 增加：

`knowledge_domains`

允许值：

- ziwei
- bazi
- qimen
- liuyao
- liuren
- fengshui
- common
- OUT_OF_SCOPE
- UNKNOWN

可多域，但：

- UNKNOWN 不能与其他值并存；
- OUT_OF_SCOPE 不能与六术域并存。

`domain_basis`

只能：

- TITLE_FILENAME
- CONTENT_VERIFIED
- MANUAL_VERIFIED
- PROJECT_CODE_PATH
- UNKNOWN

`domain_evidence`

只写短证据，不复制现代书正文。

## semantic domain 判断规则

禁止根据父目录、资料合集目录、相邻文件、作者常见研究领域、模型常识直接决定 semantic domain。

优先级：

1. CONTENT_VERIFIED：实际查看可读正文/目录/标题页，确认它研究的术数领域；
2. TITLE_FILENAME：文件自身标题已经明确写出领域，例如“奇门”“紫微斗数”“大六壬”“六爻”“八字”“玄空风水”；
3. PROJECT_CODE_PATH：仅项目代码可根据明确模块路径/类名归域；
4. MANUAL_VERIFIED：人工有直接证据；
5. 无法确认 → knowledge_domains=["UNKNOWN"]。

如果明确是六术之外的独立体系，如梅花易数、铁板神数，而本项目暂时没有该正式 domain：

`knowledge_domains=["OUT_OF_SCOPE"]`

不要为了留在六域中强行归类。

如果一份资料真实同时覆盖多个六术领域，可以列多个 knowledge_domains，但必须有直接 evidence。

## registry domain 与 semantic domain

现有 `domain` 和 source_id 前缀先保持不变，作为 stable registry bucket / provenance identity，不重新编号 515 条 source。

以后 K2 只能按 `knowledge_domains` 选择资料，不能按 `domain` 或本地文件夹直接选择。

因此允许：

`source_id=BZ-SRC-0122`
`domain=bazi`
`knowledge_domains=["liuyao"]`

前提是内容证据确实支持。

## author 角色复核

本轮再次检查所有非 UNKNOWN author。

文件名中出现一个人名，不等于这个人一定是作者。

如果标题明确写：

- 著 / 撰 / 编著 / 作者 → 可作为 author；
- 主编 / 点校 / 校 / 校订 / 译 / 整理 / 编校 → 不是 author，不得并入 author。

例如：

`袁树珊撰 谢路军主编 邓同校`

应至少保证：

`author = 袁树珊`

不能把谢路军、邓同并入 author。

若文件名只是 `梁湘润-某古本`，但没有可靠证据说明梁湘润是该古本原作者，宁可：

`author=UNKNOWN`

不要把“文件名关联者/整理者/讲解者”自动当原作者。

## 执行步骤

1. 同步 `origin/knowledge-engine-v1` 最新 head。
2. `git status --short` 必须 clean。
3. 逐条修改 `/home/joe/knowledge-intake/<domain>/sources.jsonl` 的 515 个 canonical source。
4. 保持 source_id、file_sha256、canonical 数量不变；不要为了 semantic routing 新建重复 source。
5. 重新运行：

```bash
python3 tools/validate_k1_intake.py /home/joe/knowledge-intake --write-summary /home/joe/knowledge-intake/K1_VALIDATION_RESULT.json

python3 tools/sanitize_k1_sources.py /home/joe/knowledge-intake --repo-root . --manifest knowledge/K1_SANITIZED_IMPORT.json

python3 tools/validate_sanitized_k1.py --force
python3 tools/validate_k1_source_quality.py --force
python3 tools/test_k1_source_quality.py
python3 tools/test_k1_semantic_routing.py
python3 tools/validate_k1_semantic_routing.py --force
python3 tools/validate_knowledge.py
```

最关键 Gate：

`k1-semantic-routing: PASS`
`sources=515 issues=0`

6. 即使 issues=0，也先保持 `k2_blocked=true`，等待项目端复验。
7. 将 `PROJECT_STATE` 设为：

- phase = `K1_SEMANTIC_ROUTING_COMPLETE`
- sanitized_import = `COMPLETE`
- source_quality = `COMPLETE`
- semantic_routing = `COMPLETE`
- k2_blocked = `true`

8. 重新生成并检查 STATUS；运行 `./gradlew --no-daemon :ziwei-core:test`。
9. 只提交 sanitized metadata、PROJECT_STATE、STATUS；不要提交 private intake。

## 完成后回报

只回报：

1. commit SHA
2. 六域 source 数与 total
3. `validate_k1_intake.py`
4. `validate_sanitized_k1.py --force`
5. `validate_k1_source_quality.py --force`
6. `validate_k1_semantic_routing.py --force`
7. semantic routing issues 最终数量
8. `knowledge_domains` 分布：六域/common/OUT_OF_SCOPE/UNKNOWN 各多少
9. 与 registry `domain` 不同的 source 数及 source_id 列表
10. OUT_OF_SCOPE source 列表
11. UNKNOWN semantic domain 数与原因
12. author 因“主编/校/译/整理/关联者”再次 reset 的数量和 source_id
13. manifest registry hash 检查结果
14. `validate_knowledge.py`
15. `generate_knowledge_status.py --check`
16. `:ziwei-core:test`
17. git status 是否 clean
18. commit 文件列表

不要开始 K2。
