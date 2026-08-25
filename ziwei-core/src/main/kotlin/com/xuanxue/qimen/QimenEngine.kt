package com.xuanxue.qimen

import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar
import java.time.LocalDate

/**
 * 转盘时家奇门排盘引擎（Kotlin 实现）。
 *
 * 规则来源（handoff/qimen/03_RULES.jsonl + 04_CONFLICTS.md）：
 * - R-YI-001  地盘九仪 戊己庚辛壬癸丁丙乙，戊起局数宫，阳遁顺飞/阴遁逆飞（数字飞泊）
 * - R-SKY-001 值符星移到"时干"（时干为甲 -> 旬首遁干）所在宫；天禽寄坤2
 * - R-GATE-HOME 5宫无门，寄坤2；值使门随时支（阳顺阴逆，环序）
 * - R-SPIRIT-001 神盘：小值符随值符星宫，阳遁顺/阴遁逆（环序）
 * - R-JU-001/002/003 定元三法：拆补日数分段(默认)/拆补符头/置闰 -- 以 [JuMethod] 暴露，不混名
 * - R-HIT-XING 六仪击刑：戊3 己2 庚8 辛9 壬4 癸4
 * - R-WUBU-001 五不遇时：时干克日干、同阴阳、相隔五位
 * - R-QL-001 青龙返首：天盘甲/戊 加 地盘丙（一别名族）
 *
 * 关键修正（相对旧版）：
 * - 天/人/神盘旋转改为物理环序（1→8→3→4→9→2→7→6 顺时针），不再是数字序 1..9
 * - 时干为甲不再崩溃（按旬首遁干取宫）
 * - 天禽寄坤2、中宫值使寄坤2
 * - 历法基础 lunar-java (MIT)，全部本地计算。
 */
object QimenEngine {

    /** 洛书飞泊序（地盘九仪用，数字序） */
    val LUO_SHU = intArrayOf(1, 2, 3, 4, 5, 6, 7, 8, 9)

    /** 物理环序：顺时针绕九宫（坎1→艮8→震3→巽4→离9→坤2→兑7→乾6）。转盘旋转用。 */
    val RING = intArrayOf(1, 8, 3, 4, 9, 2, 7, 6)

    // 九星原驻宫（R-STAR-HOME）
    val STAR_HOME = mapOf(
        1 to "天蓬", 2 to "天芮", 3 to "天冲", 4 to "天辅", 5 to "天禽",
        6 to "天心", 7 to "天柱", 8 to "天任", 9 to "天英",
    )

    // 八门原驻宫（R-GATE-HOME；5宫无门，寄坤2）
    val GATE_HOME = mapOf(
        1 to "休门", 2 to "死门", 3 to "伤门", 4 to "杜门",
        6 to "开门", 7 to "惊门", 8 to "生门", 9 to "景门",
    )

    // 八神（R-SPIRIT-001：阳遁顺行，阴遁逆行）
    val SHEN = listOf("值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天")

    // 三奇六仪布序（R-YI-001）
    val YI = "戊己庚辛壬癸丁丙乙"

    // 六甲旬首 -> 遁干（R-XUN-001）
    val XUN_DUN = mapOf("甲子" to "戊", "甲戌" to "己", "甲申" to "庚", "甲午" to "辛", "甲辰" to "壬", "甲寅" to "癸")

    // 六仪击刑宫（R-HIT-XING；旧表 壬亥/癸子 已废弃，见 C-HIT-XING-OLD）
    val HIT_XING = mapOf("戊" to 3, "己" to 2, "庚" to 8, "辛" to 9, "壬" to 4, "癸" to 4)

