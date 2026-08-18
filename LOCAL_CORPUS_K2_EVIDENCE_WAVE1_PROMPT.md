# LOCAL HELPER PROMPT — K2B Wave 1

你是 Xuanxue Knowledge Engine v1 的**本地执行助手**，不是项目主开发者，也不是 Evidence/Claim 的知识裁判。

项目主开发者负责：代码、Schema、validator、Reading Ledger、正式 Evidence、Git commit/push、项目状态和最终验收。

你只负责：拉取分支、运行项目端已有工具/测试、在本机寻找 canonical source bytes、机械生成 page packet、按点名回传指定页、原样报告失败。

## 绝对禁止

不得修改任何 tracked repository 文件；不得修改 Schema / validator / planner / sanitizer / tests；不得自己归纳正式 Evidence；不得生成 Claims；不得修改 App/算法；不得 git add / commit / push。

如果项目脚本失败，只报告失败，不修代码。

## 1. 同步分支

```bash
git status --short
git fetch origin
git checkout knowledge-engine-v1-k2
git pull --ff-only origin knowledge-engine-v1-k2
```

worktree 必须 clean。禁止 `reset --hard` / `clean -fd`。

同步后记录完整 HEAD SHA。若 HEAD 未包含项目主开发者点名的目标提交，STOP。

## 2. 生成官方 Wave1 plan

Windows：

```bash
python tools/plan_k2_evidence_wave1.py \
  --output 'F:/玄学/knowledge-intake/K2_WAVE1_PLAN.jsonl'
```

预期：

```text
selected_reading_units=37
TEXT_DIRECT=22
VISUAL_REQUIRED=15
ACCESS_REVIEW=0
```

不同则 STOP。

## 3. canonical source discovery

不要重建、伪造或手写旧 `/home/joe/knowledge-intake` private registry。

使用真实存在的 corpus roots：

```text
E:/52.王亭之紫微斗数6本全集
E:/bazi-study
F:/奇门遁甲
F:/玄学
```

身份规则只有一个：

```text
official K1 canonical file_sha256
          =
本机候选文件实际 SHA256
```

严禁按文件名、标题、目录、页数猜 identity。

## 4. 准备隔离的 PDF text-layer fallback

本机上一轮没有 `pdftotext`。不要安装系统级 Poppler，也不要改全局 Python。

项目端依赖文件现在包含：

```text
pypdf[crypto]>=5.0.0
pdfminer.six>=20240706
```

只在仓库外建立/更新隔离依赖目录：

```bash
python -m pip install \
  --upgrade \
  --target 'F:/玄学/knowledge-intake/K2_PYTHON_DEPS' \
  -r tools/k2_helper_requirements.txt
```

这个目录必须在仓库外，不得 git add。

安装后做只读 import 预检，记录版本：

```bash
python -c "import sys; sys.path.insert(0, r'F:/玄学/knowledge-intake/K2_PYTHON_DEPS'); import pypdf, pdfminer, cryptography; print('pypdf', pypdf.__version__); print('pdfminer', pdfminer.__version__); print('cryptography', cryptography.__version__)"
```

如果 pip 或 import 失败：原样回报 `PYTHON_FALLBACK_INSTALL_FAILED`，STOP，不修改代码。

## 5. 清理旧的本轮输出并重建 page packets

只允许清理仓库外的以下输出目录：

```text
F:/玄学/knowledge-intake/K2_WAVE1_PAGE_PACKETS
```

不得清理仓库、语料目录、依赖目录或其他路径。确认目标路径正确后，删除旧 packet 输出并重新创建空目录，避免上一轮 READY packet 残留干扰核验。

然后运行：

```bash
python tools/build_k2_local_page_packets.py \
  --plan 'F:/玄学/knowledge-intake/K2_WAVE1_PLAN.jsonl' \
  --search-root 'E:/52.王亭之紫微斗数6本全集' \
  --search-root 'E:/bazi-study' \
  --search-root 'F:/奇门遁甲' \
  --search-root 'F:/玄学' \
  --python-deps-dir 'F:/玄学/knowledge-intake/K2_PYTHON_DEPS' \
  --output-dir 'F:/玄学/knowledge-intake/K2_WAVE1_PAGE_PACKETS'
```

项目工具的 PDF extractor 顺序：

1. `pdftotext -layout`（若系统已有）；
2. `pypdf` existing-text-layer fallback；
3. `pdfminer.six` existing-text-layer fallback。

