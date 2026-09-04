# Empirical Credit Review：Sample Provenance Addendum

版本：2026-09-04  
状态：ACTIVE_CONTRACT_ADDENDUM  
依赖：`K2_PROSPECTIVE_SAMPLE_PROVENANCE_PROTOCOL.md`

本 addendum 不修改 `EMPIRICAL_CREDIT_REVIEW_V1` 的统计 policy 内容或其既有 SHA 语义。它增加一个**正交的 upstream sample-provenance + canonical sample-identity eligibility gate**。

因此：

`EMPIRICAL_CREDIT_POLICY_V1_MATCH`

只是统计/replication policy 完整性的必要条件，不是 empirical-readiness 的全部条件。

从本 addendum 起，`READY_FOR_MANUAL_EMPIRICAL_REVIEW` 还必须同时满足：

- cohort 中每条 Freeze 都存在合法、hash-bound 的 `sample_fingerprint`；
- cohort 中所有 Freeze 使用相同的 sample provenance policy version/hash；
- cohort 中所有 Freeze 使用相同的 project-wide `sample_fingerprint_key_id`；
- cohort 中所有 Freeze 使用相同的 sample identity schema version/hash；
- `sample_provenance_consistent = true`；
- `sample_fingerprint_unique = true`；
- canonical repository 的每个真实 Batch 已在第一条 Freeze 前完成 Sample Provenance Binding，并同时绑定 exact identity-schema version/hash；
- Empirical Credit Review 中声明的 sample provenance policy、key id 与 identity schema version/hash 必须与 cohort Freeze 机器重算结果完全一致。

于是机器条件变成：

`STATISTICAL_POLICY_READY`

`AND SAMPLE_PROVENANCE_CONSISTENT`

`AND SAMPLE_IDENTITY_SCHEMA_CONTEXT_CONSISTENT`

`AND SAMPLE_FINGERPRINT_UNIQUE`

`-> READY_FOR_MANUAL_EMPIRICAL_REVIEW`

若 `case_id` 全部不同、但 stable fingerprint 有重复：

`case_token_unique = true`

`sample_fingerprint_unique = false`

则必须：

`credit_readiness = NOT_ELIGIBLE`

若 fingerprint 本身唯一，但 cohort 中 identity schema version/hash 不一致，也必须：

`sample_provenance_consistent = false`

`credit_readiness = NOT_ELIGIBLE`

原因是不同 identity schema 可能通过改变字段集合或 normalization 规则制造不可比较的 digest namespace；不能把这种 schema drift 当作真实样本差异。

Empirical Credit Review record 现在必须显式携带并由机器重算：

- `sample_identity_schema_version`
- `sample_identity_schema_sha256`

validator 同时验证该 schema version 已注册，并验证 SHA 精确绑定注册内容。Review 不能通过手工填写另一个 schema version/hash 来绕过 cohort 的 Freeze provenance。

这里刻意没有把 sample provenance 或 identity schema 字段塞回 `EMPIRICAL_CREDIT_REVIEW_V1` policy record，因为 PR #41 已确立 policy record 的内容绑定与不可静默改写边界。Sample provenance 与 sample identity schema 是独立版本化合同，由各自 registry/binding/hash chain 治理；这样既不篡改 V1 的历史 policy referent，也能把新的 anti-duplication / anti-representation-drift requirement 加入整体 readiness gate。

最后仍须保持：

`CANONICAL_IDENTITY != CORRECT_REAL_WORLD_IDENTITY`

`SAMPLE_FINGERPRINT_UNIQUENESS != REAL_WORLD_SAMPLE_INDEPENDENCE`

`READY_FOR_MANUAL_EMPIRICAL_REVIEW != EMPIRICAL_CREDIT`

`EMPIRICAL_CREDIT = NONE`

直到人工/项目审查独立处理真实身份解析、样本聚类、真实独立性、泄漏、代表性、外部复现与适用边界。
