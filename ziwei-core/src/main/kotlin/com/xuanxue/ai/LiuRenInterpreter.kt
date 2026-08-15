package com.xuanxue.ai

import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuren.LiuRenEngine.LiuRenChart

/**
 * 大六壬离线解读：月将加时、四课、九宗门取法、三传、天将。
 * 课式只作别名，不下发吉凶词典。
 */
object LiuRenInterpreter : Interpreter<LiuRenChart> {
    override val toolName = "liuren_interpret"
    override val toolDesc = "大六壬课解读：四课、取法、三传、天将（离线，带来源）"

    /** 取法 → 传统课式别名。只命名，不断事。 */
    private val FA_ALIAS = mapOf(
        "贼克（上克下）" to "元首课",
        "贼克（下贼上）" to "重审课",
        "比用" to "知一课",
        "涉害" to "涉害课",
        "遥克" to "蒿矢/弹射课",
        "遥贼" to "弹射课",
        "昴星" to "虎视/冬蛇掩目课",
        "别责" to "别责课",
        "八专" to "八专课",
        "返吟" to "返吟课",
        "伏吟" to "伏吟课",
    )

    override fun interpret(c: LiuRenChart): List<String> = interpretItems(c).map { it.summary }

    fun reading(c: LiuRenChart): Reading = Reading(
        toolName = toolName,
        items = interpretItems(c),
        overall = "离线规则摘录。课式只作别名，冲突只并列。不是应期，也不宣称准确率。",
    )

    fun interpretItems(c: LiuRenChart): List<ReadingItem> {
        val items = mutableListOf<ReadingItem>()
        val alias = FA_ALIAS.entries.firstOrNull { c.sanChuan.fa.startsWith(it.key) || c.sanChuan.fa.contains(it.key) }?.value
            ?: FA_ALIAS[c.sanChuan.fa]

        items += sourcedItem(
            LAYER_ALG, "R-LR-STAMP",
            "课时【${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}】，月将【${c.yueJiang}】加时，日干寄【${c.ganJi}】。",
            "LiuRenEngine：中气换将、月将加时",
            "A",
        )

        val ke = c.siKe.mapIndexed { i, k -> "课${i + 1}${k.zhi}遁${k.dunGan}" }.joinToString("、")
        items += sourcedItem(
            LAYER_ALG, "R-LR-SIKE",
            "四课：$ke。",
            "一课日干寄宫上神，二课日支上神，三四课递取",
            "A",
        )

        items += sourcedItem(
            LAYER_ALG, "R-LR-FA",
            "九宗门取法【${c.sanChuan.fa}】" + (alias?.let { "，传统亦称$it" } ?: "") + "。此为取三传的手续名，不断事从何处起。",
            "引擎 jiuZongMen；别名是课式通称不是吉凶",
            "B",
        )

        items += sourcedItem(
            LAYER_ALG, "R-LR-SANCHUAN",
            "三传【${c.sanChuan.chu}→${c.sanChuan.zhong}→${c.sanChuan.mo}】。初中末只标顺序，不写成事之始中终吉凶。",
            "九宗门产出",
            "A",
        )

        val tj = LiuRenEngine.ZHI.mapIndexed { i, z ->
            val j = c.tianJiang.getOrNull(i).orEmpty()
            if (j.isNotEmpty()) "${z}天${c.tianPan[i]}/$j" else null
        }.filterNotNull().joinToString("、")
        items += sourcedItem(
            LAYER_ALG, "R-LR-JIANG",
            "贵人【${c.guiRen}】。天将：$tj。",
            "甲戊庚牛羊歌；昼夜由 night 参数定",
            "B",
        )

        items += sourcedItem(
            LAYER_ALG, "R-LR-KONG",
            "旬空【${c.xunKong.joinToString("")}】。只标空亡地支，不写成待填实则应事。",
            "日旬空",
            "A",
        )

        items += sourcedItem(
            LAYER_SCHOOL, "R-LR-YUAN",
            "引擎自称袁树珊《大六壬探原》体系。九宗门细目别本或不同，本机不换取法，也不用在线课盘作标准。",
            "LiuRenEngine 文件头；handoff 同类纪律",
            "B",
        )

        items += sourcedItem(
            LAYER_SCHOOL, "R-LR-DAYNIGHT",
            "贵人分昼贵夜贵。本机默认按调用参数，未传 night 时为昼贵。",
            "guiRen(dayGan, night)",
            "B",
        )

        items += sourcedItem(
            LAYER_EXP, "R-LR-NO-OMEN",
            "不下发元首宜顺势、返吟反复无常一类课名断语。空亡不作自动吉凶。",
            "与奇门空亡三说同一条：判断层与取法层分开",
            "C",
        )

        return items
    }
}
