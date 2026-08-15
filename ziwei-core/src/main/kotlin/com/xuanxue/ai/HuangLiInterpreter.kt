package com.xuanxue.ai

import com.nlf.calendar.Lunar

/**
 * 黄历离线解读：lunar-java 通书字段原样列出。
 * 宜忌是择日通书，不是八字/紫微应期。
 */
object HuangLiInterpreter {
    fun interpret(lunar: Lunar): List<String> = interpretItems(lunar).map { it.summary }

    fun reading(lunar: Lunar): Reading = Reading(
        toolName = "huangli_interpret",
        items = interpretItems(lunar),
        overall = "离线通书摘录。宜忌来自 lunar-java，通书流派不一。不是命理应期，也不宣称准确率。",
    )

    fun interpretItems(lunar: Lunar): List<ReadingItem> {
        val items = mutableListOf<ReadingItem>()
        items += sourcedItem(
            LAYER_ALG, "R-HL-DATE",
            "今日【${lunar}】。",
            "lunar-java Lunar.toString",
            "A",
        )

        val yi = lunar.getDayYi()
        val ji = lunar.getDayJi()
        items += sourcedItem(
            LAYER_ALG, "R-HL-YIJI",
            buildString {
                if (yi.isNotEmpty()) append("宜：${yi.take(8).joinToString("、")}。")
                if (ji.isNotEmpty()) append("忌：${ji.take(8).joinToString("、")}。")
                if (yi.isEmpty() && ji.isEmpty()) append("本日宜忌表为空。")
            },
            "lunar-java getDayYi / getDayJi",
            "B",
        )

        val js = lunar.getDayJiShen()
        val xs = lunar.getDayXiongSha()
        items += sourcedItem(
            LAYER_ALG, "R-HL-SHENSHA",
            buildString {
                if (js.isNotEmpty()) append("吉神：${js.take(6).joinToString("、")}。")
                if (xs.isNotEmpty()) append("凶煞：${xs.take(6).joinToString("、")}。")
                append("冲【${lunar.getDayChong()}】煞【${lunar.getDaySha()}】。")
            },
            "lunar-java 日神煞/冲煞",
            "B",
        )

        items += sourcedItem(
            LAYER_ALG, "R-HL-PENGZU",
            "彭祖百忌：${lunar.getPengZuGan()}、${lunar.getPengZuZhi()}。",
            "lunar-java 彭祖百忌字段",
            "B",
        )

        items += sourcedItem(
            LAYER_SCHOOL, "R-HL-TONGSHU",
            "通书宜忌、神煞各派用表不同。本机只跟 lunar-java 1.7.7，不仲裁哪本通书为正。",
            "cn.6tail:lunar",
            "B",
        )

        items += sourcedItem(
            LAYER_EXP, "R-HL-NO-FATE",
            "黄历宜忌是择日通书，不替代八字、紫微、奇门、六爻、六壬的结构推演，也不作应期。",
            "与各术数解读分层同一纪律",
            "C",
        )

        return items
    }
}
