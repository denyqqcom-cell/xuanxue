package com.xuanxue.app

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.DatePicker
import androidx.compose.material3.DatePickerDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberDatePickerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.xuanxue.qimen.QimenEngine
import com.xuanxue.qimen.QimenEngine.QimenChart
import java.util.Calendar

/** 奇门遁甲排盘页（转盘时家奇门，纯净版） */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QimenScreen() {
    var year by remember { mutableStateOf(2026) }
    var month by remember { mutableStateOf(8) }
    var day by remember { mutableStateOf(12) }
    var hour by remember { mutableStateOf(15) }
    var minute by remember { mutableStateOf(37) }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<QimenChart?>(null) }

    Column(
        Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text("奇门遁甲（转盘时家）", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("公历: $year-$month-$day  $hour:${"%02d".format(minute)}", Modifier.weight(1f))
                    Button(onClick = { showDatePicker = true }) { Text("选日期") }
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text("时辰:", Modifier.align(Alignment.CenterVertically))
                    listOf(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22).forEach { h ->
                        TextButton(onClick = { hour = h; minute = 30 }) {
                            Text("${h / 2 + 1}时", color = if (hour == h) Color(0xFF1E88E5) else Color.Gray, fontSize = 12.sp)
                        }
                    }
                }
                Spacer(Modifier.height(8.dp))
                Button(onClick = { chart = QimenEngine.bySolar(year, month, day, hour, minute) }, modifier = Modifier.fillMaxWidth()) {
                    Text("起局")
                }
            }
        }

        chart?.let { c ->
            Spacer(Modifier.height(16.dp))
            QimenResult(c)
            ReadingCard(com.xuanxue.ai.XuanxueAI.qimen(c))
        }
    }

    if (showDatePicker) {
        val today = Calendar.getInstance()
        val state = rememberDatePickerState(initialSelectedDateMillis = runCatching {
            java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse("$year-$month-$day")!!.time
        }.getOrDefault(System.currentTimeMillis()).coerceIn(
            java.text.SimpleDateFormat("yyyy", java.util.Locale.US).parse("1900")!!.time, today.timeInMillis
        ))
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(onClick = {
                    state.selectedDateMillis?.let { ms ->
                        val cal = Calendar.getInstance().apply { timeInMillis = ms }
                        year = cal.get(Calendar.YEAR); month = cal.get(Calendar.MONTH) + 1; day = cal.get(Calendar.DAY_OF_MONTH)
                    }
                    showDatePicker = false
                }) { Text("确定") }
            },
            dismissButton = { TextButton(onClick = { showDatePicker = false }) { Text("取消") } }
        ) { DatePicker(state = state) }
    }
}

@Composable
fun QimenResult(c: QimenChart) {
    Column {
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Text("农历: ${c.lunarDateStr}", fontSize = 14.sp)
                Text("四柱: ${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}", fontSize = 14.sp)
                Text("节气: ${c.jieQi}", fontSize = 14.sp)
                Text("局: ${c.juText}", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E88E5))
                Text(
                    "定元法: ${c.juMethod}（拆补日数分段为默认，符头/置闰可切换——流派冲突，见方法核验中心）",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                if (c.isWuBuYu) {
                    Text("五不遇时（时干克日干）", fontSize = 13.sp, color = MaterialTheme.colorScheme.error)
                }
                if (c.patterns.isNotEmpty()) {
                    Text("格局: ${c.patterns.joinToString("、")}", fontSize = 13.sp, color = MaterialTheme.colorScheme.error)
                }
                Text(
                    "值符/值使与九宫来自转盘引擎（物理环序旋转，天禽寄坤2）。完整九宫黄金夹具仍在建设中。",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.error,
                )
                Text("值符: ${c.zhiFu}   值使: ${c.zhiShi}   旬首: ${c.xunShou}遁${c.dunGan}", fontSize = 14.sp)
                Text("旬空: ${c.xunKong.joinToString("")}   马星: ${c.maXing}", fontSize = 14.sp)
            }
        }

        // 洛书九宫盘面（上 4 9 2 / 中 3 5 7 / 下 8 1 6）
        Spacer(Modifier.height(12.dp))
        val layout = listOf(listOf(4, 9, 2), listOf(3, 5, 7), listOf(8, 1, 6))
        val byPalace = c.gongs.associateBy { it.palace }
        layout.forEach { row ->
            Row(Modifier.fillMaxWidth()) {
                row.forEach { p ->
                    val g = byPalace[p]
                    Box(
                        Modifier
                            .weight(1f)
                            .padding(2.dp)
                            .aspectRatio(1f)
                            .border(1.dp, Color(0xFF90A4AE), MaterialTheme.shapes.small)
                            .background(if (g?.isMaXing == true) Color(0xFFFFF3E0) else if (g?.isKong == true) Color(0xFFECEFF1) else Color.White)
                            .padding(4.dp)
                    ) {
                        Column {
                            Row {
                                Text("$p", fontSize = 10.sp, color = Color.Gray)
                                Spacer(Modifier.weight(1f))
                                if (g?.isMaXing == true) Text("马", fontSize = 10.sp, color = Color(0xFFEF6C00))
                                if (g?.isKong == true) Text("空", fontSize = 10.sp, color = Color(0xFF90A4AE))
                            }
                            g?.diGan?.let { Text(it, fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E88E5), textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth()) }
                            g?.tianXing?.let { Text(it, fontSize = 11.sp, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth()) }
                            g?.renMen?.let { Text(it, fontSize = 11.sp, color = Color(0xFF2E7D32), textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth()) }
                            g?.shenPan?.let { Text(it, fontSize = 10.sp, color = Color(0xFF6D4C41), textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth()) }
                        }
                    }
                }
            }
        }
        Spacer(Modifier.height(8.dp))
        Text("注：地=地盘三奇六仪，星=天盘九星，门=人盘八门，神=神盘八神；中宫无门神。", fontSize = 11.sp, color = Color.Gray)
    }
}
