package com.xuanxue.app

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
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
import com.xuanxue.liuren.LiuRenEngine
import com.xuanxue.liuren.LiuRenEngine.LiuRenChart
import java.util.Calendar

/** 大六壬排盘页（袁树珊《大六壬探原》体系） */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LiuRenScreen() {
    var year by remember { mutableStateOf(2026) }
    var month by remember { mutableStateOf(8) }
    var day by remember { mutableStateOf(15) }
    var hour by remember { mutableStateOf(10) }
    var night by remember { mutableStateOf(false) }
    var showDatePicker by remember { mutableStateOf(false) }
    var chart by remember { mutableStateOf<LiuRenChart?>(null) }

    Column(
        Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text("大六壬（袁树珊《大六壬探原》体系）", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))

        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("公历: $year-$month-$day  $hour:00", Modifier.weight(1f))
                    Button(onClick = { showDatePicker = true }) { Text("选日期") }
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text("时辰:", Modifier.align(Alignment.CenterVertically))
                    listOf(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22).forEach { h ->
                        TextButton(onClick = { hour = h }) {
                            Text("${h / 2 + 1}时", color = if (hour == h) Color(0xFF1E88E5) else Color.Gray, fontSize = 12.sp)
                        }
                    }
                }
                Row {
                    TextButton(onClick = { night = false }) {
                        Text("昼占", color = if (!night) Color(0xFF1E88E5) else Color.Gray, fontWeight = if (!night) FontWeight.Bold else FontWeight.Normal)
                    }
                    TextButton(onClick = { night = true }) {
                        Text("夜占", color = if (night) Color(0xFF1E88E5) else Color.Gray, fontWeight = if (night) FontWeight.Bold else FontWeight.Normal)
                    }
                }
                Button(onClick = { chart = LiuRenEngine.bySolar(year, month, day, hour, 0, night) }, modifier = Modifier.fillMaxWidth()) {
                    Text("起课")
                }
            }
        }

        chart?.let { c ->
            Spacer(Modifier.height(16.dp))
            LiuRenResult(c)
            ReadingCard(com.xuanxue.ai.XuanxueAI.liuren(c))
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
fun LiuRenResult(c: LiuRenChart) {
    Column {
        OutlinedCard(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Text("农历: ${c.lunarDateStr}", fontSize = 14.sp)
                Text("四柱: ${c.yearGZ} ${c.monthGZ} ${c.dayGZ} ${c.hourGZ}", fontSize = 14.sp)
                Text("月将: ${c.yueJiang}（日干寄宫: ${c.ganJi}）  贵人: ${c.guiRen}  旬空: ${c.xunKong.joinToString("")}", fontSize = 14.sp)
                Text("三传: ${c.sanChuan.chu} → ${c.sanChuan.zhong} → ${c.sanChuan.mo}", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E88E5))
                Text("取法: ${c.sanChuan.fa}", fontSize = 13.sp, color = Color(0xFFE65100))
            }
        }

        Spacer(Modifier.height(12.dp))
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            // 四课
            OutlinedCard(Modifier.weight(1f)) {
                Column(Modifier.padding(10.dp)) {
                    Text("四课", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    c.siKe.forEachIndexed { i, k ->
                        Row(Modifier.padding(vertical = 2.dp)) {
                            Text("课${i + 1}", Modifier.width(36.dp), fontSize = 12.sp, color = Color.Gray)
                            Text("${k.zhi}(${k.dunGan})", fontSize = 14.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
            // 天盘
            OutlinedCard(Modifier.weight(1f)) {
                Column(Modifier.padding(10.dp)) {
                    Text("天地盘", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    LiuRenEngine.ZHI.forEachIndexed { i, z ->
                        Row(Modifier.padding(vertical = 1.dp)) {
                            Text("$z", Modifier.width(20.dp), fontSize = 12.sp, color = Color.Gray)
                            Text("${c.tianPan[i]}", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = if (c.tianPan[i] == c.yueJiang) Color(0xFF1E88E5) else Color.Unspecified)
                        }
                    }
                }
            }
        }
        Spacer(Modifier.height(8.dp))
        Text("注：天盘月将${c.yueJiang}加时（蓝色标注）。三传为初传→中传→末传。", fontSize = 11.sp, color = Color.Gray)
    }
}
