package com.xuanxue.ai

import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuren.LiuRenEngine.LiuRenChart
import com.xuanxue.liuyao.LiuYaoEngine
import com.xuanxue.liuyao.LiuYaoEngine.LiuYaoChart
import com.xuanxue.ziwei.core.ZiweiAstro.Astrolabe

/**
 * 六爻解读器：世应/动爻/六亲用神（传统断语常识）。
 */
object LiuYaoInterpreter : Interpreter<LiuYaoChart> {
    override val toolName = "liuyao_interpret"
    override val toolDesc = "六爻卦解读：世应、动爻、六亲用神"

    private val LIU_QIN_YI = mapOf(
        "父母" to "主文书、长辈、房屋车辆",
        "兄弟" to "主同辈、竞争、破费",
        "子孙" to "主子女、福神、财源、解忧",
        "妻财" to "主钱财、妻子、物欲",
        "官鬼" to "主事业、官非、压力、疾病",
    )

    override fun interpret(c: LiuYaoChart): List<String> {
        val items = mutableListOf<String>()
        items.add("起得【${c.benGua.name}】卦（${c.benGua.up}上${c.benGua.down}下，${c.benGua.palace}），日辰【${c.dayGZ}】。")
        val shi = c.benGua.yao.first { it.isShi }
        val ying = c.benGua.yao.first { it.isYing }
        items.add("世爻在${shi.index}爻【${shi.liuQin}${shi.zhi}】（${shi.liuShen}），应爻在${ying.index}爻【${ying.liuQin}${ying.zhi}】。世为己应为彼，${if (shi.index == ying.index) "世应同位" else "世应相${if (kotlin.math.abs(shi.index - ying.index) == 3) "对" else "隔"}，主事有${if (kotlin.math.abs(shi.index - ying.index) == 3) "明确对立面" else "回旋余地"}。"}")
        if (c.dongYaoIndexes.isEmpty()) {
            items.add("卦为静卦，主事态未动，宜静守待时。")
        } else {
            val dong = c.dongYaoIndexes.joinToString("、")
            items.add("${dong}爻动，主事有变。动爻六亲：${c.dongYaoIndexes.map { c.benGua.yao[it - 1] }.joinToString("、") { "${it.index}爻${it.liuQin}" }}。")
            c.bianGua?.let {
                items.add("变卦【${it.name}】，动而化变，观变卦六亲以断吉凶趋向。")
            }
        }
        val qin = c.benGua.yao.map { it.liuQin }.toSet()
        val yis = qin.mapNotNull { LIU_QIN_YI[it]?.let { d -> "$it（$d）" } }.joinToString("、")
        items.add("六亲分布：$yis。")
        return items
    }
}

/**
 * 六壬解读器：课型/三传/天将（九宗门传统释义）。
 */
object LiuRenInterpreter : Interpreter<LiuRenChart> {
    override val toolName = "liuren_interpret"
    override val toolDesc = "大六壬课解读：课型、三传、天将"

    private val KE_FA = mapOf(
        "贼克（上克下）" to "元首课，上克下理顺，事从外起，宜顺势而为",
        "贼克（下贼上）" to "重审课，下犯上多阻，事须反复审度",
        "比用" to "知一课，取与日干比和者，事有两歧而择亲",
        "涉害" to "涉害课，诸克并见而取害深，主事涉艰难险阻",
        "遥克" to "蒿矢/弹射课，无近克而远克，事起于远或暗处",
        "遥贼" to "弹射课，日干克远神，主虚惊与远谋",
        "昴星" to "虎视/冬蛇掩目课，无克无遥取酉位，主进退维谷",
        "别责" to "别责课，干支无克取合处，事有异路别途",
        "八专" to "八专课，干支同位，主事专一或偏执",
        "返吟" to "返吟课，天地盘相冲，主反复无常、来而复去",
        "伏吟" to "伏吟课，天地盘同，主伏而不动、静守为宜",
    )

    override fun interpret(c: LiuRenChart): List<String> {
        val items = mutableListOf<String>()
        items.add("课时【${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}】，月将【${c.yueJiang}】加时。")
        items.add("课型：${KE_FA[c.sanChuan.fa] ?: c.sanChuan.fa}。")
        items.add("三传【${c.sanChuan.chu}→${c.sanChuan.zhong}→${c.sanChuan.mo}】，初中末三传主事之始、中、终。")
        val tj = c.tianJiang.mapIndexedNotNull { i, t -> if (t.isNotEmpty()) "${c.tianPan[i]}=$t" else null }.joinToString("、")
        items.add("天将分布：$tj。贵人【${c.guiRen}】。")
        items.add("旬空【${c.xunKong.joinToString("")}】，空亡之地主虚，待填实之日应事。")
        return items
    }
}

