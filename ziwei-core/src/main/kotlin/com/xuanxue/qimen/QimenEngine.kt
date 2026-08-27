package com.xuanxue.qimen

import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar

/**
 * 转盘时家奇门排盘引擎（Kotlin 实现）。
 *
 * 规则来源（handoff/qimen/03_RULES.jsonl + 04_CONFLICTS.md）：
 * - R-YI-001  地盘九仪 戊己庚辛壬癸丁丙乙，戊起局数宫，阳遁顺飞/阴遁逆飞（数字飞泊）
 * - R-SKY-001 值符星移到"时干"（时干为甲 -> 旬首遁干）所在宫；天禽寄坤2
 * - R-GATE-HOME 5宫无门，寄坤2；值使门随时支（阳顺阴逆，环序）
 * - R-SPIRIT-001 神盘：小值符随值符星宫，阳遁顺/阴遁逆（环序）
 * - R-JU-001/002/003 定元方法必须显式区分；未重建的方法 fail closed
 * - R-HIT-XING 六仪击刑：戊3 己2 庚8 辛9 壬4 癸4
 * - R-WUBU-001 五不遇时：时干克日干、同阴阳、干序相隔五位（fixtures 含 甲/庚、己/乙）
 * - R-QL-001 青龙返首：天盘甲/戊 加 地盘丙（一别名族）
 *
 * 重要边界：handoff 当前没有完整九宫黄金盘，且地/天/人/神盘仍有来源冲突。
 * 因此完整盘面与由盘面派生的格局仍属于实验实现；结构测试不等于完整九宫已核验。
 */
object QimenEngine {

    /** 洛书飞泊序（地盘九仪用，数字序）。 */
    val LUO_SHU = intArrayOf(1, 2, 3, 4, 5, 6, 7, 8, 9)

    /** 物理环序：顺时针绕九宫（坎1→艮8→震3→巽4→离9→坤2→兑7→乾6）。 */
    val RING = intArrayOf(1, 8, 3, 4, 9, 2, 7, 6)

    val STAR_HOME = mapOf(
        1 to "天蓬", 2 to "天芮", 3 to "天冲", 4 to "天辅", 5 to "天禽",
        6 to "天心", 7 to "天柱", 8 to "天任", 9 to "天英",
    )

    val GATE_HOME = mapOf(
        1 to "休门", 2 to "死门", 3 to "伤门", 4 to "杜门",
        6 to "开门", 7 to "惊门", 8 to "生门", 9 to "景门",
    )

    val SHEN = listOf("值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天")
    val YI = "戊己庚辛壬癸丁丙乙"

    val XUN_DUN = mapOf(
        "甲子" to "戊", "甲戌" to "己", "甲申" to "庚",
        "甲午" to "辛", "甲辰" to "壬", "甲寅" to "癸",
    )

    val HIT_XING = mapOf("戊" to 3, "己" to 2, "庚" to 8, "辛" to 9, "壬" to 4, "癸" to 4)

    /** 定元方法身份必须显式；存在身份不代表每种方法已经可执行。 */
    enum class JuMethod {
        CHAI_BU_DAYCOUNT,
        CHAI_BU_FUTOU,
        ZHI_RUN,
    }

    data class JuRule(val yinYang: Int, val shang: Int, val zhong: Int, val xia: Int)

    val JIE_QI_JU = mapOf(
        "冬至" to JuRule(1, 1, 7, 4), "小寒" to JuRule(1, 2, 8, 5), "大寒" to JuRule(1, 3, 9, 6),
        "立春" to JuRule(1, 8, 5, 2), "雨水" to JuRule(1, 9, 6, 3), "惊蛰" to JuRule(1, 1, 7, 4),
        "春分" to JuRule(1, 3, 9, 6), "清明" to JuRule(1, 4, 1, 7), "谷雨" to JuRule(1, 5, 2, 8),
        "立夏" to JuRule(1, 4, 1, 7), "小满" to JuRule(1, 5, 2, 8), "芒种" to JuRule(1, 6, 3, 9),
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
        val isDayKong: Boolean = false,
        val isHourKong: Boolean = false,
        val isJiXing: Boolean = false,
    ) {
        /** 仅供旧 UI 兼容；业务逻辑必须优先区分日空/时空。 */
        val isKong: Boolean get() = isDayKong || isHourKong
    }

