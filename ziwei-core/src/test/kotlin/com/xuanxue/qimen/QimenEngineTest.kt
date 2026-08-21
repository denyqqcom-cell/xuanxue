package com.xuanxue.qimen

import org.json.JSONObject
import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue

class QimenEngineTest {

    private data class LiangJiaziFixture(
        val fixtureId: String,
        val polarity: String,
        val bureau: Int,
        val expectedStar: String,
        val expectedDoor: String,
    )

    private fun fixtureFile(): File {
        val relative = "knowledge/K2_SOURCE_FIXTURES/QM-SRC-0001_BUREAU_INDEX.jsonl"
        val candidates = listOf(
            File(relative),
            File("../$relative"),
        )
        return candidates.firstOrNull { it.isFile }
            ?: error("Liang fixture not found from user.dir=${System.getProperty("user.dir")}")
    }

    private fun normalizeStar(value: String): String = value
        .replace("衝", "冲")
        .replace("輔", "辅")

    private fun normalizeDoor(value: String): String = when (value) {
        "休" -> "休门"
        "生" -> "生门"
        "傷" -> "伤门"
        "杜" -> "杜门"
        "景" -> "景门"
        "死" -> "死门"
        "驚" -> "惊门"
        "開" -> "开门"
        else -> error("unexpected fixture door value=$value")
    }

    private fun loadLiangJiaziFixtures(): List<LiangJiaziFixture> = fixtureFile()
        .readLines()
        .filter { it.isNotBlank() }
        .map { raw ->
            val row = JSONObject(raw)
            val anchors = row.getJSONArray("anchors")
            var star: String? = null
            var door: String? = null
            for (i in 0 until anchors.length()) {
                val anchor = anchors.getJSONObject(i)
                when (anchor.getString("locator")) {
                    "MAIN_TABLE/甲子/TOP_STAR_HEADER" -> star = normalizeStar(anchor.getString("value"))
                    "MAIN_TABLE/甲子/BOTTOM_DOOR_FOOTER" -> door = normalizeDoor(anchor.getString("value"))
                }
            }
            LiangJiaziFixture(
                fixtureId = row.getString("fixture_id"),
                polarity = row.getString("polarity"),
                bureau = row.getInt("bureau"),
                expectedStar = requireNotNull(star) { "missing star anchor: ${row.getString("fixture_id")}" },
                expectedDoor = requireNotNull(door) { "missing door anchor: ${row.getString("fixture_id")}" },
            )
        }

    @Test
    fun liangJiaziSparseAnchorsMatchProductionChiefIdentity() {
        val fixtures = loadLiangJiaziFixtures()
        assertEquals(18, fixtures.size)

        fixtures.forEach { fixture ->
            val yinYang = if (fixture.polarity == "YANG") 1 else -1
            val di = QimenEngine.buildDiPan(yinYang, fixture.bureau)

            // 甲子旬遁戊；source fixture 的 bureau lookup 先要求戊确实落局数宫。
            val dunPalace = di.entries.single { it.value == "戊" }.key
            assertEquals(fixture.bureau, dunPalace, "${fixture.fixtureId}: 戊落宫")

            val actual = QimenEngine.chiefIdentityForDunPalace(dunPalace)
            val expected = fixture.expectedStar to fixture.expectedDoor
            assertEquals(expected, actual, "${fixture.fixtureId}: 甲子值符/值使 sparse anchors")
        }
    }

    @Test
    fun liangJiaziWrongBureauNegativeControlFailsClosed() {
        val fixtures = loadLiangJiaziFixtures()
        val expectedByBureau = fixtures
            .groupBy { it.bureau }
            .mapValues { (_, rows) -> rows.first().expectedStar to rows.first().expectedDoor }

        for (bureau in 1..9) {
            val correct = QimenEngine.chiefIdentityForDunPalace(bureau)
            val wrongBureau = bureau % 9 + 1
            val wrongOracle = requireNotNull(expectedByBureau[wrongBureau])
            assertNotEquals(wrongOracle, correct, "bureau=$bureau must reject wrong-bureau oracle=$wrongBureau")
        }
    }

    @Test
    fun liangJiaziPermutedAnchorNegativeControlFailsClosed() {
        val fixtures = loadLiangJiaziFixtures()
        val expectedByBureau = fixtures
            .groupBy { it.bureau }
            .mapValues { (_, rows) -> rows.first().expectedStar to rows.first().expectedDoor }

        for (bureau in 1..9) {
            val correct = QimenEngine.chiefIdentityForDunPalace(bureau)
            val starFrom = bureau % 9 + 1
            val doorFrom = (bureau + 1) % 9 + 1
            val permuted = requireNotNull(expectedByBureau[starFrom]).first to requireNotNull(expectedByBureau[doorFrom]).second
            assertNotEquals(permuted, correct, "bureau=$bureau must reject permuted star/door anchors")
        }
    }

    @Test
    fun bureauFiveChiefDoorUsesSourceBackedDeathGateIdentity() {
        assertEquals("天禽" to "死门", QimenEngine.chiefIdentityForDunPalace(5))
    }

    @Test
    fun alignUserScript() {
        // 对齐用户本地脚本案例：2026-08-12 申时(15:37)，立秋后 → 阴遁；此测试不授予完整九宫夹具信用。
        val c = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        println("QM1 节气=${c.jieQi} ${c.juText} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}")
        println("QM1 旬首=${c.xunShou} 遁干=${c.dunGan} 旬空=${c.xunKong} 值符=${c.zhiFu} 值使=${c.zhiShi} 马星=${c.maXing}")
        assertEquals("立秋", c.jieQi)
        assertEquals(-1, c.yinYang)
        assertEquals(5, c.ju)
        println("QM1 九宫: " + c.gongs.map { "${it.palace}宫:地${it.diGan}/星${it.tianXing}/门${it.renMen}/神${it.shenPan}${if (it.isMaXing) "【马】" else ""}${if (it.isKong) "【空】" else ""}" }.joinToString(" | "))
        assertTrue(c.gongs.all { it.diGan.isNotEmpty() })
    }

    @Test
    fun winterSolsticeYang1() {
        val c = QimenEngine.bySolar(2026, 12, 22, 10, 0)
        println("QM2 ${c.jieQi} ${c.juText} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}")
        assertTrue(c.jieQi == "冬至" || c.jieQi == "大雪", "节气=${c.jieQi}")
        if (c.jieQi == "冬至") {
            assertEquals(1, c.yinYang)
        }
        println("QM2 旬首=${c.xunShou} 遁干=${c.dunGan} 值符=${c.zhiFu} 值使=${c.zhiShi}")
    }

    @Test
    fun knownExample() {
        val c = QimenEngine.bySolar(1990, 5, 20, 12, 30)
        println("QM3 ${c.jieQi} ${c.juText} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ} 值符=${c.zhiFu} 值使=${c.zhiShi}")
        println("QM3 九宫: " + c.gongs.map { "${it.palace}宫:${it.diGan}" }.joinToString(" "))
        assertTrue(c.gongs.size == 9)
        val di = c.gongs.associate { it.palace to it.diGan }
        val ju = c.ju
        assertEquals("戊", di[ju])
    }
}
