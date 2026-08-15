package com.xuanxue.ai

import com.nlf.calendar.Solar
import com.xuanxue.qimen.QimenEngine
import java.time.LocalDate

/**
 * 奇门 handoff 里 implementation_ready 的静态表与生成器。
 * 只编码手续/对照表，不编码断语词典，不改排盘盘面。
 */
object QimenRules {

    const val LAYER_ALG = "算法"
    const val LAYER_SCHOOL = "门派"
    const val LAYER_EXP = "经验"

    val STEMS = "甲乙丙丁戊己庚辛壬癸"
    val BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

    /** R-HIT-XING；旧表壬亥/癸子已废弃（C-HIT-XING-OLD） */
    val HIT_XING: Map<String, Int> = mapOf(
        "戊" to 3, "己" to 2, "庚" to 8, "辛" to 9, "壬" to 4, "癸" to 4,
    )

    val YANG_JIEQI = setOf(
        "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰",
        "春分", "清明", "谷雨", "立夏", "小满", "芒种",
    )
    val YIN_JIEQI = setOf(
        "夏至", "小暑", "大暑", "立秋", "处暑", "白露",
        "秋分", "寒露", "霜降", "立冬", "小雪", "大雪",
    )

    /** 善天道印刷十对（R-WUBU-BOOK10）。键=日干+时干+时支 */
    val WUBU_PRINTED: Set<String> = setOf(
        "甲庚午", "乙辛巳", "丙壬辰", "丁癸卯", "戊甲寅",
        "己乙丑", "庚丙子", "辛丁酉", "壬戊申", "癸己未",
    )

    data class XunInfo(val xunShou: String, val dunYi: String, val xunKong: List<String>)

    /** R-WUBU-001：时干克日干、同阴阳、干序差 6。 */
    fun isWuBuYu(dayStem: String, hourStem: String): Boolean {
        val d = STEMS.indexOf(dayStem)
        val h = STEMS.indexOf(hourStem)
        return d >= 0 && h >= 0 && h == (d + 6) % 10
    }

    fun isPrintedWuBu(dayStem: String, hourStem: String, hourBranch: String): Boolean =
        (dayStem + hourStem + hourBranch) in WUBU_PRINTED

    /** R-CAL-002 五鼠遁 */
    fun hourStemByWuShuDun(dayStem: String, hourBranch: String): String {
        val start = when (dayStem) {
            "甲", "己" -> 0
            "乙", "庚" -> 2
            "丙", "辛" -> 4
            "丁", "壬" -> 6
            "戊", "癸" -> 8
            else -> return ""
        }
        val b = BRANCHES.indexOf(hourBranch)
        if (b < 0) return ""
        return STEMS[(start + b) % 10].toString()
    }

    /** R-XUN-001 */
    fun xunOf(hourGZ: String): XunInfo? {
        if (hourGZ.length < 2) return null
        val s = seqOf(hourGZ[0].toString(), hourGZ[1].toString()) ?: return null
        val base = (s / 10) * 10
        val xunShou = STEMS[base % 10].toString() + BRANCHES[base % 12].toString()
        val dunYi = QimenEngine.XUN_DUN[xunShou] ?: return null
        val kong = listOf(
            BRANCHES[(base + 10) % 12].toString(),
            BRANCHES[(base + 11) % 12].toString(),
        )
        return XunInfo(xunShou, dunYi, kong)
    }

    fun seqOf(gan: String, zhi: String): Int? {
        val g = STEMS.indexOf(gan)
        val z = BRANCHES.indexOf(zhi)
        if (g < 0 || z < 0) return null
        for (i in 0 until 60) {
            if (i % 10 == g && i % 12 == z) return i
        }
        return null
    }

    /** R-CAL-003：23:00–24:00 为晚子。20–23 晚子已否决。 */
    fun clockSlot(hour: Int, minute: Int): String = when {
        hour == 0 -> "早子"
        hour == 23 -> "晚子"
        else -> {
            val branchIdx = ((hour + 1) / 2) % 12
            BRANCHES[branchIdx].toString() + "时"
        }
    }

    /** R-JU-001：节气日内序号 1-5 上 / 6-10 中 / 11+ 下（16+ 仍按下元，未另有来源）。 */
    fun yuanByDayCount(dayIndex: Int): String = when {
        dayIndex <= 0 -> ""
        dayIndex <= 5 -> "上元"
        dayIndex <= 10 -> "中元"
        else -> "下元"
    }

    fun juOf(jieqi: String, yuan: String): Int? {
        val rule = QimenEngine.JIE_QI_JU[jieqi] ?: return null
        return when (yuan) {
            "上元", "上" -> rule.shang
            "中元", "中" -> rule.zhong
            "下元", "下" -> rule.xia
            else -> null
        }
    }

    fun dunLabel(jieqi: String): String? = when (jieqi) {
        in YANG_JIEQI -> "阳遁"
        in YIN_JIEQI -> "阴遁"
        else -> null
    }

    data class CivilStamp(val year: Int, val month: Int, val day: Int, val hour: Int, val minute: Int)

    fun parseSolarDate(s: String): CivilStamp? {
        val m = Regex("""(\d+)-(\d+)-(\d+)\s+(\d+):(\d+)""").matchEntire(s.trim()) ?: return null
        return CivilStamp(
            m.groupValues[1].toInt(),
            m.groupValues[2].toInt(),
            m.groupValues[3].toInt(),
            m.groupValues[4].toInt(),
            m.groupValues[5].toInt(),
        )
    }

    /**
     * 节气日内序号（公历日差，1-based）。
     * 节气时刻本身仍用 lunar-java 表；不使用「立春2.4」约数表。
     */
    fun jieqiDayIndex(year: Int, month: Int, day: Int, jieqiName: String): Int? {
        val solar = Solar.fromYmd(year, month, day)
        val start = solar.lunar.jieQiTable[jieqiName] ?: return null
        val a = LocalDate.of(start.year, start.month, start.day)
        val b = LocalDate.of(year, month, day)
        val idx = (b.toEpochDay() - a.toEpochDay()).toInt() + 1
        return idx.takeIf { it >= 1 }
    }

    fun readingItem(
        layer: String,
        ruleId: String,
        summary: String,
        source: String,
        confidence: String,
        detail: String = "",
    ): ReadingItem = ReadingItem(
        title = "$layer · $ruleId",
        summary = summary,
        detail = detail,
        layer = layer,
        ruleId = ruleId,
        source = source,
        confidence = confidence,
    )
}
