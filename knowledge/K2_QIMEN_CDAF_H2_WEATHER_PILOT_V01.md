# K2 CDAF-H2 香港显著降雨差分试验设计 v0.1

状态：`DESIGN_DRAFT / NOT_PREREGISTERED`  
Batch：`NONE`  
Freeze：`NONE`  
Outcome：`NONE`  
Empirical Credit：`NONE`  
Claim Extraction：`BLOCKED`

## 1. 研究问题

本设计只检验 CDAF-H2 在一个窄域中的增量：

`M2 - M1 = 冻结奇门符号映射相对非奇门现实基线的增量`

首个候选域固定为香港次日显著降雨。这里不测试完整天气奇门，不测试 M3 关系推演，不测试叙事解释，也不把一次批次结果推广为“奇门天气有效/无效”。

核心问题：

> 在同一个香港天文台公开天气基线之上，反馈前冻结的最小奇门正向降雨信号，能否稳定纠正一部分基线漏报，而不是增加更多误报？

## 2. 为什么选择香港与显著降雨

外部基线采用香港天文台 9-day Probability of Significant Rain（PSR）。官方定义“显著降雨”为一天内香港普遍地区累计雨量达到 10 mm 或以上，并以 Low / Medium Low / Medium / Medium High / High 五档发布；公开说明 9 日预报每日 11:30 和 16:30 发布。

官方参考：

- https://www.hko.gov.hk/en/wxinfo/currwx/fnd.htm
- https://www.hko.gov.hk/en/Whats-New/105939/The-Observatory-launches-9-day-probability-of-significant-rain-forecast
- https://www.hko.gov.hk/en/education/weather/rain/00568-Q-%26-A-for-Probability-of-Significant-Rain.html

这样 M1 不由项目自造“天气常识分数”，而是一个独立、公开、可追溯的专业气象 baseline。

## 3. 时间轴与问题冻结

候选执行时间统一使用香港时间 HKT（UTC+8）。

每个候选日 D：

1. 只读取 HKO 当日 16:30 发布的 PSR；
2. 目标日固定为 D+1 的 00:00–23:59 HKT；
3. 17:00 HKT 冻结研究问题与奇门盘；
4. 问题文本固定为：`目标日香港显著降雨研究代理是否达到 10.0 mm 或以上？`；
5. 17:00 后的新天气资料不得回写 M1/M2 Freeze。

若 16:30 PSR 在 17:00 前无法取得可靠快照，该日不进入样本；不得稍后补取最新版本冒充 16:30 版本。

## 4. M1：Context-Structured Baseline

M1 只使用 HKO 16:30 PSR 与已冻结的目标定义，不读取任何奇门盘信息。

为避免把概率区间强行伪造成精确概率，第一版只做预先固定的二分类：

- `High / Medium High -> RAIN10`；
- `Medium Low / Low -> NO_RAIN10`；
- `Medium (45–54%) -> INELIGIBLE`。

Medium 在打开奇门盘前即排除，因为该区间跨越 50%，项目不以任意 midpoint 把它制造成确定的二元 baseline。

## 5. M2 的唯一允许新增信息

### 5.1 来源基础

主要来源：QM-SRC-0021《奇门遁甲预测学（奇门遁甲现代应用技术）》。

正式 Atomic Evidence：

- `K2E-W1-QM-0021-0192` / pdf:p161-p162：占雨以天柱为雨师、天蓬为水神；天柱或天蓬乘壬癸游于一、三、六、七宫为核心降雨信号；
- `K2E-W1-QM-0021-0193` / pdf:p162：来源另有伤门、螣蛇、丁奇、反吟伏吟及特殊格局等修正；
- `K2E-W1-QM-0021-0199` / pdf:p163-p164：作者案例甚至允许“基础壬癸条件未满足时，由反吟/丙辛合化水改断有雨”，说明完整方法具有覆盖基础规则的例外自由度；
- `K2E-W1-QM-0021-0202` / pdf:p165：来源自己要求考虑地域差异。

页面复核同时显示，本书在天盘运转章节把九星与其所带三奇六仪一起移动。因此本试验把“星乘壬/癸”冻结解释为：

`该九星所在宫的 heaven-plate carried stem = 壬或癸`

不得在结果后改成“地盘壬癸也算”或“同宫任意位置出现壬癸都算”。

善天道《奇门遁甲精华》另有天气用神列表：天柱=雨师、壬癸/天蓬=主雨、天英/景门=主晴、天辅=风。它只作为文本回声和候选来源，不给 QM0021 增加经验票数，也不把其额外用神加入 v0.1。

### 5.2 CORE_RAIN_SIGNAL_V01

第一批只允许一个二值奇门信号：

```text
CORE_RAIN_SIGNAL_V01 =
  EXISTS star IN {天柱, 天蓬}
  SUCH THAT
    star.heaven_plate_carried_stem IN {壬, 癸}
    AND star.palace IN {坎1, 震3, 乾6, 兑7}
```

除此之外全部禁用。

明确禁用：

