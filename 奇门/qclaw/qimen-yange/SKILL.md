---
name: qimen-yange
description: >
  奇门歌诀与口诀 provenance 研究技能。区分古籍文本、版本异文、现代转述、教学口诀与项目推演，
  不把“多处一致”或旧技能中的现代扩写自动当成原典，也不让歌诀直接越级成现实吉凶结论。
---

# 奇门歌诀 Provenance Registry v2.0

> 上位约束：`奇门/CURRENT_METHOD_CONSTRAINTS.md`。
>
> 核心原则：**先确定“这句话到底来自哪一层”，再讨论它能不能进入方法。**

## 一、为什么旧歌诀技能需要迁移

legacy `qimen-yange` 标题写成“烟波钓叟歌详解”，但文件实际混合了至少四层内容：

1. 归因于《笺元遁甲句解烟波钓叟歌》的传统歌诀；
2. 《奇门遁甲预测学》等现代书的九星/八门解释；
3. 《图解遁甲演义》等后出资料；
4. 项目自己整理的速查表、吉凶星级、适合事项和“入门口诀”。

旧文件随后又用统一“经典版/文献来源”语气呈现，导致 `TEXT PROVENANCE -> MODERN GLOSS -> OPERATIONAL RULE` 三层被压成一层。

当前撤销这种写法。

## 二、Verse / Formula Registry Schema

每条歌诀、口诀或数字公式至少记录：

```text
verse_id
text_or_formula
text_layer = PRIMARY_TEXT / COMMENTARY_TEXT / MODERN_PARAPHRASE / TEACHING_MNEMONIC / PROJECT_GLOSS
attribution_status = PAGE_VERIFIED / LEGACY_ATTRIBUTION / ATTRIBUTION_UNRESOLVED
source_work
source_location
edition_or_witness
variant_id
variant_relation = SAME / ORTHOGRAPHIC_VARIANT / SUBSTANTIVE_VARIANT / POSSIBLE_CONFLATION / UNKNOWN
method_context
operational_status = SOURCE_ONLY / CANDIDATE / TESTABLE / CONTEXT_REQUIRED / NOT_OPERATIONAL
notes
```

只有 `PAGE_VERIFIED` 才能说“当前原页核验到该文本”。旧 skill 自己写过的引用不能反向证明原典。

## 三、旧《烟波钓叟歌》归因的当前状态

legacy skill 把整份内容统一归因于：

`《笺元遁甲句解烟波钓叟歌》宋·赵普撰，明刊本`

当前拆成：

- 书名/版本/撰者：`LEGACY_ATTRIBUTION`，等待对应 K2 source/page visual provenance；
- 阴阳遁数字歌诀：`LEGACY_TRANSCRIPTION / SOURCE_CANDIDATE`；
- 九星固定吉凶、八门固定吉凶、九遁适合事项：多为 `MODERN_GLOSS / SOURCE_MIXED`，不得自动说成古歌原文；
- 星级 `★★★★★`：`PROJECT_GLOSS / NOT_OPERATIONAL`；
- “一蓬二任三冲……”等教学速背：`TEACHING_MNEMONIC`，除非回到具体原页核验，不称原典句；
- “青龙回首/飞鸟跌穴”干对、格局大吉大凶等：转交 `qimen-gexia` Pattern Registry，不由歌诀技能裁决。

## 四、阴阳遁数字公式

legacy skill 保存了两组数字公式，例如：

- 阳遁节气对应上/中/下元局数；
- 阴遁节气对应上/中/下元局数。

当前地位：

`LEGACY_TRANSCRIPTION -> SOURCE_CANDIDATE -> qimen-qiju applicability review`

禁止仅因为歌诀可背诵就直接作为 setup implementation truth。需要确认：

- 对应哪个起局体系；
- 平气/定气；
- 正授/超神/置闰/接气；
- 节气交接时刻；
- time boundary；
- 版本是否有异文。

若不同版本产生不同局数，必须保留 `SUBSTANTIVE_VARIANT`，不能把其中一版静默“校正”为另一版。

