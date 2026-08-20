# 奇门前瞻案例镜像库 v3

> 定位：人类可读的案例索引/复盘镜像，不是独立计分数据库。
>
> 真正的机器可审计前瞻登记以 `knowledge/K2_PROSPECTIVE_CASE_REGISTRY.jsonl` 为准。

## 一、与旧 v2 的区别

旧版把“徒弟断局 → 师傅修正 → 最终结论 → 应验率”作为主流程，容易产生三个问题：

1. 反馈后修改被写成“修正”，但没有区分它是否已经污染原预测；
2. “完全应验/部分应验/未应验”没有统一、预注册评分口径；
3. 统计看板容易把不合格案例也混进所谓命中率。

v3 改为：

`Frozen Protocol -> Frozen Prediction -> Outcome Audit -> Model Delta`

不存在“师傅身份更高，所以修正自动更真”的权威链。

## 二、允许收录的案例类别

- `PROSPECTIVE_FROZEN_CASE`
- `CONTAMINATED_CASE`
- `IMPLEMENTATION_FAILURE_CASE`
- `PROJECT_RETROSPECTIVE_REANALYSIS`

文献案例主要保留在 `qimen-cases/SKILL.md` 的 SOURCE 研究路径中，不混入本库准确率统计。

## 三、案例索引格式

```markdown
# Case <case_id>

case_class:
registry_case_id:
question_domain:
method_layer:
method_family:
freeze_timestamp:
outcome_unknown_at_freeze:
eligible_for_scoring:
auxiliary_information_policy:

## Frozen protocol refs
question_fingerprint_sha256:
role_map_sha256:
eligible_features_sha256:
competing_branches_sha256:
timing_protocol_sha256:

## Frozen setup
setup_method:
setup_calibration:
seasonal_alignment:
time_boundary_system:
time_family:
layout_method:
deity_system:
star_state_system:
door_state_system:

## Frozen prediction
main_outcome_or_direction:
main_time_window:
observable_success_criteria:
observable_failure_criteria:

## Outcome audit
outcome_class: HIT / PARTIAL / MISS / UNRESOLVED / CONTAMINATED
actual_outcome_summary:
error_class:
contamination_flags:

## Post-feedback changes
setup_method_switch:
time_boundary_switch:
role_switch:
feature_switch:
method_switch:
timing_switch:
external_information_added:

## Model delta
KEEP / NARROW / REVISE / SPLIT / DEPRECATE / REJECT
notes:
```

详细私人内容留在 Git 外；本文件只保留必要研究元数据或摘要。

## 四、统计规则

统计只允许使用：

`eligible_for_scoring=true` 且满足同一 scoring contract 的 `PROSPECTIVE_FROZEN_CASE`。

必须同时报告：

- eligible 总数；
- HIT；
- PARTIAL；
- MISS；
- UNRESOLVED；
- CONTAMINATED；
- VOID/implementation failures；
- baseline 定义；
- 评分窗口与容许度。

不得把 contaminated / void / unscorable 条目删除来提高比例。

在没有足够合格样本前：

**不显示项目总体“应验率/准确率”。**

## 五、当前状态

- 合格 prospective rows：以 `K2_PROSPECTIVE_CASE_REGISTRY.jsonl` 实时状态为准；
- 本镜像库当前不人为制造示例 case；
- 空库是合法状态；
- 不因“需要统计看板”而补造案例。

## 六、复盘原则

结果出现后优先问：

1. 原 Frozen Prediction 到底说了什么；
2. success/failure criteria 是否预先明确；
3. 哪些变化发生在反馈之后；
4. 错误属于输入、排盘、方法、Role、feature、解释、应期还是基础概率；
5. 本次结果对规则是 KEEP、NARROW、REVISE、SPLIT、DEPRECATE 还是 REJECT。

不能先寻找“哪个象能解释结果”，再回头重写原预测。

---

*Cases Mirror v3 | 2026-08-21 | 与 Prospective Case Registry / Outcome Audit 对齐。*
