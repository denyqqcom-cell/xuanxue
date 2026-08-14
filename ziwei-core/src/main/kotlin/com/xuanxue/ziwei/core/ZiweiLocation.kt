package com.xuanxue.ziwei.core

import com.xuanxue.ziwei.gen.DataTables
import com.xuanxue.ziwei.gen.I18nZh
import com.xuanxue.ziwei.core.ZiweiUtils.fixEarthlyBranchIndex
import com.xuanxue.ziwei.core.ZiweiUtils.fixIndex
import com.xuanxue.ziwei.core.ZiweiUtils.fixLunarDayIndex
import com.xuanxue.ziwei.core.ZiweiUtils.fixLunarMonthIndex

/**
 * Port of iztro src/star/location.ts (MIT, SylarLong) — 安星法.
 */
object ZiweiLocation {

    data class AstrolabeParam(
        val solarDate: String,
        val timeIndex: Int,
        val gender: String? = null,
        val fixLeap: Boolean? = false,
        val from: Pair<String, String>? = null,
    )

    data class StartIndex(val ziweiIndex: Int, val tianfuIndex: Int)

    /**
     * 起紫微星诀. 六五四三二，酉午亥辰丑，局数除日数，商数宫前走；若见数无余，便要起虎口，日数小於局，还直宫中守。
     */
    fun getStartIndex(param: AstrolabeParam): StartIndex {
        val sab = ZiweiPalace.getSoulAndBody(param)
        val heavenlyStemOfSoul = sab.heavenlyStemOfSoul
        val earthlyBranchOfSoul = sab.earthlyBranchOfSoul
        val ld = LunarAdapter.solar2lunar(param.solarDate)
        val lunarDay = ld.lunarDay

        val baseHeavenlyStem = param.from?.first ?: heavenlyStemOfSoul
        val baseEarthlyBranch = param.from?.second ?: earthlyBranchOfSoul

        val fiveElementsKey = I18nZh.kot(ZiweiPalace.getFiveElementsClass(baseHeavenlyStem, baseEarthlyBranch))
        val fiveElementsValue = DataTables.FIVE_ELEMENTS_VALUE[fiveElementsKey] ?: 0

        var remainder = -1
        var quotient: Int
        var offset = -1

        val maxDays = LunarAdapter.getTotalDaysOfLunarMonth(param.solarDate)
        var day = if (param.timeIndex == 12) lunarDay + 1 else lunarDay
        if (day > maxDays) day -= maxDays

        do {
            offset++
            val divisor = day + offset
            quotient = Math.floorDiv(divisor, fiveElementsValue)
            remainder = divisor % fiveElementsValue
        } while (remainder != 0)

        quotient %= 12
        var ziweiIndex = quotient - 1

        ziweiIndex = if (offset % 2 == 0) {
            fixIndex(ziweiIndex + offset)
        } else {
            fixIndex(ziweiIndex - offset)
        }

        val tianfuIndex = fixIndex(12 - ziweiIndex)
        return StartIndex(ziweiIndex, tianfuIndex)
    }

    /**
     * 定禄存、擎羊、陀罗、天马（按年干支）.
     */
    fun getLuYangTuoMaIndex(heavenlyStemName: String, earthlyBranchName: String): LuYangTuoMa {
        var luIndex = -1
        var maIndex = 0
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")

        when (earthlyBranch) {
            "yinEarthly", "wuEarthly", "xuEarthly" -> maIndex = fixEarthlyBranchIndex("shen")
            "shenEarthly", "ziEarthly", "chenEarthly" -> maIndex = fixEarthlyBranchIndex("yin")
            "siEarthly", "youEarthly", "chouEarthly" -> maIndex = fixEarthlyBranchIndex("hai")
            "haiEarthly", "maoEarthly", "weiEarthly" -> maIndex = fixEarthlyBranchIndex("si")
        }

        val heavenlyStem = I18nZh.kot(heavenlyStemName, "Heavenly")
        when (heavenlyStem) {
            "jiaHeavenly" -> luIndex = fixEarthlyBranchIndex("yin")
            "yiHeavenly" -> luIndex = fixEarthlyBranchIndex("mao")
            "bingHeavenly", "wuHeavenly" -> luIndex = fixEarthlyBranchIndex("si")
            "dingHeavenly", "jiHeavenly" -> luIndex = fixEarthlyBranchIndex("woo")
            "gengHeavenly" -> luIndex = fixEarthlyBranchIndex("shen")
            "xinHeavenly" -> luIndex = fixEarthlyBranchIndex("you")
            "renHeavenly" -> luIndex = fixEarthlyBranchIndex("hai")
            "guiHeavenly" -> luIndex = fixEarthlyBranchIndex("zi")
        }

        return LuYangTuoMa(
            luIndex = luIndex,
            maIndex = maIndex,
            yangIndex = fixIndex(luIndex + 1),
            tuoIndex = fixIndex(luIndex - 1),
        )
    }

