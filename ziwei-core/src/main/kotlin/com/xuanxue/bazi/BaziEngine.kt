package com.xuanxue.bazi

import com.nlf.calendar.EightChar
import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar
import com.nlf.calendar.eightchar.DaYun

/**
 * 八字排盘引擎 — 基于 lunar-java (MIT, 6tail)。
 * 计算：四柱、十神、藏干、纳音、胎元/命宫/身宫、空亡、大运、流年。
 * 所有计算本地完成，无网络。
 */
object BaziEngine {

    data class Zhu(val gan: String, val zhi: String, val hideGan: List<String>,
                   val shiShenGan: String, val shiShenZhi: List<String>,
                   val naYin: String, val wuXing: String, val diShi: String)

    data class DaYunItem(val ganZhi: String, val startYear: Int, val endYear: Int,
                         val liuNian: List<Pair<String, Int>>)

    data class BaziChart(
        val solarDate: String,
        val lunarDateStr: String,
        val gender: String,           // 男/女
        val yearZhu: Zhu, val monthZhu: Zhu, val dayZhu: Zhu, val timeZhu: Zhu,
        val taiYuan: String, val mingGong: String, val shenGong: String,
        val dayKong: String,          // 空亡
        val yunGender: Int,           // lunar-java 用 1男/0女
        val startYunAge: Int,
        val daYun: List<DaYunItem>,
        val chengGu: ChengGu.Result?,
    ) {
        val fourZhu: List<Zhu> get() = listOf(yearZhu, monthZhu, dayZhu, timeZhu)
    }

    fun bySolar(year: Int, month: Int, day: Int, hour: Int, minute: Int,
                gender: String, fixLeap: Boolean = true): BaziChart {
        val solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        val lunar: Lunar = solar.lunar
        val ec: EightChar = lunar.eightChar

        fun zhu(gan: String, zhi: String, hide: List<String>, ssGan: String, ssZhi: List<String>,
                naYin: String, wx: String, diShi: String) = Zhu(gan, zhi, hide, ssGan, ssZhi, naYin, wx, diShi)

        val yearZhu = zhu(ec.getYearGan(), ec.getYearZhi(), ec.getYearHideGan(),
            ec.getYearShiShenGan(), ec.getYearShiShenZhi(), ec.getYearNaYin(), ec.getYearWuXing(), ec.getYearDiShi())
        val monthZhu = zhu(ec.getMonthGan(), ec.getMonthZhi(), ec.getMonthHideGan(),
            ec.getMonthShiShenGan(), ec.getMonthShiShenZhi(), ec.getMonthNaYin(), ec.getMonthWuXing(), ec.getMonthDiShi())
        val dayZhu = zhu(ec.getDayGan(), ec.getDayZhi(), ec.getDayHideGan(),
            ec.getDayShiShenGan(), ec.getDayShiShenZhi(), ec.getDayNaYin(), ec.getDayWuXing(), ec.getDayDiShi())
        val timeZhu = zhu(ec.getTimeGan(), ec.getTimeZhi(), ec.getTimeHideGan(),
            ec.getTimeShiShenGan(), ec.getTimeShiShenZhi(), ec.getTimeNaYin(), ec.getTimeWuXing(), ec.getTimeDiShi())

        val yun = ec.getYun(if (gender == "女") 0 else 1)
        val daYun = yun.daYun.map { dy: DaYun ->
            DaYunItem(
                ganZhi = dy.ganZhi,
                startYear = dy.startYear,
                endYear = dy.endYear,
                liuNian = dy.liuNian.map { Pair(it.ganZhi, it.year) }
            )
        }.filter { it.ganZhi.isNotBlank() }

        return BaziChart(
            solarDate = "$year-$month-$day $hour:$minute",
            lunarDateStr = lunar.toString(),
            gender = gender,
            yearZhu = yearZhu, monthZhu = monthZhu, dayZhu = dayZhu, timeZhu = timeZhu,
            taiYuan = ec.taiYuan, mingGong = ec.mingGong, shenGong = ec.shenGong,
            dayKong = ec.getDayXunKong(),
            yunGender = if (gender == "女") 0 else 1,
            startYunAge = yun.startYear,
            daYun = daYun,
            chengGu = ChengGu.calc(lunar),
        )
    }
}
