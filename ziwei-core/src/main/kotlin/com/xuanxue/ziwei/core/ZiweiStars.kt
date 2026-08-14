package com.xuanxue.ziwei.core

import com.xuanxue.ziwei.gen.DataTables
import com.xuanxue.ziwei.gen.EARTHLY_BRANCH_INFO
import com.xuanxue.ziwei.gen.I18nZh
import com.xuanxue.ziwei.core.ZiweiUtils.fixEarthlyBranchIndex
import com.xuanxue.ziwei.core.ZiweiUtils.fixIndex
import com.xuanxue.ziwei.core.ZiweiUtils.getBrightness
import com.xuanxue.ziwei.core.ZiweiUtils.getMutagen
import com.xuanxue.ziwei.core.ZiweiLocation.AstrolabeParam
import com.xuanxue.ziwei.core.ZiweiLocation.getStartIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getLuYangTuoMaIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getKuiYueIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getZuoYouIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getChangQuIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getHuoLingIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getKongJieIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getDailyStarIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getTimelyStarIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getLuanXiIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getYearlyStarIndex
import com.xuanxue.ziwei.core.ZiweiLocation.getMonthlyStarIndex

/**
 * Port of iztro src/star (MIT, SylarLong) — 安星.
 */
object ZiweiStars {

    data class Star(
        val name: String,
        val type: String,
        val scope: String,
        val brightness: String = "",
        val mutagen: String = "",
    )

    fun initStars(): MutableList<MutableList<Star>> =
        MutableList(12) { mutableListOf() }

    private fun star(nameKey: String, type: String, scope: String = "origin", brightness: String = "", mutagen: String = ""): Star =
        Star(I18nZh.t(nameKey), type, scope, brightness, mutagen)

    /**
     * 安十四主星. 紫微逆去天机星，隔一太阳武曲辰，连接天同空二宫，廉贞居处方是真。
     * 天府顺行有太阴，贪狼而后巨门临，随来天相天梁继，七杀空三是破军。
     */
    fun getMajorStar(param: AstrolabeParam): MutableList<MutableList<Star>> {
        val (ziweiIndex, tianfuIndex) = getStartIndex(param)
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(param.solarDate, param.timeIndex, "normal", "normal")
        val stars = initStars()

        val ziweiGroup = listOf("ziweiMaj", "tianjiMaj", "", "taiyangMaj", "wuquMaj", "tiantongMaj", "", "", "lianzhenMaj")
        val tianfuGroup = listOf("tianfuMaj", "taiyinMaj", "tanlangMaj", "jumenMaj", "tianxiangMaj", "tianliangMaj", "qishaMaj", "", "", "", "pojunMaj")

        ziweiGroup.forEachIndexed { i, s ->
            if (s.isNotEmpty()) {
                val idx = fixIndex(ziweiIndex - i)
                stars[idx].add(star(s, "major", brightness = getBrightness(I18nZh.t(s), idx), mutagen = getMutagen(I18nZh.t(s), ganZhi.yearly[0])))
            }
        }
        tianfuGroup.forEachIndexed { i, s ->
            if (s.isNotEmpty()) {
                val idx = fixIndex(tianfuIndex + i)
                stars[idx].add(star(s, "major", brightness = getBrightness(I18nZh.t(s), idx), mutagen = getMutagen(I18nZh.t(s), ganZhi.yearly[0])))
            }
        }
        return stars
    }

