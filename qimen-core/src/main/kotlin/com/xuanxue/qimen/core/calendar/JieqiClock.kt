package com.xuanxue.qimen.core.calendar

import com.nlf.calendar.Solar
import com.xuanxue.qimen.core.api.QimenError
import java.time.Duration
import java.time.Instant
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.ZonedDateTime
import java.time.temporal.ChronoUnit

enum class Dun { YANG, YIN }

data class JieqiStamp(
    val name: String,
    val start: ZonedDateTime,
    val secondsSinceStart: Long,
    /** Civil-date count: the local calendar date containing the exact boundary is day 1. */
    val dayIndex: Int,
    val dun: Dun,
)

/**
 * Exact jieqi boundary adapter.
 *
 * lunar-java's published tests assert second-level jieqi times. We query its astronomical/calendar
 * result in Asia/Shanghai, convert that instant to the requested zone, and never encode rounded
 * month/day memory aids such as "立春 2.4".
 */
object JieqiClock {
    private val chinaZone = ZoneId.of("Asia/Shanghai")

    private val yangTerms = setOf(
        "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰",
        "春分", "清明", "谷雨", "立夏", "小满", "芒种",
    )
    private val yinTerms = setOf(
        "夏至", "小暑", "大暑", "立秋", "处暑", "白露",
        "秋分", "寒露", "霜降", "立冬", "小雪", "大雪",
    )

    fun resolve(instant: Instant, zoneId: ZoneId): JieqiStamp {
        val china = instant.atZone(chinaZone)
        val lunar = Solar.fromYmdHms(
            china.year,
            china.monthValue,
            china.dayOfMonth,
            china.hour,
            china.minute,
            china.second,
        ).lunar

        val previous = lunar.prevJieQi
            ?: throw QimenError.AmbiguousJieqi("lunar-java returned no previous jieqi")
        val solar = previous.solar
        val boundaryChina = LocalDateTime.of(
            solar.year,
            solar.month,
            solar.day,
            solar.hour,
            solar.minute,
            solar.second,
        ).atZone(chinaZone)

        val boundaryInstant = boundaryChina.toInstant()
        if (boundaryInstant.isAfter(instant)) {
            throw QimenError.AmbiguousJieqi("jieqi boundary resolved after requested instant")
        }

        val name = previous.name
        val dun = when (name) {
            in yangTerms -> Dun.YANG
            in yinTerms -> Dun.YIN
            else -> throw QimenError.AmbiguousJieqi("unknown jieqi: $name")
        }
        val boundaryLocal = boundaryInstant.atZone(zoneId)
        val currentLocal = instant.atZone(zoneId)
        val dayIndex = ChronoUnit.DAYS.between(
            boundaryLocal.toLocalDate(),
            currentLocal.toLocalDate(),
        ).toInt() + 1

        return JieqiStamp(
            name = name,
            start = boundaryLocal,
            secondsSinceStart = Duration.between(boundaryInstant, instant).seconds,
            dayIndex = dayIndex,
            dun = dun,
        )
    }
}
