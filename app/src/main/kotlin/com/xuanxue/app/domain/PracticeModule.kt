package com.xuanxue.app.domain

enum class ModuleStage {
    Ready,
    CorpusPrep,
}

data class PracticeModule(
    val id: String,
    val title: String,
    val description: String,
    val stage: ModuleStage,
    val corpusRequest: String,
)

object PracticeModules {
    val Ziwei = PracticeModule(
        id = "ziwei",
        title = "紫微斗数",
        description = "十二宫 · 主星四化 · 大限小限",
        stage = ModuleStage.Ready,
        corpusRequest = "排盘核心已接入并通过黄金夹具验证。",
    )

    val Qimen = PracticeModule(
        id = "qimen",
        title = "奇门遁甲",
        description = "起局 · 用神 · 宫盘 · 生克 · 应期",
        stage = ModuleStage.CorpusPrep,
        corpusRequest = "需要把本地奇门资料整理成可追溯的规则、分歧、案例与起局规范，再实现 qimen-core。",
    )

    val Bazi = PracticeModule(
        id = "bazi",
        title = "八字命理",
        description = "排盘 · 旺衰 · 格局 · 十神 · 大运流年",
        stage = ModuleStage.CorpusPrep,
        corpusRequest = "需要把本地八字资料按排盘规则、流派差异、命例验证和可计算规则拆分，再实现 bazi-core。",
    )

    val Liuyao = PracticeModule(
        id = "liuyao",
        title = "六爻",
        description = "起卦 · 装卦 · 六亲 · 世应 · 动变",
        stage = ModuleStage.CorpusPrep,
        corpusRequest = "需要整理起卦与装卦算法、纳甲体系、六亲世应、旺衰动变、用神与应期规则，再实现 liuyao-core。",
    )

    val Liuren = PracticeModule(
        id = "liuren",
        title = "大六壬",
        description = "天地盘 · 四课 · 三传 · 神将 · 课体",
        stage = ModuleStage.CorpusPrep,
        corpusRequest = "需要整理月将、占时、天地盘、四课三传、天将、课体与断课规则，并记录不同传承算法分歧，再实现 liuren-core。",
    )

    val all = listOf(Ziwei, Qimen, Bazi, Liuyao, Liuren)
    val studyBacked = listOf(Qimen, Bazi, Liuyao, Liuren)

    fun byId(id: String?): PracticeModule? = all.firstOrNull { it.id == id }
}
