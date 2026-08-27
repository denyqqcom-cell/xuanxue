#!/usr/bin/env python3
"""Audit QM-SRC-0017 五不遇时 stated rule against its own printed examples.

This stays strictly source-internal: pdf:p284 is compared with the printed
examples at pdf:p294-p306. A match only establishes carrier-internal consistency
within the frozen fixture; it does not establish traditional canonicality or
real-world predictive validity.
"""

STEMS=set("甲乙丙丁戊己庚辛壬癸")
BRANCHES=set("子丑寅卯辰巳午未申酉戌亥")

def _valid_ganzhi(value):
    return isinstance(value,str) and len(value)==2 and value[0] in STEMS and value[1] in BRANCHES

def _validate_fixture(data):
    if data.get("schema_version")!="k2-source-internal-consistency-fixture-v1":
        raise ValueError("unexpected fixture schema_version")
    if data.get("scope")!="SOURCE_INTERNAL_RULE_VS_EXAMPLE_ONLY":
        raise ValueError("fixture scope must remain source-internal only")
    if data.get("interpretation_status")!="SOURCE_INTERNAL_CONSISTENT_IN_FIXTURE":
        raise ValueError("fixture must preserve source-internal consistency status")
    if data.get("resolution_status")!="NO_TENSION_IN_FIXTURE":
        raise ValueError("consistent fixture must use NO_TENSION_IN_FIXTURE")
    if data.get("empirical_credit")!="NONE" or data.get("claim_extraction_blocked") is not True:
        raise ValueError("fixture escaped empirical/Claim boundary")

    rules=data.get("stated_rule_by_day_stem")
    if not isinstance(rules,dict) or set(rules)!=STEMS:
        raise ValueError("stated_rule_by_day_stem must cover exactly ten stems")
    for stem,hours in rules.items():
        if not isinstance(hours,list) or len(hours) not in {1,2} or len(hours)!=len(set(hours)) or any(not _valid_ganzhi(x) for x in hours):
            raise ValueError(f"invalid stated 五不遇时 hours for {stem}")
        if any(x[0] == stem for x in hours):
            raise ValueError(f"五不遇时 hour stem must not equal day stem for {stem}")

    examples=data.get("examples")
    if not isinstance(examples,list) or not examples:
        raise ValueError("examples must be non-empty")
    ids=set()
    for row in examples:
        cid=row.get("case_id")
        if not isinstance(cid,str) or not cid or cid in ids:
            raise ValueError("case_id must be unique non-empty string")
        ids.add(cid)
        day=row.get("day_ganzhi")
        if not _valid_ganzhi(day):
            raise ValueError(f"invalid day_ganzhi for {cid}")
        observed=row.get("observed_wubuyushi_hour_ganzhi")
        if not isinstance(observed,list) or len(observed)!=len(set(observed)) or any(not _valid_ganzhi(x) for x in observed):
            raise ValueError(f"invalid observed 五不遇时 hours for {cid}")
        locs=row.get("source_checkpoints")
        if not isinstance(locs,list) or not locs or any(not isinstance(x,str) or not x.startswith("pdf:p") for x in locs):
            raise ValueError(f"source checkpoints required for {cid}")

def audit_fixture(data):
    _validate_fixture(data)
    rules=data["stated_rule_by_day_stem"]
    mismatches={}
    matching=0
    for row in data["examples"]:
        cid=row["case_id"]
        stem=row["day_ganzhi"][0]
        expected=rules[stem]
        observed=row["observed_wubuyushi_hour_ganzhi"]
        missing=[x for x in expected if x not in observed]
        unexpected=[x for x in observed if x not in expected]
        if missing or unexpected:
            mismatches[cid]={"missing_expected":missing,"unexpected_present":unexpected}
        else:
            matching+=1
    return {
        "source_id":data["source_id"],
        "topic":data["topic"],
        "cases_checked":len(data["examples"]),
        "matching_cases":matching,
        "mismatch_cases":len(mismatches),
        "mismatches":mismatches,
        "interpretation_status":"SOURCE_INTERNAL_TENSION" if mismatches else "SOURCE_INTERNAL_CONSISTENT_IN_FIXTURE",
        "resolution_status":"CONTEXT_REQUIRED" if mismatches else "NO_TENSION_IN_FIXTURE",
        "empirical_credit":"NONE",
        "claim_extraction_blocked":True,
    }
