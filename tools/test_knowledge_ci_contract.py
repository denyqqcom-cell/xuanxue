#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "knowledge-engine-ci.yml"
QCIC_WORKFLOW = ROOT / ".github" / "workflows" / "k2-qcic-v06-gates.yml"
COGNITIVE_WORKFLOW = ROOT / ".github" / "workflows" / "k2-qimen-cognitive-reconstruction.yml"


def require(text: str, needle: str):
    if needle not in text:
        raise AssertionError(f"missing CI contract fragment: {needle}")


def forbid(text: str, needle: str):
    if needle in text:
        raise AssertionError(f"forbidden CI contract fragment: {needle}")


def main():
    text = WORKFLOW.read_text(encoding="utf-8")
    forbid(text, "K2_PYTHON_DEPS: ${{ runner.temp }}")
    require(text, "- name: Prepare isolated K2 dependency target")
    require(text, "$env:RUNNER_TEMP")
    require(text, "$env:GITHUB_ENV")
    require(text, 'python -m pip install --target "$env:K2_PYTHON_DEPS" -r tools/k2_helper_requirements.txt')
    require(text, 'python tools/validate_k2_python_deps.py --python-deps-dir "$env:K2_PYTHON_DEPS"')
    require(text, "python3 tools/test_knowledge_ci_contract.py")
    require(text, "python3 tools/test_k2_python_deps.py")
    require(text, "python tools/test_k2_python_deps.py")
    require(text, "Verify isolated K2 PDF dependency health")

    # Accepted raw lineage remains auditable, while later full visual evidence
    # may add a reviewed correction overlay consumed as effective lineage.
    require(text, "python3 tools/test_k2_source_lineage.py")
    require(text, "python3 tools/validate_k2_lineage_integrity.py")
    require(text, "python3 tools/test_k2_lineage_corrections.py")
    require(text, "python3 tools/validate_k2_lineage_corrections.py")
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

    # K1 semantic UNKNOWN rows are immutable historical intake. Later complete
    # reading may resolve them only through the reviewed discovery-routing
    # overlay, with machine-derived remaining-backlog accounting.
    require(text, "python3 tools/test_k2_semantic_discovery_routing.py")
    require(text, "python3 tools/validate_k2_semantic_discovery_routing.py")
    for required_path in (
        ROOT / "knowledge" / "schema" / "semantic_discovery_routing.schema.json",
        ROOT / "knowledge" / "K2_SEMANTIC_DISCOVERY_ROUTING.jsonl",
        ROOT / "knowledge" / "K2_UNKNOWN_TEXTUAL_BACKLOG.json",
        ROOT / "knowledge" / "K2_SEMANTIC_DISCOVERY_ROUTING_PROTOCOL.md",
        ROOT / "tools" / "generate_k2_unknown_textual_backlog.py",
        ROOT / "tools" / "test_k2_semantic_discovery_routing.py",
        ROOT / "tools" / "validate_k2_semantic_discovery_routing.py",
    ):
        if not required_path.exists():
            raise AssertionError(f"missing semantic discovery routing artifact: {required_path.relative_to(ROOT)}")

    # Qimen deep-closure now has an explicit cognitive-reconstruction lane.
    # It must preserve historical mistakes, keep corpus-completeness claims
    # fail-closed while UNKNOWN backlog remains, and treat the new SCRM model as
    # an untested candidate rather than a source of empirical credit.
    require(text, "python3 tools/test_k2_qimen_cognitive_reconstruction.py")
    require(text, "python3 tools/validate_k2_qimen_cognitive_reconstruction.py")
    require(text, "python3 tools/test_k2_qimen_tbv.py")
    require(text, "python3 tools/validate_k2_qimen_tbv.py")
    cognitive = COGNITIVE_WORKFLOW.read_text(encoding="utf-8")
    require(cognitive, "name: K2 Qimen Cognitive Reconstruction Gates")
    require(cognitive, "python3 tools/test_k2_qimen_cognitive_reconstruction.py")
    require(cognitive, "python3 tools/validate_k2_qimen_cognitive_reconstruction.py")
    require(cognitive, "python3 tools/test_k2_qimen_tbv.py")
    require(cognitive, "python3 tools/validate_k2_qimen_tbv.py")
    for required_path in (
        ROOT / "knowledge" / "schema" / "qimen_cognitive_reconstruction_state.schema.json",
        ROOT / "knowledge" / "schema" / "qimen_cognitive_error.schema.json",
        ROOT / "knowledge" / "schema" / "qimen_scenario_reasoning.schema.json",
        ROOT / "knowledge" / "schema" / "qimen_tbv_review.schema.json",
        ROOT / "knowledge" / "schema" / "qimen_tbv_state.schema.json",
        ROOT / "knowledge" / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_STATE.json",
        ROOT / "knowledge" / "K2_QIMEN_COGNITIVE_ERROR_LEDGER.jsonl",
        ROOT / "knowledge" / "K2_QIMEN_COGNITIVE_RECONSTRUCTION_CHARTER.md",
        ROOT / "knowledge" / "K2_QIMEN_SCRM_V01.md",
        ROOT / "knowledge" / "K2_QIMEN_TBV_REVIEW_REGISTRY.jsonl",
        ROOT / "knowledge" / "K2_QIMEN_TBV_STATE.json",
        ROOT / "knowledge" / "K2_QIMEN_TBV_PROTOCOL.md",
        ROOT / "tools" / "test_k2_qimen_cognitive_reconstruction.py",
        ROOT / "tools" / "validate_k2_qimen_cognitive_reconstruction.py",
        ROOT / "tools" / "test_k2_qimen_tbv.py",
        ROOT / "tools" / "validate_k2_qimen_tbv.py",
    ):
        if not required_path.exists():
            raise AssertionError(f"missing Qimen cognitive-reconstruction artifact: {required_path.relative_to(ROOT)}")

    require(text, "python3 tools/test_k2_work_family_distillates.py")
    require(text, "python3 tools/validate_k2_work_family_distillates.py")

    # Fully visual-reviewed standalone source units (whole works or corrected
    # work parts) need their own closure lane without duplicating family credit.
    require(text, "python3 tools/test_k2_deep_source_distillates.py")
    require(text, "python3 tools/validate_k2_deep_source_distillates.py")

    require(text, "python3 tools/test_k2_evidence_reaudit.py")
    require(text, "python3 tools/validate_k2_evidence_reaudit.py")
    require(text, "python3 tools/test_k2_prospective_validation.py")
    require(text, "python3 tools/validate_k2_prospective_validation.py")

    # Claim Extraction readiness is a fail-closed review gate, not an automatic
    # phase transition. The snapshot must remain current and authorization false.
    require(text, "python3 tools/test_k2_claim_extraction_readiness.py")
    require(text, "python3 tools/validate_k2_claim_extraction_readiness.py")

    for required_path in (
        ROOT / "knowledge" / "schema" / "claim_extraction_readiness.schema.json",
        ROOT / "knowledge" / "K2_CLAIM_EXTRACTION_READINESS.json",
        ROOT / "knowledge" / "K2_CLAIM_EXTRACTION_READINESS_PROTOCOL.md",
        ROOT / "tools" / "generate_k2_claim_extraction_readiness.py",
        ROOT / "tools" / "test_k2_claim_extraction_readiness.py",
        ROOT / "tools" / "validate_k2_claim_extraction_readiness.py",
    ):
        if not required_path.exists():
            raise AssertionError(f"missing Claim Extraction readiness artifact: {required_path.relative_to(ROOT)}")

    # QCIC v0.6 is not only prose: source stance, deterministic enumeration
    # collapse and the downstream materialized eligibility view are guarded by
    # a dedicated fail-closed workflow.
    qcic = QCIC_WORKFLOW.read_text(encoding="utf-8")
    require(qcic, "name: K2 QCIC v0.6 Machine Gates")
    require(qcic, "python3 tools/test_k2_source_stance.py")
    require(qcic, "python3 tools/validate_k2_source_stance.py")
    require(qcic, "python3 tools/test_k2_enumeration_compression.py")
    require(qcic, "python3 tools/validate_k2_enumeration_compression.py")
    require(qcic, "python3 tools/test_k2_qcic_eligibility_view.py")
    require(qcic, "python3 tools/validate_k2_qcic_eligibility_view.py")

    for required_path in (
        ROOT / "knowledge" / "schema" / "source_stance.schema.json",
        ROOT / "knowledge" / "schema" / "enumeration_compression.schema.json",
        ROOT / "knowledge" / "schema" / "qcic_inference_eligibility_view.schema.json",
        ROOT / "knowledge" / "K2_SOURCE_STANCE_REGISTRY.jsonl",
        ROOT / "knowledge" / "K2_ENUMERATION_COMPRESSION_REGISTRY.jsonl",
        ROOT / "knowledge" / "K2_QCIC_V06_GATE_STATE.json",
        ROOT / "knowledge" / "K2_QCIC_INFERENCE_ELIGIBILITY_VIEW.json",
        ROOT / "tools" / "generate_k2_qcic_eligibility_view.py",
        ROOT / "tools" / "validate_k2_qcic_eligibility_view.py",
    ):
        if not required_path.exists():
            raise AssertionError(f"missing QCIC v0.6 machine-gate artifact: {required_path.relative_to(ROOT)}")

    print("knowledge-ci-contract-tests: PASS")


if __name__ == "__main__":
    main()