    data class QimenChart(
        val solarDate: String,
        val lunarDateStr: String,
        val yearGZ: String,
        val monthGZ: String,
        val dayGZ: String,
        val hourGZ: String,
        val jieQi: String,
        val yinYang: Int,
        val yuan: String,
        val ju: Int,
        val juMethod: String,
        val xunShou: String,
        val dunGan: String,
        val dayKong: List<String>,
        val hourKong: List<String>,
        val zhiFu: String,
        val zhiShi: String,
        val gongs: List<Gong>,
        val maXing: String,
        val isWuBuYu: Boolean,
        val patterns: List<String>,
        val juMethodUsed: String = "CHAI_BU_DAYCOUNT",
        val jieqiDayIndex: Int = 0,
        val yuanFutou: String = "",
    ) {
        val juText: String get() = "${if (yinYang > 0) "阳" else "阴"}遁${ju}局 $yuan"

        /** 旧字段语义等同“时旬空”，保留只为现有解释层兼容；不得再拿它代表日空。 */
        @Deprecated("Use dayKong/hourKong explicitly")
        val xunKong: List<String> get() = hourKong
    }

    /** 兼容旧 API：符头定元。 */
    fun yuanOf(dayGZ: String): String = yuanOfFutou(dayGZ)

    private fun seqOf(gan: String, zhi: String): Int {
        val g = "甲乙丙丁戊己庚辛壬癸".indexOf(gan)
        val z = "子丑寅卯辰巳午未申酉戌亥".indexOf(zhi)
        require(g >= 0 && z >= 0) { "invalid gan-zhi: $gan$zhi" }
        for (i in 0 until 60) {
            if (i % 10 == g && i % 12 == z) return i
        }
        error("invalid sexagenary pair: $gan$zhi")
    }

    private fun xunInfo(gz: String): Triple<String, String, List<String>> {
        require(gz.length >= 2) { "invalid gan-zhi: $gz" }
        val s = seqOf(gz[0].toString(), gz[1].toString())
        val base = (s / 10) * 10
        val gan = "甲乙丙丁戊己庚辛壬癸"
        val zhi = "子丑寅卯辰巳午未申酉戌亥"
        val xunShou = gan[base % 10].toString() + zhi[base % 12].toString()
        val dun = XUN_DUN[xunShou] ?: error("missing xun dun for $xunShou")
        val kong = listOf(zhi[(base + 10) % 12].toString(), zhi[(base + 11) % 12].toString())
        return Triple(xunShou, dun, kong)
    }

    fun zhiPalace(zhi: String): Int = when (zhi) {
        "子" -> 1
        "丑", "寅" -> 8
        "卯" -> 3
        "辰", "巳" -> 4
        "午" -> 9
        "未", "申" -> 2
        "酉" -> 7
        "戌", "亥" -> 6
        else -> 5
    }

    /** 时家奇门的驿马输入为占时支；函数本身只做三合局冲映射。 */
    fun maXingOf(zhi: String): String = when (zhi) {
        "寅", "午", "戌" -> "申"
        "申", "子", "辰" -> "寅"
        "巳", "酉", "丑" -> "亥"
        "亥", "卯", "未" -> "巳"
        else -> ""
    }

    /**
     * 拆补“五日符头”：每元第一日必为甲日或己日，向前回溯到最近的甲/己日。
     * 这与 xunInfo() 使用的十干支“六甲旬首”不是同一对象，禁止混用。
     */
    fun yuanOfFutou(dayGZ: String): String {
        val s = seqOf(dayGZ[0].toString(), dayGZ[1].toString())
        val fuTou = s - (s % 5)
        val gan = "甲乙丙丁戊己庚辛壬癸"
        val zhi = "子丑寅卯辰巳午未申酉戌亥"
        val ft = gan[fuTou % 10].toString() + zhi[fuTou % 12].toString()
        return when (ft) {
            "甲子", "甲午", "己卯", "己酉" -> "上元"
            "甲寅", "甲申", "己巳", "己亥" -> "中元"
            else -> "下元"
        }
    }

    /** 节气内第几天（1 起，交节当天=1）；失败返回 0，调用方必须 fail closed。 */
    fun jieqiDayIndexOf(lunar: Lunar): Int = runCatching {
        val cur = lunar.solar
        val cur12 = Solar.fromYmdHms(cur.year, cur.month, cur.day, 12, 0, 0)
        // Must use the same 24-term boundary family as bySolar(). Using getPrevJie()
        // skips 中气 such as 冬至/处暑 and can make the day index disagree with jieQi.
        val ps = lunar.getPrevJieQi(true)?.solar ?: return@runCatching 0
        val prevNoon = Solar.fromYmdHms(ps.year, ps.month, ps.day, 12, 0, 0)
        (cur12.getJulianDay() - prevNoon.getJulianDay()).toInt() + 1
    }.getOrDefault(0)

