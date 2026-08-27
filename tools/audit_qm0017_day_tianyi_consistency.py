#!/usr/bin/env python3
"""Audit one QM-SRC-0017 source-internal rule/example relationship.

This is deliberately not a traditional-canonicality resolver. It compares only
what the same carrier states at pdf:p282-p283 with what its printed examples
mark at pdf:p294-p306. Any mismatch stays a source-internal tension and is not
silently repaired from external knowledge.
"""

BRANCHES=set("子丑寅卯辰巳午未申酉戌亥")
STEMS=set("甲乙丙丁戊己庚辛壬癸")

def _validate_fixture(data):
    if data.get("schema_version")!="k2-source-internal-consistency-fixture-v1":
        raise ValueError("unexpected fixture schema_version")
    if data.get("scope")!="SOURCE_INTERNAL_RULE_VS_EXAMPLE_ONLY":
        raise ValueError("fixture scope must remain source-internal only")
    if data.get("interpretation_status")!="SOURCE_INTERNAL_TENSION":
        raise ValueError("fixture must preserve source-internal tension status")
    if data.get("resolution_status")!="CONTEXT_REQUIRED":
        raise ValueError("fixture must remain CONTEXT_REQUIRED")
    if data.get("empirical_credit")!="NONE" or data.get("claim_extraction_blocked") is not True:
        raise ValueError("fixture escaped empirical/Claim boundary")

    rules=data.get("stated_rule_by_day_stem")
    if not isinstance(rules,dict) or set(rules)!=STEMS:
        raise ValueError("stated_rule_by_day_stem must cover exactly ten stems")
    for stem,branches in rules.items():
        if not isinstance(branches,list) or len(branches)!=2 or len(set(branches))!=2 or any(b not in BRANCHES for b in branches):
            raise ValueError(f"invalid stated Tianyi branches for {stem}")

    examples=data.get("examples")
    if not isinstance(examples,list) or not examples:
        raise ValueError("examples must be non-empty")
    ids=set()
    for row in examples:
        cid=row.get("case_id")
        if not isinstance(cid,str) or not cid or cid in ids:
            raise ValueError("case_id must be unique non-empty string")
        ids.add(cid)
        ganzhi=row.get("day_ganzhi")
        if not isinstance(ganzhi,str) or len(ganzhi)!=2 or ganzhi[0] not in STEMS:
            raise ValueError(f"invalid day_ganzhi for {cid}")
        observed=row.get("observed_tianyi_hour_branches")
        if not isinstance(observed,list) or len(observed)!=len(set(observed)) or any(b not in BRANCHES for b in observed):
            raise ValueError(f"invalid observed Tianyi branches for {cid}")
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
        observed=row["observed_tianyi_hour_branches"]
        missing=[b for b in expected if b not in observed]
        unexpected=[b for b in observed if b not in expected]
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
