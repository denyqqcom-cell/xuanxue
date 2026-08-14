package com.xuanxue.app

import android.os.ParcelFileDescriptor
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import java.util.Calendar
import kotlin.math.abs
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * RC1 emulator acceptance suite.
 *
 * The workflow runs this class twice against the same source head:
 * - narrow + light theme + airplane mode
 * - wide + dark theme + airplane mode
 *
 * Screenshots are written by UiAutomation's shell identity to shared Download
 * storage so Gradle's post-test package cleanup cannot delete the evidence.
 *
 * This closes navigation/responsive/offline smoke acceptance in automation.
 * It does not claim physical-device ergonomics, divination correctness, or
 * full-board Qimen verification.
 */
@RunWith(AndroidJUnit4::class)
class RcDeviceAcceptanceTest {
    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    private val formFactor: String
        get() = InstrumentationRegistry.getArguments().getString("formFactor") ?: "unknown"

    @Test
    fun homeRendersAndResponsiveLayoutMatchesConfiguredEmulator() {
        composeRule.onNodeWithTag("home-root").assertExists()
        composeRule.onNodeWithText("玄学工具箱").assertExists()

        val ziwei = composeRule.onNodeWithTag("module-card-ziwei").fetchSemanticsNode().boundsInRoot
        val bazi = composeRule.onNodeWithTag("module-card-bazi").fetchSemanticsNode().boundsInRoot

        when (formFactor) {
            "narrow" -> {
                assertTrue("narrow layout must stack first two module cards", bazi.top >= ziwei.bottom - 2f)
            }
            "wide" -> {
                assertTrue(
                    "wide layout must put first two module cards on the same row",
                    abs(ziwei.top - bazi.top) <= 4f && bazi.left > ziwei.left,
                )
            }
            else -> error("formFactor instrumentation argument is required")
        }

        capture("${formFactor}-home")
    }

    @Test
    fun allSixModulesOpenAndReturnToHome() {
        val modules = listOf("ziwei", "bazi", "qimen", "liuyao", "liuren", "huangli")
        modules.forEach { id ->
            composeRule.onNodeWithTag("module-open-$id")
                .performScrollTo()
                .performClick()
            composeRule.onNodeWithTag("module-host-$id").assertExists()
            capture("${formFactor}-$id")
            composeRule.onNodeWithTag("back-home").performClick()
            composeRule.onNodeWithTag("home-root").assertExists()
        }
    }

    @Test
    fun qimenKeepsExperimentalBoundaryContextGateAndCurrentDeviceDateVisible() {
        composeRule.onNodeWithTag("module-open-qimen")
            .performScrollTo()
            .performClick()

        composeRule.onNodeWithTag("module-host-qimen").assertExists()
        composeRule.onNodeWithText("实验九宫 · 不作为已核验标准盘").assertExists()
        composeRule.onNodeWithText("事体与现实条件").assertExists()

        val now = Calendar.getInstance()
        val expectedDatePrefix = "公历: ${now.get(Calendar.YEAR)}-${now.get(Calendar.MONTH) + 1}-${now.get(Calendar.DAY_OF_MONTH)}"
        composeRule.onNodeWithText(expectedDatePrefix, substring = true).assertExists()

        capture("${formFactor}-qimen-boundary")
    }

    @Test
    fun auditAndOpenSourceNoticesAreReachable() {
        composeRule.onNodeWithTag("open-audit").performClick()
        composeRule.onNodeWithTag("audit-root").assertExists()
        composeRule.onNodeWithText("方法核验中心").assertExists()
        capture("${formFactor}-audit")
        composeRule.onNodeWithTag("audit-back-home").performClick()

        composeRule.onNodeWithTag("open-legal").performClick()
        composeRule.onNodeWithText("开源许可").assertExists()
        composeRule.onNodeWithText("Copyright (c) 2018 6tail", substring = true).assertExists()
        capture("${formFactor}-legal")

        composeRule.activityRule.scenario.onActivity {
            it.onBackPressedDispatcher.onBackPressed()
        }
        composeRule.onNodeWithTag("home-root").assertExists()
    }

    private fun capture(name: String) {
        composeRule.waitForIdle()
        val uiAutomation = InstrumentationRegistry.getInstrumentation().uiAutomation
        execShell(uiAutomation.executeShellCommand("mkdir -p /sdcard/Download/xuanxue-rc-screenshots"))
        execShell(uiAutomation.executeShellCommand("screencap -p /sdcard/Download/xuanxue-rc-screenshots/$name.png"))
    }

    private fun execShell(descriptor: ParcelFileDescriptor) {
        ParcelFileDescriptor.AutoCloseInputStream(descriptor).use { input ->
            input.readBytes()
        }
    }
}
