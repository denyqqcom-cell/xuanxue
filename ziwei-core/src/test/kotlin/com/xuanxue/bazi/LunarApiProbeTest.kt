package com.xuanxue.bazi

import com.nlf.calendar.EightChar
import com.nlf.calendar.Solar
import kotlin.test.Test

class LunarApiProbeTest {
    @Test
    fun probe() {
        // 1990-05-20 午时 (12:30), 男 —— 已知四柱: 庚午 辛巳 甲申 庚午
        val solar = Solar.fromYmdHms(1990, 5, 20, 12, 30, 0)
        val lunar = solar.lunar
        val ec: EightChar = lunar.eightChar
        println("PROBE year=${ec.year} month=${ec.month} day=${ec.day} time=${ec.time}")
        println("PROBE 四柱: ${ec.getYearGan()}${ec.getYearZhi()} ${ec.getMonthGan()}${ec.getMonthZhi()} ${ec.getDayGan()}${ec.getDayZhi()} ${ec.getTimeGan()}${ec.getTimeZhi()}")
        println("PROBE 年支藏干: ${ec.getYearHideGan()} 十神: ${ec.getYearShiShenGan()}${ec.getYearShiShenZhi()}")
        println("PROBE 纳音: ${ec.getYearNaYin()} ${ec.getMonthNaYin()} ${ec.getDayNaYin()} ${ec.getTimeNaYin()}")
        println("PROBE 胎元=${ec.taiYuan} 命宫=${ec.mingGong} 身宫=${ec.shenGong} 空亡=${ec.getDayXunKong()}")
        val yun = ec.getYun(1) // 1=男
        println("PROBE 起运: 顺逆=${yun.toString()} 起运${yun.startYear}岁")
        for (i in 0 until minOf(6, yun.daYun.size)) {
            val dy = yun.daYun[i]
            val ln = dy.liuNian
            val first = ln.firstOrNull()
            println("PROBE 大运${i}: ${dy.ganZhi} ${dy.startYear}-${dy.endYear}岁 首流年=${first?.ganZhi}(${first?.year})")
        }
        println("PROBE 日主=${ec.getDayGan()} 日支=${ec.getDayZhi()} 身强弱(日主十二运)=${ec.getDayDiShi()}")
    }
}
