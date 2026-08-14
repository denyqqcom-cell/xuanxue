package com.xuanxue.ai

import com.xuanxue.bazi.BaziEngine

/**
 * 八字解读器 — 离线规则解读。
 * 内容：五行分布/日主强弱(十二运)/十神结构/格局倾向/大运走向。
 * 全部为公开传统命理常识性释义。
 */
object BaziInterpreter : Interpreter<BaziEngine.BaziChart> {
    override val toolName = "bazi_interpret"
    override val toolDesc = "八字四柱解读：五行、日主强弱、十神格局、大运"

    // 五行对应的性格/倾向描述（传统常识性释义）
    private val WUXING_CHAR = mapOf(
        "金" to "性刚毅果决，重义气，喜条理",
        "木" to "性仁和向上，有生发之气，主成长",
        "水" to "性聪慧流动，主智慧与适应力",
        "火" to "性热烈明快，主礼仪与表现力",
        "土" to "性敦厚包容，主信用与承载",
    )

    // 日主五行对应的十天干特性
    private val GAN_CHAR = mapOf(
        "甲" to "阳木，如参天大树，主向上生长、独立担当",
        "乙" to "阴木，如花草藤蔓，主柔韧适应、细腻婉转",
        "丙" to "阳火，如太阳，主光明磊落、热情外放",
        "丁" to "阴火，如灯烛，主内敛温暖、思虑细腻",
        "戊" to "阳土，如高山城墙，主厚重稳固、诚信担当",
        "己" to "阴土，如田园沃土，主包容滋养、善于协调",
        "庚" to "阳金，如刀剑矿石，主刚毅果断、规则分明",
        "辛" to "阴金，如珠玉首饰，主精致敏锐、审美细腻",
        "壬" to "阳水，如江河大海，主奔流不息、格局开阔",
        "癸" to "阴水，如雨露泉眼，主滋养渗透、洞察微妙",
    )

    // 十神含义（传统）
    private val SHI_SHEN = mapOf(
        "正官" to "循规守约，责任心强，利公职与管理",
        "七杀" to "魄力与压力并存，有竞争性与行动力",
        "正印" to "贵人与庇护，利学业文化，主名声",
        "偏印" to "偏门才艺，思维独特，利专业技艺",
        "正财" to "正当收入，勤俭务实，主稳定财源",
        "偏财" to "流动之财，交际手腕，主机遇与魄力",
        "食神" to "才艺表达，福气享受，主创造力",
        "伤官" to "才华外露，锋芒锐气，主突破与个性",
        "比肩" to "自我独立，同辈助力，主自主性",
        "劫财" to "行动果断，竞争意识，主进取与破费",
    )

    private val GAN = "甲乙丙丁戊己庚辛壬癸"
    private val WX = "木木火火土土金金水水"

    override fun interpret(c: BaziEngine.BaziChart): List<String> {
        val items = mutableListOf<String>()
        val dayGan = c.dayZhu.gan
        val dayWx = WX[GAN.indexOf(dayGan)].toString()

        // 1. 日主特性
        items.add("日主【${dayGan}】${GAN_CHAR[dayGan] ?: ""}（${dayWx}）。日支【${c.dayZhu.zhi}】为${c.dayZhu.hideGan.joinToString("、")}，十二运【${c.dayZhu.diShi}】。")

        // 2. 五行分布统计（含藏干）
        val wxCount = mutableMapOf("金" to 0, "木" to 0, "水" to 0, "火" to 0, "土" to 0)
        c.fourZhu.forEach { zhu ->
            val g = zhu.gan
            val gWx = WX[GAN.indexOf(g)].toString()
            wxCount[gWx] = (wxCount[gWx] ?: 0) + 2
            zhu.hideGan.forEach { hg ->
                val hWx = WX[GAN.indexOf(hg)].toString()
                wxCount[hWx] = (wxCount[hWx] ?: 0) + 1
            }
        }
        val sorted = wxCount.entries.sortedByDescending { it.value }
        val strongest = sorted.first()
        val weakest = sorted.last()
        val balance = sorted.joinToString(" ") { "${it.key}${it.value}" }
        items.add("五行分布（含藏干计分）：$balance。最旺【${strongest.key}】${WUXING_CHAR[strongest.key] ?: ""}；最弱【${weakest.key}】。")

        // 3. 日主强弱（十二运判断简单版：长生/沐浴/冠带/临官/帝旺 为旺；病/死/墓/绝 为弱；余为平）
        val diShi = c.dayZhu.diShi
        val strength = when (diShi) {
            "长生", "沐浴", "冠带", "临官", "帝旺" -> "偏旺"
            "病", "死", "墓", "绝" -> "偏弱"
            else -> "中和"
        }
        items.add("日主十二运【${diShi}】，身${strength}。${if (strength == "偏旺") "宜泄宜克，喜财官食伤" else if (strength == "偏弱") "宜生宜扶，喜印比" else "五行趋衡，随运而行"}。")

        // 4. 十神格局
        val shiShenSet = c.fourZhu.flatMap { listOf(it.shiShenGan) + it.shiShenZhi }.toSet()
        val shenDesc = shiShenSet.filter { SHI_SHEN.containsKey(it) }.joinToString("、") { "${it}（${SHI_SHEN[it]}）" }
        items.add("命局十神：$shenDesc。")
        // 财官印食重点提示
        val keyShen = listOf("正官", "七杀", "正印", "正财", "食神")
        val present = keyShen.filter { it in shiShenSet }
        if (present.isNotEmpty()) {
            items.add("重点格局倾向：${present.joinToString("、")}。")
        } else {
            items.add("格局以比劫/偏印为主，宜从专业技艺或合作中求发展。")
        }

        // 5. 大运
        if (c.daYun.isNotEmpty()) {
            val first = c.daYun.first()
            val current = c.daYun.getOrNull(1) ?: first
            items.add("${c.startYunAge}岁起运。${current.startYear}-${current.endYear}岁行【${current.ganZhi}】运，首年流年${current.liuNian.firstOrNull()?.first ?: ""}。")
        }

        return items
    }
}
