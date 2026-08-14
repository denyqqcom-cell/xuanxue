package com.xuanxue.qimen.core.api

import com.xuanxue.qimen.core.calendar.ClockPolicy
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.GanzhiCalendar
import com.xuanxue.qimen.core.calendar.JieqiClock
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.ju.JuMethod
import com.xuanxue.qimen.core.ju.JuResolver
import com.xuanxue.qimen.core.ju.Yuan
import com.xuanxue.qimen.core.plate.EarthPlate
import com.xuanxue.qimen.core.plate.Yi
import com.xuanxue.qimen.core.school.BoardSchool
import com.xuanxue.qimen.core.school.QimenSchoolConfig
import java.time.DateTimeException
import java.time.Instant
import java.time.ZoneId

data class QimenRequest(
    val instantEpochMs: Long,
    val zoneId: String = "Asia/Shanghai",
    val longitudeEastDeg: Double? = null,
    val school: QimenSchoolConfig = QimenSchoolConfig.Default,
)

data class CivilStamp(
    val instantEpochMs: Long,
    val zoneId: String,
    val localDateTime: String,
    val qimenDate: String,
    val hourSlot: String,
)

data class QimenChart(
    val civil: CivilStamp,
    val dayPillar: StemBranch,
    val hourPillar: StemBranch,
    val xunShou: StemBranch,
    val dunYi: Yi,
    val xunKong: List<com.xuanxue.qimen.core.calendar.Branch>,
    val jieqi: String,
    val jieqiDayIndex: Int,
    val dun: Dun,
    val ju: Int,
    val yuan: Yuan,
    val juMethodUsed: JuMethod,
    val earth: EarthPlate?,
)

/** Throwable by design so it can travel through Kotlin Result without losing typed errors. */
sealed class QimenError(message: String) : IllegalArgumentException(message) {
    data class UnsupportedSchool(val flag: String) : QimenError("Unsupported qimen school/config: $flag")
    data class AmbiguousJieqi(val detail: String) : QimenError(detail)
    data class InvalidInstant(val detail: String) : QimenError(detail)
}

object QimenEngine {
    fun cast(req: QimenRequest): Result<QimenChart> {
        unsupported(req.school)?.let { return Result.failure(it) }

        return try {
            val instant = Instant.ofEpochMilli(req.instantEpochMs)
            val zone = ZoneId.of(req.zoneId)
            val local = instant.atZone(zone)
            val slot = ClockPolicy.resolve(local.toLocalTime(), req.school.lateZiRollsToNextDay)
            val qimenDate = if (slot.rollNextDay) local.toLocalDate().plusDays(1) else local.toLocalDate()
            val day = GanzhiCalendar.dayPillar(qimenDate)
            check(GanzhiCalendar.anchorsAgree(qimenDate)) { "Sexagenary anchors disagree for $qimenDate" }
            val hour = GanzhiCalendar.hourPillar(day.pillar.stem, slot.hourBranch)
            val xun = GanzhiCalendar.xun(hour)
            val jieqi = JieqiClock.resolve(instant, zone)
            val ju = JuResolver.resolveDayCount(jieqi.name, jieqi.dayIndex, jieqi.dun)

            Result.success(
                QimenChart(
                    civil = CivilStamp(
                        instantEpochMs = req.instantEpochMs,
                        zoneId = zone.id,
                        localDateTime = local.toLocalDateTime().toString(),
                        qimenDate = qimenDate.toString(),
                        hourSlot = slot.slotLabel,
                    ),
                    dayPillar = day.pillar,
                    hourPillar = hour,
                    xunShou = xun.xunShou,
                    dunYi = xun.dunYi,
                    xunKong = xun.xunKong,
                    jieqi = jieqi.name,
                    jieqiDayIndex = jieqi.dayIndex,
                    dun = jieqi.dun,
                    ju = ju.ju,
                    yuan = ju.yuan,
                    juMethodUsed = ju.method,
                    earth = null,
                ),
            )
        } catch (e: QimenError) {
            Result.failure(e)
        } catch (e: DateTimeException) {
            Result.failure(QimenError.InvalidInstant(e.message ?: "invalid date/time"))
        } catch (e: IllegalArgumentException) {
            Result.failure(QimenError.InvalidInstant(e.message ?: "invalid qimen input"))
        }
    }

    private fun unsupported(school: QimenSchoolConfig): QimenError.UnsupportedSchool? = when {
        school.useTrueSolarTime -> QimenError.UnsupportedSchool("useTrueSolarTime")
        school.juMethod == JuMethod.CHAI_BU_FUTOU -> QimenError.UnsupportedSchool("CHAI_BU_FUTOU")
        school.juMethod == JuMethod.ZHI_RUN -> QimenError.UnsupportedSchool("ZHI_RUN")
        school.juMethod == JuMethod.MAO_SHAN -> QimenError.UnsupportedSchool("MAO_SHAN")
        school.boardSchool == BoardSchool.FEI_GONG -> QimenError.UnsupportedSchool("FEI_GONG")
        else -> null
    }
}
