#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "LOCAL_AI_EXECUTION_BOUNDARY.json"
PROMPT = ROOT / "LOCAL_HELPER_CURRENT_PROMPT.md"
LEGACY = ROOT / "LOCAL_CORPUS_K2_EVIDENCE_WAVE1_PROMPT.md"
PROJECT_STATE = ROOT / "knowledge" / "PROJECT_STATE.json"


def main():
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    prompt = PROMPT.read_text(encoding="utf-8")
    legacy = LEGACY.read_text(encoding="utf-8")
    project_state = json.loads(PROJECT_STATE.read_text(encoding="utf-8"))

    assert boundary["status"] == "CURRENT"
    assert boundary["role"] == "EXECUTION_HELPER_ONLY"
    assert boundary["authority"] == "PROJECT_MAIN_AGENT"
    assert project_state["local_ai_role"] == "EXECUTION_HELPER_ONLY"
    assert project_state["execution_owner"] == "PROJECT_MAIN_AGENT"

    allowed = set(boundary["allowed_actions"])
    required_allowed = {
        "GIT_FETCH",
        "GIT_FF_ONLY_SYNC_WHEN_TRACKED_CLEAN",
        "LOCAL_MATERIAL_DISCOVERY",
        "CANONICAL_SHA256_VERIFY",
        "PDF_PAGE_COUNT_VERIFY",
        "PAGE_PACKET_INTEGRITY_VERIFY",
    }
    assert required_allowed <= allowed

    forbidden = set(boundary["forbidden_actions"])
    required_forbidden = {
        "CODE_EDIT",
        "TRACKED_FILE_EDIT",
        "KNOWLEDGE_TREE_EDIT",
        "TEST_EXECUTION",
        "GRADLE_EXECUTION",
        "INSTRUMENTATION_EXECUTION",
        "PHYSICAL_DEVICE_ACCEPTANCE_EXECUTION",
        "ADB_DEVICE_OPERATION",
        "DEPENDENCY_INSTALL",
        "ENGINEERING_JUDGMENT",
        "EVIDENCE_WRITE",
        "CLAIM_WRITE",
        "READING_LEDGER_WRITE",
        "LINEAGE_WRITE",
        "DISTILLATE_WRITE",
        "GIT_COMMIT",
        "GIT_PUSH",
        "GIT_RESET",
        "GIT_STASH",
        "GIT_CLEAN",
        "UNTRACKED_FILE_DELETE",
    }
    assert required_forbidden <= forbidden

    prompt_required = (
        "EXECUTION_HELPER_ONLY",
        "git merge --ff-only",
        "canonical SHA256",
        "MAIN_AGENT_ACTION_REQUIRED",
        "不是开发者",
        "不是测试执行器",
        "运行项目测试、Gradle、instrumentation、真机 acceptance",
    )
    missing = [item for item in prompt_required if item not in prompt]
    assert not missing, f"current local helper prompt missing boundary statements: {missing}"

    executable_forbidden = (
        "./gradlew",
        "python tools/test_",
        "run_physical_device_acceptance.sh",
        "adb devices",
        "pip install",
    )
    present = [item for item in executable_forbidden if item in prompt]
    assert not present, f"current local helper prompt contains forbidden executable instructions: {present}"

    assert legacy.startswith("# DEPRECATED")
    assert "LOCAL_HELPER_CURRENT_PROMPT.md" in legacy
    assert "LOCAL_AI_EXECUTION_BOUNDARY.json" in legacy

    print("local-ai-execution-boundary: PASS")
    print(
        "role=EXECUTION_HELPER_ONLY allowed=git_ff_sync+material_verification "
        "tests=false code_edit=false knowledge_edit=false commit_push=false"
    )


if __name__ == "__main__":
    main()
