package com.xuanxue.qimen.core.calendar

import java.time.LocalDate
import java.time.LocalTime
import java.time.temporal.ChronoUnit

/** Ten heavenly stems in canonical order. */
enum class Stem(val zh: String) {
    JIA("甲"), YI("乙"), BING("丙"), DING("丁"), WU("戊"),
    JI("己"), GENG("庚"), XIN("辛"), REN("壬"), GUI("癸");

    companion object {
        fun fromZh(value: String): Stem = entries.first { it.zh == value }
    }
}

/** Twelve earthly branches in canonical order. */
enum class Branch(val zh: String) {
    ZI("子"), CHOU("丑"), YIN("寅"), MAO("卯"), CHEN("辰"), SI("巳"),
    WU("午"), WEI("未"), SHEN("申"), YOU("酉"), XU("戌"), HAI("亥");

    companion object {
        fun fromZh(value: String): Branch = entries.first { it.zh == value }
    }
}

data class StemBranch(val stem: Stem, val branch: Branch) {
    val zh: String get() = stem.zh + branch.zh

    companion object {
        fun fromSexagenaryIndex(index: Int): StemBranch {
            val normalized = Math.floorMod(index, 60)
            return StemBranch(Stem.entries[normalized % 10], Branch.entries[normalized % 12])
        }

        fun sexagenaryIndexOf(stem: Stem, branch: Branch): Int =
            (0 until 60).firstOrNull { it % 10 == stem.ordinal && it % 12 == branch.ordinal }
                ?: error("Invalid stem-branch pairing: ${stem.zh}${branch.zh}")
    }
}

enum class ZiSlot(val zh: String) { EARLY("早子"), LATE("晚子") }

data class ClockSlot(
    val branch: Branch,
    val ziSlot: ZiSlot? = null,
    val rollNextDay: Boolean = false,
)

object GanzhiCalendar {
    private val anchorDate: LocalDate = LocalDate.of(1900, 1, 1)
    private const val anchorIndex: Int = 10 // 甲戌

    /**
     * Day pillar based on the two-anchor handoff contract:
     * 1900-01-01 = 甲戌, which independently yields 2000-01-01 = 戊午.
     */
    fun dayPillar(date: LocalDate): StemBranch {
        val delta = ChronoUnit.DAYS.between(anchorDate, date)
        val index = Math.floorMod(anchorIndex.toLong() + delta, 60L).toInt()
        return StemBranch.fromSexagenaryIndex(index)
    }

    /** 五鼠遁: 甲己甲、乙庚丙、丙辛戊、丁壬庚、戊癸壬起子。 */
    fun hourPillar(dayStem: Stem, hourBranch: Branch): StemBranch {
        val ziStemIndex = (dayStem.ordinal % 5) * 2
        val hourStem = Stem.entries[(ziStemIndex + hourBranch.ordinal) % 10]
        return StemBranch(hourStem, hourBranch)
    }

    /**
     * Default 13-slot clock used by the handoff: 00:00-00:59 early 子,
     * 23:00-23:59 late 子, with optional qimen-day rollover at late 子.
     */
    fun clockSlot(time: LocalTime, lateZiRollsToNextDay: Boolean = true): ClockSlot {
        val hour = time.hour
        return when (hour) {
            0 -> ClockSlot(Branch.ZI, ZiSlot.EARLY, false)
            1, 2 -> ClockSlot(Branch.CHOU)
            3, 4 -> ClockSlot(Branch.YIN)
            5, 6 -> ClockSlot(Branch.MAO)
            7, 8 -> ClockSlot(Branch.CHEN)
            9, 10 -> ClockSlot(Branch.SI)
            11, 12 -> ClockSlot(Branch.WU)
            13, 14 -> ClockSlot(Branch.WEI)
            15, 16 -> ClockSlot(Branch.SHEN)
            17, 18 -> ClockSlot(Branch.YOU)
            19, 20 -> ClockSlot(Branch.XU)
            21, 22 -> ClockSlot(Branch.HAI)
            23 -> ClockSlot(Branch.ZI, ZiSlot.LATE, lateZiRollsToNextDay)
            else -> error("Invalid hour: $hour")
        }
    }
}