    /** 安 14 辅星 */
    fun getMinorStar(solarDateStr: String, timeIndex: Int, fixLeap: Boolean?): MutableList<MutableList<Star>> {
        val stars = initStars()
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(solarDateStr, timeIndex, "normal", "normal")
        val monthIndex = ZiweiUtils.fixLunarMonthIndex(solarDateStr, timeIndex, fixLeap)

        val (zuoIndex, youIndex) = getZuoYouIndex(monthIndex + 1)
        val (changIndex, quIndex) = getChangQuIndex(timeIndex)
        val (kuiIndex, yueIndex) = getKuiYueIndex(ganZhi.yearly[0])
        val (huoIndex, lingIndex) = getHuoLingIndex(ganZhi.yearly[1], timeIndex)
        val (kongIndex, jieIndex) = getKongJieIndex(timeIndex)
        val (luIndex, maIndex, yangIndex, tuoIndex) = getLuYangTuoMaIndex(ganZhi.yearly[0], ganZhi.yearly[1])

        stars[zuoIndex].add(star("zuofuMin", "soft", brightness = getBrightness("左辅", zuoIndex), mutagen = getMutagen("左辅", ganZhi.yearly[0])))
        stars[youIndex].add(star("youbiMin", "soft", brightness = getBrightness("右弼", youIndex), mutagen = getMutagen("右弼", ganZhi.yearly[0])))
        stars[changIndex].add(star("wenchangMin", "soft", brightness = getBrightness("文昌", changIndex), mutagen = getMutagen("文昌", ganZhi.yearly[0])))
        stars[quIndex].add(star("wenquMin", "soft", brightness = getBrightness("文曲", quIndex), mutagen = getMutagen("文曲", ganZhi.yearly[0])))
        stars[kuiIndex].add(star("tiankuiMin", "soft", brightness = getBrightness("天魁", kuiIndex)))
        stars[yueIndex].add(star("tianyueMin", "soft", brightness = getBrightness("天钺", yueIndex)))
        stars[luIndex].add(star("lucunMin", "lucun", brightness = getBrightness("禄存", luIndex)))
        stars[maIndex].add(star("tianmaMin", "tianma", brightness = getBrightness("天马", maIndex)))
        stars[kongIndex].add(star("dikongMin", "tough", brightness = getBrightness("地空", kongIndex)))
        stars[jieIndex].add(star("dijieMin", "tough", brightness = getBrightness("地劫", jieIndex)))
        stars[huoIndex].add(star("huoxingMin", "tough", brightness = getBrightness("火星", huoIndex)))
        stars[lingIndex].add(star("lingxingMin", "tough", brightness = getBrightness("铃星", lingIndex)))
        stars[yangIndex].add(star("qingyangMin", "tough", brightness = getBrightness("擎羊", yangIndex)))
        stars[tuoIndex].add(star("tuoluoMin", "tough", brightness = getBrightness("陀罗", tuoIndex)))

        return stars
    }

