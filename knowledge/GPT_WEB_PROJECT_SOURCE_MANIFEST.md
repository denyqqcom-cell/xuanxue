# GPT Web 项目来源 Manifest — 奇门遁甲 / Xuanxue Knowledge Engine

状态：`SOURCE_PLAN_PREPARED / PROJECT_PANEL_NOT_VERIFIED / CARRIER_IDENTITY_GATE_DEFINED / P0_METADATA_PARTIAL`  
用途：指导 ChatGPT Web 项目“来源”添加、carrier 身份确认与后续原页复核  
原则：`canonical source != reading note != atomic evidence != distillate != claim`

> 本 Manifest 只规定应该添加什么、为什么添加、如何识别。当前执行环境不能读取或写入 ChatGPT Web 项目的“来源”面板，因此不得把本文件解释为“这些来源已经上传成功”。项目面板中的实际存在状态必须由 UI/未来可用工具重新确认。

## 1. 添加来源的硬规则

1. 优先 canonical carrier（原始 PDF / 扫描件 / 原版讲义），不能用二手摘要代替需要原页验证的资料。
2. 同一本书不同文件必须先做 carrier identity / edition / page-map 核对，不能仅按相似标题合并。
3. GitHub 中的 Evidence、Reading Ledger、Distillate 是研究产物，不是 canonical source 的替身。
4. 当某个 fixture / rule 需要“原页日期、时柱、九宫版式、表格或图像”时，必须能回到原始页面；文本摘要不足即保持 blocker。
5. 项目来源中保留互相冲突的文献，不为了获得统一结论而删除异说。
6. 来源进入项目只获得 `SOURCE_ACCESS`，不会自动获得 `SOURCE_CREDIT / METHOD_CREDIT / EMPIRICAL_CREDIT`。
7. K1 `knowledge/domains/*/sources.jsonl` 是 `SANITIZED_METADATA_ONLY`：记录中的 `file_sha256 / pages / readability` 可用于 carrier 身份比对，但该 JSONL 本身不是 PDF carrier，也不证明 PDF bytes 已打包进 GitHub。
8. 当前 K1 source-quality contract 要求 source registry `local_only=true`、`packaged=false`，并禁止本地路径泄漏。因此从 GitHub 找不到原 PDF 时，不能把“有 metadata”误写成“仓库已有原页”。

## 2. Carrier Identity Gate — 新来源进入原页验证前必须先过

对 GPT Web 项目中新补入的 PDF / course carrier，先执行身份门，再允许其页面参与 JuMethod / Plate fixture verification。

### 2.1 优先级

```text
exact SHA-256 match
    > verified edition/front matter + page-map
    > title/page-count similarity
    > filename similarity
```

文件名只能用于发现候选，不能单独建立 canonical identity。

### 2.2 身份状态

#### A. `CANONICAL_CARRIER_MATCH`

必须满足：

- 上传文件 SHA-256 与 K1 canonical `file_sha256` 完全一致；
- PDF 可正常访问目标页；
- 页数与 registry 无不可解释冲突。

此时旧 K2 page locator 可以继续作为候选 locator，但目标页仍应重新看原页，不因 hash 相同而免除内容复核。

#### B. `VARIANT_REVIEW_REQUIRED`

适用于：

- 标题/作者明显相同但 SHA-256 不同；或
- 页数不同；或
- OCR 重制、重排、拆分/合并版；或
- edition/carrier 不同。

必须先建立 page-map，例如：

```text
old canonical pdf:p123 -> uploaded variant pdf:p127
```

在 page-map 建立前，旧 Evidence 的页码不能直接套用到新文件。

#### C. `SOURCE_ACCESS_ONLY_NOT_IDENTITY_VERIFIED`

如果项目来源面板只能提供可读内容，暂时不能取得文件 SHA：

- 可以用于检索候选页；
- 可以用于发现冲突；
- 不能据此关闭需要 canonical identity 的 Gate 0/A；
- 必须保留 `identity_pending=true`。

### 2.3 K2 verified metadata 与 carrier identity 是两层不同门

