# K2 Source Segments — attribution basis addendum

版本：2026-09-03  
阶段：K2B / Deep Closure  
状态：ACTIVE_CONTRACT

## 1. SOURCE_INTERNAL_ATTRIBUTION

当 segment 的作者归属只来自同一 canonical carrier 内部的题跋、编后语、编辑说明或类似载本内部陈述，而尚未经过外部版本学/文献学核验时，允许：

`author_basis = SOURCE_INTERNAL_ATTRIBUTION`

该 basis 表示“载本内部确实这样归属”，不表示“历史作者事实已经独立验证”。

## 2. 与其他 basis 的区别

- `TITLE_PAGE`：该 segment 自身题名页直接署名；
- `CONTENT_VERIFIED`：segment 正文或可直接归属于正文的内部内容明确建立作者身份；
- `SOURCE_INTERNAL_ATTRIBUTION`：归属来自 carrier 内部编辑性/题跋性陈述，仍需外部作者学核验；
- `UNKNOWN`：现有 reviewed carrier 不能可靠给出作者。

不得为了通过 validator 把 `SOURCE_INTERNAL_ATTRIBUTION` 升格成 `CONTENT_VERIFIED`。

## 3. Credit 边界

`SOURCE_INTERNAL_ATTRIBUTION` 只增加 provenance credit，不增加 method、empirical 或 Claim credit。

`PROVENANCE CREDIT != AUTHORSHIP TRUTH != METHOD VALIDITY != EMPIRICAL VALIDITY`
