#!/usr/bin/env python3
"""Fail closed on Android V1.0 stable-release invariants.

This gate validates packaging, security and release metadata. It does not prove
astrology/divination correctness and it does not replace emulator evidence or
visual acceptance review.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
APP_GRADLE = ROOT / "app" / "build.gradle.kts"
MANIFEST = ROOT / "app" / "src" / "main" / "AndroidManifest.xml"
STRINGS = ROOT / "app" / "src" / "main" / "res" / "values" / "strings.xml"
LAUNCHER_ICON = ROOT / "app" / "src" / "main" / "res" / "drawable" / "ic_launcher.xml"
DEVICE_ACCEPTANCE = ROOT / "DEVICE_ACCEPTANCE.md"
RELEASE_ACCEPTANCE = ROOT / "RELEASE_ACCEPTANCE.md"
PRIVACY = ROOT / "PRIVACY.md"
ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    gradle = APP_GRADLE.read_text(encoding="utf-8")
    require('versionName = "1.0.0"' in gradle, "versionName must be 1.0.0")
    require(re.search(r"versionCode\s*=\s*1\b", gradle) is not None, "V1.0 versionCode must be 1")
    require('buildConfigField("String", "RELEASE_CHANNEL", "\\\"stable\\\"")' in gradle, "RELEASE_CHANNEL must be stable")
    require('applicationIdSuffix = ".debug"' in gradle, "debug acceptance package must use .debug applicationIdSuffix")
    require('versionNameSuffix = "-debug"' in gradle, "debug acceptance package must expose -debug versionNameSuffix")
    require('versionName = "1.0.0-rc1"' not in gradle, "RC version metadata must not remain in stable build config")
    require("storePassword" not in gradle and "keyPassword" not in gradle, "signing secrets must not be hard-coded in app/build.gradle.kts")

    strings_root = ET.parse(STRINGS).getroot()
    app_name = next((n.text or "" for n in strings_root.findall("string") if n.attrib.get("name") == "app_name"), "")
    require(app_name == "玄学排盘", "launcher label must be the stable name 玄学排盘")

    require(LAUNCHER_ICON.is_file() and LAUNCHER_ICON.stat().st_size > 0, "original launcher icon resource is missing")
    if LAUNCHER_ICON.is_file():
        icon_text = LAUNCHER_ICON.read_text(encoding="utf-8")
        require("android:pathData" in icon_text and "#315D58" in icon_text, "launcher icon must remain the reviewed project vector asset")

    manifest_root = ET.parse(MANIFEST).getroot()
    permissions = [node.attrib.get(ANDROID_NS + "name", "") for node in manifest_root.findall("uses-permission")]
    require("android.permission.INTERNET" not in permissions, "V1.0 must remain offline: INTERNET permission found")

    app = manifest_root.find("application")
    require(app is not None, "AndroidManifest.xml missing <application>")
    if app is not None:
        require(app.attrib.get(ANDROID_NS + "allowBackup") == "false", "allowBackup must remain false")
        require(app.attrib.get(ANDROID_NS + "usesCleartextTraffic") == "false", "usesCleartextTraffic must remain false")
        require(app.attrib.get(ANDROID_NS + "icon") == "@drawable/ic_launcher", "application icon must point to reviewed ic_launcher")
        require(app.attrib.get(ANDROID_NS + "roundIcon") == "@drawable/ic_launcher", "roundIcon must point to reviewed ic_launcher")
        exported = []
        for tag in ("activity", "activity-alias", "service", "receiver", "provider"):
            for node in app.findall(tag):
                if node.attrib.get(ANDROID_NS + "exported") == "true":
                    exported.append((tag, node.attrib.get(ANDROID_NS + "name", "")))
        require(exported == [("activity", ".MainActivity")], f"unexpected exported Android component(s): {exported}")

    require(DEVICE_ACCEPTANCE.is_file() and DEVICE_ACCEPTANCE.stat().st_size > 0, "DEVICE_ACCEPTANCE.md must exist")
    require(RELEASE_ACCEPTANCE.is_file() and RELEASE_ACCEPTANCE.stat().st_size > 0, "RELEASE_ACCEPTANCE.md must exist")
    require(PRIVACY.is_file() and PRIVACY.stat().st_size > 0, "PRIVACY.md must exist")

    if PRIVACY.is_file():
        privacy_text = PRIVACY.read_text(encoding="utf-8")
        require("android.permission.INTERNET" in privacy_text, "privacy policy must explicitly disclose the current network-permission state")
        require("1.0.0" in privacy_text, "privacy policy must identify V1.0")
        require("1.0.0-rc1" not in privacy_text, "stable privacy policy must not describe RC1 as the current version")

    if RELEASE_ACCEPTANCE.is_file():
        acceptance_text = RELEASE_ACCEPTANCE.read_text(encoding="utf-8")
        require("com.xuanxue.app.debug" in acceptance_text, "release contract must identify debug acceptance package")
        require("visible Android crash/ANR dialog" in acceptance_text, "release contract must fail closed on visible crash/ANR dialogs")
        require("evidence screenshots" in acceptance_text, "release contract must require screenshot evidence review")

    forbidden_suffixes = {".jks", ".keystore", ".p12", ".pfx"}
    leaked_key_files = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() in forbidden_suffixes]
    require(not leaked_key_files, f"private signing container committed to repository: {leaked_key_files}")

    if errors:
        print("V1 RELEASE VALIDATION: FAIL", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print("V1 RELEASE VALIDATION: PASS")
    print("version=1.0.0")
    print("release_channel=stable")
    print("stable_package=com.xuanxue.app")
    print("debug_acceptance_package=com.xuanxue.app.debug")
    print("network=offline")
    print("cleartext=false")
    print("backup=false")
    print("launcher_icon=reviewed_project_vector")
    print("privacy_policy=present")
    print("release_contract=present")
    print("exported_components=MainActivity_only")
    print("emulator_and_visual_acceptance=required_same_head")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
