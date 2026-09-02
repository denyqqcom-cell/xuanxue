package com.xuanxue.ai

import com.xuanxue.liuren.LiuRenEngine.LiuRenChart
import com.xuanxue.qimen.QimenEngine.QimenChart
import com.xuanxue.liuyao.LiuYaoEngine.LiuYaoChart
import com.xuanxue.ziwei.core.ZiweiAstro.Astrolabe

/**
 * 奇门解释层。
 *
 * handoff/qimen 明确记录：当前资料有 calendar/table/map fixtures，但完整九宫只完成局部来源夹具，
 * 地盘 walk 与人盘方向仍有冲突。因此这里不再把完整九宫当作已核验事实去断吉凶；
 * JuMethod 身份也必须进入解释 provenance，工程默认不能被静默当成传统唯一法。
 */
object QimenInterpreter : Interpreter<QimenChart> {
    override val toolName = "qimen_interpret"
    override val toolDesc = "奇门基础事实整理：历法、局、日空/时空、定元实现身份；完整九宫仅标实验"

    override fun interpret(c: QimenChart): List<String> = buildList {
        add("当前引擎结果：四柱【${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}】，节气【${c.jieQi}】，${c.juText}；定元实现【${c.juMethodUsed}】。局数与定元必须结合所选方法理解，不把工程默认或“拆补”标签当成只有一种实现。")
        when (c.juMethodUsed) {
            "CHAI_BU_DAYCOUNT" -> add("定元实现边界：CHAI_BU_DAYCOUNT 是当前工程为兼容既有行为保留的日数分段近似；它不等同于已经验证的传统唯一拆补法，也不能借其他 JuMethod 的来源信用。")
            "CHAI_BU_FUTOU" -> add("定元实现边界：weather-v0.1 当前 CHAI_BU_FUTOU method vector 的甲/己五日符头、三元分类、实际交节切换、无闰拆补与局表组件已有来源约束，并通过独立天文边界回归；这只关闭该候选方法身份，不等于 DAYCOUNT、ZHI_RUN、完整置闰法或所有奇门起局传统等价，更不等于现实预测有效。")
            "ZHI_RUN" -> add("定元实现边界：ZHI_RUN 当前未重建/未夹具验证，正常执行应 fail-closed；若这里出现可执行结果，必须视为工程异常而不是术理证据。")
            else -> add("定元实现边界：当前 method id 未进入已登记方法身份表，不对其来源或正确性作推断。")
        }
        add("旬法信息：时旬首【${c.xunShou}】，遁干【${c.dunGan}】，日空【${c.dayKong.joinToString("、")}】，时空【${c.hourKong.joinToString("、")}】；马星【${c.maXing}】按当前时家实现由占时支取得。日空与时空是不同盘面字段，不再揉成一个“旬空”。")
        if (c.isWuBuYu) {
            add("历法/旬法标记：当前时柱满足五不遇时 generator。这里只记录规则命中，不把该标签单独翻译成现实事件。")
        }
        if (c.patterns.isNotEmpty()) {
            add("实验格局候选：${c.patterns.joinToString("、")}。这些候选依赖尚未完成多盘来源核验的天/地盘实现，因此不进入确定性断语。")
        }
        add("九宫实验边界：当前引擎可以生成值符【${c.zhiFu}】、值使【${c.zhiShi}】以及星门神九宫，但目前只有局部 source-grounded plate fixtures，尚不足以把完整九宫推广为全局黄金盘；因此本离线解释层不依据这些字段输出吉凶、成败或应期。")
        add("解盘纪律：书本象意、星门神标签与格局命中只属于候选语义，不是个案结论。进一步解盘必须先固定具体事体、角色/取用、时间尺度与现实约束，再检查哪些规则满足适用前提；随后根据落宫、生克、同宫/对宫、旺衰、空墓等已核验关系做情境化推演，并保留有区分力的竞争解释或弃权路径。缺少现实条件时不补造反馈，结果未知前不能用故事贴合度替代证据。")
    }
}

/** 六爻解释层：先展示结构，再提示传统取用必须结合事体。 */
object LiuYaoInterpreter : Interpreter<LiuYaoChart> {
    override val toolName = "liuyao_interpret"
    override val toolDesc = "六爻卦结构整理：世应、动爻、六亲、变卦"

    private val LIU_QIN_SCOPE = mapOf(
        "父母" to "传统取象常涉及文书、长辈、房屋等",
        "兄弟" to "传统取象常涉及同辈、竞争等",
        "子孙" to "传统取象常涉及子女、福神、解忧等",
        "妻财" to "传统取象常涉及钱财、伴侣、资源等",
        "官鬼" to "传统取象常涉及事业、压力、疾病等",
    )

