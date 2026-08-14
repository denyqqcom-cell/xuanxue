package com.xuanxue.ai

import com.xuanxue.bazi.BaziEngine

/**
 * 八字离线解释层。
 *
 * 本层只整理已经计算出的四柱、藏干、十神与大运时间线，并明确区分“结构事实”和
 * “传统解释”。不再仅凭日柱十二运就判定身强弱，也不把五行/天干标签写成人格定论。
 */
object BaziInterpreter : Interpreter<BaziEngine.BaziChart> {
    override val toolName = "bazi_interpret"
    override val toolDesc = "八字四柱结构整理：日主、五行显示权重、十神分布、大运时间线"

    private val GAN = "甲乙丙丁戊己庚辛壬癸"
    private val WX = "木木火火土土金金水水"

    override fun interpret(c: BaziEngine.BaziChart): List<String> {
        val items = mutableListOf<String>()
        val dayGan = c.dayZhu.gan
        val dayWx = WX.getOrNull(GAN.indexOf(dayGan))?.toString().orEmpty()

        items += "四柱结构：日主【$dayGan】属【$dayWx】，日支【${c.dayZhu.zhi}】，藏干【${c.dayZhu.hideGan.joinToString("、")}】，日柱十二运【${c.dayZhu.diShi}】。"

        // 这里只做可重复的“显示权重”：天干=2、藏干=1。它不是旺衰算法，也不是喜忌算法。
        val wxCount = mutableMapOf("金" to 0, "木" to 0, "水" to 0, "火" to 0, "土" to 0)
        c.fourZhu.forEach { zhu ->
            val ganIndex = GAN.indexOf(zhu.gan)
            if (ganIndex >= 0) {
                val ganWx = WX[ganIndex].toString()
                wxCount[ganWx] = (wxCount[ganWx] ?: 0) + 2
            }
            zhu.hideGan.forEach { hiddenGan ->
                val hiddenIndex = GAN.indexOf(hiddenGan)
                if (hiddenIndex >= 0) {
                    val hiddenWx = WX[hiddenIndex].toString()
                    wxCount[hiddenWx] = (wxCount[hiddenWx] ?: 0) + 1
                }
            }
        }
        val displayWeight = wxCount.entries
            .sortedByDescending { it.value }
            .joinToString(" ") { "${it.key}${it.value}" }
        items += "五行显示权重（天干=2、藏干=1）：$displayWeight。这个数字只用于观察盘面分布，不能直接等同于旺衰、格局或喜忌。"

        val shiShen = c.fourZhu
            .flatMap { listOf(it.shiShenGan) + it.shiShenZhi }
            .filter { it.isNotBlank() }
        val counts = shiShen.groupingBy { it }.eachCount()
            .entries.sortedByDescending { it.value }
            .joinToString("、") { "${it.key}×${it.value}" }
        if (counts.isNotBlank()) {
            items += "十神结构：$counts。当前只展示出现频次；具体取用必须结合月令、透藏、根气、制化与具体事体，不从频次直接推出吉凶。"
        }

        items += "身强弱边界：当前版本不使用“日柱十二运单点”直接判身强弱。十二运保留为盘面事实，后续需要建立可追溯的月令/根气/透藏/制化规则与夹具后再开放强弱结论。"

        if (c.daYun.isNotEmpty()) {
            val timeline = c.daYun.take(4).joinToString("；") { "${it.startYear}-${it.endYear} ${it.ganZhi}" }
            items += "大运时间线：${c.startYunAge}岁起运；$timeline。这里只显示时间与干支，不自动把某一步运写成必然吉凶。"
        }

        return items
    }
}
