package com.xuanxue.ai

import com.xuanxue.bazi.BaziEngine
import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.ziwei.core.ZiweiAstro
import kotlin.test.Test
import kotlin.test.assertTrue

class InterpretersTest {

    @Test
    fun baziReading() {
        val c = BaziEngine.bySolar(1990, 5, 20, 12, 30, "男")
        val r = XuanxueAI.bazi(c)
        println("AI1 八字:\n" + r.text)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("日主"))
        assertTrue(r.text.contains("五行分布"))
        assertTrue(r.items.any { it.ruleId == "R-BZ-LIANG-VOTE" })
    }

    @Test
    fun ziweiReading() {
        val a = ZiweiAstro.bySolar("1990-05-20", 6, "male")
        val r = XuanxueAI.ziwei(a)
        println("AI2 紫微:\n" + r.text)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.items.any { it.ruleId == "R-ZW-MING" })
        assertTrue(r.text.contains("命宫") || r.text.contains("主星"))
        assertTrue(!r.text.contains("帝星，主贵气"))
        assertTrue(!r.text.contains("得财之机"))
    }

    @Test
    fun qimenReading() {
        val c = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        val r = XuanxueAI.qimen(c)
        println("AI3 奇门:\n" + r.text)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("值符"))
        assertTrue(r.items.any { it.ruleId.startsWith("R-") })
        assertTrue(r.overall.contains("门派冲突只并列") || r.text.contains("门派冲突只并列"))
    }

    @Test
    fun liuyaoReading() {
        val c = LiuYaoEngine.byNumbers(1, 1, 3, 2026, 8, 15, 10)
        val r = XuanxueAI.liuyao(c)
        println("AI4 六爻:\n" + r.text)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("世爻"))
        assertTrue(r.items.any { it.ruleId == "R-LY-SHIYING" })
        assertTrue(!r.text.contains("主文书、长辈"))
        assertTrue(!r.text.contains("宜静守待时"))
        assertTrue(!r.text.contains("观变卦六亲以断吉凶趋向"))
    }

    @Test
    fun liurenReading() {
        val c = LiuRenEngine.bySolar(1949, 10, 1, 0, 0)
        val r = XuanxueAI.liuren(c)
        println("AI5 六壬:\n" + r.text)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.text.contains("元首课") || r.text.contains("取法") || r.text.contains("课型"))
        assertTrue(r.items.any { it.ruleId == "R-LR-FA" })
        assertTrue(!r.text.contains("宜顺势而为"))
        assertTrue(!r.text.contains("待填实之日应事"))
    }

    @Test
    fun huangliReading() {
        val l = com.nlf.calendar.Solar.fromYmd(2026, 8, 15).lunar
        val r = XuanxueAI.huangli(l)
        println("AI6 黄历:\n" + r.text)
        assertTrue(r.items.isNotEmpty())
        assertTrue(r.items.any { it.ruleId == "R-HL-YIJI" })
        assertTrue(r.overall.contains("不是命理应期") || r.text.contains("不是命理应期"))
    }

    @Test
    fun toolsRegistered() {
        assertTrue(XuanxueAI.tools.size == 6)
        assertTrue(XuanxueAI.tools.all { it["name"] != null && it["description"] != null })
        println("AI7 工具注册表: " + XuanxueAI.tools.joinToString(", ") { it["name"] as String })
    }
}