    private fun yuanOfDayCount(lunar: Lunar): String = yuanByDayCount(jieqiDayIndexOf(lunar))

    /** R-JU-001 只明确给出 1..15；0 或 >15 不猜测。 */
    fun yuanByDayCount(dayIndex: Int): String = when (dayIndex) {
        in 1..5 -> "上元"
        in 6..10 -> "中元"
        in 11..15 -> "下元"
        else -> throw IllegalArgumentException("CHAI_BU_DAYCOUNT dayIndex must be 1..15, got $dayIndex")
    }

    /**
     * 五不遇时 generator。
     * 现有 fixtures 明确给出 甲日庚午、己日乙亥为 true；十干按阴阳同性且 hourGan 克 dayGan
     * 可归一为 hour index = day index + 6 (mod 10)。
     */
    internal fun isWuBuYuStemPair(dayGan: Char, hourGan: Char): Boolean {
        val gan = "甲乙丙丁戊己庚辛壬癸"
        val d = gan.indexOf(dayGan)
        val h = gan.indexOf(hourGan)
        if (d < 0 || h < 0) return false
        return d % 2 == h % 2 && (h - d + 10) % 10 == 6
    }

    private fun isWuBuYuShi(dayGZ: String, hourGZ: String): Boolean =
        dayGZ.isNotEmpty() && hourGZ.isNotEmpty() && isWuBuYuStemPair(dayGZ[0], hourGZ[0])

