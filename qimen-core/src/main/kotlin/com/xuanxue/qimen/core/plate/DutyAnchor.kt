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
    CENTER_PALACE_REQUIRES_HOST_RULE,
}

data class DutyAnchor(
    val dunYiPalace: Int,
    val valueStar: QimenStar,
    val valueGate: QimenGate?,
    val gateState: DutyGateAnchorState,
)

/**
 * 值符/值使的“旬首初始锚点”。
 *
 * 规则边界：
 * 1. 先在地盘找到本旬遁仪所在宫；
 * 2. 该宫原驻九星为值符星；
 * 3. 该宫原驻八门为值使门；
 * 4. 若遁仪落中五，八门没有原驻中门，不能在这里猜“寄坤/寄艮”，必须显式保持未决。
 *
 * 这里只解析初始锚点，不负责天盘旋转或值使随时支移动。
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
        val gate = homeGates[palace]
        return DutyAnchor(
            dunYiPalace = palace,
            valueStar = star,
            valueGate = gate,
            gateState = if (gate == null) {
                DutyGateAnchorState.CENTER_PALACE_REQUIRES_HOST_RULE
            } else {
                DutyGateAnchorState.RESOLVED
            },
        )
    }
}
