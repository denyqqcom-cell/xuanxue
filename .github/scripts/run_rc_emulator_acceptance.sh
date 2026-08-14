#!/usr/bin/env bash
set -euo pipefail

mkdir -p build/rc-device-acceptance/narrow build/rc-device-acceptance/wide

adb shell cmd connectivity airplane-mode enable || {
  adb shell settings put global airplane_mode_on 1
  adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true
}
airplane="$(adb shell settings get global airplane_mode_on | tr -d '\r')"
test "$airplane" = "1"

run_profile() {
  local form_factor="$1"
  local theme="$2"
  local size="$3"
  local density="$4"
  local night="$5"
  local out="build/rc-device-acceptance/${form_factor}"
  local remote_screens="/sdcard/Download/xuanxue-rc-screenshots"

  echo "=== ${form_factor^^} / ${theme^^} ==="
  adb shell wm size "$size"
  adb shell wm density "$density"
  adb shell cmd uimode night "$night"
  adb shell rm -rf "$remote_screens"
  adb shell mkdir -p "$remote_screens"
  adb shell am force-stop com.xuanxue.app.rc 2>/dev/null || true

  ./gradlew --no-daemon :app:connectedDebugAndroidTest \
    -Pandroid.testInstrumentationRunnerArguments.class=com.xuanxue.app.RcDeviceAcceptanceTest \
    -Pandroid.testInstrumentationRunnerArguments.formFactor="$form_factor"

  local screenshot_count
  screenshot_count="$(adb shell "find '$remote_screens' -maxdepth 1 -type f -name '*.png' | wc -l" | tr -d '\r[:space:]')"
  if [[ "$screenshot_count" -lt 10 ]]; then
    echo "Expected at least 10 acceptance screenshots for $form_factor, found $screenshot_count" >&2
    adb shell "find '$remote_screens' -maxdepth 1 -type f -print" >&2 || true
    exit 1
  fi
  rm -rf "$out/screenshots"
  adb pull "$remote_screens" "$out/screenshots"

  rm -rf "$out/test-results" "$out/html-report"
  if [[ -d app/build/outputs/androidTest-results/connected ]]; then
    cp -R app/build/outputs/androidTest-results/connected "$out/test-results"
  fi
  if [[ -d app/build/reports/androidTests/connected ]]; then
    cp -R app/build/reports/androidTests/connected "$out/html-report"
  fi

  {
    echo "source_head_sha=${SOURCE_HEAD_SHA}"
    echo "form_factor=${form_factor}"
    echo "theme=${theme}"
    echo "airplane_mode=$(adb shell settings get global airplane_mode_on | tr -d '\r')"
    echo "acceptance_screenshots=${screenshot_count}"
    adb shell wm size
    adb shell wm density
  } > "$out/ENVIRONMENT.txt"
}

run_profile narrow light 1080x1920 420 no
run_profile wide dark 1600x1200 240 yes

# connectedDebugAndroidTest may uninstall the target package during cleanup.
# Reinstall the exact debug APK built from this source head before runtime checks.
test -s app/build/outputs/apk/debug/app-debug.apk
adb install -r app/build/outputs/apk/debug/app-debug.apk >/dev/null
adb shell pm path com.xuanxue.app.rc > build/rc-device-acceptance/PACKAGE_PATH.txt
grep -Fq 'package:' build/rc-device-acceptance/PACKAGE_PATH.txt

package_dump="$(adb shell dumpsys package com.xuanxue.app.rc)"
if grep -Fq 'android.permission.INTERNET' <<<"$package_dump"; then
  echo 'Runtime package unexpectedly declares android.permission.INTERNET' >&2
  exit 1
fi
if ! grep -Fq 'versionName=1.0.0-rc1-debug' <<<"$package_dump"; then
  echo 'Installed acceptance package is not the expected RC1 debug version.' >&2
  exit 1
fi

final_airplane="$(adb shell settings get global airplane_mode_on | tr -d '\r')"
test "$final_airplane" = "1"
{
  echo "internet_permission=absent"
  echo "airplane_mode=${final_airplane}"
  echo "package=com.xuanxue.app.rc"
  echo "version_name=1.0.0-rc1-debug"
  echo "source_head_sha=${SOURCE_HEAD_SHA}"
} > build/rc-device-acceptance/RUNTIME_SECURITY.txt
