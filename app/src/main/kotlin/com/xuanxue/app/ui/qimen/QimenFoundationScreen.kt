package com.xuanxue.app.ui.qimen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.xuanxue.app.ui.components.ScreenTopBar
import com.xuanxue.qimen.core.api.QimenChart
import com.xuanxue.qimen.core.api.QimenEngine
import com.xuanxue.qimen.core.api.QimenRequest
import com.xuanxue.qimen.core.calendar.Dun
import com.xuanxue.qimen.core.relations.WuBuYu
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter

@Composable
fun QimenFoundationScreen(onBack: () -> Unit) {
    val zone = remember { ZoneId.of("Asia/Shanghai") }
    val initial = remember { LocalDateTime.now(zone).withNano(0) }
    var dateText by rememberSaveable { mutableStateOf(initial.toLocalDate().toString()) }
    var timeText by rememberSaveable {
        mutableStateOf(initial.toLocalTime().format(DateTimeFormatter.ofPattern("HH:mm:ss")))
    }
    var chart by remember { mutableStateOf<QimenChart?>(null) }
    var errorText by remember { mutableStateOf<String?>(null) }

    Column(modifier = Modifier.fillMaxSize()) {
        ScreenTopBar(
            title = "奇门遁甲",
            subtitle = "基础起局 · 尚未开放完整九宫",
            onBack = onBack,
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 18.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Surface(
                color = MaterialTheme.colorScheme.primaryContainer,
                shape = MaterialTheme.shapes.large,
            ) {
                Column(
                    modifier = Modifier.padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(7.dp),
                ) {
                    Text("先把能证明的部分做对。", style = MaterialTheme.typography.headlineSmall)
                    Text(
                        "当前核心只计算精确节气边界、日时干支、旬首旬空、阴阳遁与拆补日数局。地盘走法尚未取得完整九宫黄金夹具，所以这里不会画一张看似完整但来源不稳的盘。",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer,
                    )
                }
            }

            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    Text("起局时间", style = MaterialTheme.typography.titleMedium)
                    OutlinedTextField(
                        value = dateText,
                        onValueChange = { dateText = it },
                        label = { Text("日期 YYYY-MM-DD") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                    )
                    OutlinedTextField(
                        value = timeText,
                        onValueChange = { timeText = it },
                        label = { Text("时间 HH:mm 或 HH:mm:ss") },
                        supportingText = { Text("当前 v1 固定按 Asia/Shanghai；23:00–23:59 默认晚子滚次日。") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                    )
                    Button(
                        onClick = {
                            val result = runCatching {
                                val date = LocalDate.parse(dateText.trim())
                                val rawTime = timeText.trim()
                                val time = if (rawTime.length == 5) {
                                    LocalTime.parse(rawTime, DateTimeFormatter.ofPattern("HH:mm"))
                                } else {
                                    LocalTime.parse(rawTime, DateTimeFormatter.ofPattern("HH:mm:ss"))
                                }
                                val epochMs = LocalDateTime.of(date, time).atZone(zone).toInstant().toEpochMilli()
                                QimenEngine.cast(QimenRequest(epochMs)).getOrThrow()
                            }
                            chart = result.getOrNull()
                            errorText = result.exceptionOrNull()?.message
                        },
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        Text("计算基础局")
                    }
                    if (errorText != null) {
                        Text(
                            errorText.orEmpty(),
                            color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodySmall,
                        )
                    }
                }
            }

            chart?.let { QimenFoundationResult(it) }

            OutlinedCard(Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(7.dp),
                ) {
                    Text("当前算法边界", style = MaterialTheme.typography.titleMedium)
                    Text(
                        "置闰、拆补符头、茅山、飞宫、真太阳时均为 UnsupportedSchool。完整地盘、天盘、人盘、神盘仍锁定；十干克应与断语也没有进入 qimen-core。",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

@Composable
private fun QimenFoundationResult(chart: QimenChart) {
    val dunLabel = if (chart.dun == Dun.YANG) "阳遁" else "阴遁"
    val xunKong = chart.xunKong.joinToString("、") { it.symbol }
    val wuBuYu = WuBuYu.isWuBuYu(chart.dayPillar.stem, chart.hourPillar)

    OutlinedCard(Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text("基础局结果", style = MaterialTheme.typography.titleLarge)
                Text(
                    "$dunLabel${chart.ju}局",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                )
            }
            Text("${chart.jieqi} · 第 ${chart.jieqiDayIndex} 日 · ${chart.yuan.label}元 · ${chart.juMethodUsed.name}")
            Text("日柱 ${chart.dayPillar.text}　时柱 ${chart.hourPillar.text}")
            Text("旬首 ${chart.xunShou.text}　遁仪 ${chart.dunYi.symbol}　旬空 $xunKong")
            Text(
                if (wuBuYu) "五不遇时：是（generator 规则）" else "五不遇时：否（generator 规则）",
                color = if (wuBuYu) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface,
            )

            Surface(
                color = MaterialTheme.colorScheme.surfaceVariant,
                shape = MaterialTheme.shapes.medium,
            ) {
                Column(
                    modifier = Modifier.padding(13.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp),
                ) {
                    Text("九宫未绘制", style = MaterialTheme.typography.titleSmall)
                    Text(
                        "earth = null。地盘算法未解锁；等地盘走法冲突关闭并取得完整九宫夹具后再开放。",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}
