# Android 真机验收清单

本清单用于 `app-integration-v3` 的人工触控与视觉验收。它不替代核心算法 fixture、Android Lint、APK 内容审计，也不把“界面正常”视为术数规则已被验证。

## 自动化真机 smoke runner

仓库提供 `.github/scripts/run_physical_device_acceptance.sh`，用于在**唯一一台已授权的真实 Android 设备**上运行现有 `RcDeviceAcceptanceTest` 的窄屏路径。

它与 emulator runner 有意不同：

- 必须只有一个 ADB target，且 `state=device`；
- `ro.kernel.qemu=1` 时直接拒绝，不能把模拟器冒充真机；
- 可通过 `EXPECTED_MODEL` 绑定预期型号，例如 Moto X30 Pro 使用 `XT2241-1`；
- `SOURCE_HEAD_SHA` 必须与本地实际 `git rev-parse HEAD` 完全一致，否则拒绝生成可能被错误标记的真机证据；
- tracked worktree 与 index 必须干净；未跟踪文件不会被 runner 自动删除，也不会被冒充成 tracked clean/dirty 结论；
- ADB 默认从 `PATH` 使用 `adb`；若 WSL 中没有 `adb`，可通过 `ADB_BIN` 显式指向已授权且可执行的现有 ADB，例如 Windows `adb.exe` 在 WSL 中对应的 `/mnt/c/.../adb.exe` 路径；
- 只运行 `formFactor=narrow`；
- **不修改** `wm size`、`wm density`、深浅色模式、飞行模式或网络状态；
- 测试前后会重新读取这些系统状态，发生漂移即 fail closed；
- 记录 source HEAD、实际 checkout HEAD、ADB 版本、设备型号、Android/API、APK SHA256、截图数量和 logcat 尾部；
- 至少应取得 16 张现有 instrumentation evidence screenshot。

在仓库根目录执行示例：

```bash
SOURCE_HEAD_SHA="$(git rev-parse HEAD)" \
EXPECTED_MODEL="XT2241-1" \
bash .github/scripts/run_physical_device_acceptance.sh
```

如果当前 WSL 没有 `adb`，但 Windows 已有与这台真机连接成功的 `adb.exe`，可显式传入其 WSL 可执行路径，而不是另装一套 platform-tools：

```bash
ADB_BIN="/mnt/c/path/to/platform-tools/adb.exe" \
SOURCE_HEAD_SHA="$(git rev-parse HEAD)" \
EXPECTED_MODEL="XT2241-1" \
bash .github/scripts/run_physical_device_acceptance.sh
```

输出位于：

```text
build/physical-device-acceptance/
```

其中 `RESULT.txt` 只有在 source HEAD 与实际 checkout HEAD 一致、tracked worktree/index 干净、instrumentation 完成、截图数量达标、且测试前后系统状态未发生变化时才写入 `status=PASS`。

这条自动化只关闭窄屏真机 smoke / navigation / structural-result / crash-ANR evidence；深色模式、飞行模式、人体工学与完整人工视觉检查仍按下面清单单独验收。真机 PASS 也不等于任何术数预测获得 empirical credit。

## 建议至少覆盖

- 一台窄屏手机：检查单列布局、横向时辰选择、长文本换行。
- 一台较宽手机或平板：检查首页双列模块、大六壬双栏结构。
- 系统浅色与深色模式各一次。
- 飞行模式一次：当前版本不依赖网络，所有排盘与离线解释应继续可用。

## 必验路径

### 首页 / 导航

- 首页六个模块均可进入：紫微、八字、奇门、六爻、大六壬、黄历。
- “方法核验中心”与“开源许可”可进入并可返回。
- Android 系统返回键从模块页回首页，不出现死页或退出异常。
- 窄屏为单列模块卡；约 720dp 以上为双列；内容宽度不过度拉伸。

### 紫微斗数

- 日期、13 个时辰、性别与闰月修正均可操作。
- 13 个时辰可横向滚动。
- 排盘后默认选中命宫。
- 点击十二宫任一宫位，选中边框/背景发生变化，下面详情同步切换。
- 九宫格只保留宫名、干支、主星、大限等摘要；辅星/杂曜在详情层查看，不再形成整屏信息墙。
- “命宫干支”字段没有被误写成整盘四柱干支。

### 八字

- 时辰快捷项显示为独立的 `00:30`、`02:30` … `22:30`，不能全部重复成同一时间。
- 四柱、藏干、十神、纳音、大运可正常显示。
- 离线解释不得恢复“只凭十二运直接判身强弱/喜忌”的旧文案。

### 奇门遁甲

- 首次进入时日期与时间来自设备当前时钟，不是写死的测试日期。
- 实验九宫警示必须清楚可见。
- 未填写具体事体时，解释卡只能展示结构与边界，不自动输出成败、吉凶或应期。
- 填写具体问题后，用户输入必须标为“事体上下文”，不能伪装成来源证据。
- 九宫当前仍明确标记为实验实现。

### 六爻

- 首次进入时日期与小时来自设备当前时钟。
- 时间起卦与数字起卦可切换。
- 窄屏数字输入框纵向排列；宽屏可横向排列。
- 世、应、动爻标记清晰可辨。
- 未提供事体时不自动替用户选唯一用神。

### 大六壬

- 首次进入时日期与小时来自设备当前时钟。
- 昼占 / 夜占可切换。
- 窄屏时“四课”和“天地盘”上下排列；宽屏时左右并列。
- 三传、取法、旬空等结构字段不被直接翻译成确定现实吉凶。
- 未提供具体事体时不自动进入类神、应事、应期判断。

### 黄历 / 合规

- 飞行模式下黄历仍可打开并显示本地计算字段。
- 开源许可页可读取随 APK 打包的 notices。
- App 不出现登录、广告、支付、推送或网络权限请求。

## 失败即阻止合并的项目

- source HEAD 与实际 checkout HEAD 不一致，或 tracked worktree/index 存在改动。
- 崩溃、ANR、无法返回首页。
- 文字重叠、关键按钮被裁切或无法触控。
- 当前时间类模块仍显示写死日期/小时。
- 奇门实验九宫被表现成“已核验标准盘”。
- 没有具体事体时仍自动输出用神、成败、应期。
- APK 出现研究目录、扫描件、OCR 全文、外部字体或未经版权审查的资产。
- 开源许可文件缺失。

## 回报格式

```text
设备 / Android：
屏幕尺寸或分辨率：
浅色 / 深色：
测试 commit：
测试 APK SHA256：

首页：PASS / FAIL
紫微：PASS / FAIL
八字：PASS / FAIL
奇门：PASS / FAIL
六爻：PASS / FAIL
大六壬：PASS / FAIL
黄历：PASS / FAIL
许可与离线：PASS / FAIL

问题：
1.
2.
截图：
```

只有核心测试、Lint、APK 内容审计与本清单关键路径都通过，才适合把 PR 从 Draft 推向合并审查。
