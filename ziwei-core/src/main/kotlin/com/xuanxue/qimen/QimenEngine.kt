package com.xuanxue.qimen

import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar

/**
 * 时家奇门实验排盘引擎（Kotlin 实现）。
 *
 * 当前状态不是“完整黄金盘”：节气/局数、地盘、值符值使等部分正在逐层做来源夹具核验，
 * 天盘/门盘/神盘完整旋转仍保留实验性质。基础干支/节气/旬空由 lunar-java (MIT) 提供。
 *
 * 梁湘润《奇门遁甲入门》K2 source fixture 当前只对十八局甲子栏的值符星/值使门保存了
 * copyright-safe sparse anchors；通过这些 anchors 只能证明对应 lookup implementation fidelity，
 * 不能证明完整九宫正确，更不能证明预测有效。
 */
object QimenEngine {

    // 九宫洛书数序（飞布索引）：1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离
    val LUO_SHU = intArrayOf(1, 2, 3, 4, 5, 6, 7, 8, 9)

    // 九星原驻宫
    val STAR_HOME = mapOf(
        1 to "天蓬", 2 to "天芮", 3 to "天冲", 4 to "天辅", 5 to "天禽",
        6 to "天心", 7 to "天柱", 8 to "天任", 9 to "天英",
    )

    // 八门原驻宫。五中宫没有独立门位；中宫值班的值使身份另见 chiefIdentityForDunPalace。
    val GATE_HOME = mapOf(
        1 to "休门", 2 to "死门", 3 to "伤门", 4 to "杜门",
        6 to "开门", 7 to "惊门", 8 to "生门", 9 to "景门",
    )

    // 八神（当前实验实现：阳遁顺行，阴遁逆行）
    val SHEN = listOf("值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天")

    // 三奇六仪
    val YI = "戊己庚辛壬癸丁丙乙"

    // 六甲旬首 -> 遁干
    val XUN_DUN = mapOf("甲子" to "戊", "甲戌" to "己", "甲申" to "庚", "甲午" to "辛", "甲辰" to "壬", "甲寅" to "癸")

    data class JuRule(val yinYang: Int, val shang: Int, val zhong: Int, val xia: Int)

    // 二十四节气定局（上/中/下元局数）：阳遁(冬至起)、阴遁(夏至起)
    val JIE_QI_JU = mapOf(
        // 阳遁
        "冬至" to JuRule(1, 1, 7, 4), "小寒" to JuRule(1, 2, 8, 5), "大寒" to JuRule(1, 3, 9, 6),
        "立春" to JuRule(1, 8, 5, 2), "雨水" to JuRule(1, 9, 6, 3), "惊蛰" to JuRule(1, 1, 7, 4),
        "春分" to JuRule(1, 3, 9, 6), "清明" to JuRule(1, 4, 1, 7), "谷雨" to JuRule(1, 5, 2, 8),
        "立夏" to JuRule(1, 4, 1, 7), "小满" to JuRule(1, 5, 2, 8), "芒种" to JuRule(1, 6, 3, 9),
        // 阴遁
        "夏至" to JuRule(-1, 9, 3, 6), "小暑" to JuRule(-1, 8, 2, 5), "大暑" to JuRule(-1, 7, 1, 4),
        "立秋" to JuRule(-1, 2, 5, 8), "处暑" to JuRule(-1, 1, 4, 7), "白露" to JuRule(-1, 9, 3, 6),
        "秋分" to JuRule(-1, 7, 1, 4), "寒露" to JuRule(-1, 6, 9, 3), "霜降" to JuRule(-1, 5, 8, 2),
        "立冬" to JuRule(-1, 6, 9, 3), "小雪" to JuRule(-1, 5, 8, 2), "大雪" to JuRule(-1, 4, 7, 1),
    )

    data class Gong(
        val palace: Int,
        val diGan: String,
        val tianXing: String,
        val renMen: String,
        val shenPan: String,
        val isMaXing: Boolean = false,
        val isKong: Boolean = false,
    )

    data class QimenChart(
        val solarDate: String,
        val lunarDateStr: String,
        val yearGZ: String, val monthGZ: String, val dayGZ: String, val hourGZ: String,
        val jieQi: String,
        val yinYang: Int,
        val yuan: String,
        val ju: Int,
        val xunShou: String,
        val dunGan: String,
        val xunKong: List<String>,
        val zhiFu: String,
        val zhiShi: String,
        val gongs: List<Gong>,
        val maXing: String,
    ) {
        val juText: String get() = "${if (yinYang > 0) "阳" else "阴"}遁${ju}局 $yuan"
    }

