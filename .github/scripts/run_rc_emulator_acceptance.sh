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

  echo "=== ${form_factor^^} / ${theme^^} ==="
  adb shell wm size "$size"
  adb shell wm density "$density"
  adb shell cmd uimode night "$night"
  adb shell am force-stop com.xuanxue.app.rc 2>/dev/null || true

  ./gradlew --no-daemon :app:connectedDebugAndroidTest \
    -Pandroid.testInstrumentationRunnerArguments.class=com.xuanxue.app.RcDeviceAcceptanceTest \
    -Pandroid.testInstrumentationRunnerArguments.formFactor="$form_factor"

  adb pull /sdcard/Android/data/com.xuanxue.app.rc/files/rc-screenshots "$out/screenshots" || true
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
    adb shell wm size
    adb shell wm density
  } > "$out/ENVIRONMENT.txt"
}

run_profile narrow light 1080x1920 420 no
run_profile wide dark 1600x1200 240 yes

adb shell pm path com.xuanxue.app.rc > build/rc-device-acceptance/PACKAGE_PATH.txt
if adb shell dumpsys package com.xuanxue.app.rc | grep -Fq 'android.permission.INTERNET'; then
  echo 'Runtime package unexpectedly declares android.permission.INTERNET' >&2
  exit 1
fi
{
  echo "internet_permission=absent"
  echo "airplane_mode=$(adb shell settings get global airplane_mode_on | tr -d '\r')"
  echo "source_head_sha=${SOURCE_HEAD_SHA}"
} > build/rc-device-acceptance/RUNTIME_SECURITY.txt
