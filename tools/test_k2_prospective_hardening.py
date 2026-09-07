#!/usr/bin/env python3
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_k2_prospective_validation as fixtures
import validate_k2_prospective_validation as base

try:
    import validate_k2_prospective_hardening as hardening
except ImportError:
    hardening = None


HARDENING_FIELDS = {"outcome_ontology", "factor_budget", "path_budget"}


def plan():
    p = fixtures.plan()
    p["freeze_required_fields"] = sorted(set(p["freeze_required_fields"]) | HARDENING_FIELDS)
    return p


def batch(p=None):
    return fixtures.batch(p or plan())


def ontology():
    return {
        "target_domain": "qimen",
        "target_variable": "NORMALIZED_EVENT_A",
        "event_definition": "EVENT_A",
        "direction": "OCCUR",
        "event_window": {
            "start_at_utc": "2026-08-22T00:00:00Z",
            "end_at_utc": "2026-08-23T00:00:00Z",
        },
        "threshold": None,
        "tolerance": None,
        "unit": None,
        "scale": "BINARY",
        "subject_binding": "OBJECT_A",
        "matching_rule": "EXACT_CATEGORY_MATCH",
        "missingness_handling": "UNEVALUABLE",
        "censoring_handling": "UNEVALUABLE",
        "scorable_conditions": ["outcome observed within frozen window"],
        "non_scorable_conditions": ["outcome source unavailable"],
    }


def freeze(p=None, b=None):
    p = p or plan()
    b = b or batch(p)
    f = fixtures.freeze(p, b)
    f["frozen_payload"]["outcome_ontology"] = ontology()
    f["frozen_payload"]["factor_budget"] = 2
    f["frozen_payload"]["path_budget"] = 2
    f["frozen_payload_sha256"] = base.canonical_sha256(f["frozen_payload"])
    return f


def validate_all(p, b=None, f=None):
    plans = [p]
    batches = [b] if b is not None else []
    freezes = [f] if f is not None else []
    issues = list(base.validate_records(fixtures.distillates(), plans, batches, freezes, []))
    if hardening is not None:
        issues.extend(hardening.validate_hardening(fixtures.distillates(), plans, batches, freezes, []))
    return issues


def text(issues):
    return "; ".join(f"{key}: {message}" for key, message in issues)


def assert_fail(p, b, f, needle):
    issues = validate_all(p, b, f)
    rendered = text(issues)
    assert issues, f"expected fail-closed issue containing {needle!r}"
    assert needle in rendered, (needle, rendered)


def main():
    p = plan()
    b = batch(p)
    f = freeze(p, b)

    issues = validate_all(p, b, f)
    assert not issues, issues

    badp = copy.deepcopy(p)
    badp["freeze_required_fields"].remove("outcome_ontology")
    badb = batch(badp)
    badf = freeze(badp, badb)
    assert_fail(badp, badb, badf, "hardening fields")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["outcome_ontology"] = "decide after outcome"
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "outcome_ontology must be machine-evaluable object")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["outcome_ontology"]["extra"] = "post-hoc degree of freedom"
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "outcome_ontology fields mismatch")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["outcome_ontology"]["target_domain"] = "bazi"
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "target_domain outside governed routes")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["outcome_ontology"]["event_window"]["end_at_utc"] = "2026-08-21T00:00:00Z"
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "event_window end must be after start")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["outcome_ontology"]["threshold"] = "TBD"
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "threshold must be null or finite numeric")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["factor_budget"] = 1
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "eligible_rule_set exceeds factor_budget")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["path_budget"] = 1
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "interpretation_path exceeds path_budget")

    bad = copy.deepcopy(f)
    bad["frozen_payload"]["factor_budget"] = 0
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, bad, "factor_budget must be positive integer")

    print("k2-prospective-hardening-tests: PASS")
    print("cases=9")


if __name__ == "__main__":
    main()
