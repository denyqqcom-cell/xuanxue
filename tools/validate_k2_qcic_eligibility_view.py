#!/usr/bin/env python3
import json,sys
from pathlib import Path
from generate_k2_qcic_eligibility_view import ROOT,OUT,actual_view,render_view,SCHEMA_VERSION

TOP_KEYS={"schema_version","generated_from","claim_extraction_blocked","empirical_credit","source_summaries","stance_topics","enumeration_units"}
SUMMARY_KEYS={"source_id","stance_topic_count","author_method_candidate_count","excluded_stance_topic_count","held_stance_topic_count","collapsed_enumerated_entries","effective_structure_units","empirical_evidence_units","claim_eligible"}
STANCE_KEYS={"source_id","work_id","topic_key","effective_stance_id","stance","author_method_pool_eligible","inference_eligibility","evidence_locators","claim_eligible"}
ENUM_KEYS={"source_id","work_id","compression_id","generative_rule_id","method_layer","enumerated_entries_count","effective_structure_units","empirical_evidence_units","reconstruction_test_status","inference_eligibility","claim_eligible"}

def fail(msg):
    print(f"k2-qcic-eligibility-view: FAIL: {msg}",file=sys.stderr);raise SystemExit(1)

def validate_shape(view):
    issues=[]
    if not isinstance(view,dict):return ["view must be object"]
    if set(view)!=TOP_KEYS:issues.append(f"top-level keys mismatch: {sorted(set(view)^TOP_KEYS)}")
    if view.get("schema_version")!=SCHEMA_VERSION:issues.append("schema_version mismatch")
    if view.get("claim_extraction_blocked") is not True:issues.append("claim_extraction_blocked must be true")
    if view.get("empirical_credit")!="NONE":issues.append("empirical_credit must be NONE")
    gf=view.get("generated_from")
    if not isinstance(gf,list) or len(gf)!=len(set(gf)) or len(gf)<3:issues.append("generated_from must be unique list")
    for key,required in (("source_summaries",SUMMARY_KEYS),("stance_topics",STANCE_KEYS),("enumeration_units",ENUM_KEYS)):
        rows=view.get(key)
        if not isinstance(rows,list):issues.append(f"{key} must be array");continue
        for i,r in enumerate(rows):
            if not isinstance(r,dict) or set(r)!=required:issues.append(f"{key}[{i}] keys mismatch")
            if isinstance(r,dict) and r.get("claim_eligible") is not False:issues.append(f"{key}[{i}] claim_eligible must be false")
    return issues

def main():
    if not OUT.exists():fail(f"missing generated view: {OUT.relative_to(ROOT)}")
    try:stored=json.loads(OUT.read_text(encoding="utf-8"))
    except Exception as e:fail(f"invalid generated JSON: {e}")
    issues=validate_shape(stored)
    if issues:fail("; ".join(issues[:20]))
    expected=render_view(actual_view(ROOT))
    actual=OUT.read_text(encoding="utf-8")
    if actual!=expected:fail("generated eligibility view is stale; run tools/generate_k2_qcic_eligibility_view.py --write")
    print("k2-qcic-eligibility-view: PASS")
    print(f"sources={len(stored['source_summaries'])} stance_topics={len(stored['stance_topics'])} enumeration_units={len(stored['enumeration_units'])} claim_extraction_blocked=true")
if __name__=="__main__":main()
