package com.xuanxue.app.ui

import androidx.activity.compose.BackHandler
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import com.xuanxue.app.ui.chart.BirthProfile
import com.xuanxue.app.ui.chart.ChartScreen
import com.xuanxue.app.ui.chart.CreateChartScreen
import com.xuanxue.app.ui.home.HomeScreen
import com.xuanxue.app.ui.legal.OpenSourceScreen
import com.xuanxue.ziwei.core.ZiweiAstro

private enum class AppScreen {
    Home,
    Create,
    Chart,
    Licenses,
}

@Composable
fun XuanxueApp() {
    var screenName by rememberSaveable { mutableStateOf(AppScreen.Home.name) }
    var savedDate by rememberSaveable { mutableStateOf<String?>(null) }
    var savedTimeIndex by rememberSaveable { mutableStateOf(6) }
    var savedGender by rememberSaveable { mutableStateOf("male") }
    var savedFixLeap by rememberSaveable { mutableStateOf(false) }

    val screen = runCatching { AppScreen.valueOf(screenName) }.getOrDefault(AppScreen.Home)
    val profile = savedDate?.let {
        BirthProfile(
            solarDate = it,
            timeIndex = savedTimeIndex,
            gender = savedGender,
            fixLeap = savedFixLeap,
        )
    }
    val chart = remember(profile) {
        profile?.let {
            ZiweiAstro.bySolar(
                solarDate = it.solarDate,
                timeIndex = it.timeIndex,
                gender = it.gender,
                fixLeap = it.fixLeap,
            )
        }
    }

    BackHandler(enabled = screen != AppScreen.Home) {
        screenName = AppScreen.Home.name
    }

    when (screen) {
        AppScreen.Home -> HomeScreen(
            onNewChart = { screenName = AppScreen.Create.name },
            onLicenses = { screenName = AppScreen.Licenses.name },
        )

        AppScreen.Create -> CreateChartScreen(
            initialProfile = profile,
            onBack = { screenName = AppScreen.Home.name },
            onGenerate = {
                savedDate = it.solarDate
                savedTimeIndex = it.timeIndex
                savedGender = it.gender
                savedFixLeap = it.fixLeap
                screenName = AppScreen.Chart.name
            },
        )

        AppScreen.Chart -> {
            if (profile != null && chart != null) {
                ChartScreen(
                    profile = profile,
                    chart = chart,
                    onBack = { screenName = AppScreen.Home.name },
                    onEdit = { screenName = AppScreen.Create.name },
                )
            } else {
                screenName = AppScreen.Home.name
            }
        }

        AppScreen.Licenses -> OpenSourceScreen(
            onBack = { screenName = AppScreen.Home.name },
        )
    }
}
