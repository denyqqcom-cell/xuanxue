package com.xuanxue.app.ui.qimen

import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.calendar.JieqiClock
import java.time.Instant
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter

/**
 * Android 输入层只负责把用户明确输入的北京时间转换为 core request。
 * 不读取设备时区去偷偷改写用户选择；当前 qimen-core v1 只支持 Asia/Shanghai。
 */
object QimenCastInput {
    const val ZONE_ID: String = JieqiClock.SUPPORTED_ZONE

    data class DisplayValue(
        val dateText: String,
        val timeText: String,
    )

    sealed class InputError(message: String) : IllegalArgumentException(message) {
        class InvalidDate(value: String) : InputError("日期格式或日期无效：$value；请使用 YYYY-MM-DD")
        class InvalidTime(value: String) : InputError("时间格式或时间无效：$value；请使用 HH:mm（00:00-23:59）")
    }

    private val dateRegex = Regex("^\\d{4}-\\d{2}-\\d{2}$")
    private val timeRegex = Regex("^\\d{2}:\\d{2}$")
    private val dateFormatter = DateTimeFormatter.ofPattern("uuuu-MM-dd")
    private val timeFormatter = DateTimeFormatter.ofPattern("HH:mm")

    fun toRequest(dateText: String, timeText: String): Result<QimenRequest> = runCatching {
        val dateValue = dateText.trim()
        val timeValue = timeText.trim()

        if (!dateRegex.matches(dateValue)) throw InputError.InvalidDate(dateValue)
        if (!timeRegex.matches(timeValue)) throw InputError.InvalidTime(timeValue)

        val date = try {
            LocalDate.parse(dateValue, dateFormatter)
        } catch (_: Exception) {
            throw InputError.InvalidDate(dateValue)
        }
        val time = try {
            LocalTime.parse(timeValue, timeFormatter)
        } catch (_: Exception) {
            throw InputError.InvalidTime(timeValue)
        }

        val epochMs = LocalDateTime.of(date, time)
            .atZone(ZoneId.of(ZONE_ID))
            .toInstant()
            .toEpochMilli()

        QimenRequest(
            instantEpochMs = epochMs,
            zoneId = ZONE_ID,
        )
    }

    fun displayForEpochMs(epochMs: Long): DisplayValue {
        val local = Instant.ofEpochMilli(epochMs)
            .atZone(ZoneId.of(ZONE_ID))
            .toLocalDateTime()
        return DisplayValue(
            dateText = local.toLocalDate().format(dateFormatter),
            timeText = local.toLocalTime().format(timeFormatter),
        )
    }
}
