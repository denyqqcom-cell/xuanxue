package com.xuanxue.app.ui.chart

data class BirthProfile(
    val solarDate: String,
    val timeIndex: Int,
    val gender: String,
    val fixLeap: Boolean,
) {
    val genderLabel: String
        get() = if (gender == "female") "女" else "男"

    val timeLabel: String
        get() = SHICHEN_LABELS.getOrElse(timeIndex) { SHICHEN_LABELS[0] }
}

val SHICHEN_LABELS = listOf(
    "早子时 00:00–01:00",
    "丑时 01:00–03:00",
    "寅时 03:00–05:00",
    "卯时 05:00–07:00",
    "辰时 07:00–09:00",
    "巳时 09:00–11:00",
    "午时 11:00–13:00",
    "未时 13:00–15:00",
    "申时 15:00–17:00",
    "酉时 17:00–19:00",
    "戌时 19:00–21:00",
    "亥时 21:00–23:00",
    "晚子时 23:00–00:00",
)
