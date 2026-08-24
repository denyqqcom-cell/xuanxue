#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / ".github" / "scripts" / "run_physical_device_acceptance.sh"


def assert_query_only(text: str, command: str):
    for raw in text.splitlines():
        code = raw.split("#", 1)[0]
        if command not in code:
            continue
        tail = code.split(command, 1)[1].strip()
        if tail and not tail.startswith(("|", ">", "2>", ";")):
            raise AssertionError(f"physical-device runner may not mutate system setting via {command!r}: {raw}")


def assert_no_hardcoded_adb(text: str):
    for raw in text.splitlines():
        code = raw.split("#", 1)[0]
        if re.search(r"(^|[<(\s])adb(?=\s)", code):
            raise AssertionError(f"physical-device runner must route ADB through ADB_BIN: {raw}")


def main():
    text = RUNNER.read_text(encoding="utf-8")

    required = (
        "exactly one ADB target",
        "ro.kernel.qemu",
        "EXPECTED_MODEL",
        "SOURCE_HEAD_SHA",
        'ACTUAL_HEAD_SHA="$(git rev-parse HEAD)"',
        'if [[ "$ACTUAL_HEAD_SHA" != "$SOURCE_HEAD_SHA" ]]',
        "Source HEAD mismatch",
        "git diff --quiet --",
        "git diff --cached --quiet --",
        'ADB_BIN="${ADB_BIN:-adb}"',
        'ADB_BASE=("$ADB_BIN")',
        '"${ADB_BASE[@]}" devices',
        'ADB=("${ADB_BASE[@]}" -s "$SERIAL")',
        "adb_version=",
        ":app:connectedDebugAndroidTest",
        "formFactor=narrow",
        "acceptance_screenshots",
        "actual_head_sha=",
        "system_state_preserved=true",
    )
    missing = [needle for needle in required if needle not in text]
    assert not missing, f"physical-device runner missing contract fragments: {missing}"

    forbidden_literals = (
        "airplane-mode enable",
        "airplane-mode disable",
        "settings put global airplane_mode_on",
    )
    present = [needle for needle in forbidden_literals if needle in text]
    assert not present, f"physical-device runner may not mutate network state: {present}"

    assert_no_hardcoded_adb(text)
    assert_query_only(text, "wm size")
    assert_query_only(text, "wm density")
    assert_query_only(text, "cmd uimode night")

    print("physical-device-acceptance-contract: PASS")
    print(
        "single_device=true physical_only=true form_factor=narrow "
        "source_head_match=true tracked_worktree_clean=true configurable_adb=true "
        "system_setting_mutation=false"
    )


if __name__ == "__main__":
    main()
