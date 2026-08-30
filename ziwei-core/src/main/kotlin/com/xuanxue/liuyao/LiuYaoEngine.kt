package com.xuanxue.liuyao

import com.nlf.calendar.Lunar
import com.nlf.calendar.Solar

/**
 * 六爻（纳甲筮法）装卦引擎 — Kotlin 实现。
 * 规则来源：公开传统（八宫卦序/纳甲/世应/六亲/六神），《周易》卦名公有领域。
 * 起卦：时间起卦（梅花易数式，农历年月日时）+ 数字起卦（三数：上卦/下卦/动爻）。
 * 基础干支由 lunar-java (MIT) 提供。全部本地计算。
 */
object LiuYaoEngine {

    // 先天八卦数（梅花易数起卦）
    val XIAN_TIAN = mapOf("乾" to 1, "兑" to 2, "离" to 3, "震" to 4, "巽" to 5, "坎" to 6, "艮" to 7, "坤" to 8)

    // 八卦五行（纳甲筮法用后天八卦配五行）
    val GUA_WUXING = mapOf("乾" to "金", "兑" to "金", "离" to "火", "震" to "木", "巽" to "木", "坎" to "水", "艮" to "土", "坤" to "土")

    // 八宫 64 卦（Pair = 上卦 to 下卦；每宫 8 卦，顺序=本宫/一世/二世/三世/四世/五世/游魂/归魂）
    val EIGHT_PALACES: Map<String, List<Pair<String, String>>> = mapOf(
        "乾宫" to listOf(
            "乾" to "乾", // 乾为天（本宫）
            "乾" to "巽", // 天风姤（一世）
            "乾" to "艮", // 天山遁（二世）
            "乾" to "坤", // 天地否（三世）
            "巽" to "坤", // 风地观（四世）
            "艮" to "坤", // 山地剥（五世）
            "离" to "坤", // 火地晋（游魂）
            "离" to "乾", // 火天大有（归魂）
        ),
        "兑宫" to listOf(
            "兑" to "兑", // 兑为泽（本宫）
            "兑" to "坎", // 泽水困（一世）
            "兑" to "坤", // 泽地萃（二世）
            "兑" to "艮", // 泽山咸（三世）
            "坎" to "艮", // 水山蹇（四世）
            "坤" to "艮", // 地山谦（五世）
            "震" to "艮", // 雷山小过（游魂）
            "震" to "兑", // 雷泽归妹（归魂）
        ),
        "离宫" to listOf(
            "离" to "离", // 离为火（本宫）
            "离" to "艮", // 火山旅（一世）
            "离" to "巽", // 火风鼎（二世）
            "离" to "坎", // 火水未济（三世）
            "艮" to "坎", // 山水蒙（四世）
            "巽" to "坎", // 风水涣（五世）
            "乾" to "坎", // 天水讼（游魂）
            "乾" to "离", // 天火同人（归魂）
        ),
        "震宫" to listOf(
            "震" to "震", // 震为雷（本宫）
            "震" to "坤", // 雷地豫（一世）
            "震" to "坎", // 雷水解（二世）
            "震" to "巽", // 雷风恒（三世）
            "坤" to "巽", // 地风升（四世）
            "坎" to "巽", // 水风井（五世）
            "兑" to "巽", // 泽风大过（游魂）
            "兑" to "震", // 泽雷随（归魂）
        ),
        "巽宫" to listOf(
            "巽" to "巽", // 巽为风（本宫）
            "巽" to "乾", // 风天小畜（一世）
            "巽" to "离", // 风火家人（二世）
            "巽" to "震", // 风雷益（三世）
            "乾" to "震", // 天雷无妄（四世）
            "离" to "震", // 火雷噬嗑（五世）
            "艮" to "震", // 山雷颐（游魂）
            "艮" to "巽", // 山风蛊（归魂）
        ),
        "坎宫" to listOf(
            "坎" to "坎", // 坎为水（本宫）
            "坎" to "兑", // 水泽节（一世）
            "坎" to "震", // 水雷屯（二世）
            "坎" to "离", // 水火既济（三世）
            "兑" to "离", // 泽火革（四世）
            "震" to "离", // 雷火丰（五世）
            "坤" to "离", // 地火明夷（游魂）
            "坤" to "坎", // 地水师（归魂）
        ),
        "艮宫" to listOf(
            "艮" to "艮", // 艮为山（本宫）
            "艮" to "离", // 山火贲（一世）
            "艮" to "乾", // 山天大畜（二世）
            "艮" to "兑", // 山泽损（三世）
            "离" to "兑", // 火泽睽（四世）
            "乾" to "兑", // 天泽履（五世）
            "巽" to "兑", // 风泽中孚（游魂）
            "巽" to "艮", // 风山渐（归魂）
        ),
        "坤宫" to listOf(
            "坤" to "坤", // 坤为地（本宫）
            "坤" to "震", // 地雷复（一世）
            "坤" to "兑", // 地泽临（二世）
            "坤" to "乾", // 地天泰（三世）
            "震" to "乾", // 雷天大壮（四世）
            "兑" to "乾", // 泽天夬（五世）
            "坎" to "乾", // 水天需（游魂）
            "坎" to "坤", // 水地比（归魂）
        ),
    )

