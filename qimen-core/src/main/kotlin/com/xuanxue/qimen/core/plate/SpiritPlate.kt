package com.xuanxue.qimen.core.plate

import com.xuanxue.qimen.core.calendar.Dun

enum class QimenSpirit(val zh: String) {
    VALUE_SYMBOL("值符"),
    TENG_SHE("螣蛇"),
    TAI_YIN("太阴"),
    LIU_HE("六合"),
    BAI_HU("白虎"),
    XUAN_WU("玄武"),
    JIU_DI("九地"),
    JIU_TIAN("九天"),
}

enum class SpiritMethod {
    /** 小值符逐时追随天盘大值符；当前完整阴阳实例支持的方法。 */
    FOLLOW_VALUE_STAR,
    /** 资料另载“每旬移动一宫”的地盘八神法；尚未建立独立夹具，因此只保留方法标识。 */
    PER_XUN_GROUND_SPIRITS,
}

sealed class SpiritPlateError(message: String) : IllegalStateException(message) {
    class UnsupportedMethod(method: SpiritMethod) : SpiritPlateError("Spirit method is not verified yet: $method")
    class CenterValueStarUnverified : SpiritPlateError(
        "Spirit layout is not verified for a value star currently landing in center palace 5",
    )
}

data class SpiritPlate internal constructor(
    val method: SpiritMethod,
    private val spiritsByPalace: Map<Int, QimenSpirit>,
) {
    init {
        check(spiritsByPalace.keys == HumanPlate.OUTER_PALACES) { "Spirit plate must occupy exactly the eight outer palaces" }
        check(spiritsByPalace.values.toSet() == QimenSpirit.entries.toSet()) { "Spirit plate must contain all eight spirits exactly once" }
    }

    fun spiritAt(palace: Int): QimenSpirit? {
        require(palace in 1..9) { "Palace must be 1..9, got $palace" }
        return spiritsByPalace[palace]
    }

    fun asMap(): Map<Int, QimenSpirit> = spiritsByPalace.toSortedMap()
}

/**
 * 神盘采用显式 school/method，不把不同传承静默合并。
 *
 * FOLLOW_VALUE_STAR：小值符与大值符同宫；固定次序为
 * 值符 -> 螣蛇 -> 太阴 -> 六合 -> 白虎 -> 玄武 -> 九地 -> 九天。
 * 阳遁沿外八宫顺时针，阴遁沿外八宫逆时针。
 *
 * 另一种“每旬移动一宫”的地盘八神法目前不编码，只保留 method id 并硬拒绝。
 */
object SpiritPlateBuilder {
    private val clockwisePalaceRing = listOf(1, 8, 3, 4, 9, 2, 7, 6)
    private val spiritCycle = QimenSpirit.entries.toList()

    fun build(
        duty: DutyRuntime,
        dun: Dun,
        method: SpiritMethod = SpiritMethod.FOLLOW_VALUE_STAR,
    ): Result<SpiritPlate> = runCatching {
        if (method != SpiritMethod.FOLLOW_VALUE_STAR) {
            throw SpiritPlateError.UnsupportedMethod(method)
        }
        if (duty.valueStarPalace == 5) {
            throw SpiritPlateError.CenterValueStarUnverified()
        }

        val start = clockwisePalaceRing.indexOf(duty.valueStarPalace)
        require(start >= 0) { "Value star palace is not on outer ring: ${duty.valueStarPalace}" }
        val direction = if (dun == Dun.YANG) 1 else -1

        val map = buildMap {
            for (offset in spiritCycle.indices) {
                val ringIndex = Math.floorMod(start + direction * offset, clockwisePalaceRing.size)
                put(clockwisePalaceRing[ringIndex], spiritCycle[offset])
            }
        }
        SpiritPlate(method, map)
    }
}
