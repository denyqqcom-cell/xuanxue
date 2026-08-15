package com.xuanxue.ai

import com.xuanxue.qimen.QimenEngine
import com.xuanxue.qimen.QimenEngine.QimenChart

/**
 * 奇门离线解读：只编译 handoff/qimen 里可对照的规则。
 * 算法 / 门派 / 经验分开；冲突只并列；不贴吉凶词典；不改盘面。
 */
object QimenInterpreter : Interpreter<QimenChart> {
    override val toolName = "qimen_interpret"
    override val toolDesc = "奇门遁甲盘解读：局法分叉、旬、五不遇时、击刑表、空亡并列（离线，带来源）"

    override fun interpret(c: QimenChart): List<String> = interpretItems(c).map { it.summary }

    fun reading(c: QimenChart): Reading = Reading(
        toolName = toolName,
        items = interpretItems(c),
        overall = "离线规则摘录。算法、门派、经验已分开；门派冲突只并列，不改盘面。不是应期，也不宣称准确率。",
    )

    fun interpretItems(c: QimenChart): List<ReadingItem> {
        val items = mutableListOf<ReadingItem>()
        val stamp = QimenRules.parseSolarDate(c.solarDate)

        items += QimenRules.readingItem(
            QimenRules.LAYER_ALG, "R-CAL-001",
            "时值【${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}】，节气【${c.jieQi}】。本机盘面 ${c.juText}。",
            "handoff 交叉验证锚点；盘面四柱取自本机引擎",
            "A",
        )

        val dayStem = c.dayGZ.firstOrNull()?.toString().orEmpty()
        val hourBranch = c.hourGZ.getOrNull(1)?.toString().orEmpty()
        val expectedHourStem = QimenRules.hourStemByWuShuDun(dayStem, hourBranch)
        if (expectedHourStem.isNotEmpty()) {
            val actual = c.hourGZ.firstOrNull()?.toString().orEmpty()
            val match = if (actual == expectedHourStem) "与五鼠遁表一致" else "本机时干$actual，五鼠遁表为$expectedHourStem，未改盘"
            items += QimenRules.readingItem(
                QimenRules.LAYER_ALG, "R-CAL-002",
                "时柱【${c.hourGZ}】按五鼠遁起时干，$match。",
                "qimen-qiju §11 日上起时",
                "A",
            )
        }

        if (stamp != null) {
            val slot = QimenRules.clockSlot(stamp.hour, stamp.minute)
            items += QimenRules.readingItem(
                QimenRules.LAYER_ALG, "R-CAL-003",
                "本机钟点 ${stamp.hour}:${"%02d".format(stamp.minute)} 按十三时辰为【$slot】。晚子只取 23:00–24:00；20:00–23:00 当晚子的笔记已否决（R-CAL-003B）。",
                "qiju §6；与紫微页同一套十三时辰",
                "B",
            )
        }

        val dunByJie = QimenRules.dunLabel(c.jieQi)
        if (dunByJie != null) {
            val boardDun = if (c.yinYang > 0) "阳遁" else "阴遁"
            val same = dunByJie == boardDun
            items += QimenRules.readingItem(
                QimenRules.LAYER_ALG, "R-DUN-001",
                "节气【${c.jieQi}】属$dunByJie（冬至至芒种阳，夏至至大雪阴）。本机盘面为$boardDun${if (same) "，一致" else "，不一致，只标出不改盘"}。",
                "qimen-qiju §1.1；知识库 §3",
                "B",
            )
        }

        val xun = QimenRules.xunOf(c.hourGZ)
        if (xun != null) {
            items += QimenRules.readingItem(
                QimenRules.LAYER_ALG, "R-XUN-001",
                "时旬首【${xun.xunShou}】遁【${xun.dunYi}】，旬空【${xun.xunKong.joinToString("")}】。",
                "qiju §3.3",
                "A",
            )
        }

        val dayIdx = if (c.jieqiDayIndex > 0) c.jieqiDayIndex else stamp?.let {
            QimenRules.jieqiDayIndex(it.year, it.month, it.day, c.jieQi)
        }
        val futouYuan = c.yuanFutou.ifEmpty { QimenEngine.yuanOf(c.dayGZ) }
        val futouJu = QimenRules.juOf(c.jieQi, futouYuan)
        val juSplit = futouJu != null && (futouYuan != c.yuan || futouJu != c.ju)
        items += QimenRules.readingItem(
            QimenRules.LAYER_SCHOOL, "R-JU-001",
            buildString {
                append("本机默认拆补·日数分段（${c.juMethodUsed}）")
                if (dayIdx != null) append("：${c.jieQi}第${dayIdx}天→${c.yuan}→${c.ju}局。")
                else append("：${c.yuan}→${c.ju}局。")
                if (futouJu != null) {
                    append("符头定元（R-JU-002）为${futouYuan}→${futouJu}局。")
                    if (juSplit) append("两法局数不同，盘面已按日数分段；符头只对照。")
                    else append("此日两法相同。")
                }
                if (dayIdx != null && dayIdx > 15) append("节气长于15日，下元划分为未另有来源。")
            },
            "知识库 §3.1；qiju §2.4；B01 pp.66–68 自相矛盾见 C-JU-CHAIBU-INTERNAL",
            "B",
        )

        val dunPalace = c.gongs.firstOrNull { it.diGan == c.dunGan }?.palace
        if (dunPalace != null) {
            val homeStar = QimenEngine.STAR_HOME[dunPalace]
            val homeGate = if (dunPalace == 5) "中5无门，寄坤2" else QimenEngine.GATE_HOME[dunPalace]
            items += QimenRules.readingItem(
                QimenRules.LAYER_ALG, "R-STAR-HOME",
                "遁仪【${c.dunGan}】在本机地盘${dunPalace}宫。原驻星【$homeStar】、原驻门【$homeGate】。本机值符【${c.zhiFu}】值使【${c.zhiShi}】。",
                "知识库 §2.1 §2.2；值符值使取原驻",
                "B",
            )
        }

        val hits = QimenRules.HIT_XING.mapNotNull { (yi, palace) ->
            val at = c.gongs.firstOrNull { it.diGan == yi }?.palace
            if (at == palace) "${yi}落${palace}宫" else null
        }
        items += QimenRules.readingItem(
            QimenRules.LAYER_ALG, "R-HIT-XING",
            buildString {
                append("六仪击刑表：戊3 己2 庚8 辛9 壬4 癸4。")
                if (hits.isEmpty()) append("本机地盘未落到表上宫位。")
                else append("按本机盘面触发：${hits.joinToString("、")}。")
                append("地盘走步尚未双书复核（C-PLATE-WALK），此条只对照表，不断吉凶。已废弃壬击刑亥、癸击刑子。")
            },
            "交叉验证 §验证2；知识库 §4.4",
            "B",
        )

        val hourStem = c.hourGZ.firstOrNull()?.toString().orEmpty()
        if (QimenRules.isWuBuYu(dayStem, hourStem)) {
            val printed = QimenRules.isPrintedWuBu(dayStem, hourStem, hourBranch)
            items += QimenRules.readingItem(
                QimenRules.LAYER_ALG, "R-WUBU-001",
                buildString {
                    append("时柱相对日干触发五不遇时生成器（日【$dayStem】时【${c.hourGZ}】）。")
                    if (printed) append("此对见于善天道印刷十对。")
                    else append("此对是生成器补全，印刷十对可能未列（R-WUBU-BOOK10）。")
                    append("只标手续，不断事。")
                },
                "交叉验证 §验证1；善天道精华 pp.25-26 经笔记转写",
                "B",
            )
        } else {
            items += QimenRules.readingItem(
                QimenRules.LAYER_ALG, "R-WUBU-001",
                "时柱未触发五不遇时生成器。",
                "交叉验证 §验证1",
                "B",
            )
        }

        items += QimenRules.readingItem(
            QimenRules.LAYER_SCHOOL, "R-GATE-ROT-A",
            "本机人盘按顺时针转排（笔记中的另一句）。阳顺阴逆随时支（B01 pp.70–71 转述）尚未解锁。人盘方向有分叉，本条只提示。",
            "qiju §10.3；C-GATE-ROTATION",
            "D",
        )

        val ma = c.gongs.firstOrNull { it.isMaXing }
        if (ma != null) {
            items += QimenRules.readingItem(
                QimenRules.LAYER_EXP, "R-MA-001",
                "驿马临${ma.palace}宫（地支【${c.maXing}】）。只标动态，不预设吉凶；方向要看星门神，本机不做应期。",
                "用户 2026-06-15 反省；handoff R-MA-001",
                "C",
            )
        }

        val kong = c.gongs.filter { it.isKong }.map { "${it.palace}宫" }
        if (kong.isNotEmpty()) {
            items += QimenRules.readingItem(
                QimenRules.LAYER_SCHOOL, "R-KONG-A",
                "旬空落${kong.joinToString("、")}。三说只并列、不自动取舍：①幺学声笔记转述「逢空则不吉」（B01 p.76）；②实例解析转述「空亡=方向未定」（B06 p.81）；③2026-06-15 练习改写「方向待定」（n=1，不是定律）。默认不把①写成硬失败。",
                "知识库 §4.3；C-KONG-MEANING",
                "C",
            )
        }

        items += QimenRules.readingItem(
            QimenRules.LAYER_SCHOOL, "R-YONG-001",
            "用神：幺学声以日干为求测者，善天道或以年命。本机不自动取用神宫。",
            "精读笔记_预测学收尾 §1.1；知识库 §5.3",
            "C",
        )

        items += QimenRules.readingItem(
            QimenRules.LAYER_EXP, "R-PRI-001",
            "先看顺序两说并列，不自动选：练习优先开门/外因，再看值符+死门情绪；善天道急则从神、缓则从门。",
            "6/15反省；知识库 §5.3；C-PRIORITY-VS-URGENCY",
            "C",
        )

        items += QimenRules.readingItem(
            QimenRules.LAYER_EXP, "R-SCORE-001",
            "不启用凶格分数自动决断，也不在本机输出大凶/停看。",
            "知识库 §4.2",
            "C",
        )

        return items
    }
}
