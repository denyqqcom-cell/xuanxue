package com.xuanxue.ai

import com.xuanxue.ziwei.core.ZiweiAstro.Astrolabe

/**
 * 紫微离线解读：命宫/身宫/四化/五行局只标盘面。
 * 不下发十四主星性格词典；不写概率百分比。
 */
object ZiweiInterpreter : Interpreter<Astrolabe> {
    override val toolName = "ziwei_interpret"
    override val toolDesc = "紫微斗数盘解读：命宫主星、四化落点（离线，带来源）"

    override fun interpret(a: Astrolabe): List<String> = interpretItems(a).map { it.summary }

    fun reading(a: Astrolabe): Reading = Reading(
        toolName = toolName,
        items = interpretItems(a),
        overall = "离线规则摘录。主星只列名与亮度，不套性格。不写概率。不是应期，也不宣称准确率。",
    )

    fun interpretItems(a: Astrolabe): List<ReadingItem> {
        val items = mutableListOf<ReadingItem>()
        val ming = a.palaces.firstOrNull { it.name == "命宫" }
        val shen = a.palaces.firstOrNull { it.isBodyPalace }

        if (ming != null) {
            val stars = ming.majorStars
            val starTxt = if (stars.isEmpty()) {
                val dui = a.palaces[(ming.index + 6) % a.palaces.size]
                val borrow = dui.majorStars.joinToString("、") { starLabel(it) }.ifEmpty { "对宫亦无主星" }
                "无主星，对宫【${dui.name}】主星：$borrow（借对宫是安星手续，不断吉凶）"
            } else {
                stars.joinToString("、") { starLabel(it) }
            }
            items += sourcedItem(
                LAYER_ALG, "R-ZW-MING",
                "命宫【${ming.heavenlyStem}${ming.earthlyBranch}】，主星：$starTxt。",
                "iztro default 安星；宫名来自本机盘",
                "A",
            )
        }

        if (shen != null) {
            val stars = shen.majorStars.joinToString("、") { starLabel(it) }.ifEmpty { "无主星" }
            items += sourcedItem(
                LAYER_ALG, "R-ZW-BODY",
                "身宫【${shen.name} ${shen.heavenlyStem}${shen.earthlyBranch}】，主星：$stars。",
                "身宫指数 isBodyPalace",
                "A",
            )
        }

        val sihua = a.palaces.flatMap { p ->
            (p.majorStars + p.minorStars).mapNotNull { s ->
                s.mutagen.takeIf { it.isNotEmpty() }?.let { "${p.name}${s.name}化$it" }
            }
        }
        items += sourcedItem(
            LAYER_ALG, "R-ZW-SIHUA",
            if (sihua.isEmpty()) "本机盘面未见四化标记。"
            else "四化落点：${sihua.joinToString("、")}。只标落宫落星，不写成得财/掌权/名声/收敛。",
            "iztro mutagen 字段",
            "A",
        )

        items += sourcedItem(
            LAYER_ALG, "R-ZW-JU",
            "五行局【${a.fiveElementsClass}】，命主【${a.soul}】，身主【${a.body}】。",
            "本机 Astrolabe 字段",
            "A",
        )

        items += sourcedItem(
            LAYER_SCHOOL, "R-ZW-IZTRO",
            "安星算法是 iztro MIT 移植（NOTICE），派别 default。不是中州派全书重排，也不保证与王亭之全集逐星一致。",
            "ziwei-core / NOTICE",
            "B",
        )

        items += sourcedItem(
            LAYER_SCHOOL, "R-ZW-ZHONGZHOU",
            "仓库笔记按中州派学习。笔记24：王亭之称五行生克是子平附会的点缀，v0.3 已把能量前置降为参考。本机不做五行能量定性。",
            "紫薇/学习笔记/24-情境推演框架v0.3",
            "B",
        )

        items += sourcedItem(
            LAYER_EXP, "R-ZW-V03",
            "不下发十四主星性格词典。不写百分比运气。程度若将来标注只用高/中/低，本机此版不标程度。",
            "笔记24 修改2；与八字十神词典同一纪律",
            "C",
        )

        return items
    }

    private fun starLabel(s: com.xuanxue.ziwei.core.ZiweiStars.Star): String =
        buildString {
            append(s.name)
            if (s.brightness.isNotEmpty()) append("(${s.brightness})")
            if (s.mutagen.isNotEmpty()) append("化${s.mutagen}")
        }
}
