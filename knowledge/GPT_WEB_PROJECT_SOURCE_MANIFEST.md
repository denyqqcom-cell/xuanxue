# GPT Web 项目来源 Manifest — 奇门遁甲 / Xuanxue Knowledge Engine

状态：`SOURCE_PLAN_PREPARED / PROJECT_PANEL_NOT_VERIFIED`  
用途：指导 ChatGPT Web 项目“来源”添加与后续原页复核  
原则：`canonical source != reading note != atomic evidence != distillate != claim`

> 本 Manifest 只规定应该添加什么、为什么添加、如何识别。当前执行环境不能读取或写入 ChatGPT Web 项目的“来源”面板，因此不得把本文件解释为“这些来源已经上传成功”。项目面板中的实际存在状态必须由 UI/未来可用工具重新确认。

## 1. 添加来源的硬规则

1. 优先 canonical carrier（原始 PDF / 扫描件 / 原版讲义），不能用二手摘要代替需要原页验证的资料。
2. 同一本书不同文件必须先做 carrier identity / edition / page-map 核对，不能仅按相似标题合并。
3. GitHub 中的 Evidence、Reading Ledger、Distillate 是研究产物，不是 canonical source 的替身。
4. 当某个 fixture / rule 需要“原页日期、时柱、九宫版式、表格或图像”时，必须能回到原始页面；文本摘要不足即保持 blocker。
5. 项目来源中保留互相冲突的文献，不为了获得统一结论而删除异说。
6. 来源进入项目只获得 `SOURCE_ACCESS`，不会自动获得 `SOURCE_CREDIT / METHOD_CREDIT / EMPIRICAL_CREDIT`。

## 2. P0 — 当前门禁直接依赖的 canonical sources

### P0-01 — QM-SRC-0021

- Source ID：`QM-SRC-0021`
- Canonical title：幺学声《奇门遁甲预测学（奇门遁甲现代应用技术）》
- 已知阅读规模：约 285 页
- 当前 K2：Wave1 COMPLETE；Atomic Evidence 435；已有 Deep Source Distillate
- GPT Web 项目来源面板状态：`NEEDS_CONFIRMATION`
- 必须添加的原因：
  - `JU_METHOD_VALIDATION`
  - `PLATE_PAIRING_VALIDATION`
  - weather-v0.1 原始天气规则页
  - 2004-05-29 戊午时 source plate 原页复核
  - 被撤回的 2002 天气案例日期/时柱元数据重新核验
- 特别要求：必须保留页面图像/版式。只导入 OCR 文本不能充分验证九宫图和相邻字段。
- 禁止替代：`K2_EVIDENCE_WAVE1.jsonl`、Deep Source Distillate、旧学习笔记均不能替代本 PDF 的原页。

### P0-02 — QM-SRC-0028

- Source ID：`QM-SRC-0028`
- Canonical title：善天道《奇门遁甲讲义71页》
- Source type：`COURSE`
- 已知阅读规模：71 页
- 当前 K2：Wave1 COMPLETE；Atomic Evidence 50
- GPT Web 项目来源面板状态：`NEEDS_CONFIRMATION`
- 必须添加的原因：
  - 五日甲/己符头规则原页核验
  - 上中下元地支分类
  - 实际交节时辰切换规则
  - 拆补 / 置闰等方法边界
- 特别要求：课程资料不能自动提升为古籍权威；它只作为一个明确 lineage 的教学来源参与交叉验证。

### P0-03 — 项目 handoff / 方法规范

- Canonical artifact：`奇门遁甲项目_GPT跨窗口续接与记忆规范_2026-08-19(1).md`
- 当前会话：`可访问`
- GPT Web 项目来源面板状态：`NEEDS_CONFIRMATION`
- 用途：保证跨窗口继续遵守：
  - SOURCE → READING → ATOMIC EVIDENCE → CONFLICT/APPLICABILITY REVIEW → CLAIM → TEST/FEEDBACK → REVISED MODEL
  - `CASE_RECORD != CLAIM`
  - Claim Extraction fail-closed
  - 不把 handoff 中的历史状态当作当前 GitHub 事实
- 注意：这是项目方法规范，不是奇门术理来源。

## 3. P1 — 已完成 Wave1、适合用于交叉验证的奇门 sources

### P1-01 — QM-SRC-0001

