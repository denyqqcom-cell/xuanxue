#!/usr/bin/env bash
set -euo pipefail

apk="${1:-app/build/outputs/apk/debug/app-debug.apk}"

if [[ ! -f "$apk" ]]; then
  echo "APK not found: $apk" >&2
  exit 1
fi

entries="$(mktemp)"
trap 'rm -f "$entries"' EXIT
unzip -Z1 "$apk" | sort > "$entries"

# Release binary must not accidentally contain research/source-book material.
for pattern in \
  '\.pdf$' \
  '\.epub$' \
  '\.mobi$' \
  '\.docx?$' \
  '\.rtf$' \
  '\.ttf$' \
  '\.otf$' \
  '(^|/)handoff/' \
  '(^|/)奇门/' \
  '(^|/)八字/' \
  '(^|/)紫薇/' \
  '(^|/)风水/' \
  '(^|/)学习资料/' \
  '全文' \
  '_scan' \
  'ocr'; do
  if grep -Eiq "$pattern" "$entries"; then
    echo "Forbidden/review-required content found in APK (pattern: $pattern):" >&2
    grep -Ei "$pattern" "$entries" >&2 || true
    exit 1
  fi
done

# For now the only first-party packaged assets approved by the copyright gate are license files.
unexpected_assets="$(grep '^assets/' "$entries" | grep -Ev '^assets/licenses/(APACHE-2\.0\.txt|OPEN_SOURCE_NOTICES\.txt)$' || true)"
if [[ -n "$unexpected_assets" ]]; then
  echo "Unexpected APK assets require explicit copyright review:" >&2
  echo "$unexpected_assets" >&2
  exit 1
fi

for required in \
  'assets/licenses/APACHE-2.0.txt' \
  'assets/licenses/OPEN_SOURCE_NOTICES.txt'; do
  if ! grep -Fxq "$required" "$entries"; then
    echo "Required packaged notice missing from APK: $required" >&2
    exit 1
  fi
done

echo "APK content audit PASS: $apk"
