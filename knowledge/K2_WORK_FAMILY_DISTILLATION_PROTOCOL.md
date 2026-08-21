# K2 Work-Family Distillation Protocol

版本：2026-08-22
阶段：K2B / Deep Closure
状态：ACTIVE

## 1. 为什么需要 work-family distillate

上下册、分卷与 composite carrier segment 可以分别提供 unique coverage，但它们共同属于一个 work family。若只逐 PDF 摘要，会再次把载体边界误当知识边界。

Work-family distillate 的任务不是把书变短，而是回答：

- 整个 work family 真正增加了什么结构理解；
- 哪些只是作者的方法，而不是现实真理；
- 哪些规则有明确对象与时序边界；
- 哪些旧模型必须被拆分或降级；
- 什么仍然没有 empirical credit；
- 什么候选模型值得进入前瞻验证。

## 2. 数据文件

`knowledge/K2_WORK_FAMILY_DISTILLATES.jsonl`

每一行对应一个已完成 work-family review 的 distillate。

它必须引用：

- `K2_SEGMENT_LINEAGE.jsonl` 的完整 family member set；
- `K2_DEEP_READING_LEDGER.jsonl` 的真实 carrier Reading Credit；
- composite member 的 `K2_SEGMENT_EVIDENCE.jsonl`；
- 未分段 source member 的可审计 `source@pdf:pN` locator。

## 3. Credit 必须拆开

每个 distillate 都必须显式声明：

- `source_credit = FULL_WORK_FAMILY_REVIEWED`；
- `empirical_credit = NONE`，除非未来独立 prospective testing 合法升级；
- `claim_extraction_blocked = true` 在 K2B 阶段保持不变。

古籍越老、作者越有名、上下册越一致，都不能自动增加 empirical credit。

## 4. Credit decision

对于八神、中宫、movement 等关键争议点，不使用“书上有所以就是真”的二元裁决，而记录：

- `topic`；
- `source_credit`；
- `empirical_credit`；
- `decision`；
- `summary`；
- `anchors`。

允许出现 `NO_SOURCE_CREDIT`：完整读完一本书后，明确知道它**没有**支持某个常见说法，本身也是高价值知识。

## 5. 自我生成但不自我迷信

`testable_hypotheses` 可以记录项目自己长出的候选模型，但必须满足：

- 可在反馈前冻结；
- 有明确失败条件；
- 当前状态为 `UNTESTED`；
- 不因它是“自己创新”而获得额外信用。

自建理论也必须接受与古籍相同、甚至更严格的证伪纪律。
