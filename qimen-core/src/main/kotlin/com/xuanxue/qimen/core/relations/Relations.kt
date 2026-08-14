package com.xuanxue.qimen.core.relations

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.GanzhiCalendar
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.plate.PalaceId
import com.xuanxue.qimen.core.plate.Yi

enum class WuBuYuMethod { GENERATOR, SHANTIANDAO_PRINTED }

object WuBuYu {
    /**
     * Generator school: hour stem overcomes day stem and shares polarity.
     * We also verify that the supplied hour pillar is the 五鼠遁 result for that day/branch,
     * so an impossible stem-branch combination cannot become a false positive.
     */
    fun isWuBuYu(
        dayStem: Stem,
        hourPillar: StemBranch,
        method: WuBuYuMethod = WuBuYuMethod.GENERATOR,
    ): Boolean {
        val actualHour = GanzhiCalendar.hourPillar(dayStem, hourPillar.branch)
        if (actualHour != hourPillar) return false
        return when (method) {
            WuBuYuMethod.GENERATOR ->
                hourPillar.stem.element.overcomes(dayStem.element) &&
                    hourPillar.stem.polarity == dayStem.polarity

            WuBuYuMethod.SHANTIANDAO_PRINTED ->
                PrintedPair(dayStem, hourPillar) in printedTen
        }
    }

    fun generatedHours(dayStem: Stem): List<StemBranch> = Branch.entries
        .map { GanzhiCalendar.hourPillar(dayStem, it) }
        .filter { isWuBuYu(dayStem, it, WuBuYuMethod.GENERATOR) }

    private data class PrintedPair(val dayStem: Stem, val hour: StemBranch)

    /** Ten factual pairs from the handoff notes; kept as an optional comparison school. */
    private val printedTen = setOf(
        PrintedPair(Stem.JIA, StemBranch(Stem.GENG, Branch.WU)),
        PrintedPair(Stem.YI, StemBranch(Stem.XIN, Branch.SI)),
        PrintedPair(Stem.BING, StemBranch(Stem.REN, Branch.CHEN)),
        PrintedPair(Stem.DING, StemBranch(Stem.GUI, Branch.MAO)),
        PrintedPair(Stem.WU, StemBranch(Stem.JIA, Branch.YIN)),
        PrintedPair(Stem.JI, StemBranch(Stem.YI, Branch.CHOU)),
        PrintedPair(Stem.GENG, StemBranch(Stem.BING, Branch.ZI)),
        PrintedPair(Stem.XIN, StemBranch(Stem.DING, Branch.YOU)),
        PrintedPair(Stem.REN, StemBranch(Stem.WU, Branch.SHEN)),
        PrintedPair(Stem.GUI, StemBranch(Stem.JI, Branch.WEI)),
    )
}

object HitXingMap {
    private val map = mapOf(
        Yi.WU to PalaceId.ZHEN_3,
        Yi.JI to PalaceId.KUN_2,
        Yi.GENG to PalaceId.GEN_8,
        Yi.XIN to PalaceId.LI_9,
        Yi.REN to PalaceId.XUN_4,
        Yi.GUI to PalaceId.XUN_4,
    )

    fun palaceFor(yi: Yi): PalaceId? = map[yi]
}
