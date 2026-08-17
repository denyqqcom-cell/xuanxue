# Engineering handoff standard

`handoff/` 是本地研究材料与可进入 App 逻辑之间的工程边界。`knowledge/` 则是新的六术统一知识治理层；两者配合使用，不把原书复制进 Git。

六个正式术数域：`ziwei / bazi / qimen / liuyao / liuren / fengshui`。黄历属于公共历法/民俗工具，不作为第七个术数域参与成熟度竞争。

## 当前迁移状态

- `qimen/`：已有第一套完整 handoff pack，但完整九宫 golden board 仍为 0；迁移到 `knowledge/` 时只做引用与结构化再审计，不抬高成熟度。
- `ziwei/`：现有 Kotlin 与 iztro fixture 属于实现 parity 证据；仍需要独立 corpus/provenance handoff。
- `bazi/`：需要 K1 corpus index 后再建立 handoff。
- `liuyao/`：需要 K1 corpus index 后再建立 handoff。
- `liuren/`：需要 K1 corpus index 后再建立 handoff。
- `fengshui/`：首次纳入统一工程治理，必须先分清形势、八宅、玄空、三元、三合、罗盘/坐向等体系，禁止大一统混算。

六域 K1 本地书籍盘点统一使用 `LOCAL_CORPUS_K1_PROMPT.md`，每次只处理一个领域。

## 每个完成版 handoff 必须包含

1. `00_CORPUS_MANIFEST.md` — 唯一来源、重复项、版本/时代、页数/文本层、本地路径、版权状态。
2. `01_SYSTEM_MAP.md` — 系统层次、术语、流派边界和依赖图。
3. `02_ALGORITHM_SPEC.md` — 只写可计算步骤，明确输入、输出、条件和 school id。
4. `03_RULES.jsonl` — `rule_id / conditions / source_ids / confidence / conflicts / implementation_ready`。
5. `04_CONFLICTS.md` — 不同书/流派冲突，不得强行平均成假共识。
6. `05_FIXTURES.jsonl` — 可复现输入、预期结构输出、来源、school、是否 retrospective。
7. `06_CASES.md` — retrospective / half-blind / blind 分开；回看解释不当作预测准确率。
8. `07_COPYRIGHT_GATE.md` — `ALLOW_IN_APP / RESEARCH_ONLY / FORBIDDEN_TO_PACKAGE`。
9. `08_IMPLEMENTATION_HANDOFF.md` — Kotlin API、config、Unsupported、错误与测试清单。
10. `09_OPEN_QUESTIONS.md` — 缺失证据和 blocker。
11. `HANDOFF_SUMMARY.md` — 数量、成熟度、最大冲突、版权风险、下一工程任务。

## 三层边界

1. **Structure** — 历法/排盘/装卦/起课/坐向等确定性结构。
2. **Selection** — 用神、类神、主客、宫位/对象选择，必须绑定具体事体与流派。
3. **Interpretation** — 情境推演、反证、应期和置信边界。

如果 handoff 只验证 Structure，UI/AI 就只能开放 Structure。模型记忆不是补齐 Selection/Interpretation 的许可证。

## 自动 Gate

`tools/validate_handoff.py` 继续负责既有 handoff pack 的完整性；`tools/validate_knowledge.py` 负责六术统一 Knowledge Engine 的领域、成熟度、schema 与版权边界。

正式规则不得使用 `MODEL_KNOWLEDGE_ONLY` 作为算法来源或 golden fixture。规则即使有书本来源，也必须独立改写为程序事实/过程，并明确 school、冲突和输入输出。

## 最低实现 Gate

一条算法进入 App core 至少要求：

- provenance 明确；
- school/method 明确；
- 输入输出可执行；
- 冲突已由证据解决、配置化或保持 Unsupported；
- 精确算法路径有至少一条 reproducible fixture；
- fixture 不是纯模型知识；
- copyright gate 允许进入 App。

判断/解释规则还必须声明具体事体条件。`符号 -> 固定现实结论` 不会因为传统上常见就自动成为 implementation-ready。

## 版权边界

禁止提交或打包现代书扫描、全文 OCR、完整现代表格/图解、长现代翻译/注释、商业 App 文案、未知许可截图/字体/视觉资产。

古籍底文与现代扫描、标点、翻译、注释、排版属于不同版权对象；古籍公版不自动意味着现代数字影像可再分发。
