package com.xuanxue.qimen.core.plate

import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem

/** 地盘一个宫位当前承载的六仪/三奇。 */
data class EarthPlateCell(
    val palace: Int,
    val stem: Stem,
)

data class EarthPlate(
    val dun: Dun,
    val ju: Int,
    val cells: List<EarthPlateCell>,
) {
    init {
        require(ju in 1..9) { "ju must be 1..9, got $ju" }
        require(cells.size == 9) { "earth plate must contain 9 cells" }
        require(cells.map { it.palace }.toSet() == (1..9).toSet()) {
            "earth plate must cover palaces 1..9 exactly once"
        }
        require(cells.map { it.stem }.toSet().size == 9) {
            "earth plate must contain 9 unique yi/qi stems"
        }
    }

    fun stemAt(palace: Int): Stem =
        cells.firstOrNull { it.palace == palace }?.stem
            ?: error("No earth stem at palace $palace")

    fun palaceOf(stem: Stem): Int? = cells.firstOrNull { it.stem == stem }?.palace
}

/**
 * 时家排宫法地盘九仪。
 *
 * 已直接复核的两份资料共同支持：
 * - 次序固定为 戊己庚辛壬癸丁丙乙；
 * - “几局”即戊落几宫；
 * - 阳遁按宫数 1→9 顺排并循环，阴遁按宫数逆排并循环。
 *
 * 这里刻意只实现地盘。天盘九星、人盘八门、神盘八神不从该规则外推。
 */
object EarthPlateBuilder {
    val sequence: List<Stem> = listOf(
        Stem.WU,
        Stem.JI,
        Stem.GENG,
        Stem.XIN,
        Stem.REN,
        Stem.GUI,
        Stem.DING,
        Stem.BING,
        Stem.YI,
    )

    fun build(dun: Dun, ju: Int): EarthPlate {
        require(ju in 1..9) { "ju must be 1..9, got $ju" }

        val cells = sequence.mapIndexed { index, stem ->
            val signedOffset = if (dun == Dun.YANG) index else -index
            val palace = Math.floorMod((ju - 1) + signedOffset, 9) + 1
            EarthPlateCell(palace = palace, stem = stem)
        }.sortedBy { it.palace }

        return EarthPlate(dun = dun, ju = ju, cells = cells)
    }
}
