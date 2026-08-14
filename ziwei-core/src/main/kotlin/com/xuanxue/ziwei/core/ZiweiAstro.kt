package com.xuanxue.ziwei.core

import com.nlf.calendar.Solar
import com.xuanxue.ziwei.gen.DataTables
import com.xuanxue.ziwei.gen.EARTHLY_BRANCH_INFO
import com.xuanxue.ziwei.gen.I18nZh
import com.xuanxue.ziwei.core.ZiweiStars.Star
import com.xuanxue.ziwei.core.ZiweiPalace.Decadal
import com.xuanxue.ziwei.core.ZiweiLocation.AstrolabeParam

/**
 * Port of iztro src/astro/astro.ts bySolar main flow (MIT, SylarLong).
 * Config defaults: yearDivide='normal', horoscopeDivide='normal', dayDivide='forward', algorithm='default'.
 */
object ZiweiAstro {

    data class Palace(
        val index: Int,
        val name: String,
        val isBodyPalace: Boolean,
        val isOriginalPalace: Boolean,
        val heavenlyStem: String,
        val earthlyBranch: String,
        val majorStars: List<Star>,
        val minorStars: List<Star>,
        val adjectiveStars: List<Star>,
        val changsheng12: String,
        val boshi12: String,
        val jiangqian12: String,
        val suiqian12: String,
        val decadal: Decadal?,
        val ages: List<Int>?,
    )

    data class Astrolabe(
        val gender: String,
        val solarDate: String,
        val lunarDate: String,
        val time: String,
        val timeRange: String,
        val earthlyBranchOfSoulPalace: String,
        val earthlyBranchOfBodyPalace: String,
        val soul: String,
        val body: String,
        val fiveElementsClass: String,
        val palaces: List<Palace>,
    )

    fun bySolar(solarDate: String, timeIndex: Int, gender: String, fixLeap: Boolean = true): Astrolabe {
        var tIndex = timeIndex
        // dayDivide default 'forward' -> no adjustment; kept for parity
        // if (dayDivide == 'current' && tIndex >= 12) tIndex = 0

        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(solarDate, tIndex, "normal", "normal")
        val earthlyBranchOfYear = I18nZh.kot(ganZhi.yearly[1], "Earthly")
        val heavenlyStemOfYear = I18nZh.kot(ganZhi.yearly[0], "Heavenly")

        val sab = ZiweiPalace.getSoulAndBody(AstrolabeParam(solarDate, tIndex, gender, fixLeap))
        val palaceNames = ZiweiPalace.getPalaceNames(sab.soulIndex)
        val majorStars = ZiweiStars.getMajorStar(AstrolabeParam(solarDate, tIndex, gender, fixLeap))
        val minorStars = ZiweiStars.getMinorStar(solarDate, tIndex, fixLeap)
        val adjectiveStars = ZiweiStars.getAdjectiveStar(AstrolabeParam(solarDate, tIndex, gender, fixLeap))
        val changsheng12 = ZiweiStars.getChangsheng12(AstrolabeParam(solarDate, tIndex, gender, fixLeap))
        val boshi12 = ZiweiStars.getBoShi12(solarDate, gender)
        val (suiqian12, jiangqian12) = ZiweiStars.getYearly12(solarDate)
        val horoscope = ZiweiPalace.getHoroscope(AstrolabeParam(solarDate, tIndex, gender, fixLeap))

        val palaces = mutableListOf<Palace>()
        for (i in 0 until 12) {
            val heavenlyStemOfPalaceKey = DataTables.HEAVENLY_STEMS[
                ZiweiUtils.fixIndex(DataTables.HEAVENLY_STEMS.indexOf(I18nZh.kot(sab.heavenlyStemOfSoul, "Heavenly")) - sab.soulIndex + i, 10)
            ]
            val earthlyBranchOfPalaceKey = DataTables.EARTHLY_BRANCHES[ZiweiUtils.fixIndex(2 + i)]

            palaces.add(
                Palace(
                    index = i,
                    name = palaceNames[i],
                    isBodyPalace = sab.bodyIndex == i,
                    isOriginalPalace = !listOf("ziEarthly", "chouEarthly").contains(earthlyBranchOfPalaceKey) &&
                        heavenlyStemOfPalaceKey == heavenlyStemOfYear,
                    heavenlyStem = I18nZh.t(heavenlyStemOfPalaceKey),
                    earthlyBranch = I18nZh.t(earthlyBranchOfPalaceKey),
                    majorStars = majorStars[i],
                    minorStars = minorStars[i],
                    adjectiveStars = adjectiveStars[i],
                    changsheng12 = changsheng12[i],
                    boshi12 = boshi12[i],
                    jiangqian12 = jiangqian12[i],
                    suiqian12 = suiqian12[i],
                    decadal = horoscope.decadals[i],
                    ages = horoscope.ages[i],
                ),
            )
        }

        val earthlyBranchOfSoulPalaceKey = DataTables.EARTHLY_BRANCHES[ZiweiUtils.fixIndex(sab.soulIndex + 2)]
        val earthlyBranchOfBodyPalace = I18nZh.t(DataTables.EARTHLY_BRANCHES[ZiweiUtils.fixIndex(sab.bodyIndex + 2)])

        val norm = LunarAdapter.normalizeDateStr(solarDate)
        val lunar = Solar.fromYmd(norm[0], norm[1], norm[2]).lunar
        val lunarDateStr = lunar.toString()

        val soul = I18nZh.t(
            EARTHLY_BRANCH_INFO[earthlyBranchOfYear]?.let {
                // default algorithm: 以命宫地支找命主
                EARTHLY_BRANCH_INFO_BY_PALACE[sab.earthlyBranchOfSoul] ?: it.soul
            } ?: "",
        )

        val body = I18nZh.t(EARTHLY_BRANCH_INFO[earthlyBranchOfYear]?.body ?: "")

        return Astrolabe(
            gender = I18nZh.t(I18nZh.kot(gender)),
            solarDate = solarDate,
            lunarDate = lunarDateStr,
            time = I18nZh.t(DataTables.CHINESE_TIME[timeIndex]),
            timeRange = DataTables.TIME_RANGE[timeIndex],
            earthlyBranchOfSoulPalace = I18nZh.t(earthlyBranchOfSoulPalaceKey),
            earthlyBranchOfBodyPalace = earthlyBranchOfBodyPalace,
            soul = soul,
            body = body,
            fiveElementsClass = ZiweiPalace.getFiveElementsClass(sab.heavenlyStemOfSoul, sab.earthlyBranchOfSoul),
            palaces = palaces,
        )
    }

    /** 命主按命宫地支（default 派别） */
    private val EARTHLY_BRANCH_INFO_BY_PALACE: Map<String, String> = mapOf(
        "子" to "tanlangMaj", "丑" to "jumenMaj", "寅" to "lucunMin", "卯" to "wenquMin",
        "辰" to "lianzhenMaj", "巳" to "wuquMaj", "午" to "pojunMaj", "未" to "wuquMaj",
        "申" to "lianzhenMaj", "酉" to "wenquMin", "戌" to "lucunMin", "亥" to "jumenMaj",
    )
}
