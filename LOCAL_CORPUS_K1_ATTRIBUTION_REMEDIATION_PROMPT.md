# K1 Attribution Remediation — local AI handoff

你现在负责 Xuanxue Knowledge Engine v1 的 `K1_ATTRIBUTION_REVIEW`。

本轮**不是 K2**。不要抽取术数规则、不要写 Claim、不要改 App/算法。

当前事实：

- `/home/joe/knowledge-intake/` 已通过 `validate_k1_intake.py`；
- 911 scanned / 542 distinct SHA / 515 canonical / 345 duplicates / 51 excluded；
- 515 条 sanitized metadata 已进入 `knowledge-engine-v1`；
- 数量、SHA 唯一性、隐私路径、二进制版权边界均已通过；
- 项目端独立抽样发现 **author / school / pages / enum / title quality** 污染，因此 K2 继续 BLOCKED。

## 1. 先同步准确分支

```bash
git status --short
git fetch origin
git checkout knowledge-engine-v1
git pull --ff-only origin knowledge-engine-v1
```

worktree 必须 clean。禁止 `reset --hard` / `clean -fd`。

## 2. 必须理解的错误类型

项目端已直接在 GitHub 发现以下例子：

- `BZ-SRC-0003` 标题是 `八字论命苏民峰`，author 却是 `王亭之 / 苏民峰`；
- `BZ-SRC-0009` 标题是 `韦千里 - 千里命稿`，author 却是 `王亭之 / 韦千里`；
- `LY-SRC-0001/0002/0003` 的 `六爻新大陸 / 卜筮正宗 / 增刪卜易` 都被写成 author=`王亭之`；
- `QM-SRC-0001` `梁湘润-奇门遁甲入门` 被写成 `王亭之 / 梁湘润`；
- 多本梁湘润风水书被写成 `王亭之 / 梁湘润`；
- 六壬若干资料的 author 字段混入 `王亭之`，甚至编辑/校者姓名与标题不一致；
- `_books_digest`、`_books_toc`、Markdown 笔记、代码文件的 `pages` 很可能是行数，不是真实页数；
- 部分 title 含 `www.*`、`更多教程加微信...` 等分发/广告噪声；
- 当前 sanitized rows 使用 `modern`、`modern_publication_or_scan` 等值，与 canonical Source schema 不一致。

这些不是“格式小问题”，会直接污染以后 Claim 的来源、流派和证据权重。

## 3. 作者归属硬规则

**绝对禁止**从以下信息推作者：

- 父目录/祖先目录名称；
- “王亭之全集”“梁湘润目录”等 collection folder；
- 相邻文件作者；
- 某作者常用流派；
- 模型常识；
- 旧 AI 笔记里的未经核实归属。

author 只允许使用以下证据：

- `FILENAME`：当前文件名/可公开 canonical title 明确包含作者；
- `EMBEDDED_METADATA`：文件自身 metadata 明确给作者；
- `TITLE_PAGE`：实际打开原文件 title page/版权页确认；
- `MANUAL_VERIFIED`：有独立人工证据。

无法满足就：

```json
"author": "UNKNOWN",
"author_basis": "UNKNOWN",
"author_evidence": null
```

不要为了“资料完整”保留猜测作者。

如果 author 非 UNKNOWN，必须增加：

```json
"author_basis": "FILENAME|EMBEDDED_METADATA|TITLE_PAGE|MANUAL_VERIFIED",
"author_evidence": "不超过240字符的短证据说明"
```

若 `author_basis=FILENAME`，author 中每一个姓名都必须真的出现在当前 canonical title/文件名里。

## 4. 流派 school_ids 硬规则

禁止因为“某作者通常属于某派”自动写 school。

非 UNKNOWN school 只能来自：

- `FILENAME`
- `TITLE_PAGE`
- `CONTENT_VERIFIED`
- `MANUAL_VERIFIED`

必须增加：

```json
"school_basis": "...",
"school_evidence": "短证据"
```

如果只是作者推断、目录推断、模型记忆：

```json
"school_ids": ["UNKNOWN"],
"school_basis": "UNKNOWN",
"school_evidence": null
```

