package com.xuanxue.liuren

import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar

/**
 * 大六壬排盘引擎 — Kotlin 实现。
 * 规则依据：袁树珊《大六壬探原》体系（公开传统规则，本地古籍校核）。
 * 月将/天地盘/四课/九宗门三传/十二天将/旬空/遁干/六亲。
 * 基础干支/节气由 lunar-java (MIT) 提供。全部本地计算。
 */
object LiuRenEngine {

    val ZHI = listOf("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")

    // 十干寄宫（日干寄地支）
    val GAN_JI = mapOf("甲" to "寅", "乙" to "辰", "丙" to "巳", "丁" to "未", "戊" to "巳",
        "己" to "未", "庚" to "申", "辛" to "戌", "壬" to "亥", "癸" to "丑")

    // 月将（太阳过宫，中气换将）：雨水后亥将 → 大寒后子将
    // 节气名 -> 月将支
    val YUE_JIANG = mapOf(
        "雨水" to "亥", "春分" to "戌", "谷雨" to "酉", "小满" to "申", "夏至" to "未", "大暑" to "午",
        "处暑" to "巳", "秋分" to "辰", "霜降" to "卯", "小雪" to "寅", "冬至" to "丑", "大寒" to "子",
    )
    // 节气顺序（用于取上一个中气）
    val JIE_QI_ORDER = listOf("小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
        "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至")

    // 十二天将（贵人起）：贵人/螣蛇/朱雀/六合/勾陈/青龙/天空/白虎/太常/玄武/太阴/天后
    val TIAN_JIANG = listOf("贵人", "螣蛇", "朱雀", "六合", "勾陈", "青龙", "天空", "白虎", "太常", "玄武", "太阴", "天后")

    // 贵人歌：甲戊庚牛羊 乙己鼠猴乡 丙丁猪鸡位 壬癸蛇兔藏 六辛逢马虎
    // 白天（昼贵）取阳支，夜（暮贵）取阴支。简化：甲戊庚->丑(牛)未(羊); 乙己->子(鼠)申(猴); 丙丁->亥(猪)酉(鸡); 壬癸->巳(蛇)卯(兔); 辛->午(马)寅(虎)
    fun guiRen(dayGan: String, night: Boolean): String = when (dayGan) {
        "甲", "戊", "庚" -> if (night) "未" else "丑"
        "乙", "己" -> if (night) "申" else "子"
        "丙", "丁" -> if (night) "酉" else "亥"
        "壬", "癸" -> if (night) "卯" else "巳"
        else -> if (night) "寅" else "午" // 辛
    }

    // 五行
    val ZHI_WUXING = mapOf("子" to "水", "丑" to "土", "寅" to "木", "卯" to "木", "辰" to "土", "巳" to "火",
        "午" to "火", "未" to "土", "申" to "金", "酉" to "金", "戌" to "土", "亥" to "水")
    val GAN_WUXING = mapOf("甲" to "木", "乙" to "木", "丙" to "火", "丁" to "火", "戊" to "土", "己" to "土",
        "庚" to "金", "辛" to "金", "壬" to "水", "癸" to "水")

    // 十二地支冲
    fun chong(z: String): String = ZHI[(ZHI.indexOf(z) + 6) % 12]

    // 六冲对（返吟用）
    private val CHONG_MAP = ZHI.associateWith { chong(it) }

    // 地支六合
    fun he(z: String): String = ZHI[(ZHI.indexOf(z) + 7) % 12]

    // 六壬遁干（旬遁）：时支遁干用五鼠遁（以日干起）
    fun dunGanOf(dayGan: String, zhi: String): String {
        val start = mapOf("甲" to 0, "己" to 0, "乙" to 2, "庚" to 2, "丙" to 4, "辛" to 4,
            "丁" to 6, "壬" to 6, "戊" to 8, "癸" to 8)[dayGan] ?: 0
        return "甲乙丙丁戊己庚辛壬癸"[((start + ZHI.indexOf(zhi)) % 10)].toString()
    }

    data class Ke(val zhi: String, val dunGan: String)  // 课神（地盘支 + 遁干）

    data class SanChuan(val chu: String, val zhong: String, val mo: String, val fa: String) // 三传 + 取法

