package com.xuanxue.qimen.core.plate

import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch
import com.xuanxue.qimen.core.xun.XunInfo

data class DutyRuntime(
    val anchor: DutyAnchor,
    /** 值符星按时干在地盘所落之宫定位；甲时以本旬遁仪代甲。 */
    val valueStarPalace: Int,
    /** 值使按旬首时支起点，阳顺阴逆，每个时辰移动一宫。中五只记录宫数，不在此猜寄宫。 */
    val valueGatePalace: Int?,
    val branchStepsFromXunHead: Int,
)

object DutyMovementResolver {
    fun resolve(
        earthPlate: EarthPlate,
        xun: XunInfo,
        hourPillar: StemBranch,
        dun: Dun,
    ): DutyRuntime {
        val anchor = DutyAnchorResolver.resolve(earthPlate, xun)

        val effectiveHourStem = if (hourPillar.stem == Stem.JIA) xun.dunYi else hourPillar.stem
        val starPalace = earthPlate.palaceOf(effectiveHourStem)
            ?: error("Effective hour stem ${effectiveHourStem.zh} is missing from earth plate")

        val branchSteps = Math.floorMod(
            hourPillar.branch.ordinal - xun.xunShou.branch.ordinal,
            12,
        )
        require(branchSteps in 0..9) {
            "Hour ${hourPillar.zh} is not inside resolved xun ${xun.xunShou.zh}; steps=$branchSteps"
        }

        val gatePalace = if (anchor.valueGate == null) {
            null
        } else {
            val signedSteps = if (dun == Dun.YANG) branchSteps else -branchSteps
            Math.floorMod((anchor.dunYiPalace - 1) + signedSteps, 9) + 1
        }

        return DutyRuntime(
            anchor = anchor,
            valueStarPalace = starPalace,
            valueGatePalace = gatePalace,
            branchStepsFromXunHead = branchSteps,
        )
    }
}
