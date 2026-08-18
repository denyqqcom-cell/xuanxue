package com.xuanxue.qimen.core.plate

import com.xuanxue.qimen.core.calendar.Dun

enum class FullPlateLockReason {
    VALUE_STAR_IN_CENTER,
    VALUE_GATE_IN_CENTER,
}

data class FullPlate(
    val earth: EarthPlate,
    val sky: SkyPlate,
    val human: HumanPlate,
    val spirit: SpiritPlate,
)

sealed interface FullPlateResolution {
    data class Resolved(val plate: FullPlate) : FullPlateResolution
    data class Locked(val reasons: Set<FullPlateLockReason>) : FullPlateResolution
}

/**
 * 只在当前已验证的转盘规则可以完整构造四层盘时返回 Resolved。
 *
 * 当前唯一剩余的结构性硬锁是“值符或值使当前落中五”的完整盘表示：资料已经证明这些情况会发生，
 * 但尚没有足够清晰的对应完整九宫图用于确认天盘/人盘/神盘的表示方式，所以不能静默寄宫。
 */
object FullPlateResolver {
    fun resolve(
        earthPlate: EarthPlate,
        duty: DutyRuntime,
        dun: Dun,
        spiritMethod: SpiritMethod = SpiritMethod.FOLLOW_VALUE_STAR,
    ): FullPlateResolution {
        val reasons = buildSet {
            if (duty.valueStarPalace == 5) add(FullPlateLockReason.VALUE_STAR_IN_CENTER)
            if (duty.valueGatePalace == 5) add(FullPlateLockReason.VALUE_GATE_IN_CENTER)
        }
        if (reasons.isNotEmpty()) {
            return FullPlateResolution.Locked(reasons)
        }

        val sky = SkyPlateBuilder.build(earthPlate, duty).getOrThrow()
        val human = HumanPlateBuilder.build(duty).getOrThrow()
        val spirit = SpiritPlateBuilder.build(duty, dun, spiritMethod).getOrThrow()
        return FullPlateResolution.Resolved(
            FullPlate(
                earth = earthPlate,
                sky = sky,
                human = human,
                spirit = spirit,
            ),
        )
    }
}
