package com.xuanxue.ziwei.core

import com.xuanxue.ziwei.gen.DataTables
import com.xuanxue.ziwei.gen.EARTHLY_BRANCH_INFO
import com.xuanxue.ziwei.gen.I18nZh
import com.xuanxue.ziwei.core.ZiweiUtils.fixEarthlyBranchIndex
import com.xuanxue.ziwei.core.ZiweiUtils.fixIndex
import com.xuanxue.ziwei.core.ZiweiUtils.fixLunarMonthIndex
import com.xuanxue.ziwei.core.ZiweiUtils.getAgeIndex
import com.xuanxue.ziwei.core.ZiweiLocation.AstrolabeParam

/**
 * Port of iztro src/astro/palace.ts (MIT, SylarLong).
 */
object ZiweiPalace {

    data class SoulAndBody(
        val soulIndex: Int,
        val bodyIndex: Int,
        val heavenlyStemOfSoul: String,
        val earthlyBranchOfSoul: String,
    )

    /**
     * 定寅首 + 安命身宫诀.
     * 寅起正月顺数至生月，逆数生时为命宫；顺数生时为身宫。
     */
    fun getSoulAndBody(param: AstrolabeParam): SoulAndBody {
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(
            param.solarDate, param.timeIndex, "normal", "normal",
        )
        val earthlyBranchOfTime = I18nZh.kot(ganZhi.hourly[1], "Earthly")
        val heavenlyStemOfYear = I18nZh.kot(ganZhi.yearly[0], "Heavenly")

        val firstIndex = DataTables.EARTHLY_BRANCHES.indexOf("yinEarthly")
        val monthIndex = fixLunarMonthIndex(param.solarDate, param.timeIndex, param.fixLeap)

        var soulIndex = fixIndex(monthIndex - DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranchOfTime))
        var bodyIndex = fixIndex(monthIndex + DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranchOfTime))

        if (param.from != null) {
            soulIndex = fixEarthlyBranchIndex(param.from.second)
            val bodyOffset = listOf(0, 2, 4, 6, 8, 10, 0, 2, 4, 6, 8, 10, 0)
            bodyIndex = fixIndex(bodyOffset[param.timeIndex] + soulIndex)
        }

        val startHeavenlyStem = DataTables.TIGER_RULE[heavenlyStemOfYear] ?: "jiaHeavenly"
        val heavenlyStemOfSoulIndex = fixIndex(DataTables.HEAVENLY_STEMS.indexOf(startHeavenlyStem) + soulIndex, 10)
        val heavenlyStemOfSoul = I18nZh.t(DataTables.HEAVENLY_STEMS[heavenlyStemOfSoulIndex])
        val earthlyBranchOfSoul = I18nZh.t(DataTables.EARTHLY_BRANCHES[fixIndex(soulIndex + firstIndex)])

        return SoulAndBody(soulIndex, bodyIndex, heavenlyStemOfSoul, earthlyBranchOfSoul)
    }

    /** 定五行局（以命宫天干地支而定） */
    fun getFiveElementsClass(heavenlyStemName: String, earthlyBranchName: String): String {
        val fiveElementsTable = listOf("wood3rd", "metal4th", "water2nd", "fire6th", "earth5th")
        val heavenlyStem = I18nZh.kot(heavenlyStemName, "Heavenly")
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")

        val heavenlyStemNumber = Math.floorDiv(DataTables.HEAVENLY_STEMS.indexOf(heavenlyStem), 2) + 1
        val earthlyBranchNumber = Math.floorDiv(fixIndex(DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranch), 6), 2) + 1
        var index = heavenlyStemNumber + earthlyBranchNumber
        while (index > 5) index -= 5
        return I18nZh.t(fiveElementsTable[index - 1])
    }

    /** 从寅宫开始的各宫名 */
    fun getPalaceNames(fromIndex: Int): List<String> {
        val names = MutableList(12) { "" }
        for (i in 0 until 12) {
            val idx = fixIndex(i - fromIndex)
            names[i] = I18nZh.t(DataTables.PALACES[idx])
        }
        return names
    }

    data class Decadal(val range: List<Int>, val heavenlyStem: String, val earthlyBranch: String)

    /**
     * 起大限：大限由命宫起，阳男阴女顺行，阴男阳女逆行，每十年过一宫限。
     * 小限：寅午戌人辰上起，申子辰人自戌宫，巳酉丑人未宫始，亥卯未人起丑宫；男顺女逆。
     */
    fun getHoroscope(param: AstrolabeParam): Horoscope {
        val decadals = MutableList<Decadal?>(12) { null }
        val genderKey = I18nZh.kot(param.gender ?: "male")
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(param.solarDate, param.timeIndex, "normal", "normal")
        val heavenlyStem = I18nZh.kot(ganZhi.yearly[0], "Heavenly")
        val earthlyBranch = I18nZh.kot(ganZhi.yearly[1], "Earthly")
        val sab = getSoulAndBody(param)
        val fiveElementsClass = I18nZh.kot(
            getFiveElementsClass(param.from?.first ?: sab.heavenlyStemOfSoul, param.from?.second ?: sab.earthlyBranchOfSoul),
        )
        val fiveElementsValue = DataTables.FIVE_ELEMENTS_VALUE[fiveElementsClass] ?: 0

        val startHeavenlyStem = DataTables.TIGER_RULE[heavenlyStem] ?: "jiaHeavenly"

        val yinYangOfYear = EARTHLY_BRANCH_INFO[earthlyBranch]?.yinYang ?: "阳"

        for (i in 0 until 12) {
            val idx = if (DataTables.GENDER[genderKey] == yinYangOfYear) {
                fixIndex(sab.soulIndex + i)
            } else {
                fixIndex(sab.soulIndex - i)
            }
            val start = fiveElementsValue + 10 * i
            val heavenlyStemIndex = fixIndex(DataTables.HEAVENLY_STEMS.indexOf(startHeavenlyStem) + idx, 10)
            val earthlyBranchIndex = fixIndex(DataTables.EARTHLY_BRANCHES.indexOf("yinEarthly") + idx)

            decadals[idx] = Decadal(
                range = listOf(start, start + 9),
                heavenlyStem = I18nZh.t(DataTables.HEAVENLY_STEMS[heavenlyStemIndex]),
                earthlyBranch = I18nZh.t(DataTables.EARTHLY_BRANCHES[earthlyBranchIndex]),
            )
        }

        val ageIdx = getAgeIndex(ganZhi.yearly[1])
        val ages = MutableList<List<Int>?>(12) { null }
        for (i in 0 until 12) {
            val age = MutableList(10) { 0 }
            for (j in 0 until 10) {
                age[j] = 12 * j + i + 1
            }
            val idx = if (I18nZh.kot(param.gender ?: "male") == "male") fixIndex(ageIdx + i) else fixIndex(ageIdx - i)
            ages[idx] = age
        }

        return Horoscope(decadals, ages)
    }

    data class Horoscope(val decadals: MutableList<Decadal?>, val ages: MutableList<List<Int>?>)
}
