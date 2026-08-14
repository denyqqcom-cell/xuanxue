package com.xuanxue.qimen.core.school

enum class JuMethod {
    /** 直接按节气后的第 1-5/6-10/11-15 日切上中下元；直接复核原书后不再作为默认。 */
    CHAI_BU_DAYCOUNT,

    /** 交节立即换节气，但上中下元仍按最近甲/己日符头确定。 */
    CHAI_BU_FUTOU,
    ZHI_RUN,
    MAO_SHAN,
}

enum class BoardSchool {
    ZHUAN_PAN,
    FEI_GONG,
}

enum class PersonToken {
    DAY_STEM,
    YEAR_PILLAR,
}

data class QimenSchoolConfig(
    val juMethod: JuMethod = JuMethod.CHAI_BU_FUTOU,
    val lateZiRollsToNextDay: Boolean = true,
    val useTrueSolarTime: Boolean = false,
    val boardSchool: BoardSchool = BoardSchool.ZHUAN_PAN,
    val personToken: PersonToken = PersonToken.DAY_STEM,
) {
    fun unsupportedFlagOrNull(): String? = when {
        useTrueSolarTime -> "true_solar_time"
        juMethod == JuMethod.CHAI_BU_DAYCOUNT -> "chai_bu_daycount_unverified"
        juMethod == JuMethod.ZHI_RUN -> "zhi_run"
        juMethod == JuMethod.MAO_SHAN -> "mao_shan"
        boardSchool == BoardSchool.FEI_GONG -> "fei_gong"
        else -> null
    }
}

sealed class QimenError(message: String) : IllegalStateException(message) {
    class UnsupportedSchool(val flag: String) : QimenError("Unsupported qimen school/config: $flag")
    class UnsupportedZone(val zoneId: String) : QimenError("Unsupported qimen timezone in v1: $zoneId")
    class JieqiResolution(val detail: String) : QimenError("Unable to resolve jieqi: $detail")
    class PlateNotVerified : QimenError("Nine-palace plate is intentionally locked until full-board fixtures exist")
}