`K2_VERIFIED_SOURCE_METADATA.jsonl` 验证的是诸如作者、题名、版本等 source metadata 的可追溯性；它不是 carrier bytes 的替身。

反过来，SHA 完全匹配也不能自动证明作者/版本字段已经经过独立 K2 metadata review。

因此推荐顺序：

```text
carrier SHA / variant identity
        ↓
front matter / title-page metadata verification
        ↓
page-map / page locator confirmation
        ↓
source-grounded rule or plate fixture
```

## 3. P0 — 当前门禁直接依赖的 canonical sources

### P0-01 — QM-SRC-0021

- Source ID：`QM-SRC-0021`
- K1 title：`《奇门遁甲预测学》（奇门遁甲现代应用技术）`
- 作者：幺学声
- K1 author basis：`TITLE_PAGE`，题名页 PDF p1
- Source type：`BOOK`
- Canonical K1 SHA-256：`e804e292b446821e40965caa012e51d256f9eb9317f8b9519bbf4baebdbf4dd9`
- K1 pages：`285`
- K1 readability：`TEXT_OK`
- K1 carrier policy：`local_only=true / packaged=false / SANITIZED_METADATA_ONLY`
- K2 lineage：`PRIMARY_WORK / WORK-000027 / PRIMARY_CANDIDATE`
- 当前 K2：Wave1 COMPLETE；Atomic Evidence 435；已有 Deep Source Distillate
- `K2_VERIFIED_SOURCE_METADATA.jsonl` 当前状态：`REVIEWED / pdf:p1 / TEXT_LAYER / title+author`
- metadata closure：`L1 METADATA_VERIFIED = CLOSED`
- carrier identity：`L2 CARRIER_IDENTITY_VERIFIED = OPEN`
- target-page verification：`L3 TARGET_PAGE_VERIFIED = OPEN`
- GPT Web 项目来源面板状态：`NEEDS_CONFIRMATION`
- 必须添加的原因：
  - `JU_METHOD_VALIDATION`
  - `PLATE_PAIRING_VALIDATION`
  - weather-v0.1 原始天气规则页
  - 2004-05-29 戊午时 source plate 原页复核
  - 被撤回的 2002 天气案例日期/时柱元数据重新核验
- 特别要求：必须保留页面图像/版式。只导入 OCR 文本不能充分验证九宫图和相邻字段。
- 禁止替代：`K2_EVIDENCE_WAVE1.jsonl`、Deep Source Distillate、旧学习笔记均不能替代本 PDF 的原页。

**加入 GPT Web 后第一步不是直接读案例，而是先比对 SHA。**

```text
expected_sha256 = e804e292b446821e40965caa012e51d256f9eb9317f8b9519bbf4baebdbf4dd9
expected_pages  = 285
```

若 SHA 不同，即使也是幺学声同名书，也先标 `VARIANT_REVIEW_REQUIRED`，建立 page-map 后再复核 2004/2002 fixture。

### P0-02 — QM-SRC-0028

- Source ID：`QM-SRC-0028`
- K1 title：`善天道-奇门遁甲讲义71页`
- 作者：善天道
- K1 author basis：`FILENAME`
- Source type：`COURSE`
- Canonical K1 SHA-256：`bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243`
- K1 pages：`71`
- K1 readability：`TEXT_OK`
- K1 carrier policy：`local_only=true / packaged=false / SANITIZED_METADATA_ONLY`
- K2 lineage：`PRIMARY_WORK / WORK-000018 / PRIMARY_CANDIDATE`
- 当前 K2：Wave1 COMPLETE；Atomic Evidence 50
- `K2_VERIFIED_SOURCE_METADATA.jsonl` 当前状态：`NO_ROW / TITLE_PAGE_OR_EXPLICIT_SIGNATURE_REVIEW_REQUIRED`
- metadata closure：`L1 METADATA_VERIFIED = OPEN`
- carrier identity：`L2 CARRIER_IDENTITY_VERIFIED = OPEN`
- target-page verification：`L3 TARGET_PAGE_VERIFIED = OPEN`
- GPT Web 项目来源面板状态：`NEEDS_CONFIRMATION`
- 必须添加的原因：
  - 五日甲/己符头规则原页核验
  - 上中下元地支分类
  - 实际交节时辰切换规则
  - 拆补 / 置闰等方法边界
