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
import com.xuanxue.qimen.core.plate.FullPlateResolution
import com.xuanxue.qimen.core.plate.FullPlateResolver
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
    /** 当前支持的转盘方法已能构造地/天/人/神四层。 */
    FULL_PLATE_RESOLVED_SUPPORTED_METHOD,
    /** 值符或值使当前落中五，缺少清晰完整来源图，因此只返回已经验证的局部层。 */
    FULL_PLATE_LOCKED_CENTER_TARGET,
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
    val fullPlate: FullPlateResolution,
    val plateState: PlateState,
)

/**
 * 当前引擎先完成确定性历法/定局/地盘，再解析值符值使。
 * 当值符和值使都不落中五时，按已由阴阳完整实例复核的转盘规则构造天盘、人盘、神盘；
 * 若命中尚未解决的中五表示边界，则显式返回 Locked，而不是猜一个看似完整的盘。
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
        val fullPlate = FullPlateResolver.resolve(earthPlate, duty, jieqi.dun)
        val plateState = when (fullPlate) {
            is FullPlateResolution.Resolved -> PlateState.FULL_PLATE_RESOLVED_SUPPORTED_METHOD
            is FullPlateResolution.Locked -> PlateState.FULL_PLATE_LOCKED_CENTER_TARGET
        }

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
            fullPlate = fullPlate,
            plateState = plateState,
        )
    }
}
