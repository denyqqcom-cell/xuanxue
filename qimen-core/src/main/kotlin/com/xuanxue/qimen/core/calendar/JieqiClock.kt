package com.xuanxue.qimen.core.calendar

import com.nlf.calendar.Solar
import java.time.Duration
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

/**
 * 二十四节气。这里只承担时间边界，不承担上中下元或排盘流派判定。
 */
enum class Jieqi(val zh: String) {
    DONG_ZHI("冬至"),
    XIAO_HAN("小寒"),
    DA_HAN("大寒"),
    LI_CHUN("立春"),
    YU_SHUI("雨水"),
    JING_ZHE("惊蛰"),
    CHUN_FEN("春分"),
    QING_MING("清明"),
    GU_YU("谷雨"),
    LI_XIA("立夏"),
    XIAO_MAN("小满"),
    MANG_ZHONG("芒种"),
    XIA_ZHI("夏至"),
    XIAO_SHU("小暑"),
    DA_SHU("大暑"),
    LI_QIU("立秋"),
    CHU_SHU("处暑"),
    BAI_LU("白露"),
    QIU_FEN("秋分"),
    HAN_LU("寒露"),
    SHUANG_JIANG("霜降"),
    LI_DONG("立冬"),
    XIAO_XUE("小雪"),
    DA_XUE("大雪");

    companion object {
        fun fromZh(value: String): Jieqi = entries.firstOrNull { it.zh == value }
            ?: error("Unknown jieqi: $value")
    }
}

enum class Dun {
    YANG,
    YIN,
}

data class JieqiStamp(
    val jieqi: Jieqi,
    val start: LocalDateTime,
    val secondsSinceStart: Long,
    /** 交节所在公历日记作第 1 日。它只是时间元数据，不直接等同于拆补的上中下元。 */
    val civilDayIndex: Int,
    val dun: Dun,
)

/**
 * 精确节气时刻适配层。
 *
 * v1 只承诺 Asia/Shanghai。lunar-java 的 Solar/JieQi API 本身没有 ZoneId 参数，
 * 因此这里宁可拒绝其他时区，也不做看似通用但语义不清的转换。
 */
object JieqiClock {
    const val SUPPORTED_ZONE = "Asia/Shanghai"
    private val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

    private data class Boundary(val jieqi: Jieqi, val start: LocalDateTime)

    fun resolve(localDateTime: LocalDateTime, zoneId: String = SUPPORTED_ZONE): JieqiStamp {
        require(zoneId == SUPPORTED_ZONE) {
            "qimen-core v1 only supports $SUPPORTED_ZONE for jieqi; got $zoneId"
        }

        val current = boundariesAround(localDateTime.year)
            .asSequence()
            .filter { !it.start.isAfter(localDateTime) }
            .maxByOrNull { it.start }
            ?: error("Unable to resolve previous jieqi for $localDateTime")

        val seconds = Duration.between(current.start, localDateTime).seconds
        val civilDayIndex = ChronoUnit.DAYS.between(
            current.start.toLocalDate(),
            localDateTime.toLocalDate(),
        ).toInt() + 1

        return JieqiStamp(
            jieqi = current.jieqi,
            start = current.start,
            secondsSinceStart = seconds,
            civilDayIndex = civilDayIndex,
            dun = dunFor(current.jieqi),
        )
    }

    fun dunFor(jieqi: Jieqi): Dun = when (jieqi) {
        Jieqi.DONG_ZHI,
        Jieqi.XIAO_HAN,
        Jieqi.DA_HAN,
        Jieqi.LI_CHUN,
        Jieqi.YU_SHUI,
        Jieqi.JING_ZHE,
        Jieqi.CHUN_FEN,
        Jieqi.QING_MING,
        Jieqi.GU_YU,
        Jieqi.LI_XIA,
        Jieqi.XIAO_MAN,
        Jieqi.MANG_ZHONG -> Dun.YANG

        else -> Dun.YIN
    }

    private fun boundariesAround(year: Int): List<Boundary> {
        val found = linkedMapOf<Pair<Jieqi, LocalDateTime>, Boundary>()
        for (anchorYear in (year - 1)..(year + 1)) {
            val table = Solar.fromYmd(anchorYear, 7, 1).lunar.jieQiTable
            for (jieqi in Jieqi.entries) {
                val solar = table[jieqi.zh] ?: continue
                val start = LocalDateTime.parse(solar.toYmdHms(), formatter)
                found[jieqi to start] = Boundary(jieqi, start)
            }
        }
        return found.values.sortedBy { it.start }
    }
}
