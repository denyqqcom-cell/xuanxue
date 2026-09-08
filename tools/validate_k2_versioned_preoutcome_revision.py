#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_k2_prospective_validation as base
import validate_k2_prospective_hardening as hardening

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"

REVISION_FIELD = "revision_lock"
REVISION_FIELDS = {
    "prediction_version",
    "parent_freeze_id",
    "prediction_issued_at_utc",
    "information_cutoff_at_utc",
    "allowed_information_channels",
    "primary_scoring_policy",
    "scoring_eligibility",
}
PRIMARY_SCORING_POLICIES = {"FIRST_ISSUED", "LATEST_PRE_OUTCOME_CUTOFF"}
SCORING_ELIGIBILITIES = {"SCORABLE_PRE_OUTCOME", "AUDIT_ONLY_POST_OUTCOME"}


def case_key(freeze):
    return (freeze.get("batch_id"), freeze.get("case_id"))


def case_groups(freezes):
    out = {}
    for freeze in freezes:
        out.setdefault(case_key(freeze), []).append(freeze)
    return out


def lock_of(freeze):
    payload = freeze.get("frozen_payload") if isinstance(freeze, dict) else None
    return payload.get(REVISION_FIELD) if isinstance(payload, dict) else None


def unique_case_count_by_batch(freezes):
    out = {}
    for batch_id, case_id in case_groups(freezes):
        if batch_id is not None and case_id is not None:
            out[batch_id] = out.get(batch_id, 0) + 1
    return out


def versioned_case_keys(freezes):
    keys = set()
    for key, rows in case_groups(freezes).items():
        if rows and all(isinstance(lock_of(row), dict) for row in rows):
            keys.add(key)
    return keys


def filter_legacy_counting_issues(issues, freezes, batches):
    """Suppress only legacy row-count errors replaced by explicit revision semantics."""
    freeze_by_id = {row.get("freeze_id"): row for row in freezes}
    versioned = versioned_case_keys(freezes)
    batch_by_id = {row.get("batch_id"): row for row in batches}
    unique_counts = unique_case_count_by_batch(freezes)
    kept = []
    for owner, message in issues:
        freeze = freeze_by_id.get(owner)
        if message == "duplicate case_id inside batch" and freeze is not None and case_key(freeze) in versioned:
            continue
        if message == "freeze count exceeds planned_case_count" and freeze is not None and case_key(freeze) in versioned:
            batch = batch_by_id.get(freeze.get("batch_id")) or {}
            planned = batch.get("planned_case_count")
            if isinstance(planned, int) and not isinstance(planned, bool) and unique_counts.get(freeze.get("batch_id"), 0) <= planned:
                continue
        kept.append((owner, message))
    return kept


def _utc(owner, field, value, issues):
    parsed = base.utc_value(value)
    if parsed is None:
        issues.append((owner, f"{field} must be UTC second timestamp ending Z"))
    return parsed