    data class LiuRenChart(
        val solarDate: String,
        val lunarDateStr: String,
        val yearGZ: String, val monthGZ: String, val dayGZ: String, val hourGZ: String,
        val yueJiang: String,          // 月将
        val tianPan: List<String>,     // 天盘（12 支，index=地盘支序）
        val siKe: List<Ke>,            // 四课（课1-4）
        val sanChuan: SanChuan,        // 三传
        val guiRen: String,            // 贵人（昼夜）
        val xunKong: List<String>,     // 旬空
        val ganJi: String,             // 日干寄宫
    )

    fun bySolar(year: Int, month: Int, day: Int, hour: Int, minute: Int, night: Boolean = false): LiuRenChart {
        val solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        val lunar: Lunar = solar.lunar
        val ec = lunar.eightChar
        val yearGZ = ec.getYearGan() + ec.getYearZhi()
        val monthGZ = ec.getMonthGan() + ec.getMonthZhi()
        val dayGZ = ec.getDayGan() + ec.getDayZhi()
        val hourGZ = ec.getTimeGan() + ec.getTimeZhi()
        val dayGan = dayGZ[0].toString()
        val dayZhi = dayGZ[1].toString()
        val hourZhi = hourGZ[1].toString()

        // 月将：上一个中气定（雨水→亥将...大寒→子将；中气即十二中气）
        val prevQi = runCatching { lunar.getPrevQi()?.name }.getOrNull()
            ?: runCatching { lunar.getPrevJieQi(false)?.name }.getOrNull()
            ?: "冬至"
        val yueJiang = YUE_JIANG[prevQi] ?: "亥"

        // 天地盘：月将加时（天盘月将落于地盘时支位，其余顺排）
        val tianPan = MutableList(12) { "" }
        val startIdx = ZHI.indexOf(hourZhi)
        val yjIdx = ZHI.indexOf(yueJiang)
        for (i in 0 until 12) {
            val diZhi = ZHI[(startIdx + i) % 12]          // 地盘支
            val tianZhi = ZHI[(yjIdx + i) % 12]           // 天盘支
            tianPan[ZHI.indexOf(diZhi)] = tianZhi
        }

        // 四课：一课=日干寄宫支上的天盘支，二课=日支上的天盘支，三课=一课支上的天盘支，四课=二课支上的天盘支
        val ganJi = GAN_JI[dayGan] ?: dayZhi
        val ke1Zhi = tianPan[ZHI.indexOf(ganJi)]
        val ke2Zhi = tianPan[ZHI.indexOf(dayZhi)]
        val ke3Zhi = tianPan[ZHI.indexOf(ke1Zhi)]
        val ke4Zhi = tianPan[ZHI.indexOf(ke2Zhi)]
        val siKe = listOf(
            Ke(ke1Zhi, dunGanOf(dayGan, ke1Zhi)),
            Ke(ke2Zhi, dunGanOf(dayGan, ke2Zhi)),
            Ke(ke3Zhi, dunGanOf(dayGan, ke3Zhi)),
            Ke(ke4Zhi, dunGanOf(dayGan, ke4Zhi)),
        )

        // 九宗门取三传
        val sanChuan = jiuZongMen(dayGan, dayZhi, ganJi, tianPan, siKe)

        // 旬空
        val daySeq = seqOf(dayGZ)
        val base = (daySeq / 10) * 10
        val kong = listOf(ZHI[(base + 10) % 12], ZHI[(base + 11) % 12])

        return LiuRenChart(
            solarDate = "$year-$month-$day $hour:${"%02d".format(minute)}",
            lunarDateStr = lunar.toString(),
            yearGZ = yearGZ, monthGZ = monthGZ, dayGZ = dayGZ, hourGZ = hourGZ,
            yueJiang = yueJiang, tianPan = tianPan, siKe = siKe,
            sanChuan = sanChuan,
            guiRen = guiRen(dayGan, night),
            xunKong = kong, ganJi = ganJi,
        )
    }

    private fun seqOf(gz: String): Int {
        val g = "甲乙丙丁戊己庚辛壬癸".indexOf(gz[0])
        val z = ZHI.indexOf(gz[1].toString())
        for (i in 0 until 60) if (i % 10 == g && i % 12 == z) return i
        return 0
    }

    // 天盘支上神（地盘支 -> 天盘支）
    private fun shangShen(tianPan: List<String>, diZhi: String): String = tianPan[ZHI.indexOf(diZhi)]

