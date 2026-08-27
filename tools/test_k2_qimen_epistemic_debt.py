#!/usr/bin/env python3
import copy
from pathlib import Path

import validate_k2_qimen_epistemic_debt as v

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"


def expect_issue(issues, needle):
    assert any(needle in issue for issue in issues), (needle, issues)


def main():
    base_issues = v.validate(ROOT)
    assert base_issues == [], base_issues

    rows = v.load_jsonl(K / "K2_QIMEN_EPISTEMIC_DEBT.jsonl")
    bias_ids = v.known_bias_ids(ROOT)
    assert len(rows) >= 11

    # Unresolved recurrence can never silently promote itself.
    mutated = copy.deepcopy(rows)
    mutated[0]["promotion_status"] = "RELEASED"
    issues = v.validate_rows(mutated, ROOT, bias_ids)
    expect_issue(issues, "promotion BLOCKED")

    # Audit/engineering success cannot manufacture empirical credit.
    mutated = copy.deepcopy(rows)
    mutated[0]["empirical_credit"] = "STRONG"
    issues = v.validate_rows(mutated, ROOT, bias_ids)
    expect_issue(issues, "cannot grant empirical credit")

    # Release requires unknown-outcome prospective conditions, not a case count.
    mutated = copy.deepcopy(rows)
    mutated[2]["required_before_release"]["unknown_outcome"] = False
    issues = v.validate_rows(mutated, ROOT, bias_ids)
    expect_issue(issues, "unknown_outcome")

    # A new debt must link back to a known cognitive error rather than inventing history.
    mutated = copy.deepcopy(rows)
    mutated[0]["historical_bias_refs"] = ["QCR-BIAS-999"]
    issues = v.validate_rows(mutated, ROOT, bias_ids)
    expect_issue(issues, "unknown historical bias refs")

    # A recurrence debt is not considered repaired merely because a reflection was written.
    mutated = copy.deepcopy(rows)
    recurrence = next(row for row in mutated if row["category"] == "KNOWN_BIAS_RECURRENCE")
    recurrence["resolution_status"] = "REPAIRED"
    issues = v.validate_rows(mutated, ROOT, bias_ids)
    expect_issue(issues, "cannot be REPAIRED")

    # Every declared recurrence category must remain instantiated in the ledger.
    mutated = [row for row in copy.deepcopy(rows) if row["category"] != "CONTROL_COMPLEXITY_ILLUSION"]
    issues = v.validate_rows(mutated, ROOT, bias_ids)
    expect_issue(issues, "category coverage mismatch")

    protocol = (K / "K2_QIMEN_EPISTEMIC_DEBT_PROTOCOL.md").read_text(encoding="utf-8")

    # The protocol must explicitly reject magic-count promotion.
    mutated_protocol = protocol.replace("THREE_SUCCESSES != VALIDATION", "")
    issues = v.validate_protocol(mutated_protocol)
    expect_issue(issues, "THREE_SUCCESSES != VALIDATION")

    # Fractional scores and percentages are not validation credit unless calibrated.
    mutated_protocol = protocol.replace("UNCALIBRATED_SCORE != VALIDATION_CREDIT", "")
    issues = v.validate_protocol(mutated_protocol)
    expect_issue(issues, "UNCALIBRATED_SCORE != VALIDATION_CREDIT")

    # A more coherent story cannot become an empirical proxy.
    mutated_protocol = protocol.replace("NARRATIVE_COHERENCE != EMPIRICAL_VALIDITY", "")
    issues = v.validate_protocol(mutated_protocol)
    expect_issue(issues, "NARRATIVE_COHERENCE != EMPIRICAL_VALIDITY")

    # One failure cannot silently be relabeled as a theory boundary.
    mutated_protocol = protocol.replace("BOUNDARY_CLAIM_REQUIRES_COMPETING_CAUSES", "")
    issues = v.validate_protocol(mutated_protocol)
    expect_issue(issues, "BOUNDARY_CLAIM_REQUIRES_COMPETING_CAUSES")

    # More audit machinery is not itself cognitive or empirical progress.
    mutated_protocol = protocol.replace("CONTROL_COMPLEXITY != EMPIRICAL_PROGRESS", "")
    issues = v.validate_protocol(mutated_protocol)
    expect_issue(issues, "CONTROL_COMPLEXITY != EMPIRICAL_PROGRESS")

    # The schema itself must encode fail-closed promotion and zero empirical credit.
    schema = v.load_json(K / "schema" / "qimen_epistemic_debt.schema.json")
    mutated_schema = copy.deepcopy(schema)
    mutated_schema["properties"]["promotion_status"] = {"type": "string"}
    issues = v.validate_schema_contract(mutated_schema)
    expect_issue(issues, "promotion_status=BLOCKED")

    # The schema may not drop a recurrence category without the validator noticing.
    mutated_schema = copy.deepcopy(schema)
    mutated_schema["properties"]["category"]["enum"].remove("NARRATIVE_COHERENCE")
    issues = v.validate_schema_contract(mutated_schema)
    expect_issue(issues, "category coverage drift")

    print("k2-qimen-epistemic-debt-tests: PASS")
    print("negative_cases=13 base_contract=PASS")


if __name__ == "__main__":
    main()
