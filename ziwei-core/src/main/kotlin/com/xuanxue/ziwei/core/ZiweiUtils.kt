package com.xuanxue.ziwei.core

import com.xuanxue.ziwei.gen.DataTables
import com.xuanxue.ziwei.gen.HEAVENLY_STEM_INFO
import com.xuanxue.ziwei.gen.I18nZh

/**
 * Port of iztro src/utils/index.ts (MIT, SylarLong).
 */
object ZiweiUtils {

    fun fixIndex(index: Int, max: Int = 12): Int {
        var i = index
        if (i < 0) return fixIndex(i + max, max)
        if (i > max - 1) return fixIndex(i - max, max)
        return i
    }

    /** 地支名 -> 宫位索引（寅=0） */
    fun earthlyBranchIndexToPalaceIndex(earthlyBranchName: String): Int {
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        val yin = I18nZh.kot("yinEarthly", "Earthly")
        return fixIndex(DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranch) - DataTables.EARTHLY_BRANCHES.indexOf(yin))
    }

    fun getBrightness(starName: String, index: Int): String {
        val star = I18nZh.kot(starName)
        val targetBrightness = DataTables.STARS_INFO[star]?.brightness ?: return ""
        return I18nZh.t(targetBrightness[fixIndex(index)])
    }

    fun getMutagen(starName: String, heavenlyStemName: String): String {
        val heavenlyStem = I18nZh.kot(heavenlyStemName, "Heavenly")
        val starKey = I18nZh.kot(starName)
        val target = getTargetMutagens(heavenlyStem)
        val idx = target.indexOf(starKey)
        return if (idx < 0) "" else I18nZh.t(DataTables.MUTAGEN[idx])
    }

    fun getMutagensByHeavenlyStem(heavenlyStemName: String): List<String> {
        val heavenlyStem = I18nZh.kot(heavenlyStemName, "Heavenly")
        return getTargetMutagens(heavenlyStem).map { I18nZh.t(it) }
    }

    private fun getTargetMutagens(heavenlyStem: String): List<String> {
        // custom mutagens override not needed for v1; use built-in table
        return HEAVENLY_STEM_INFO[heavenlyStem]?.mutagen ?: emptyList()
    }

    /** 地支名 -> 宫位索引（寅=0） */
    fun fixEarthlyBranchIndex(earthlyBranchName: String): Int {
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        return fixIndex(DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranch) - DataTables.EARTHLY_BRANCHES.indexOf("yinEarthly"))
    }

    /** 调整农历月份索引（闰月处理），mirror of fixLunarMonthIndex */
    fun fixLunarMonthIndex(solarDateStr: String, timeIndex: Int, fixLeap: Boolean?): Int {
        val ld = LunarAdapter.solar2lunar(solarDateStr)
        val firstIndex = DataTables.EARTHLY_BRANCHES.indexOf("yinEarthly")
        val needToAdd = ld.isLeap && (fixLeap ?: false) && ld.lunarDay > 15 && timeIndex != 12
        return fixIndex(ld.lunarMonth + 1 - firstIndex + (if (needToAdd) 1 else 0))
    }

    fun fixLunarDayIndex(lunarDay: Int, timeIndex: Int): Int =
        if (timeIndex >= 12) lunarDay else lunarDay - 1

    fun timeToIndex(hour: Int): Int {
        if (hour == 0) return 0
        if (hour == 23) return 12
        return Math.floorDiv(hour + 1, 2)
    }

    /**
     * 起小限. 寅午戌人辰上起，申子辰人自戌宫，巳酉丑人未宫始，亥卯未人起丑宫。
     */
    fun getAgeIndex(earthlyBranchName: String): Int {
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        var ageIdx = -1
        when (earthlyBranch) {
            "yinEarthly", "wuEarthly", "xuEarthly" -> ageIdx = fixEarthlyBranchIndex("chen")
            "shenEarthly", "ziEarthly", "chenEarthly" -> ageIdx = fixEarthlyBranchIndex("xu")
            "siEarthly", "youEarthly", "chouEarthly" -> ageIdx = fixEarthlyBranchIndex("wei")
            "haiEarthly", "maoEarthly", "weiEarthly" -> ageIdx = fixIndex(fixEarthlyBranchIndex("chou"))
        }
        return ageIdx
    }
}