## 五、已发现的 provenance / semantic 风险

### 5.1 “核心经典歌诀”不等于整页内容都来自原典

旧文件把现代九星人物/事项解释、八门吉凶表、九遁用途与格局星级放在古籍标题下，容易造成来源漂移。

处理：现代解释必须单独标 `MODERN_PARAPHRASE / MODERN_SOURCE_GLOSS`。

### 5.2 “多处一致”不能替代 witness comparison

两个现代资料引用同一句，不代表它们独立见到同一原典版本。需要区分：

- 是否互相转引；
- 是否来自同一现代底本；
- 字句是否真的一致；
- 差异是否改变算法。

因此 source consensus 只提高 provenance confidence，不自动提高 Empirical Support。

### 5.3 操作口诀必须绑定 method context

“超神/接气”“置闰”“节气局数”等一旦影响排盘，就必须路由到 `qimen-qiju`：

`text witness -> algorithm interpretation -> setup_method/version -> implementation fixture`

结果后不能因为另一句口诀更符合结果而切换算法。

### 5.4 吉凶歌诀不能越级成现实 verdict

九星、八门、格局的“吉/凶”若来自传统文本，只是 `SOURCE_SYMBOLISM / SOURCE_CLAIM`。现实解盘仍要经过 Role Map、状态、关系、method context、竞争证据与前瞻测试。

## 六、旧文件中的格局干对冲突如何处理

legacy yange 曾把某些格局直接写成“甲/丙”组合，而当前 `qimen-gexia` 又保存了以隐藏甲/遁仪语境表达的其他干对版本。

当前不在本技能里决定谁“正确”。统一标：

`CROSS_SOURCE_PATTERN_LINEAGE_REQUIRED`

并交给 Pattern Registry 比较：

- 原文到底写甲还是遁甲后的六仪；
- 是名称定义、口诀简写还是排盘层转换；
- 天盘/地盘方向是否一致；
- 不同流派是否本来就不同。

没有完成 lineage review 前，不允许把歌诀版本直接写进 operational lookup。

## 七、文本核验等级

### `PAGE_VERIFIED`
主审直接看到 canonical 原页并核对该句/表。

### `LEGACY_ATTRIBUTION`
旧技能/旧笔记声称来源如此，但当前尚未回原页复核。

### `ATTRIBUTION_UNRESOLVED`
连来源作品/版本/页码都不能可靠确定。

### `SOURCE_INCONSISTENCY`
同一来源/同一 legacy artifact 内部出现实质矛盾。

### `CROSS_SOURCE_VARIANT`
不同来源给出不同字句/算法，不强行合并。

## 八、歌诀进入运行层的 Gate

只有当歌诀承载实际算法或角色规则时，才考虑进入运行层，并依次要求：

`PAGE/LINEAGE VERIFIED`
→ `method_context identified`
→ `algorithm interpretation explicit`
→ `implementation checked`
→ `feedback-before freeze field`
→ `prospective eligibility review`

即使全部通过，也只说明来源/实现可重复；预测有效性仍需独立 prospective evidence。

## 九、禁止事项

- 不把 legacy 引用自动升级为 PAGE_VERIFIED；
- 不把现代释义塞进古籍原文名下；
- 不因为多书同引就说“古法已验证”；
- 不静默修正异文；
- 不把歌诀吉凶直接输出为高风险现实事实；
- 不用结果后挑出的异文/口诀修补原预测；
- 不以背诵便利性决定方法正确性。

## 十、后续阅读任务

对《笺元遁甲句解烟波钓叟歌》等 canonical source 的正式 K2 阅读，按 source lineage 与实际 execution lane 进行逐页/逐单元核验。届时：

- 保留原典文本与现代解释分层；
- 记录版本 witness；
- 发现异文不静默合并；
- 只有主审实际核验的页面获得 Reading/Evidence credit。

---

*Yange v2.0 | 2026-08-21 | 从“歌诀大全”迁移为 provenance / variant / method-context registry。*
