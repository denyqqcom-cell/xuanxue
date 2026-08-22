# 善天道三册 K2B Per-Book Source Review Acceptance

版本：2026-08-23  
阶段：K2B / Deep Closure  
Decision：PASS  
Acceptance scope：SOURCE REVIEW ONLY  
Claim Extraction：BLOCKED  
Empirical credit：NONE

## 1. 接受对象

本轮在已经完成 course provenance closure 的基础上，正式关闭三本作品自己的 per-book deep review：

- QM-SRC-0027 / WORK-000228 / 《善天道-奇门遁甲精华》；
- QM-SRC-0028 / WORK-000018 / 《善天道-奇门遁甲讲义71页》；
- QM-SRC-0029 / WORK-000019 / 《善天道-奇门遁甲高级研修班讲义294页》。

三者保持三个不同 work_id；同时继续受 `COURSE-QM-SHANTIADAO-001` single-vote 约束。

## 2. Per-book 结论

### QM-SRC-0027 — SYNOPSIS_COMPENDIUM

接受结论：

- 32/32 页完整视觉阅读；
- source role 为课程精华/速查式汇编；
- 前部压缩基础排盘与符号属性，后部把大量问题域整理成用神/参数清单；
- 其内容适合成为 `ROLE_CANDIDATE_LIBRARY`，不应成为“全库规则随时可调”的开放字典；
- p4 的“拆补法（推荐方法）”不能覆盖完整版讲义中仍存在的拆补/置闰分歧；
- 大选、战争、案件、诉讼、商贸、贷款、疾病等高风险清单只保留来源研究价值。

### QM-SRC-0028 — FOUNDATION

接受结论：

- 71/71 页完整视觉阅读；
- 原 Wave1 50 条 Atomic Evidence 保留；
- 50/50 re-audit 已关闭，其中 11 条 HOLD_CONFLICT、4 条高风险 DOWNGRADE_NOT_CLAIM；
- 原 distillate `K2D-W1-QM-SRC-0028` 不删除，本轮 deep-source distillate 明确承接它；
- 基础讲义最可保留的是排盘/结构与条件化组合方法，不是单一吉凶标签；
- 拆补/置闰、九星旺衰、八神转法与内部文本疑点继续保持 unresolved。

### QM-SRC-0029 — ADVANCED_EXTENSION

接受结论：

- 294/294 页完整视觉阅读；
- 该书把断局组织成较明确的流程：先选主要参数，再做基本盘面标注，然后区分宫内细节与宫际关系，最后进入问题域与应期；
- 作者开篇明确承认模型不可能100%断准，应期也被称为困难且有分歧；
- 年命/日干的主要当事人选择存在两种意见，作者只是个人偏向年命；
- 大量案例可证明作者如何使用规则，但不能提供前瞻 empirical credit；
- “马星冲墓/空”、旺衰削弱空亡等修正暴露出较大的解释自由度，因此必须进入预注册 correction rule，而不是继续作为自由补丁。

## 3. 三本合起来真正让项目改变了什么

本轮不是把三本书合成一套‘更完整的教科书’，而是拆出了三种不同知识功能：

1. **0027：候选角色库** — 告诉项目“可能有哪些角色”；
2. **0028：基础结构与冲突层** — 告诉项目“结构怎样搭、哪些地方不能机械统一”；
3. **0029：推演流程与修正自由度** — 告诉项目“实际断局怎样走、哪里最容易事后拟合”。

由此形成新的候选架构：

`Provenance Gate -> Question Topology -> Role Candidate Library -> Eligible Rule Set Freeze -> Base Plate Annotation -> Relational Inference -> Correction Rule Registry -> Timing/Uncertainty -> Prospective Validation`

正式记录为：

`K2_QIMEN_CONTROLLED_INFERENCE_MODEL.md` / QCIC v0.1。

## 4. 为什么这不等于“学会善天道就能直接解盘”

三本完整阅读后的最大反结论恰恰是：

- 条目越多，不代表解释越可靠；
- 修正规则越多，不代表模型越强；
- 案例越多，不代表前瞻准确率越高；
- 同课书越多，不代表独立来源越多。

如果没有冻结角色、规则和修正优先级，资料越丰富反而越容易在结果之后找到一个能解释成功的路径。

因此本轮 per-book acceptance 只是学习闭环，不是理论真实性背书。

## 5. Acceptance Gate

本轮满足：

- canonical SHA 与 source registry 一致；
- deep reading = COMPLETE / VISUAL_PAGE / p1-pN；
- 三本均有 deep-source distillate；
- 0028 prior distillate 与 Evidence re-audit 被显式接入；
- course provenance single-vote 继续生效；
- work-family sources 被排除在 deep-source lane 外，避免重复信用；
- source anchors 仅允许引用本书合法页码；
- testable hypotheses 全部保持 UNTESTED；
- empirical_credit = NONE；
- claim_extraction_blocked = true。

因此本轮可以正式记为：

**QM0027_PER_BOOK_SOURCE_REVIEW_ACCEPTED**  
**QM0028_PER_BOOK_DEEP_REVIEW_ACCEPTED**  
**QM0029_PER_BOOK_SOURCE_REVIEW_ACCEPTED**  
**SHANTIADAO_THREE_BOOK_PER_BOOK_CLOSURE_COMPLETE**

但仍不能记为：

`SHANTIADAO_RULES_VALIDATED`  
`CLAIM_EXTRACTION_OPEN`  
`HIGH_RISK_OPERATIONAL_USE_ALLOWED`