def _validate_lock(freeze_id, lock):
    issues = []
    if not isinstance(lock, dict):
        return [(freeze_id, "revision_lock must be machine-evaluable object")]
    if set(lock) != REVISION_FIELDS:
        issues.append((freeze_id, f"revision_lock fields mismatch missing={sorted(REVISION_FIELDS-set(lock))} extra={sorted(set(lock)-REVISION_FIELDS)}"))
    version = lock.get("prediction_version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        issues.append((freeze_id, "prediction_version must be positive integer"))
    parent = lock.get("parent_freeze_id")
    if parent is not None and not base.nonempty_text(parent):
        issues.append((freeze_id, "parent_freeze_id must be null or non-empty text"))
    issued = _utc(freeze_id, "prediction_issued_at_utc", lock.get("prediction_issued_at_utc"), issues)
    cutoff = _utc(freeze_id, "information_cutoff_at_utc", lock.get("information_cutoff_at_utc"), issues)
    if issued is not None and cutoff is not None and cutoff > issued:
        issues.append((freeze_id, "information cutoff must not be after prediction issue"))
    channels = lock.get("allowed_information_channels")
    if not isinstance(channels, list) or not channels or any(not base.nonempty_text(x) for x in channels) or len(channels) != len(set(channels)):
        issues.append((freeze_id, "allowed_information_channels must be non-empty unique string array"))
    if lock.get("primary_scoring_policy") not in PRIMARY_SCORING_POLICIES:
        issues.append((freeze_id, f"primary_scoring_policy must be one of {sorted(PRIMARY_SCORING_POLICIES)}"))
    if lock.get("scoring_eligibility") not in SCORING_ELIGIBILITIES:
        issues.append((freeze_id, f"scoring_eligibility must be one of {sorted(SCORING_ELIGIBILITIES)}"))
    return issues


def primary_scoring_freeze(rows, observed_at=None):
    ordered = sorted(rows, key=lambda row: lock_of(row).get("prediction_version") if isinstance(lock_of(row), dict) else 10**9)
    if not ordered:
        return None
    first_lock = lock_of(ordered[0]) or {}
    policy = first_lock.get("primary_scoring_policy")
    eligible = []
    for row in ordered:
        lock = lock_of(row) or {}
        issued = base.utc_value(lock.get("prediction_issued_at_utc"))
        if lock.get("scoring_eligibility") != "SCORABLE_PRE_OUTCOME":
            continue
        if observed_at is not None and issued is not None and issued >= observed_at:
            continue
        eligible.append(row)
    if not eligible:
        return None
    if policy == "FIRST_ISSUED":
        return eligible[0]
    if policy == "LATEST_PRE_OUTCOME_CUTOFF":
        return max(
            eligible,
            key=lambda row: (
                base.utc_value((lock_of(row) or {}).get("information_cutoff_at_utc")),
                (lock_of(row) or {}).get("prediction_version", 0),
            ),
        )
    return None


def validate_revision_semantics(plans, batches, freezes, outcomes):
    issues = []
    plan_by_id = {row.get("plan_id"): row for row in plans}
    batch_by_id = {row.get("batch_id"): row for row in batches}
    freeze_by_id = {row.get("freeze_id"): row for row in freezes}

    for plan in plans:
        required = plan.get("freeze_required_fields")
        if not isinstance(required, list) or REVISION_FIELD not in required:
            issues.append((plan.get("plan_id") or "<missing>", "freeze_required_fields missing revision_lock"))

    unique_counts = unique_case_count_by_batch(freezes)
    for batch_id, count in unique_counts.items():
        batch = batch_by_id.get(batch_id) or {}
        planned = batch.get("planned_case_count")
        if isinstance(planned, int) and not isinstance(planned, bool) and count > planned:
            issues.append((batch_id or "<missing>", "unique preregistered case count exceeds planned_case_count"))

    outcomes_by_case = {}
    for outcome in outcomes:
        freeze = freeze_by_id.get(outcome.get("freeze_id"))
        if freeze is not None:
            outcomes_by_case.setdefault(case_key(freeze), []).append(outcome)

    for key, rows in case_groups(freezes).items():
        batch_id, case_id = key
        owner = f"{batch_id or '<missing>'}/{case_id or '<missing>'}"
        plan_ids = {row.get("plan_id") for row in rows}
        if len(plan_ids) != 1:
            issues.append((owner, "all prediction versions for one case must bind one plan_id"))
        plan = plan_by_id.get(next(iter(plan_ids), None))
        if plan is not None and REVISION_FIELD not in (plan.get("freeze_required_fields") or []):
            continue

        for row in rows:
            issues.extend(_validate_lock(row.get("freeze_id") or owner, lock_of(row)))

        valid_rows = [row for row in rows if isinstance(lock_of(row), dict) and isinstance(lock_of(row).get("prediction_version"), int)]
        ordered = sorted(valid_rows, key=lambda row: lock_of(row)["prediction_version"])
        versions = [lock_of(row)["prediction_version"] for row in ordered]
        if versions and versions != list(range(1, len(versions) + 1)):
            issues.append((owner, "prediction versions must be contiguous from 1"))
        if len(versions) != len(set(versions)):
            issues.append((owner, "prediction_version must be unique within case"))

        base_channels = None
        base_policy = None
        previous = None
        previous_issued = None
        previous_cutoff = None
        for index, row in enumerate(ordered):
            lock = lock_of(row)
            freeze_id = row.get("freeze_id") or owner
            version = lock.get("prediction_version")
            if index == 0:
                if version == 1 and lock.get("parent_freeze_id") is not None:
                    issues.append((freeze_id, "prediction version 1 parent_freeze_id must be null"))
                base_channels = lock.get("allowed_information_channels")
                base_policy = lock.get("primary_scoring_policy")
            else:
                if lock.get("parent_freeze_id") != previous.get("freeze_id"):
                    issues.append((freeze_id, "parent_freeze_id must bind previous immutable version"))
                if lock.get("allowed_information_channels") != base_channels:
                    issues.append((freeze_id, "allowed information channels cannot expand or change across revisions"))
                if lock.get("primary_scoring_policy") != base_policy:
                    issues.append((freeze_id, "primary_scoring_policy cannot change across revisions"))
            issued = base.utc_value(lock.get("prediction_issued_at_utc"))
            cutoff = base.utc_value(lock.get("information_cutoff_at_utc"))
            frozen_at = base.utc_value(row.get("frozen_at_utc"))
            if issued is not None and frozen_at is not None and issued != frozen_at:
                issues.append((freeze_id, "prediction_issued_at_utc must equal immutable freeze timestamp"))
            if previous_issued is not None and issued is not None and issued <= previous_issued:
                issues.append((freeze_id, "prediction issue time must increase across revisions"))
            if previous_cutoff is not None and cutoff is not None and cutoff < previous_cutoff:
                issues.append((freeze_id, "information cutoff cannot move backward across revisions"))
            previous = row
            previous_issued = issued
            previous_cutoff = cutoff

        case_outcomes = outcomes_by_case.get(key, [])
        if len(case_outcomes) > 1:
            issues.append((owner, "one preregistered case may retain only one scored outcome"))
        if case_outcomes:
            outcome = case_outcomes[0]
            observed_at = base.utc_value(outcome.get("observed_at_utc"))
            for row in ordered:
                lock = lock_of(row)
                issued = base.utc_value(lock.get("prediction_issued_at_utc"))
                eligibility = lock.get("scoring_eligibility")
                if observed_at is not None and issued is not None:
                    if issued >= observed_at and eligibility != "AUDIT_ONLY_POST_OUTCOME":
                        issues.append((row.get("freeze_id") or owner, "outcome-visible revision must be AUDIT_ONLY_POST_OUTCOME"))
                    if issued < observed_at and eligibility == "AUDIT_ONLY_POST_OUTCOME":
                        issues.append((row.get("freeze_id") or owner, "pre-outcome revision cannot be marked AUDIT_ONLY_POST_OUTCOME"))
            primary = primary_scoring_freeze(ordered, observed_at)
            if primary is None:
                issues.append((owner, "no primary scorable prediction version available for outcome"))
            elif outcome.get("freeze_id") != primary.get("freeze_id"):
                issues.append((outcome.get("outcome_id") or owner, "outcome binds non-primary scoring version"))

    return issues


def validate_records(distillates, plans, batches, freezes, outcomes):
    base_issues = list(base.validate_records(distillates, plans, batches, freezes, outcomes))
    issues = filter_legacy_counting_issues(base_issues, freezes, batches)
    issues.extend(hardening.validate_hardening(distillates, plans, batches, freezes, outcomes))
    issues.extend(validate_revision_semantics(plans, batches, freezes, outcomes))
    return issues


def fail(message):
    print(f"k2-versioned-preoutcome-revision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    project = base.load_json(K / "PROJECT_STATE.json")
    if project.get("phase") != "K2_EVIDENCE_EXTRACTION":
        fail("validator only valid during K2_EVIDENCE_EXTRACTION")
    if project.get("claim_extraction_blocked") is not True:
        fail("Claim Extraction must remain blocked")
    distillates = base.load_work_family_distillates(ROOT)
    plans = base.load_jsonl(K / "K2_PROSPECTIVE_TEST_PLANS.jsonl")
    batches = base.load_jsonl(K / "K2_PROSPECTIVE_BATCHES.jsonl")
    freezes = base.load_jsonl(K / "K2_PROSPECTIVE_FREEZES.jsonl")
    outcomes = base.load_jsonl(K / "K2_PROSPECTIVE_OUTCOMES.jsonl")
    issues = validate_records(distillates, plans, batches, freezes, outcomes)
    if issues:
        fail(f"issues={len(issues)} first={issues[0][0]}: {issues[0][1]}")
    print("k2-versioned-preoutcome-revision: PASS")
    print(f"plans={len(plans)} batches={len(batches)} freezes={len(freezes)} outcomes={len(outcomes)} issues=0")
    print("case_denominator=UNIQUE_BATCH_CASE_ID")
    print("versioned_preoutcome_revision=IMPLEMENTED")
    print("empirical_credit_upgrade_blocked=true")


if __name__ == "__main__":
    main()
