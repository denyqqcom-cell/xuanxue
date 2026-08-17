# Local Corpus K1 — Sanitized Import Prompt

把下面整段转发给能访问 `/home/joe/knowledge-intake/` 与本机 `xuanxue` checkout 的 AI。

---

你现在负责 Xuanxue Knowledge Engine v1 的 **K1_SANITIZED_IMPORT**。

前置事实：

- `/home/joe/knowledge-intake/` 已通过 `tools/validate_k1_intake.py`，结果 `k1-intake: PASS`。
- accounting 已对齐：911 scanned / 542 distinct SHA / 515 canonical / 345 duplicate / 51 excluded。
- 六域 `K1_INDEX_STATUS` 全部 PASS。
- **禁止开始 K2 Claim Extraction。**
- 本轮唯一目标：把本机 canonical source 的“安全元数据”导入 GitHub 可审计的 `knowledge/`，让项目真正吸收 Source Registry，但不上传原书、路径、扫描、OCR 或现代长文本。

## 1. 同步正确分支

在本机 xuanxue 仓库执行：

```bash
git status --short
git fetch origin
git checkout knowledge-engine-v1
git pull --ff-only origin knowledge-engine-v1
```

开始前 worktree 必须 clean。若不 clean，STOP，不要 reset/clean 掉未知改动。

## 2. 再跑一次本地 K1 Gate

```bash
python3 tools/validate_k1_intake.py \
  /home/joe/knowledge-intake \
  --write-summary /home/joe/knowledge-intake/K1_VALIDATION_RESULT.json
```

必须看到：

`k1-intake: PASS`

否则 STOP。

## 3. 使用项目官方 sanitizer

禁止手工复制 `sources.jsonl`。

运行：

```bash
python3 tools/sanitize_k1_sources.py \
  /home/joe/knowledge-intake \
  --repo-root . \
  --manifest knowledge/K1_SANITIZED_IMPORT.json
```

它只能生成/更新：

- `knowledge/domains/ziwei/sources.jsonl`
- `knowledge/domains/bazi/sources.jsonl`
- `knowledge/domains/qimen/sources.jsonl`
- `knowledge/domains/liuyao/sources.jsonl`
- `knowledge/domains/liuren/sources.jsonl`
- `knowledge/domains/fengshui/sources.jsonl`
- `knowledge/K1_SANITIZED_IMPORT.json`

Sanitizer 必须剥离：

- `local_path`
- `size_bytes`
- `sampled_locations`
- `notes`
- `/home/...`、`/mnt/...`、Windows 盘符路径等本机定位信息

保留的只是可审计来源元数据，例如 source_id、title、author、type、era、edition、hash、pages、readability、school_ids、copyright、status。

## 4. 强制验收 sanitized registry

```bash
python3 tools/validate_sanitized_k1.py --force
python3 tools/test_k1_sanitization.py
python3 tools/validate_knowledge.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

全部必须 PASS。

## 5. 人工检查泄漏与版权边界

运行：

```bash
git status --short
git diff --stat
git diff -- knowledge/K1_SANITIZED_IMPORT.json

grep -RInE '(/home/|/mnt/|[A-Za-z]:\\)' knowledge/domains/*/sources.jsonl || true
find knowledge -type f \( -iname '*.pdf' -o -iname '*.epub' -o -iname '*.doc' -o -iname '*.docx' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' -o -iname '*.ttf' -o -iname '*.otf' \) -print
```

要求：

- grep 不得命中真实本机路径；
- find 不得发现新增研究二进制；
- 不得出现原书正文、OCR 长段、扫描、完整现代作者表格/图解；
- 不得擅自修改 App、算法、Claim、Fixture、Interpretation。

## 6. 数量必须精确

sanitized source 数必须为：

- ziwei = 148
- bazi = 168
- qimen = 154
- liuyao = 7
- liuren = 10
- fengshui = 28
- total = 515

任何差异都 STOP，不能为了对数补造 source。

## 7. Git 提交边界

这次**允许**把 sanitized metadata 提交到 `knowledge-engine-v1`，因为它已经经过项目 sanitizer；但 `knowledge-intake/` 仍绝对禁止提交。

提交前：

```bash
git status --short
```

允许的业务改动仅限上述 7 个 sanitized import 文件。若出现其他未知改动，STOP。

然后：

```bash
git add \
  knowledge/K1_SANITIZED_IMPORT.json \
  knowledge/domains/ziwei/sources.jsonl \
  knowledge/domains/bazi/sources.jsonl \
  knowledge/domains/qimen/sources.jsonl \
  knowledge/domains/liuyao/sources.jsonl \
  knowledge/domains/liuren/sources.jsonl \
  knowledge/domains/fengshui/sources.jsonl

git commit -m "knowledge: import sanitized K1 source registries"
git push origin knowledge-engine-v1
```

不要提交 `/home/joe/knowledge-intake/`，不要提交原书。

## 8. 完成后只回报

回报：

1. commit SHA；
2. `git status --short` 是否 clean；
3. `validate_k1_intake.py` 结果；
4. `sanitize_k1_sources.py` 结果与六域数量；
5. `validate_sanitized_k1.py --force` 结果；
6. `test_k1_sanitization.py` 结果；
7. `:ziwei-core:test` 结果；
8. 路径泄漏 grep 是否 0 命中；
9. 研究二进制 find 是否 0 命中；
10. 实际提交文件列表。

**不要开始 K2。** 项目端会在 GitHub 上再次读取这 515 条 sanitized registry、跑 CI、检查 source/hash/count/privacy/copyright，然后才决定是否把六域正式升级到 `L1_INDEXED` 并解除 K2 Gate。

---
