package com.xuanxue.qimen.core.ju

import com.xuanxue.qimen.core.calendar.Dun

enum class JuMethod {
    CHAI_BU_DAYCOUNT,
    CHAI_BU_FUTOU,
    ZHI_RUN,
    MAO_SHAN,
}

enum class Yuan(val label: String) { UPPER("上"), MIDDLE("中"), LOWER("下") }

data class JuResolution(
    val dun: Dun,
    val ju: Int,
    val yuan: Yuan,
    val method: JuMethod,
    /** Handoff explicitly marks day 16+ as unresolved; default currently keeps 下元. */
    val beyondDocumentedFifteenDays: Boolean,
)

object JuResolver {
    private val table: Map<Pair<Dun, String>, IntArray> = buildMap {
        fun row(dun: Dun, terms: List<String>, upper: Int, middle: Int, lower: Int) {
            terms.forEach { put(dun to it, intArrayOf(upper, middle, lower)) }
        }

        row(Dun.YANG, listOf("冬至", "惊蛰"), 1, 7, 4)
        row(Dun.YANG, listOf("小寒"), 2, 8, 5)
        row(Dun.YANG, listOf("大寒", "春分"), 3, 9, 6)
        row(Dun.YANG, listOf("立春"), 8, 5, 2)
        row(Dun.YANG, listOf("雨水"), 9, 6, 3)
        row(Dun.YANG, listOf("清明", "立夏"), 4, 1, 7)
        row(Dun.YANG, listOf("谷雨", "小满"), 5, 2, 8)
        row(Dun.YANG, listOf("芒种"), 6, 3, 9)

        row(Dun.YIN, listOf("夏至", "白露"), 9, 3, 6)
        row(Dun.YIN, listOf("小暑"), 8, 2, 5)
        row(Dun.YIN, listOf("大暑", "秋分"), 7, 1, 4)
        row(Dun.YIN, listOf("立秋"), 2, 5, 8)
        row(Dun.YIN, listOf("处暑"), 1, 4, 7)
        row(Dun.YIN, listOf("寒露", "立冬"), 6, 9, 3)
        row(Dun.YIN, listOf("霜降", "小雪"), 5, 8, 2)
        row(Dun.YIN, listOf("大雪"), 4, 7, 1)
    }

    fun resolveDayCount(jieqi: String, dayIndex: Int, dun: Dun): JuResolution {
        require(dayIndex >= 1) { "dayIndex must be 1-based" }
        val yuan = when (dayIndex) {
            in 1..5 -> Yuan.UPPER
            in 6..10 -> Yuan.MIDDLE
            else -> Yuan.LOWER
        }
        val expectedDun = if (jieqi in setOf(
                "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰",
                "春分", "清明", "谷雨", "立夏", "小满", "芒种",
            )) Dun.YANG else Dun.YIN
        require(dun == expectedDun) { "Jieqi $jieqi is inconsistent with dun=$dun" }

        val values = table[dun to jieqi] ?: error("No ju table row for $dun $jieqi")
        val ju = values[yuan.ordinal]
        return JuResolution(
            dun = dun,
            ju = ju,
            yuan = yuan,
            method = JuMethod.CHAI_BU_DAYCOUNT,
            beyondDocumentedFifteenDays = dayIndex > 15,
        )
    }

    internal fun rowsForInvariantTest(): Collection<IntArray> = table.values
}
