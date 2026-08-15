package com.xuanxue.ai

import com.nlf.calendar.Lunar
import com.xuanxue.bazi.BaziEngine
import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.ziwei.core.ZiweiAstro

/**
 * 解读引擎统一入口 — 每个解读器即一个"工具"（将来 BYOK 云端 AI 可注册为 function-calling 工具）。
 */
object XuanxueAI {

    /** 工具注册表（JSON schema 化的接口描述，BYOK 模式复用） */
    val tools: List<Map<String, Any>> = listOf(
        mapOf("name" to "bazi_interpret", "description" to "八字四柱解读：五行、梁氏投票身强弱、十神只列名（离线，带来源）"),
        mapOf("name" to "ziwei_interpret", "description" to "紫微斗数盘解读：命宫主星、四化落点（离线，带来源）"),
        mapOf("name" to "qimen_interpret", "description" to "奇门遁甲盘解读：局法分叉、旬、五不遇时、击刑表、空亡并列（离线，带来源）"),
        mapOf("name" to "liuyao_interpret", "description" to "六爻卦解读：世应、动爻、六亲名目（离线，带来源）"),
        mapOf("name" to "liuren_interpret", "description" to "大六壬课解读：四课、取法、三传、天将（离线，带来源）"),
        mapOf("name" to "huangli_interpret", "description" to "黄历解读：宜忌、神煞、通书来源（离线，带来源）"),
    )

    fun bazi(c: BaziEngine.BaziChart): Reading = BaziInterpreter.reading(c)

    fun ziwei(a: ZiweiAstro.Astrolabe): Reading = ZiweiInterpreter.reading(a)

    fun qimen(c: QimenEngine.QimenChart): Reading = QimenInterpreter.reading(c)

    fun liuyao(c: LiuYaoEngine.LiuYaoChart): Reading = LiuYaoInterpreter.reading(c)

    fun liuren(c: LiuRenEngine.LiuRenChart): Reading = LiuRenInterpreter.reading(c)

    fun huangli(l: Lunar): Reading = HuangLiInterpreter.reading(l)
}