    /** 默认只执行当前可编码的 CHAI_BU_DAYCOUNT；其他方法身份保留但必须显式选择。 */
    fun bySolar(
        year: Int,
        month: Int,
        day: Int,
        hour: Int,
        minute: Int,
        juMethod: JuMethod = JuMethod.CHAI_BU_DAYCOUNT,
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
            ?: error("cannot resolve jieqi")

        val rule = JIE_QI_JU[jieQi] ?: error("unsupported jieqi: $jieQi")
        val yinYang = rule.yinYang
        val yuan = when (juMethod) {
            JuMethod.CHAI_BU_DAYCOUNT -> yuanOfDayCount(lunar)
            JuMethod.CHAI_BU_FUTOU -> yuanOfFutou(dayGZ)
            JuMethod.ZHI_RUN -> throw UnsupportedOperationException(
                "ZHI_RUN is not rebuilt/fixture-verified; do not substitute FUTOU as an approximation",
            )
        }
        val ju = when (yuan) {
            "上元" -> rule.shang
            "中元" -> rule.zhong
            else -> rule.xia
        }

        val (xunShou, dunGan, hourKong) = xunInfo(hourGZ)
        val (_, _, dayKong) = xunInfo(dayGZ)

        val di = mutableMapOf<Int, String>()
        for (k in 0 until 9) {
            val yi = YI[k].toString()
            val idx = LUO_SHU.indexOf(ju)
            val pos = if (yinYang > 0) LUO_SHU[(idx + k) % 9]
            else LUO_SHU[((idx - k) % 9 + 9) % 9]
            di[pos] = yi
        }

        val dunPalace = di.entries.first { it.value == dunGan }.key
        val zhiFu = STAR_HOME[dunPalace] ?: ""
        val zhiShi = if (dunPalace == 5) GATE_HOME[2]!! else GATE_HOME[dunPalace] ?: ""

        val shiGanOrDun = if (hourGZ[0] == '甲') dunGan else hourGZ[0].toString()
        val shiGanPalace = di.entries.first { it.value == shiGanOrDun }.key
        val zhiFuPalace = if (shiGanPalace == 5) 2 else shiGanPalace

        val ring = RING.toList()
        val starsOnRing = ring.map { STAR_HOME[it]!! }
        val tian = mutableMapOf<Int, String>()
        if (dunPalace == 5) {
            val ruiIdx = ring.indexOf(2)
            val fuIdx = ring.indexOf(zhiFuPalace)
            val shift = (fuIdx - ruiIdx + 8) % 8
            for (sourceIdx in 0 until 8) {
                tian[ring[(sourceIdx + shift) % 8]] = starsOnRing[sourceIdx]
            }
            val ruiNew = tian.entries.first { it.value == "天芮" }.key
            tian[ruiNew] = "天禽天芮"
        } else {
            val srcIdx = ring.indexOf(dunPalace)
            val fuIdx = ring.indexOf(zhiFuPalace)
            val shift = (fuIdx - srcIdx + 8) % 8
            for (sourceIdx in 0 until 8) {
                tian[ring[(sourceIdx + shift) % 8]] = starsOnRing[sourceIdx]
            }
            val ruiNew = tian.entries.first { it.value == "天芮" }.key
            tian[ruiNew] = "天芮天禽"
        }

        val zhiOfXunShou = xunShou[1].toString()
        val branches = "子丑寅卯辰巳午未申酉戌亥"
        val hSteps = (branches.indexOf(hourGZ[1].toString()) - branches.indexOf(zhiOfXunShou) + 12) % 12
        val zhiShiSrcPalace = if (dunPalace == 5) 2 else dunPalace
        var target = zhiShiSrcPalace
        repeat(hSteps) {
            val next = if (yinYang > 0) (if (target == 9) 1 else target + 1)
            else (if (target == 1) 9 else target - 1)
            target = if (next == 5) (if (yinYang > 0) 6 else 4) else next
        }
        val men = mutableMapOf<Int, String>()
        val srcGateIdx = ring.indexOf(zhiShiSrcPalace)
        val targetIdx = ring.indexOf(target)
        val gatesOnRing = ring.map { GATE_HOME[it]!! }
        for (k in 0 until 8) {
            men[ring[(targetIdx + k) % 8]] = gatesOnRing[(srcGateIdx + k) % 8]
        }

        val shen = mutableMapOf<Int, String>()
        val fuIdx2 = ring.indexOf(zhiFuPalace)
        for (k in 0 until 8) {
            val p = if (yinYang > 0) ring[(fuIdx2 + k) % 8]
            else ring[((fuIdx2 - k) % 8 + 8) % 8]
            shen[p] = SHEN[k]
        }

        val ma = maXingOf(hourGZ[1].toString())
        val maPalace = zhiPalace(ma)
        val dayKongPalaces = dayKong.map { zhiPalace(it) }.toSet()
        val hourKongPalaces = hourKong.map { zhiPalace(it) }.toSet()

        val tianYi = mutableMapOf<Int, String>()
        val effectiveDunPalace = dunPalace.takeIf { it != 5 } ?: 2
        val diYiOrder = (0 until 8).map { k ->
            if (yinYang > 0) ring[(ring.indexOf(effectiveDunPalace) + k) % 8]
            else ring[((ring.indexOf(effectiveDunPalace) - k) % 8 + 8) % 8]
        }
        val shiftRing = ((ring.indexOf(zhiFuPalace) - ring.indexOf(effectiveDunPalace)) % 8 + 8) % 8
        for (k in 0 until 8) {
            val srcP = diYiOrder[k]
            val yi = di[srcP] ?: ""
            val dstP = if (yinYang > 0) ring[(ring.indexOf(srcP) + shiftRing) % 8]
            else ring[((ring.indexOf(srcP) - shiftRing) % 8 + 8) % 8]
            tianYi[dstP] = yi
        }

        val patterns = mutableListOf<String>()
        for ((p, ty) in tianYi) {
            if (ty == "戊" && di[p] == "丙") patterns.add("青龙返首(${p}宫)")
            if (HIT_XING[ty] == p) patterns.add("六仪击刑(${ty}落${p}宫)")
        }

        val gongs = (1..9).map { p ->
            Gong(
                palace = p,
                diGan = di[p] ?: "",
                tianXing = tian[p] ?: "",
                renMen = men[p] ?: "",
                shenPan = shen[p] ?: "",
                isMaXing = p == maPalace,
                isDayKong = p in dayKongPalaces,
                isHourKong = p in hourKongPalaces,
                isJiXing = HIT_XING[tianYi[p]] == p,
            )
        }

        return QimenChart(
            solarDate = "$year-$month-$day $hour:${"%02d".format(minute)}",
            lunarDateStr = lunar.toString(),
            yearGZ = yearGZ,
            monthGZ = monthGZ,
            dayGZ = dayGZ,
            hourGZ = hourGZ,
            jieQi = jieQi,
            yinYang = yinYang,
            yuan = yuan,
            ju = ju,
            juMethod = when (juMethod) {
                JuMethod.CHAI_BU_DAYCOUNT -> "拆补·日数分段"
                JuMethod.CHAI_BU_FUTOU -> "拆补·符头（实验）"
                JuMethod.ZHI_RUN -> error("unreachable")
            },
            xunShou = xunShou,
            dunGan = dunGan,
            dayKong = dayKong,
            hourKong = hourKong,
            zhiFu = zhiFu,
            zhiShi = zhiShi,
            gongs = gongs,
            maXing = ma,
            isWuBuYu = isWuBuYuShi(dayGZ, hourGZ),
            patterns = patterns,
            juMethodUsed = juMethod.name,
            jieqiDayIndex = jieqiDayIndexOf(lunar),
            yuanFutou = yuanOfFutou(dayGZ),
        )
    }
}