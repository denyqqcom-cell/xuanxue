# LOCAL AI SUPPLEMENT — K2 Lineage 405-Issue Closure

本文件是 `LOCAL_CORPUS_K2_LINEAGE_COVERAGE_REMEDIATION_PROMPT.md` 的**强制补充**。两份必须同时执行；若有冲突，以本文件与最新版 `tools/validate_k2_source_lineage.py` 为准。

项目端在升级后的 part-aware validator 上对当前 515 行 lineage 实跑得到：

```text
k2-source-lineage: REVIEW_REQUIRED
sources=515 lineage_rows=515 issues=405
```

这 405 项不是 405 本书都错，而是第一版 lineage 尚未满足新版 K2A 语义。除 Work/Part/Variant 之外，还必须关闭下面两类系统问题。

## 1. SECONDARY_NOTE 必须退出 textual reading lane

K1 `evidence_role=SECONDARY_NOTE` 的 source，在 K2 必须保持：

```text
relation = SECONDARY_NOTE
independence_class = NOT_ELIGIBLE
k2_eligible = false
read_priority = SKIP
part_label = null
variant_of_source_id = null
```

原因：笔记可以在以后作为导航、回溯或待验证线索，但不能与原书一起进入 K2B 的独立文本阅读/投票通道。

当前第一版很多 SECONDARY_NOTE 仍保留 P1/P2/P3，因此 validator 会报：

`SECONDARY_NOTE must be SKIP in textual reading lane`

**全部 SECONDARY_NOTE 都要统一复核，不是只改日志 sample。**

不要删除笔记，也不要改 source_id；只修 K2 lineage role/priority。

## 2. K1 semantic UNKNOWN 的 textual source 在 K2A 不得被提前“认领”

如果 K1 Source Registry 是：

```text
evidence_role = TEXTUAL_SOURCE
knowledge_domains = ["UNKNOWN"]
```

K2A 必须保持：

```text
relation = UNKNOWN
work_id = null
independence_class = UNKNOWN
lineage_basis = UNKNOWN
lineage_evidence = null
k2_eligible = false
read_priority = P3
part_label = null
variant_of_source_id = null
```

不能仅凭同目录、相似标题、work family normalization，就把它变成 PRIMARY_WORK / WORK_PART / SAME_WORK_VARIANT。

理由：K1 已明确表示“这份文本究竟属于六术哪个语义域尚无证据”。K2A 不能绕过 K1 semantic routing，自行把它送入某个六术 reading lane。

本轮不要为了修 K2 去改 K1 `knowledge_domains`。

如果真实阅读能证明其领域，那属于以后受控的 semantic enrichment；本轮先保持 UNKNOWN。

## 3. WORK_PART / SAME_WORK_VARIANT 仍按主 Prompt 全量复核

当前旧 lineage 有 97 条 SAME_WORK_VARIANT。全部必须重审：

- 真正同 coverage 的另一载体 → SAME_WORK_VARIANT + `variant_of_source_id`
- 互补卷/册/篇/分页 → WORK_PART + `part_label`
- 系列中实际独立作品 → 新 work_id + PRIMARY_WORK
- 证据不足 → UNKNOWN

所有 SAME_WORK_VARIANT 必须直接指向同 work_id 的 PRIMARY_WORK 或 WORK_PART，不能形成 variant 链。

## 4. ChengGu 仍按项目端裁定

`ZW-SRC-0087`：

```text
relation = IMPLEMENTATION
independence_class = IMPLEMENTATION_ONLY
k2_eligible = false
read_priority = SKIP
```

即使 K1 `knowledge_domains=["OUT_OF_SCOPE"]` 也不改成 textual OUT_OF_SCOPE。semantic scope 与 source role 是两条轴。

## 5. 其他 role 也必须保持 fail-closed

`IMPLEMENTATION_EVIDENCE`：

```text
relation=IMPLEMENTATION
independence_class=IMPLEMENTATION_ONLY
k2_eligible=false
read_priority=SKIP
```

`AUXILIARY_INDEX`：

```text
relation=AUXILIARY_INDEX
independence_class=NOT_ELIGIBLE
k2_eligible=false
read_priority=SKIP
```

K1 semantic `OUT_OF_SCOPE` 的 TEXTUAL_SOURCE：

```text
relation=OUT_OF_SCOPE
independence_class=NOT_ELIGIBLE
k2_eligible=false
read_priority=SKIP
```

## 6. 正确的本地完成条件

保持：

`knowledge/K2_SOURCE_LINEAGE_STATE.json.status = REVIEW_REQUIRED`

本地 AI **不得**改 COMPLETE。

修完 private draft 后必须重新走 official sanitizer，然后运行：

```bash
python3 tools/test_k2_source_lineage.py
python3 tools/validate_k2_source_lineage.py
python3 tools/validate_knowledge.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

本地正确终点必须是：

```text
k2-source-lineage: REVIEW_REQUIRED
sources=515 lineage_rows=515 issues=0; promote state only after project review
```

不是 PASS，也不是 COMPLETE；`issues=0` 后由项目端再次独立验收并负责提升状态。

## 7. 最终回报额外增加

除主 Prompt 要求的 31 项外，再报告：

32. 修复前 405 issues → 修复后 issues 数
33. SECONDARY_NOTE 总数、其中改成 SKIP 的数量、最终非 SKIP 数（必须 0）
34. K1 `knowledge_domains=[UNKNOWN]` 且 TEXTUAL_SOURCE 的数量，以及最终 relation 非 UNKNOWN 数（必须 0）
35. IMPLEMENTATION 最终非 SKIP 数（必须 0）
36. AUXILIARY_INDEX 最终非 SKIP 数（必须 0）
37. OUT_OF_SCOPE textual 最终进入 K2 textual lane 数（必须 0）

严禁开始 Evidence / Claim Extraction。