    // 九宗门：贼克/比用/涉害/遥克/昴星/别责/八专/返吟/伏吟
    fun jiuZongMen(dayGan: String, dayZhi: String, ganJi: String, tianPan: List<String>, siKe: List<Ke>): SanChuan {
        val keZhis = siKe.map { it.zhi }
        val ganWx = GAN_WUXING[dayGan] ?: "木"

        // 返吟（天地盘全冲）：天盘与地盘相冲
        val isFanYin = tianPan.indices.all { tianPan[it] == chong(ZHI[it]) }
        // 伏吟（天地盘同）
        val isFuYin = tianPan.indices.all { tianPan[it] == ZHI[it] }

        // 上克下（天盘支克地盘支）与下贼上（地盘支克天盘支）——四课上神与下神
        // 四课下神：课1下=干寄宫，课2下=日支，课3下=课1上，课4下=课2上
        val lower = listOf(ganJi, dayZhi, keZhis[0], keZhis[1])
        val upper = keZhis
        fun ke(c: String, d: String): Boolean = KE_MAP[ZHI_WUXING[c] ?: ""] == (ZHI_WUXING[d] ?: "") // c 克 d
        val shangKe = (0 until 4).filter { ke(upper[it], lower[it]) }          // 上克下
        val xiaZe = (0 until 4).filter { ke(lower[it], upper[it]) }            // 下贼上

        // 三传通用：初传取上神，中传=初传上神，末传=中传上神
        fun chuanOf(chuZhi: String): SanChuan {
            val zhong = shangShen(tianPan, chuZhi)
            val mo = shangShen(tianPan, zhong)
            return SanChuan(chuZhi, zhong, mo, "三传递克")
        }

        // 1. 贼克
        if (shangKe.isNotEmpty() && xiaZe.isEmpty()) {
            val chu = keZhis[shangKe.first()]
            return chuanOf(chu).copy(fa = "贼克（上克下）")
        }
        if (xiaZe.isNotEmpty() && shangKe.isEmpty()) {
            val chu = keZhis[xiaZe.first()]
            return chuanOf(chu).copy(fa = "贼克（下贼上）")
        }
        // 2. 比用（多克取与日干比和者）
        if (shangKe.size > 1 || xiaZe.size > 1) {
            val candidates = if (shangKe.size >= xiaZe.size) shangKe.map { keZhis[it] } else xiaZe.map { keZhis[it] }
            val bi = candidates.filter { ZHI_WUXING[it] == ganWx }
            val chu = bi.firstOrNull() ?: candidates.first()
            return chuanOf(chu).copy(fa = "比用")
        }
        // 3. 遥克（无贼克）：上神克日干（遥克）或日干克上神（遥贼）
        if (shangKe.isEmpty() && xiaZe.isEmpty() && !isFanYin) {
            val yaoKe = keZhis.filter { KE_MAP[ZHI_WUXING[it] ?: ""] == ganWx }
            val yaoZe = keZhis.filter { KE_MAP[ganWx] == ZHI_WUXING[it] ?: "" }
            val chu = (yaoKe + yaoZe).firstOrNull()
            if (chu != null) return chuanOf(chu).copy(fa = "遥克")
        }
        // 4. 昴星（无贼克无遥克）：阳日取地盘酉上天盘，阴日取天盘酉下地盘
        if (shangKe.isEmpty() && xiaZe.isEmpty()) {
            val isYang = dayGan in listOf("甲", "丙", "戊", "庚", "壬")
            val chu = if (isYang) tianPan[ZHI.indexOf("酉")] else ZHI[tianPan.indexOf("酉")]
            if (chu.isNotEmpty()) return chuanOf(chu).copy(fa = "昴星")
        }
        // 5. 别责/八专/返吟/伏吟 简化处理
        if (isFuYin) {
            val chu = shangShen(tianPan, ganJi)
            return chuanOf(chu).copy(fa = "伏吟")
        }
        if (isFanYin) {
            val chu = shangShen(tianPan, ganJi)
            return chuanOf(chu).copy(fa = "返吟")
        }
        // 6. 八专（干支寄宫同位）：取干支上神
        val chu = shangShen(tianPan, ganJi)
        return chuanOf(chu).copy(fa = "八专")
    }

    // 相克表：谁克谁（X 克 Y）
    private val KE_MAP = mapOf("金" to "木", "木" to "土", "土" to "水", "水" to "火", "火" to "金")
}
