package com.xuanxue.qimen.core.school

enum class JuMethod {
    CHAI_BU_DAYCOUNT,
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
    val juMethod: JuMethod = JuMethod.CHAI_BU_DAYCOUNT,
    val lateZiRollsToNextDay: Boolean = true,
    val useTrueSolarTime: Boolean = false,
    val boardSchool: BoardSchool = BoardSchool.ZHUAN_PAN,
    val personToken: PersonToken = PersonToken.DAY_STEM,
) {
    fun unsupportedFlagOrNull(): String? = when {
        useTrueSolarTime -> "true_solar_time"
        juMethod == JuMethod.CHAI_BU_FUTOU -> "chai_bu_futou"
        juMethod == JuMethod.ZHI_RUN -> "zhi_run"
        juMethod == JuMethod.MAO_SHAN -> "mao_shan"
        boardSchool == BoardSchool.FEI_GONG -> "fei_gong"
        else -> null
    }
}

sealed class QimenError(message: String) : IllegalStateException(message) {
    class UnsupportedSchool(val flag: String) : QimenError("Unsupported qimen school/config: $flag")
    class MissingJieqiClock : QimenError("Jieqi clock is not implemented; full plate generation is intentionally locked")
}
