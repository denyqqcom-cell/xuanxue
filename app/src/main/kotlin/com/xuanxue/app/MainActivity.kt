package com.xuanxue.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.xuanxue.app.ui.XuanxueApp
import com.xuanxue.app.ui.theme.XuanxueTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            XuanxueTheme {
                XuanxueApp()
            }
        }
    }
}
