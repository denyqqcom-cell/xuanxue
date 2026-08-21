---
name: qimen-qiju
description: >
  奇门起局 Setup Method Registry。用于识别阴阳遁、局数、符头/节气处理、时间边界、
  转盘/飞宫等起局算法与来源差异，并在反馈前冻结具体 setup protocol。
---

# 起局排盘：Setup Method Registry v2.2

> **上位约束**：`奇门/CURRENT_METHOD_CONSTRAINTS.md`、`knowledge/K2_PROSPECTIVE_CASE_PROTOCOL.md`、`qimen-overview/SKILL.md`。
>
> **核心原则**：盘错会使后续解释失去可比性；但“某一种起局法是唯一正宗/最准”也不能由书名或习惯直接决定。

## 一、起局不是一个参数，而是一组算法选择

至少分开：

```text
setup_method
setup_calibration
seasonal_alignment
time_boundary_system
time_family
layout_method
deity_system
bureau_table_source
implementation_version
```

这些字段共同决定结构输入。反馈后切换其中任何关键字段，不能修补原模型成绩。

## 二、当前 Setup Method Registry

详细迁移审计见 `SETUP_METHOD_REGISTRY.md`。

| setup_method | legacy description | current status |
|---|---|---|
| `FUTOU_ZHIRUN` | 依符头、正授/超神/接气/置闰处理 | SOURCE_REVIEW_REQUIRED |
| `CHAIBU_SOLAR_TERM` | 以节气交接为主并拆补三元 | SOURCE_REVIEW_REQUIRED |
| `MAOSHAN_SOLAR_TERM` | 旧技能称“完全按实际节气起局” | DEFINITION_OVERLAP_UNRESOLVED |
| `SOURCE_DEFINED_OTHER` | 其他来源专用算法 | CONTEXT_REQUIRED |

当前没有“默认推荐使用”的 setup method。

## 三、阴阳遁与局数：结构先行，来源算法分开

传统资料常以冬至后至夏至前为阳遁、夏至后至冬至前为阴遁，并按所用方法决定三元/局数。该结构可作为 source-defined baseline，但具体换局时刻、三元划分、符头处理仍由 `setup_method + setup_calibration + seasonal_alignment` 决定。

不得只写“今天是某节气，所以必定某局”，除非所用 setup protocol 已冻结并可复算。

## 四、超神 / 接气：legacy 内部定义互相反转

旧技能前段写：

- 超神 = 节气先到、旬首未到；
- 接气 = 旬首先到、节气未到。

同一文件后段又写：

- 超神 = 上元符头在节气前面；
- 接气 = 节气在前、符头在后。

两组定义方向相反。

当前状态：

`SOURCE_INCONSISTENCY / TERMINOLOGY_DIRECTION_CONFLICT`

处理：

- 不静默选一组；
- 不凭记忆改成“通常定义”；
- 后续必须回到各来源原页逐条核验；
- 在核验前，正式模型若依赖超神/接气方向，必须绑定明确 source-specific setup identifier，否则 `CONTEXT_REQUIRED`。

## 五、拆补法：旧技能存在两套不完全相同的描述

前段把拆补法简化为：

`节气第1-5天上元 / 6-10天中元 / 11-15天下元`

后段又描述为：

`残上→中→下→补上` 或 `残下→上→中→补下`

后者显式保留符头与交节不重合导致的“拆/补”残段，不能简单等同于固定 5+5+5 自然日切块。

当前状态：

`SOURCE_INCONSISTENCY / ALGORITHM_VARIANT_REQUIRED`

旧技能中的 2026-06 示例只能算 legacy example，不能作为已验证 fixture，除非时间引擎、交节时刻、日界规则和 source algorithm 全部复核。

## 六、拆补 vs 茅山：旧定义重叠，暂不强行区分

旧文件一处说拆补“直接取用节气，按节气内天数分段”，又说茅山“完全按实际节气，不参考符头，节气到即换”。两者在当前表述下高度重叠，缺少足够算法差异。

当前状态：

`DEFINITION_OVERLAP_UNRESOLVED`

因此不能仅凭名称创建两套“已知不同”的预测模型；先做来源级算法拆解。

## 七、时间边界：必须成为一等变量

旧技能出现明显冲突：

- 一处写“20点~23点为晚子时”；
- 另一处写“23-24点为晚子时算次日”。

这会直接影响日干支、时干支乃至整个盘。

当前新增：

```text
time_boundary_system
```

正式模型必须事前声明采用的日界/子时规则及实现来源。例如：

- `CIVIL_MIDNIGHT`
- `ZI_START_23`
- `SOURCE_DEFINED_OTHER`
- `NOT_APPLICABLE`

上述枚举只是项目上下文标签，不声明哪一个玄学上正确。

如果不同日界会生成不同盘，应建立独立 A/B model，而不是结果后切换。

## 八、宫序与“顺时针”不能混写

旧技能多处把：

`一坎、二坤、三震、四巽、五中、六乾、七兑、八艮、九离`

