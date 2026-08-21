# 奇门 Theory - Validation - Landing Matrix

状态：ACTIVE / v0.1 / 2026-08-21

目的：任何重要认识都必须同时回答三个问题：

1. **Theory**：我们到底主张什么？
2. **Validation**：它被哪一种证据检验过？
3. **Landing**：它是否进入 runtime / App / 解盘？以什么边界进入？

本矩阵防止：

`书证很多 -> 直接上线`

或：

`代码能跑 -> 当成理论正确`

或：

`App 已上线 -> 倒推已经验证`。

---

## 状态码

- `T0`：只有想法/来源线索
- `T1`：claim 与适用域已定义
- `T2`：有 rival / failure condition，可测试
- `V0`：未验证
- `VS`：Source Fidelity 有支持
- `VI`：Implementation Fidelity 有支持
- `VN`：已有 deliberate negative control
- `VP`：有 clean prospective support
- `L0`：未进入运行层
- `LR`：进入 research/runtime variant
- `LA`：进入 App/用户执行路径
- `LG`：成为 global default
- `BLOCKED`：明确不允许继续升级

`VS / VI / VN` 都不等于 `VP`。

---

## 当前关键对象矩阵

| 对象 / claim | Theory | Validation | Landing | 当前结论 / 下一步 |
|---|---|---|---|---|
| 梁书十八局 `甲子` sparse chief identity | T1 | VS + VI + VN | LR | 只覆盖 tracked sparse anchors；不得外推 full chart |
| `SHANTI_DAO_71_P21_P22` non-Jiazi rotation profile | T2 | VS + VI + VN + selected cross-source VI | LR + LA | 可复现有限 worked-plate 星/门/神结构；没有预测 Empirical Support |
| 中五值使 full-door host rule | T1 | VS 不足 | L0 / fail-closed | `SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED`；等独立 worked plate |
| `TIME-BRANCH INTERVAL` | T1 | VS | L0 | 来源可定义时支区间；不能自动推完整换日 |
| `HOUR-STEM DAY-BASIS` split-zi | T2 | QM-SRC-0027 p3 = VS | L0 | `23-24` 晚子时使用下一日干组五子遁；仍不是完整 day rollover |
| `DAY-PILLAR ROLLOVER` at 23:00 | T2 | V0 | L0 / BLOCKED | 缺边界 worked plate；不得用晚子时表偷证完整换日 |
| 八神 universal `白虎=勾陈 / 玄武=朱雀` | T1 rival hypotheses exist | cross-source VS shows conflict | BLOCKED | 不允许 global alias；Test C 仍 UNRESOLVED |
| `ZHU_BAI_DUAL_POSITION_WITNESS` | T1 | targeted visual VS | L0 | 只证明一条早期 carrier/context 的 distinct simultaneous positions |
| 九星旺相休囚分类 | T1 | two source convergence = VS | LR as source-specific state system | 不能恢复固定数值权重；继续查 lineage / prospective ablation |
| `旺相全额 / 休囚减半` | historical claim only | V0 / contradicted by evidence discipline | BLOCKED | DEPRECATED；除非新 prospective test 重新建立 |
| 八门旺衰 state system | T1 | incomplete VS | L0/variant only | AQ-005 尚未闭合；需第二个 method-context 清楚来源 |
| `Sequence-Object Type Safety` | T2 engineering discipline | VI/VN through engine failures & tests | LR + LA indirectly | 保持；若没有减少 implementation error，可压缩 |
| `Representation-Object Type Safety` | T2 | VI/VN via hidden-Jia failure | LR | 保持；继续寻找 representation drift |
| `Semantic-Object Type Safety` | T2 | source-review failure modes = VS-methodology | Research only | 不能因相同 token 跨 method object 合并 lineage |
| Context Compression | T2 | V0 prospective | protocol/constraints only | 需要 `SOURCE_RESTRICTED vs CONTEXT_FROZEN_RELATIONAL` matched prospective |
| Role Map Freeze | T2 | V0 prospective | research protocol | 需 analyst agreement + matched outcome test |
| Branch-Discrimination Gate | T2 | protocol-level only | research protocol | 需验证是否减少 all-branches-can-hit |
| Baseline Firewall | T2 | protocol-level only | research protocol | 需 auxiliary ablation 与 contamination audit |
| Outcome-to-Rule Firewall | T2 | historical failure rationale | authoritative constraint | 需观察是否减少 single-case global patches |
| `反证情境压缩法 v0.3-alpha` | T2 | V0 overall | research methodology only | PROVISIONAL / UNVALIDATED；不升 v0.4 |

---

## 升级规则

### Theory 升级

`T0 -> T1` 需要 claim 与适用对象明确。

`T1 -> T2` 需要：

- rival model；
- observable discriminator；
- failure condition；
- 结果后不可改变的关键字段。

不能因为“解释很有道理”升 T2。

### Validation 升级

`VS`：只说明来源读对/多个来源关系更清楚。

`VI`：只说明实现能复刻 source oracle。

`VN`：说明测试会拒绝某些 deliberate wrong input。

`VP`：必须 clean unknown-outcome、feedback 前 freeze、可评分，并保留 miss。

任何对象没有 VP，不得写“现实有效已验证”。

### Landing 升级

`L0 -> LR`：可以进入显式 research/source-specific variant。

`LR -> LA`：进入 App 前必须保留 profile、warning 与 evidence boundary。

`LA -> LG`：成为 global default 是最高风险动作；至少要求 method/source conflicts 已有合理解决，并需要比单纯 VI/VN 更强的现实证据。

目前奇门核心争议对象原则上不允许轻易 `LG`。

---

## 每轮更新纪律

每次重要 book cycle、implementation bug、negative control 或 prospective outcome 后，先更新这里的**状态变化**，再考虑写新理论。

允许的变化包括：

- `T2 -> T1`：发现 claim 过宽；
- `VI -> VS only`：发现 implementation oracle 不独立；
- `LR -> L0`：variant 证据不足，撤回；
- `BLOCKED`：明确禁止旧结论复活；
- `NO-OP`：新资料没有改变状态。

这个矩阵的价值不是让每个格子越来越高级，而是让“没有升级”也成为合法学习结果。
