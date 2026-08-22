# K2 Course-Provenance Lineage Protocol

版本：2026-08-23  
阶段：K2B / Deep Closure  
状态：ACTIVE

## 1. 为什么 Source Lineage 还不够

`K2_SOURCE_LINEAGE.jsonl` 解决的是“是不是同一作品、同一分卷、同一载体覆盖”的 work identity 问题。  
但教学体系还存在另一种依赖：**不同作品可以来自同一课程、同一讲师体系、同一套讲义演化链**。

因此必须把两层分开：

`WORK LINEAGE != COURSE PROVENANCE`

同课并不等于同书；同书也不需要再用同课关系表达。

## 2. 数据文件

- `knowledge/K2_COURSE_LINEAGE.jsonl`
- `knowledge/schema/course_lineage.schema.json`

每行绑定一个 canonical `source_id` 与其既有 `work_id`，只描述跨作品的教学来源关系，不改写 `K2_SOURCE_LINEAGE.jsonl` 的作品身份。

## 3. 核心规则

1. 同一 `course_family_id` 中的成员必须是**不同 work_id**；同一作品的扫描、分卷、版本仍由 Source Lineage 处理。
2. `SAME_TEACHING_PROVENANCE` 表示共享教学体系，不证明一个文件复制自另一个文件。
3. `DERIVATIVE_TEACHING_PROVENANCE` 只表示课程层的摘要、汇编或再表达关系；没有直接书目证据时，不得据此宣称确定的出版先后或逐字派生。
4. resolved course family 的成员 `independent_vote_allowed=false`。跨源一致性最多取得一个 provenance-family credit，不能按 PDF 数量重复计票。
5. 同课成员仍可提供不同的 unique coverage；“不独立投票”不等于“不值得读”。
6. 作者、年代、版本、school attribution 不得沿 course family 自动传播。每个 source 仍需自己的页面证据。
7. Course provenance 只影响来源独立性与后续证据权重，不提供 empirical credit，不把 Evidence 升格为 Truth/Claim。
8. 如果关系尚不能从内容证明，保留 `UNKNOWN`，不得为了闭环而猜测。

## 4. course_role

- `FOUNDATION`：基础课程/基础讲义；
- `ADVANCED_EXTENSION`：同一教学体系的高级或扩展课程；
- `SYNOPSIS_COMPENDIUM`：把同体系知识压缩、汇编、速查化的载体；
- `SIBLING_WORK`：同体系但目前不能判定基础/高级/摘要角色；
- `UNKNOWN`：课程角色尚不能确定。

## 5. 善天道三册的闭环原则

QM-SRC-0027 / 0028 / 0029 的完整阅读显示：

- 三者不是同一作品的扫描或上下卷，因此保留三个不同 `work_id`；
- 0028 承担基础讲义角色；
- 0029 是高级课程扩展，包含大量分类占验与案例；
- 0027 是高度压缩的培训精华/速查式汇编，其取用与应用条目横跨基础与高级材料；
- 三者共享显著教学结构与术语路径，因此不得作为三个独立“书证票”。

这里的 derivative 是**课程层结构依赖**，不是未经证明的书目学“谁抄谁”。

## 6. 验证

`tools/validate_k2_course_lineage.py` 必须 fail-closed：

- canonical source 与 `work_id` 必须存在且匹配；
- 一个 source 不能进入多个 course family；
- 同 family 不得重复 work_id；
- resolved family 至少两部不同作品；
- resolved member 不得允许独立重复投票；
- `SYNOPSIS_COMPENDIUM` 必须具有课程派生关系和同 family 的相关源；
- related source 必须位于同 family；
- 项目仍必须 `claim_extraction_blocked=true`。

此层用于抑制 lineage vote inflation，不是制造新的“多来源共识”。
