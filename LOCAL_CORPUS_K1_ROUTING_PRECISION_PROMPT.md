# Local Corpus K1 — Semantic Routing Precision Remediation

继续执行 Xuanxue Knowledge Engine v1。

本轮唯一任务：修复 K1 Semantic Routing 最后 7 条高风险记录。

严禁开始 K2 Claim Extraction。
严禁抽取新的术数规则。
严禁修改 App、排盘算法、Interpreter。
严禁修改 validator 来迁就数据。
严禁提交 knowledge-intake。
严禁上传原书、扫描页、全文 OCR。

## 一、先同步最新版

进入本机 xuanxue 仓库：

```bash
git status --short
git fetch origin
git checkout knowledge-engine-v1
git pull --ff-only origin knowledge-engine-v1
```

`git status --short` 必须 clean。

如果存在未知改动：STOP。
禁止 `reset --hard` / `clean -fd`。

最新版已经修复项目端 validator 的两个误区：

1. `TITLE_FILENAME` 不再把已确认作者姓名中的术数词当成 work-title domain evidence，例如 `紫微杨` 中的 `紫微`；
2. validator 已识别历史混合文件名 `紫wei斗shu`、英语代码标识 `BaziRules`、以及已确认的 OUT_OF_SCOPE 标识如 `京房易/周易變占`。

因此当前剩余问题不是要求你批量重做 515 条，而是对 **7 条真正没有足够 TITLE_FILENAME 证据的记录**回到本机文件重新核验。

## 二、必须复核的 7 条

```text
ZW-SRC-0027  紫微扬-术数述异b
ZW-SRC-0028  紫微杨+《清室气数录》b
ZW-SRC-0034  紫微杨+《蕉窗传灯录》b
ZW-SRC-0036  紫微杨-燃犀日知录b
ZW-SRC-0037  紫微杨传灯录b
ZW-SRC-0038  紫微杨：天网搜索录b
ZW-SRC-0087  ChengGu
```

不要把 `紫微杨 / 紫微扬` 这个作者名本身当成 `ziwei` 证据。

### ZW-SRC-0027 / 0028 / 0034 / 0036 / 0037 / 0038

逐个打开真实本地文件。

优先使用：

1. TITLE_PAGE
2. TOC / 目录
3. 可读正文中明确的体系说明
4. 扫描件首页/目录页的人工视觉确认

本轮只是确认“资料属于哪个知识领域”，不是提取规则。

如果真实内容明确属于紫微：

```json
"knowledge_domains": ["ziwei"],
"domain_basis": "CONTENT_VERIFIED",
"domain_evidence": "short factual evidence only"
```

如果明确属于风水：

```json
"knowledge_domains": ["fengshui"]
```

如果明确跨两个正式领域，且文件内容确实覆盖两者：

```json
"knowledge_domains": ["ziwei", "fengshui"],
"domain_basis": "CONTENT_VERIFIED"
```

禁止因为作者涉猎多个术数而多域分配。

如果确认属于当前六术之外的独立体系：

```json
"knowledge_domains": ["OUT_OF_SCOPE"]
```

如果看完可访问的首页/目录/可读内容仍不能判断：

```json
"knowledge_domains": ["UNKNOWN"],
"domain_basis": "UNKNOWN",
"domain_evidence": null
```

**UNKNOWN 是允许结果。不要为了通过 Gate 猜。**

### ZW-SRC-0087 — ChengGu

这是 CODE / implementation evidence。

不要因为它现在放在某个 registry 就判断领域，也不要仅凭 `ChengGu` 这个英文 identifier 推断成 bazi。

检查真实：

- 文件路径；
- package / module；
- class/function 内容；
- 调用方；
- 测试对应的功能。

如果项目代码路径和实现明确属于 bazi module：

```json
"knowledge_domains": ["bazi"],
"domain_basis": "PROJECT_CODE_PATH",
"domain_evidence": "short project-path/module evidence"
```

如果代码内容明确说明属于 bazi，但路径本身不够：

```json
"knowledge_domains": ["bazi"],
"domain_basis": "CONTENT_VERIFIED"
```