    // 世应位置（八宫卦序 index 0-7）：世爻 1-6，应爻 1-6（从初爻=1 起）
    val SHI_INDEX = intArrayOf(6, 1, 2, 3, 4, 5, 4, 3)   // 本宫世6，一世世1...游魂世4，归魂世3
    val YING_INDEX = intArrayOf(3, 4, 5, 6, 1, 2, 1, 6)  // 相应位置（世±3）

    // 纳甲表：八纯卦内卦/外卦纳支（从初爻到上爻 6 支）
    // 阳卦顺行（子寅辰午申戌 或 寅辰午申戌子...），阴卦逆行（丑亥酉未巳卯...）
    // 乾内:甲子寅辰 乾外:壬午申戌 | 坤内:乙未巳卯 坤外:癸丑亥酉
    // 震内:庚子寅辰 震外:庚午申戌 | 巽内:辛丑亥酉 巽外:辛未巳卯
    // 坎内:戊寅辰午 坎外:戊申戌子 | 离内:己卯丑亥 离外:己酉未巳
    // 艮内:丙辰午申 艮外:丙戌子寅 | 兑内:丁巳卯丑 兑外:丁亥酉未
    data class NaJia(val gan: String, val zhi: List<String>)

    val NA_JIA = mapOf(
        "乾" to NaJia("甲壬", listOf("子", "寅", "辰", "午", "申", "戌")), // 内外同支顺行，乾内甲外壬
        "坤" to NaJia("乙癸", listOf("未", "巳", "卯", "丑", "亥", "酉")),
        "震" to NaJia("庚", listOf("子", "寅", "辰", "午", "申", "戌")),
        "巽" to NaJia("辛", listOf("丑", "亥", "酉", "未", "巳", "卯")),
        "坎" to NaJia("戊", listOf("寅", "辰", "午", "申", "戌", "子")),
        "离" to NaJia("己", listOf("卯", "丑", "亥", "酉", "未", "巳")),
        "艮" to NaJia("丙", listOf("辰", "午", "申", "戌", "子", "寅")),
        "兑" to NaJia("丁", listOf("巳", "卯", "丑", "亥", "酉", "未")),
    )