    /** 安杂耀（38 颗，default 派别） */
    fun getAdjectiveStar(param: AstrolabeParam): MutableList<MutableList<Star>> {
        val stars = initStars()
        val yearlyIndex = getYearlyStarIndex(param)
        val monthlyIndex = getMonthlyStarIndex(param.solarDate, param.timeIndex, param.fixLeap)
        val dailyIndex = getDailyStarIndex(param.solarDate, param.timeIndex, param.fixLeap)
        val timelyIndex = getTimelyStarIndex(param.timeIndex)
        val (hongluanIndex, tianxiIndex) = getLuanXiIndex(ganZhiYearlyBranch(param))

        stars[hongluanIndex].add(star("hongluan", "flower"))
        stars[tianxiIndex].add(star("tianxi", "flower"))
        stars[monthlyIndex.tianyaoIndex].add(star("tianyao", "flower"))
        stars[yearlyIndex.xianchiIndex].add(star("xianchi", "flower"))
        stars[monthlyIndex.yuejieIndex].add(star("jieshen", "helper"))
        stars[dailyIndex.santaiIndex].add(star("santai", "adjective"))
        stars[dailyIndex.bazuoIndex].add(star("bazuo", "adjective"))
        stars[dailyIndex.enguangIndex].add(star("engguang", "adjective"))
        stars[dailyIndex.tianguiIndex].add(star("tiangui", "adjective"))
        stars[yearlyIndex.longchiIndex].add(star("longchi", "adjective"))
        stars[yearlyIndex.fenggeIndex].add(star("fengge", "adjective"))
        stars[yearlyIndex.tiancaiIndex].add(star("tiancai", "adjective"))
        stars[yearlyIndex.tianshouIndex].add(star("tianshou", "adjective"))
        stars[timelyIndex.taifuIndex].add(star("taifu", "adjective"))
        stars[timelyIndex.fenggaoIndex].add(star("fenggao", "adjective"))
        stars[monthlyIndex.tianwuIndex].add(star("tianwu", "adjective"))
        stars[yearlyIndex.huagaiIndex].add(star("huagai", "adjective"))
        stars[yearlyIndex.tianguanIndex].add(star("tianguan", "adjective"))
        stars[yearlyIndex.tianfuIndex].add(star("tianfu", "adjective"))
        stars[yearlyIndex.tianchuIndex].add(star("tianchu", "adjective"))
        stars[monthlyIndex.tianyueIndex].add(star("tianyue", "adjective"))
        stars[yearlyIndex.tiandeIndex].add(star("tiande", "adjective"))
        stars[yearlyIndex.yuedeIndex].add(star("yuede", "adjective"))
        stars[yearlyIndex.tiankongIndex].add(star("tiankong", "adjective"))
        stars[yearlyIndex.xunkongIndex].add(star("xunkong", "adjective"))
        stars[yearlyIndex.jieluIndex].add(star("jielu", "adjective"))
        stars[yearlyIndex.kongwangIndex].add(star("kongwang", "adjective"))
        stars[yearlyIndex.guchenIndex].add(star("guchen", "adjective"))
        stars[yearlyIndex.guasuIndex].add(star("guasu", "adjective"))
        stars[yearlyIndex.feilianIndex].add(star("feilian", "adjective"))
        stars[yearlyIndex.posuiIndex].add(star("posui", "adjective"))
        stars[monthlyIndex.tianxingIndex].add(star("tianxing", "adjective"))
        stars[monthlyIndex.yinshaIndex].add(star("yinsha", "adjective"))
        stars[yearlyIndex.tiankuIndex].add(star("tianku", "adjective"))
        stars[yearlyIndex.tianxuIndex].add(star("tianxu", "adjective"))
        stars[yearlyIndex.tianshiIndex].add(star("tianshi", "adjective"))
        stars[yearlyIndex.tianshangIndex].add(star("tianshang", "adjective"))
        stars[yearlyIndex.nianjieIndex].add(star("nianjie", "helper"))

        return stars
    }

    private fun ganZhiYearlyBranch(param: AstrolabeParam): String =
        LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(param.solarDate, param.timeIndex, "normal", "normal").yearly[1]

    /** 长生 12 神 */
    fun getChangesheng12StartIndex(fiveElementClassName: String): Int {
        val fiveElementClass = I18nZh.kot(fiveElementClassName)
        val v = DataTables.FIVE_ELEMENTS_VALUE[fiveElementClass]
        return when (v) {
            2 -> fixEarthlyBranchIndex("shen")
            3 -> fixEarthlyBranchIndex("hai")
            4 -> fixEarthlyBranchIndex("si")
            5 -> fixEarthlyBranchIndex("shen")
            6 -> fixEarthlyBranchIndex("yin")
            else -> 0
        }
    }

    fun getChangsheng12(param: AstrolabeParam): List<String> {
        val changsheng12 = MutableList(12) { "" }
        val genderKey = I18nZh.kot(param.gender ?: "male")
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(param.solarDate, 0, "normal", "normal")
        val earthlyBranchOfYear = I18nZh.kot(ganZhi.yearly[1], "Earthly")
        val sab = ZiweiPalace.getSoulAndBody(param)
        val fiveElementClass = ZiweiPalace.getFiveElementsClass(sab.heavenlyStemOfSoul, sab.earthlyBranchOfSoul)
        val stars = listOf("changsheng", "muyu", "guandai", "linguan", "diwang", "shuai", "bing", "si", "mu", "jue", "tai", "yang")
        val startIdx = getChangesheng12StartIndex(fiveElementClass)
        val yinYangOfYear = EARTHLY_BRANCH_INFO[earthlyBranchOfYear]?.yinYang ?: "阳"

        for (i in stars.indices) {
            val idx = if (DataTables.GENDER[genderKey] == yinYangOfYear) {
                fixIndex(i + startIdx)
            } else {
                fixIndex(startIdx - i)
            }
            changsheng12[idx] = I18nZh.t(stars[i])
        }
        return changsheng12
    }

