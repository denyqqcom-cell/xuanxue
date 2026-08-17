# LOCAL AI PROMPT — K2 Lineage Coverage Remediation

你现在负责 Xuanxue Knowledge Engine v1 的 **K2_SOURCE_LINEAGE_COVERAGE_REVIEW**。

K1 已正式关闭。本轮仍属于 K2A Source Lineage，**严禁开始 Evidence / Claim Extraction**。

本轮不是重新做 515 条 Source Registry，也不是重新做 K1。项目端已经接受 K1。

你的任务是修复 K2A 第一版 lineage 中一个新的系统性问题：

> `SAME_WORK_VARIANT` 被同时用于“同内容的另一载体”和“同一作品的不同卷/册/篇/分页”。

这会让 K2B 有机会把包含独立内容的卷二、卷三、下册、分页段错误当成可跳过的重复版本。

────────────────────
一、先同步正确分支
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

- `knowledge/K2_LINEAGE_PROJECT_REVIEW.md`
- `knowledge/K2_SOURCE_LINEAGE_PROTOCOL.md`
- `knowledge/schema/source_lineage.schema.json`
- `tools/sanitize_k2_lineage.py`
- `tools/validate_k2_source_lineage.py`
- `tools/test_k2_source_lineage.py`

如果有未知本地改动，STOP。

禁止 `reset --hard` / `clean -fd`。

────────────────────
二、当前已知输入
────────────────────

第一版 lineage：

- rows = 515
- distinct work_id = 396
- PRIMARY_WORK = 69
- SAME_WORK_VARIANT = 97
- COMMENTARY_DERIVATIVE = 8
- SECONDARY_NOTE = 159
- IMPLEMENTATION = 65
- AUXILIARY_INDEX = 67
- OUT_OF_SCOPE = 6
- UNKNOWN = 44

第一版已成功做到：

- NOTE / CODE / AUX 角色锁定；
- commentary parent 保留；
- 六术薄 corpus 未被降低优先级；
- UNKNOWN 没有为了覆盖率乱猜；
- 515 canonical source_id 没有增删。

这些正确部分不要推翻。

────────────────────
三、ChengGu 的项目端裁定
────────────────────

`ZW-SRC-0087 ChengGu`：

K1 已确认：

- `evidence_role = IMPLEMENTATION_EVIDENCE`
- `knowledge_domains = ["OUT_OF_SCOPE"]`

这两个事实可以同时成立。

它在 K2 必须保持：

```text
relation = IMPLEMENTATION
independence_class = IMPLEMENTATION_ONLY
k2_eligible = false
read_priority = SKIP
lineage_basis = PROJECT_CODE_PATH 或 CONTENT_VERIFIED
```

不要把它改成 `OUT_OF_SCOPE` textual row。

也不要回改 K1 `knowledge_domains`。

项目端 validator 已修正为：semantic OUT_OF_SCOPE 与 source role 分开判断。

────────────────────
四、新的 relation：WORK_PART
────────────────────

新版 relation 允许：

- PRIMARY_WORK
- WORK_PART
- SAME_WORK_VARIANT
- COMMENTARY_DERIVATIVE
- SECONDARY_NOTE
- IMPLEMENTATION
- AUXILIARY_INDEX
- OUT_OF_SCOPE
- UNKNOWN

定义：

### PRIMARY_WORK

当前 source 本身覆盖完整 underlying work。

通常：

```text
independence_class = PRIMARY_CANDIDATE
k2_eligible = true
part_label = null
variant_of_source_id = null
```

### WORK_PART

source 只是同一 underlying work 的互补部分，例如：

- 上 / 中 / 下册
- 卷一 / 卷二
- 第一篇 / 第二篇
- 一至六册中的其中一册
- 非重叠 page split
- 同一完整作品拆成若干文件

必须：

```text
relation = WORK_PART
work_id = 同一个 underlying work
part_label = 能区分这一部分的简短标签
variant_of_source_id = null
independence_class = SAME_WORK_NOT_INDEPENDENT
k2_eligible = true
```

重点：

**WORK_PART 不是独立支持票，但它包含独特内容，因此不能 SKIP。**

### SAME_WORK_VARIANT

只有当 source 与另一 canonical source 覆盖基本相同内容时使用，例如：

- 同一完整书另一扫描版
- 同一卷另一清晰版
- 同一内容不同排版
- OCR / 整洁载体与原载体覆盖相同

必须新增：

```text
variant_of_source_id = 某个 PRIMARY_WORK 或 WORK_PART 的 source_id
```

禁止 variant 指向另一个 variant。

如果 variant_of 指向 WORK_PART：

`part_label` 必须与目标 WORK_PART 完全相同。

────────────────────
五、最重要：重新审核全部 97 条 SAME_WORK_VARIANT
────────────────────

不能只修几个案例。

当前 97 条 `SAME_WORK_VARIANT` 必须全部重新判断。