/**
 * 紫微解读器：命宫主星/四化/身宫（星曜传统释义，不引用商业文案）。
 */
object ZiweiInterpreter : Interpreter<Astrolabe> {
    override val toolName = "ziwei_interpret"
    override val toolDesc = "紫微斗数盘解读：命宫主星、四化"

    private val STAR_CHAR = mapOf(
        "紫微" to "帝星，主贵气与领导力，格局高者掌权",
        "天机" to "智星，主聪明机变，善策划",
        "太阳" to "贵星，主光明磊落、热心助人",
        "武曲" to "财星，主刚毅务实、财帛经营",
        "天同" to "福星，主温和享福、随和",
        "廉贞" to "次桃花星，主才艺与是非并存",
        "天府" to "库星，主稳重守成、财库丰盈",
        "太阴" to "田宅主，主细腻内敛、母性照拂",
        "贪狼" to "桃花星，主才艺交际、欲望与进取",
        "巨门" to "暗星，主口才与是非、需谨言",
        "天相" to "印星，主辅佐协调、公正",
        "天梁" to "荫星，主长辈庇护、解难",
        "七杀" to "将星，主魄力冲劲、先难后成",
        "破军" to "耗星，主开创变动、破旧立新",
    )

    private val SI_HUA = mapOf("禄" to "得财之机", "权" to "掌权之机", "科" to "名声之机", "忌" to "收敛之忧")

    override fun interpret(a: Astrolabe): List<String> {
        val items = mutableListOf<String>()
        val ming = a.palaces.firstOrNull { it.name == "命宫" }
        if (ming != null) {
            val stars = ming.majorStars.map { it.name }
            val starDesc = stars.joinToString("、") { "${it}（${STAR_CHAR[it] ?: "主星"}）" }
            items.add("命宫【${ming.name}】${ming.heavenlyStem}${ming.earthlyBranch}，主星：${if (stars.isEmpty()) "无主星（借对宫）" else starDesc}。")
        }
        // 四化：仅列有化禄/权/科/忌之星
        val sihua = a.palaces.flatMap { p ->
            p.majorStars.mapNotNull { s ->
                s.mutagen?.let { m -> "${p.name}${s.name}化$m" }
            }
        }
        if (sihua.isNotEmpty()) {
            val lu = sihua.filter { it.endsWith("禄") }.joinToString("、")
            val quan = sihua.filter { it.endsWith("权") }.joinToString("、")
            val ke = sihua.filter { it.endsWith("科") }.joinToString("、")
            val ji = sihua.filter { it.endsWith("忌") }.joinToString("、")
            items.add(
                buildString {
                    if (lu.isNotEmpty()) append("化禄：$lu（得财之机）。")
                    if (quan.isNotEmpty()) append("化权：$quan（掌权之机）。")
                    if (ke.isNotEmpty()) append("化科：$ke（名声之机）。")
                    if (ji.isNotEmpty()) append("化忌：$ji（收敛之忧）。")
                }
            )
        }
        items.add("五行局【${a.fiveElementsClass}】，命主【${a.soul}】，身主【${a.body}】。")
        return items
    }
}

/**
 * 黄历解读器：宜忌/吉神/冲煞（lunar-java 数据直接组织）。
 */
object HuangLiInterpreter {
    fun interpret(lunar: com.nlf.calendar.Lunar): List<String> {
        val items = mutableListOf<String>()
        items.add("今日【${lunar.toString()}】。")
        val yi = lunar.getDayYi().take(8)
        val ji = lunar.getDayJi().take(8)
        if (yi.isNotEmpty()) items.add("宜：${yi.joinToString("、")}。")
        if (ji.isNotEmpty()) items.add("忌：${ji.joinToString("、")}。")
        val js = lunar.getDayJiShen().take(6)
        if (js.isNotEmpty()) items.add("吉神：${js.joinToString("、")}。")
        val xs = lunar.getDayXiongSha().take(6)
        if (xs.isNotEmpty()) items.add("凶煞：${xs.joinToString("、")}。")
        items.add("冲【${lunar.getDayChong()}】煞【${lunar.getDaySha()}】，彭祖百忌：${lunar.getPengZuGan()}、${lunar.getPengZuZhi()}。")
        return items
    }
}
