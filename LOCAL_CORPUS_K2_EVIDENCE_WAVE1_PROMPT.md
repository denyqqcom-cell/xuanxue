# LOCAL HELPER PROMPT — K2B Wave 1

你是 Xuanxue Knowledge Engine v1 的**本地执行助手**，不是项目主开发者，也不是 Evidence/Claim 的知识裁判。

项目主开发者会负责：代码、Schema、validator、Reading Ledger、Evidence 归一化、Git commit/push、项目状态和最终验收。

你本轮只负责：

1. 拉取指定分支；
2. 运行项目端已经写好的 planner / extraction helper / tests；
3. 找到本机 source_id 对应资料；
4. 机械提取已有真实文字层；
5. 报告缺文件、SHA 不一致、vision 失败、文字层失败和测试日志；
6. 按项目主开发者点名时，把指定 source/page packet 的内容回传给项目主开发者审核。

## 绝对禁止

不得：

- 修改任何 tracked repository 文件；
- 修改 Schema / validator / planner / sanitizer / tests；
- 自己生成正式 `knowledge/K2_*` ledger/evidence；
- 自己归纳 atomic Evidence；
- 做 Claim Extraction；
- 判断流派谁对谁错；
- 修改 App/算法；
- git add / commit / push。

如果项目脚本失败，只报告失败，不要修代码。

## 一、同步分支

执行：

```bash
git status --short
git fetch origin
git checkout knowledge-engine-v1-k2
git pull --ff-only origin knowledge-engine-v1-k2
```

`git status --short` 必须 clean。

若不 clean：停止并回报。禁止 `reset --hard`、禁止 `clean -fd`。

## 二、运行官方 Wave1 planner

执行：

```bash
python3 tools/plan_k2_evidence_wave1.py \
  --output /home/joe/knowledge-intake/K2_WAVE1_PLAN.jsonl
```

回报完整 stdout。

planner 会为每个 reading unit 给出：

- `TEXT_DIRECT`
- `VISUAL_REQUIRED`
- `ACCESS_REVIEW`

并带上 canonical `file_sha256`。不要自行更改 execution lane、source_id 或 hash。

当前项目端预期 Wave1 仍是 37 个 selected reading units；若不是 37，停止并回报。

## 三、构建本地 page packets

执行：

```bash
python3 tools/build_k2_local_page_packets.py \
  --plan /home/joe/knowledge-intake/K2_WAVE1_PLAN.jsonl \
  --intake-root /home/joe/knowledge-intake \
  --output-dir /home/joe/knowledge-intake/K2_WAVE1_PAGE_PACKETS
```

这个脚本是项目主开发者写好的机械工具。

它会先核对三层 source identity：

```text
official Wave1 plan file_sha256
=
private K1 sources.jsonl file_sha256
=
本机实际文件 SHA256
```

任一不一致都会直接 FAIL。遇到这种情况只回报，不要替换文件、改 hash 或修脚本。

通过 identity Gate 后，它只能：

- 为 `TEXT_DIRECT` 源从 PDF 已有文字层逐页抽取文本；
- 保持 PDF 页边界；
- 记录 source_file_sha256、每页 text SHA256、char_count，以及完整 packet_sha256；
- 对 `VISUAL_REQUIRED` 源诚实标记 BLOCKED；
- 输出全部内容到仓库外 `/home/joe/knowledge-intake/`。

它不会、也不允许你自己补做 Evidence。

## 四、SCAN/OCR_WEAK 的处理

如果本机 vision 后端仍然返回 401 / `User not found`：

不要 OCR 猜测，不要用文字层冒充原页核验。

`VISUAL_REQUIRED` 源保持：

```text
BLOCKED
blocker_code = VISION_UNAVAILABLE
```

这是合格且诚实的执行结果，不是需要你修复的数据错误。

## 五、TEXT_DIRECT 的处理

你不负责把 page packet 归纳成 Evidence。

page packet 建好以后，只做两件事：

1. 检查 manifest 中 READY/BLOCKED 数量、source_file_sha256 与 packet_sha256；
2. 项目主开发者点名某个 source_id 或页段时，把对应 `.pages.jsonl` 中指定页面的原始 page packet 内容回传。

不要主动把 2000 页一次性贴出来。

不要总结、改写或筛选“重要规则”；由项目主开发者逐批审核并写正式 Evidence。

## 六、已有六壬 34 条结果

此前第一次失败执行中，liuren 曾留下 34 条已经过本地合规检查的候选 Evidence。

不要删除，不要重写，不要提交。

只回报它们当前本地文件路径、文件 SHA256、行数，以及每条是否仍能追溯到 source_id/source_location。

项目主开发者会决定是否复用并重新写入正式 public Evidence。

## 七、运行测试

只运行，不修改：

```bash
python3 tools/test_k2_evidence.py
python3 tools/validate_k2_lineage_integrity.py
python3 tools/validate_knowledge.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

如果任何一个 FAIL：原样回报日志，停止。不要修。

## 八、最终只回报

只回报以下内容，不 commit/push：

1. 当前 branch HEAD SHA；
2. `git status --short`；
3. planner stdout；
4. selected reading units 数；
5. execution lane 分布；
6. page packet builder stdout；
7. READY source_id 列表；
8. BLOCKED source_id 列表；
9. blocker_code 分布；
10. source hash identity Gate 是否 37/37 通过；
11. READY 总页数、总 char_count；
12. READY 每个 source 的 source_file_sha256 + packet_sha256；
13. `ZW-SRC-0001` packet 是否仍为 55 页；
14. 现存 liuren 34 条候选文件路径、SHA256、行数、provenance 完整性；
15. `test_k2_evidence.py` 结果；
16. `validate_k2_lineage_integrity.py` 结果；
17. `validate_knowledge.py` 结果；
18. `generate_knowledge_status.py --check` 结果；
19. `:ziwei-core:test` 结果；
20. 最终 `git status --short`，必须仍 clean。

完成后停止，等待项目主开发者点名要读取的 source/page packet。

**不要修改代码，不要生成正式 Evidence，不要 commit，不要 push。**