- 特别要求：课程资料不能自动提升为古籍权威；它只作为一个明确 lineage 的教学来源参与交叉验证。
- 特别限制：不能因为 K1 filename 标出“善天道”就伪造 `TITLE_PAGE` author basis；只有 carrier 原页实际支持的字段才能进入 verified metadata。

```text
expected_sha256 = bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243
expected_pages  = 71
```

`QM-SRC-0044` 是该课程的 `SAME_WORK_VARIANT`，不能作为“第二个独立来源”关闭独立性要求。若 GPT Web 上传的是 0044 对应 carrier，也必须保留 variant lineage，而不是静默当成 0028 canonical PDF。

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

## 4. P1 — 已完成 Wave1、适合用于交叉验证的奇门 sources

### P1-01 — QM-SRC-0001

- 梁湘润《奇门遁甲入门》
- 约 57 页
- Wave1 COMPLETE
- verification lane：`VISUAL_PAGE`
- 当前 Evidence：3
- K2 verified metadata：题名/封面页 PDF p1 已独立核验梁湘润署名与题名
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
- 作者：`王云鹏`
- 作者核验：`K2_VERIFIED_SOURCE_METADATA` 已通过正文/作者通讯处 PDF p415 独立核为王云鹏
- Canonical SHA-256：`f80169f351740a338d5227225e96939fb3a7045a4e4037b4b3b035bf66630fc7`
- 约 415 页
- Wave1 COMPLETE
- verification lane：`TEXT_LAYER_FULL`
- 当前 Evidence：128
- 用途：大体量现代应用规则交叉验证。

> 修订记录：本 Manifest 旧版曾沿用 K1 初始 registry 的 `author=UNKNOWN`，但后续 K2 verified metadata 已给出 p415 的作者证据。此处已纠正，避免旧 intake metadata 压过后续人工核验。

### P1-04 — QM-SRC-0017

- 费秉勋《奇门遁甲新述》
- 时代文艺出版社 1991年3月第1版
- Canonical SHA-256：`f895e60c0cb0e52de43e1c4b17856d780499dae32cd8a058317305e5b8ca83d1`
- 419 页
- K2 verified metadata：`REVIEWED / pdf:p3 / VISUAL_PAGE`
- 当前会话 carrier：SHA-256 与 K1 canonical 完全一致，`CANONICAL_CARRIER_MATCH`
- 本轮原页复核：PDF p15-p17（printed p6-p8）
- 方法贡献：独立支持甲/己五日 head、上中下元 branch class，并给出 `1990-01-27 壬辰 -> 大寒下元 -> 阳6` dated structural example
- 信用边界：相关章节属于“超神接气和置闰”；只能给共享五日符头子结构与该 dated result 增加 cross-source structure credit，不能把费氏完整置闰法与 `CHAI_BU_FUTOU` 静默视为同一方法。
- durable review：`K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md`

## 5. P1 — 当前会话已有、值得加入项目来源用于古籍/现代文献交叉验证的文件

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

## 6. P2 — 后续扩展来源，不因“更多”而自动优先

只有在 P0 原页缺口关闭后，再扩大到：

- 更多拆补 / 置闰 / 茅山等起局法的第一手来源；
- 能给出完整 dated chart、而不是只有断语的 source cases；
- 不同地域/时代的天气占法原文；
- 现代统计/预测比较方法文献，用于 CDAF 与 prospective validation（它们属于 methodology source，不属于术理 source）。

原则是：

`source count growth != knowledge quality growth`

如果新增资料只重复已有口诀、不提供新的 lineage、边界、冲突、图盘 fixture 或可验证信息，则优先级低于补齐关键原页。

## 7. Web 项目来源的推荐命名

