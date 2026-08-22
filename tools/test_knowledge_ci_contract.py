#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "knowledge-engine-ci.yml"


def require(text: str, needle: str):
    if needle not in text:
        raise AssertionError(f"missing CI contract fragment: {needle}")


def forbid(text: str, needle: str):
    if needle in text:
        raise AssertionError(f"forbidden CI contract fragment: {needle}")


def main():
    text = WORKFLOW.read_text(encoding="utf-8")

    # Runtime-only runner paths must be established after a runner exists,
    # then exported through GITHUB_ENV for subsequent Windows steps.
    forbid(text, "K2_PYTHON_DEPS: ${{ runner.temp }}")
    require(text, "- name: Prepare isolated K2 dependency target")
    require(text, "$env:RUNNER_TEMP")
    require(text, "$env:GITHUB_ENV")
    require(text, 'python -m pip install --target "$env:K2_PYTHON_DEPS" -r tools/k2_helper_requirements.txt')
    require(text, 'python tools/validate_k2_python_deps.py --python-deps-dir "$env:K2_PYTHON_DEPS"')

    # Both local contract tests and the real isolated dependency validator are
    # required in CI so a pure-Python shell cannot masquerade as a healthy
    # native dependency installation.
    require(text, "python3 tools/test_knowledge_ci_contract.py")
    require(text, "python3 tools/test_k2_python_deps.py")
    require(text, "python tools/test_k2_python_deps.py")
    require(text, "Verify isolated K2 PDF dependency health")

    # Work identity and cross-work course provenance are orthogonal. Both must
    # remain fail-closed so same-course works cannot inflate source votes.
    require(text, "python3 tools/test_k2_source_lineage.py")
    require(text, "python3 tools/validate_k2_lineage_integrity.py")
    require(text, "python3 tools/test_k2_course_lineage.py")
    require(text, "python3 tools/validate_k2_course_lineage.py")

    # Composite-carrier facts must remain guarded at every refinement layer.
    require(text, "python3 tools/test_k2_source_segments.py")
    require(text, "python3 tools/validate_k2_source_segments.py")
    require(text, "python3 tools/test_k2_segment_lineage.py")
    require(text, "python3 tools/validate_k2_segment_lineage.py")
    require(text, "python3 tools/test_k2_segment_evidence.py")
    require(text, "python3 tools/validate_k2_segment_evidence.py")
    require(text, "python3 tools/test_k2_deep_reading.py")
    require(text, "python3 tools/validate_k2_deep_reading.py")
    require(text, "python3 tools/test_k2_work_family_distillates.py")
    require(text, "python3 tools/validate_k2_work_family_distillates.py")

    # Fully visual-reviewed standalone books need their own closure lane. It is
    # distinct from Wave1 book distillates and from multi-carrier work-family
    # distillation, and it must preserve course-family single-vote constraints.
    require(text, "python3 tools/test_k2_deep_source_distillates.py")
    require(text, "python3 tools/validate_k2_deep_source_distillates.py")

    # Re-audit overlays must be enforced after source-local evidence validation:
    # historical Evidence can be held/downgraded without rewriting provenance.
    require(text, "python3 tools/test_k2_evidence_reaudit.py")
    require(text, "python3 tools/validate_k2_evidence_reaudit.py")

    # Candidate theories may not obtain empirical credit without a
    # pre-outcome freeze and fail-closed prospective validation contract.
    require(text, "python3 tools/test_k2_prospective_validation.py")
    require(text, "python3 tools/validate_k2_prospective_validation.py")

    print("knowledge-ci-contract-tests: PASS")


if __name__ == "__main__":
    main()
