package com.xuanxue.ai

import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.liuyao.LiuYaoEngine.LiuYaoChart
import kotlin.math.abs

/**
 * 六爻离线解读：纳甲装卦手续。不下发六亲象义词典，不自动用神、不自动吉凶。
 */
object LiuYaoInterpreter : Interpreter<LiuYaoChart> {
    override val toolName = "liuyao_interpret"
    override val toolDesc = "六爻卦解读：世应、动爻、六亲名目（离线，带来源）"

    override fun interpret(c: LiuYaoChart): List<String> = interpretItems(c).map { it.summary }

    fun reading(c: LiuYaoChart): Reading = Reading(
        toolName = toolName,
        items = interpretItems(c),
        overall = "离线规则摘录。算法、门派、经验已分开。六亲只列名，不套象义。不是应期，也不宣称准确率。",
    )

    fun interpretItems(c: LiuYaoChart): List<ReadingItem> {
        val items = mutableListOf<ReadingItem>()
        val shi = c.benGua.yao.first { it.isShi }
        val ying = c.benGua.yao.first { it.isYing }

        items += sourcedItem(
            LAYER_ALG, "R-LY-GUA",
            "本卦【${c.benGua.name}】${c.benGua.up}上${c.benGua.down}下，${c.benGua.palace}，日辰【${c.dayGZ}】时【${c.hourGZ}】。",
            "LiuYaoEngine 纳甲筮法；卦名公有领域",
            "A",
        )

        val rel = when (abs(shi.index - ying.index)) {
            0 -> "世应同位"
            3 -> "世应相对（差3爻）"
            else -> "世应相隔（差${abs(shi.index - ying.index)}爻）"
        }
        items += sourcedItem(
            LAYER_ALG, "R-LY-SHIYING",
            "世爻在${shi.index}爻【${shi.liuQin}${shi.gan}${shi.zhi}】六神【${shi.liuShen}】；应爻在${ying.index}爻【${ying.liuQin}${ying.gan}${ying.zhi}】。$rel。只标位置，不断对立或回旋。",
            "八宫世应表 SHI_INDEX/YING_INDEX",
            "A",
        )

        if (c.dongYaoIndexes.isEmpty()) {
            items += sourcedItem(
                LAYER_ALG, "R-LY-DONG",
                "无动爻，静卦。本机不把静卦写成宜静守。",
                "动爻表 dongYaoIndexes",
                "A",
            )
        } else {
            val dong = c.dongYaoIndexes.joinToString("、") { i ->
                val y = c.benGua.yao[i - 1]
                "${i}爻${y.liuQin}${y.zhi}"
            }
            items += sourcedItem(
                LAYER_ALG, "R-LY-DONG",
                "${c.dongYaoIndexes.joinToString("、")}爻动：$dong。" +
                    (c.bianGua?.let { "变卦【${it.name}】（${it.up}上${it.down}下）。" } ?: "变卦未生成。") +
                    "只标动变，不观吉凶趋向。",
                "纳甲动爻变卦",
                "A",
            )
        }

        val qin = c.benGua.yao.map { "${it.index}${it.liuQin}${it.zhi}" }.joinToString("、")
        items += sourcedItem(
            LAYER_ALG, "R-LY-QIN",
            "本卦六亲名目：$qin。",
            "纳甲六亲：生克比于本宫五行",
            "A",
        )

        val xun = QimenRules.xunOf(c.dayGZ)
        if (xun != null) {
            val kongYao = c.benGua.yao.filter { it.zhi in xun.xunKong }
            items += sourcedItem(
                LAYER_ALG, "R-LY-KONG",
                "日辰旬空【${xun.xunKong.joinToString("")}】。" +
                    if (kongYao.isEmpty()) "本卦地支未落空。"
                    else "落在${kongYao.joinToString("、") { "${it.index}爻${it.liuQin}${it.zhi}" }}。只标空，不断不成。",
                "日旬空与纳支对照",
                "B",
            )
        }

        items += sourcedItem(
            LAYER_SCHOOL, "R-LY-YONG",
            "用神按所问六亲取，本机不自动指定。『世为自己、应为他人』是纳甲习用，不是唯一取用。",
            "纳甲筮法通行手续；仓库无增删卜易断语包",
            "B",
        )

        items += sourcedItem(
            LAYER_SCHOOL, "R-LY-QIJUA",
            "本机数字起卦走先天八卦数；时间起卦走梅花年月日时取上下卦。与三钱摇卦不是同一手续。",
            "LiuYaoEngine.byNumbers / bySolar",
            "B",
        )

        items += sourcedItem(
            LAYER_EXP, "R-LY-NO-OMEN",
            "父母/兄弟/子孙/妻财/官鬼的性格象义词典不下发。不自动吉凶，不宣称准确率。",
            "与八字/奇门同一条：先结构后象，象不下发",
            "C",
        )

        return items
    }
}
