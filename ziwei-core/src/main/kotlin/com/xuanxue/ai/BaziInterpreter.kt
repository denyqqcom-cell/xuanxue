package com.xuanxue.ai

import com.xuanxue.bazi.BaziEngine
import com.xuanxue.bazi.BaziEngine.BaziChart

/**
 * 八字离线解读：只编译笔记里可对照的手续。
 * 先结构后十神；十神不断性格；不自动应期；不宣称准确率。
 */
object BaziInterpreter : Interpreter<BaziChart> {
    override val toolName = "bazi_interpret"
    override val toolDesc = "八字四柱解读：五行、梁氏投票身强弱、十神只列名、空亡（离线，带来源）"

    override fun interpret(c: BaziChart): List<String> = interpretItems(c).map { it.summary }

    fun reading(c: BaziChart): Reading = Reading(
        toolName = toolName,
        items = interpretItems(c),
        overall = "离线规则摘录。先定日主强弱，再看十神。十神性格词典不下发。不是应期，也不宣称准确率。",
    )

    fun interpretItems(c: BaziChart): List<ReadingItem> {
        val items = mutableListOf<ReadingItem>()
        val dayGan = c.dayZhu.gan
        val dayWx = BaziRules.wxOfStem(dayGan)

        items += BaziRules.readingItem(
            BaziRules.LAYER_ALG, "R-BZ-PILLAR",
            "日主【$dayGan】属$dayWx。四柱【${c.yearZhu.gan}${c.yearZhu.zhi} ${c.monthZhu.gan}${c.monthZhu.zhi} ${c.dayZhu.gan}${c.dayZhu.zhi} ${c.timeZhu.gan}${c.timeZhu.zhi}】，日支藏干${c.dayZhu.hideGan.joinToString("、")}，日空【${c.dayKong}】。",
            "本机 BaziEngine / lunar-java 四柱",
            "A",
        )

        val wxCount = BaziRules.countWuXing(
            c.fourZhu.map { it.gan },
            c.fourZhu.flatMap { it.hideGan },
        )
        val sorted = wxCount.entries.sortedByDescending { it.value }
        items += BaziRules.readingItem(
            BaziRules.LAYER_ALG, "R-BZ-WUXING",
            "五行分布（干2分、藏干1分）：${sorted.joinToString(" ") { "${it.key}${it.value}" }}。最旺【${sorted.first().key}】，最弱【${sorted.last().key}】。此为计数，不是旺衰定论。",
            "公开干支五行表；计分权重为本机约定",
            "B",
        )

        val hideAll = c.fourZhu.flatMap { it.hideGan }
        val otherStems = listOf(c.yearZhu.gan, c.monthZhu.gan, c.timeZhu.gan)
        val vote = BaziRules.liangVote(
            dayGan,
            c.yearZhu.gan, c.yearZhu.zhi,
            c.monthZhu.gan, c.monthZhu.zhi,
            c.dayZhu.zhi,
            c.timeZhu.gan, c.timeZhu.zhi,
            hideAll,
            otherStems,
        )
        val voteLine = vote.votes.joinToString("、") {
            "${it.pos}${it.token}${BaziRules.kindLabel(it.kind)}${if (it.score > 0) "正" else if (it.score < 0) "负" else "平"}"
        }
        items += BaziRules.readingItem(
            BaziRules.LAYER_SCHOOL, "R-BZ-LIANG-VOTE",
            "梁湘润复式投票（笔记04重推）：${vote.plus}正 ${vote.minus}负 → 日主$dayGan 身${vote.strength}。得令=${if (vote.deLing) "是" else "否"}，得地(支藏比劫)=${if (vote.deDi) "是" else "否"}，得党(他干比劫)=${if (vote.deDang) "是" else "否"}。地支用本气，墓库未细分。",
            "笔记04 诸家交叉比对 · 梁湘润复式投票",
            "B",
            detail = voteLine,
        )

        items += BaziRules.readingItem(
            BaziRules.LAYER_SCHOOL, "R-BZ-DISHI",
            "日支十二运【${c.dayZhu.diShi}】只作数据。任铁樵经笔记04转述：执着长生十二宫生死败绝不足凭，本机不用十二运单独判身强弱。",
            "笔记04 明确否定的流行做法",
            "B",
        )

        val yong = when (vote.strength) {
            "偏旺" -> "扶抑方向倾向泄耗克（食伤/财/官杀）"
            "偏弱" -> "扶抑方向倾向生扶（印/比劫）"
            else -> "扶抑未一边倒，先看成败与流通，不自动取用"
        }
        items += BaziRules.readingItem(
            BaziRules.LAYER_SCHOOL, "R-BZ-YONG",
            "日主$dayGan，身${vote.strength}。$yong。用神一词在梁氏有格局/通关/病药/专旺/调候五义，本机只标扶抑方向，不点具体用神字。调候与扶抑谁优先（梁高调候 / 任未明言）只并列，不自动选。",
            "笔记04 用神五义；笔记39 第1步必须声明身强身弱",
            "B",
        )

        val shenSet = c.fourZhu.flatMap { listOf(it.shiShenGan) + it.shiShenZhi }.filter { it.isNotBlank() }.toSet()
        items += BaziRules.readingItem(
            BaziRules.LAYER_ALG, "R-BZ-SHISHEN",
            "日主$dayGan，身${vote.strength}。命局十神名目：${shenSet.joinToString("、")}。十神吉凶由用神/忌神决定，不下发性格词典，也不把正官等写成必定贵。",
            "笔记39 铁律；笔记15 公理1 结构优先",
            "B",
        )

        items += BaziRules.readingItem(
            BaziRules.LAYER_SCHOOL, "R-BZ-SHENSHA",
            "神煞不作吉凶主判。任铁樵经笔记转述反对专以神煞论命；梁湘润用作应期辅助。本机两者并列，不排神煞表。",
            "笔记04 神煞对立",
            "C",
        )

        if (c.daYun.isNotEmpty()) {
            val current = c.daYun.getOrNull(1) ?: c.daYun.first()
            items += BaziRules.readingItem(
                BaziRules.LAYER_ALG, "R-BZ-DAYUN",
                "${c.startYunAge}岁起运。列出大运【${current.ganZhi}】（${current.startYear}-${current.endYear}岁）仅作柱名。不按「印比运=贵人」套话；应期须运干运支逐柱对照原局，本机不做应期。",
                "笔记39 大运三问；笔记15 规则D 运限二分（观察，未升级）",
                "C",
            )
        }

        items += BaziRules.readingItem(
            BaziRules.LAYER_EXP, "R-BZ-CONG",
            "旺极从强、弱极从弱只作提醒，本机不自动改判从格。",
            "笔记39 日主强弱口诀",
            "C",
        )

        c.chengGu?.let { cg ->
            items += BaziRules.readingItem(
                BaziRules.LAYER_EXP, "R-BZ-CHENGGU",
                "称骨【${cg.weightText}】为袁天罡称骨歌民俗算法，非子平结构推演，不参与身强弱。",
                "公有领域歌诀；BaziEngine.ChengGu",
                "C",
            )
        }

        return items
    }
}
