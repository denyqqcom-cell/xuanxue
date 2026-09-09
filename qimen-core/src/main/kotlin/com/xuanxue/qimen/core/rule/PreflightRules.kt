package com.xuanxue.qimen.core.rule

import com.xuanxue.qimen.core.calendar.Stem

object PreflightRules {
    /** 五不遇时 generator: hour stem = day stem + 6 (mod 10). */
    fun isWuBuYu(dayStem: Stem, hourStem: Stem): Boolean =
        hourStem.ordinal == (dayStem.ordinal + 6) % 10

    /** 六仪击刑静态表，来自 handoff R-HIT-XING；只返回可验证的六仪。 */
    fun hitXingPalace(yi: Stem): Int? = when (yi) {
        Stem.WU -> 3
        Stem.JI -> 2
        Stem.GENG -> 8
        Stem.XIN -> 9
        Stem.REN -> 4
        Stem.GUI -> 4
        else -> null
    }
}