    data class LuYangTuoMa(val luIndex: Int, val maIndex: Int, val yangIndex: Int, val tuoIndex: Int)

    /** 天魁天钺（按年干）：甲戊庚丑未、乙己子申、辛午寅、壬癸卯巳、丙丁亥酉 */
    fun getKuiYueIndex(heavenlyStemName: String): KuiYue {
        var kuiIndex = -1
        var yueIndex = -1
        val heavenlyStem = I18nZh.kot(heavenlyStemName, "Heavenly")
        when (heavenlyStem) {
            "jiaHeavenly", "wuHeavenly", "gengHeavenly" -> {
                kuiIndex = fixEarthlyBranchIndex("chou"); yueIndex = fixEarthlyBranchIndex("wei")
            }
            "yiHeavenly", "jiHeavenly" -> {
                kuiIndex = fixEarthlyBranchIndex("zi"); yueIndex = fixEarthlyBranchIndex("shen")
            }
            "xinHeavenly" -> {
                kuiIndex = fixEarthlyBranchIndex("woo"); yueIndex = fixEarthlyBranchIndex("yin")
            }
            "bingHeavenly", "dingHeavenly" -> {
                kuiIndex = fixEarthlyBranchIndex("hai"); yueIndex = fixEarthlyBranchIndex("you")
            }
            "renHeavenly", "guiHeavenly" -> {
                kuiIndex = fixEarthlyBranchIndex("mao"); yueIndex = fixEarthlyBranchIndex("si")
            }
        }
        return KuiYue(kuiIndex, yueIndex)
    }

    data class KuiYue(val kuiIndex: Int, val yueIndex: Int)

    /** 左辅右弼（按生月）：辰上顺正寻左辅，戌上逆正右弼当 */
    fun getZuoYouIndex(lunarMonth: Int): ZuoYou {
        val zuoIndex = fixIndex(fixEarthlyBranchIndex("chen") + (lunarMonth - 1))
        val youIndex = fixIndex(fixEarthlyBranchIndex("xu") - (lunarMonth - 1))
        return ZuoYou(zuoIndex, youIndex)
    }

    data class ZuoYou(val zuoIndex: Int, val youIndex: Int)

    /** 文昌文曲（按时支）：辰上顺时文曲位，戌上逆时觅文昌 */
    fun getChangQuIndex(timeIndex: Int): ChangQu {
        val changIndex = fixIndex(fixEarthlyBranchIndex("xu") - fixIndex(timeIndex))
        val quIndex = fixIndex(fixEarthlyBranchIndex("chen") + fixIndex(timeIndex))
        return ChangQu(changIndex, quIndex)
    }

    data class ChangQu(val changIndex: Int, val quIndex: Int)

    /** 日系星：三台、八座、恩光、天贵 */
    fun getDailyStarIndex(solarDateStr: String, timeIndex: Int, fixLeap: Boolean?): DailyStar {
        val ld = LunarAdapter.solar2lunar(solarDateStr)
        val lunarDay = ld.lunarDay
        val monthIndex = fixLunarMonthIndex(solarDateStr, timeIndex, fixLeap)
        val (zuoIndex, youIndex) = getZuoYouIndex(monthIndex + 1)
        val (changIndex, quIndex) = getChangQuIndex(timeIndex)
        val dayIndex = fixLunarDayIndex(lunarDay, timeIndex)
        val santaiIndex = fixIndex((zuoIndex + dayIndex) % 12)
        val bazuoIndex = fixIndex((youIndex - dayIndex) % 12)
        val enguangIndex = fixIndex(((changIndex + dayIndex) % 12) - 1)
        val tianguiIndex = fixIndex(((quIndex + dayIndex) % 12) - 1)
        return DailyStar(santaiIndex, bazuoIndex, enguangIndex, tianguiIndex)
    }