例如标题明确写“中州派”才能在 K1 直接保留中州派；其他情况宁可 UNKNOWN，留到 K2 阅读后再升级。

## 5. pages 字段硬规则

`pages` 只表示**真实文档页数**。

允许：

- PDF parser 得出的页数 → `PDF_PAGE_COUNT`
- 真正分页文档的页数 → `DOCUMENT_PAGE_COUNT`
- 人工核对页数 → `MANUAL_VERIFIED`

必须增加：

```json
"pages_basis": "PDF_PAGE_COUNT|DOCUMENT_PAGE_COUNT|MANUAL_VERIFIED"
```

对于：

- `.md`
- `.txt`
- `.py`
- `.kt`
- `.json/.jsonl`
- `_books_digest`
- `_books_toc`
- 代码/索引

如果当前数字其实是行数/字符数，必须：

```json
"pages": null,
"pages_basis": "UNKNOWN"
```

不要把 line count 继续叫 pages。

## 6. era 统一 canonical enum

只能使用：

```text
ANCIENT
PRE_MODERN
MODERN
UNKNOWN
```

禁止：

```text
modern
pre_1950_text_in_modern_file
```

如果只能确认“现代文件里装着古籍”，`era` 描述的是**内容/作品时代**；文件扫描/排版权利由 copyright 字段处理。

无法确认作品时代就 UNKNOWN。

## 7. copyright 统一 canonical enum

只能使用：

```text
PUBLIC_DOMAIN_TEXT_ONLY
LICENSED
RESEARCH_ONLY
UNKNOWN
FORBIDDEN_TO_PACKAGE
```

保守映射原则：

- 现代出版物/现代扫描 → `FORBIDDEN_TO_PACKAGE`
- 古籍原文但文件为现代扫描/现代排版，且扫描/排版权利未确认 → `RESEARCH_ONLY` 或更严格 `FORBIDDEN_TO_PACKAGE`
- 用户学习笔记如果可能含现代书摘录/派生内容 → `RESEARCH_ONLY`
- 本项目明确 MIT 代码 → `LICENSED`
- 仅“古籍文字本身公版”且不会误把现代扫描/标点/校注一起授权时，才可 `PUBLIC_DOMAIN_TEXT_ONLY`
- 不确定 → `UNKNOWN`

**不要把 user_owned_notes / modern_publication_or_scan / project_or_mit_code 等旧标签直接带入公开 registry。**

## 8. evidence_role 必须补齐

每条 source 都必须明确其证据角色：

- BOOK / COURSE / ANCIENT_TEXT / ARTICLE / CASE_COLLECTION → `TEXTUAL_SOURCE`
- NOTE → `SECONDARY_NOTE`
- CODE → `IMPLEMENTATION_EVIDENCE`
- OTHER → `AUXILIARY_INDEX`

这不是可靠性评级。

尤其：

- `SECONDARY_NOTE` 不能在 K2 冒充独立原书证据；
- `IMPLEMENTATION_EVIDENCE` 只能证明代码/实现，不证明传统术理真值；
- `AUXILIARY_INDEX` 只用于导航/检索。

## 9. canonical title 清洗

保留能识别资料的书名/文件标题，但去掉明显分发噪声，例如：

- `www.xxx`
- 下载站后缀
- `更多教程加微信...`
- QQ/微信广告
- 非书名性质的推广文本

不要擅自把 UNKNOWN 书名改成模型记忆中的“标准书名”。

如果不能确认，保留最小可识别标题，不补作者/出版社。

## 10. 对 515 条逐条执行，不只修项目端举例

必须检查六域全部 515 canonical source：

- ziwei 148
- bazi 168
- qimen 154
- liuyao 7
- liuren 10
- fengshui 28

项目端例子只是暴露系统性问题，不是修完这些 ID 就结束。

优先用脚本批量发现：

- author 中含 `/` 的行；
- author 非 UNKNOWN 但文件名/title 不含作者的行；
- non-canonical era/copyright；
- pages 非 null 但来源为代码/Markdown/索引的行；
- title 含 www/微信/QQ/URL 的行；
- school_ids 非 UNKNOWN 但无直接证据的行。

