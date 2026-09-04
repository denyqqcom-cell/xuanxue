# K2 Prospective Sample Provenance Protocol

版本：2026-09-04  
状态：ACTIVE_CONTRACT  
上游：`K2_PROSPECTIVE_VALIDATION_PROTOCOL.md`  
下游：`K2_PROSPECTIVE_EMPIRICAL_CREDIT_REVIEW_PROTOCOL.md`

## 1. 目的

当前 prospective chain 已能冻结 hypothesis、route、模型版本、comparator、评分函数、固定 N、Outcome 集合、统计政策与 replication review，但 `case_id` 仍只是仓库匿名 token。

因此必须区分：

`CASE_TOKEN_UNIQUENESS != REAL_WORLD_SAMPLE_IDENTITY`

把同一个现实事件改写成另一个 `case_id`，不能因此获得第二个独立样本信用。

本协议增加一个**结果未知前生成、跨 Batch 稳定、仓库中只保存不可逆伪匿名摘要**的 sample fingerprint 层，用于减少最直接的重复计票风险。

它仍然不是现实样本独立性的证明。

## 2. 两个正式 ledger

Policy registry：

`knowledge/K2_PROSPECTIVE_SAMPLE_PROVENANCE_POLICIES.jsonl`

Batch binding ledger：

`knowledge/K2_PROSPECTIVE_SAMPLE_PROVENANCE_BINDINGS.jsonl`

当前 `SAMPLE_PROVENANCE_V1` 固定：

- `fingerprint_method = HMAC_SHA256_V1`
- `fingerprint_scope = PROJECT_WIDE`
- `fingerprint_key_id = K2_SAMPLE_FINGERPRINT_KEY_V1`
- 每个 Batch 必须在第一条 Freeze 前完成绑定
- 每条 Freeze 必须带 fingerprint
- 同一 Batch 内 fingerprint 不得重复
- empirical replication cohort 内 fingerprint 不得重复
- 原始身份材料和 HMAC secret 不得写入仓库
- `research_only = true`

Policy 内容本身通过 canonical SHA256 绑定。若未来轮换 key、method 或 scope，必须新增 policy 版本，不能静默改写 V1。

## 3. 为什么使用 keyed HMAC，而不是普通 SHA256

如果直接对姓名、电话号码、日期、事件编号等低熵身份材料做普通 SHA256，攻击者可以离线枚举候选值并反查摘要。

因此当前 helper 使用：

`HMAC-SHA256(secret, canonical_identity_envelope)`

secret 只存在于本地受控环境，通过环境变量：

`K2_SAMPLE_FINGERPRINT_SECRET`

提供；仓库永远不保存 secret。

helper：

`tools/k2_sample_fingerprint.py`

从 stdin 接收本地 canonical identity JSON，只输出 64 位小写 fingerprint。原始 identity JSON 不应进入 Git、CI log、Issue、PR、Evidence 或 Freeze payload。

核心边界：

`HMAC_FINGERPRINT != ANONYMITY_PROOF`

它只是比未加密普通 hash 更适合低熵身份材料的伪匿名去重标识。拥有 secret 或足够额外信息仍可能造成关联风险，因此原始 identity material 和 key 必须继续留在受控本地边界。

## 4. Batch binding chronology

每个真实 Batch 必须有且只有一个 binding：

`batch_id + exact batch_sha256 + sample provenance policy version/hash`

并满足：

`batch.preregistered_at_utc < binding.bound_at_utc < first_freeze.frozen_at_utc`

这样可以阻止看过案例或结果后才决定 fingerprint 方法、scope 或 key generation。

绑定 ledger 只保存公开 policy/key identifier，不保存 secret。

## 5. Freeze contract

每条 Freeze 的 `frozen_payload` 必须在 outcome 未知时写入：

- `sample_provenance_policy_version`
- `sample_provenance_policy_sha256`
- `sample_fingerprint_key_id`
- `sample_fingerprint`

四者进入既有 `frozen_payload_sha256`，因此 Outcome 继续通过原有 freeze hash chain 继承这份身份去重承诺。

禁止在 payload 中新增：

- `sample_identity`
- `sample_identity_material`
- `raw_sample_identity`
- `raw_identity`
- `fingerprint_secret`
- `sample_fingerprint_secret`
- `sample_fingerprint_key`

这些字段若出现，sample-provenance validator 必须 fail closed。

## 6. 去重层级

当前机器门禁分两层：

1. Batch 内：相同 fingerprint 重复出现直接视为重复样本记录；
2. Empirical replication cohort：即使 `case_id` 不同，只要 stable fingerprint 重复，`sample_fingerprint_unique=false`，不能进入 `READY_FOR_MANUAL_EMPIRICAL_REVIEW`。

因此：

`DIFFERENT_CASE_ID + SAME_SAMPLE_FINGERPRINT -> NOT_ELIGIBLE`

同时仍保留原有 `case_token_unique`，因为 token 与 fingerprint 是两个不同的审计维度。

## 7. 仍然不能证明什么

即使 cohort 内所有 fingerprint 唯一，也只能说明：在**相同 project-wide HMAC contract 与同一 key generation**下，没有检测到完全相同的 identity material 重复。

它不能证明：

- 两个不同 identity material 在统计上独立；
- 同一个现实事件没有被错误规范化成不同 identity material；
- 没有家庭、群体、时间、空间或信息源聚类；
- 样本具有代表性；
- 采样无选择偏差；
- 没有信息泄漏；
- 任何奇门、紫微或其他术数理论成立。

所以：

`SAMPLE_FINGERPRINT_UNIQUENESS != REAL_WORLD_SAMPLE_INDEPENDENCE`

`REAL_WORLD_SAMPLE_INDEPENDENCE != EXTERNAL_VALIDITY`

当前 empirical readiness 仍然最高只到：

`READY_FOR_MANUAL_EMPIRICAL_REVIEW`

并继续保持：

`empirical_credit = NONE`

直到单独的人类/项目信用审查处理现实独立性、泄漏、代表性、外部复现和适用边界。