    override fun interpret(c: LiuYaoChart): List<String> = buildList {
        add("卦象事实：【${c.benGua.name}】（${c.benGua.up}上${c.benGua.down}下，所属${c.benGua.palace}），日辰【${c.dayGZ}】。")
        val shi = c.benGua.yao.first { it.isShi }
        val ying = c.benGua.yao.first { it.isYing }
        add("世应位置：世爻在${shi.index}爻【${shi.liuQin}${shi.zhi}·${shi.liuShen}】，应爻在${ying.index}爻【${ying.liuQin}${ying.zhi}】。这里只记录位置关系，不从距离直接推出成败。")
        if (c.dongYaoIndexes.isEmpty()) {
            add("动爻结构：本卦没有变爻。‘无变爻’是结构事实，不自动等于现实中必须静守。")
        } else {
            val moving = c.dongYaoIndexes.map { c.benGua.yao[it - 1] }
            add("动爻结构：${moving.joinToString("、") { "${it.index}爻${it.liuQin}${it.zhi}" }}；${c.bianGua?.let { "变卦【${it.name}】" } ?: "无变卦数据"}。")
        }
        val qin = c.benGua.yao.map { it.liuQin }.toSet()
        val scopes = qin.mapNotNull { q -> LIU_QIN_SCOPE[q]?.let { "$q：$it" } }.joinToString("；")
        if (scopes.isNotBlank()) add("六亲传统取象范围：$scopes。真正用神必须先知道用户问什么，不能只见六亲就自动下结论。")
    }
}

/** 大六壬解释层：课型、三传、天将先作为结构事实展示。 */
object LiuRenInterpreter : Interpreter<LiuRenChart> {
    override val toolName = "liuren_interpret"
    override val toolDesc = "大六壬课结构整理：课型、三传、天将、旬空"

    private val KE_FA_LABEL = mapOf(
        "贼克（上克下）" to "传统分类常称元首课",
        "贼克（下贼上）" to "传统分类常称重审课",
        "比用" to "传统分类常称知一课",
        "涉害" to "涉害取法",
        "遥克" to "遥克取法",
        "遥贼" to "遥贼取法",
        "昴星" to "昴星取法",
        "别责" to "别责取法",
        "八专" to "八专取法",
        "返吟" to "返吟结构",
        "伏吟" to "伏吟结构",
    )

    override fun interpret(c: LiuRenChart): List<String> = buildList {
        add("课时事实：【${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}】，月将【${c.yueJiang}】加时。")
        add("课型：${c.sanChuan.fa}${KE_FA_LABEL[c.sanChuan.fa]?.let { "（$it）" } ?: ""}。课型名称是传统分类，不单独承担现实吉凶结论。")
        add("三传：【${c.sanChuan.chu}→${c.sanChuan.zhong}→${c.sanChuan.mo}】。初中末的意义需要与四课、类神和具体事体共同判断。")
        val tianJiang = c.tianJiang.mapIndexedNotNull { i, t -> if (t.isNotEmpty()) "${c.tianPan[i]}=$t" else null }.joinToString("、")
        add("天将分布：$tianJiang；贵人【${c.guiRen}】；旬空【${c.xunKong.joinToString("、")}】。当前只展示计算结果，不自动把空亡翻译成确定应期。")
    }
}

/** 紫微解释层：先列盘面结构，不把星曜标签直接人格化或事件化。 */
object ZiweiInterpreter : Interpreter<Astrolabe> {
    override val toolName = "ziwei_interpret"
    override val toolDesc = "紫微斗数结构整理：命宫主星、四化、五行局、命身主"

    override fun interpret(a: Astrolabe): List<String> = buildList {
        val ming = a.palaces.firstOrNull { it.name == "命宫" }
        if (ming != null) {
            val stars = ming.majorStars.joinToString("、") { star ->
                buildString {
                    append(star.name)
                    star.brightness?.takeIf { it.isNotBlank() }?.let { append("[$it]") }
                    star.mutagen?.takeIf { it.isNotBlank() }?.let { append("化$it") }
                }
            }
            add("命宫结构：【${ming.heavenlyStem}${ming.earthlyBranch}】，主星【${if (stars.isBlank()) "无主星" else stars}】。主星名称与亮度属于盘面字段，不直接等同于人格或事件结论。")
        }

        val siHua = a.palaces.flatMap { palace ->
            palace.majorStars.mapNotNull { star ->
                star.mutagen?.takeIf { it.isNotBlank() }?.let { "${palace.name}${star.name}化$it" }
            }
        }
        if (siHua.isNotEmpty()) add("四化分布：${siHua.joinToString("、")}。这里只列位置与标签，不把禄权科忌直接翻译成必然财、权、名、祸。")

        add("基础字段：五行局【${a.fiveElementsClass}】，命主【${a.soul}】，身主【${a.body}】。当前 fixture 证明 Kotlin 与 iztro 实现一致，不代表传统解释本身经过科学验证。")
    }
}

/** 黄历解释层：只组织 lunar-java 返回的传统历法字段。 */
object HuangLiInterpreter {
    fun interpret(lunar: com.nlf.calendar.Lunar): List<String> = buildList {
        add("日期：【${lunar}】。")
        val yi = lunar.getDayYi().take(8)
        val ji = lunar.getDayJi().take(8)
        if (yi.isNotEmpty()) add("传统黄历宜：${yi.joinToString("、")}。")
        if (ji.isNotEmpty()) add("传统黄历忌：${ji.joinToString("、")}。")
        val jiShen = lunar.getDayJiShen().take(6)
        if (jiShen.isNotEmpty()) add("吉神字段：${jiShen.joinToString("、")}。")
        val xiongSha = lunar.getDayXiongSha().take(6)
        if (xiongSha.isNotEmpty()) add("凶煞字段：${xiongSha.joinToString("、")}。")
        add("冲【${lunar.getDayChong()}】煞【${lunar.getDaySha()}】，彭祖百忌：${lunar.getPengZuGan()}、${lunar.getPengZuZhi()}。以上属于传统历法/民俗数据，不作为科学因果预测。")
    }
}
