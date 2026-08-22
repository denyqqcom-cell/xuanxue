# K2 Evidence Re-audit Protocol

版本：2026-08-23  
阶段：K2B / Deep Closure  
状态：ACTIVE

## 1. 为什么不直接改写旧 Evidence

Atomic Evidence 的职责是忠实记录“某来源在某页说了什么”。  
后续完整阅读可能发现来源不独立、规则只适用于特定场景、存在高风险应用，或旧的 `claim_readiness` 过于宽松。

若直接删除或重写历史 Evidence，会把“来源事实”和“项目后来学会了什么”混在一起，破坏审计链。

因此使用：

`SOURCE EVIDENCE -> RE-AUDIT OVERLAY -> EFFECTIVE READINESS`

Re-audit 只能维持或收紧后续可用性，不能偷偷把旧记录升级得更可信。

## 2. 数据文件

- `knowledge/K2_EVIDENCE_REAUDIT_STATE.json`
- `knowledge/K2_EVIDENCE_REAUDIT.jsonl`
- `knowledge/schema/evidence_reaudit.schema.json`

`coverage=COMPLETE` 的 target 必须覆盖该 source 当前全部 Atomic Evidence；少一条就 fail。

## 3. disposition

- `KEEP`：保留原 `claim_readiness`；
- `HOLD_CONFLICT`：原本就是 `CONFLICT_CANDIDATE`，继续保留冲突状态；
- `DOWNGRADE_NOT_CLAIM`：来源记录仍保留，但后续不得当作可操作 Claim；
- `REJECT`：保留历史痕迹，但明确排除后续使用。

## 4. Course-family gate

若 `K2_COURSE_LINEAGE.jsonl` 已证明该 source 属于不独立的课程家族：

`independence_policy = COURSE_FAMILY_SINGLE_VOTE`

这意味着同家族多本讲义内容一致时，最多取得一个来源家族 credit；不能因 0027/0028/0029 三个 PDF 一致而得到三票。

## 5. 高风险材料

医疗、金融、法律/刑事等传统占断条目可以作为“该来源如此取用”的历史研究材料保留，但不应仅凭术数文本进入现实操作规则。

因此 re-audit 可将其有效状态降为：

`NOT_CLAIM`

这不是裁决该来源“真假”，而是把文本支持与现实高风险建议分开。

## 6. Fail-closed 规则

`tools/validate_k2_evidence_reaudit.py` 必须保证：

- audit row 引用真实 Atomic Evidence；
- source_id 必须匹配；
- effective readiness 不得比原记录更宽松；
- `KEEP` 不得改变 readiness；
- `HOLD_CONFLICT` 只能用于原冲突记录；
- `DOWNGRADE_NOT_CLAIM` 必须真正降为 NOT_CLAIM；
- 高风险 audit 必须 NOT_CLAIM；
- course-family 非独立成员必须使用 single-vote policy；
- `coverage=COMPLETE` 必须 100% 覆盖 target source 的 Evidence；
- K2B 期间 `claim_extraction_blocked=true` 保持不变。

Re-audit 的目标不是制造更多记录，而是让已有记录**可以被降权、冻结、排除，并留下原因**。