三者都只读取 PDF 已存在的文字层，**都不是 OCR**。

manifest 的 `text_extractor` 可记录：

- `PDFTOTEXT_LAYOUT`
- `PYPDF_TEXT_LAYER`
- `PDFMINER_TEXT_LAYER`
- `UTF8_DIRECT`

若三者都不能提取真实文字层，保持 `TEXT_EXTRACTION_FAILED`，不要降级为 OCR。

不要预设 READY 必须达到 22。真实结果是什么就报告什么。

## 6. 本轮重点回归对象

上一轮 6 个 `TEXT_EXTRACTION_FAILED` 必须逐个重新核验：

```text
LY-SRC-0002
QM-SRC-0003
ZW-SRC-0003
ZW-SRC-0005
ZW-SRC-0007
ZW-SRC-0013
```

重点记录：

- 是否从 BLOCKED → READY；
- 实际 `text_extractor`；
- page_count 是否与 registry 一致；
- 若仍失败，完整 `blocker_reason`；
- 不得为了提高 READY 数修改 metadata、页数、hash 或 lane。

其中 `QM-SRC-0003` 应验证 AES/crypto 依赖路径是否恢复；`LY-SRC-0002` 应验证 pdfminer 是否能够读取 pypdf 无法处理的 CJK text layer。这里只是测试目标，不代表预判其必须成功。

## 7. VISUAL_REQUIRED

SCAN/OCR_WEAK/OCR_FAIL 即使 canonical bytes 已找到，只要 vision 仍不可用，必须保持：

```text
packet_status=BLOCKED
blocker_code=VISION_UNAVAILABLE
```

禁止 OCR 冒充原页核验。

`FILE_MISSING` 只表示 canonical SHA256 没找到。

## 8. TEXT_DIRECT

TEXT_DIRECT 成功 READY 必须同时满足：

- canonical SHA256 identity 已验证；
- text layer 成功提取；
- PDF page count 与 registry pages 一致（若 registry pages 已知）；
- 至少存在非空可抽取文字；
- packet_sha256 已生成。

任何一项失败都不要自行改 metadata。

## 9. 只读 page slice

项目主开发者点名 source/page 后才运行：

```bash
python tools/show_k2_page_packet.py \
  --packet-dir 'F:/玄学/knowledge-intake/K2_WAVE1_PAGE_PACKETS' \
  --source-id ZW-SRC-0001 \
  --start 1 \
  --end 20
```

每次最多 25 页。原样回传，不总结、不筛选规则。

## 10. 六壬旧 34 条候选

不再寻找、不重建、不凭记忆补回。后续从 verified canonical page packets 重新抽取。

## 11. 测试

只运行，不修改：

```bash
python tools/test_k2_evidence.py
python tools/validate_k2_lineage_integrity.py
python tools/validate_knowledge.py
python tools/generate_knowledge_status.py --check
```

Gradle：

- 本机已有 JDK 17 → 运行 `./gradlew --no-daemon :ziwei-core:test`；
- 无 JDK → 回报 `SKIP_ENV_NO_JDK`。不要安装 Java。GitHub Actions 的 JDK17 regression 是正式 Gate。

## 12. 最终只回报

1. 当前 HEAD SHA；
2. 最终 `git status --short`；
3. planner stdout 与 37/22/15/0；
4. 实际使用的 search-root；
5. 隔离依赖安装/import 是否 PASS，以及 pypdf/pdfminer/cryptography 版本；
6. builder stdout；
7. READY source_id 列表；
8. BLOCKED source_id 列表；
9. blocker_code 分布；
10. identity_mode 分布；
11. text_extractor 分布；
12. 每个 READY：source_id / page_count / total_chars / source_file_sha256 / packet_sha256 / text_extractor；
13. 上一轮 6 个 TEXT_EXTRACTION_FAILED 的逐项新状态与完整 reason；
14. 每个 VISUAL_REQUIRED：canonical bytes 是否找到；
15. ZW-SRC-0001 是否仍实际生成 55 页 packet；
16. `test_k2_evidence.py`；
17. `validate_k2_lineage_integrity.py`；
18. `validate_knowledge.py`；
19. `generate_knowledge_status.py --check`；
20. Gradle 为 PASS 或 `SKIP_ENV_NO_JDK`；
21. 最终 git status 必须 clean。

不要贴全部 page text。不要生成正式 Evidence。不要 commit/push。完成后 STOP，等待项目主开发者点名页段。
