package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Jieqi
import com.xuanxue.qimen.core.calendar.JieqiClock
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.ju.FutouYuanResolver
import com.xuanxue.qimen.core.ju.JuTable
import com.xuanxue.qimen.core.ju.Yuan
import com.xuanxue.qimen.core.school.JuMethod
import com.xuanxue.qimen.core.school.QimenSchoolConfig
import java.time.LocalDateTime
import kotlin.test.Test
import kotlin.test.assertEquals

class QimenJieqiJuTest {
    @Test
    fun jieqiChangesAtExactLibraryBoundary() {
        val beforeLiqiu = JieqiClock.resolve(LocalDateTime.of(2022, 8, 7, 20, 29, 7))
        val atLiqiu = JieqiClock.resolve(LocalDateTime.of(2022, 8, 7, 20, 29, 8))
        assertEquals(Jieqi.DA_SHU, beforeLiqiu.jieqi)
        assertEquals(Jieqi.LI_QIU, atLiqiu.jieqi)
        assertEquals(Dun.YIN, atLiqiu.dun)
        assertEquals(1, atLiqiu.civilDayIndex)
        assertEquals(0L, atLiqiu.secondsSinceStart)

        val beforeLichun = JieqiClock.resolve(LocalDateTime.of(2022, 2, 4, 4, 50, 46))
        val atLichun = JieqiClock.resolve(LocalDateTime.of(2022, 2, 4, 4, 50, 47))
        assertEquals(Jieqi.DA_HAN, beforeLichun.jieqi)
        assertEquals(Jieqi.LI_CHUN, atLichun.jieqi)
        assertEquals(Dun.YANG, atLichun.dun)
    }

    @Test
    fun futouDeterminesYuanInsteadOfTermDayNumber() {
        val guichou = StemBranch(Stem.GUI, Branch.CHOU)
        val a = FutouYuanResolver.resolve(guichou)
        assertEquals("己酉", a.futou.zh)
        assertEquals(Yuan.SHANG, a.yuan)
        assertEquals(4, a.daysBack)
        assertEquals(8, JuTable.resolve(Jieqi.LI_CHUN, Dun.YANG, a.yuan).ju)

        val xinwei = StemBranch(Stem.XIN, Branch.WEI)
        val b = FutouYuanResolver.resolve(xinwei)
        assertEquals("己巳", b.futou.zh)
        assertEquals(Yuan.ZHONG, b.yuan)
        assertEquals(2, b.daysBack)
        assertEquals(5, JuTable.resolve(Jieqi.LI_CHUN, Dun.YANG, b.yuan).ju)
    }

    @Test
    fun allJuRowsStayWithinOneToNine() {
        Jieqi.entries.forEach { term ->
            val dun = JieqiClock.dunFor(term)
            Yuan.entries.forEach { yuan ->
                val ju = JuTable.resolve(term, dun, yuan).ju
                check(ju in 1..9)
            }
        }
    }

    @Test
    fun sourceReviewedDefaultIsFutouChaibu() {
        val school = QimenSchoolConfig()
        assertEquals(JuMethod.CHAI_BU_FUTOU, school.juMethod)
        assertEquals(null, school.unsupportedFlagOrNull())
        assertEquals(
            "chai_bu_daycount_unverified",
            QimenSchoolConfig(juMethod = JuMethod.CHAI_BU_DAYCOUNT).unsupportedFlagOrNull(),
        )
    }
}
