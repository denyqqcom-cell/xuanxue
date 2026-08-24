#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / ".github" / "scripts" / "run_physical_device_acceptance.sh"


def main():
    text = RUNNER.read_text(encoding="utf-8")

    required = (
        "exactly one ADB target",
        "ro.kernel.qemu",
        "EXPECTED_MODEL",
        "SOURCE_HEAD_SHA",
        ":app:connectedDebugAndroidTest",
        "formFactor=narrow",
        "acceptance_screenshots",
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

    setter_patterns = (
        r"\bwm\s+size\s+\S+",
        r"\bwm\s+density\s+\S+",
        r"\bcmd\s+uimode\s+night\s+\S+",
    )
    for pattern in setter_patterns:
        assert re.search(pattern, text) is None, f"physical-device runner contains system-setting mutator: {pattern}"

    print("physical-device-acceptance-contract: PASS")
    print("single_device=true physical_only=true form_factor=narrow system_setting_mutation=false")


if __name__ == "__main__":
    main()