并且对每一条 variant，必须一起检查该 `work_id` family 中的：

- PRIMARY_WORK
- 其他 SAME_WORK_VARIANT
- 可能的 UNKNOWN

因为 family 的第一条 PRIMARY_WORK 也可能其实只是“第一册/上册”。

每一个当前 variant 最终只能：

A. 确认真的是同覆盖版本
→ 保持 SAME_WORK_VARIANT
→ 补 `variant_of_source_id`

B. 实际是互补卷/册/篇/分页
→ 改 WORK_PART
→ 补 `part_label`

C. 实际是系列中的另一部独立作品
→ 分配新的 `work_id`
→ 改 PRIMARY_WORK

D. 证据不够
→ UNKNOWN

禁止因为标题 normalization 后一样，就自动判 A。

────────────────────
六、已确认必须重点复核的 family
────────────────────

至少完整复核之前报告的最大 family：

1. WORK-000106 命理探原/探源各版及分页
2. WORK-000063 八字真诀启示录火/电/雷/风集及分页
3. WORK-000058 命谱/袁氏命谱各版及分页
4. WORK-000003 紫微斗数全集一–六
5. WORK-000045 apk common 辅助文件
6. WORK-000089 星相书简法卷
7. WORK-000157 中州派玄空风水第1–5篇
8. WORK-000073 命略本纪上下/高清
9. WORK-000075 大流年批导/批道法
10. WORK-000080 子平教材讲义
11. WORK-000127 甲遁真授秘录上下+全文
12. WORK-000009 斗数四书
13. WORK-000066 余/佘氏用神辞渊
14. WORK-000069 刑冲合会透解
15. WORK-000079 子平基础概要
16. WORK-000167 中州派玄空學上中下
17. WORK-000113 图解奇门遁甲大全 1–3
18. WORK-000121 奇门遁甲应用学+OCR/全文
19. WORK-000128 烟波钓叟歌+OCR/全文
20. WORK-000133 曾子南三元奇门讲义上中下

但这 20 个不是全部范围；全部 97 variant 都要处理。

────────────────────
七、几个具体判断原则
────────────────────

### 紫微斗数全集（一）至（六）

这些是互补卷册，不是六个相同内容的版本。

如果本地确认六册共同构成同一套完整作品，正确方向通常是：

```text
同一 work_id
六条均为 WORK_PART
part_label = 第一册 / 第二册 / ...
k2_eligible = true
```

除非另有一个真正“六册合一本”的完整 source，才让合一本成为 PRIMARY_WORK。

不要为了保留 PRIMARY_CANDIDATE 而把第一册假装成完整 work。

### 上中下册

优先视为 WORK_PART 候选。

如果另一个文件只是“上册高清版”，则：

- 上册 primary carrier → WORK_PART(part_label=上册)
- 上册高清版 → SAME_WORK_VARIANT，variant_of 指向上册 primary carrier

### 全文 + 上下册

例如：

- 完整全文真实覆盖全书 → 可以 PRIMARY_WORK
- 上册 / 下册 → WORK_PART
- “全文 OCR”若只是完整原书的 OCR 载体 → SAME_WORK_VARIANT 指向 PRIMARY_WORK，通常低优先或非必要阅读

但若 `_全文.txt` 在 K1 已是 AUXILIARY_INDEX，则必须继续 AUXILIARY_INDEX，不能因为内容多改成 textual PRIMARY_WORK。

### 系列书

例如标题都属于某“系列”，但每册有不同副标题、不同主题、独立出版意义：

不要因为系列前缀一样就共享一个 work_id。

应根据真实标题页/目录判断是不是：

- 一个 work 的不同 part；
或
- 多个独立 work。

以后对同作者/同系列的依赖会在更高层 lineage 处理，**不能用错误合并 work_id 来代替作者依赖治理。**

────────────────────
八、part_label 规则
────────────────────

必须简短、稳定，只描述 coverage，不写长原文。

例如：

```text
第一册
第二册
上册
中册
下册
卷一
卷二
第1篇
第2篇
pages-001-050
pages-051-100
```

同一个 `work_id` 内，不允许两个 WORK_PART 使用同一个 part_label。

如果同一个 part 有第二个扫描版，第二个必须 SAME_WORK_VARIANT，而不是再建一个 WORK_PART。

────────────────────
九、variant_of_source_id 规则
────────────────────

所有 SAME_WORK_VARIANT 必须有：

`variant_of_source_id`

目标必须：

- 存在于 515 canonical source；
- 与 variant 使用相同 work_id；
- relation 为 PRIMARY_WORK 或 WORK_PART；
- 不能是自己；
- 不能指向另一个 SAME_WORK_VARIANT。

如果目标是 WORK_PART，variant 的 part_label 必须与目标一致。

────────────────────
十、不要错误制造“独立票”
────────────────────

把系列拆成不同 work_id，不代表以后可以无条件当独立证据。