    /**
     * 京房纳甲按实际上下卦装配，而不是按整卦所属八宫把六爻统一套一张纯卦表。
     * lineInTrigram 取 1..3；下卦使用内卦三爻，上卦使用外卦三爻。
     */
    private fun naJiaForLine(trigram: String, lineInTrigram: Int, outer: Boolean): Pair<String, String> {
        require(lineInTrigram in 1..3)
        val na = NA_JIA[trigram] ?: error("Missing NaJia table for $trigram")
        val zhiIndex = if (outer) lineInTrigram + 2 else lineInTrigram - 1
        val gan = if (na.gan.length >= 2) {
            if (outer) na.gan[1] else na.gan[0]
        } else {
            na.gan[0]
        }
        return gan.toString() to na.zhi[zhiIndex]
    }

    // 六神：日干起（从初爻起）
    val LIU_SHEN = listOf("青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武")
    fun liuShenOf(dayGan: String): List<String> {
        val start = when (dayGan[0]) {
            '甲', '乙' -> 0; '丙', '丁' -> 1; '戊', '己' -> 2; '庚', '辛' -> 3; else -> 5 // 壬癸
        }
        return (0 until 6).map { LIU_SHEN[(start + it) % 6] }
    }

    // 五行生克六亲（以卦宫五行为我）：生我父母/我生子孙/克我官鬼/我克妻财/比和兄弟
    private val SHENG = mapOf("金" to "水", "水" to "木", "木" to "火", "火" to "土", "土" to "金")
    private val KE = mapOf("金" to "木", "木" to "土", "土" to "水", "水" to "火", "火" to "金")
    fun liuQinOf(gongWx: String, zhiWx: String): String = when {
        zhiWx == gongWx -> "兄弟"
        SHENG[gongWx] == zhiWx -> "子孙"   // 我生
        SHENG[zhiWx] == gongWx -> "父母"   // 生我
        KE[zhiWx] == gongWx -> "官鬼"      // 克我
        else -> "妻财"                     // 我克
    }

    val ZHI_WUXING = mapOf(
        "子" to "水", "丑" to "土", "寅" to "木", "卯" to "木", "辰" to "土", "巳" to "火",
        "午" to "火", "未" to "土", "申" to "金", "酉" to "金", "戌" to "土", "亥" to "水",
    )

    // 每宫 8 卦名（与 EIGHT_PALACES 顺序一一对应，京房八宫标准卦名）
    val PALACE_GUA_NAMES: Map<String, List<String>> = mapOf(
        "乾宫" to listOf("乾为天", "天风姤", "天山遁", "天地否", "风地观", "山地剥", "火地晋", "火天大有"),
        "兑宫" to listOf("兑为泽", "泽水困", "泽地萃", "泽山咸", "水山蹇", "地山谦", "雷山小过", "雷泽归妹"),
        "离宫" to listOf("离为火", "火山旅", "火风鼎", "火水未济", "山水蒙", "风水涣", "天水讼", "天火同人"),
        "震宫" to listOf("震为雷", "雷地豫", "雷水解", "雷风恒", "地风升", "水风井", "泽风大过", "泽雷随"),
        "巽宫" to listOf("巽为风", "风天小畜", "风火家人", "风雷益", "天雷无妄", "火雷噬嗑", "山雷颐", "山风蛊"),
        "坎宫" to listOf("坎为水", "水泽节", "水雷屯", "水火既济", "泽火革", "雷火丰", "地火明夷", "地水师"),
        "艮宫" to listOf("艮为山", "山火贲", "山天大畜", "山泽损", "火泽睽", "天泽履", "风泽中孚", "风山渐"),
        "坤宫" to listOf("坤为地", "地雷复", "地泽临", "地天泰", "雷天大壮", "泽天夬", "水天需", "水地比"),
    )

    fun guaNameOf(palace: String, up: String, down: String): String {
        val list = EIGHT_PALACES[palace] ?: return up + down
        val idx = list.indexOf(up to down)
        if (idx >= 0) return (PALACE_GUA_NAMES[palace] ?: emptyList()).getOrElse(idx) { up + down }
        return up + down
    }

    // 找卦所在宫 + 宫序（0-7）
    fun palaceOf(up: String, down: String): Pair<String, Int>? {
        for ((palace, list) in EIGHT_PALACES) {
            val idx = list.indexOf(up to down)
            if (idx >= 0) return palace to idx
        }
        return null
    }

