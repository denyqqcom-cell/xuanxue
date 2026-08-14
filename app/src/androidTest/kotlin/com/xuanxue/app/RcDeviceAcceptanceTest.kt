package com.xuanxue.app

import android.content.ContentValues
import android.graphics.Bitmap
import android.os.Environment
import android.os.SystemClock
import android.provider.MediaStore
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
 * Screenshots are synchronously captured from UiAutomation and persisted into
 * shared Downloads through MediaStore so post-test APK cleanup cannot erase
 * acceptance evidence. A short frame-settle delay is intentional: Compose can
 * be semantically idle before the emulator compositor has presented the new
 * frame, and visual evidence must reflect the asserted screen rather than the
 * preceding frame.
 *
 * This closes navigation/responsive/offline/main-path smoke acceptance in
 * automation. It does not claim physical-device ergonomics, divination
 * correctness, or full-board Qimen verification.
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
            openModule(id)
            capture("${formFactor}-$id")
            backHome()
        }
    }

    @Test
    fun coreModuleActionsProduceStructuralResultsWithoutCrashing() {
        openModule("ziwei")
        composeRule.onNodeWithText("排盘").performScrollTo().performClick()
        composeRule.onNodeWithText("十二宫概览 · 点击宫位查看完整星曜与限运").assertExists().performScrollTo()
        composeRule.onNodeWithText("命宫干支", substring = true).assertExists()
        capture("${formFactor}-ziwei-result")
        backHome()

        openModule("bazi")
        composeRule.onNodeWithText("00:30").assertExists()
        composeRule.onNodeWithText("02:30").assertExists()
        composeRule.onNodeWithText("排盘").performScrollTo().performClick()
        composeRule.onNodeWithText("大运 (", substring = true).assertExists()
        composeRule.onNodeWithText("年柱").assertExists().performScrollTo()
        capture("${formFactor}-bazi-result")
        backHome()

        openModule("qimen")
        composeRule.onNodeWithText("生成当前实验局").performScrollTo().performClick()
        composeRule.onNodeWithText("基础结果").assertExists().performScrollTo()
        composeRule.onNodeWithText("实验九宫（开发核对视图）").assertExists()
        capture("${formFactor}-qimen-result")
        backHome()

        openModule("liuyao")
        composeRule.onNodeWithText("数字起卦").performScrollTo().performClick()
        composeRule.onNodeWithText("上卦数").assertExists()
        composeRule.onNodeWithText("下卦数").assertExists()
        composeRule.onNodeWithText("动爻数").assertExists()
        composeRule.onNodeWithText("起卦").performScrollTo().performClick()
        composeRule.onNodeWithText("动爻:", substring = true).assertExists().performScrollTo()
        capture("${formFactor}-liuyao-result")
        backHome()

        openModule("liuren")
        composeRule.onNodeWithText("夜占").performScrollTo().performClick()
        composeRule.onNodeWithText("起课").performScrollTo().performClick()
        composeRule.onNodeWithText("三传:", substring = true).assertExists().performScrollTo()
        composeRule.onNodeWithText("四课").assertExists()
        composeRule.onNodeWithText("天地盘").assertExists()
        capture("${formFactor}-liuren-result")
        backHome()

        openModule("huangli")
        composeRule.onNodeWithText("黄历（万年历）").assertExists()
        composeRule.onNodeWithText("干支").assertExists()
        composeRule.onNodeWithText("宜").assertExists().performScrollTo()
        composeRule.onNodeWithText("忌").assertExists()
        capture("${formFactor}-huangli-result")
        backHome()
    }

    @Test
    fun qimenKeepsExperimentalBoundaryContextGateAndCurrentDeviceDateVisible() {
        openModule("qimen")

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

    private fun openModule(id: String) {
        composeRule.onNodeWithTag("module-open-$id")
            .performScrollTo()
            .performClick()
        composeRule.onNodeWithTag("module-host-$id").assertExists()
    }

    private fun backHome() {
        composeRule.onNodeWithTag("back-home").performClick()
        composeRule.onNodeWithTag("home-root").assertExists()
    }

    private fun capture(name: String) {
        composeRule.waitForIdle()
        SystemClock.sleep(300)
        composeRule.waitForIdle()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val bitmap = instrumentation.uiAutomation.takeScreenshot()
            ?: error("UiAutomation screenshot returned null")
        val resolver = instrumentation.targetContext.contentResolver
        val values = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, "$name.png")
            put(MediaStore.MediaColumns.MIME_TYPE, "image/png")
            put(
                MediaStore.MediaColumns.RELATIVE_PATH,
                Environment.DIRECTORY_DOWNLOADS + "/xuanxue-rc-screenshots",
            )
            put(MediaStore.MediaColumns.IS_PENDING, 1)
        }
        val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
            ?: error("Unable to create MediaStore screenshot for $name")
        try {
            resolver.openOutputStream(uri)?.use { output ->
                check(bitmap.compress(Bitmap.CompressFormat.PNG, 100, output)) {
                    "Failed to encode screenshot $name"
                }
            } ?: error("Unable to open screenshot output stream for $name")
            values.clear()
            values.put(MediaStore.MediaColumns.IS_PENDING, 0)
            resolver.update(uri, values, null, null)
        } catch (t: Throwable) {
            resolver.delete(uri, null, null)
            throw t
        } finally {
            bitmap.recycle()
        }
    }
}
