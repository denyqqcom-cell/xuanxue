package com.xuanxue.qimen.core.api

import com.xuanxue.qimen.core.calendar.GanzhiCalendar
import com.xuanxue.qimen.core.calendar.JieqiClock
import com.xuanxue.qimen.core.calendar.JieqiStamp
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.ju.FutouYuanResolver
import com.xuanxue.qimen.core.ju.JuTable
import com.xuanxue.qimen.core.ju.Yuan
import com.xuanxue.qimen.core.plate.DutyMovementResolver
import com.xuanxue.qimen.core.plate.DutyRuntime
import com.xuanxue.qimen.core.plate.EarthPlate
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import com.xuanxue.qimen.core.rule.PreflightRules
import com.xuanxue.qimen.core.school.JuMethod
import com.xuanxue.qimen.core.school.QimenError
import com.xuanxue.qimen.core.school.QimenSchoolConfig
import com.xuanxue.qimen.core.xun.XunInfo
import com.xuanxue.qimen.core.xun.XunResolver
import java.time.Instant
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneId

data class QimenRequest(
    val instantEpochMs: Long,
    val zoneId: String = JieqiClock.SUPPORTED_ZONE,
    val longitudeEastDeg: Double? = null,
    val school: QimenSchoolConfig = QimenSchoolConfig(),
)

enum class PlateState {
    /** 地盘九仪及值符/值使锚点与当前落宫已验证；完整天盘、人盘、神盘仍锁定。 */
    EARTH_PLATE_VERIFIED_FULL_PLATE_LOCKED,
}

data class QimenChart(
    val localDateTime: LocalDateTime,
    val zoneId: String,
    val qimenDate: LocalDate,
    val dayPillar: StemBranch,
    val hourPillar: StemBranch,
    val xun: XunInfo,
    val jieqi: JieqiStamp,
    val futou: StemBranch,
    val yuan: Yuan,
    val ju: Int,
    val juMethodUsed: JuMethod,
    val isWuBuYu: Boolean,
    val earthPlate: EarthPlate,
    val duty: DutyRuntime,
    val plateState: PlateState = PlateState.EARTH_PLATE_VERIFIED_FULL_PLATE_LOCKED,
)

/**
 * v1 生成可验证的盘前数据、地盘九仪，以及值符/值使的已验证运行锚点。
 * 完整天盘九星、人盘八门、神盘八神仍被硬锁，避免把局部规则伪装成完整盘。
 */
object QimenEngine {
    fun cast(request: QimenRequest): Result<QimenChart> = runCatching {
        request.school.unsupportedFlagOrNull()?.let { throw QimenError.UnsupportedSchool(it) }
        if (request.zoneId != JieqiClock.SUPPORTED_ZONE) {
            throw QimenError.UnsupportedZone(request.zoneId)
        }
        if (request.school.useTrueSolarTime || request.longitudeEastDeg != null && request.school.useTrueSolarTime) {
            throw QimenError.UnsupportedSchool("true_solar_time")
        }

        val zone = ZoneId.of(request.zoneId)
        val localDateTime = Instant.ofEpochMilli(request.instantEpochMs)
            .atZone(zone)
            .toLocalDateTime()

        val slot = GanzhiCalendar.clockSlot(
            localDateTime.toLocalTime(),
            request.school.lateZiRollsToNextDay,
        )
        val qimenDate = if (slot.rollNextDay) {
            localDateTime.toLocalDate().plusDays(1)
        } else {
            localDateTime.toLocalDate()
        }
        val dayPillar = GanzhiCalendar.dayPillar(qimenDate)
        val hourPillar = GanzhiCalendar.hourPillar(dayPillar.stem, slot.branch)
        val xun = XunResolver.resolve(hourPillar)
        val jieqi = try {
            JieqiClock.resolve(localDateTime, request.zoneId)
        } catch (e: Exception) {
            throw QimenError.JieqiResolution(e.message ?: e::class.java.simpleName)
        }
        val futou = FutouYuanResolver.resolve(dayPillar)
        val ju = JuTable.resolve(jieqi.jieqi, jieqi.dun, futou.yuan)
        val earthPlate = EarthPlateBuilder.build(jieqi.dun, ju.ju)
        val duty = DutyMovementResolver.resolve(earthPlate, xun, hourPillar, jieqi.dun)

        QimenChart(
            localDateTime = localDateTime,
            zoneId = request.zoneId,
            qimenDate = qimenDate,
            dayPillar = dayPillar,
            hourPillar = hourPillar,
            xun = xun,
            jieqi = jieqi,
            futou = futou.futou,
            yuan = futou.yuan,
            ju = ju.ju,
            juMethodUsed = request.school.juMethod,
            isWuBuYu = PreflightRules.isWuBuYu(dayPillar.stem, hourPillar.stem),
            earthPlate = earthPlate,
            duty = duty,
        )
    }
}
