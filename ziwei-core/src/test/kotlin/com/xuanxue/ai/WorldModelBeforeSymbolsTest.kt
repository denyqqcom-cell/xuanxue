package com.xuanxue.ai

import kotlin.test.Test
import kotlin.test.assertNotNull

class WorldModelBeforeSymbolsTest {
    @Test
    fun `core exposes explicit M0 to M4 reasoning contract`() {
        assertNotNull(
            Class.forName("com.xuanxue.ai.QimenReasoningStages"),
            "World Model Before Symbols core contract is not implemented",
        )
    }
}
