package com.xuanxue.ai

/**
 * 八字笔记里可对照的手续。不编码性格断语，不自动应期。
 * 来源：`八字/学习笔记/04` 梁氏投票、`39` 手册铁律、`15` 结构优先。
 */
object BaziRules {

    const val LAYER_ALG = "算法"
    const val LAYER_SCHOOL = "门派"
    const val LAYER_EXP = "经验"

    val STEM_WX = mapOf(
        "甲" to "木", "乙" to "木", "丙" to "火", "丁" to "火", "戊" to "土",
        "己" to "土", "庚" to "金", "辛" to "金", "壬" to "水", "癸" to "水",
    )
    val BRANCH_WX = mapOf(
        "子" to "水", "丑" to "土", "寅" to "木", "卯" to "木", "辰" to "土", "巳" to "火",
        "午" to "火", "未" to "土", "申" to "金", "酉" to "金", "戌" to "土", "亥" to "水",
    )
    private val SHENG = mapOf("水" to "木", "木" to "火", "火" to "土", "土" to "金", "金" to "水")
    private val KE = mapOf("木" to "土", "土" to "水", "水" to "火", "火" to "金", "金" to "木")

    enum class VoteKind { BI_JIE, YIN, SHI_SHANG, CAI, GUAN_SHA, UNKNOWN }

    data class Vote(
        val pos: String,
        val token: String,
        val wx: String,
        val kind: VoteKind,
        val score: Int,
    )

    data class LiangVote(
        val dayWx: String,
        val deLing: Boolean,
        val deDi: Boolean,
        val deDang: Boolean,
        val votes: List<Vote>,
        val plus: Int,
        val minus: Int,
    ) {
        val strength: String
            get() = when {
                plus > minus -> "偏旺"
                minus > plus -> "偏弱"
                else -> "中和"
            }
    }

    fun wxOfStem(gan: String): String = STEM_WX[gan].orEmpty()
    fun wxOfBranch(zhi: String): String = BRANCH_WX[zhi].orEmpty()

    fun kindOf(dayWx: String, otherWx: String): VoteKind = when {
        otherWx.isEmpty() || dayWx.isEmpty() -> VoteKind.UNKNOWN
        otherWx == dayWx -> VoteKind.BI_JIE
        SHENG[otherWx] == dayWx -> VoteKind.YIN
        SHENG[dayWx] == otherWx -> VoteKind.SHI_SHANG
        KE[dayWx] == otherWx -> VoteKind.CAI
        KE[otherWx] == dayWx -> VoteKind.GUAN_SHA
        else -> VoteKind.UNKNOWN
    }

    fun scoreOf(kind: VoteKind): Int = when (kind) {
        VoteKind.BI_JIE, VoteKind.YIN -> 1
        VoteKind.SHI_SHANG, VoteKind.CAI, VoteKind.GUAN_SHA -> -1
        VoteKind.UNKNOWN -> 0
    }

    fun kindLabel(kind: VoteKind): String = when (kind) {
        VoteKind.BI_JIE -> "比劫"
        VoteKind.YIN -> "印"
        VoteKind.SHI_SHANG -> "食伤"
        VoteKind.CAI -> "财"
        VoteKind.GUAN_SHA -> "官杀"
        VoteKind.UNKNOWN -> "未分"
    }

    /**
     * 梁湘润复式投票：年干支、月干支、日支、时干支对日主计正负。
     * 地支用本气，墓库藏干未细分。
     */
    fun liangVote(
        dayGan: String,
        yearGan: String, yearZhi: String,
        monthGan: String, monthZhi: String,
        dayZhi: String,
        timeGan: String, timeZhi: String,
        hideGan: List<String>,
        otherStems: List<String>,
    ): LiangVote {
        val dayWx = wxOfStem(dayGan)
        fun one(pos: String, token: String, wx: String): Vote {
            val k = kindOf(dayWx, wx)
            return Vote(pos, token, wx, k, scoreOf(k))
        }
        val votes = listOf(
            one("年干", yearGan, wxOfStem(yearGan)),
            one("年支", yearZhi, wxOfBranch(yearZhi)),
            one("月干", monthGan, wxOfStem(monthGan)),
            one("月支", monthZhi, wxOfBranch(monthZhi)),
            one("日支", dayZhi, wxOfBranch(dayZhi)),
            one("时干", timeGan, wxOfStem(timeGan)),
            one("时支", timeZhi, wxOfBranch(timeZhi)),
        )
        val plus = votes.count { it.score > 0 }
        val minus = votes.count { it.score < 0 }
        val deLing = wxOfBranch(monthZhi) == dayWx
        val deDi = hideGan.any { wxOfStem(it) == dayWx }
        val deDang = otherStems.any { wxOfStem(it) == dayWx }
        return LiangVote(dayWx, deLing, deDi, deDang, votes, plus, minus)
    }

    fun countWuXing(stems: List<String>, hideGan: List<String>): Map<String, Int> {
        val wxCount = mutableMapOf("金" to 0, "木" to 0, "水" to 0, "火" to 0, "土" to 0)
        stems.forEach { g ->
            val w = wxOfStem(g)
            if (w.isNotEmpty()) wxCount[w] = (wxCount[w] ?: 0) + 2
        }
        hideGan.forEach { hg ->
            val w = wxOfStem(hg)
            if (w.isNotEmpty()) wxCount[w] = (wxCount[w] ?: 0) + 1
        }
        return wxCount
    }

    fun readingItem(
        layer: String,
        ruleId: String,
        summary: String,
        source: String,
        confidence: String,
        detail: String = "",
    ): ReadingItem = ReadingItem(
        title = "$layer · $ruleId",
        summary = summary,
        detail = detail,
        layer = layer,
        ruleId = ruleId,
        source = source,
        confidence = confidence,
    )
}
