package com.xuanxue.qimen.core.school

import com.xuanxue.qimen.core.ju.JuMethod

enum class BoardSchool { ZHUAN_PAN, FEI_GONG }
enum class PersonToken { DAY_STEM, YEAR_PILLAR }

data class QimenSchoolConfig(
    val juMethod: JuMethod = JuMethod.CHAI_BU_DAYCOUNT,
    val lateZiRollsToNextDay: Boolean = true,
    val useTrueSolarTime: Boolean = false,
    val boardSchool: BoardSchool = BoardSchool.ZHUAN_PAN,
    val personToken: PersonToken = PersonToken.DAY_STEM,
) {
    companion object {
        val Default = QimenSchoolConfig()
    }
}
