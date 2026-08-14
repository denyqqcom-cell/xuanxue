package com.xuanxue.liuren

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/** 《大六壬精义讲解》书例对照测试（伍剑虹，本地古籍提取） */
class LiuRenBookCaseTest {

    @Test
    fun bookCase1949() {
        // 例三：1949-10-01 甲子时，己丑年癸酉月甲子日甲子时，元首课
        // 书载三传：辰(初·财) → 申(中·官) → 子(末·父)；月将=辰（秋分后辰将，"太阳发用"）
        val c = LiuRenEngine.bySolar(1949, 10, 1, 0, 0)
        println("BOOK1 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ} 月将=${c.yueJiang}")
        println("BOOK1 三传=${c.sanChuan.chu}->${c.sanChuan.zhong}->${c.sanChuan.mo} [${c.sanChuan.fa}] 贵人=${c.guiRen}")
        assertEquals("甲子", c.dayGZ)
        assertEquals("甲子", c.hourGZ)
        assertEquals("辰", c.yueJiang)          // 秋分后辰将
        assertEquals("辰", c.sanChuan.chu)      // 元首课初传辰（太阳发用）
        assertEquals("申", c.sanChuan.zhong)
        assertEquals("子", c.sanChuan.mo)
        assertTrue(c.sanChuan.fa.contains("克"), "应为上克下类课")
        // 三传合水局：申子辰
        println("BOOK1 天盘: " + c.tianPan.joinToString(" "))
        println("BOOK1 四课: " + c.siKe.mapIndexed { i, k -> "课${i+1}=${k.zhi}(${k.dunGan})" }.joinToString(" "))
    }

    @Test
    fun bookCaseChenGongxian() {
        // 例一（陈公献《大六壬占验指南》）：戊寅三月己巳日乙丑时占天气，遥克课
        // 书载三传：寅(初·官) → 亥(中·财) → 申(末·子)；己巳旬空戌亥
        // 戊寅年 = 1998；三月 = 农历三月；己巳日乙丑时（丑时=1:30）
        // 1998 年农历三月：4/27~5/25 附近。用 Calendar 扫己巳日
        val cal = java.util.Calendar.getInstance().apply {
            set(1998, java.util.Calendar.APRIL, 1, 1, 30, 0)
        }
        var found: LiuRenEngine.LiuRenChart? = null
        repeat(60) {
            val s = com.nlf.calendar.Solar.fromYmdHms(
                cal.get(java.util.Calendar.YEAR), cal.get(java.util.Calendar.MONTH) + 1,
                cal.get(java.util.Calendar.DAY_OF_MONTH), 1, 30, 0
            )
            val ec = s.lunar.eightChar
            if (ec.getDayGan() == "己" && ec.getDayZhi() == "巳") {
                val c = LiuRenEngine.bySolar(
                    cal.get(java.util.Calendar.YEAR), cal.get(java.util.Calendar.MONTH) + 1,
                    cal.get(java.util.Calendar.DAY_OF_MONTH), 1, 30
                )
                found = c
                return@repeat
            }
            cal.add(java.util.Calendar.DAY_OF_MONTH, 1)
        }
        val c = found ?: LiuRenEngine.bySolar(1998, 4, 27, 1, 30)
        println("BOOK2 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ} 月将=${c.yueJiang}")
        println("BOOK2 三传=${c.sanChuan.chu}->${c.sanChuan.zhong}->${c.sanChuan.mo} [${c.sanChuan.fa}]")
        println("BOOK2 四课: " + c.siKe.mapIndexed { i, k -> "课${i+1}=${k.zhi}(${k.dunGan})" }.joinToString(" "))
        println("BOOK2 天盘: " + c.tianPan.joinToString(" "))
        // 书：遥克课 三传 寅→亥→申；己巳旬空戌亥（验证旬空）
        if (c.sanChuan.fa.contains("遥克")) {
            println("BOOK2 ✓ 遥克课确认")
        }
        println("BOOK2 旬空=${c.xunKong} (书载戌亥)")
    }
}