    private fun seqOf(gan: String, zhi: String): Int {
        val g = "甲乙丙丁戊己庚辛壬癸".indexOf(gan)
        val z = "子丑寅卯辰巳午未申酉戌亥".indexOf(zhi)
        for (i in 0 until 60) {
            if (i % 10 == g && i % 12 == z) return i
        }
        return 0
    }

    private fun xunInfo(gz: String): Triple<String, String, List<String>> {
        val gan = gz[0].toString(); val zhi = gz[1].toString()
        val s = seqOf(gan, zhi)
        val base = (s / 10) * 10
        val xunShou = "甲乙丙丁戊己庚辛壬癸"[base % 10].toString() + "子丑寅卯辰巳午未申酉戌亥"[base % 12].toString()
        val dun = XUN_DUN[xunShou] ?: ""
        val kong = listOf(
            "子丑寅卯辰巳午未申酉戌亥"[(base + 10) % 12].toString(),
            "子丑寅卯辰巳午未申酉戌亥"[(base + 11) % 12].toString(),
        )
        return Triple(xunShou, dun, kong)
    }

    fun zhiPalace(zhi: String): Int = when (zhi) {
        "子" -> 1; "丑", "寅" -> 8; "卯" -> 3; "辰", "巳" -> 4; "午" -> 9
        "未", "申" -> 2; "酉" -> 7; "戌", "亥" -> 6; else -> 5
    }

    fun maXingOf(dayZhi: String): String = when (dayZhi) {
        "寅", "午", "戌" -> "申"; "申", "子", "辰" -> "寅"
        "巳", "酉", "丑" -> "亥"; "亥", "卯", "未" -> "巳"; else -> ""
    }

    fun yuanOf(dayGZ: String): String {
        val s = seqOf(dayGZ[0].toString(), dayGZ[1].toString())
        val fuTou = s - (s % 10)
        val ftGan = "甲乙丙丁戊己庚辛壬癸"[fuTou % 10].toString()
        val ftZhi = "子丑寅卯辰巳午未申酉戌亥"[fuTou % 12].toString()
        return when (ftGan + ftZhi) {
            "甲子", "甲午", "己卯", "己酉" -> "上元"
            "甲寅", "甲申", "己巳", "己亥" -> "中元"
            else -> "下元"
        }
    }

    /**
     * 构造当前实现的地盘三奇六仪。
     * 这是给 production bySolar 和 source-fixture implementation test 共用的单一路径，
     * 避免测试重写一份“看起来一样”的实现。
     */
    internal fun buildDiPan(yinYang: Int, ju: Int): Map<Int, String> {
        require(yinYang == 1 || yinYang == -1) { "yinYang must be 1 or -1" }
        require(ju in 1..9) { "ju must be 1..9" }

        val di = mutableMapOf<Int, String>()
        val startIdx = LUO_SHU.indexOf(ju)
        for (k in 0 until 9) {
            val yi = YI[k].toString()
            val pos = if (yinYang > 0) {
                LUO_SHU[(startIdx + k) % 9]
            } else {
                LUO_SHU[((startIdx - k) % 9 + 9) % 9]
            }
            di[pos] = yi
        }
        return di
    }

    /**
     * 遁干所在宫的值符星/值使门身份。
     *
     * 5 宫特例目前只在“值符/值使身份”层做 source-backed 处理：
     * - 梁湘润《奇门遁甲入门》十八局甲子 sparse fixture：五局 = 天禽 / 死；
     * - 善天道《奇门遁甲讲义》p19、p21-p22 的可见原页把五宫寄坤二宫、天禽并天芮、死门对应写在同一结构里。
     *
     * 这不等于完整门盘旋转已经验证，也不把“寄坤二宫”的所有后续算法自动推广为已证实规则。
     */
    internal fun chiefIdentityForDunPalace(dunPalace: Int): Pair<String, String> {
        require(dunPalace in 1..9) { "dunPalace must be 1..9" }
        val star = STAR_HOME[dunPalace] ?: ""
        val gate = if (dunPalace == 5) "死门" else (GATE_HOME[dunPalace] ?: "")
        return star to gate
    }