    data class DailyStar(val santaiIndex: Int, val bazuoIndex: Int, val enguangIndex: Int, val tianguiIndex: Int)

    /** 时系星：台辅、封诰 */
    fun getTimelyStarIndex(timeIndex: Int): TimelyStar {
        val taifuIndex = fixIndex(fixEarthlyBranchIndex("woo") + fixIndex(timeIndex))
        val fenggaoIndex = fixIndex(fixEarthlyBranchIndex("yin") + fixIndex(timeIndex))
        return TimelyStar(taifuIndex, fenggaoIndex)
    }

    data class TimelyStar(val taifuIndex: Int, val fenggaoIndex: Int)

    /** 地空地劫（按时支）：亥上子时顺安劫，逆回便是地空亡 */
    fun getKongJieIndex(timeIndex: Int): KongJie {
        val fixedTimeIndex = fixIndex(timeIndex)
        val haiIndex = fixEarthlyBranchIndex("hai")
        return KongJie(fixIndex(haiIndex - fixedTimeIndex), fixIndex(haiIndex + fixedTimeIndex))
    }

    data class KongJie(val kongIndex: Int, val jieIndex: Int)

    /** 火星铃星（按年支、时支）：申子辰人寅戌扬，寅午戌人丑卯方，巳酉丑人卯戌位，亥卯未人酉戌房 */
    fun getHuoLingIndex(earthlyBranchName: String, timeIndex: Int): HuoLing {
        var huoIndex = -1
        var lingIndex = -1
        val fixedTimeIndex = fixIndex(timeIndex)
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        when (earthlyBranch) {
            "yinEarthly", "wuEarthly", "xuEarthly" -> {
                huoIndex = fixEarthlyBranchIndex("chou") + fixedTimeIndex
                lingIndex = fixEarthlyBranchIndex("mao") + fixedTimeIndex
            }
            "shenEarthly", "ziEarthly", "chenEarthly" -> {
                huoIndex = fixEarthlyBranchIndex("yin") + fixedTimeIndex
                lingIndex = fixEarthlyBranchIndex("xu") + fixedTimeIndex
            }
            "siEarthly", "youEarthly", "chouEarthly" -> {
                huoIndex = fixEarthlyBranchIndex("mao") + fixedTimeIndex
                lingIndex = fixEarthlyBranchIndex("xu") + fixedTimeIndex
            }
            "haiEarthly", "weiEarthly", "maoEarthly" -> {
                huoIndex = fixEarthlyBranchIndex("you") + fixedTimeIndex
                lingIndex = fixEarthlyBranchIndex("xu") + fixedTimeIndex
            }
        }
        return HuoLing(fixIndex(huoIndex), fixIndex(lingIndex))
    }

    data class HuoLing(val huoIndex: Int, val lingIndex: Int)

