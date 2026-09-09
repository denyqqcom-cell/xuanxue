package com.xuanxue.qimen.core.plate

sealed class HumanPlateError(message: String) : IllegalStateException(message) {
    class CenterValueGateUnverified : HumanPlateError(
        "Full human-plate layout is not verified for a value gate currently landing in center palace 5",
    )
}

data class HumanPlate internal constructor(
    private val gatesByPalace: Map<Int, QimenGate>,
) {
    init {
        check(gatesByPalace.keys == OUTER_PALACES) { "Human plate must occupy exactly the eight outer palaces" }
        check(gatesByPalace.values.toSet() == QimenGate.entries.toSet()) { "Human plate must contain all eight gates exactly once" }
    }

    fun gateAt(palace: Int): QimenGate? {
        require(palace in 1..9) { "Palace must be 1..9, got $palace" }
        return gatesByPalace[palace]
    }

    fun asMap(): Map<Int, QimenGate> = gatesByPalace.toSortedMap()

    companion object {
        val OUTER_PALACES: Set<Int> = setOf(1, 2, 3, 4, 6, 7, 8, 9)
    }
}

/**
 * 转盘人盘八门。
 *
 * 已验证的两层运动不能混为一条规则：
 * 1. 值使门的“当前落宫”由 DutyMovementResolver 处理：从旬首遁仪宫起，阳遁宫数递增、阴遁递减；
 * 2. 当值使已经落在外八宫后，其余七门保持固定相邻次序，沿外八宫顺时针环排列。
 *
 * 外八宫顺时针环：1坎 -> 8艮 -> 3震 -> 4巽 -> 9离 -> 2坤 -> 7兑 -> 6乾 -> 1坎。
 * 八门固定次序：休 -> 生 -> 伤 -> 杜 -> 景 -> 死 -> 惊 -> 开 -> 休。
 *
 * 原书明确值使有时会运行到中五，但当前没有找到该时刻的完整八门九宫图；因此值使当前落5时硬锁，
 * 不把“寄二宫”等别层规则自行套到人盘排列。
 */
object HumanPlateBuilder {
    private val clockwisePalaceRing = listOf(1, 8, 3, 4, 9, 2, 7, 6)
    private val gateCycle = listOf(
        QimenGate.XIU,
        QimenGate.SHENG,
        QimenGate.SHANG,
        QimenGate.DU,
        QimenGate.JING_SCENERY,
        QimenGate.SI,
        QimenGate.JING,
        QimenGate.KAI,
    )

    fun build(duty: DutyRuntime): Result<HumanPlate> = runCatching {
        if (duty.valueGatePalace == 5) {
            throw HumanPlateError.CenterValueGateUnverified()
        }

        val palaceStart = clockwisePalaceRing.indexOf(duty.valueGatePalace)
        require(palaceStart >= 0) { "Value gate palace is not on outer ring: ${duty.valueGatePalace}" }
        val gateStart = gateCycle.indexOf(duty.anchor.valueGate)
        check(gateStart >= 0) { "Unknown value gate: ${duty.anchor.valueGate}" }

        val map = buildMap {
            for (offset in 0 until 8) {
                val palace = clockwisePalaceRing[(palaceStart + offset) % 8]
                val gate = gateCycle[(gateStart + offset) % 8]
                put(palace, gate)
            }
        }
        HumanPlate(map)
    }
}
