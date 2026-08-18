package com.xuanxue.qimen.core

import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.plate.EarthPlateBuilder
import kotlin.test.Test
import kotlin.test.assertEquals

class EarthPlateSourceFixtureTest {
    @Test
    fun yangThreeMatchesWorkedSourceExample() {
        val plate = EarthPlateBuilder.build(Dun.YANG, 3)
        val expected = mapOf(
            1 to Stem.BING,
            2 to Stem.YI,
            3 to Stem.WU,
            4 to Stem.JI,
            5 to Stem.GENG,
            6 to Stem.XIN,
            7 to Stem.REN,
            8 to Stem.GUI,
            9 to Stem.DING,
        )
        expected.forEach { (palace, stem) ->
            assertEquals(stem, plate.stemAt(palace), "yang 3 palace $palace")
        }
    }

    @Test
    fun yinThreeMatchesWorkedSourceExample() {
        val plate = EarthPlateBuilder.build(Dun.YIN, 3)
        val expected = mapOf(
            1 to Stem.GENG,
            2 to Stem.JI,
            3 to Stem.WU,
            4 to Stem.YI,
            5 to Stem.BING,
            6 to Stem.DING,
            7 to Stem.GUI,
            8 to Stem.REN,
            9 to Stem.XIN,
        )
        expected.forEach { (palace, stem) ->
            assertEquals(stem, plate.stemAt(palace), "yin 3 palace $palace")
        }
    }

    @Test
    fun allEighteenJuCoverEveryPalaceAndEveryYiQiExactlyOnce() {
        for (dun in Dun.entries) {
            for (ju in 1..9) {
                val plate = EarthPlateBuilder.build(dun, ju)
                assertEquals((1..9).toSet(), plate.cells.map { it.palace }.toSet(), "$dun $ju palaces")
                assertEquals(EarthPlateBuilder.sequence.toSet(), plate.cells.map { it.stem }.toSet(), "$dun $ju stems")
                assertEquals(ju, plate.palaceOf(Stem.WU), "$dun $ju must put Wu at ju palace")
            }
        }
    }
}