描述成“顺时针依次排列”，阴遁又描述成“逆时针依次排列”。这是高风险实现表述：洛书九宫编号与物理顺/逆时针不是同一个概念，且固定宫位不会因阴阳遁而整体重新排成另一套方位。

当前硬规则：

- 区分 `PALACE_NUMBER_ORDER`、`GEOMETRIC_ROTATION_ORDER`、`SOURCE_DEFINED_SEQUENCE`；
- 不再用“顺时针/逆时针”替代宫序算法；
- 六仪三奇、八门、八神的顺逆必须明确究竟是按宫号、洛书路线、几何旋转还是来源特定序列。

若实现文档只有“顺/逆”而没有 sequence definition，标 `IMPLEMENTATION_AMBIGUITY`。

## 九、值符 / 值使 / 八门运转：来源语义需要拆层

旧技能同时写：

- 值使门随时支，按阳顺阴逆随时辰地支运转；
- 八门永远顺时针转排，不论阴阳遁。

这两句可能分别描述“值使落宫计算”和“八门门序布置”，也可能存在冲突；旧文件没有把对象层分清。

当前状态：

`SEMANTIC_LAYER_AMBIGUITY`

后续实现必须分别定义：

```text
chief_door_position_rule
door_sequence_rule
rotation_direction_rule
```

不把一句口诀扩成未定义的统一算法。

## 十、六甲旬首与遁仪：保留结构索引，不扩张效验

常见结构索引：

| 旬首 | 遁仪 | 旬空 |
|---|---|---|
| 甲子 | 戊 | 戌亥 |
| 甲戌 | 己 | 申酉 |
| 甲申 | 庚 | 午未 |
| 甲午 | 辛 | 辰巳 |
| 甲辰 | 壬 | 寅卯 |
| 甲寅 | 癸 | 子丑 |

这是起局结构资料，不证明后续预测有效。

## 十一、“几局”的结构定义与 lookup fixture

旧资料把“甲子戊落几宫即几局”作为局号解释。当前可以作为特定传统 setup 的 source-defined structural rule，但必须绑定 layout/setup source。

梁书 p32-p49 十八局表已建立 `LIANG_18_BUREAU` fixture index；即使未来做到 `IMPLEMENTATION_CHECKED`，也只说明来源复刻成功。

## 十二、setup_calibration 与 seasonal_alignment 不得混成 setup_method

当前项目区分：

```text
setup_method             # 具体起局算法族/版本
setup_calibration        # PINGQI / DINGQI / ...
seasonal_alignment       # ZHENGSHOU / CHAOSHEN / ZHIRUN / JIEQI / ...
time_boundary_system     # 日界/子时规则
```

它们可能相互关联，但不能为了减少字段而事后互相替代。

## 十三、来源 provenance

旧文件多次写 `《奇门遁甲应用学》佚名`。K2 已页内核验对应工作作者为**王云鹏**，所以当前运行层使用王云鹏归属；这只是 provenance correction，不代表其中起局规则已被经验验证。

旧文件还引用：

- 善天道讲义；
- 幺学声/《奇门遁甲预测学》；
- 《图解奇门遁甲大全》；
- 搜狗问问、知乎等网页。

未完成当前 page-level K2 verification 的具体条目统一视为：

`LEGACY_SOURCE_NOTE` 或 `LEGACY_WEB_NOTE`。

网页说明不能代替原书算法核验。

## 十四、正式起局输出模板

```markdown
# Setup Protocol
- setup_method:
- setup_method_version/source:
- setup_calibration:
- seasonal_alignment:
- time_boundary_system:
- time_family:
- layout_method:
- yin_yang_dun:
- ju_number:
- bureau_table_source:
- deity_system:
- star_state_system:
- door_state_system:
- solar_term_timestamp_source:
- input_timezone:
- implementation_version:
- self_check:
- unresolved_conflicts:
```

正式前瞻模型中的关键字段与 hashes 同步到 Prospective Registry / local frozen packet。

## 十五、反馈后禁止事项

结果出来以后不得：

- 从拆补切到置闰/茅山；
- 从一个超神/接气定义切到另一套；
- 改节气交接算法；
- 改日界/子时规则；
- 改宫序/旋转序列；
- 因为另一盘更像结果而追认它为“真盘”。

这些变化只能创建新模型版本，原预测照原协议评分。

## 十六、当前研究任务

优先级：

1. 对各来源逐页核验超神/接气定义；
2. 拆解拆补、置闰、茅山为可执行伪代码；
3. 定义时间边界与节气时刻输入协议；
4. 对同一 timestamp 并行生成不同 setup model；
5. 比较 setup divergence rate 与 prediction divergence rate；
6. 加 wrong-setup / boundary timestamp negative controls。

这一步首先验证**执行可重复性与方法分叉**，不是先证明哪一法最准。

---

*QClaw qimen-qiju v2.2 | Setup Method Registry migration | 2026-08-21*
