#!/usr/bin/env python3
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_k2_prospective_hardening as fixtures
import validate_k2_prospective_validation as base
import validate_k2_prospective_hardening as hardening

REVISION_FIELD = "revision_lock"
PRIMARY_SCORING_POLICIES = {"FIRST_ISSUED", "LATEST_PRE_OUTCOME_CUTOFF"}


def revision_lock(version, parent_freeze_id, issued_at, cutoff_at, policy="LATEST_PRE_OUTCOME_CUTOFF", eligibility="SCORABLE_PRE_OUTCOME"):
    return {
        "prediction_version": version,
        "parent_freeze_id": parent_freeze_id,
        "prediction_issued_at_utc": issued_at,
        "information_cutoff_at_utc": cutoff_at,
        "allowed_information_channels": ["PREDECLARED_CASE_INPUT", "PREDECLARED_UPDATE_CHANNEL"],
        "primary_scoring_policy": policy,
        "scoring_eligibility": eligibility,
    }


def plan():
    p = fixtures.plan()
    p["freeze_required_fields"] = sorted(set(p["freeze_required_fields"]) | {REVISION_FIELD})
    return p


def versioned_freeze(p, b, version=1, parent=None, issued_at="2026-08-22T00:00:00Z", cutoff_at="2026-08-21T23:59:00Z", prediction="EVENT_A", policy="LATEST_PRE_OUTCOME_CUTOFF", eligibility="SCORABLE_PRE_OUTCOME"):
    f = fixtures.freeze(p, b)
    f["freeze_id"] = "K2PVF-CASE_001" if version == 1 else f"K2PVF-CASE_001_V{version}"
    f["frozen_at_utc"] = issued_at
    f["frozen_payload"][REVISION_FIELD] = revision_lock(version, parent, issued_at, cutoff_at, policy, eligibility)
    f["frozen_payload"]["prediction"] = prediction
    f["frozen_payload_sha256"] = base.canonical_sha256(f["frozen_payload"])
    return f


def outcome_for(f, observed_at="2026-08-23T00:00:00Z"):
    o = fixtures.fixtures.outcome(f)
    o["observed_at_utc"] = observed_at
    return o


def validate(p, b, freezes, outcomes):
    ds = fixtures.fixtures.distillates()
    issues = list(base.validate_records(ds, [p], [b], freezes, outcomes))
    issues.extend(hardening.validate_hardening(ds, [p], [b], freezes, outcomes))
    return issues


def text(issues):
    return "; ".join(f"{key}: {message}" for key, message in issues)


def assert_fail(p, b, freezes, outcomes, needle):
    issues = validate(p, b, freezes, outcomes)
    rendered = text(issues)
    assert issues, f"expected fail-closed issue containing {needle!r}"
    assert needle in rendered, (needle, rendered)


def main():
    p = plan()
    b = fixtures.batch(p)

    v1 = versioned_freeze(p, b)
    v2 = versioned_freeze(
        p, b,
        version=2,
        parent=v1["freeze_id"],
        issued_at="2026-08-22T06:00:00Z",
        cutoff_at="2026-08-22T05:59:00Z",
        prediction="EVENT_B",
    )
    o2 = outcome_for(v2)

    # Required capability: one preregistered case may retain multiple immutable
    # pre-outcome prediction versions without inflating the case denominator.
    issues = validate(p, b, [v1, v2], [o2])
    assert not issues, issues

    # Version sequence and parent chain are immutable/auditable.
    bad = copy.deepcopy(v2)
    bad["frozen_payload"][REVISION_FIELD]["prediction_version"] = 3
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, [v1, bad], [], "prediction versions must be contiguous")

    bad = copy.deepcopy(v2)
    bad["frozen_payload"][REVISION_FIELD]["parent_freeze_id"] = "K2PVF-NOT_THE_PARENT"
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, [v1, bad], [], "parent_freeze_id must bind previous immutable version")

    # New information may arrive before outcome, but cutoff must not move past issue time.
    bad = copy.deepcopy(v2)
    bad["frozen_payload"][REVISION_FIELD]["information_cutoff_at_utc"] = "2026-08-22T07:00:00Z"
    bad["frozen_payload_sha256"] = base.canonical_sha256(bad["frozen_payload"])
    assert_fail(p, b, [v1, bad], [], "information cutoff must not be after prediction issue")

    # Scoring policy is frozen before outcome and cannot cherry-pick a favorable version.
    first_policy_v1 = versioned_freeze(p, b, policy="FIRST_ISSUED")
    first_policy_v2 = versioned_freeze(
        p, b, version=2, parent=first_policy_v1["freeze_id"],
        issued_at="2026-08-22T06:00:00Z", cutoff_at="2026-08-22T05:59:00Z",
        prediction="EVENT_B", policy="FIRST_ISSUED",
    )
    cherry = outcome_for(first_policy_v2)
    assert_fail(p, b, [first_policy_v1, first_policy_v2], [cherry], "outcome binds non-primary scoring version")

    # Once the outcome is visible, another revision is audit-only/non-scorable.
    late = versioned_freeze(
        p, b, version=3, parent=v2["freeze_id"],
        issued_at="2026-08-24T00:00:00Z", cutoff_at="2026-08-23T23:59:00Z",
        prediction="EVENT_A", eligibility="SCORABLE_PRE_OUTCOME",
    )
    assert_fail(p, b, [v1, v2, late], [o2], "outcome-visible revision must be AUDIT_ONLY_POST_OUTCOME")

    print("k2-versioned-preoutcome-revision-tests: PASS")
    print("cases=5")


if __name__ == "__main__":
    main()
