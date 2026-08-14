package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.JieqiClock
import java.time.Instant
import java.time.ZoneId
import kotlin.test.Test
import kotlin.test.assertEquals

class JieqiClockTest {
    private val shanghai = ZoneId.of("Asia/Shanghai")

    /**
     * lunar-java upstream JieQiTest publishes 2022-08-07 20:29:08 as 立秋.
     * This is an external library boundary test, not a book-derived qimen fixture.
     */
    @Test
    fun `jieqi flips at tested astronomical boundary instead of rounded civil date`() {
        val before = JieqiClock.resolve(Instant.parse("2022-08-07T12:29:07Z"), shanghai)
        val at = JieqiClock.resolve(Instant.parse("2022-08-07T12:29:08Z"), shanghai)

        assertEquals("大暑", before.name)
        assertEquals("立秋", at.name)
        assertEquals(Dun.YIN, at.dun)
        assertEquals(1, at.dayIndex)
        assertEquals(0L, at.secondsSinceStart)
    }

    @Test
    fun `jieqi day count is local civil date based`() {
        val nextDay = JieqiClock.resolve(Instant.parse("2022-08-08T04:00:00Z"), shanghai)
        assertEquals("立秋", nextDay.name)
        assertEquals(2, nextDay.dayIndex)
    }
}