K2B/K2C 后面还会处理：

- 同作者依赖；
- 同流派依赖；
- 引用/抄录依赖；
- commentary parent；
- claim-level independence。

所以本轮只追求 bibliographic / coverage identity 正确。

禁止为了增加 `PRIMARY_WORK` 数量故意拆 work。

────────────────────
十一、UNKNOWN 合法
────────────────────

如果不能确认：

- 是版本还是分卷；
- 是系列独立书还是同一作品；
- page split 是否重叠；

可以：

```text
relation=UNKNOWN
independence_class=UNKNOWN
lineage_basis=UNKNOWN
lineage_evidence=null
k2_eligible=false
```

不要猜。

────────────────────
十二、只修改 private draft
────────────────────

编辑：

`/home/joe/knowledge-intake/K2_SOURCE_LINEAGE_DRAFT.jsonl`

仍必须 515 行。

禁止提交 `knowledge-intake/`。

新增字段允许：

```text
part_label
variant_of_source_id
```

所有行建议显式包含这两个字段；不适用时写 null。

────────────────────
十三、使用 official sanitizer
────────────────────

执行：

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

最终公开文件：

`knowledge/K2_SOURCE_LINEAGE.jsonl`

禁止手工复制作为最终产物。

────────────────────
十四、机器验收
────────────────────

保持：

`knowledge/K2_SOURCE_LINEAGE_STATE.json.status = REVIEW_REQUIRED`

**本地 AI 本轮不得自行改成 COMPLETE。**

执行：

```bash
python3 tools/test_k2_source_lineage.py
python3 tools/validate_k2_source_lineage.py
python3 tools/validate_knowledge.py
python3 tools/generate_knowledge_status.py --check
./gradlew --no-daemon :ziwei-core:test
```

正确目标：

```text
k2-source-lineage: REVIEW_REQUIRED
sources=515 lineage_rows=515 issues=0; promote state only after project review
```

注意：

本轮不要运行 `--force` 作为最终 Gate，因为 state 故意保持 REVIEW_REQUIRED。

项目端收到数据后再独立复验，并决定是否把 state 提升 COMPLETE。

────────────────────
十五、自验收必须覆盖
────────────────────

至少完成：

- 全部 97 个旧 SAME_WORK_VARIANT 的逐条复核；
- 所有涉及这些 variant 的 work family 全成员复核；
- 所有新增 WORK_PART；
- 所有仍保留的 SAME_WORK_VARIANT 的 `variant_of_source_id`；
- 至少检查 20 个最大 family；
- 所有 P0 family；
- 六爻和六壬全部 textual source；
- ChengGu 双约束；
- commentary 8 条不得被本轮误改；
- NOTE/CODE/AUX role 数量异常变化必须解释。

────────────────────
十六、提交边界
────────────────────

本轮原则上只允许提交：

`knowledge/K2_SOURCE_LINEAGE.jsonl`

如果 sanitizer 输出格式变化，只提交上述公开 lineage。

不要提交：

- K2_SOURCE_LINEAGE_STATE.json 的 COMPLETE 状态；
- PROJECT_STATE；
- claims / evidence / fixtures；
- App / 算法；
- validator / tests；
- knowledge-intake；
- PDF / 扫描 / OCR。

commit + push：

`origin/knowledge-engine-v1-k2`

然后 STOP。

────────────────────
十七、最终回报
────────────────────

只回报：

1. commit SHA
2. lineage rows
3. distinct work_id
4. PRIMARY_WORK 数
5. WORK_PART 数
6. SAME_WORK_VARIANT 数
7. COMMENTARY_DERIVATIVE 数
8. SECONDARY_NOTE 数
9. IMPLEMENTATION 数
10. AUXILIARY_INDEX 数
11. OUT_OF_SCOPE 数
12. UNKNOWN 数
13. 旧 97 SAME_WORK_VARIANT 最终去向：仍 variant / WORK_PART / 独立 PRIMARY_WORK / UNKNOWN 各多少
14. 新增或拆分的 work_id 数
15. WORK_PART 按六术分布
16. SAME_WORK_VARIANT 中 variant_of 指向 PRIMARY_WORK / WORK_PART 各多少
17. 最大 20 work family 的最终关系摘要
18. 紫微斗数全集一–六最终关系
19. 甲遁真授秘录上下+全文最终关系
20. 曾子南三元奇门讲义上中下最终关系
21. 中州派玄空资料 family 最终关系
22. ChengGu 最终 relation / independence / eligible / priority
23. commentary 8 条是否保持
24. NOTE/CODE/AUX 数量是否保持；若变化说明原因
25. test_k2_source_lineage.py
26. validate_k2_source_lineage.py（非 --force）与 issues 数
27. validate_knowledge.py
28. status --check
29. ziwei-core:test
30. git status
31. 实际 commit 文件列表

严禁开始 Evidence / Claim Extraction。
