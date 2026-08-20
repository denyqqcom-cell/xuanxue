#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "constraints": ROOT / "奇门" / "CURRENT_METHOD_CONSTRAINTS.md",
    "workflow": ROOT / "奇门" / "qclaw" / "WORKFLOW.md",
    "agent": ROOT / "奇门" / "qclaw" / "_AGENT_INSTRUCTIONS.md",
    "overview": ROOT / "奇门" / "qclaw" / "qimen-overview" / "SKILL.md",
}


def fail(msg: str) -> None:
    raise SystemExit(f"qimen-execution-freeze-contract: FAIL: {msg}")


def main() -> None:
    texts = {name: path.read_text(encoding="utf-8") for name, path in FILES.items()}

    required_common = (
        "star_state_system",
        "door_state_system",
        "deity_system",
        "setup_calibration",
        "seasonal_alignment",
        "method_layer",
        "Role Map",
        "Frozen Prediction",
    )
    for name, text in texts.items():
        for needle in required_common:
            if needle not in text:
                fail(f"{name} missing {needle!r}")

    for name in ("constraints", "workflow", "agent", "overview"):
        text = texts[name]
        if "CONTEXT_REQUIRED" not in text or "NOT_APPLICABLE" not in text:
            fail(f"{name} must define unresolved/not-used state-system behavior")

    if "STATE_SYSTEM_ERROR" not in texts["workflow"]:
        fail("workflow missing STATE_SYSTEM_ERROR")
    if "STATE_SYSTEM_ERROR" not in texts["agent"]:
        fail("agent missing STATE_SYSTEM_ERROR")
    if "STATE_SYSTEM_ERROR" not in texts["overview"]:
        fail("overview missing STATE_SYSTEM_ERROR")

    if "State-System Gate" not in texts["constraints"]:
        fail("constraints missing State-System Gate")
    if "State-System Freeze" not in texts["overview"]:
        fail("overview missing State-System Freeze")

    # Protect against the old execution drift: a scored model cannot defer state-system choice until feedback.
    for name in ("constraints", "workflow", "agent", "overview"):
        text = texts[name]
        if "结果后" not in text and "反馈后" not in text:
            fail(f"{name} missing post-feedback prohibition")

    print("qimen-execution-freeze-contract: PASS")


if __name__ == "__main__":
    main()
