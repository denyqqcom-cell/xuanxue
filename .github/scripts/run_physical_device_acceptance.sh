#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

OUT="build/physical-device-acceptance"
REMOTE_SCREENS="/sdcard/Download/xuanxue-v1-screenshots"
mkdir -p "$OUT"

ACTUAL_HEAD_SHA="$(git rev-parse HEAD)"
SOURCE_HEAD_SHA="${SOURCE_HEAD_SHA:-$ACTUAL_HEAD_SHA}"
export SOURCE_HEAD_SHA

if [[ "$ACTUAL_HEAD_SHA" != "$SOURCE_HEAD_SHA" ]]; then
  echo "Source HEAD mismatch: expected=$SOURCE_HEAD_SHA actual=$ACTUAL_HEAD_SHA. Refusing mislabeled physical-device evidence." >&2
  exit 1
fi
if ! git diff --quiet -- || ! git diff --cached --quiet --; then
  echo "Physical-device acceptance requires a clean tracked worktree and index." >&2
  git status --short --untracked-files=no >&2 || true
  exit 1
fi

# Default to adb from PATH, but allow an already-authorized bridge such as a
# Windows platform-tools adb.exe exposed inside WSL via an explicit path.
ADB_BIN="${ADB_BIN:-adb}"
if [[ "$ADB_BIN" == */* ]]; then
  if [[ ! -x "$ADB_BIN" ]]; then
    echo "Configured ADB_BIN is not executable: $ADB_BIN" >&2
    exit 1
  fi
elif ! command -v "$ADB_BIN" >/dev/null 2>&1; then
  echo "ADB executable not found in PATH: $ADB_BIN" >&2
  exit 1
fi
ADB_BASE=("$ADB_BIN")
ADB_VERSION="$("${ADB_BASE[@]}" version | sed -n '1p' | tr -d '\r')"

# GRADLE_CONNECTED remains the default. ADB_DIRECT is an explicit physical-only
# transport for environments such as WSL where DDMLib cannot see the Windows
# USB namespace even though the selected ADB_BIN can reach the authorized phone.
INSTRUMENTATION_MODE="${INSTRUMENTATION_MODE:-GRADLE_CONNECTED}"
case "$INSTRUMENTATION_MODE" in
  GRADLE_CONNECTED|ADB_DIRECT) ;;
  *)
    echo "Unsupported INSTRUMENTATION_MODE: $INSTRUMENTATION_MODE" >&2
    exit 1
    ;;
esac

# Windows adb.exe may emit CRLF when invoked through WSL. Normalize the device
# list before parsing so a ready state cannot become the literal "device\r".
mapfile -t DEVICE_ROWS < <("${ADB_BASE[@]}" devices | tr -d '\r' | awk 'NR > 1 && NF >= 2 {print $1 "\t" $2}')
if [[ "${#DEVICE_ROWS[@]}" -ne 1 ]]; then
  echo "Physical-device acceptance requires exactly one ADB target; found ${#DEVICE_ROWS[@]}." >&2
  "${ADB_BASE[@]}" devices -l >&2 || true
  exit 1
fi

SERIAL="${DEVICE_ROWS[0]%%$'\t'*}"
STATE="${DEVICE_ROWS[0]#*$'\t'}"
if [[ "$STATE" != "device" ]]; then
  echo "ADB target $SERIAL is not ready: state=$STATE" >&2
  "${ADB_BASE[@]}" devices -l >&2 || true
  exit 1
fi
ADB=("${ADB_BASE[@]}" -s "$SERIAL")

BOOT_COMPLETED="$("${ADB[@]}" shell getprop sys.boot_completed | tr -d '\r')"
MODEL="$("${ADB[@]}" shell getprop ro.product.model | tr -d '\r')"
DEVICE="$("${ADB[@]}" shell getprop ro.product.device | tr -d '\r')"
MANUFACTURER="$("${ADB[@]}" shell getprop ro.product.manufacturer | tr -d '\r')"
ANDROID_RELEASE="$("${ADB[@]}" shell getprop ro.build.version.release | tr -d '\r')"
ANDROID_SDK="$("${ADB[@]}" shell getprop ro.build.version.sdk | tr -d '\r')"
QEMU="$("${ADB[@]}" shell getprop ro.kernel.qemu | tr -d '\r')"

if [[ "$BOOT_COMPLETED" != "1" ]]; then
  echo "ADB target has not completed boot." >&2
  exit 1
fi
if [[ "$QEMU" == "1" ]]; then
  echo "Physical-device acceptance refuses emulator/qemu targets." >&2
  exit 1
fi
if [[ -n "${EXPECTED_MODEL:-}" && "$MODEL" != "$EXPECTED_MODEL" ]]; then
  echo "Device model mismatch: expected=$EXPECTED_MODEL actual=$MODEL" >&2
  exit 1
fi

BEFORE_SIZE="$("${ADB[@]}" shell wm size | tr -d '\r')"
BEFORE_DENSITY="$("${ADB[@]}" shell wm density | tr -d '\r')"
BEFORE_NIGHT="$("${ADB[@]}" shell cmd uimode night 2>&1 | tr -d '\r' || true)"
BEFORE_AIRPLANE="$("${ADB[@]}" shell settings get global airplane_mode_on | tr -d '\r' || true)"

cat > "$OUT/DEVICE_BEFORE.txt" <<EOF
source_head_sha=$SOURCE_HEAD_SHA
actual_head_sha=$ACTUAL_HEAD_SHA
adb_version=$ADB_VERSION
instrumentation_mode=$INSTRUMENTATION_MODE
serial=$SERIAL
manufacturer=$MANUFACTURER
model=$MODEL
device=$DEVICE
android_release=$ANDROID_RELEASE
android_sdk=$ANDROID_SDK
boot_completed=$BOOT_COMPLETED
ro.kernel.qemu=$QEMU
wm_size=$BEFORE_SIZE
wm_density=$BEFORE_DENSITY
uimode_night=$BEFORE_NIGHT
airplane_mode=$BEFORE_AIRPLANE
EOF

# This runner is intentionally non-invasive with respect to device system
# configuration: it does NOT modify display size, density, UI mode, airplane
# mode, or network state. It only exercises the native narrow-phone layout
# against the device's current system configuration.
"${ADB[@]}" logcat -c || true
"${ADB[@]}" shell rm -rf "$REMOTE_SCREENS"
"${ADB[@]}" shell mkdir -p "$REMOTE_SCREENS"

./gradlew --no-daemon :app:assembleDebug :app:assembleDebugAndroidTest

TEST_CLASS="com.xuanxue.app.RcDeviceAcceptanceTest"
TEST_SOURCE="app/src/androidTest/kotlin/com/xuanxue/app/RcDeviceAcceptanceTest.kt"
EXPECTED_TEST_COUNT="$(grep -c '^[[:space:]]*@Test' "$TEST_SOURCE")"
if [[ "$EXPECTED_TEST_COUNT" -lt 1 ]]; then
  echo "Unable to determine physical-device instrumentation test count." >&2
  exit 1
fi

INSTRUMENTATION_COMPONENT="gradle-connected"
INSTRUMENTATION_LOG="$OUT/INSTRUMENTATION.txt"
rm -f "$INSTRUMENTATION_LOG"

if [[ "$INSTRUMENTATION_MODE" == "GRADLE_CONNECTED" ]]; then
  ./gradlew --no-daemon :app:connectedDebugAndroidTest \
    -Pandroid.testInstrumentationRunnerArguments.class="$TEST_CLASS" \
    -Pandroid.testInstrumentationRunnerArguments.formFactor=narrow
else
  MAIN_APK="app/build/outputs/apk/debug/app-debug.apk"
  TEST_APK="app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk"
  test -s "$MAIN_APK"
  test -s "$TEST_APK"

  "${ADB[@]}" install -r -t "$MAIN_APK" >/dev/null
  "${ADB[@]}" install -r -t "$TEST_APK" >/dev/null

  mapfile -t INSTRUMENTATION_ROWS < <(
    "${ADB[@]}" shell pm list instrumentation \
      | tr -d '\r' \
      | awk '/target=com\.xuanxue\.app\.debug/ {line=$0; sub(/^instrumentation:/, "", line); sub(/ .*/, "", line); print line}'
  )
  if [[ "${#INSTRUMENTATION_ROWS[@]}" -ne 1 ]]; then
    echo "ADB_DIRECT requires exactly one instrumentation targeting com.xuanxue.app.debug; found ${#INSTRUMENTATION_ROWS[@]}." >&2
    "${ADB[@]}" shell pm list instrumentation >&2 || true
    exit 1
  fi
  INSTRUMENTATION_COMPONENT="${INSTRUMENTATION_ROWS[0]}"

  set +e
  "${ADB[@]}" shell am instrument -w -r \
    -e class "$TEST_CLASS" \
    -e formFactor narrow \
    "$INSTRUMENTATION_COMPONENT" 2>&1 \
    | tr -d '\r' \
    | tee "$INSTRUMENTATION_LOG"
  INSTRUMENTATION_EXIT="${PIPESTATUS[0]}"
  set -e

  if [[ "$INSTRUMENTATION_EXIT" -ne 0 ]]; then
    echo "ADB_DIRECT instrumentation command failed: exit=$INSTRUMENTATION_EXIT" >&2
    exit 1
  fi
  if grep -Eq 'FAILURES!!!|INSTRUMENTATION_FAILED|INSTRUMENTATION_STATUS: Error' "$INSTRUMENTATION_LOG"; then
    echo "ADB_DIRECT instrumentation reported a failure." >&2
    exit 1
  fi
  if ! grep -Fq "OK ($EXPECTED_TEST_COUNT tests)" "$INSTRUMENTATION_LOG"; then
    echo "ADB_DIRECT instrumentation did not report all $EXPECTED_TEST_COUNT tests as OK." >&2
    exit 1
  fi
  if ! grep -Fq 'INSTRUMENTATION_CODE: -1' "$INSTRUMENTATION_LOG"; then
    echo "ADB_DIRECT instrumentation missing successful INSTRUMENTATION_CODE: -1." >&2
    exit 1
  fi
