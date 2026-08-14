package com.xuanxue.app.ui.chart

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.DatePicker
import androidx.compose.material3.DatePickerDialog
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Switch
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
import androidx.compose.ui.unit.dp
import com.xuanxue.app.ui.components.ScreenTopBar
import com.xuanxue.app.ui.components.SectionTitle
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateChartScreen(
    initialProfile: BirthProfile?,
    onBack: () -> Unit,
    onGenerate: (BirthProfile) -> Unit,
) {
    var solarDate by remember(initialProfile) { mutableStateOf(initialProfile?.solarDate) }
    var timeIndex by remember(initialProfile) { mutableStateOf(initialProfile?.timeIndex ?: 6) }
    var gender by remember(initialProfile) { mutableStateOf(initialProfile?.gender ?: "male") }
    var fixLeap by remember(initialProfile) { mutableStateOf(initialProfile?.fixLeap ?: false) }
    var showDatePicker by remember { mutableStateOf(false) }
    var showAdvanced by remember { mutableStateOf(false) }
    var timeExpanded by remember { mutableStateOf(false) }

    val datePickerState = rememberDatePickerState(
        initialSelectedDateMillis = initialProfile?.solarDate?.let(::millisOfUtc),
    )

    Column(Modifier.fillMaxSize()) {
        ScreenTopBar(
            title = if (initialProfile == null) "新建命盘" else "编辑命盘",
            subtitle = "紫微斗数 · 本地计算",
            onBack = onBack,
        )
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 18.dp, vertical = 10.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            SectionTitle("出生资料", "只保留排盘真正需要的信息")

            OutlinedCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { showDatePicker = true },
            ) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text("公历出生日期", style = MaterialTheme.typography.labelLarge)
                    Text(
                        solarDate ?: "请选择日期",
                        style = MaterialTheme.typography.titleLarge,
                        color = if (solarDate == null) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurface,
                    )
                }
            }

            Column(verticalArrangement = Arrangement.spacedBy(7.dp)) {
                Text("出生时辰", style = MaterialTheme.typography.labelLarge)
                Box(Modifier.fillMaxWidth()) {
                    OutlinedButton(
                        onClick = { timeExpanded = true },
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        Text(SHICHEN_LABELS[timeIndex])
                    }
                    DropdownMenu(
                        expanded = timeExpanded,
                        onDismissRequest = { timeExpanded = false },
                    ) {
                        SHICHEN_LABELS.forEachIndexed { index, label ->
                            DropdownMenuItem(
                                text = { Text(label) },
                                onClick = {
                                    timeIndex = index
                                    timeExpanded = false
                                },
                            )
                        }
                    }
                }
            }

            Column(verticalArrangement = Arrangement.spacedBy(7.dp)) {
                Text("性别", style = MaterialTheme.typography.labelLarge)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(
                        selected = gender == "male",
                        onClick = { gender = "male" },
                        label = { Text("男") },
                    )
                    FilterChip(
                        selected = gender == "female",
                        onClick = { gender = "female" },
                        label = { Text("女") },
                    )
                }
            }

            HorizontalDivider()
            TextButton(onClick = { showAdvanced = !showAdvanced }) {
                Text(if (showAdvanced) "收起高级排盘设置" else "高级排盘设置")
            }

            if (showAdvanced) {
                OutlinedCard(Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Column(
                            modifier = Modifier.weight(1f),
                            verticalArrangement = Arrangement.spacedBy(3.dp),
                        ) {
                            Text("闰月修正", style = MaterialTheme.typography.titleMedium)
                            Text(
                                "仅在你明确需要按闰月规则修正时开启。",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                        Switch(checked = fixLeap, onCheckedChange = { fixLeap = it })
                    }
                }
            }

            Spacer(Modifier.height(4.dp))
            Button(
                onClick = {
                    solarDate?.let {
                        onGenerate(
                            BirthProfile(
                                solarDate = it,
                                timeIndex = timeIndex,
                                gender = gender,
                                fixLeap = fixLeap,
                            ),
                        )
                    }
                },
                enabled = solarDate != null,
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text("生成命盘")
            }
            Text(
                "出生资料只用于本机排盘，本版本没有网络权限。",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }

    if (showDatePicker) {
        DatePickerDialog(
            onDismissRequest = { showDatePicker = false },
            confirmButton = {
                TextButton(
                    onClick = {
                        datePickerState.selectedDateMillis?.let { solarDate = formatUtc(it) }
                        showDatePicker = false
                    },
                ) { Text("确定") }
            },
            dismissButton = {
                TextButton(onClick = { showDatePicker = false }) { Text("取消") }
            },
        ) {
            DatePicker(state = datePickerState)
        }
    }
}

private val utc: TimeZone = TimeZone.getTimeZone("UTC")

private fun formatUtc(millis: Long): String =
    SimpleDateFormat("yyyy-MM-dd", Locale.ROOT).apply { timeZone = utc }.format(Date(millis))

private fun millisOfUtc(date: String): Long? =
    runCatching {
        SimpleDateFormat("yyyy-MM-dd", Locale.ROOT).apply {
            timeZone = utc
            isLenient = false
        }.parse(date)?.time
    }.getOrNull()