    data class Yao(
        val index: Int,          // 1-6（初爻=1）
        val gan: String,         // 纳甲天干
        val zhi: String,         // 纳甲地支
        val wuxing: String,      // 地支五行
        val liuQin: String,      // 六亲
        val liuShen: String,     // 六神
        val isShi: Boolean,      // 世爻
        val isYing: Boolean,     // 应爻
        val isDong: Boolean,     // 动爻
        val isYang: Boolean,     // 阳爻（—）阴爻（--）
    )

    data class Gua(
        val up: String, val down: String,          // 上下卦
        val name: String,                          // 卦名
        val palace: String,                        // 宫
        val palaceIndex: Int,                      // 宫序 0-7
        val yao: List<Yao>,
    )

    data class LiuYaoChart(
        val solarDate: String,
        val lunarDateStr: String,
        val dayGZ: String, val hourGZ: String,
        val benGua: Gua,                           // 本卦
        val bianGua: Gua?,                         // 变卦（有动爻时）
        val dongYaoIndexes: List<Int>,             // 动爻位置
        val guaShen: String?,                      // 卦身（简易：世爻所在）
    )

    // 数字起卦：三数（上卦/下卦/动爻）
    fun byNumbers(n1: Int, n2: Int, n3: Int, year: Int, month: Int, day: Int, hour: Int): LiuYaoChart {
        val upNum = ((n1 - 1) % 8 + 8) % 8 + 1
        val downNum = ((n2 - 1) % 8 + 8) % 8 + 1
        val dong = ((n3 - 1) % 6 + 6) % 6  // 0-5
        val up = XIAN_TIAN.entries.first { it.value == upNum }.key
        val down = XIAN_TIAN.entries.first { it.value == downNum }.key
        return build(up, down, listOf(dong), year, month, day, hour)
    }

    // 时间起卦（梅花易数：年支数+月+日 = 上卦；+时 = 下卦；总数 %6 = 动爻）
    fun bySolar(year: Int, month: Int, day: Int, hour: Int): LiuYaoChart {
        val solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        val lunar = solar.lunar
        val zhiNum = "子丑寅卯辰巳午未申酉戌亥".indexOf(lunar.getYearZhi().toString()) + 1
        val upNum = ((zhiNum + lunar.month + lunar.day) % 8).let { if (it == 0) 8 else it }
        val downNum = ((zhiNum + lunar.month + lunar.day + (hour / 2) + 1) % 8).let { if (it == 0) 8 else it }
        val total = zhiNum + lunar.month + lunar.day + (hour / 2) + 1
        val dong = (total % 6).let { if (it == 0) 5 else it - 1 }
        val up = XIAN_TIAN.entries.first { it.value == upNum }.key
        val down = XIAN_TIAN.entries.first { it.value == downNum }.key
        return build(up, down, listOf(dong), year, month, day, hour)
    }

