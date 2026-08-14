package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.GanzhiCalendar
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.rule.PreflightRules
import com.xuanxue.qimen.core.xun.XunResolver
import org.json.JSONObject
import java.time.LocalDate
import java.time.LocalTime
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class QimenCoreFixtureTest {
    private fun fixtures(): List<JSONObject> =
        checkNotNull(javaClass.classLoader.getResourceAsStream("fixtures.jsonl"))
            .bufferedReader()
            .useLines { lines -> lines.filter { it.isNotBlank() }.map(::JSONObject).toList() }

    @Test
    fun handoffFixturesPassForImplementedKinds() {
        fixtures().forEach { fixture ->
            val input = fixture.getJSONObject("input")
            val expected = fixture.getJSONObject("expected")
            when (fixture.getString("kind")) {
                "calendar" -> {
                    val actual = GanzhiCalendar.dayPillar(LocalDate.parse(input.getString("civilDate")))
                    assertEquals(expected.getString("dayStem"), actual.stem.zh, fixture.getString("fixture_id"))
                    assertEquals(expected.getString("dayBranch"), actual.branch.zh, fixture.getString("fixture_id"))
                }
                "hour_pillar" -> {
                    val actual = GanzhiCalendar.hourPillar(
                        Stem.fromZh(input.getString("dayStem")),
                        Branch.fromZh(input.getString("hourBranch")),
                    )
                    assertEquals(expected.getString("hourStem"), actual.stem.zh, fixture.getString("fixture_id"))
                }
                "xun" -> {
                    val info = XunResolver.resolve(
                        StemBranch(
                            Stem.fromZh(input.getString("hourStem")),
                            Branch.fromZh(input.getString("hourBranch")),
                        ),
                    )
                    assertEquals(expected.getString("dunYi"), info.dunYi.zh, fixture.getString("fixture_id"))
                    val expectedKong = expected.getJSONArray("xunKong").let { arr ->
                        (0 until arr.length()).map(arr::getString)
                    }
                    assertEquals(expectedKong, info.xunKong.map { it.zh }, fixture.getString("fixture_id"))
                }
                "wubuyu" -> {
                    val actual = PreflightRules.isWuBuYu(
                        Stem.fromZh(input.getString("dayStem")),
                        Stem.fromZh(input.getString("hourStem")),
                    )
                    assertEquals(expected.getBoolean("isWuBuYu"), actual, fixture.getString("fixture_id"))
                }
                "hit_xing" -> {
                    val actual = PreflightRules.hitXingPalace(Stem.fromZh(input.getString("yi")))
                    assertEquals(expected.getInt("xingPalace"), actual, fixture.getString("fixture_id"))
                }
                "clock" -> {
                    val actual = GanzhiCalendar.clockSlot(
                        LocalTime.parse(input.getString("time")),
                        input.optBoolean("lateZiRollsToNextDay", true),
                    )
                    assertEquals(expected.getString("hourBranch"), actual.branch.zh, fixture.getString("fixture_id"))
                    assertEquals(expected.getString("slot"), actual.ziSlot?.zh, fixture.getString("fixture_id"))
                    if (expected.has("rollNextDay")) {
                        assertEquals(expected.getBoolean("rollNextDay"), actual.rollNextDay, fixture.getString("fixture_id"))
                    }
                }
            }
        }
    }

    @Test
    fun twoAnchorsStayConsistentAcrossModernDates() {
        assertEquals("甲戌", GanzhiCalendar.dayPillar(LocalDate.of(1900, 1, 1)).zh)
        assertEquals("戊午", GanzhiCalendar.dayPillar(LocalDate.of(2000, 1, 1)).zh)
        assertEquals("癸丑", GanzhiCalendar.dayPillar(LocalDate.of(2026, 8, 7)).zh)
    }

    @Test
    fun nonMatchingWuBuYuIsFalse() {
        assertTrue(!PreflightRules.isWuBuYu(Stem.JIA, Stem.XIN))
    }
}