添加到 GPT Web 项目时，建议统一使用：

`[SourceID] 作者/传承 — 书名 — edition/carrier — identity-status`

例如：

`[QM-SRC-0021] 幺学声 — 奇门遁甲预测学（奇门遁甲现代应用技术） — PDF — IDENTITY_PENDING`

`[QM-SRC-0028] 善天道 — 奇门遁甲讲义71页 — course PDF — IDENTITY_PENDING`

SHA 核验后再改为：

`... — CANONICAL_CARRIER_MATCH`

如果 Source ID 尚未分配：

`[UNREGISTERED] 原文件名 — 待K1身份核验`

在身份确认前不要临时编造正式 Source ID。

## 8. 当前最重要的补源任务

优先级固定为：

`QM-SRC-0021 canonical PDF -> QM-SRC-0028 canonical PDF -> handoff spec -> 已完成Wave1其他canonical carriers -> 古籍/现代扩展来源`

原因不是 0021/0028 “更权威”，而是当前工程存在可验证、可关闭的具体原页 blocker。先解决可证伪问题，比继续增加来源数量更有认知价值。

补源后的执行链固定为：

```text
PROJECT SOURCE ACCESS
    ↓
SHA / VARIANT IDENTITY CHECK
    ↓
FRONT-MATTER METADATA REVIEW
    ↓
PAGE-MAP CONFIRMATION
    ↓
ORIGINAL PAGE REVERIFICATION
    ↓
DATED JU / PLATE FIXTURE
    ↓
GATE 0 / A REVIEW
```

不得从 `PROJECT SOURCE ACCESS` 直接跳到 `GATE CLOSED`。

## 9. 当前明确未关闭的 source gaps

```text
QM-SRC-0021_PROJECT_SOURCE_ACCESS      = NEEDS_CONFIRMATION
QM-SRC-0021_CARRIER_IDENTITY           = NOT_REVERIFIED_IN_GPT_PROJECT
QM-SRC-0021_K2_VERIFIED_METADATA_ROW   = REVIEWED
QM-SRC-0021_2002_CASE_ORIGINAL_PAGE    = REVERIFICATION_REQUIRED

QM-SRC-0028_PROJECT_SOURCE_ACCESS      = NEEDS_CONFIRMATION
QM-SRC-0028_CARRIER_IDENTITY           = NOT_REVERIFIED_IN_GPT_PROJECT
QM-SRC-0028_K2_VERIFIED_METADATA_ROW   = MISSING_TITLE_PAGE_REVIEW_REQUIRED

QM-SRC-0017_LOCAL_CARRIER_IDENTITY     = CANONICAL_CARRIER_MATCH
JU_METHOD_SHARED_FIVE_DAY_HEAD_SUPPORT = MULTI_SOURCE
JU_METHOD_SECOND_DATED_STRUCTURE       = SATISFIED_AT_SHARED_SUBSTRUCTURE_LEVEL_BY_QM-SRC-0017
JU_METHOD_FULL_IDENTITY                = OPEN
PLATE_PAIRING_SECOND_FIXTURE           = BLOCKED_ON_SOURCE_PAGE
SOLAR_TERM_BOUNDARY_SOURCE_FIXTURE     = BLOCKED_ON_CHAI_BU_FUTOU_SPECIFIC_SOURCE_PAGE
```

这些状态用于阻止“GitHub 已有摘要/证据，所以原书页也等于已验证”的错误推理，也阻止“两个方法某天给出相同局数，所以整套方法相同”的新错误推理。

## 10. 非主张边界

本 Manifest 不表示：

- GPT Web 项目已经添加了这些文件；
- 文献中的理论已经验证有效；
- Wave1 COMPLETE 等于全书每个命题都可靠；
- SHA 匹配等于书中方法正确；
- 古籍比现代教材天然更真；
- 多来源一致即可替代前瞻验证；
- 共享五日符头子结构等于拆补、置闰等完整 JuMethod 等价。

它只建立下一轮 source-access、carrier identity 与原页复核的可执行顺序。
