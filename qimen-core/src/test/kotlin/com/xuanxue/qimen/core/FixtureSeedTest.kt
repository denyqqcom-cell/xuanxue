package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.ClockPolicy
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.GanzhiCalendar
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.ju.JuResolver
import com.xuanxue.qimen.core.plate.Yi
import com.xuanxue.qimen.core.relations.HitXingMap
import com.xuanxue.qimen.core.relations.WuBuYu
import java.time.LocalDate
import java.time.LocalTime
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class FixtureSeedTest {
    private val lines: List<String> = requireNotNull(
        javaClass.classLoader.getResourceAsStream("fixtures.jsonl"),
    ).bufferedReader().use { it.readLines().filter(String::isNotBlank) }

    @Test
    fun `all 17 handoff seed fixtures execute`() {
        assertEquals(17, lines.size)
        lines.forEach { line ->
            when (string(line, "kind")) {
                "calendar" -> {
                    val result = GanzhiCalendar.dayPillar(LocalDate.parse(string(line, "civilDate")))
                    assertEquals(string(line, "dayStem"), result.pillar.stem.symbol, fixtureId(line))
                    assertEquals(string(line, "dayBranch"), result.pillar.branch.symbol, fixtureId(line))
                }
                "hour_pillar" -> {
                    val result = GanzhiCalendar.hourPillar(
                        Stem.fromSymbol(string(line, "dayStem")),
                        Branch.fromSymbol(string(line, "hourBranch")),
                    )
                    assertEquals(string(line, "hourStem"), result.stem.symbol, fixtureId(line))
                }
                "xun" -> {
                    val result = GanzhiCalendar.xun(
                        StemBranch(
                            Stem.fromSymbol(string(line, "hourStem")),
                            Branch.fromSymbol(string(line, "hourBranch")),
                        ),
                    )
                    assertEquals(string(line, "dunYi"), result.dunYi.symbol, fixtureId(line))
                    assertEquals(stringArray(line, "xunKong"), result.xunKong.map { it.symbol }, fixtureId(line))
                }
                "wubuyu" -> {
                    val result = WuBuYu.isWuBuYu(
                        Stem.fromSymbol(string(line, "dayStem")),
                        StemBranch(
                            Stem.fromSymbol(string(line, "hourStem")),
                            Branch.fromSymbol(string(line, "hourBranch")),
                        ),
                    )
                    assertEquals(boolean(line, "isWuBuYu"), result, fixtureId(line))
                }
                "hit_xing" -> {
                    val result = HitXingMap.palaceFor(Yi.fromSymbol(string(line, "yi")))
                    assertEquals(int(line, "xingPalace"), result?.number, fixtureId(line))
                }
                "ju_table" -> {
                    val yuanLabel = string(line, "yuan")
                    val day = when (yuanLabel) { "上" -> 1; "中" -> 6; else -> 11 }
                    val result = JuResolver.resolveDayCount(
                        string(line, "jieqi"),
                        day,
                        Dun.valueOf(string(line, "dun")),
                    )
                    assertEquals(int(line, "ju"), result.ju, fixtureId(line))
                }
                "clock" -> {
                    val result = ClockPolicy.resolve(
                        LocalTime.parse(string(line, "time")),
                        boolean(line, "lateZiRollsToNextDay"),
                    )
                    assertEquals(string(line, "hourBranch"), result.hourBranch.symbol, fixtureId(line))
                    assertEquals(string(line, "slot"), result.slotLabel, fixtureId(line))
                    if (line.contains("\"rollNextDay\"")) {
                        assertEquals(boolean(line, "rollNextDay"), result.rollNextDay, fixtureId(line))
                    }
                }
                else -> error("Unknown fixture kind: ${string(line, "kind")}")
            }
        }
    }

    @Test
    fun `1900 and 2000 anchors agree across deterministic twentieth and twenty-first century sample`() {
        val dates = listOf(
            "1900-01-01", "1912-02-29", "1949-10-01", "1969-07-20",
            "1999-12-31", "2000-01-01", "2008-08-08", "2026-08-07",
            "2049-10-01", "2099-12-31",
        ).map(LocalDate::parse)
        assertTrue(dates.all(GanzhiCalendar::anchorsAgree))
    }

    @Test
    fun `generator preserves the two handoff extras omitted by printed ten`() {
        val jiHours = WuBuYu.generatedHours(Stem.JI).map { it.text }
        val gengHours = WuBuYu.generatedHours(Stem.GENG).map { it.text }
        assertTrue("乙丑" in jiHours)
        assertTrue("乙亥" in jiHours)
        assertTrue("丙子" in gengHours)
        assertTrue("丙戌" in gengHours)
    }

    @Test
    fun `every ju row stays inside one palace group`() {
        val groups = setOf(setOf(1, 4, 7), setOf(2, 5, 8), setOf(3, 6, 9))
        JuResolver.rowsForInvariantTest().forEach { row ->
            assertTrue(row.toSet() in groups, "bad ju row=${row.toList()}")
        }
    }

    private fun fixtureId(line: String) = string(line, "fixture_id")

    private fun string(line: String, key: String): String =
        Regex("\\\"$key\\\"\\s*:\\s*\\\"([^\\\"]*)\\\"")
            .find(line)?.groupValues?.get(1)
            ?: error("missing string key=$key in $line")

    private fun boolean(line: String, key: String): Boolean =
        Regex("\\\"$key\\\"\\s*:\\s*(true|false)")
            .find(line)?.groupValues?.get(1)?.toBooleanStrict()
            ?: error("missing boolean key=$key in $line")

    private fun int(line: String, key: String): Int =
        Regex("\\\"$key\\\"\\s*:\\s*(\\d+)")
            .find(line)?.groupValues?.get(1)?.toInt()
            ?: error("missing int key=$key in $line")

    private fun stringArray(line: String, key: String): List<String> {
        val body = Regex("\\\"$key\\\"\\s*:\\s*\\[([^]]*)]")
            .find(line)?.groupValues?.get(1)
            ?: error("missing array key=$key in $line")
        return Regex("\\\"([^\\\"]+)\\\"").findAll(body).map { it.groupValues[1] }.toList()
    }
}
