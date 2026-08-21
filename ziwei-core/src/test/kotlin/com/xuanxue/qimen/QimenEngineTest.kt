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

    private fun anchorScore(actual: Map<Int, String>, expected: Map<Int, String>): Int =
        expected.count { (palace, value) -> actual[palace] == value }

    private fun shiftOuterRingValues(actual: Map<Int, String>, shift: Int): Map<Int, String> {
        val ring = QimenEngine.ROTATION_RING.toList()
        return ring.associateWith { palace ->
            val index = ring.indexOf(palace)
            val source = ring[((index - shift) % ring.size + ring.size) % ring.size]
            actual[source].orEmpty()
        }
    }

    @Test
    fun liangJiaziSparseAnchorsMatchProductionChiefIdentity() {
        val fixtures = loadLiangJiaziFixtures()
        assertEquals(18, fixtures.size)

        fixtures.forEach { fixture ->
            val yinYang = if (fixture.polarity == "YANG") 1 else -1
            val di = QimenEngine.buildDiPan(yinYang, fixture.bureau)

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
    fun shantiandaoFuTouYuanMatchesWorkedExampleDays() {
        assertEquals("中元", QimenEngine.yuanOfFuTou("癸酉"))
        assertEquals("下元", QimenEngine.yuanOfFuTou("丙子"))
        assertNotEquals(QimenEngine.yuanOf("癸酉"), QimenEngine.yuanOfFuTou("癸酉"))
    }

    @Test
    fun shantiandaoYang3WorkedPlateMatchesIndependentVisualAnchors() {
        val c = QimenEngine.bySolar(
            1995, 6, 11, 9, 30,
            QimenEngine.MethodProfile.SHANTI_DAO_71_P21_P22,
        )
        val g = c.gongs.associateBy { it.palace }

        assertEquals(QimenEngine.MethodProfile.SHANTI_DAO_71_P21_P22, c.methodProfile)
        assertEquals("芒种", c.jieQi)
        assertEquals(1, c.yinYang)
        assertEquals("中元", c.yuan)
        assertEquals(3, c.ju)
        assertEquals("丁巳", c.hourGZ)
        assertEquals("甲寅", c.xunShou)
        assertEquals("癸", c.dunGan)
        assertEquals("天任", c.zhiFu)
        assertEquals("生门", c.zhiShi)
        assertTrue(c.implementationWarnings.isEmpty())

        assertEquals("天任", g.getValue(9).tianXing)
        assertEquals("天冲", g.getValue(2).tianXing)
        assertEquals("天芮/天禽", g.getValue(1).tianXing)
        assertEquals("生门", g.getValue(2).renMen)
        assertEquals("休门", g.getValue(9).renMen)
        assertEquals("值符", g.getValue(9).shenPan)
        assertEquals("腾蛇", g.getValue(2).shenPan)
        assertEquals("白虎", g.getValue(1).shenPan)
    }

    @Test
    fun shantiandaoYin8WorkedPlateMatchesIndependentVisualAnchors() {
        val c = QimenEngine.bySolar(
            1995, 8, 13, 20, 0,
            QimenEngine.MethodProfile.SHANTI_DAO_71_P21_P22,
        )
        val g = c.gongs.associateBy { it.palace }

        assertEquals("立秋", c.jieQi)
        assertEquals(-1, c.yinYang)
        assertEquals("下元", c.yuan)
        assertEquals(8, c.ju)
        assertEquals("戊戌", c.hourGZ)
        assertEquals("甲午", c.xunShou)
        assertEquals("辛", c.dunGan)
        assertEquals("天禽", c.zhiFu)
        assertEquals("死门", c.zhiShi)
        assertTrue(c.implementationWarnings.isEmpty())

        assertEquals("天芮/天禽", g.getValue(8).tianXing)
        assertEquals("天柱", g.getValue(3).tianXing)
        assertEquals("天英", g.getValue(1).tianXing)
        assertEquals("死门", g.getValue(1).renMen)
        assertEquals("惊门", g.getValue(8).renMen)
        assertEquals("景门", g.getValue(6).renMen)
        assertEquals("值符", g.getValue(8).shenPan)
        assertEquals("腾蛇", g.getValue(1).shenPan)
        assertEquals("玄武", g.getValue(9).shenPan)
        assertEquals("九天", g.getValue(3).shenPan)
    }

    @Test
    fun shantiandaoWrongBureauCannotRescueWorkedPlateAnchors() {
        val correctYang = QimenEngine.buildShantiandao71Layers(
            yinYang = 1,
            di = QimenEngine.buildDiPan(1, 3),
            hourGZ = "丁巳",
        )
        val wrongYang = QimenEngine.buildShantiandao71Layers(
            yinYang = 1,
            di = QimenEngine.buildDiPan(1, 4),
            hourGZ = "丁巳",
        )

        assertEquals("天任", correctYang.stars[9])
        assertEquals("生门", correctYang.doors[2])
        assertNotEquals(correctYang.stars[9], wrongYang.stars[9])
        assertNotEquals(correctYang.doors[2], wrongYang.doors[2])

        val correctYin = QimenEngine.buildShantiandao71Layers(
            yinYang = -1,
            di = QimenEngine.buildDiPan(-1, 8),
            hourGZ = "戊戌",
        )
        val wrongYin = QimenEngine.buildShantiandao71Layers(
            yinYang = -1,
            di = QimenEngine.buildDiPan(-1, 7),
            hourGZ = "戊戌",
        )

        assertEquals("天芮/天禽", correctYin.stars[8])
        assertEquals("死门", correctYin.doors[1])
        assertNotEquals(correctYin.stars[8], wrongYin.stars[8])
        assertNotEquals(correctYin.doors[1], wrongYin.doors[1])
    }

    @Test
    fun shantiandaoWrongHourCannotRescueYang3VisualOracle() {
        val di = QimenEngine.buildDiPan(1, 3)
        val correct = QimenEngine.buildShantiandao71Layers(1, di, "丁巳")
        val wrongHour = QimenEngine.buildShantiandao71Layers(1, di, "丙辰")

        val expectedStars = mapOf(9 to "天任", 2 to "天冲", 1 to "天芮/天禽")
        val expectedDoors = mapOf(2 to "生门", 9 to "休门")
        val expectedDeities = mapOf(9 to "值符", 2 to "腾蛇", 1 to "白虎")

        val correctScore = anchorScore(correct.stars, expectedStars) +
            anchorScore(correct.doors, expectedDoors) +
            anchorScore(correct.deities, expectedDeities)
        val wrongScore = anchorScore(wrongHour.stars, expectedStars) +
            anchorScore(wrongHour.doors, expectedDoors) +
            anchorScore(wrongHour.deities, expectedDeities)

        assertEquals(8, correctScore)
        assertTrue(wrongScore < correctScore, "wrong hour must lose source-defined sparse oracle score")
    }

    @Test
    fun shantiandaoPermutedLayerLabelsLoseYang3VisualOracleScore() {
        val correct = QimenEngine.buildShantiandao71Layers(
            yinYang = 1,
            di = QimenEngine.buildDiPan(1, 3),
            hourGZ = "丁巳",
        )

        val expectedStars = mapOf(9 to "天任", 2 to "天冲", 1 to "天芮/天禽")
        val expectedDoors = mapOf(2 to "生门", 9 to "休门")
        val expectedDeities = mapOf(9 to "值符", 2 to "腾蛇", 1 to "白虎")

        val correctScore = anchorScore(correct.stars, expectedStars) +
            anchorScore(correct.doors, expectedDoors) +
            anchorScore(correct.deities, expectedDeities)

        val permutedStars = shiftOuterRingValues(correct.stars, 1)
        val permutedDoors = shiftOuterRingValues(correct.doors, 2)
        val permutedDeities = shiftOuterRingValues(correct.deities, 3)
        val permutedScore = anchorScore(permutedStars, expectedStars) +
            anchorScore(permutedDoors, expectedDoors) +
            anchorScore(permutedDeities, expectedDeities)

        assertEquals(8, correctScore)
        assertTrue(permutedScore < correctScore, "permuted layers must not tie the correct sparse oracle")
    }

    @Test
    fun legacyProfileIsNotMistakenForShantiandaoWorkedPlate() {
        val sourceYang = QimenEngine.bySolar(
            1995, 6, 11, 9, 30,
            QimenEngine.MethodProfile.SHANTI_DAO_71_P21_P22,
        )
        val legacyYang = QimenEngine.bySolar(1995, 6, 11, 9, 30)

        assertEquals("中元", sourceYang.yuan)
        assertEquals(3, sourceYang.ju)
        assertNotEquals(sourceYang.yuan, legacyYang.yuan)
        assertNotEquals(sourceYang.ju, legacyYang.ju)

        val sourceYin = QimenEngine.bySolar(
            1995, 8, 13, 20, 0,
            QimenEngine.MethodProfile.SHANTI_DAO_71_P21_P22,
        )
        val legacyYin = QimenEngine.bySolar(1995, 8, 13, 20, 0)
        val sourceG = sourceYin.gongs.associateBy { it.palace }
        val legacyG = legacyYin.gongs.associateBy { it.palace }

        val discriminatingAnchors = listOf(
            sourceG.getValue(8).tianXing != legacyG.getValue(8).tianXing,
            sourceG.getValue(1).renMen != legacyG.getValue(1).renMen,
            sourceG.getValue(1).shenPan != legacyG.getValue(1).shenPan,
        )
        assertTrue(discriminatingAnchors.count { it } >= 2, "legacy profile must remain distinguishable from source profile")
    }

    @Test
    fun shantiandaoCenterDoorTargetFailsClosedInsteadOfGuessing() {
        val unresolved = QimenEngine.buildShantiandao71Layers(
            yinYang = -1,
            di = QimenEngine.buildDiPan(-1, 8),
            hourGZ = "甲午",
        )

        assertTrue(unresolved.doors.isEmpty())
        assertEquals(
            listOf("SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED"),
            unresolved.warnings,
        )
    }

    @Test
    fun alignUserScript() {
        val c = QimenEngine.bySolar(2026, 8, 12, 15, 37)
        println("QM1 节气=${c.jieQi} ${c.juText} 四柱=${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}")
        println("QM1 旬首=${c.xunShou} 遁干=${c.dunGan} 旬空=${c.xunKong} 值符=${c.zhiFu} 值使=${c.zhiShi} 马星=${c.maXing}")
        assertEquals(QimenEngine.MethodProfile.LEGACY_EXPERIMENTAL, c.methodProfile)
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
