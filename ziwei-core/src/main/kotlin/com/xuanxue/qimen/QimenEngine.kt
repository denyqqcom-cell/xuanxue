package com.xuanxue.qimen

import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar
import java.time.LocalDate

/**
 * 转盘时家奇门排盘引擎（Kotlin 实现）。
 * 规则来源：公开古籍（《烟波钓叟歌》/奇门遁甲预测学）；定局/旬首/地盘九仪/值符值使对齐
 * 用户本地验证脚本（_tmp_paipan_core.py），天/门/神盘旋转按标准转盘奇门补全。
 * 基础干支/节气/旬空由 lunar-java (MIT) 提供。全部本地计算。
 */
object QimenEngine {

    // 九宫洛书顺序（顺飞）：1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离
    val LUO_SHU = intArrayOf(1, 2, 3, 4, 5, 6, 7, 8, 9)

    // 九星原驻宫（转盘奇门定式）
    val STAR_HOME = mapOf(
        1 to "天蓬", 2 to "天芮", 3 to "天冲", 4 to "天辅", 5 to "天禽",
        6 to "天心", 7 to "天柱", 8 to "天任", 9 to "天英",
    )

    // 八门原驻宫
    val GATE_HOME = mapOf(
        1 to "休门", 2 to "死门", 3 to "伤门", 4 to "杜门",
        6 to "开门", 7 to "惊门", 8 to "生门", 9 to "景门",
    )

