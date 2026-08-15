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
        mapOf("name" to "bazi_interpret", "description" to "八字四柱解读：五行、日主强弱、十神格局、大运"),
        mapOf("name" to "ziwei_interpret", "description" to "紫微斗数盘解读：命宫主星、四化"),
        mapOf("name" to "qimen_interpret", "description" to "奇门遁甲盘解读：局法分叉、旬、五不遇时、击刑表、空亡并列（离线，带来源）"),
        mapOf("name" to "liuyao_interpret", "description" to "六爻卦解读：世应、动爻、六亲用神"),
        mapOf("name" to "liuren_interpret", "description" to "大六壬课解读：课型、三传、天将"),
        mapOf("name" to "huangli_interpret", "description" to "黄历解读：宜忌、吉神、冲煞"),
    )

    fun bazi(c: BaziEngine.BaziChart): Reading =
        Reading("bazi", BaziInterpreter.interpret(c).map { ReadingItem("八字", it) })

    fun ziwei(a: ZiweiAstro.Astrolabe): Reading =
        Reading("ziwei", ZiweiInterpreter.interpret(a).map { ReadingItem("紫微", it) })

    fun qimen(c: QimenEngine.QimenChart): Reading = QimenInterpreter.reading(c)

    fun liuyao(c: LiuYaoEngine.LiuYaoChart): Reading =
        Reading("liuyao", LiuYaoInterpreter.interpret(c).map { ReadingItem("六爻", it) })

    fun liuren(c: LiuRenEngine.LiuRenChart): Reading =
        Reading("liuren", LiuRenInterpreter.interpret(c).map { ReadingItem("六壬", it) })

    fun huangli(l: Lunar): Reading =
        Reading("huangli", HuangLiInterpreter.interpret(l).map { ReadingItem("黄历", it) })
}