fi

SCREENSHOT_COUNT="$("${ADB[@]}" shell "find '$REMOTE_SCREENS' -maxdepth 1 -type f -name '*.png' | wc -l" | tr -d '\r[:space:]')"
if [[ "$SCREENSHOT_COUNT" -lt 16 ]]; then
  echo "Expected at least 16 physical-device acceptance screenshots; found $SCREENSHOT_COUNT." >&2
  "${ADB[@]}" shell "find '$REMOTE_SCREENS' -maxdepth 1 -type f -print" >&2 || true
  exit 1
fi

rm -rf "$OUT/screenshots" "$OUT/test-results" "$OUT/html-report"
"${ADB[@]}" pull "$REMOTE_SCREENS" "$OUT/screenshots" >/dev/null
if [[ "$INSTRUMENTATION_MODE" == "GRADLE_CONNECTED" ]]; then
  if [[ -d app/build/outputs/androidTest-results/connected ]]; then
    cp -R app/build/outputs/androidTest-results/connected "$OUT/test-results"
  fi
  if [[ -d app/build/reports/androidTests/connected ]]; then
    cp -R app/build/reports/androidTests/connected "$OUT/html-report"
  fi
else
  mkdir -p "$OUT/test-results"
  cp "$INSTRUMENTATION_LOG" "$OUT/test-results/instrumentation.txt"