    private fun build(up: String, down: String, dongIndexes: List<Int>, year: Int, month: Int, day: Int, hour: Int): LiuYaoChart {
        val solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        val lunar = solar.lunar
        val ec = lunar.eightChar
        val dayGZ = ec.getDayGan() + ec.getDayZhi()
        val hourGZ = ec.getTimeGan() + ec.getTimeZhi()

        val (palace, palaceIdx) = palaceOf(up, down) ?: ("乾宫" to 0)
        val gongWx = GUA_WUXING[palace.removeSuffix("宫")] ?: "金"
        val liuShen = liuShenOf(dayGZ[0].toString())
        val shi = SHI_INDEX[palaceIdx]
        val ying = YING_INDEX[palaceIdx]

        val benYao = (1..6).map { i ->
            val inUp = i > 3
            val guaPart = if (inUp) up else down
            val posInGua = if (inUp) i - 3 else i
            val (gan, zhi) = naJiaForLine(guaPart, posInGua, outer = inUp)
            Yao(
                index = i,
                gan = gan,
                zhi = zhi,
                wuxing = ZHI_WUXING[zhi] ?: "",
                liuQin = liuQinOf(gongWx, ZHI_WUXING[zhi] ?: ""),
                liuShen = liuShen[i - 1],
                isShi = i == shi,
                isYing = i == ying,
                isDong = i - 1 in dongIndexes,
                isYang = yaoYinYang(guaPart, posInGua),
            )
        }

        // 变卦：动爻逐爻翻转（爻1-3 翻下卦，爻4-6 翻上卦）
        var bianGua: Gua? = null
        if (dongIndexes.isNotEmpty()) {
            val downYao = dongIndexes.filter { it < 3 }.map { it + 1 }
            val upYao = dongIndexes.filter { it >= 3 }.map { it - 2 }
            val newDown = if (downYao.isNotEmpty()) flipYao(down, downYao) else down
            val newUp = if (upYao.isNotEmpty()) flipYao(up, upYao) else up
            val (bPalace, bIdx) = palaceOf(newUp, newDown) ?: ("乾宫" to 0)
            val bShi = SHI_INDEX[bIdx]
            val bYing = YING_INDEX[bIdx]
            val bGongWx = GUA_WUXING[bPalace.removeSuffix("宫")] ?: "金"
            val bYao = (1..6).map { i ->
                val inUp = i > 3
                val guaPart = if (inUp) newUp else newDown
                val posInGua = if (inUp) i - 3 else i
                val (gan, zhi) = naJiaForLine(guaPart, posInGua, outer = inUp)
                Yao(
                    index = i,
                    gan = gan,
                    zhi = zhi,
                    wuxing = ZHI_WUXING[zhi] ?: "",
                    liuQin = liuQinOf(bGongWx, ZHI_WUXING[zhi] ?: ""),
                    liuShen = liuShen[i - 1],
                    isShi = i == bShi,
                    isYing = i == bYing,
                    isDong = false,
                    isYang = yaoYinYang(guaPart, posInGua),
                )
            }
            bianGua = Gua(newUp, newDown, guaNameOf(bPalace, newUp, newDown), bPalace, bIdx, bYao)
        }

        val ben = Gua(up, down, guaNameOf(palace, up, down), palace, palaceIdx, benYao)
        return LiuYaoChart(
            solarDate = "$year-$month-$day $hour:00",
            lunarDateStr = lunar.toString(),
            dayGZ = dayGZ, hourGZ = hourGZ,
            benGua = ben,
            bianGua = bianGua,
            dongYaoIndexes = dongIndexes.map { it + 1 },
            guaShen = benYao.firstOrNull { it.isShi }?.zhi,
        )
    }

    // 八卦二进制（自下而上：位1=初爻）：乾111 兑110 离101 震100 巽011 坎010 艮001 坤000
    val GUA_BINARY = mapOf(
        "乾" to "111", "兑" to "110", "离" to "101", "震" to "100",
        "巽" to "011", "坎" to "010", "艮" to "001", "坤" to "000",
    )
    private val BINARY_GUA = GUA_BINARY.entries.associate { it.value to it.key }

    // 翻转指定爻位（1-6，初爻=1）后的新卦
    fun flipYao(gua: String, yaoIndexesInGua: List<Int>): String {
        val bin = GUA_BINARY[gua] ?: return gua
        val chars = bin.toCharArray()
        yaoIndexesInGua.forEach { pos ->
            val idx = pos - 1
            if (idx in 0..2) chars[idx] = if (chars[idx] == '1') '0' else '1'
        }
        return BINARY_GUA[String(chars)] ?: gua
    }

    // 卦三爻阴阳（自下而上）
    fun yaoYinYang(gua: String, pos: Int): Boolean = (GUA_BINARY[gua]?.get(pos - 1) ?: '1') == '1'
}
