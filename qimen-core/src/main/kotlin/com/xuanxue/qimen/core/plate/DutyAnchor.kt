package com.xuanxue.qimen.core.plate

import com.xuanxue.qimen.core.xun.XunInfo

enum class QimenStar(val zh: String) {
    TIAN_PENG("天蓬"),
    TIAN_RUI("天芮"),
    TIAN_CHONG("天冲"),
    TIAN_FU("天辅"),
    TIAN_QIN("天禽"),
    TIAN_XIN("天心"),
    TIAN_ZHU("天柱"),
    TIAN_REN("天任"),
    TIAN_YING("天英"),
}

enum class QimenGate(val zh: String) {
    XIU("休门"),
    SI("死门"),
    SHANG("伤门"),
    DU("杜门"),
    KAI("开门"),
    JING("惊门"),
    SHENG("生门"),
    JING_SCENERY("景门"),
}

enum class DutyGateAnchorState {
    RESOLVED,
    /** 当前支持的转盘规则中，中五寄坤二，因此中五旬首取坤二原驻死门为值使门。 */
    CENTER_PALACE_HOSTED_KUN2,
}

data class DutyAnchor(
    /** 旬首遁仪在地盘的实际宫位；值使随时支推进也从这里起步。 */
    val dunYiPalace: Int,
    val valueStar: QimenStar,
    /** 值使门的原驻来源宫；中五时为寄宫坤二。 */
    val gateHomePalace: Int,
    val valueGate: QimenGate,
    val gateState: DutyGateAnchorState,
)

/**
 * 值符/值使的旬首初始锚点。
 *
 * 当前支持的转盘规则：
 * 1. 在地盘找到本旬遁仪所在宫；
 * 2. 该宫原驻九星为值符星；
 * 3. 普通八宫以同宫原驻八门为值使门；
 * 4. 遁仪落中五时，采用已由完整阴遁实例复核的“中五寄坤二”：值符为天禽，值使取坤二死门，
 *    但值使的时支推进起点仍是中五宫，而不是二宫。
 *
 * 这里只解析旬首锚点，不负责完整天盘/人盘排列。
 */
object DutyAnchorResolver {
    private val homeStars = mapOf(
        1 to QimenStar.TIAN_PENG,
        2 to QimenStar.TIAN_RUI,
        3 to QimenStar.TIAN_CHONG,
        4 to QimenStar.TIAN_FU,
        5 to QimenStar.TIAN_QIN,
        6 to QimenStar.TIAN_XIN,
        7 to QimenStar.TIAN_ZHU,
        8 to QimenStar.TIAN_REN,
        9 to QimenStar.TIAN_YING,
    )

    private val homeGates = mapOf(
        1 to QimenGate.XIU,
        2 to QimenGate.SI,
        3 to QimenGate.SHANG,
        4 to QimenGate.DU,
        6 to QimenGate.KAI,
        7 to QimenGate.JING,
        8 to QimenGate.SHENG,
        9 to QimenGate.JING_SCENERY,
    )

    fun resolve(earthPlate: EarthPlate, xun: XunInfo): DutyAnchor {
        val palace = earthPlate.palaceOf(xun.dunYi)
            ?: error("Xun dun-yi ${xun.dunYi.zh} is missing from earth plate")
        val star = checkNotNull(homeStars[palace]) { "Missing home star for palace $palace" }
        val centerHosted = palace == 5
        val gateHomePalace = if (centerHosted) 2 else palace
        val gate = checkNotNull(homeGates[gateHomePalace]) {
            "Missing home gate for resolved host palace $gateHomePalace"
        }
        return DutyAnchor(
            dunYiPalace = palace,
            valueStar = star,
            gateHomePalace = gateHomePalace,
            valueGate = gate,
            gateState = if (centerHosted) {
                DutyGateAnchorState.CENTER_PALACE_HOSTED_KUN2
            } else {
                DutyGateAnchorState.RESOLVED
            },
        )
    }
}
