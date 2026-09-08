#!/usr/bin/env python3
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_k2_versioned_preoutcome_revision as rvfx
import validate_k2_empirical_credit_review as er
import validate_k2_prospective_validation as pv
import validate_k2_sample_provenance as sp
import k2_sample_fingerprint as sf

SAMPLE_FINGERPRINT = "3" * 64


def bind_sample_provenance(freeze, policy, schema):
    row = copy.deepcopy(freeze)
    payload = row["frozen_payload"]
    payload["sample_provenance_policy_version"] = policy["policy_version"]
    payload["sample_provenance_policy_sha256"] = pv.canonical_sha256(policy)
    payload["sample_fingerprint_key_id"] = policy["fingerprint_key_id"]
    payload["sample_identity_schema_version"] = schema["schema_version"]
    payload["sample_identity_schema_sha256"] = sf.canonical_sha256(schema)
    payload["sample_fingerprint"] = SAMPLE_FINGERPRINT
    row["frozen_payload_sha256"] = pv.canonical_sha256(payload)
    return row


def sample_binding(batch, policy, schema):
    return {
        "binding_id": "K2PVSPB-BATCH_001",
        "batch_id": batch["batch_id"],
        "batch_sha256": pv.canonical_sha256(batch),
        "bound_at_utc": "2026-08-21T23:30:00Z",
        "sample_provenance_policy_version": policy["policy_version"],
        "sample_provenance_policy_sha256": pv.canonical_sha256(policy),
        "sample_identity_schema_version": schema["schema_version"],
        "sample_identity_schema_sha256": sf.canonical_sha256(schema),
        "research_only": True,
        "status": "BOUND",
    }


def main():
    p = rvfx.plan()
    b = rvfx.fixtures.batch(p)
    b["planned_case_count"] = 1

    sample_policy = sp.load_policies()[0]
    sample_schema = sp.load_identity_schemas()[0]

    v1 = bind_sample_provenance(rvfx.versioned_freeze(p, b), sample_policy, sample_schema)
    v2 = bind_sample_provenance(rvfx.versioned_freeze(
        p, b,
        version=2,
        parent=v1["freeze_id"],
        issued_at="2026-08-22T06:00:00Z",
        cutoff_at="2026-08-22T05:59:00Z",
        prediction="EVENT_B",
    ), sample_policy, sample_schema)
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
    ), sample_policy, sample_schema)

    binding = sample_binding(b, sample_policy, sample_schema)

    # The same underlying sample fingerprint may repeat across immutable revisions,
    # but only because all rows bind the same versioned case identity.
    provenance_issues = sp.validate_records(
        [b], [v1, v2, v3], [binding], [sample_policy], [sample_schema]
    )
    assert not provenance_issues, provenance_issues

    empirical_policy = er.policy_for_batch(b)
    assert empirical_policy is not None
    summary = er.compute_credit_summary(p, [b], [v1, v2, v3], [outcome], [], empirical_policy)

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

    # End-to-end empirical validator must use revision-aware upstream semantics and
    # preserve pre-outcome sample-provenance binding without duplicate-version inflation.
    issues = er.validate_records(
        rvfx.fixtures.fixtures.distillates(),
        [p], [b], [v1, v2, v3], [outcome], [], [],
        sample_provenance_policies=[sample_policy],
        sample_provenance_bindings=[binding],
        enforce_sample_provenance=True,
        sample_identity_schemas=[sample_schema],
    )
    text = "; ".join(f"{owner}: {message}" for owner, message in issues)
    assert not issues, text

    print("k2-versioned-empirical-projection-tests: PASS")
    print("cases=3")


if __name__ == "__main__":
    main()
