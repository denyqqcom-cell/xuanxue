package com.xuanxue.app

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.xuanxue.app.ui.qimen.QimenAiScreen
import com.xuanxue.app.ui.qimen.QimenCastScreen
import com.xuanxue.qimen.core.api.QimenChart

private enum class QimenRoute {
    HOME,
    CAST,
    AI,
}

/**
 * 旧首页与后续 UI/UX v2 之间的薄入口层。
 * 奇门先明确起局时间并生成同一张 QimenChart，再把它交给 AI 解盘页。
 */
@Composable
fun XuanxueRoot() {
    var route by remember { mutableStateOf(QimenRoute.HOME) }
    var selectedQimenChart by remember { mutableStateOf<QimenChart?>(null) }

    BackHandler(enabled = route != QimenRoute.HOME) {
        route = when (route) {
            QimenRoute.AI -> QimenRoute.CAST
            QimenRoute.CAST -> QimenRoute.HOME
            QimenRoute.HOME -> QimenRoute.HOME
        }
    }

    when (route) {
        QimenRoute.CAST -> {
            QimenCastScreen(
                onBack = { route = QimenRoute.HOME },
                onOpenAi = { chart ->
                    selectedQimenChart = chart
                    route = QimenRoute.AI
                },
            )
            return
        }

        QimenRoute.AI -> {
            val chart = selectedQimenChart
            if (chart == null) {
                route = QimenRoute.CAST
            } else {
                QimenAiScreen(
                    chart = chart,
                    onBack = { route = QimenRoute.CAST },
                )
                return
            }
        }

        QimenRoute.HOME -> Unit
    }

    Box(Modifier.fillMaxSize()) {
        XuanxueApp()
        ExtendedFloatingActionButton(
            onClick = {
                selectedQimenChart = null
                route = QimenRoute.CAST
            },
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp),
        ) {
            Text("奇门起局 / AI")
        }
    }
}