    fun bySolar(year: Int, month: Int, day: Int, hour: Int, minute: Int): QimenChart {
        val solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        val lunar: Lunar = solar.lunar
        val ec = lunar.eightChar

        val yearGZ = ec.getYearGan() + ec.getYearZhi()
        val monthGZ = ec.getMonthGan() + ec.getMonthZhi()
        val dayGZ = ec.getDayGan() + ec.getDayZhi()
        val hourGZ = ec.getTimeGan() + ec.getTimeZhi()

        val jieQi = runCatching { lunar.getPrevJieQi(true)?.name }.getOrNull()
            ?: runCatching { lunar.getPrevJieQi()?.name }.getOrNull()
            ?: "冬至"

        val rule = JIE_QI_JU[jieQi] ?: JuRule(1, 1, 7, 4)
        val yinYang = rule.yinYang
        val yuan = yuanOf(dayGZ)
        val ju = when (yuan) { "上元" -> rule.shang; "中元" -> rule.zhong; else -> rule.xia }

        val (xunShou, dunGan, xunKong) = xunInfo(hourGZ)

        val di = buildDiPan(yinYang, ju)

        // 值符值使：先定位遁干，再调用 source-bounded chief identity 规则。
        val dunPalace = di.entries.first { it.value == dunGan }.key
        val (zhiFu, zhiShi) = chiefIdentityForDunPalace(dunPalace)

        // 天盘：当前实验旋转实现，尚未由完整九宫黄金夹具证明。
        val shiGanPalace = di.entries.first { it.value == hourGZ[0].toString() }.key
        val tian = mutableMapOf<Int, String>()
        val starsByPalace = STAR_HOME.toSortedMap()
        val shift = (LUO_SHU.indexOf(shiGanPalace) - LUO_SHU.indexOf(dunPalace) + 9) % 9
        for (p in 1..9) {
            val srcIdx = LUO_SHU.indexOf(p)
            val newIdx = (srcIdx + shift) % 9
            val newP = LUO_SHU[newIdx]
            tian[newP] = starsByPalace[p] ?: ""
        }

        // 人盘：当前实验旋转实现；五中宫没有独立门位，完整八门转盘仍待 source-specific fixture。
        val shiZhiPalace = zhiPalace(hourGZ[1].toString())
        val men = mutableMapOf<Int, String>()
        val shift2 = (LUO_SHU.indexOf(shiZhiPalace) - LUO_SHU.indexOf(dunPalace) + 9) % 9
        for (p in 1..9) {
            val srcIdx = LUO_SHU.indexOf(p)
            val newIdx = (srcIdx + shift2) % 9
            val newP = LUO_SHU[newIdx]
            men[newP] = GATE_HOME[p] ?: ""
        }

        // 神盘：当前实验实现。值符落中宫时暂按既有寄坤二处理；尚未提升为 source-verified full-plate rule。
        val shen = mutableMapOf<Int, String>()
        val shenOrder = if (yinYang > 0) listOf(1, 2, 3, 4, 6, 7, 8, 9) else listOf(9, 8, 7, 6, 4, 3, 2, 1)
        val zhiFuStart = if (shiGanPalace == 5) 2 else shiGanPalace
        val startIdx = shenOrder.indexOf(zhiFuStart).coerceAtLeast(0)
        for (k in 0 until 8) {
            shen[shenOrder[(startIdx + k) % 8]] = SHEN[k]
        }

        val ma = maXingOf(dayGZ[1].toString())
        val maPalace = zhiPalace(ma)
        val kongPalaces = xunKong.map { zhiPalace(it) }

        val gongs = (1..9).map { p ->
            Gong(
                palace = p,
                diGan = di[p] ?: "",
                tianXing = tian[p] ?: "",
                renMen = men[p] ?: "",
                shenPan = shen[p] ?: "",
                isMaXing = p == maPalace,
                isKong = p in kongPalaces,
            )
        }

        return QimenChart(
            solarDate = "$year-$month-$day $hour:${"%02d".format(minute)}",
            lunarDateStr = lunar.toString(),
            yearGZ = yearGZ, monthGZ = monthGZ, dayGZ = dayGZ, hourGZ = hourGZ,
            jieQi = jieQi,
            yinYang = yinYang, yuan = yuan, ju = ju,
            xunShou = xunShou, dunGan = dunGan, xunKong = xunKong,
            zhiFu = zhiFu, zhiShi = zhiShi,
            gongs = gongs,
            maXing = ma,
        )
    }
}
