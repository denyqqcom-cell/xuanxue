package com.xuanxue.qimen.core.calendar

import com.xuanxue.qimen.core.plate.Yi
import java.time.LocalDate
import java.time.temporal.ChronoUnit

/** Stable symbolic types. Chinese glyphs are data labels, not copied prose. */
enum class Polarity { YANG, YIN }

enum class FiveElement {
    WOOD, FIRE, EARTH, METAL, WATER;

    fun overcomes(other: FiveElement): Boolean = when (this) {
        WOOD -> other == EARTH
        FIRE -> other == METAL
        EARTH -> other == WATER
        METAL -> other == WOOD
        WATER -> other == FIRE
    }
}

enum class Stem(
    val symbol: String,
    val element: FiveElement,
    val polarity: Polarity,
) {
    JIA("甲", FiveElement.WOOD, Polarity.YANG),
    YI("乙", FiveElement.WOOD, Polarity.YIN),
    BING("丙", FiveElement.FIRE, Polarity.YANG),
    DING("丁", FiveElement.FIRE, Polarity.YIN),
    WU("戊", FiveElement.EARTH, Polarity.YANG),
    JI("己", FiveElement.EARTH, Polarity.YIN),
    GENG("庚", FiveElement.METAL, Polarity.YANG),
    XIN("辛", FiveElement.METAL, Polarity.YIN),
    REN("壬", FiveElement.WATER, Polarity.YANG),
    GUI("癸", FiveElement.WATER, Polarity.YIN),
    ;

    companion object {
        fun fromSymbol(value: String): Stem = entries.first { it.symbol == value }
    }
}

enum class Branch(val symbol: String) {
    ZI("子"), CHOU("丑"), YIN("寅"), MAO("卯"), CHEN("辰"), SI("巳"),
    WU("午"), WEI("未"), SHEN("申"), YOU("酉"), XU("戌"), HAI("亥"),
    ;

    companion object {
        fun fromSymbol(value: String): Branch = entries.first { it.symbol == value }
    }
}

data class StemBranch(val stem: Stem, val branch: Branch) {
    val text: String get() = stem.symbol + branch.symbol
}

data class DayPillarResult(
    val pillar: StemBranch,
    /** 1-based position in the sixty-jiazi cycle. */
    val jiaziIndex: Int,
)

data class XunInfo(
    val xunShou: StemBranch,
    val dunYi: Yi,
    val xunKong: List<Branch>,
)

object SexagenaryCycle {
    val all: List<StemBranch> = List(60) { index ->
        StemBranch(Stem.entries[index % 10], Branch.entries[index % 12])
    }

    fun indexOf(pillar: StemBranch): Int = all.indexOf(pillar)
}

object GanzhiCalendar {
    private val anchor1900Date = LocalDate.of(1900, 1, 1)
    private val anchor1900 = StemBranch(Stem.JIA, Branch.XU)
    private val anchor2000Date = LocalDate.of(2000, 1, 1)
    private val anchor2000 = StemBranch(Stem.WU, Branch.WU)

    fun dayPillar(date: LocalDate): DayPillarResult {
        require(!date.isBefore(anchor1900Date)) { "qimen-core v1 supports civil dates from 1900-01-01" }
        return dayPillarFromAnchor(date, anchor1900Date, anchor1900)
    }

    internal fun dayPillarFromAnchor(
        date: LocalDate,
        anchorDate: LocalDate,
        anchorPillar: StemBranch,
    ): DayPillarResult {
        val anchorIndex = SexagenaryCycle.indexOf(anchorPillar)
        require(anchorIndex >= 0) { "Invalid sexagenary anchor ${anchorPillar.text}" }
        val delta = ChronoUnit.DAYS.between(anchorDate, date)
        val index = Math.floorMod(anchorIndex.toLong() + delta, 60L).toInt()
        return DayPillarResult(SexagenaryCycle.all[index], index + 1)
    }

    /** Independent implementation check required by the handoff. */
    fun anchorsAgree(date: LocalDate): Boolean {
        val from1900 = dayPillarFromAnchor(date, anchor1900Date, anchor1900)
        val from2000 = dayPillarFromAnchor(date, anchor2000Date, anchor2000)
        return from1900.pillar == from2000.pillar
    }

    /** 五鼠遁: choose the stem at 子 by day stem, then walk the 12 branches. */
    fun hourPillar(dayStem: Stem, hourBranch: Branch): StemBranch {
        val ziStemIndex = (dayStem.ordinal % 5) * 2
        val stem = Stem.entries[(ziStemIndex + hourBranch.ordinal) % 10]
        return StemBranch(stem, hourBranch)
    }

    fun xun(hourPillar: StemBranch): XunInfo {
        val index = SexagenaryCycle.indexOf(hourPillar)
        require(index >= 0) { "Hour pillar ${hourPillar.text} is not a valid sixty-jiazi pair" }
        val group = index / 10
        val xunShou = SexagenaryCycle.all[group * 10]
        val dunYi = listOf(Yi.WU, Yi.JI, Yi.GENG, Yi.XIN, Yi.REN, Yi.GUI)[group]
        val xunKong = listOf(
            listOf(Branch.XU, Branch.HAI),
            listOf(Branch.SHEN, Branch.YOU),
            listOf(Branch.WU, Branch.WEI),
            listOf(Branch.CHEN, Branch.SI),
            listOf(Branch.YIN, Branch.MAO),
            listOf(Branch.ZI, Branch.CHOU),
        )[group]
        return XunInfo(xunShou, dunYi, xunKong)
    }
}
