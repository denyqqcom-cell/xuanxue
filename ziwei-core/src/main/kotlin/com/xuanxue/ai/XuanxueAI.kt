package com.xuanxue.ai

import com.nlf.calendar.Lunar
import com.xuanxue.bazi.BaziEngine
import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.ziwei.core.ZiweiAstro

/**
 * 统一离线解释入口。
 *
 * 每个结果同时带当前仓库的核验摘要与来源 ID。事占类模块另外接收 ReadingContext，
 * 强制把“盘面结构”和“用户现实问题”分开；没有具体事体时不自动选用神/类神，也不
 * 输出成败、吉凶或应期。
 */
object XuanxueAI {

    /** Provider-neutral 工具描述；真正 BYOK 联网仍未启用。 */
    val tools: List<Map<String, Any>> = listOf(
        mapOf("name" to "bazi_interpret", "description" to "八字结构整理：四柱、五行显示权重、十神、大运时间线"),
        mapOf("name" to "ziwei_interpret", "description" to "紫微盘结构整理：命宫主星、四化、五行局"),
        mapOf("name" to "qimen_interpret", "description" to "奇门基础事实整理：历法、局、旬首旬空；需具体事体后才进入取用层"),
        mapOf("name" to "liuyao_interpret", "description" to "六爻结构整理：世应、动爻、六亲、变卦；具体取用依赖事体"),
        mapOf("name" to "liuren_interpret", "description" to "大六壬结构整理：课型、三传、天将、旬空；类神取用依赖事体"),
        mapOf("name" to "huangli_interpret", "description" to "黄历字段整理：宜忌、吉神凶煞、冲煞"),
    )

    private fun buildReading(
        id: String,
        rawItems: List<String>,
        itemTitle: String,
        grade: EvidenceGrade,
        context: ReadingContext? = null,
        requireSpecificContext: Boolean = false,
        extraCaveats: List<String> = emptyList(),
    ): Reading {
        val audit = MethodAuditRegistry.byId(id)
        val sourceIds = audit?.sourceIds.orEmpty()
        val caveats = buildList {
            addAll(audit?.limitations.orEmpty())
            addAll(extraCaveats)
            if (requireSpecificContext) {
                when {
                    context == null || (context.normalizedQuestion.isEmpty() && context.normalizedKnownFacts.isEmpty()) ->
                        add("尚未提供具体事体；当前只展示排盘/卦课结构，不进入取用、成败与应期判断。")
                    !context.isSpecific ->
                        add("事体描述仍过短；请补充明确问题与已知现实条件后，再进入情境推演。")
                }
            }
        }.distinct()

        val contextItems = buildList {
            if (context != null && (
                    context.domain != QueryDomain.GENERAL ||
                        context.normalizedQuestion.isNotEmpty() ||
                        context.normalizedKnownFacts.isNotEmpty()
                    )
            ) {
                add(
                    ReadingItem(
                        title = "事体上下文",
                        summary = context.summary(),
                        evidenceGrade = EvidenceGrade.USER_CONTEXT,
                        caveat = "这是用户提供的现实条件，只用于限定分析场景，不会提高排盘算法或传统规则的证据等级。",
                    ),
                )
            }
        }

        return Reading(
            toolName = id,
            overall = audit?.summary.orEmpty(),
            caveats = caveats,
            items = contextItems + rawItems.map { text ->
                ReadingItem(
                    title = itemTitle,
                    summary = text,
                    evidenceGrade = grade,
                    sourceIds = sourceIds,
                )
            },
        )
    }

    fun bazi(c: BaziEngine.BaziChart): Reading = buildReading(
        id = "bazi",
        rawItems = BaziInterpreter.interpret(c),
        itemTitle = "八字",
        grade = EvidenceGrade.TRADITIONAL_HEURISTIC,
        extraCaveats = listOf("当前版本不输出基于单一十二运的身强弱结论。"),
    )

    fun ziwei(a: ZiweiAstro.Astrolabe): Reading = buildReading(
        id = "ziwei",
        rawItems = ZiweiInterpreter.interpret(a),
        itemTitle = "紫微",
        grade = EvidenceGrade.VERIFIED_FIXTURE,
        extraCaveats = listOf("夹具证明的是 Kotlin 与 iztro 的实现一致性，不是对星曜解释作独立真值验证。"),
    )

    fun qimen(c: QimenEngine.QimenChart, context: ReadingContext = ReadingContext()): Reading {
        val audit = MethodAuditRegistry.qimen
        val hasRealityContext = context.domain != QueryDomain.GENERAL ||
            context.normalizedQuestion.isNotEmpty() ||
            context.normalizedKnownFacts.isNotEmpty()
        val caveats = buildList {
            addAll(audit.limitations)
            add("完整九宫、值符值使、星门神盘仍按实验实现管理；离线解释层不会据此直接断成败或应期。")
            when {
                !hasRealityContext ->
                    add("尚未提供具体事体；当前只展示排盘/规则/项目边界，不进入取用、成败与应期判断。")
                !context.isSpecific ->
                    add("事体描述仍过短；请补充明确问题与已知现实条件后，再进入情境推演。")
            }
        }.distinct()

        return Reading(
            toolName = "qimen",
            overall = audit.summary,
            caveats = caveats,
            contextSummary = if (hasRealityContext) context.summary() else "",
            contextCaveat = if (hasRealityContext) {
                "这是用户提供的现实条件，属于 M0/M1 reality input，不属于盘面事实、来源规则、项目推论或未经验证假设，也不会提高任何术数规则的证据等级。"
            } else {
                ""
            },
            items = QimenProductProjection.items(c, audit.sourceIds),
        )
    }

    fun liuyao(c: LiuYaoEngine.LiuYaoChart, context: ReadingContext = ReadingContext()): Reading = buildReading(
        id = "liuyao",
        rawItems = LiuYaoInterpreter.interpret(c),
        itemTitle = "六爻",
        grade = EvidenceGrade.TRADITIONAL_HEURISTIC,
        context = context,
        requireSpecificContext = true,
        extraCaveats = listOf("仓库尚未建立六爻多来源取用规则 handoff；当前不会根据问题类别机械映射唯一用神。"),
    )

    fun liuren(c: LiuRenEngine.LiuRenChart, context: ReadingContext = ReadingContext()): Reading = buildReading(
        id = "liuren",
        rawItems = LiuRenInterpreter.interpret(c),
        itemTitle = "六壬",
        grade = EvidenceGrade.TRADITIONAL_HEURISTIC,
        context = context,
        requireSpecificContext = true,
        extraCaveats = listOf("课例回归证明部分算法路径可复现；类神、应事与应期仍需具体事体和多来源规则核验。"),
    )

    fun huangli(l: Lunar): Reading = buildReading(
        id = "huangli",
        rawItems = HuangLiInterpreter.interpret(l),
        itemTitle = "黄历",
        grade = EvidenceGrade.SOURCE_DERIVED,
    )
}