    /** 定元方法（C-JU-CHAIBU-INTERNAL：冲突以 flag 暴露，禁止混名"拆补"） */
    enum class JuMethod {
        /** 拆补·日数分段（R-JU-001 默认）：节气内第 1-5/6-10/11-15 天 -> 上/中/下元 */
        CHAI_BU_DAYCOUNT,
        /** 拆补·符头（R-JU-002，B01 pp.66-67）：甲己符头定元 */
        CHAI_BU_FUTOU,
        /** 置闰（R-JU-003）：符头+超神/接气，芒种/大雪置闰（当前按符头近似实现，标注实验） */
        ZHI_RUN,
    }

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
        val isJiXing: Boolean = false,   // 六仪击刑（天盘仪落宫）
    )

    data class QimenChart(
        val solarDate: String,
        val lunarDateStr: String,
        val yearGZ: String, val monthGZ: String, val dayGZ: String, val hourGZ: String,
        val jieQi: String,          // 当前节气
        val yinYang: Int,           // 1 阳遁 / -1 阴遁
        val yuan: String,           // 上元/中元/下元
        val ju: Int,                // 局数 1-9
        val juMethod: String,       // 定元方法标签（冲突暴露）
        val xunShou: String,        // 时旬首
        val dunGan: String,         // 遁干
        val xunKong: List<String>,  // 旬空地支
        val zhiFu: String,          // 值符星
        val zhiShi: String,         // 值使门
        val gongs: List<Gong>,      // 九宫（1-9 顺序）
        val maXing: String,         // 马星地支
        val isWuBuYu: Boolean,      // 五不遇时（R-WUBU-001）
        val patterns: List<String>, // 格局（青龙返首等，R-QL-001）
        val juMethodUsed: String = "CHAI_BU_DAYCOUNT",  // 兼容旧字段（远端 AI 层引用）
        val jieqiDayIndex: Int = 0,                      // 节气内第几天（1 起）
        val yuanFutou: String = "",                      // 符头法定元（对照）
    ) {
        val juText: String get() = "${if (yinYang > 0) "阳" else "阴"}遁${ju}局 $yuan"
    }

    /** 兼容 API（远端 AI 层引用）：符头定元 */
    fun yuanOf(dayGZ: String): String = yuanOfFutou(dayGZ)

    // 干支序号（60 甲子 0-59）
    private fun seqOf(gan: String, zhi: String): Int {
        val g = "甲乙丙丁戊己庚辛壬癸".indexOf(gan)
        val z = "子丑寅卯辰巳午未申酉戌亥".indexOf(zhi)
        for (i in 0 until 60) {
            if (i % 10 == g && i % 12 == z) return i
        }
        return 0
    }

    // 时旬信息：旬首、遁干、旬空
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

    /** 符头定元（R-JU-002）：甲子/甲午/己卯/己酉 上元；甲寅/甲申/己巳/己亥 中元；其余 下元 */
    fun yuanOfFutou(dayGZ: String): String {
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

    /** 节气内第几天（1 起，交节当天=1）；失败返回 0 */
    fun jieqiDayIndexOf(lunar: Lunar): Int = runCatching {
        val cur = lunar.solar
        val cur12 = Solar.fromYmdHms(cur.year, cur.month, cur.day, 12, 0, 0)
        val ps = lunar.getPrevJie(true)?.solar ?: return@runCatching 0
        val prevNoon = Solar.fromYmdHms(ps.year, ps.month, ps.day, 12, 0, 0)
        (cur12.getJulianDay() - prevNoon.getJulianDay()).toInt() + 1
    }.getOrDefault(0)

    /** 拆补·日数分段定元（R-JU-001 默认）：节气内第 1-5/6-10/11-15 天 */
    private fun yuanOfDayCount(lunar: Lunar): String = yuanByDayCount(jieqiDayIndexOf(lunar))

    fun yuanByDayCount(dayIndex: Int): String = when {
        dayIndex <= 5 -> "上元"
        dayIndex <= 10 -> "中元"
        else -> "下元"
    }

    // 五不遇时（R-WUBU-001）：时干克日干、同阴阳、相隔五位
    private fun isWuBuYuShi(dayGZ: String, hourGZ: String): Boolean {
        val d = "甲乙丙丁戊己庚辛壬癸".indexOf(dayGZ[0])
        val h = "甲乙丙丁戊己庚辛壬癸".indexOf(hourGZ[0])
        if (d < 0 || h < 0) return false
        if ((h - d + 10) % 10 != 5) return false       // 相隔五位
        if (d % 2 != h % 2) return false                 // 同阴阳（相隔五位天然满足，双保险）
        val wuxing = intArrayOf(0, 0, 1, 1, 2, 2, 3, 3, 4, 4)  // 木木火火土土金金水水
        val ke = setOf(0 to 4, 4 to 0, 1 to 3, 3 to 1, 2 to 2).let { pairs ->
            pairs.any { (a, b) -> wuxing[h] == a && wuxing[d] == b }
        }
        return ke
    }

    /** 排盘主入口。默认 [JuMethod.CHAI_BU_DAYCOUNT]（handoff R-JU-001 默认）。 */
    fun bySolar(
        year: Int, month: Int, day: Int, hour: Int, minute: Int,
        juMethod: JuMethod = JuMethod.CHAI_BU_DAYCOUNT,
    ): QimenChart {
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

        // 定局：节气表 + 定元（方法以 flag 暴露，C-JU 冲突不混名）
        val rule = JIE_QI_JU[jieQi] ?: JuRule(1, 1, 7, 4)
        val yinYang = rule.yinYang
        val yuan = when (juMethod) {
            JuMethod.CHAI_BU_DAYCOUNT -> yuanOfDayCount(lunar)
            JuMethod.CHAI_BU_FUTOU, JuMethod.ZHI_RUN -> yuanOfFutou(dayGZ)
        }
        val ju = when (yuan) { "上元" -> rule.shang; "中元" -> rule.zhong; else -> rule.xia }

        // 时旬
        val (xunShou, dunGan, xunKong) = xunInfo(hourGZ)

        // 地盘（R-YI-001）：数字飞泊，戊起局数宫，阳遁顺飞/阴遁逆飞
        val di = mutableMapOf<Int, String>()
        for (k in 0 until 9) {
            val yi = YI[k].toString()
            val idx = LUO_SHU.indexOf(ju)
            val pos = if (yinYang > 0) LUO_SHU[(idx + k) % 9]
            else LUO_SHU[((idx - k) % 9 + 9) % 9]
            di[pos] = yi
        }

        // 值符值使：遁干落地盘宫 -> 原驻星/门（5宫门寄坤2，R-GATE-HOME）
        val dunPalace = di.entries.first { it.value == dunGan }.key
        val zhiFu = STAR_HOME[dunPalace] ?: ""
        val zhiShi = if (dunPalace == 5) GATE_HOME[2]!! else GATE_HOME[dunPalace] ?: ""

        // 值符落宫（R-SKY-001）：时干所在宫；时干为甲 -> 用旬首遁干（甲遁于六仪）
        val shiGanOrDun = if (hourGZ[0] == '甲') dunGan else hourGZ[0].toString()
        val shiGanPalace = di.entries.first { it.value == shiGanOrDun }.key
        // 中五宫寄坤2（值符落中宫随寄）
        val zhiFuPalace = if (shiGanPalace == 5) 2 else shiGanPalace

        // 天盘（转盘）：值符星转到值符落宫，其余星沿物理环序保持相对次序。
        // 天禽寄坤2（R-SKY-001）：禽不独立占位，寄于芮所在宫位序列。
        val ring = RING.toList()  // [1,8,3,4,9,2,7,6]
        // 八方星序（不含天禽）：沿环序的原驻星，从坎1起
        val starsOnRing = ring.map { STAR_HOME[it]!! }  // 蓬任冲辅英芮柱心
        val qinHome = 5
        val tian = mutableMapOf<Int, String>()
        val srcPalaceOfZhiFuStar = dunPalace  // 值符星原宫
        if (srcPalaceOfZhiFuStar == qinHome) {
            // 值符星为天禽（中宫）：禽随芮（坤2系）走
            val ruiIdx = ring.indexOf(2)
            val fuIdx = ring.indexOf(zhiFuPalace)
            for (k in 0 until 8) {
                tian[ring[(fuIdx - ruiIdx + k + 8) % 8]] = starsOnRing[k]
            }
            // 天禽寄到芮星所在宫（追加标注）
            val ruiNew = tian.entries.first { it.value == "天芮" }.key
            tian[ruiNew] = "天禽天芮"   // 禽寄芮宫
        } else {
            val srcIdx = ring.indexOf(srcPalaceOfZhiFuStar)
            val fuIdx = ring.indexOf(zhiFuPalace)
            for (k in 0 until 8) {
                tian[ring[(fuIdx - srcIdx + k + 8) % 8]] = starsOnRing[(srcIdx + k) % 8]
            }
            // 天禽寄芮：芮现在哪宫，禽跟到哪宫（同宫双星）
            val ruiNew = tian.entries.first { it.value == "天芮" }.key
            tian[ruiNew] = "天芮天禽"
        }

        // 人盘（值使门随时支）：值使落宫按洛书数字序飞泊（阳顺阴逆，中宫寄2），
        // 其余七门保持与值使的环序相对位置（转盘刚性旋转跟随）。
        val zhiOfXunShou = xunShou[1].toString()
        val hSteps = ("子丑寅卯辰巳午未申酉戌亥".indexOf(hourGZ[1].toString()) -
            "子丑寅卯辰巳午未申酉戌亥".indexOf(zhiOfXunShou) + 12) % 12
        val zhiShiSrcPalace = if (dunPalace == 5) 2 else dunPalace  // 值使门原宫（中宫寄2）
        var target = zhiShiSrcPalace
        repeat(hSteps) {
            val next = if (yinYang > 0) (if (target == 9) 1 else target + 1)
            else (if (target == 1) 9 else target - 1)
            target = if (next == 5) (if (yinYang > 0) 6 else 4) else next  // 飞泊跳中宫（寄走）
        }
        val men = mutableMapOf<Int, String>()
        val srcGateIdx = ring.indexOf(zhiShiSrcPalace)
        val targetIdx = ring.indexOf(target)
        val gatesOnRing = ring.map { GATE_HOME[it]!! }
        for (k in 0 until 8) {
            // 门 plate 整体旋转：原宫 srcGateIdx 的值使门 -> target
            men[ring[(targetIdx + k) % 8]] = gatesOnRing[(srcGateIdx + k) % 8]
        }

        // 神盘（R-SPIRIT-001）：小值符落值符星宫，沿环序阳顺阴逆
        val shen = mutableMapOf<Int, String>()
        val fuIdx2 = ring.indexOf(zhiFuPalace)
        for (k in 0 until 8) {
            val p = if (yinYang > 0) ring[(fuIdx2 + k) % 8] else ring[((fuIdx2 - k) % 8 + 8) % 8]
            shen[p] = SHEN[k]
        }

        // 马星 + 旬空落宫
        val ma = maXingOf(dayGZ[1].toString())
        val maPalace = zhiPalace(ma)
        val kongPalaces = xunKong.map { zhiPalace(it) }


        // 天盘干：星与仪同源同转——天盘星 X 落宫 p，则天盘干 = 地盘起转前该星原驻宫的仪。
        // 由于天盘整体与地盘用同一环序旋转，天盘仪落宫 = 星落宫（星仪同宫旋转）。
        // 计算：地盘中 dunPalace 起转后，仪 yi_k 落在 tian 旋转后的同位。
        // 简洁做法：天盘仪 = 与值符星一起旋转的地盘仪。地盘仪序列（从 dunPalace 沿环）整体旋转 shift 步。
        val tianYi = mutableMapOf<Int, String>()
        // 地盘仪在环上的次序：从 dunPalace 沿环序（阳顺/阴逆与星一致）
        val diYiOrder = (0 until 8).map { k ->
            if (yinYang > 0) ring[(ring.indexOf(dunPalace.takeIf { it != 5 } ?: 2) + k) % 8]
            else ring[((ring.indexOf(dunPalace.takeIf { it != 5 } ?: 2) - k) % 8 + 8) % 8]
        }
        val shiftRing = ((ring.indexOf(zhiFuPalace) - ring.indexOf(dunPalace.takeIf { it != 5 } ?: 2)) % 8 + 8) % 8
        for (k in 0 until 8) {
            val srcP = diYiOrder[k]
            val yi = di[srcP] ?: ""
            val dstP = if (yinYang > 0) ring[(ring.indexOf(srcP) + shiftRing) % 8]
            else ring[((ring.indexOf(srcP) - shiftRing) % 8 + 8) % 8]
            tianYi[dstP] = yi
        }

        val patterns = mutableListOf<String>()
        // 青龙返首（R-QL-001）：天盘甲/戊 加 地盘丙
        for ((p, ty) in tianYi) {
            if ((ty == "戊") && di[p] == "丙") patterns.add("青龙返首(${p}宫)")
        }
        // 击刑（R-HIT-XING）
        for ((p, ty) in tianYi) {
            if (HIT_XING[ty] == p) patterns.add("六仪击刑(${ty}落${p}宫)")
        }

        val wubuyu = isWuBuYuShi(dayGZ, hourGZ)

        val gongs = (1..9).map { p ->
            Gong(
                palace = p,
                diGan = di[p] ?: "",
                tianXing = tian[p] ?: "",
                renMen = men[p] ?: "",
                shenPan = shen[p] ?: "",
                isMaXing = p == maPalace,
                isKong = p in kongPalaces,
                isJiXing = HIT_XING[tianYi[p]] == p,
            )
        }

        return QimenChart(
            solarDate = "$year-$month-$day $hour:${"%02d".format(minute)}",
            lunarDateStr = lunar.toString(),
            yearGZ = yearGZ, monthGZ = monthGZ, dayGZ = dayGZ, hourGZ = hourGZ,
            jieQi = jieQi,
            yinYang = yinYang, yuan = yuan, ju = ju,
            juMethod = when (juMethod) {
                JuMethod.CHAI_BU_DAYCOUNT -> "拆补·日数分段"
                JuMethod.CHAI_BU_FUTOU -> "拆补·符头"
                JuMethod.ZHI_RUN -> "置闰(近似)"
            },
            xunShou = xunShou, dunGan = dunGan, xunKong = xunKong,
            zhiFu = zhiFu, zhiShi = zhiShi,
            gongs = gongs,
            maXing = ma,
            isWuBuYu = wubuyu,
            patterns = patterns,
            juMethodUsed = when (juMethod) {
                JuMethod.CHAI_BU_DAYCOUNT -> "CHAI_BU_DAYCOUNT"
                JuMethod.CHAI_BU_FUTOU -> "CHAI_BU_FUTOU"
                JuMethod.ZHI_RUN -> "ZHI_RUN"
            },
            jieqiDayIndex = jieqiDayIndexOf(lunar),
            yuanFutou = yuanOfFutou(dayGZ),
        )
    }
}
