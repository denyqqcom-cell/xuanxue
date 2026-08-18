package com.xuanxue.qimen.core.ju

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.calendar.Jieqi
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch

enum class Yuan(val zh: String) {
    SHANG("上"),
    ZHONG("中"),
    XIA("下"),
}

data class FutouYuan(
    val currentDay: StemBranch,
    val futou: StemBranch,
    val daysBack: Int,
    val yuan: Yuan,
)

/**
 * 拆补的“元”按最近一个甲/己日符头所属地支组确定。
 * 交节只改变当前节气；不会把交节当日强制改成上元。
 */
object FutouYuanResolver {
    fun resolve(dayPillar: StemBranch): FutouYuan {
        val currentIndex = StemBranch.sexagenaryIndexOf(dayPillar.stem, dayPillar.branch)
        val daysBack = dayPillar.stem.ordinal % 5
        val futou = StemBranch.fromSexagenaryIndex(currentIndex - daysBack)
        check(futou.stem == Stem.JIA || futou.stem == Stem.JI) {
            "Resolved futou must be Jia/Ji, got ${futou.zh}"
        }
        return FutouYuan(
            currentDay = dayPillar,
            futou = futou,
            daysBack = daysBack,
            yuan = yuanOfFutouBranch(futou.branch),
        )
    }

    fun yuanOfFutouBranch(branch: Branch): Yuan = when (branch) {
        Branch.ZI, Branch.WU, Branch.MAO, Branch.YOU -> Yuan.SHANG
        Branch.YIN, Branch.SHEN, Branch.SI, Branch.HAI -> Yuan.ZHONG
        Branch.CHEN, Branch.XU, Branch.CHOU, Branch.WEI -> Yuan.XIA
    }
}

data class JuResult(
    val jieqi: Jieqi,
    val dun: Dun,
    val yuan: Yuan,
    val ju: Int,
)

/**
 * 二十四节气 × 上中下元局数表。
 * 这是数值规则数据，不包含现代书籍的解释文字。
 */
object JuTable {
    private val rows: Map<Jieqi, Triple<Int, Int, Int>> = mapOf(
        Jieqi.DONG_ZHI to Triple(1, 7, 4),
        Jieqi.XIAO_HAN to Triple(2, 8, 5),
        Jieqi.DA_HAN to Triple(3, 9, 6),
        Jieqi.LI_CHUN to Triple(8, 5, 2),
        Jieqi.YU_SHUI to Triple(9, 6, 3),
        Jieqi.JING_ZHE to Triple(1, 7, 4),
        Jieqi.CHUN_FEN to Triple(3, 9, 6),
        Jieqi.QING_MING to Triple(4, 1, 7),
        Jieqi.GU_YU to Triple(5, 2, 8),
        Jieqi.LI_XIA to Triple(4, 1, 7),
        Jieqi.XIAO_MAN to Triple(5, 2, 8),
        Jieqi.MANG_ZHONG to Triple(6, 3, 9),
        Jieqi.XIA_ZHI to Triple(9, 3, 6),
        Jieqi.XIAO_SHU to Triple(8, 2, 5),
        Jieqi.DA_SHU to Triple(7, 1, 4),
        Jieqi.LI_QIU to Triple(2, 5, 8),
        Jieqi.CHU_SHU to Triple(1, 4, 7),
        Jieqi.BAI_LU to Triple(9, 3, 6),
        Jieqi.QIU_FEN to Triple(7, 1, 4),
        Jieqi.HAN_LU to Triple(6, 9, 3),
        Jieqi.SHUANG_JIANG to Triple(5, 8, 2),
        Jieqi.LI_DONG to Triple(6, 9, 3),
        Jieqi.XIAO_XUE to Triple(5, 8, 2),
        Jieqi.DA_XUE to Triple(4, 7, 1),
    )

    init {
        check(rows.size == Jieqi.entries.size)
        rows.values.forEach { row ->
            check(listOf(row.first, row.second, row.third).all { it in 1..9 })
        }
    }

    fun resolve(jieqi: Jieqi, dun: Dun, yuan: Yuan): JuResult {
        val expectedDun = com.xuanxue.qimen.core.calendar.JieqiClock.dunFor(jieqi)
        require(dun == expectedDun) {
            "Dun $dun conflicts with jieqi ${jieqi.zh}; expected $expectedDun"
        }
        val row = checkNotNull(rows[jieqi])
        val ju = when (yuan) {
            Yuan.SHANG -> row.first
            Yuan.ZHONG -> row.second
            Yuan.XIA -> row.third
        }
        return JuResult(jieqi, dun, yuan, ju)
    }
}
