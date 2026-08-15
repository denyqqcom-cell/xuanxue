# Local Corpus K1 Remediation Prompt

把下面整段转发给能访问 `/home/joe/knowledge-intake/` 与本机 corpus 的 AI。目标是**关闭 K1 的索引与会计问题**，不是开始 K2，也不是补术数规则。

---

你现在负责 Xuanxue Knowledge Engine v1 的 **K1_RECONCILIATION**。

已有 K1 Source Registry 位于：

`/home/joe/knowledge-intake/`

已报告：扫描 910 个文件、541 个不同 SHA256；六域 canonical unique 合计 514、duplicates 合计 345。项目端复核发现当前汇总存在两项未解释差额：

- 910 - (514 + 345) = 51 个扫描文件尚未在总账中明确 disposition；
- 541 - 514 = 27 个 distinct SHA 尚未解释为什么不是 canonical domain source。

**不要假设这些是错误，也不要为了对数而改数字。必须逐文件建立可审计总账，确认它们究竟是 cross-domain、excluded、unsupported、archive/container、project artifact、重复登记遗漏，还是原统计口径问题。**

## 1. 先获取项目端 validator

从仓库分支 `knowledge-engine-v1` 使用最新版：

`tools/validate_k1_intake.py`

不要修改 validator 来迁就现有输出。若输出格式与合同不一致，修正 intake 元数据。

## 2. 新增全局本机总账

在 `/home/joe/knowledge-intake/` 根目录新增：

### `inventory_ledger.jsonl`

对本轮“扫描过”的每一个文件必须恰好一行，至少：

`path, sha256, disposition, domain, source_id, reason`

`disposition` 只能是：

- `CANONICAL`
- `DUPLICATE`
- `EXCLUDED`
- `CROSS_DOMAIN`
- `OTHER`

规则：

- `CANONICAL` 必须有 source_id；
- `EXCLUDED/OTHER` 必须写具体 reason；
- duplicate 必须能追到 canonical source；
- 不允许为了让数字吻合而重复/伪造 ledger 行；
- ledger 只留本机，不提交 Git。

### `K1_ACCOUNTING.json`

至少：

```json
{
  "scanned_files_total": 910,
  "distinct_sha256_total": 541,
  "accounting_method": "...",
  "notes": "..."
}
```

如果重新逐文件核对后发现 910 或 541 原统计有误，可以修正，但必须在 notes 解释旧数 → 新数的原因和证据。

## 3. 纠正 K1 Gate 语义

项目端明确区分：

### K1_INDEX_STATUS

回答：本机可发现 corpus 是否已经诚实发现、去重、索引？

### K2_READINESS

回答：这些资料是否足够丰富/可读，可以进入有价值的 Claim Extraction 与后续交叉验证？

因此：

- `liuyao` 书少，不自动等于 K1 PARTIAL；如果所有可发现六爻资料都已经索引，K1 可以 PASS，但 K2_READINESS 可以是 `THIN_CORPUS`。
- `fengshui` 没有笔记、体系尚未拆读，也不自动等于 K1 PARTIAL；如果资料发现与索引完整，K1 可以 PASS，但 K2_READINESS 可以是 `READING_REQUIRED` / `THIN_OR_UNBALANCED_CORPUS`。

**禁止为了拿 PASS 人为增加、移动或重复来源。**

请在每个领域 `K1_REPORT.md` 增加：

- `K1_INDEX_STATUS = PASS | PARTIAL | BLOCKED`
- `K2_READINESS = READY_FOR_EXTRACTION | THIN_CORPUS | READING_REQUIRED | BLOCKED`
- `coverage_gap = ...`

## 4. 六爻专项复核

重新检查之前被八字目录发现、但内容更接近卜筮/六爻的 cross-domain 资料，例如《火珠林》及其他卜筮类资料，确认：

- 是否应该只作为 `cross_domain` 候选；
- 是否已有六爻目录 canonical copy；
- 是否因目录位置错误而漏入六爻 Source Registry。

不要把梅花易数等不同体系为了增加数量强行算成六爻。

## 5. 风水专项复核

K1 不要求已经读懂全部体系，但 Source Registry 必须能看出候选资料至少属于/可能属于：

- 形势
- 八宅
- 玄空飞星
- 三元
- 三合
- 罗盘/坐向基础

无法判断写 `UNKNOWN`，不要凭模型常识给 school。

同时把“坐山/向首/度数/磁北真北/建造入伙时间”等未在索引命中的内容作为 K2 coverage gap，不要假装已经有资料支持。

## 6. 重新执行项目端机器验收

完成后在本机执行等价命令：

```bash
python3 tools/validate_k1_intake.py /home/joe/knowledge-intake \
  --write-summary /home/joe/knowledge-intake/K1_VALIDATION_RESULT.json
```

如果你的当前 checkout 没有该脚本，从 `knowledge-engine-v1` 分支读取它；不要把整个 intake git add。

必须得到：

`k1-intake: PASS`

若 FAIL，按错误修 intake，直到 PASS 或遇到无法解决的真实 blocker。

## 7. 最终回报

不要开始 K2。

只回报：

1. `K1_VALIDATION_RESULT.json`
2. `K1_ACCOUNTING.json`
3. 六域新的 `K1_INDEX_STATUS / K2_READINESS / coverage_gap`
4. 原 51 文件差额分别落到哪些 disposition、多少条
5. 原 27 distinct SHA 差额如何解释
6. 若 910/541 被修正，给旧值→新值及原因
7. validator 最终 PASS/PARTIAL/BLOCKED

不要上传原书、扫描页、全文 OCR，也不要执行 git add/commit/push。

---