fi
"${ADB[@]}" logcat -d -t 5000 > "$OUT/LOGCAT_TAIL.txt" 2>&1 || true

AFTER_SIZE="$("${ADB[@]}" shell wm size | tr -d '\r')"
AFTER_DENSITY="$("${ADB[@]}" shell wm density | tr -d '\r')"
AFTER_NIGHT="$("${ADB[@]}" shell cmd uimode night 2>&1 | tr -d '\r' || true)"
AFTER_AIRPLANE="$("${ADB[@]}" shell settings get global airplane_mode_on | tr -d '\r' || true)"

if [[ "$AFTER_SIZE" != "$BEFORE_SIZE" || "$AFTER_DENSITY" != "$BEFORE_DENSITY" || "$AFTER_NIGHT" != "$BEFORE_NIGHT" || "$AFTER_AIRPLANE" != "$BEFORE_AIRPLANE" ]]; then
  echo "Physical-device system state drift detected; acceptance fails closed." >&2
  exit 1
fi

APK="app/build/outputs/apk/debug/app-debug.apk"
test -s "$APK"
APK_SHA256="$(sha256sum "$APK" | awk '{print $1}')"

cat > "$OUT/RESULT.txt" <<EOF
status=PASS
source_head_sha=$SOURCE_HEAD_SHA
actual_head_sha=$ACTUAL_HEAD_SHA
adb_version=$ADB_VERSION
instrumentation_mode=$INSTRUMENTATION_MODE
instrumentation_component=$INSTRUMENTATION_COMPONENT
instrumentation_tests=$EXPECTED_TEST_COUNT
serial=$SERIAL
manufacturer=$MANUFACTURER
model=$MODEL
device=$DEVICE
android_release=$ANDROID_RELEASE
android_sdk=$ANDROID_SDK
form_factor=narrow
acceptance_screenshots=$SCREENSHOT_COUNT
apk_sha256=$APK_SHA256
system_state_preserved=true
wm_size=$AFTER_SIZE
wm_density=$AFTER_DENSITY
uimode_night=$AFTER_NIGHT
airplane_mode=$AFTER_AIRPLANE
EOF

printf 'physical-device-acceptance: PASS\nmodel=%s serial=%s screenshots=%s tests=%s mode=%s source_head_sha=%s\n' \
  "$MODEL" "$SERIAL" "$SCREENSHOT_COUNT" "$EXPECTED_TEST_COUNT" "$INSTRUMENTATION_MODE" "$SOURCE_HEAD_SHA"
