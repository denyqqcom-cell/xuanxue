package com.xuanxue.qimen

import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar

/**
 * 时家奇门实验排盘引擎（Kotlin 实现）。
 *
 * 当前状态不是“完整黄金盘”。默认 `LEGACY_EXPERIMENTAL` 保留既有行为；
 * `SHANTI_DAO_71_P21_P22` 是从善天道《奇门遁甲讲义71页》p21-p22
 * 两个 worked plate 独立原页复核后建立的窄范围 source-defined profile。
 *
 * Source Fidelity / Implementation Fidelity != Predictive Validity。
 */
object QimenEngine {

    enum class MethodProfile {
        LEGACY_EXPERIMENTAL,
        SHANTI_DAO_71_P21_P22,
    }

    // 九宫洛书数序（飞布索引）：1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离
    val LUO_SHU = intArrayOf(1, 2, 3, 4, 5, 6, 7, 8, 9)

    // 转盘外八宫几何顺时针序。不要与 1..9 飞布数序混为同一个对象。
    internal val ROTATION_RING = intArrayOf(1, 8, 3, 4, 9, 2, 7, 6)

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

    // 善天道 p21-p22 worked plates 使用的八神序列。
    val SHEN = listOf("值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天")

    // 善天道 p21-p22 的九星转盘把中五天禽寄随坤二天芮转动。
    // 这是 source-profile 表示，不把 p31/p55 的八神谱系冲突一并“解决”。
    internal val SHANTI_STAR_RING_HOME = mapOf(
        1 to "天蓬",
        8 to "天任",
        3 to "天冲",
        4 to "天辅",
        9 to "天英",
        2 to "天芮/天禽",
        7 to "天柱",
        6 to "天心",
    )

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
        val methodProfile: MethodProfile = MethodProfile.LEGACY_EXPERIMENTAL,
        val implementationWarnings: List<String> = emptyList(),
    ) {
        val juText: String get() = "${if (yinYang > 0) "阳" else "阴"}遁${ju}局 $yuan"
    }

    internal data class RotationLayers(
        val stars: Map<Int, String>,
        val doors: Map<Int, String>,
        val deities: Map<Int, String>,
        val warnings: List<String> = emptyList(),
    )

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

    /**
     * 地盘不直接出现甲；六甲以旬首遁干表示。
     * 因此遇到甲时，找“时干所在宫”必须先把甲解析为本旬遁干。
     * 这是输入表示层处理，不是对某一占断体系的优越性判断。
     */
    private fun representedHourStem(hourGZ: String, dunGan: String): String =
        if (hourGZ[0] == '甲') dunGan else hourGZ[0].toString()

    fun zhiPalace(zhi: String): Int = when (zhi) {
        "子" -> 1; "丑", "寅" -> 8; "卯" -> 3; "辰", "巳" -> 4; "午" -> 9
        "未", "申" -> 2; "酉" -> 7; "戌", "亥" -> 6; else -> 5
    }

    fun maXingOf(dayZhi: String): String = when (dayZhi) {
        "寅", "午", "戌" -> "申"; "申", "子", "辰" -> "寅"
        "巳", "酉", "丑" -> "亥"; "亥", "卯", "未" -> "巳"; else -> ""
    }

    /**
     * 既有 legacy 定元路径，保留用于向后兼容与 A/B。
     * 它不是善天道 p21-p22 worked examples 的 source-defined 符头算法。
     */
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
     * 善天道 71 页 p15-p18、p21-p22 所述符头定元：
     * 每五日以前一甲/己日为符头，再按符头地支分上中下元。
     *
     * Source fidelity only；没有因此证明此法预测更有效。
     */
    internal fun yuanOfFuTou(dayGZ: String): String {
        val s = seqOf(dayGZ[0].toString(), dayGZ[1].toString())
        val stemIndex = s % 10
        val offset = if (stemIndex <= 4) stemIndex else stemIndex - 5
        val fuTou = s - offset
        val ftZhi = "子丑寅卯辰巳午未申酉戌亥"[((fuTou % 12) + 12) % 12].toString()
        return when (ftZhi) {
            "子", "午", "卯", "酉" -> "上元"
            "寅", "申", "巳", "亥" -> "中元"
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
     * - 善天道《奇门遁甲讲义》p19、p21-p22 把五宫天禽寄坤二、死门为值使。
     *
     * 这不等于所有 full-plate hosting 规则已经验证。
     */
    internal fun chiefIdentityForDunPalace(dunPalace: Int): Pair<String, String> {
        require(dunPalace in 1..9) { "dunPalace must be 1..9" }
        val star = STAR_HOME[dunPalace] ?: ""
        val gate = if (dunPalace == 5) "死门" else (GATE_HOME[dunPalace] ?: "")
        return star to gate
    }

    private fun ringIndex(palace: Int): Int {
        val idx = ROTATION_RING.indexOf(palace)
        require(idx >= 0) { "palace $palace is not on the outer rotation ring" }
        return idx
    }

    private fun hostToKun(palace: Int): Int = if (palace == 5) 2 else palace

    private fun rotateRingMap(base: Map<Int, String>, fromPalace: Int, toPalace: Int): Map<Int, String> {
        val from = ringIndex(fromPalace)
        val to = ringIndex(toPalace)
        val shift = (to - from + ROTATION_RING.size) % ROTATION_RING.size
        return base.mapKeys { (p, _) ->
            val src = ringIndex(p)
            ROTATION_RING[(src + shift) % ROTATION_RING.size]
        }
    }

    private fun advanceNinePalaces(start: Int, signedSteps: Int): Int {
        val zero = start - 1
        return ((zero + signedSteps) % 9 + 9) % 9 + 1
    }

    /**
     * 善天道 p21-p22 worked plates 的窄范围 source-defined full-rotation profile。
     *
     * 关键对象分离：
     * - 地盘飞布：1..9 数序；
     * - 九星/八门转盘：外八宫几何环；
     * - 天禽随天芮寄坤二参与转盘；
     * - 六甲时的甲不直接出现在地盘，先以本旬遁干解析“时干所在宫”；
     * - 值使“随时宫”先按阴阳遁在 1..9 数序计时，再把值使门轮对齐目标外宫；
     * - 八神从大值符落宫起，阳顺/阴逆沿外八宫。
     *
     * 当值使计时结果正落中五宫时，p21-p22 没给出足以独立确定完整八门轮的 worked plate。
     * 此 profile 因此返回空门盘并显式 warning，而不是静默猜一个寄宫规则。
     */
    internal fun buildShantiandao71Layers(
        yinYang: Int,
        di: Map<Int, String>,
        hourGZ: String,
    ): RotationLayers {
        require(yinYang == 1 || yinYang == -1) { "yinYang must be 1 or -1" }
        require(hourGZ.length >= 2) { "hourGZ must contain stem and branch" }

        val (_, dunGan, _) = xunInfo(hourGZ)
        val dunPalace = di.entries.single { it.value == dunGan }.key
        val visibleHourStem = representedHourStem(hourGZ, dunGan)
        val shiGanPalace = di.entries.single { it.value == visibleHourStem }.key

        val starOrigin = hostToKun(dunPalace)
        val starTarget = hostToKun(shiGanPalace)
        val stars = rotateRingMap(SHANTI_STAR_RING_HOME, starOrigin, starTarget)

        val hourOffset = seqOf(hourGZ[0].toString(), hourGZ[1].toString()) % 10
        val doorTarget = advanceNinePalaces(dunPalace, yinYang * hourOffset)
        val warnings = mutableListOf<String>()
        val doors = if (doorTarget == 5) {
            warnings += "SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED"
            emptyMap()
        } else {
            val doorOrigin = hostToKun(dunPalace)
            rotateRingMap(GATE_HOME, doorOrigin, doorTarget)
        }

        val deities = mutableMapOf<Int, String>()
        val start = ringIndex(starTarget)
        val direction = if (yinYang > 0) 1 else -1
        for (k in SHEN.indices) {
            val idx = ((start + direction * k) % ROTATION_RING.size + ROTATION_RING.size) % ROTATION_RING.size
            deities[ROTATION_RING[idx]] = SHEN[k]
        }

        return RotationLayers(stars, doors, deities, warnings)
    }

    private fun buildLegacyLayers(
        yinYang: Int,
        di: Map<Int, String>,
        hourGZ: String,
        dunPalace: Int,
    ): RotationLayers {
        val (_, dunGan, _) = xunInfo(hourGZ)
        val visibleHourStem = representedHourStem(hourGZ, dunGan)
        val shiGanPalace = di.entries.first { it.value == visibleHourStem }.key

        // Legacy 天盘：数序平移。保留既有行为用于 A/B，不再把它叫 source-verified full rotation。
        val tian = mutableMapOf<Int, String>()
        val starsByPalace = STAR_HOME.toSortedMap()
        val shift = (LUO_SHU.indexOf(shiGanPalace) - LUO_SHU.indexOf(dunPalace) + 9) % 9
        for (p in 1..9) {
            val srcIdx = LUO_SHU.indexOf(p)
            val newIdx = (srcIdx + shift) % 9
            val newP = LUO_SHU[newIdx]
            tian[newP] = starsByPalace[p] ?: ""
        }

        // Legacy 人盘：地支宫位 + 数序平移。
        val shiZhiPalace = zhiPalace(hourGZ[1].toString())
        val men = mutableMapOf<Int, String>()
        val shift2 = (LUO_SHU.indexOf(shiZhiPalace) - LUO_SHU.indexOf(dunPalace) + 9) % 9
        for (p in 1..9) {
            val srcIdx = LUO_SHU.indexOf(p)
            val newIdx = (srcIdx + shift2) % 9
            val newP = LUO_SHU[newIdx]
            men[newP] = GATE_HOME[p] ?: ""
        }

        // Legacy 神盘：保留既有实现用于对照。
        val shen = mutableMapOf<Int, String>()
        val shenOrder = if (yinYang > 0) listOf(1, 2, 3, 4, 6, 7, 8, 9) else listOf(9, 8, 7, 6, 4, 3, 2, 1)
        val zhiFuStart = if (shiGanPalace == 5) 2 else shiGanPalace
        val startIdx = shenOrder.indexOf(zhiFuStart).coerceAtLeast(0)
        for (k in 0 until 8) {
            shen[shenOrder[(startIdx + k) % 8]] = SHEN[k]
        }

        return RotationLayers(tian, men, shen)
    }

    fun bySolar(year: Int, month: Int, day: Int, hour: Int, minute: Int): QimenChart =
        bySolar(year, month, day, hour, minute, MethodProfile.LEGACY_EXPERIMENTAL)

    fun bySolar(
        year: Int,
        month: Int,
        day: Int,
        hour: Int,
        minute: Int,
        methodProfile: MethodProfile,
    ): QimenChart {
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
        val yuan = when (methodProfile) {
            MethodProfile.LEGACY_EXPERIMENTAL -> yuanOf(dayGZ)
            MethodProfile.SHANTI_DAO_71_P21_P22 -> yuanOfFuTou(dayGZ)
        }
        val ju = when (yuan) { "上元" -> rule.shang; "中元" -> rule.zhong; else -> rule.xia }

        val (xunShou, dunGan, xunKong) = xunInfo(hourGZ)

        val di = buildDiPan(yinYang, ju)

        val dunPalace = di.entries.first { it.value == dunGan }.key
        val (zhiFu, zhiShi) = chiefIdentityForDunPalace(dunPalace)

        val layers = when (methodProfile) {
            MethodProfile.LEGACY_EXPERIMENTAL -> buildLegacyLayers(yinYang, di, hourGZ, dunPalace)
            MethodProfile.SHANTI_DAO_71_P21_P22 -> buildShantiandao71Layers(yinYang, di, hourGZ)
        }

        val ma = maXingOf(dayGZ[1].toString())
        val maPalace = zhiPalace(ma)
        val kongPalaces = xunKong.map { zhiPalace(it) }

        val gongs = (1..9).map { p ->
            Gong(
                palace = p,
                diGan = di[p] ?: "",
                tianXing = layers.stars[p] ?: "",
                renMen = layers.doors[p] ?: "",
                shenPan = layers.deities[p] ?: "",
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
            methodProfile = methodProfile,
            implementationWarnings = layers.warnings,
        )
    }
}