如果称骨在本项目治理上并不属于六个正式术数，而只是附属民俗算法，可以：

```json
"knowledge_domains": ["OUT_OF_SCOPE"]
```

但必须有项目实际代码/产品分类证据，不要使用模型常识决定。

无法确认则 `UNKNOWN`。

## 三、不要改其余 508 条，除非 validator 给出新的确定问题

当前 508 条已经通过最新版精度规则或使用了更强 evidence。

本轮禁止顺手大规模重写 author/school/title/domain。

如发现 7 条之外有真实新错误，可以报告，但不要无证据批改。

## 四、先修改 private intake

修改：

```text
/home/joe/knowledge-intake/ziwei/sources.jsonl
```

必要时只修改这 7 条对应记录。

不要把 private intake 提交 Git。

## 五、重新运行本地 K1 Gate

```bash
python3 tools/validate_k1_intake.py \
  /home/joe/knowledge-intake \
  --write-summary \
  /home/joe/knowledge-intake/K1_VALIDATION_RESULT.json
```

必须：

```text
k1-intake: PASS
```

515 canonical / SHA identity 必须保持。

## 六、必须通过 official sanitizer 重新生成

```bash
python3 tools/sanitize_k1_sources.py \
  /home/joe/knowledge-intake \
  --repo-root . \
  --manifest knowledge/K1_SANITIZED_IMPORT.json
```

禁止手工直接修改 GitHub `sources.jsonl` 作为最终来源。

## 七、机器验收

依次执行：

```bash
python3 tools/validate_sanitized_k1.py --force
python3 tools/validate_k1_source_quality.py --force
python3 tools/test_k1_source_quality.py
python3 tools/test_k1_semantic_routing.py
python3 tools/validate_k1_semantic_routing.py --force
python3 tools/validate_knowledge.py
```

硬 Gate：

```text
k1-semantic-routing: PASS
sources=515 issues=0
```

如果仍有 issue：不要把 `semantic_routing` 改 COMPLETE，继续按实际证据修复。

## 八、状态升级

只有最新版 semantic routing validator = 0 issues 后，才允许：

```json
"phase": "K1_SEMANTIC_ROUTING_COMPLETE",
"semantic_routing": "COMPLETE",
"k2_blocked": true
```

`k2_blocked` 仍然必须 true，等待项目端最终复验。

然后：

```bash
python3 tools/generate_knowledge_status.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

必须全部 PASS。

## 九、提交边界

只允许提交：

- `knowledge/K1_SANITIZED_IMPORT.json`
- `knowledge/PROJECT_STATE.json`
- `knowledge/STATUS.md`
- 实际发生变化的 `knowledge/domains/*/sources.jsonl`

禁止提交：

- `knowledge-intake/`
- PDF / 扫描 / OCR
- claims / fixtures / interpretation
- App / 算法
- validator / test（项目端已经修好，不要改）

提交并 push：

```bash
git add <allowed files only>
git commit -m "knowledge: close K1 semantic routing precision gaps"
git push origin knowledge-engine-v1
```

然后立即停止，不开始 K2。

## 十、最终只回报

1. commit SHA
2. 7 条 source 的最终 `knowledge_domains / domain_basis / domain_evidence`
3. 其中多少条 CONTENT_VERIFIED
4. 多少条 PROJECT_CODE_PATH
5. 多少条 UNKNOWN
6. 多少条 OUT_OF_SCOPE
7. 是否有多域记录，如有列 source_id
8. `validate_k1_intake.py` 结果
9. `validate_sanitized_k1.py --force` 结果
10. `validate_k1_source_quality.py --force` 结果
11. `test_k1_semantic_routing.py` 结果
12. `validate_k1_semantic_routing.py --force` 结果与 issues 数
13. manifest hash Gate 结果
14. `validate_knowledge.py` 结果
15. `generate_knowledge_status.py --check` 结果
16. `:ziwei-core:test` 结果
17. `git status --short` 是否 clean
18. commit 文件列表

不要开始 K2。
