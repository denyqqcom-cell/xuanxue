package com.xuanxue.qimen.core.plate

sealed class SkyPlateError(message: String) : IllegalStateException(message) {
    class CenterValueStarUnverified : SkyPlateError(
        "Full sky-plate layout is not verified for a value star currently landing in center palace 5",
    )
}

data class SkyPlate internal constructor(
    private val starsByPalace: Map<Int, List<QimenStar>>,
) {
    init {
        check(starsByPalace.keys == HumanPlate.OUTER_PALACES) { "Sky plate must occupy exactly the eight outer palaces" }
        val flattened = starsByPalace.values.flatten()
        check(flattened.size == 9) { "Sky plate must contain nine stars including hosted Tian-Qin" }
        check(flattened.toSet() == QimenStar.entries.toSet()) { "Sky plate must contain every star exactly once" }
    }

    fun starsAt(palace: Int): List<QimenStar> {
        require(palace in 1..9) { "Palace must be 1..9, got $palace" }
        return starsByPalace[palace].orEmpty()
    }

    fun asMap(): Map<Int, List<QimenStar>> = starsByPalace.toSortedMap()
}

/**
 * 转盘天盘九星。
 *
 * 当前来源复核支持：中五天禽通常寄坤二，与天芮作为同一旋转组；因此天盘实际按八个外宫星组旋转。
 * 外八宫顺时针环：1坎 -> 8艮 -> 3震 -> 4巽 -> 9离 -> 2坤 -> 7兑 -> 6乾 -> 1坎。
 * 原驻星组依该环为：蓬 -> 任 -> 冲 -> 辅 -> 英 -> (芮+禽) -> 柱 -> 心。
 *
 * 值符星先由 DutyMovementResolver 按时干确定当前落宫；随后它所属星组落在该外宫，
 * 其余星组保持固定相邻次序，沿外八宫顺时针铺开。
 *
 * 若值符当前恰落中五，当前资料尚无一张足够清晰的完整天盘实例确认如何表示，因此硬锁而不猜。
 */
object SkyPlateBuilder {
    private val clockwisePalaceRing = listOf(1, 8, 3, 4, 9, 2, 7, 6)
    private val starGroups = listOf(
        listOf(QimenStar.TIAN_PENG),
        listOf(QimenStar.TIAN_REN),
        listOf(QimenStar.TIAN_CHONG),
        listOf(QimenStar.TIAN_FU),
        listOf(QimenStar.TIAN_YING),
        listOf(QimenStar.TIAN_RUI, QimenStar.TIAN_QIN),
        listOf(QimenStar.TIAN_ZHU),
        listOf(QimenStar.TIAN_XIN),
    )

    fun build(duty: DutyRuntime): Result<SkyPlate> = runCatching {
        if (duty.valueStarPalace == 5) {
            throw SkyPlateError.CenterValueStarUnverified()
        }
        val palaceStart = clockwisePalaceRing.indexOf(duty.valueStarPalace)
        require(palaceStart >= 0) { "Value star palace is not on outer ring: ${duty.valueStarPalace}" }
        val groupStart = starGroups.indexOfFirst { duty.anchor.valueStar in it }
        check(groupStart >= 0) { "Value star has no rotating group: ${duty.anchor.valueStar}" }

        val map = buildMap {
            for (offset in 0 until 8) {
                val palace = clockwisePalaceRing[(palaceStart + offset) % 8]
                val group = starGroups[(groupStart + offset) % 8]
                put(palace, group)
            }
        }
        SkyPlate(map)
    }
}
