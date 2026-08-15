package com.xuanxue.ai

import com.xuanxue.bazi.BaziEngine
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class BaziRulesTest {

    @Test
    fun liangVoteNote04Example() {
        // 笔记04：己未 丙寅 甲子 庚午，甲日主，2正5负
        val v = BaziRules.liangVote(
            dayGan = "甲",
            yearGan = "己", yearZhi = "未",
            monthGan = "丙", monthZhi = "寅",
            dayZhi = "子",
            timeGan = "庚", timeZhi = "午",
            hideGan = listOf("己", "丁", "乙", "丙", "戊", "甲", "癸", "庚", "己", "丁"),
            otherStems = listOf("己", "丙", "庚"),
        )
        assertEquals(2, v.plus)
        assertEquals(5, v.minus)
        assertEquals("偏弱", v.strength)
        assertTrue(v.deLing) // 寅月，甲木得令
    }

    @Test
    fun yiYou1990IsWeakByVote() {
        val c = BaziEngine.bySolar(1990, 5, 20, 12, 30, "男")
        assertEquals("乙", c.dayZhu.gan)
        val v = BaziRules.liangVote(
            c.dayZhu.gan,
            c.yearZhu.gan, c.yearZhu.zhi,
            c.monthZhu.gan, c.monthZhu.zhi,
            c.dayZhu.zhi,
            c.timeZhu.gan, c.timeZhu.zhi,
            c.fourZhu.flatMap { it.hideGan },
            listOf(c.yearZhu.gan, c.monthZhu.gan, c.timeZhu.gan),
        )
        assertEquals("偏弱", v.strength)
        val r = XuanxueAI.bazi(c)
        assertTrue(r.text.contains("日主"))
        assertTrue(r.text.contains("五行分布"))
        assertTrue(r.text.contains("身偏弱"))
        assertTrue(r.items.any { it.ruleId == "R-BZ-LIANG-VOTE" })
        assertTrue(r.items.any { it.layer == BaziRules.LAYER_ALG })
        assertFalse(r.text.contains("性刚毅果决"))
        assertFalse(r.text.contains("如参天大树"))
        assertFalse(r.text.contains("宜泄宜克，喜财官食伤"))
        assertTrue(r.overall.contains("不宣称准确率"))
    }
}
