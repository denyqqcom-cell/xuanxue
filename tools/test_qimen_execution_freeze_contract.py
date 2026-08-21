#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "constraints": ROOT / "奇门" / "CURRENT_METHOD_CONSTRAINTS.md",
    "prospective": ROOT / "knowledge" / "K2_PROSPECTIVE_CASE_PROTOCOL.md",
    "workflow": ROOT / "奇门" / "qclaw" / "WORKFLOW.md",
    "agent": ROOT / "奇门" / "qclaw" / "_AGENT_INSTRUCTIONS.md",
    "overview": ROOT / "奇门" / "qclaw" / "qimen-overview" / "SKILL.md",
}
ENGINE = ROOT / "ziwei-core" / "src" / "main" / "kotlin" / "com" / "xuanxue" / "qimen" / "QimenEngine.kt"
APP = ROOT / "app" / "src" / "main" / "kotlin" / "com" / "xuanxue" / "app" / "QimenScreen.kt"
INTERPRETERS = ROOT / "ziwei-core" / "src" / "main" / "kotlin" / "com" / "xuanxue" / "ai" / "Interpreters.kt"


def fail(msg: str) -> None:
    raise SystemExit(f"qimen-execution-freeze-contract: FAIL: {msg}")


def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        fail(f"{where} missing {needle!r}")


def main() -> None:
    texts = {name: path.read_text(encoding="utf-8") for name, path in FILES.items()}

    required_common = (
        "method_layer",
        "setup_method",
        "setup_calibration",
        "seasonal_alignment",
        "time_boundary_system",
        "deity_system",
        "star_state_system",
        "door_state_system",
        "Role Map",
        "Frozen Prediction",
    )
    for name,text in texts.items():
        for needle in required_common:
            if needle not in text:fail(f"{name} missing {needle!r}")
        if "CONTEXT_REQUIRED" not in text or "NOT_APPLICABLE" not in text:
            fail(f"{name} must define unresolved/not-used behavior")
        if "结果后" not in text and "反馈后" not in text and "post-feedback" not in text:
            fail(f"{name} missing post-feedback prohibition")

    if "State-System Gate" not in texts["constraints"]:fail("constraints missing State-System Gate")
    if "Baseline Firewall" not in texts["constraints"]:fail("constraints missing Baseline Firewall")
    if "Branch-Discrimination Gate" not in texts["constraints"]:fail("constraints missing Branch-Discrimination Gate")
    if "Ambiguity-Debt Gate" not in texts["constraints"]:fail("constraints missing Ambiguity-Debt Gate")
    if "Model-Compression Review" not in texts["constraints"]:fail("constraints missing Model-Compression Review")
    if "Source-Topology Gate" not in texts["constraints"]:fail("constraints missing Source-Topology Gate")
    if "NEUTRAL_SETUP_FACTS" not in texts["constraints"] or "PREDICTIVE_AUXILIARY_FACTS" not in texts["constraints"]:
        fail("constraints missing baseline fact separation")

    for needle in (
        "Baseline Firewall",
        "NEUTRAL_SETUP_FACTS",
        "PREDICTIVE_AUXILIARY_FACTS",
        "Branch-Discrimination",
        "Ambiguity Debt",
        "Model-Compression",
    ):
        if needle not in texts["prospective"]:fail(f"prospective missing {needle!r}")

    if "time_boundary_system" not in texts["constraints"]:fail("constraints missing time-boundary gate")
    if "STATE_SYSTEM_ERROR" not in texts["workflow"]:fail("workflow missing STATE_SYSTEM_ERROR")
    if "TIME_BOUNDARY_ERROR" not in texts["workflow"]:fail("workflow missing TIME_BOUNDARY_ERROR")
    if "STATE_SYSTEM_ERROR" not in texts["agent"]:fail("agent missing STATE_SYSTEM_ERROR")
    if "TIME_BOUNDARY_ERROR" not in texts["agent"]:fail("agent missing TIME_BOUNDARY_ERROR")
    if "STATE_SYSTEM_ERROR" not in texts["overview"]:fail("overview missing STATE_SYSTEM_ERROR")
    if "TIME_BOUNDARY_ERROR" not in texts["overview"]:fail("overview missing TIME_BOUNDARY_ERROR")

    # Method Freeze must survive the jump from research documents into executable code.
    # Otherwise the project can say “freeze method” while the App silently uses one default.
    engine = ENGINE.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    interpreters = INTERPRETERS.read_text(encoding="utf-8")

    for needle in (
        "enum class MethodProfile",
        "LEGACY_EXPERIMENTAL",
        "SHANTI_DAO_71_P21_P22",
        "implementationWarnings",
        "representedHourStem",
        "SHANTI_DAO_71_DOOR_TARGET_CENTER_UNRESOLVED",
    ):
        require(engine, needle, "QimenEngine.kt")

    for needle in (
        "var methodProfile",
        "QimenEngine.MethodProfile.LEGACY_EXPERIMENTAL",
        "QimenEngine.MethodProfile.SHANTI_DAO_71_P21_P22",
        "methodProfile)",
        "implementationWarnings",
        "方法配置",
    ):
        require(app, needle, "QimenScreen.kt")

    for needle in (
        "c.methodProfile",
        "c.implementationWarnings",
        "静默切换",
        "不等于预测现实已经得到验证",
    ):
        require(interpreters, needle, "Interpreters.kt")

    print("qimen-execution-freeze-contract: PASS")


if __name__ == "__main__":
    main()
