# QM-SRC-0027 — 起局 / 子时边界定向审计

Status: `TARGETED_SOURCE_REVIEW / SOURCE_FIDELITY_ONLY / NO_EMPIRICAL_CREDIT / NO_RUNTIME_DEFAULT_CHANGE`

Date: 2026-08-21

Source:

- `QM-SRC-0027`
- `WORK-000228`
- carrier: `善天道-奇门遁甲精华..pdf`
- canonical SHA256: `193a03145b3992d9a78962b205b9fa83b73ee1f368947694b761483ea7112581`
- PDF pages: `32`
- K1 readability: `TEXT_OK`

本次最初目标只是 AQ-004 的 `time_boundary_system` 定向核验。导航过程中实际检查范围扩展到全书 text layer，并对关键页做原页视觉复核。由于正式 `Pre-Book Retrospective` 未在这次全文浏览之前完成，**不得把这次浏览追认成新的 per-book COMPLETE / Reading Credit**。本记录只给被明确复核的 source claims 记 Source Fidelity。

`Process performed != process credit earned`。

---

## 1. 题名与载体署名

PDF p1 页眉可直接看到题名：

`善天道奇门遁甲精华培训教材`

同一页眉另有 `山枫道人` 标识与联系方式。

当前只能安全升级：

- title: `PAGE_VERIFIED`
- `山枫道人`: `PAGE_VERIFIED_HEADER_ATTRIBUTION`

不能仅凭页眉把 `山枫道人` 直接升级为正式作者，也不能继续把文件名中的“善天道”自动当作者名。

这暴露一个旧 K1 元数据风险：`filename attribution != author identity`。

---

## 2. p3：真正的“早子 / 晚子”边界 witness

PDF p3 原页把时辰明确拆成：

- `0:00-1:00`：早子时；
- `21:00-23:00`：亥时；
- `23:00-24:00`：晚子时。

更重要的是，晚子时的时干并不沿用同栏早子时的时干，而是使用下一日干组对应的子时干。

例如在 `甲己日` 一栏：

- 早子时对应 `甲子时`；
- 晚子时对应 `丙子时`。

这说明该来源至少在**时干推定**这一对象上，把 `23:00-24:00` 与次日日干组发生了结构关联。

当前最窄结论：

`SHANTI_DAO_JINGHUA_P3_SPLIT_ZI_HOUR_STEM_BASIS`

它支持：

`SOURCE_DEFINED_OTHER` 的 split-zi boundary candidate。

它**尚不足以单独证明**：

- 23:00 后完整日柱已经统一换日；
- civil calendar date 必须整体前移；
- 所有 setup family 都应采用 `ZI_START_23`；
- 23:00 边界后的完整奇门盘已经有 worked-plate oracle。

因此当前不把它粗暴映射成全局 `ZI_START_23` truth。

---

## 3. p4：超神 / 接气获得 source-specific 方向证据

PDF p4 把上、中、下三元与子午卯酉 / 寅申巳亥 / 辰戌丑未分组，并列出符头。

同页对术语方向作出明确 source-level 定义：

- 超神：上元符头在节气之前；
- 接气：节气在前、上元符头在后；
- 置闰：上元符头超过节气九天；
- 并写有“不置闰—拆补法（推荐方法）”的教学立场。

因此 `QJ-01` 不再只能写成“legacy file 自相矛盾”。现在可以更精确地说：

- `QM-SRC-0027 p4` 明确支持其中一套术语方向；
- 另一套相反定义仍需找到自己的 source witness；
- source-specific 支持不能直接消灭 cross-source / legacy conflict。

`SOURCE AGREEMENT != UNIVERSAL TERMINOLOGY RESOLUTION`。

---

## 4. p4 仍不能关闭“拆补法”算法缺口

本页虽然明确偏好“拆补法”，但没有把以下两个竞争 executable models 充分拆开：

- 固定 `5+5+5` 自然日分段；
- 交节与符头错位时的 `残元 -> 中/下 -> 补元` 模型。

因此：

`拆补法（推荐）` 只是 source teaching preference，**不是完整 executable spec，更不是准确率证据**。

`QJ-02 / QJ-03` 继续保持 `ALGORITHM_VARIANT_REQUIRED / DEFINITION_OVERLAP_UNRESOLVED`。

---

## 5. 八神：同一 32 页载体内部已经混入两套词汇层

p1-p2 / p10-p11 的基础列表使用现代常见序列：

`值符 / 螣蛇 / 太阴 / 六合 / 白虎 / 玄武 / 九地 / 九天`

