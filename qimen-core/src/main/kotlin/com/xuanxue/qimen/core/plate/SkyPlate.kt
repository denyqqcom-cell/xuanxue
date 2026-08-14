package com.xuanxue.qimen.core.plate

import com.xuanxue.qimen.core.calendar.Stem

sealed class SkyPlateError(message: String) : IllegalStateException(message) {
    class CenterValueStarUnverified : SkyPlateError(
        "Full sky-plate layout is not verified for a value star currently landing in center palace 5",
    )
}

data class SkyStarPlacement(
    val star: QimenStar,
    /** 此星从原驻地盘宫随天盘旋转时携带的六仪三奇。 */
    val carriedStem: Stem,
    val homePalace: Int,
)

data class SkyPlate internal constructor(
    private val placementsByPalace: Map<Int, List<SkyStarPlacement>>,
) {
    init {
        check(placementsByPalace.keys == HumanPlate.OUTER_PALACES) { "Sky plate must occupy exactly the eight outer palaces" }
        val flattened = placementsByPalace.values.flatten()
        check(flattened.size == 9) { "Sky plate must contain nine stars including hosted Tian-Qin" }
        check(flattened.map { it.star }.toSet() == QimenStar.entries.toSet()) { "Sky plate must contain every star exactly once" }
        check(flattened.map { it.homePalace }.toSet() == (1..9).toSet()) { "Sky plate must carry all nine earth-palace stems exactly once" }
    }

    fun placementsAt(palace: Int): List<SkyStarPlacement> {
        require(palace in 1..9) { "Palace must be 1..9, got $palace" }
        return placementsByPalace[palace].orEmpty()
    }

    fun starsAt(palace: Int): List<QimenStar> = placementsAt(palace).map { it.star }

    fun carriedStemsAt(palace: Int): List<Stem> = placementsAt(palace).map { it.carriedStem }

    fun asMap(): Map<Int, List<SkyStarPlacement>> = placementsByPalace.toSortedMap()
}

/**
 * 转盘天盘九星与随星携带的天盘六仪三奇。
 *
 * 当前来源复核支持：中五天禽通常寄坤二，与天芮作为同一旋转组；因此天盘按八个外宫星组旋转。
 * 外八宫顺时针环：1坎 -> 8艮 -> 3震 -> 4巽 -> 9离 -> 2坤 -> 7兑 -> 6乾 -> 1坎。
 * 原驻星组依该环为：蓬 -> 任 -> 冲 -> 辅 -> 英 -> (芮+禽) -> 柱 -> 心。
 *
 * 每颗星携带它原驻地盘宫当局的六仪三奇一起旋转；芮来自坤二，禽来自中五，两者寄在同一目标宫。
 * 值符先由 DutyMovementResolver 按时干确定当前落宫，之后其余星组保持固定相邻次序沿外八宫顺时针铺开。
 *
 * 若值符当前恰落中五，当前资料尚无足够清晰的完整天盘实例确认如何表示，因此硬锁而不猜。
 */
object SkyPlateBuilder {
    private data class HomeStar(val star: QimenStar, val homePalace: Int)

    private val clockwisePalaceRing = listOf(1, 8, 3, 4, 9, 2, 7, 6)
    private val starGroups = listOf(
        listOf(HomeStar(QimenStar.TIAN_PENG, 1)),
        listOf(HomeStar(QimenStar.TIAN_REN, 8)),
        listOf(HomeStar(QimenStar.TIAN_CHONG, 3)),
        listOf(HomeStar(QimenStar.TIAN_FU, 4)),
        listOf(HomeStar(QimenStar.TIAN_YING, 9)),
        listOf(
            HomeStar(QimenStar.TIAN_RUI, 2),
            HomeStar(QimenStar.TIAN_QIN, 5),
        ),
        listOf(HomeStar(QimenStar.TIAN_ZHU, 7)),
        listOf(HomeStar(QimenStar.TIAN_XIN, 6)),
    )

    fun build(earthPlate: EarthPlate, duty: DutyRuntime): Result<SkyPlate> = runCatching {
        if (duty.valueStarPalace == 5) {
            throw SkyPlateError.CenterValueStarUnverified()
        }
        val palaceStart = clockwisePalaceRing.indexOf(duty.valueStarPalace)
        require(palaceStart >= 0) { "Value star palace is not on outer ring: ${duty.valueStarPalace}" }
        val groupStart = starGroups.indexOfFirst { group -> group.any { it.star == duty.anchor.valueStar } }
        check(groupStart >= 0) { "Value star has no rotating group: ${duty.anchor.valueStar}" }

        val map = buildMap {
            for (offset in 0 until 8) {
                val palace = clockwisePalaceRing[(palaceStart + offset) % 8]
                val group = starGroups[(groupStart + offset) % 8]
                put(
                    palace,
                    group.map { home ->
                        SkyStarPlacement(
                            star = home.star,
                            carriedStem = earthPlate.stemAt(home.homePalace),
                            homePalace = home.homePalace,
                        )
                    },
                )
            }
        }
        SkyPlate(map)
    }
}
