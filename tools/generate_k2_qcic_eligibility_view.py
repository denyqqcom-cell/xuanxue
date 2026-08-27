#!/usr/bin/env python3
import argparse,json,sys
from collections import defaultdict
from pathlib import Path

from validate_k2_source_stance import (
    validate_rows as validate_stance_rows,
    coverage_issues as stance_coverage_issues,
    effective_stance_rows,
    source_index as stance_source_index,
    lineage_index as stance_lineage_index,
    deep_reading_index as stance_deep_reading_index,
)
from validate_k2_enumeration_compression import (
    validate_rows as validate_enum_rows,
    coverage_issues as enum_coverage_issues,
    reconstruction_result_issues,
    source_index as enum_source_index,
    lineage_index as enum_lineage_index,
    deep_reading_index as enum_deep_reading_index,
)

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"
OUT=K/"K2_QCIC_INFERENCE_ELIGIBILITY_VIEW.json"
SCHEMA_VERSION="k2-qcic-inference-eligibility-v1"
GENERATED_FROM=[
    "knowledge/K2_QCIC_V06_GATE_STATE.json",
    "knowledge/K2_SOURCE_STANCE_REGISTRY.jsonl",
    "knowledge/K2_ENUMERATION_COMPRESSION_REGISTRY.jsonl",
    "knowledge/K2_ENUMERATION_RECONSTRUCTION_RESULTS.jsonl",
]

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path):
    rows=[]
    if not path.exists():
        raise ValueError(f"missing required JSONL: {path.relative_to(ROOT)}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():rows.append(json.loads(raw))
    return rows

def validated_inputs(root=ROOT):
    k=root/"knowledge"
    state=load_json(k/"K2_QCIC_V06_GATE_STATE.json")
    stances=load_jsonl(k/"K2_SOURCE_STANCE_REGISTRY.jsonl")
    enums=load_jsonl(k/"K2_ENUMERATION_COMPRESSION_REGISTRY.jsonl")
    recon_results=load_jsonl(k/"K2_ENUMERATION_RECONSTRUCTION_RESULTS.jsonl")
    issues=[]
    issues.extend(validate_stance_rows(stance_source_index(root),stance_lineage_index(root),stance_deep_reading_index(root),stances))
    issues.extend(stance_coverage_issues(stances,state))
    issues.extend(validate_enum_rows(enum_source_index(root),enum_lineage_index(root),enum_deep_reading_index(root),enums))
    issues.extend(enum_coverage_issues(enums,state))
    issues.extend(reconstruction_result_issues(enums,recon_results))
    if issues:
        raise ValueError("invalid QCIC gate inputs: "+"; ".join(f"{a}: {b}" for a,b in issues[:20]))
    return state,stances,enums

def stance_eligibility(row):
    stance=row["stance"];eligible=row["author_method_pool_eligible"]
    if stance=="SOURCE_ENDORSES" and eligible:
        return "ALLOW_SOURCE_LOCAL_CANDIDATE"
    if stance=="SOURCE_ENDORSES":
        return "EXCLUDE_NOT_AUTHOR_METHOD_POOL"
    if stance=="SOURCE_REPORTS":
        return "EXCLUDE_SOURCE_REPORTS_ONLY"
    if stance=="SOURCE_REJECTS":
        return "EXCLUDE_SOURCE_REJECTED"
    if stance=="SOURCE_UNCERTAIN":
        return "HOLD_SOURCE_UNCERTAIN"
    raise ValueError(f"unsupported stance {stance}")

def enum_eligibility(row):
    status=row["reconstruction_test_status"]
    if status=="PASS":return "STRUCTURE_ONLY_RECONSTRUCTION_PASS"
    if status=="UNTESTED":return "STRUCTURE_ONLY_RECONSTRUCTION_UNTESTED"
    if status=="FAIL":return "HOLD_STRUCTURE_RECONSTRUCTION_FAILED"
    raise ValueError(f"unsupported reconstruction status {status}")

def build_view(state,stance_rows,enum_rows):
    effective=effective_stance_rows(stance_rows)
    stance_topics=[]
    for r in effective:
        stance_topics.append({
            "author_method_pool_eligible":r["author_method_pool_eligible"],
            "claim_eligible":False,
            "effective_stance_id":r["stance_id"],
            "evidence_locators":list(r["evidence_locators"]),
            "inference_eligibility":stance_eligibility(r),
            "source_id":r["source_id"],
            "stance":r["stance"],
            "topic_key":r["topic_key"],
            "work_id":r["work_id"],
        })
    stance_topics.sort(key=lambda r:(r["source_id"],r["topic_key"],r["effective_stance_id"]))

    enumeration_units=[]
    for r in sorted(enum_rows,key=lambda x:(x["source_id"],x["generative_rule_id"],x["compression_id"])):
        enumeration_units.append({
            "claim_eligible":False,
            "compression_id":r["compression_id"],
            "effective_structure_units":r["collapsed_structure_units"],
            "empirical_evidence_units":r["empirical_evidence_units"],
            "enumerated_entries_count":r["enumerated_entries_count"],
            "generative_rule_id":r["generative_rule_id"],
            "inference_eligibility":enum_eligibility(r),
            "method_layer":r["method_layer"],
            "reconstruction_test_status":r["reconstruction_test_status"],
            "source_id":r["source_id"],
            "work_id":r["work_id"],
        })

    topics_by_source=defaultdict(list);enum_by_source=defaultdict(list)
    for r in stance_topics:topics_by_source[r["source_id"]].append(r)
    for r in enumeration_units:enum_by_source[r["source_id"]].append(r)
    summaries=[]
    for target in sorted(state["targets"],key=lambda t:t["source_id"]):
        sid=target["source_id"];topics=topics_by_source[sid];enums=enum_by_source[sid]
        summaries.append({
            "author_method_candidate_count":sum(1 for r in topics if r["inference_eligibility"]=="ALLOW_SOURCE_LOCAL_CANDIDATE"),
            "claim_eligible":False,
            "collapsed_enumerated_entries":sum(r["enumerated_entries_count"] for r in enums),
            "effective_structure_units":sum(r["effective_structure_units"] for r in enums),
            "empirical_evidence_units":sum(r["empirical_evidence_units"] for r in enums),
            "excluded_stance_topic_count":sum(1 for r in topics if r["inference_eligibility"].startswith("EXCLUDE_")),
            "held_stance_topic_count":sum(1 for r in topics if r["inference_eligibility"].startswith("HOLD_")),
            "source_id":sid,
            "stance_topic_count":len(topics),
        })

    return {
        "claim_extraction_blocked":True,
        "empirical_credit":"NONE",
        "enumeration_units":enumeration_units,
        "generated_from":list(GENERATED_FROM),
        "schema_version":SCHEMA_VERSION,
        "source_summaries":summaries,
        "stance_topics":stance_topics,
    }

def render_view(view):
    return json.dumps(view,ensure_ascii=False,sort_keys=True,indent=2)+"\n"

def actual_view(root=ROOT):
    state,stances,enums=validated_inputs(root)
    return build_view(state,stances,enums)

def main():
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write",action="store_true")
    g.add_argument("--stdout",action="store_true")
    args=p.parse_args()
    text=render_view(actual_view(ROOT))
    if args.write:
        OUT.write_text(text,encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)}")
    else:
        sys.stdout.write(text)
if __name__=="__main__":main()