    // 八神（阳遁顺行，阴遁逆行）
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
        val palace: Int,           // 洛书宫 1-9
        val diGan: String,         // 地盘三奇六仪
        val tianXing: String,      // 天盘九星
        val renMen: String,        // 人盘八门
        val shenPan: String,       // 神盘八神
        val isMaXing: Boolean = false,   // 马星
        val isKong: Boolean = false,     // 旬空
    )

    data class QimenChart(
        val solarDate: String,
        val lunarDateStr: String,
        val yearGZ: String, val monthGZ: String, val dayGZ: String, val hourGZ: String,
        val jieQi: String,          // 当前节气
        val yinYang: Int,           // 1 阳遁 / -1 阴遁
        val yuan: String,           // 上元/中元/下元
        val ju: Int,                // 局数 1-9
        val xunShou: String,        // 时旬首
        val dunGan: String,         // 遁干
        val xunKong: List<String>,  // 旬空地支
        val zhiFu: String,          // 值符星
        val zhiShi: String,         // 值使门
        val gongs: List<Gong>,      // 九宫（1-9 顺序）
        val maXing: String,         // 马星地支
        val juMethodUsed: String = "CHAI_BU_DAYCOUNT",
        val jieqiDayIndex: Int = 0,
        val yuanFutou: String = "",
    ) {
        val juText: String get() = "${if (yinYang > 0) "阳" else "阴"}遁${ju}局 $yuan"
    }

    // 干支序号（60 甲子 0-59）
    private fun seqOf(gan: String, zhi: String): Int {
        val g = "甲乙丙丁戊己庚辛壬癸".indexOf(gan)
        val z = "子丑寅卯辰巳午未申酉戌亥".indexOf(zhi)
        for (i in 0 until 60) {
            if (i % 10 == g && i % 12 == z) return i
        }
        return 0
    }

    // 时旬信息：旬首、遁干、旬空、时干在旬内序
    private fun xunInfo(gz: String): Triple<String, String, List<String>> {
        val gan = gz[0].toString(); val zhi = gz[1].toString()
        val s = seqOf(gan, zhi)
        val base = (s / 10) * 10
        val xunShou = "甲乙丙丁戊己庚辛壬癸"[base % 10].toString() + "子丑寅卯辰巳午未申酉戌亥"[base % 12].toString()
        val dun = XUN_DUN[xunShou] ?: ""
        val kong = listOf("子丑寅卯辰巳午未申酉戌亥"[(base + 10) % 12].toString(), "子丑寅卯辰巳午未申酉戌亥"[(base + 11) % 12].toString())
        return Triple(xunShou, dun, kong)
    }

    // 地支落洛书宫（奇门定式）
    fun zhiPalace(zhi: String): Int = when (zhi) {
        "子" -> 1; "丑", "寅" -> 8; "卯" -> 3; "辰", "巳" -> 4; "午" -> 9
        "未", "申" -> 2; "酉" -> 7; "戌", "亥" -> 6; else -> 5
    }

    // 日支驿马（三合局冲）
    fun maXingOf(dayZhi: String): String = when (dayZhi) {
        "寅", "午", "戌" -> "申"; "申", "子", "辰" -> "寅"
        "巳", "酉", "丑" -> "亥"; "亥", "卯", "未" -> "巳"; else -> ""
    }

    /** R-JU-001：节气日内序号 1-5 上 / 6-10 中 / 11+ 下。 */
    fun yuanByDayCount(dayIndex: Int): String = when {
        dayIndex <= 5 -> "上元"
        dayIndex <= 10 -> "中元"
        else -> "下元"
    }

    fun jieqiDayIndexOf(lunar: Lunar, jieQiName: String, year: Int, month: Int, day: Int): Int {
        val start = lunar.jieQiTable[jieQiName] ?: return 1
        val a = LocalDate.of(start.year, start.month, start.day)
        val b = LocalDate.of(year, month, day)
        val idx = (b.toEpochDay() - a.toEpochDay()).toInt() + 1
        return if (idx >= 1) idx else 1
    }

    // 定元：符头法 —— 日干支旬首定元（甲子/甲午/己卯/己酉 上元；甲寅/甲申/己巳/己亥 中元；其余 下元）
    // 仅作门派对对照，默认起局不再使用。
    fun yuanOf(dayGZ: String): String {
        val s = seqOf(dayGZ[0].toString(), dayGZ[1].toString())
        val fuTou = s - (s % 10)  // 旬首序号
        val ftGan = "甲乙丙丁戊己庚辛壬癸"[fuTou % 10].toString()
        val ftZhi = "子丑寅卯辰巳午未申酉戌亥"[fuTou % 12].toString()
        return when (ftGan + ftZhi) {
            "甲子", "甲午", "己卯", "己酉" -> "上元"
            "甲寅", "甲申", "己巳", "己亥" -> "中元"
            else -> "下元"
        }
    }

    fun bySolar(year: Int, month: Int, day: Int, hour: Int, minute: Int): QimenChart {
        val solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        val lunar: Lunar = solar.lunar
        val ec = lunar.eightChar

        val yearGZ = ec.getYearGan() + ec.getYearZhi()
        val monthGZ = ec.getMonthGan() + ec.getMonthZhi()
        val dayGZ = ec.getDayGan() + ec.getDayZhi()
        val hourGZ = ec.getTimeGan() + ec.getTimeZhi()

        // 当前节气（上一个节，非中气——奇门定局用节）
        val jieQi = runCatching { lunar.getPrevJieQi(true)?.name }.getOrNull()
            ?: runCatching { lunar.getPrevJieQi()?.name }.getOrNull()
            ?: "冬至"

        // 定局：节气表 + 拆补·日数分段（handoff 默认 R-JU-001）。符头另存对照，不参与起局。
        val rule = JIE_QI_JU[jieQi] ?: JuRule(1, 1, 7, 4)
        val yinYang = rule.yinYang
        val jieqiDayIndex = jieqiDayIndexOf(lunar, jieQi, year, month, day)
        val yuan = yuanByDayCount(jieqiDayIndex)
        val yuanFutou = yuanOf(dayGZ)
        val ju = when (yuan) { "上元" -> rule.shang; "中元" -> rule.zhong; else -> rule.xia }

        // 时旬
        val (xunShou, dunGan, xunKong) = xunInfo(hourGZ)

        // 地盘：阳遁顺飞/阴遁逆飞，戊起局数宫
        val di = mutableMapOf<Int, String>()
        for (k in 0 until 9) {
            val yi = YI[k].toString()
            val pos = if (yinYang > 0) {
                // 顺飞：局数宫起，按洛书顺序
                val idx = LUO_SHU.indexOf(ju)
                LUO_SHU[(idx + k) % 9]
            } else {
                val idx = LUO_SHU.indexOf(ju)
                LUO_SHU[((idx - k) % 9 + 9) % 9]
            }
            di[pos] = yi
        }

        // 值符值使：遁干落地盘宫 -> 原驻星/门
        val dunPalace = di.entries.first { it.value == dunGan }.key
        val zhiFu = STAR_HOME[dunPalace] ?: ""
        val zhiShi = GATE_HOME[dunPalace] ?: ""

        // 天盘：值符星随时干落宫（转盘奇门：值符星转到时干所在宫，其余星沿洛书序顺排）
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

        // 人盘：值使门随时支落宫（值使门原宫 -> 时支宫，其余门沿洛书序顺排）
        val shiZhiPalace = zhiPalace(hourGZ[1].toString())
        val men = mutableMapOf<Int, String>()
        val shift2 = (LUO_SHU.indexOf(shiZhiPalace) - LUO_SHU.indexOf(dunPalace) + 9) % 9
        for (p in 1..9) {
            val srcIdx = LUO_SHU.indexOf(p)
            val newIdx = (srcIdx + shift2) % 9
            val newP = LUO_SHU[newIdx]
            men[newP] = GATE_HOME[p] ?: ""
        }

        // 神盘：值符神随值符星（阳遁顺行/阴遁逆行），跳过中宫（神不入中），值符落时干宫
        val shen = mutableMapOf<Int, String>()
        val shenOrder = if (yinYang > 0) listOf(1, 2, 3, 4, 6, 7, 8, 9) else listOf(9, 8, 7, 6, 4, 3, 2, 1)
        val zhiFuStart = if (shiGanPalace == 5) 2 else shiGanPalace // 时干落中宫则值符随寄坤二
        val startIdx = shenOrder.indexOf(zhiFuStart).coerceAtLeast(0)
        for (k in 0 until 8) {
            shen[shenOrder[(startIdx + k) % 8]] = SHEN[k]
        }

        // 马星 + 旬空落宫
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
            juMethodUsed = "CHAI_BU_DAYCOUNT",
            jieqiDayIndex = jieqiDayIndex,
            yuanFutou = yuanFutou,
        )
    }
}