并给出阳遁顺、阴遁逆的教学说明。

但 p29 婚姻段落又同时出现 `朱雀`、`勾陈`、`白虎`、`玄武` 等词。

因此，即使不借助 71 页讲义，本 source 自身也已经说明：

`one carrier != one clean deity taxonomy`

当前只能分类为：

`SOURCE_INTERNAL_LEXICON_MIX / POSSIBLE_EDITORIAL_SYNTHESIS`

不能从这本教材直接推出：

- `白虎 = 勾陈`；
- `玄武 = 朱雀`；
- 或“阳遁/阴遁必然换名”。

这进一步支持 Test C 继续保持 `UNRESOLVED / NO_RUNTIME_GLOBAL_ALIAS`。

---

## 6. p25-p26：五不遇时的“规则定义”与“列举表”存在张力，但不能再武断叫“漏列”

来源先定义五不遇时为：

`时干克日干 + 阳克阳 / 阴克阴 + 二干相隔五位`

随后列出十个常见日/时组合。

结合本书 p3 的完整十二时辰干支表，若把上述判据机械应用到一整日十二时辰，`己日` 的 `乙亥`、`庚日` 的 `丙戌` 会成为需要进一步解释的候选。

过去项目曾直接把这件事写成“原表漏列第二时辰”。现在降级为：

`DERIVED_ENUMERATION_TENSION / LINEAGE_CHECK_REQUIRED`

原因：

1. 推导成立不等于传统术语定义一定按纯算法穷举；
2. 可能还存在未写出的 branch / day-boundary / conventional-selection condition；
3. 需要另一独立原始来源说明五不遇时到底是十个专名组合，还是按判据全日扫描。

因此旧结论“确定漏列”属于过度确定，应视为历史认识债务，不再作为 active rule。

---

## 7. 高风险断语继续隔离

p26-p32 大量把固定用神、吉凶、婚姻、疾病、刑事、求财等直接连接到具体现实结论。

其中包含婚姻早亡、疾病年命不保等高风险确定性语言。

本次分类统一为：

`SOURCE_CLAIM / HIGH_RISK / NOT_CLAIM / RESEARCH_ONLY`

不得因“教材写得很明确”就进入当前高风险现实判断层。

`Source Fidelity can be high while Empirical Support remains zero/unknown.`

---

## 8. 对现有 Setup Registry 的实际影响

### QJ-01 超神 / 接气

`NARROW / SOURCE-SPECIFIC SUPPORT ADDED`

`QM-SRC-0027 p4` 支持“符头在前为超神，节气在前为接气”这一 source-specific terminology。

### QJ-02 / QJ-03 拆补

`NO-OP`

有名称偏好，没有足够 executable detail。

### QJ-04 子时边界

`SOURCE_BOUNDARY_WITNESS_FOUND`

p3 提供真正的 23:00 / 0:00 split-zi witness，并显示晚子时的 hour-stem day-basis 发生变化。

但仍：

`EXECUTABLE_FULL-PLATE_CONTROL_NOT_READY`

因为没有找到同页或邻页的 23:00 边界 worked plate 来独立核对完整日柱 / 局 / 星门神。

---

## 9. 下一步判别实验

AQ-004 下一步不再问“有没有人说 23 点换日”，而要找能区分算法对象的原页：

1. 明确 22:xx 与 23:xx 的日干支 / 时干支变化；
2. 或给出 23:00-00:59 的 worked plate；
3. 同时能确认所用 setup family；
4. 最好允许并行生成 `CIVIL_MIDNIGHT` 与 source-defined split-zi 两个模型；
5. deliberate wrong-boundary model 必须在 source oracle 上失分，才算真正 negative control。

在找到这种 witness 之前，不为“完成 AQ-004”制造伪边界测试。

---

## 10. 本轮方法论教训

这次还有一个流程层错误：研究起点是 targeted source attack，但导航时顺手把 32 页 text layer 全部读了。

这本身不是知识错误，却暴露了一个新风险：

`research curiosity can bypass a pre-book gate without malicious intent`。

所以正式处理是：

- 保留已经看到的内容，不假装没看过；
- 不追认 per-book COMPLETE credit；
- 把 source-specific 新证据记在本 targeted review；
- 若未来把 QM-SRC-0027 升级为正式完整 K2 book cycle，先补一个明确标记为 `POST-EXPOSURE RETROSPECTIVE` 的隔离记录，再按协议重做正式 distillate；
- 不通过“补一个文档”伪造时间顺序。

**流程真实性本身也是 Evidence discipline 的一部分。**
