package com.xuanxue.ai

import com.xuanxue.qimen.QimenEngine.QimenChart

/**
 * 奇门产品层的结构化投影。
 *
 * 这里不重新排盘，也不新增预测算法，只把已经存在的 chart / source / project / hypothesis
 * 信息分到不同 provenance 通道，避免 UI 把“系统算出的字段”“书里/规则里怎么说”“项目自己的
 * 推论”和“仍未验证的候选”混成一段看起来同等可信的文字。
 */
object QimenProductProjection {

    fun items(c: QimenChart, sourceIds: List<String>): List<ReadingItem> = buildList {
        add(
            ReadingItem(
                title = "当前计算字段",
                summary = "四柱【${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}】，节气【${c.jieQi}】，${c.juText}；时旬首【${c.xunShou}】，遁干【${c.dunGan}】，日空【${c.dayKong.joinToString("、")}】，时空【${c.hourKong.joinToString("、")}】，马星【${c.maXing}】。",
                evidenceGrade = EvidenceGrade.SOURCE_DERIVED,
                provenance = ProductProvenance.CHART_FACT,
                caveat = "这是当前引擎对本次输入生成的字段快照。盘面事实只描述系统输出，不自动承担现实吉凶、成败或应期结论。",
            ),
        )

        add(
            ReadingItem(
                title = "旬空与马星取法",
                summary = "当前项目把日空与时空作为两个不同字段保留；马星按占时支确定。局数与定元仍必须绑定所采用的方法，不能把单一实现写成唯一传统标准。",
                evidenceGrade = EvidenceGrade.SOURCE_DERIVED,
                provenance = ProductProvenance.SOURCE_RULE,
                sourceIds = sourceIds,
                caveat = "来源规则表示当前资料/审查支持这种取法或区分，不等于该规则已经获得独立现实效度。",
            ),
        )

        if (c.isWuBuYu) {
            add(
                ReadingItem(
                    title = "五不遇时规则命中",
                    summary = "当前时柱满足项目已工程化的五不遇时 generator 条件。",
                    evidenceGrade = EvidenceGrade.SOURCE_DERIVED,
                    provenance = ProductProvenance.SOURCE_RULE,
                    sourceIds = sourceIds,
                    caveat = "这里只记录规则命中；不会把一个传统标签直接翻译成具体现实事件。",
                ),
            )
        }

        add(
            ReadingItem(
                title = "情境推演入口",
                summary = "进一步判断必须先冻结具体事体与现实约束，再做取用/映射；盘面符号最早只能在现实模型之后进入。缺少具体事体时，本层不补造成败、吉凶或应期。",
                evidenceGrade = EvidenceGrade.EXPERIMENTAL,
                provenance = ProductProvenance.PROJECT_INFERENCE,
                caveat = "这是本项目的认知治理与推演方法，不冒充古籍原文，也不提供新的 empirical credit。",
            ),
        )

        if (c.patterns.isNotEmpty()) {
            add(
                ReadingItem(
                    title = "实验格局候选",
                    summary = c.patterns.joinToString("、"),
                    evidenceGrade = EvidenceGrade.EXPERIMENTAL,
                    provenance = ProductProvenance.UNVERIFIED_HYPOTHESIS,
                    sourceIds = sourceIds,
                    caveat = "这些候选依赖尚未由完整九宫黄金盘关闭的天/地/人/神盘实现，因此不进入确定性断语。",
                ),
            )
        }

        add(
            ReadingItem(
                title = "九宫实验边界",
                summary = "当前引擎可以生成值符【${c.zhiFu}】、值使【${c.zhiShi}】以及星门神九宫，但 handoff/qimen/05_FIXTURES.jsonl 的完整九宫黄金盘仍为 0，且地盘 walk / 人盘方向仍有未关闭冲突。",
                evidenceGrade = EvidenceGrade.EXPERIMENTAL,
                provenance = ProductProvenance.UNVERIFIED_HYPOTHESIS,
                sourceIds = sourceIds,
                caveat = "因此完整九宫只能作为开发与假设层展示，不能凭这些字段直接输出吉凶、成败或应期。",
            ),
        )
    }
}