- 梁湘润《奇门遁甲入门》
- 约 57 页
- Wave1 COMPLETE
- verification lane：`VISUAL_PAGE`
- 当前 Evidence：3
- 用途：基础起局/术语的独立来源对照；不能因 Evidence 少就被视为弱来源，仍需看其具体页面质量与来源年代。

### P1-02 — QM-SRC-0003

- 杜新会、郭军飞《奇门直断》
- 约 45 页
- Wave1 COMPLETE
- verification lane：`VISUAL_PAGE`
- 当前 Evidence：73
- 用途：案例型方法与直断规则反审；书中已知结果案例只能作为 retrospective material，不能计算前瞻准确率。

### P1-03 — QM-SRC-0016

- 《奇门遁甲应用学》
- 作者状态：`UNKNOWN / 需保留来源不确定性`
- 约 415 页
- Wave1 COMPLETE
- verification lane：`TEXT_LAYER_FULL`
- 当前 Evidence：128
- 用途：大体量现代应用规则交叉验证；作者不明本身属于 provenance limitation。

## 4. P1 — 当前会话已有、值得加入项目来源用于古籍/现代文献交叉验证的文件

以下文件在当前会话环境中已有文件载体，但不能由此推断它们已经存在于 GPT Web 项目“来源”面板：

- 《奇门遁甲秘传》姜春龙.pdf
- 《奇门遁甲新述》费秉勋著 时代文艺出版社1991.pdf
- 《奇门遁甲吉凶占断教程》.pdf
- 《金函玉镜奇门遁甲秘笈全书(上)》诸葛亮.pdf
- 《金函玉镜奇门遁甲秘笈全书(下)》诸葛亮.pdf
- 《笺元遁甲句解烟波钓叟歌》繁体竖版（宋）趙普撰 明刊本 台湾国家图书馆藏.pdf
- 《奇门精粹：奇门遁甲典籍大全》.pdf

建议用途：

- 做 lineage / source genealogy；
- 比较同一口诀在不同时期、不同载体的版本差异；
- 检查现代教材是否把古文规则简化、扩张或改写；
- 发现冲突时建立 conflict record，而不是多数表决。

这些资料不能替代 `QM-SRC-0021 / QM-SRC-0028` 的精确原页，因为当前 JuMethod 与 weather fixture gate 绑定的是后两者的具体页面和方法身份。

## 5. P2 — 后续扩展来源，不因“更多”而自动优先

只有在 P0 原页缺口关闭后，再扩大到：

- 更多拆补 / 置闰 / 茅山等起局法的第一手来源；
- 能给出完整 dated chart、而不是只有断语的 source cases；
- 不同地域/时代的天气占法原文；
- 现代统计/预测比较方法文献，用于 CDAF 与 prospective validation（它们属于 methodology source，不属于术理 source）。

原则是：

`source count growth != knowledge quality growth`

如果新增资料只重复已有口诀、不提供新的 lineage、边界、冲突、图盘 fixture 或可验证信息，则优先级低于补齐关键原页。

## 6. Web 项目来源的推荐命名

添加到 GPT Web 项目时，建议统一使用：

`[SourceID] 作者/传承 — 书名 — edition/carrier`

例如：

`[QM-SRC-0021] 幺学声 — 奇门遁甲预测学（奇门遁甲现代应用技术） — canonical PDF`

`[QM-SRC-0028] 善天道 — 奇门遁甲讲义71页 — course PDF`

如果 Source ID 尚未分配：

`[UNREGISTERED] 原文件名 — 待K1身份核验`

在身份确认前不要临时编造正式 Source ID。

## 7. 当前最重要的补源任务

优先级固定为：

`QM-SRC-0021 canonical PDF -> QM-SRC-0028 canonical PDF -> handoff spec -> 已完成Wave1其他canonical carriers -> 古籍/现代扩展来源`

原因不是 0021/0028 “更权威”，而是当前工程存在可验证、可关闭的具体原页 blocker。先解决可证伪问题，比继续增加来源数量更有认知价值。

## 8. 非主张边界

本 Manifest 不表示：

- GPT Web 项目已经添加了这些文件；
- 文献中的理论已经验证有效；
- Wave1 COMPLETE 等于全书每个命题都可靠；
- 古籍比现代教材天然更真；
- 多来源一致即可替代前瞻验证。

它只建立下一轮 source-access 的可执行顺序与身份纪律。
