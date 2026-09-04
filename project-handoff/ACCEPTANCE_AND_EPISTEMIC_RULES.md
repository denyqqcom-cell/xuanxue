# ACCEPTANCE AND EPISTEMIC RULES

本文件定义“什么可以叫 PASS，什么不能叫证据”。

## 1. 五条状态链，禁止一个总完成度

### Corpus Mastery

记录：Registry / Lineage / Reading / Evidence / Distillate / Conflict / Applicability。

不能把 `515 sources registered` 写成 `515 sources learned`。

### Cognitive Reconstruction

记录：Theory / assumptions / boundary / rival model / abstention / belief revision。

一本书或多个来源一致，只能增加 source support，不能自动升级现实真值。

### Engine Structural Credit

记录：algorithm identity / source-grounded fixture / reproducibility / school/method scope。

`one fixture PASS != whole algorithm PASS`

`whole board structural PASS != predictive validity`

### Product Acceptance

记录：Core / Knowledge / Product UX / Emulator / Physical。

UI 能正确分层，不等于分层内容本身现实有效。

### Prospective Empirical Credit

记录：Preregistration / Batch / Freeze / Outcome / Batch Review / replication / manual credit decision。

没有真实 prospective outcome 时，`empirical_credit = NONE`。

## 2. Acceptance status vocabulary

统一使用：

- `PASS` — exact scope / exact head 有直接证据；
- `FAIL` — exact scope 可复现失败；
- `INHERITED` — binary/tree/implementation 与旧验收等价，但本 exact head 未执行；
- `BLOCKED` — 因权限、依赖或先决条件不能执行；
- `NOT_RUN` — 可以执行但本轮未跑；
- `NOT_APPLICABLE` — 本次改动不涉及该层；
- `UNKNOWN` — 证据不足，不能判。

禁止把 `INHERITED / BLOCKED / NOT_RUN` 写成 PASS。

## 3. 四层工程 acceptance

### CORE

确定性核心逻辑与 unit tests。

### KNOWLEDGE

Source/Lineage/Reading/Evidence/Claim/Prospective governance contracts。

### EMULATOR / PRODUCT

App assemble/lint/instrumentation、窄屏/宽屏、用户实际 UI contract。

### PHYSICAL

Moto X30 Pro 或指定真实设备 exact-head instrumentation / smoke / screenshot evidence。

若没有 exact-head physical execution：最多 `INHERITED`。

## 4. Product provenance contract

奇门用户界面当前要求四类分析 provenance：

1. `CHART_FACT / 盘面事实`
2. `SOURCE_RULE / 来源规则`
3. `PROJECT_INFERENCE / 项目推论`
4. `UNVERIFIED_HYPOTHESIS / 未经验证假设`

用户现实输入单独呈现，不属于四类。

四类是**信息性质**，不是吉凶等级，也不是 EvidenceGrade 的替代品。

## 5. Epistemic invariants

长期强制：

```text
Evidence != Truth != Claim
Source Credit != Method Credit != Empirical Credit
CI PASS != Predictive Validity
Fixture PASS != Metaphysical Truth
Source Agreement != External Validation
Known-outcome Retrospective Explanation != Prospective Prediction
Canonical Sample Identity != Correct Real-world Identity
Unique Sample Fingerprint != Statistical Independence
READY_FOR_MANUAL_EMPIRICAL_REVIEW != Empirical Credit
```

## 6. World Model Before Symbols

奇门 contextual reasoning 的次序不得回退为 symbol-first：

```text
M0 Reality input normalized/frozen
M1 Reality-only world model
M2 Chart/symbol mapping enters
M3 Prediction / ABSTAIN / UNEVALUABLE frozen
M4 Narrative can explain M3 but cannot rewrite it
```

若 M1 消费了奇门盘面字段，则属于 information-order violation。

## 7. Anti-KPI rules

以下都不是强制数量目标：

- 必须 DELETE 至少一条规则；
- 必须发现固定数量 latent factor；
- Evidence 条数越多越好；
- gate 数越多越成熟；
- CI run 数越多越可靠；
- 达到某个全库阅读比例就自动允许单一实验。

认知审查允许：

```text
KEEP
MERGE
DOWNGRADE
SPLIT
DELETE
```

结果由证据决定，不为了 KPI 做理论动作。

## 8. Reading / Evidence boundary

- `packet READY != read COMPLETE`
- `Deep Reading != Formal Wave1 COMPLETE`
- `Composite Execution Closure != Legacy COMPLETE`
- `Evidence count != independent vote count`
- 同一作品不同扫描/册/派生 carrier 不得重复增加独立支持票。

现代书籍不得复制长段原文进入公开 Git；保存 derived fact + locator + provenance。

## 9. Experiment boundary

生产实验必须在 outcome 之前冻结：

- exact hypothesis content/context；
- model/engine version；
- comparator；
- sample size；
- scoring function；
- decision rule；
- sample identity/provenance schema；
- sample binding；
- outcome route；
- review/credit policy。

真实 Batch / Freeze / Outcome 一旦开始，不允许事后换规则、换 metric、补样、挑 case、挑 replication subset。

## 10. Merge / destructive action boundary

- 未明确授权：不 Merge；
- 不删除历史失败；
- 不为了对齐 remote 粗暴 `reset --hard`；
- local-only commits 先 preserve；
- secrets / raw identity / private corpus path 不进入公开 Git。
