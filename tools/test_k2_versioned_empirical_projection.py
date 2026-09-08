#!/usr/bin/env python3
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_k2_versioned_preoutcome_revision as rvfx
import validate_k2_empirical_credit_review as er
import validate_k2_prospective_validation as pv

SAMPLE_POLICY_SHA = "1" * 64
SAMPLE_SCHEMA_SHA = "2" * 64
SAMPLE_FINGERPRINT = "3" * 64


def bind_sample_provenance(freeze):
    row = copy.deepcopy(freeze)
    payload = row["frozen_payload"]
    payload["sample_provenance_policy_version"] = "SAMPLE_PROVENANCE_V1"
    payload["sample_provenance_policy_sha256"] = SAMPLE_POLICY_SHA
    payload["sample_fingerprint_key_id"] = "TEST_KEY_V1"
    payload["sample_identity_schema_version"] = "SAMPLE_IDENTITY_V1"
    payload["sample_identity_schema_sha256"] = SAMPLE_SCHEMA_SHA
    payload["sample_fingerprint"] = SAMPLE_FINGERPRINT
    row["frozen_payload_sha256"] = pv.canonical_sha256(payload)
    return row


def main():
    p = rvfx.plan()
    b = rvfx.fixtures.batch(p)
    b["planned_case_count"] = 1

    v1 = bind_sample_provenance(rvfx.versioned_freeze(p, b))
    v2 = bind_sample_provenance(rvfx.versioned_freeze(
        p, b,
        version=2,
        parent=v1["freeze_id"],
        issued_at="2026-08-22T06:00:00Z",
        cutoff_at="2026-08-22T05:59:00Z",
        prediction="EVENT_B",
    ))
    outcome = rvfx.outcome_for(v2)

    # Audit-only history must remain retained without becoming another empirical case.
    v3 = bind_sample_provenance(rvfx.versioned_freeze(
        p, b,
        version=3,
        parent=v2["freeze_id"],
        issued_at="2026-08-24T00:00:00Z",
        cutoff_at="2026-08-23T23:59:00Z",
        prediction="EVENT_A",
        eligibility="AUDIT_ONLY_POST_OUTCOME",
    ))

    policy = er.policy_for_batch(b)
    assert policy is not None
    summary = er.compute_credit_summary(p, [b], [v1, v2, v3], [outcome], [], policy)

    # One underlying case, three immutable prediction versions.
    assert summary["total_case_count"] == 1, summary
    assert summary["case_token_unique"] is True, summary
    assert summary["sample_provenance_consistent"] is True, summary
    assert summary["sample_fingerprint_unique"] is True, summary

    # Only the pre-frozen primary scoring version contributes to score projection.
    assert summary["tie_count"] == 1, summary
    assert summary["candidate_win_count"] == 0, summary
    assert summary["comparator_win_count"] == 0, summary
    assert summary["pooled_paired_delta"] == 0.0, summary

    # Empirical validator must accept the revision-aware prospective history itself;
    # absence of a credit-review row must not resurrect legacy duplicate-Freeze errors.
    issues = er.validate_records(
        rvfx.fixtures.fixtures.distillates(),
        [p], [b], [v1, v2, v3], [outcome], [], [],
    )
    text = "; ".join(f"{owner}: {message}" for owner, message in issues)
    assert not issues, text

    print("k2-versioned-empirical-projection-tests: PASS")
    print("cases=2")


if __name__ == "__main__":
    main()