    /** 博士 12 神（从禄存起，阳男阴女顺行） */
    fun getBoShi12(solarDateStr: String, gender: String): List<String> {
        val genderKey = I18nZh.kot(gender)
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(solarDateStr, 0, "normal", "normal")
        val earthlyBranchOfYear = I18nZh.kot(ganZhi.yearly[1], "Earthly")
        val stars = listOf("boshi", "lishi", "qinglong", "xiaohao", "jiangjun", "zhoushu", "faylian", "xishen", "bingfu", "dahao", "fubing", "guanfu")
        val (luIndex, _, _, _) = getLuYangTuoMaIndex(ganZhi.yearly[0], ganZhi.yearly[1])
        val boshi12 = MutableList(12) { "" }
        val yinYangOfYear = EARTHLY_BRANCH_INFO[earthlyBranchOfYear]?.yinYang ?: "阳"

        for (i in stars.indices) {
            val idx = if (DataTables.GENDER[genderKey] == yinYangOfYear) fixIndex(luIndex + i) else fixIndex(luIndex - i)
            boshi12[idx] = I18nZh.t(stars[i])
        }
        return boshi12
    }

    /** 流年岁前 12 神 + 将前 12 神（default 派别） */
    fun getYearly12(solarDateStr: String): Pair<List<String>, List<String>> {
        val jiangqian12 = MutableList(12) { "" }
        val suiqian12 = MutableList(12) { "" }
        val ganZhi = LunarAdapter.getHeavenlyStemAndEarthlyBranchBySolarDate(solarDateStr, 0, "normal", "normal")

        val ts12shen = listOf("suijian", "huiqi", "sangmen", "guansuo", "gwanfu", "xiaohao", "dahao", "longde", "baihu", "tiande", "diaoke", "bingfu")
        for (i in ts12shen.indices) {
            val idx = fixIndex(fixEarthlyBranchIndex(ganZhi.yearly[1]) + i)
            suiqian12[idx] = I18nZh.t(ts12shen[i])
        }

        val jq12shen = listOf("jiangxing", "panan", "suiyi", "xiishen", "huagai", "jiesha", "zhaisha", "tiansha", "zhibei", "xianchi", "yuesha", "wangshen")
        val jiangqian12StartIndex = getJiangqian12StartIndex(ganZhi.yearly[1])
        for (i in jq12shen.indices) {
            val idx = fixIndex(jiangqian12StartIndex + i)
            jiangqian12[idx] = I18nZh.t(jq12shen[i])
        }

        return Pair(suiqian12, jiangqian12)
    }

    fun getJiangqian12StartIndex(earthlyBranchName: String): Int {
        var jqStartIdx = -1
        val earthlyBranchOfYear = I18nZh.kot(earthlyBranchName, "Earthly")
        when (earthlyBranchOfYear) {
            "yinEarthly", "wuEarthly", "xuEarthly" -> jqStartIdx = fixEarthlyBranchIndex("woo")
            "shenEarthly", "ziEarthly", "chenEarthly" -> jqStartIdx = fixEarthlyBranchIndex("zi")
            "siEarthly", "youEarthly", "chouEarthly" -> jqStartIdx = fixEarthlyBranchIndex("you")
            "haiEarthly", "maoEarthly", "weiEarthly" -> jqStartIdx = fixEarthlyBranchIndex("mao")
        }
        return fixIndex(jqStartIdx)
    }
}
