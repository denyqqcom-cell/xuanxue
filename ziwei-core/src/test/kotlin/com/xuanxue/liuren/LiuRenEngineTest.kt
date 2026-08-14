package com.xuanxue.liuren

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class LiuRenEngineTest {

    @Test
    fun basicStructure() {
        val c = LiuRenEngine.bySolar(2026, 8, 15, 10, 0)
        println("NR1 ${c.solarDate} 月将=${c.yueJiang} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}")
        println("NR1 天盘: " + c.tianPan.joinToString(" "))
        println("NR1 四课: " + c.siKe.mapIndexed { i, k -> "课${i + 1}=${k.zhi}(${k.dunGan})" }.joinToString(" "))
        println("NR1 三传: ${c.sanChuan.chu}->${c.sanChuan.zhong}->${c.sanChuan.mo} [${c.sanChuan.fa}] 贵人=${c.guiRen} 旬空=${c.xunKong}")
        assertTrue(c.tianPan.all { it.isNotEmpty() })
        assertEquals(4, c.siKe.size)
        assertTrue(c.sanChuan.chu.isNotEmpty())
        assertTrue(c.xunKong.size == 2)
        // 天地盘每个地支恰出现一次
        assertEquals(12, c.tianPan.toSet().size)
    }

    @Test
    fun tianPanKnown() {
        // 月将加时验证：天盘月将落于时支位
        val c = LiuRenEngine.bySolar(2026, 8, 15, 10, 0)
        val hourZhi = c.hourGZ[1].toString()
        assertEquals(c.yueJiang, c.tianPan[LiuRenEngine.ZHI.indexOf(hourZhi)], "天盘时支位应为月将")
        println("NR2 时支=$hourZhi 天盘[$hourZhi]=${c.tianPan[LiuRenEngine.ZHI.indexOf(hourZhi)]} = 月将${c.yueJiang} ✓")
    }

    @Test
    fun dunGanKnown() {
        // 甲日起甲子时：甲子 乙丑 丙寅...
        assertEquals("甲", LiuRenEngine.dunGanOf("甲", "子"))
        assertEquals("乙", LiuRenEngine.dunGanOf("甲", "丑"))
        assertEquals("丙", LiuRenEngine.dunGanOf("甲", "寅"))
        // 乙日起丙子时
        assertEquals("丙", LiuRenEngine.dunGanOf("乙", "子"))
        assertEquals("戊", LiuRenEngine.dunGanOf("丙", "子"))
        println("NR3 遁干验证 ✓")
    }

    @Test
    fun guiRenKnown() {
        assertEquals("丑", LiuRenEngine.guiRen("甲", false))  // 甲日昼贵丑（甲戊庚牛羊）
        assertEquals("未", LiuRenEngine.guiRen("甲", true))   // 夜贵未
        assertEquals("子", LiuRenEngine.guiRen("乙", false))  // 乙己鼠猴乡
        assertEquals("巳", LiuRenEngine.guiRen("壬", false))  // 壬癸蛇兔藏
        println("NR4 贵人验证 ✓")
    }

    @Test
    fun keXiaoKnown() {
        // 贼克验证：构造一个天盘使课1上克下
        // 简化：验证九宗门返回合法
        val c = LiuRenEngine.bySolar(1990, 5, 20, 12, 30)
        println("NR5 ${c.solarDate} 三传=${c.sanChuan.chu}->${c.sanChuan.zhong}->${c.sanChuan.mo} [${c.sanChuan.fa}]")
        assertTrue(c.sanChuan.chu in LiuRenEngine.ZHI)
    }
}