- 伤门放大雨势；
- 螣蛇、丁奇、天英、天辅；
- 值符远近快慢；
- 反吟/伏吟；
- 庚+丙、丙+辛合化水等例外；
- 虎猖狂、蛇夭矫、龙反首；
- 外应；
- 结果后地域修正；
- “故事更像下雨”的自由解释；
- 未校准的大小雨分数、百分比或权重。

禁用不表示这些规则已经被判错，只表示它们没有进入这个最小消融组件。

## 6. M2 如何在 M1 上产生增量

为了保持 `M2 = M1 + minimal symbolic information`，v0.1 不让奇门完全替代 HKO baseline，也不把“没有核心信号”强制解释成无雨。

冻结更新函数：

```text
IF M1 == NO_RAIN10 AND CORE_RAIN_SIGNAL_V01 == TRUE:
    M2 = RAIN10
ELSE:
    M2 = M1
```

因此 M2 只有一种越权能力：当专业 baseline 偏向无显著降雨，而来源支持的核心正向降雨信号出现时，尝试纠正一次潜在漏报。

这使增量含义非常具体：

- `M1 wrong / M2 right` = unique correction；
- `M1 right / M2 wrong` = unique degradation；
- 两者相同 = 不为奇门制造虚假增量。

第一版不允许奇门把 `RAIN10` 改成 `NO_RAIN10`，因为“壬主大雨、癸主小雨”没有被校准到 HKO 的 10 mm 阈值，而完整来源的无雨/例外体系自由度过高。

## 7. Outcome：公开观测研究代理

HKO PSR 的正式概念是“香港普遍地区”累计雨量。公开 Daily Total Rainfall 数据提供多个固定站点的日总雨量与 data-completeness 字段，但项目当前没有证据证明公开站点简单平均值就是 HKO 当前 PSR 内部正式 verification target。

因此 outcome 必须明确称为：

`HK_TERRITORY_RAIN10_RESEARCH_PROXY_V01`

而不是“官方 PSR 实际值”。

Batch preregistration 时一次性冻结：

1. DATA.GOV.HK 当时列出的全部 `Daily Total Rainfall Current Year` 站点资源及 resource ID；
2. 站点集合后续不得按结果增删；
3. 目标日每个冻结站点必须有数值且 `Data completeness = C`；
4. 任一冻结站点缺失、不可用或 completeness 非 C，则该 case = `UNEVALUABLE`；
5. 全部合格时取冻结站点日雨量的简单算术平均；
6. 平均值 `>= 10.0 mm -> RAIN10`，否则 `NO_RAIN10`。

官方数据入口与字典：

- https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-total-rainfall
- https://data.weather.gov.hk/weatherAPI/doc/data_dictionary_daily_total_rainfall.pdf

这个代理不是面积加权，也不是对 HKO 内部验证站网的冒充；它的价值是公开、固定、可重算、无法按结果挑站。

## 8. 入样与排除规则

候选日只有在打开 M2 前满足以下全部条件才可入样：

- HKO 16:30 D+1 PSR 快照可追溯；
- PSR 不为 Medium；
- 目标日期与问题文本可唯一冻结；
- 指定 Qimen engine/model commit 可重建 17:00 HKT 盘；
- weather protocol version 已冻结；
- outcome station panel 已在 Batch 层冻结。

排除不得参考：

- 奇门盘是否“好看”；
- CORE_RAIN_SIGNAL 是否出现；
- 后来是否下雨；
- M1/M2 谁对谁错。

结果后发现 outcome 数据不完整，只能标 `UNEVALUABLE`，不得改成事前“不入样”。

## 9. 仍未关闭的 Batch blocker

本文件现在仍不是 Batch preregistration，因为还有一项不能假装已经解决：

`SERIAL_DEPENDENCE / SAMPLE_ADEQUACY`

连续天气日明显相关。如果直接把每天当独立 Bernoulli 样本并用普通二项/麦克尼马检验，会夸大有效样本量。

Batch 创建前必须再冻结：

- 日历采样 cadence 或明确的 block-analysis unit；
- planned duration / case-count 或非结果驱动 stopping rule；
- primary paired statistic；
- 如何处理 serial dependence；
- 最小 discordant-pair / information threshold；
- Batch Review 的成功/失败/信息不足判据。

这些没有关闭之前：

`BATCH_READY = false`

不得为了制造进度随手写“20例”“30例”“三次命中”。

## 10. 失败与解释边界

若未来该 weather batch 显示 unique degradation >= unique correction，或在冻结统计规则下没有可区分增量，则只能得到：

`CORE_RAIN_SIGNAL_V01 在该香港次日显著降雨设计中未获得增量信用。`

不能直接得到：

- 所有奇门天气规则无效；
- 所有奇门无效；
- H2 在所有问题域无效。

反之即使 M2 获得正增量，也只能进入复制/Batch Review；不能由单批升级为普遍经验真理。

## 11. 当前状态

- source-grounded weather rule：`CLOSED FOR V0.1`；
- M1 baseline definition：`CLOSED FOR V0.1`；
- M2 update function：`CLOSED FOR V0.1`；
- public outcome proxy definition：`CLOSED FOR V0.1`；
- modifiers/exceptions：`DISABLED`；
- serial-dependence/sample-adequacy design：`OPEN`；
- Batch：`NOT CREATED`；
- Empirical Credit：`NONE`。