    /** 红鸾天喜（按年支）：卯上起子逆数之，数到当生太岁支；对宫天喜 */
    fun getLuanXiIndex(earthlyBranchName: String): LuanXi {
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        val hongluanIndex = fixIndex(fixEarthlyBranchIndex("mao") - DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranch))
        val tianxiIndex = fixIndex(hongluanIndex + 6)
        return LuanXi(hongluanIndex, tianxiIndex)
    }

    data class LuanXi(val hongluanIndex: Int, val tianxiIndex: Int)

    /** 华盖咸池（按年支） */
    fun getHuagaiXianchiIndex(earthlyBranchName: String): HuaGaiXianChi {
        var hgIdx = -1
        var xcIdx = -1
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        when (earthlyBranch) {
            "yinEarthly", "wuEarthly", "xuEarthly" -> {
                hgIdx = fixEarthlyBranchIndex("xu"); xcIdx = fixEarthlyBranchIndex("mao")
            }
            "shenEarthly", "ziEarthly", "chenEarthly" -> {
                hgIdx = fixEarthlyBranchIndex("chen"); xcIdx = fixEarthlyBranchIndex("you")
            }
            "siEarthly", "youEarthly", "chouEarthly" -> {
                hgIdx = fixEarthlyBranchIndex("chou"); xcIdx = fixEarthlyBranchIndex("woo")
            }
            "haiEarthly", "weiEarthly", "maoEarthly" -> {
                hgIdx = fixEarthlyBranchIndex("wei"); xcIdx = fixEarthlyBranchIndex("zi")
            }
        }
        return HuaGaiXianChi(fixIndex(hgIdx), fixIndex(xcIdx))
    }

    data class HuaGaiXianChi(val huagaiIndex: Int, val xianchiIndex: Int)

    /** 孤辰寡宿（按年支）：寅卯辰年安巳丑，巳午未年安申辰，申酉戌年安亥未，亥子丑年安寅戌 */
    fun getGuGuaIndex(earthlyBranchName: String): GuGua {
        var guIdx = -1
        var guaIdx = -1
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        when (earthlyBranch) {
            "yinEarthly", "maoEarthly", "chenEarthly" -> {
                guIdx = fixEarthlyBranchIndex("si"); guaIdx = fixEarthlyBranchIndex("chou")
            }
            "siEarthly", "wuEarthly", "weiEarthly" -> {
                guIdx = fixEarthlyBranchIndex("shen"); guaIdx = fixEarthlyBranchIndex("chen")
            }
            "shenEarthly", "youEarthly", "xuEarthly" -> {
                guIdx = fixEarthlyBranchIndex("hai"); guaIdx = fixEarthlyBranchIndex("wei")
            }
            "haiEarthly", "ziEarthly", "chouEarthly" -> {
                guIdx = fixEarthlyBranchIndex("yin"); guaIdx = fixEarthlyBranchIndex("xu")
            }
        }
        return GuGua(fixIndex(guIdx), fixIndex(guaIdx))
    }

    data class GuGua(val guchenIndex: Int, val guasuIndex: Int)

    /** 劫杀（年支）：申子辰人蛇开口、亥卯未人猴速走、寅午戌人猪面黑、巳酉丑人虎咆哮 */
    fun getJieshaAdjIndex(earthlyBranchKey: String): Int = when (earthlyBranchKey) {
        "shenEarthly", "ziEarthly", "chenEarthly" -> 3
        "haiEarthly", "maoEarthly", "weiEarthly" -> 6
        "yinEarthly", "wuEarthly", "xuEarthly" -> 9
        else -> 0
    }

    /** 大耗（年支对冲，阳顺阴逆移一宫） */
    fun getDahaoIndex(earthlyBranchKey: String): Int {
        val matched = listOf(
            "weiEarthly", "wuEarthly", "youEarthly", "shenEarthly", "haiEarthly", "xuEarthly",
            "chouEarthly", "ziEarthly", "maoEarthly", "yinEarthly", "siEarthly", "chenEarthly",
        )[DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranchKey)]
        return fixIndex(DataTables.EARTHLY_BRANCHES.indexOf(matched) - 2)
    }

    /** 年系星索引（天才、天寿、天厨、破碎、蜚蠊、龙池、凤阁、天哭、天虚、天官、天福、天德、月德、天空、截路、空亡、旬空、劫杀、年解、大耗、天伤、天使） */
    fun getYearlyStarIndex(param: AstrolabeParam): YearlyStar {
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(param.solarDate, param.timeIndex, "normal", "normal")
        val (soulIndex, bodyIndex) = ZiweiPalace.getSoulAndBody(param)
        val heavenlyStem = I18nZh.kot(ganZhi.yearly[0], "Heavenly")
        val earthlyBranch = I18nZh.kot(ganZhi.yearly[1], "Earthly")
        val hsIdx = DataTables.HEAVENLY_STEMS.indexOf(heavenlyStem)
        val ebIdx = DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranch)

        val (huagaiIndex, xianchiIndex) = getHuagaiXianchiIndex(ganZhi.yearly[1])
        val (guchenIndex, guasuIndex) = getGuGuaIndex(ganZhi.yearly[1])
        val tiancaiIndex = fixIndex(soulIndex + ebIdx)
        val tianshouIndex = fixIndex(bodyIndex + ebIdx)
        val tianchuIndex = fixIndex(fixEarthlyBranchIndex(listOf("si", "woo", "zi", "si", "woo", "shen", "yin", "woo", "you", "hai")[hsIdx]))
        val posuiIndex = fixIndex(fixEarthlyBranchIndex(listOf("si", "chou", "you")[ebIdx % 3]))
        val feilianIndex = fixIndex(fixEarthlyBranchIndex(listOf("shen", "you", "xu", "si", "woo", "wei", "yin", "mao", "chen", "hai", "zi", "chou")[ebIdx]))
        val longchiIndex = fixIndex(fixEarthlyBranchIndex("chen") + ebIdx)
        val fenggeIndex = fixIndex(fixEarthlyBranchIndex("xu") - ebIdx)
        val tiankuIndex = fixIndex(fixEarthlyBranchIndex("woo") - ebIdx)
        val tianxuIndex = fixIndex(fixEarthlyBranchIndex("woo") + ebIdx)
        val tianguanIndex = fixIndex(fixEarthlyBranchIndex(listOf("wei", "chen", "si", "yin", "mao", "you", "hai", "you", "xu", "woo")[hsIdx]))
        val tianfuIndex = fixIndex(fixEarthlyBranchIndex(listOf("you", "shen", "zi", "hai", "mao", "yin", "woo", "si", "woo", "si")[hsIdx]))
        val tiandeIndex = fixIndex(fixEarthlyBranchIndex("you") + ebIdx)
        val yuedeIndex = fixIndex(fixEarthlyBranchIndex("si") + ebIdx)
        val tiankongIndex = fixIndex(fixEarthlyBranchIndex(ganZhi.yearly[1]) + 1)
        val jieluIndex = fixIndex(fixEarthlyBranchIndex(listOf("shen", "woo", "chen", "yin", "zi")[hsIdx % 5]))
        val kongwangIndex = fixIndex(fixEarthlyBranchIndex(listOf("you", "wei", "si", "mao", "chou")[hsIdx % 5]))
        var xunkongIndex = fixIndex(fixEarthlyBranchIndex(ganZhi.yearly[1]) + DataTables.HEAVENLY_STEMS.indexOf("guiHeavenly") - hsIdx + 1)

        val yinyang = ebIdx % 2
        if (yinyang != xunkongIndex % 2) {
            xunkongIndex = fixIndex(xunkongIndex + 1)
        }

        val jiekongIndex = if (yinyang == 0) jieluIndex else kongwangIndex
        val jieshaAdjIndex = getJieshaAdjIndex(earthlyBranch)
        val nianjieIndex = getNianjieIndex(ganZhi.yearly[1])
        val dahaoAdjIndex = getDahaoIndex(earthlyBranch)
        val (tianshiIndex, tianshangIndex) = getTianshiTianshangIndex(param.gender ?: "male", earthlyBranch, soulIndex)

        return YearlyStar(
            xianchiIndex, huagaiIndex, guchenIndex, guasuIndex, tiancaiIndex, tianshouIndex,
            tianchuIndex, posuiIndex, feilianIndex, longchiIndex, fenggeIndex, tiankuIndex,
            tianxuIndex, tianguanIndex, tianfuIndex, tiandeIndex, yuedeIndex, tiankongIndex,
            jieluIndex, kongwangIndex, xunkongIndex, tianshangIndex, tianshiIndex, jiekongIndex,
            jieshaAdjIndex, nianjieIndex, dahaoAdjIndex,
        )
    }

    data class YearlyStar(
        val xianchiIndex: Int, val huagaiIndex: Int, val guchenIndex: Int, val guasuIndex: Int,
        val tiancaiIndex: Int, val tianshouIndex: Int, val tianchuIndex: Int, val posuiIndex: Int,
        val feilianIndex: Int, val longchiIndex: Int, val fenggeIndex: Int, val tiankuIndex: Int,
        val tianxuIndex: Int, val tianguanIndex: Int, val tianfuIndex: Int, val tiandeIndex: Int,
        val yuedeIndex: Int, val tiankongIndex: Int, val jieluIndex: Int, val kongwangIndex: Int,
        val xunkongIndex: Int, val tianshangIndex: Int, val tianshiIndex: Int, val jiekongIndex: Int,
        val jieshaAdjIndex: Int, val nianjieIndex: Int, val dahaoAdjIndex: Int,
    )

    /** 天伤天使：天伤奴仆、天使疾厄。default 派别不互换（中州派阴男阳女才换） */
    fun getTianshiTianshangIndex(gender: String, earthlyBranch: String, soulIndex: Int): Pair<Int, Int> {
        val tianshangIndex = fixIndex(DataTables.PALACES.indexOf("friendsPalace") + soulIndex)
        val tianshiIndex = fixIndex(DataTables.PALACES.indexOf("healthPalace") + soulIndex)
        // algorithm == 'default': 无互换
        return Pair(tianshiIndex, tianshangIndex)
    }

    /** 年解（按年支）：解神从戌上起子，逆数至当生年太岁 */
    fun getNianjieIndex(earthlyBranchName: String): Int {
        val earthlyBranch = I18nZh.kot(earthlyBranchName, "Earthly")
        return fixIndex(
            fixEarthlyBranchIndex(
                listOf("xu", "you", "shen", "wei", "woo", "si", "chen", "mao", "yin", "chou", "zi", "hai")
                    [DataTables.EARTHLY_BRANCHES.indexOf(earthlyBranch)],
            ),
        )
    }

    /** 月系星（解神、天姚、天刑、阴煞、天月、天巫） */
    fun getMonthlyStarIndex(solarDate: String, timeIndex: Int, fixLeap: Boolean?): MonthlyStar {
        val monthIndex = fixLunarMonthIndex(solarDate, timeIndex, fixLeap)
        val jieshenIndex = fixIndex(fixEarthlyBranchIndex(listOf("shen", "xu", "zi", "yin", "chen", "woo")[Math.floorDiv(monthIndex, 2)]))
        val tianyaoIndex = fixIndex(fixEarthlyBranchIndex("chou") + monthIndex)
        val tianxingIndex = fixIndex(fixEarthlyBranchIndex("you") + monthIndex)
        val yinshaIndex = fixIndex(fixEarthlyBranchIndex(listOf("yin", "zi", "xu", "shen", "woo", "chen")[monthIndex % 6]))
        val tianyueIndex = fixIndex(fixEarthlyBranchIndex(listOf("xu", "si", "chen", "yin", "wei", "mao", "hai", "wei", "yin", "woo", "xu", "yin")[monthIndex]))
        val tianwuIndex = fixIndex(fixEarthlyBranchIndex(listOf("si", "shen", "yin", "hai")[monthIndex % 4]))
        return MonthlyStar(jieshenIndex, tianyaoIndex, tianxingIndex, yinshaIndex, tianyueIndex, tianwuIndex)
    }

    data class MonthlyStar(
        val yuejieIndex: Int, val tianyaoIndex: Int, val tianxingIndex: Int,
        val yinshaIndex: Int, val tianyueIndex: Int, val tianwuIndex: Int,
    )

    /** 流昌流曲（按大限/流年天干） */
    fun getChangQuIndexByHeavenlyStem(heavenlyStemName: String): ChangQu {
        var changIndex = -1
        var quIndex = -1
        val heavenlyStem = I18nZh.kot(heavenlyStemName, "Heavenly")
        when (heavenlyStem) {
            "jiaHeavenly" -> { changIndex = fixEarthlyBranchIndex("si"); quIndex = fixEarthlyBranchIndex("you") }
            "yiHeavenly" -> { changIndex = fixEarthlyBranchIndex("woo"); quIndex = fixEarthlyBranchIndex("shen") }
            "bingHeavenly", "wuHeavenly" -> { changIndex = fixEarthlyBranchIndex("shen"); quIndex = fixEarthlyBranchIndex("woo") }
            "dingHeavenly", "jiHeavenly" -> { changIndex = fixEarthlyBranchIndex("you"); quIndex = fixEarthlyBranchIndex("si") }
            "gengHeavenly" -> { changIndex = fixEarthlyBranchIndex("hai"); quIndex = fixEarthlyBranchIndex("mao") }
            "xinHeavenly" -> { changIndex = fixEarthlyBranchIndex("zi"); quIndex = fixEarthlyBranchIndex("yin") }
            "renHeavenly" -> { changIndex = fixEarthlyBranchIndex("yin"); quIndex = fixEarthlyBranchIndex("zi") }
            "guiHeavenly" -> { changIndex = fixEarthlyBranchIndex("mao"); quIndex = fixEarthlyBranchIndex("hai") }
        }
        return ChangQu(changIndex, quIndex)
    }
}
