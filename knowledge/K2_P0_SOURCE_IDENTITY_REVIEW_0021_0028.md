# K2 P0 Source Identity Review — QM-SRC-0021 / QM-SRC-0028

状态：`PARTIAL / FAIL_CLOSED / NO_EMPIRICAL_CREDIT`  
用途：把 P0 来源的 `metadata verification`、`carrier identity`、`page-level content verification` 三层彻底分开，避免“有标题/作者记录”被误写成“原 PDF 已完成身份核验”。

## 1. 三层门禁不是一件事

```text
L1 METADATA_VERIFIED
= 作者/题名/版本等字段能锚定到已复核页

L2 CARRIER_IDENTITY_VERIFIED
= 当前可访问 PDF carrier 的 SHA-256 与 canonical K1 file_sha256 完全一致，或已完成 variant/page-map review

L3 TARGET_PAGE_VERIFIED
= 当前研究所依赖的具体算法页、盘图页、日期/时柱页已经在该已确认 carrier 上重新核对
```

任何一层通过都不能自动替代下一层。

特别禁止：

```text
K1 metadata exists -> carrier verified
Wave1 COMPLETE -> target page visually verified
same title -> same carrier
same work variant -> independent source
```

## 2. QM-SRC-0021

Canonical K1 identity metadata：

- source_id: `QM-SRC-0021`
- work_id: `WORK-000027`
- title: `《奇门遁甲预测学》（奇门遁甲现代应用技术）`
- author: `幺学声`
- author_basis: `TITLE_PAGE`
- author_evidence: `题名页（PDF p1）列作者为幺学声`
- canonical_sha256: `e804e292b446821e40965caa012e51d256f9eb9317f8b9519bbf4baebdbf4dd9`
- pages: `285`
- readability: `TEXT_OK`
- K2 reading: `COMPLETE / TEXT_LAYER_FULL / p1-p285`

### L1 METADATA_VERIFIED

`CLOSED`

`K2_VERIFIED_SOURCE_METADATA.jsonl` 已新增：

- evidence_locator: `pdf:p1`
- verification_basis: `TEXT_LAYER`
- verified title + author

这只确认 metadata provenance，不确认当前 ChatGPT Web 项目中的 PDF bytes。

### L2 CARRIER_IDENTITY_VERIFIED

`OPEN`

当前 GitHub knowledge tree 不打包该 PDF，K1 policy 为：

`local_only=true / packaged=false / SANITIZED_METADATA_ONLY`

关闭条件：

1. 取得当前可访问 carrier；
2. 计算 SHA-256；
3. 若等于 canonical SHA，则标 `CANONICAL_CARRIER_MATCH`；
4. 若不等，则进入 `VARIANT_REVIEW_REQUIRED`，先建立 edition/front-matter/page-map。

### L3 TARGET_PAGE_VERIFIED

`OPEN / PARTIAL HISTORICAL REVIEW ONLY`

当前研究仍需要在 L2 通过后的 carrier 上重新核验：

- 2004-05-29 戊午时完整 source plate；
- 拆补 / 定元相关原页；
- weather-v0.1 天柱/天蓬乘壬癸规则原页；
- 之前撤回的 2002 weather example 日期/时柱字段。

旧 Atomic Evidence / Distillate 可以帮助定位，但不能替代该页重新核验。

## 3. QM-SRC-0028

Canonical K1 identity metadata：

- source_id: `QM-SRC-0028`
- work_id: `WORK-000018`
- title: `善天道-奇门遁甲讲义71页`
- author: `善天道`
- author_basis: `FILENAME`
- canonical_sha256: `bd15a964d722e1b013367741f69460467f354dab73c927fe30409c041c060243`
- pages: `71`
- readability: `TEXT_OK`
- K2 reading: `COMPLETE / TEXT_LAYER_FULL / p1-p71`

### L1 METADATA_VERIFIED

`OPEN`

原因：当前 K1 作者依据仍是 `FILENAME`。虽然课程内容已经完整阅读，但这不等于题名页/署名页已经形成独立 verified-metadata 记录。

不得为了与 0021 状态对称而伪造 `TITLE_PAGE` 依据。

关闭条件：从 canonical carrier 的题名页、封面、版权页或正文明确署名处建立可复核 locator；若没有作者署名，则只验证实际可支持的字段，不强求 author。

### L2 CARRIER_IDENTITY_VERIFIED

`OPEN`

与 0021 相同：必须对当前可访问 carrier 做 SHA / variant identity 检查。

另外：

`QM-SRC-0044` 已在 lineage 中标为：

- relation: `SAME_WORK_VARIANT`
- variant_of_source_id: `QM-SRC-0028`
- independence_class: `SAME_WORK_NOT_INDEPENDENT`

所以 0028 与 0044 不得作为两个独立来源票关闭方法独立性门。

### L3 TARGET_PAGE_VERIFIED

`OPEN`

P0 目标页包括：

- p16-p17：甲/己五日符头及上中下元地支分类；
- p17-p18：拆补法交节切换；
- p18：拆补与置闰方法立场及来源自身承认的非绝对结果；
- 任何未来用于 engine golden fixture 的完整 dated plate 页。

现有 Atomic Evidence 对上述规则有 TEXT_LAYER 支持，但在 carrier identity 未关闭前，不提升为 canonical page identity closure。

## 4. 当前 Gate 状态

```text
QM-SRC-0021 METADATA_VERIFIED        = CLOSED
QM-SRC-0021 CARRIER_IDENTITY          = OPEN
QM-SRC-0021 TARGET_PAGE_VERIFICATION  = OPEN

QM-SRC-0028 METADATA_VERIFIED        = OPEN
QM-SRC-0028 CARRIER_IDENTITY          = OPEN
QM-SRC-0028 TARGET_PAGE_VERIFICATION  = OPEN

QM-SRC-0044 INDEPENDENT_VOTE          = FORBIDDEN
```

因此：

`JU_METHOD_VALIDATION` 继续 OPEN。  
`PLATE_PAIRING_VALIDATION` 继续 PARTIAL。  
不得创建 weather Batch。  
不得增加 Empirical Credit。

## 5. 认识论结论

本 review 的价值不是增加一条术理规则，而是阻止三类来源幻觉：

1. **metadata illusion**：有书名作者记录，就当作原 PDF 已确认；
2. **reading illusion**：全书读完，就当作每个目标页的版式/字段都已重新验证；
3. **independence illusion**：同一课程的不同 carrier，被算作两个独立来源。

只有 L1/L2/L3 分层关闭后，来源才能进入下一层 JuMethod / Plate fixture 验证。
