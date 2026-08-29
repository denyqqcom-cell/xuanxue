package com.xuanxue.ai

/**
 * 当前仓库层面的“方法核验状态”。
 *
 * 它描述的是代码/资料/夹具的成熟度，不对术数本身作科学有效性背书。
 */
enum class MethodMaturity(val label: String) {
    IMPLEMENTATION_PARITY("实现一致性已核验"),
    SOURCE_BACKED("资料可追溯"),
    PARTIAL_FIXTURES("部分夹具核验"),
    INTERNAL_REGRESSION("内部回归"),
    EXPERIMENTAL("实验能力"),
}

data class MethodAudit(
    val id: String,
    val title: String,
    val maturity: MethodMaturity,
    val summary: String,
    val verified: List<String>,
    val limitations: List<String>,
    val sourceIds: List<String>,
)

/**
 * 只登记当前仓库能够真实证明的状态。
 * 不把“测试通过”偷换成“术数必然正确”，也不把书中断语偷换成算法事实。
 */
object MethodAuditRegistry {
    val ziwei = MethodAudit(
        id = "ziwei",
        title = "紫微斗数",
        maturity = MethodMaturity.IMPLEMENTATION_PARITY,
        summary = "Kotlin 移植结果已用 7 组 fixture 与 iztro 原版逐字段比对；这证明移植一致，不等于对紫微术理作独立真伪验证。",
        verified = listOf(
            "7 组 fixture 覆盖阳男午时、阴女子时、闰月、晚子时、立春边界等输入",
            "核心排盘数据结构与 iztro 原版输出做一致性断言",
        ),
        limitations = listOf(
            "fixture 来自同一上游算法，属于实现 parity，不是独立第三方真值",
            "星曜性格、吉凶和事件判断属于传统解释层，不应伪装成计算事实",
        ),
        sourceIds = listOf("NOTICE", "ziwei-core/src/test/resources/fixtures.jsonl"),
    )

    val bazi = MethodAudit(
        id = "bazi",
        title = "八字",
        maturity = MethodMaturity.SOURCE_BACKED,
        summary = "四柱与历法基础由 lunar-java 本地计算；当前五行权重、身强弱与十神性格文字仍属于本项目的启发式解释层。",
        verified = listOf(
            "四柱/干支/历法基础来自 lunar-java",
            "BaziEngine 有单元测试覆盖基本排盘输出",
        ),
        limitations = listOf(
            "当前‘含藏干计分’不是统一流派标准",
            "仅凭日柱十二运判断身强弱过于简化，不能标记为定论",
            "十神性格文字属于传统解释，不是客观人格测量",
        ),
        sourceIds = listOf("NOTICE", "ziwei-core/src/test/kotlin/com/xuanxue/bazi/BaziEngineTest.kt"),
    )

    val qimen = MethodAudit(
        id = "qimen",
        title = "奇门遁甲",
        maturity = MethodMaturity.EXPERIMENTAL,
        summary = "资料交接与当前 K2 审计已把日时干支、旬首旬空、五不遇时、击刑、部分定局规则和局部 source-grounded dated fixtures 工程化；但这些局部夹具不足以建立完整九宫全局黄金盘，JuMethod 完整方法身份、交节边界与部分盘层冲突仍未关闭。",
        verified = listOf(
            "handoff/qimen 有 corpus manifest、规则分级、冲突表与 calendar/table/map fixtures",
            "可编码层包括日柱、五鼠遁、旬首旬空、五不遇时和部分静态映射",
            "甲/己五日符头及上中下元地支分类已有跨来源结构支持；1990-01-27 大寒下元阳遁六局已进入 dated regression",
            "QM-SRC-0021 的 2004-05-29 chart-only anchor 提供局部 dated plate / 九星位置核对，不代表全盘全局已验证",
        ),
        limitations = listOf(
            "已有局部 source-grounded dated plate fixture，但数量与覆盖不足，不能当作完整九宫全局黄金盘",
            "共享甲/己五日符头子结构不等于完整 JuMethod 等价；CHAI_BU_FUTOU 的交节、超神接气、置闰等方法身份仍需分别验证",
            "地盘 walk / 天盘 / 门盘 / 神盘的来源冲突与完整覆盖尚未全部关闭",
            "当前 QimenEngine 的完整九宫仍属于实验实现，局部 fixture 通过不能推广成全局术理验真",
            "用户可见断语必须带 school/source_id 或省略；现代书籍长断语禁止打包进 APK",
        ),
        sourceIds = listOf(
            "handoff/qimen/HANDOFF_SUMMARY.md",
            "handoff/qimen/04_CONFLICTS.md",
            "handoff/qimen/05_FIXTURES.jsonl",
            "handoff/qimen/07_COPYRIGHT_GATE.md",
            "knowledge/K2_QIMEN_JU_METHOD_CROSS_SOURCE_REVIEW_V01.md",
            "knowledge/K2_QIMEN_CDAF_H2_WEATHER_PILOT_V01_GATE_AMENDMENT.md",
        ),
    )

    val liuyao = MethodAudit(
        id = "liuyao",
        title = "六爻",
        maturity = MethodMaturity.INTERNAL_REGRESSION,
        summary = "当前实现包含纳甲、世应、六亲、六神与变卦等内部回归；仓库尚没有像 qimen handoff 那样独立整理的来源/冲突/版权交接包。",
        verified = listOf("LiuYaoEngine 有单元测试覆盖卦象与变卦基本合同"),
        limitations = listOf(
            "内部测试不能替代多来源课例交叉核验",
            "六亲用神、动爻吉凶等属于传统解释层，需按具体事体取用",
        ),
        sourceIds = listOf("ziwei-core/src/test/kotlin/com/xuanxue/liuyao/"),
    )

    val liuren = MethodAudit(
        id = "liuren",
        title = "大六壬",
        maturity = MethodMaturity.PARTIAL_FIXTURES,
        summary = "当前实现含九宗门、三传与天将，并有 1949-10-01 书例回归；但尚未形成完整的多书冲突矩阵与版权 gate。",
        verified = listOf(
            "1949-10-01 课例用于回归四柱/月将/三传/课型/贵人",
            "十二天将布宫与九宗门有内部测试",
        ),
        limitations = listOf(
            "单一或少量书例不能覆盖全部课式边界",
            "课型释义与应事仍属于传统解释层",
        ),
        sourceIds = listOf("ziwei-core/src/test/kotlin/com/xuanxue/liuren/"),
    )

    val huangli = MethodAudit(
        id = "huangli",
        title = "黄历",
        maturity = MethodMaturity.SOURCE_BACKED,
        summary = "宜忌、吉神凶煞、冲煞等数据直接来自 lunar-java 的本地历法接口。",
        verified = listOf("日期与黄历字段由 lunar-java 1.7.7 本地计算"),
        limitations = listOf(
            "这些字段属于传统历法/民俗信息，不是科学因果预测",
            "App 只组织展示上游字段，不应额外放大成保证性吉凶结论",
        ),
        sourceIds = listOf("NOTICE", "cn.6tail:lunar:1.7.7"),
    )

    val all: List<MethodAudit> = listOf(ziwei, bazi, qimen, liuyao, liuren, huangli)

    fun byId(id: String): MethodAudit? = all.firstOrNull { it.id == id }
}
