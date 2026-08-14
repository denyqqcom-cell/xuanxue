package com.xuanxue.ziwei.core

import com.nlf.calendar.Lunar
import com.nlf.calendar.LunarMonth
import com.nlf.calendar.LunarYear
import com.nlf.calendar.Solar

/**
 * Lunar adapter replicating lunar-lite (MIT, SylarLong) semantics on top of
 * lunar-java (MIT, 6tail) — same algorithm family, same author lineage.
 */
object LunarAdapter {

    data class GanZhiResult(
        val yearly: List<String>,
        val monthly: List<String>,
        val daily: List<String>,
        val hourly: List<String>,
    )

    data class LunarDate(
        val lunarYear: Int,
        val lunarMonth: Int,
        val lunarDay: Int,
        val isLeap: Boolean,
    )

    /** Split "YYYY-MM-DD" (or with time) into ints; mirrors lunar-lite normalizeDateStr */
    fun normalizeDateStr(dateStr: String): List<Int> =
        dateStr.split(Regex("[ \\-:/.]+")).map { Math.abs(it.toInt()) }

    /** solar -> lunar, mirroring lunar-lite solar2lunar */
    fun solar2lunar(dateStr: String): LunarDate {
        val (y, m, d) = normalizeDateStr(dateStr)
        val lunar = Solar.fromYmd(y, m, d).lunar
        return LunarDate(
            lunarYear = lunar.year,
            lunarMonth = Math.abs(lunar.month),
            lunarDay = lunar.day,
            isLeap = lunar.month < 0,
        )
    }

    fun lunar2solar(dateStr: String, isLeapMonth: Boolean): Triple<Int, Int, Int> {
        val (y, m, d) = normalizeDateStr(dateStr)
        var lunar = Lunar.fromYmd(y, m, d)
        val leapMonth = LunarYear.fromYear(lunar.year).leapMonth
        if (leapMonth > 0 && leapMonth == m && isLeapMonth) {
            lunar = Lunar.fromYmd(y, 0 - m, d)
        }
        val solar = lunar.solar
        return Triple(solar.year, solar.month, solar.day)
    }

    /**
     * Mirror of lunar-lite getHeavenlyStemAndEarthlyBranchBySolarDate.
     * timeIndex: 0..12 (12 = 晚子时). yearDivide: 'normal'|'exact'. monthDivide: 'normal'|'exact'.
     */
    fun getHeavenlyStemAndEarthlyBranchBySolarDate(
        dateStr: String,
        timeIndex: Int,
        yearDivide: String = "normal",
        monthDivide: String = "normal",
    ): GanZhiResult {
        val (y, m, d) = normalizeDateStr(dateStr)
        val hour = Math.max(timeIndex * 2 - 1, 0)
        val solar = Solar.fromYmdHms(y, m, d, hour, 30, 0)
        val lunar = solar.lunar

        val yearlyGan = if (yearDivide == "normal") lunar.yearGan else lunar.yearGanByLiChun
        val yearlyZhi = if (yearDivide == "normal") lunar.yearZhi else lunar.yearZhiByLiChun
        val yearly = listOf(yearlyGan, yearlyZhi)

        val monthly: List<String> = if (monthDivide == "exact") {
            listOf(lunar.monthGanExact, lunar.monthZhiExact)
        } else {
            calculateMonthlyGanZhi(yearlyGan, lunar)
        }

        val daily = listOf(lunar.dayGanExact, lunar.dayZhiExact)
        val hourly = listOf(lunar.timeGan, lunar.timeZhi)

        return GanZhiResult(yearly, monthly, daily, hourly)
    }

    /** 五虎遁 monthly gan-zhi when dividing by 初一 (mirror of lunar-lite calculateMonthlyGanZhi) */
    private val HEAVENLY_STEMS = listOf("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸")
    private val MONTHLY_EARTHLY_BRANCHES = listOf("寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑")
    private val FIVE_TIGER = listOf("丙", "戊", "庚", "壬", "甲", "丙", "戊", "庚", "壬", "甲")

    private fun calculateMonthlyGanZhi(yearlyGan: String, lunar: Lunar): List<String> {
        val fixLeap = if (lunar.month < 0 && lunar.day > 15) 1 else 0
        val ganIdx = fixIndex(
            HEAVENLY_STEMS.indexOf(FIVE_TIGER[HEAVENLY_STEMS.indexOf(yearlyGan)]) + Math.abs(lunar.month) - 1 + fixLeap,
            10,
        )
        val zhiIdx = Math.abs(lunar.month) - 1 + fixLeap
        return listOf(HEAVENLY_STEMS[ganIdx], MONTHLY_EARTHLY_BRANCHES[zhiIdx])
    }

    /** Mirror of lunar-lite getTotalDaysOfLunarMonth(solarDateStr) via LunarMonth */
    fun getTotalDaysOfLunarMonth(solarDateStr: String): Int {
        val ld = solar2lunar(solarDateStr)
        val month = LunarMonth.fromYm(ld.lunarYear, if (ld.isLeap) 0 - ld.lunarMonth else ld.lunarMonth)
        return month?.dayCount ?: 0
    }

    fun fixIndex(index: Int, max: Int = 12): Int {
        var i = index
        if (i < 0) return fixIndex(i + max, max)
        if (i > max - 1) return fixIndex(i - max, max)
        if (i == 0 && 1.0 / i == Double.NEGATIVE_INFINITY) return 0
        return i
    }
}
