package com.xuanxue.ai

import com.xuanxue.qimen.QimenEngine
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotEquals
import kotlin.test.assertNotNull
import kotlin.test.assertTrue

class QimenRulesTest {

    @Test
    fun wubuGeneratorMatchesPrintedJiaGengWu() {
        assertTrue(QimenRules.isWuBuYu("甲", "庚"))
        assertTrue(QimenRules.isPrintedWuBu("甲", "庚", "午"))
    }

    @Test
    fun wubuGeneratorExtraJiYiHaiNotInPrintedTable() {
        assertTrue(QimenRules.isWuBuYu("己", "乙"))
        assertFalse(QimenRules.isPrintedWuBu("己", "乙", "亥"))
        assertTrue(QimenRules.isPrintedWuBu("己", "乙", "丑"))
    }

    @Test
    fun hitXingMap() {
        assertEquals(3, QimenRules.HIT_XING["戊"])
        assertEquals(4, QimenRules.HIT_XING["壬"])
        assertEquals(4, QimenRules.HIT_XING["癸"])
        assertFalse(QimenRules.HIT_XING.containsValue(11))
    }

    @Test
    fun xunJiaziAndJiaxu() {
        val a = QimenRules.xunOf("甲子")
        assertNotNull(a)
        assertEquals("戊", a.dunYi)
        assertEquals(listOf("戌", "亥"), a.xunKong)
        val b = QimenRules.xunOf("甲戌")
        assertNotNull(b)
        assertEquals("己", b.dunYi)
        assertEquals(listOf("申", "酉"), b.xunKong)
    }

    @Test
    fun wuShuDun() {
        assertEquals("甲", QimenRules.hourStemByWuShuDun("甲", "子"))
        assertEquals("甲", QimenRules.hourStemByWuShuDun("己", "子"))
        assertEquals("丙", QimenRules.hourStemByWuShuDun("乙", "子"))
        assertEquals("庚", QimenRules.hourStemByWuShuDun("癸", "申"))
    }

    @Test
    fun juTableDongzhiShangAndLiqiuXia() {
        assertEquals(1, QimenRules.juOf("冬至", "上元"))
        assertEquals(8, QimenRules.juOf("立秋", "下元"))
        assertEquals("阴遁", QimenRules.dunLabel("立秋"))
        assertEquals("阳遁", QimenRules.dunLabel("冬至"))
    }

    @Test
    fun clockSlots() {
        assertEquals("早子", QimenRules.clockSlot(0, 30))
        assertEquals("晚子", QimenRules.clockSlot(23, 30))
        assertTrue(QimenRules.clockSlot(20, 30).contains("戌"))
    }

    @Test
    fun liqiu20260807JuMethodsSplit() {
        val c = QimenEngine.bySolar(2026, 8, 7, 16, 0)
        assertEquals("立秋", c.jieQi)
        val idx = QimenRules.jieqiDayIndex(2026, 8, 7, c.jieQi)
        assertNotNull(idx)
        val dayYuan = QimenRules.yuanByDayCount(idx)
        val dayJu = QimenRules.juOf(c.jieQi, dayYuan)
        assertNotNull(dayJu)
        assertTrue(idx >= 1)
        val r = XuanxueAI.qimen(c)
        assertTrue(r.items.any { it.ruleId == "R-JU-001" })
        assertTrue(r.text.contains("符头"))
        assertTrue(r.text.contains("日数分段"))
        assertTrue(r.text.contains("${c.ju}局"))
        assertTrue(r.text.contains("${dayJu}局"))
        if (c.yuan != dayYuan || c.ju != dayJu) {
            assertNotEquals(c.ju, dayJu)
            assertTrue(r.text.contains("两法局数不同"))
        }
    }

    @Test
    fun sourcedReadingHasNoOmenDictionary() {
        val c = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        val r = XuanxueAI.qimen(c)
        val text = r.text
        assertTrue(r.items.isNotEmpty())
        assertTrue(text.contains("值符"))
        assertTrue(r.items.any { it.ruleId == "R-XUN-001" })
        assertTrue(r.items.any { it.ruleId == "R-MA-001" })
        assertTrue(r.items.any { it.layer == QimenRules.LAYER_ALG })
        assertTrue(r.items.any { it.layer == QimenRules.LAYER_SCHOOL })
        assertTrue(r.items.any { it.layer == QimenRules.LAYER_EXP })
        assertFalse(text.contains("宜休养生息"))
        assertFalse(text.contains("利出行变动"))
        assertFalse(text.contains("暂缓待填实"))
        assertFalse(text.contains("八门吉凶"))
        assertTrue(text.contains("不宣称准确率") || r.overall.contains("不宣称准确率"))
        assertTrue(r.items.none { it.ruleId == "R-SCORE-001" && it.summary.contains("大凶") && it.summary.contains("停看") && !it.summary.contains("不") })
    }
}
