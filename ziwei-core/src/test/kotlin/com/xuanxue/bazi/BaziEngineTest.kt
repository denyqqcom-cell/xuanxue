package com.xuanxue.bazi

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class BaziEngineTest {

    @Test
    fun yangMaleNoon() {
        // 1990-05-20 12:30 男 —— 庚午 辛巳 乙酉 壬午
        val c = BaziEngine.bySolar(1990, 5, 20, 12, 30, "男")
        assertEquals("庚午", c.yearZhu.gan + c.yearZhu.zhi)
        assertEquals("辛巳", c.monthZhu.gan + c.monthZhu.zhi)
        assertEquals("乙酉", c.dayZhu.gan + c.dayZhu.zhi)
        assertEquals("壬午", c.timeZhu.gan + c.timeZhu.zhi)
        assertEquals("泉中水", c.dayZhu.naYin)
        // 十神: 日主乙, 年干庚=正官
        assertEquals("正官", c.yearZhu.shiShenGan)
        // 起运: 阳男顺排, 5岁起
        assertTrue(c.startYunAge >= 1 && c.startYunAge <= 8)
        assertTrue(c.daYun.isNotEmpty())
        assertEquals("壬午", c.daYun.first().ganZhi) // 顺排: 辛巳月后为壬午
        // 称骨: 庚午年=1.9 + 四月=0.9 + 廿六=1.8 + 午时=1.0 = 5.6两
        assertEquals("5两6钱", c.chengGu?.weightText)
        assertTrue(c.chengGu?.poem?.isNotEmpty() == true)
        println("BAZI_OK ${c.fourZhu.map { it.gan + it.zhi }} 称骨=${c.chengGu?.weightText} 大运0=${c.daYun.first().ganZhi}")
    }

    @Test
    fun yinFemaleNight() {
        // 1988-12-01 23:30 女 —— 戊辰 癸亥 甲子 甲子 (晚子时日柱换日)
        val c = BaziEngine.bySolar(1988, 12, 1, 23, 30, "女")
        assertEquals("戊辰", c.yearZhu.gan + c.yearZhu.zhi)
        println("BAZI2 ${c.fourZhu.map { it.gan + it.zhi }} 起运${c.startYunAge}岁")
        // 阴女顺排
        assertTrue(c.daYun.isNotEmpty())
    }

    @Test
    fun chengGuKnown() {
        // 2000-01-01 00:30 男: 己卯年(兔=0.7) 冬月(11=0.9) 廿五(1.5) 子时(1.6) = 4.7两
        val c = BaziEngine.bySolar(2000, 1, 1, 0, 30, "男")
        assertEquals("4两7钱", c.chengGu?.weightText)
        println("BAZI3 称骨=${c.chengGu?.weightText} 四柱=${c.fourZhu.map { it.gan + it.zhi }}")
    }
}