然后逐项按证据修正。

## 11. 修改位置

先修本地 private intake：

```text
/home/joe/knowledge-intake/<domain>/sources.jsonl
```

允许增加：

- author_basis
- author_evidence
- school_basis
- school_evidence
- pages_basis
- evidence_role

不要删除 `local_path` 等本地审计字段；它们仍留在 private intake，sanitizer 会剥离。

不要直接手工编辑 GitHub 的六个 sanitized registries作为最终解决方案。

## 12. 重新跑 K1 local validator

修完 private intake 后：

```bash
python3 tools/validate_k1_intake.py \
  /home/joe/knowledge-intake \
  --write-summary /home/joe/knowledge-intake/K1_VALIDATION_RESULT.json
```

必须继续：

```text
k1-intake: PASS
```

515 canonical / 345 duplicates 的 identity/hash accounting 不应因 metadata cleanup 改变。

## 13. 重新生成 sanitized registry

只能运行官方 sanitizer：

```bash
python3 tools/sanitize_k1_sources.py \
  /home/joe/knowledge-intake \
  --repo-root . \
  --manifest knowledge/K1_SANITIZED_IMPORT.json
```

然后必须运行：

```bash
python3 tools/validate_sanitized_k1.py --force
python3 tools/validate_k1_source_quality.py --force
python3 tools/test_k1_sanitization.py
python3 tools/test_k1_source_quality.py
python3 tools/validate_knowledge.py
```

其中最关键的是：

```text
k1-source-quality: PASS
sources=515 issues=0
```

任何 issue 不得通过修改 validator 绕过。

## 14. 更新项目状态仅在 zero issue 之后

只有 `validate_k1_source_quality.py --force` = PASS 后，才允许把：

```json
"phase": "K1_ATTRIBUTION_REVIEW",
"sanitized_import": "STRUCTURAL_PASS",
"source_quality": "REVIEW_REQUIRED",
"k2_blocked": true
```

更新为：

```json
"phase": "K1_PROJECT_IMPORT_COMPLETE",
"sanitized_import": "COMPLETE",
"source_quality": "COMPLETE",
"k2_blocked": true
```

**仍然保持 k2_blocked=true。**

项目端还要再次审核后才解锁 K2。

更新状态后运行：

```bash
python3 tools/generate_knowledge_status.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

全部 PASS。

## 15. Git diff / 提交边界

本轮允许修改：

- `/home/joe/knowledge-intake/*/sources.jsonl`（本机，不提交）
- `knowledge/K1_SANITIZED_IMPORT.json`
- 六域 `knowledge/domains/*/sources.jsonl`
- `knowledge/PROJECT_STATE.json`
- `knowledge/STATUS.md`

不要改：

- App
- 排盘算法
- claims
- fixtures
- interpretation
- 原始书文件
- OCR 正文

提交前：

```bash
git status --short
git diff --stat
```

确认没有 `knowledge-intake/`。

提交建议：

```bash
git add knowledge/K1_SANITIZED_IMPORT.json \
  knowledge/PROJECT_STATE.json \
  knowledge/STATUS.md \
  knowledge/domains/*/sources.jsonl

git commit -m "knowledge: remediate K1 source attribution metadata"
git push origin knowledge-engine-v1
```

## 16. 完成后停止，不开始 K2

只回报：

1. commit SHA
2. 六域 source 数和 total
3. `validate_k1_intake.py` 结果
4. `validate_sanitized_k1.py --force` 结果
5. `validate_k1_source_quality.py --force` 结果和 issue 数
6. `test_k1_source_quality.py` 结果
7. `validate_knowledge.py` 结果
8. `generate_knowledge_status.py --check` 结果
9. `:ziwei-core:test` 结果
10. 修正统计：
   - author reset to UNKNOWN 数量
   - author verified 数量与 basis 分布
   - school reset/verified 数量
   - pages nulled 数量
   - era normalization 数量
   - copyright normalization 数量
   - title cleanup 数量
11. `git status --short` 是否 clean
12. 实际 commit 文件列表

不要开始 K2。项目端会再做一次 GitHub 独立抽样和机器闭环。
