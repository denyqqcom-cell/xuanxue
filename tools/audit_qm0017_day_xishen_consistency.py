#!/usr/bin/env python3
"""Audit QM-SRC-0017's stated day-Xishen rule against its printed examples.

The audit is source-internal only: pdf:p282 supplies the stated mapping and
pdf:p294-p306 supply consecutive printed day-example titles. Agreement is
structural/textual consistency inside this carrier, not empirical validation.
"""

STEMS=set("甲乙丙丁戊己庚辛壬癸")
PALACES={"艮","乾","坤","离","巽"}


def _validate_fixture(data):
    if data.get("schema_version")!="k2-source-internal-consistency-fixture-v1":
        raise ValueError("unexpected fixture schema_version")
    if data.get("scope")!="SOURCE_INTERNAL_RULE_VS_EXAMPLE_ONLY":
        raise ValueError("fixture scope must remain source-internal only")
    if data.get("empirical_credit")!="NONE" or data.get("claim_extraction_blocked") is not True:
        raise ValueError("fixture escaped empirical/Claim boundary")

    rules=data.get("stated_rule_by_day_stem")
    if not isinstance(rules,dict) or set(rules)!=STEMS:
        raise ValueError("stated_rule_by_day_stem must cover exactly ten stems")
    if any(p not in PALACES for p in rules.values()):
        raise ValueError("invalid Xishen palace in stated rule")

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
        if row.get("observed_xishen_palace") not in PALACES:
            raise ValueError(f"invalid observed Xishen palace for {cid}")
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
        expected=rules[row["day_ganzhi"][0]]
        observed=row["observed_xishen_palace"]
        if expected!=observed:
            mismatches[cid]={"expected_palace":expected,"observed_palace":observed}
        else:
            matching+=1

    if mismatches:
        interpretation="SOURCE_INTERNAL_TENSION"
        resolution="CONTEXT_REQUIRED"
    else:
        interpretation="SOURCE_INTERNAL_CONSISTENT_IN_FIXTURE"
        resolution="NO_TENSION_IN_FIXTURE"

    return {
        "source_id":data["source_id"],
        "topic":data["topic"],
        "cases_checked":len(data["examples"]),
        "matching_cases":matching,
        "mismatch_cases":len(mismatches),
        "mismatches":mismatches,
        "interpretation_status":interpretation,
        "resolution_status":resolution,
        "empirical_credit":"NONE",
        "claim_extraction_blocked":True,
    }
