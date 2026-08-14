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
 * 每个结果同时带当前仓库的核验摘要与来源 ID，避免 UI 只显示“结论”却看不到
 * 这条信息到底来自夹具、上游数据、传统启发式还是实验实现。
 */
object XuanxueAI {

    /** Provider-neutral 工具描述；真正 BYOK 联网仍未启用。 */
    val tools: List<Map<String, Any>> = listOf(
        mapOf("name" to "bazi_interpret", "description" to "八字结构整理：四柱、五行显示权重、十神、大运时间线"),
        mapOf("name" to "ziwei_interpret", "description" to "紫微盘结构整理：命宫主星、四化、五行局"),
        mapOf("name" to "qimen_interpret", "description" to "奇门基础事实整理：历法、局、旬首旬空；九宫实验能力不作定论"),
        mapOf("name" to "liuyao_interpret", "description" to "六爻结构整理：世应、动爻、六亲、变卦"),
        mapOf("name" to "liuren_interpret", "description" to "大六壬结构整理：课型、三传、天将、旬空"),
        mapOf("name" to "huangli_interpret", "description" to "黄历字段整理：宜忌、吉神凶煞、冲煞"),
    )

    private fun buildReading(
        id: String,
        rawItems: List<String>,
        itemTitle: String,
        grade: EvidenceGrade,
        extraCaveats: List<String> = emptyList(),
    ): Reading {
        val audit = MethodAuditRegistry.byId(id)
        val sourceIds = audit?.sourceIds.orEmpty()
        val caveats = buildList {
            addAll(audit?.limitations.orEmpty())
            addAll(extraCaveats)
        }.distinct()
        return Reading(
            toolName = id,
            overall = audit?.summary.orEmpty(),
            caveats = caveats,
            items = rawItems.map { text ->
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

    fun qimen(c: QimenEngine.QimenChart): Reading = buildReading(
        id = "qimen",
        rawItems = QimenInterpreter.interpret(c),
        itemTitle = "奇门",
        grade = EvidenceGrade.SOURCE_DERIVED,
        extraCaveats = listOf("完整九宫、值符值使、星门神盘仍按实验实现管理；离线解释层不会据此直接断成败或应期。"),
    )

    fun liuyao(c: LiuYaoEngine.LiuYaoChart): Reading = buildReading(
        id = "liuyao",
        rawItems = LiuYaoInterpreter.interpret(c),
        itemTitle = "六爻",
        grade = EvidenceGrade.TRADITIONAL_HEURISTIC,
        extraCaveats = listOf("未提供具体事体时，只展示结构，不自动替用户选用神。"),
    )

    fun liuren(c: LiuRenEngine.LiuRenChart): Reading = buildReading(
        id = "liuren",
        rawItems = LiuRenInterpreter.interpret(c),
        itemTitle = "六壬",
        grade = EvidenceGrade.TRADITIONAL_HEURISTIC,
        extraCaveats = listOf("课例回归证明部分算法路径可复现，不等于全部课式已完成多来源核验。"),
    )

    fun huangli(l: Lunar): Reading = buildReading(
        id = "huangli",
        rawItems = HuangLiInterpreter.interpret(l),
        itemTitle = "黄历",
        grade = EvidenceGrade.SOURCE_DERIVED,
    )
}
