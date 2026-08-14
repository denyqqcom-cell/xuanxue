package com.xuanxue.qimen.core.plate

enum class PalaceId(val number: Int, val trigram: String) {
    KAN_1(1, "坎"),
    KUN_2(2, "坤"),
    ZHEN_3(3, "震"),
    XUN_4(4, "巽"),
    CENTER_5(5, "中"),
    QIAN_6(6, "乾"),
    DUI_7(7, "兑"),
    GEN_8(8, "艮"),
    LI_9(9, "离"),
    ;

    companion object {
        fun fromNumber(number: Int): PalaceId = entries.first { it.number == number }
    }
}

enum class Yi(val symbol: String) {
    WU("戊"), JI("己"), GENG("庚"), XIN("辛"), REN("壬"), GUI("癸"),
    DING("丁"), BING("丙"), YI("乙"),
    ;

    companion object {
        fun fromSymbol(value: String): Yi = entries.first { it.symbol == value }
    }
}

/** Intentionally nullable in QimenChart until the earth-plate walk conflict has fixtures. */
data class EarthPlate(val yiByPalace: Map<PalaceId, Yi>)
