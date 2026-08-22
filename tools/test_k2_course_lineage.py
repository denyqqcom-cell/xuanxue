#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_k2_course_lineage as v

def src(sid="QM-SRC-0001"):
    return {"source_id":sid,"domain":"qimen"}

def work(sid="QM-SRC-0001",wid="WORK-1"):
    return {"source_id":sid,"work_id":wid}

def row(**o):
    r={
      "course_family_id":"COURSE-QM-1","domain":"qimen","source_id":"QM-SRC-0001","work_id":"WORK-1",
      "relation_scope":"COURSE_PROVENANCE","course_role":"FOUNDATION",
      "dependence_class":"SAME_TEACHING_PROVENANCE","independent_vote_allowed":False,
      "related_source_ids":["QM-SRC-0002"],"lineage_basis":"CONTENT_VERIFIED",
      "lineage_evidence":"shared course structure confirmed by full reading","review_status":"REVIEWED","notes":None
    }
    r.update(o);return r

def main():
    assert not v.inspect(row(),src(),work())
    issues=v.inspect(row(independent_vote_allowed=True),src(),work())
    assert any("independent vote" in msg for _,msg in issues),issues
    issues=v.inspect(row(course_role="SYNOPSIS_COMPENDIUM"),src(),work())
    assert any("SYNOPSIS_COMPENDIUM" in msg for _,msg in issues),issues

    sources={"QM-SRC-0001":src(),"QM-SRC-0002":src("QM-SRC-0002")}
    works={"QM-SRC-0001":work(),"QM-SRC-0002":work("QM-SRC-0002","WORK-2")}
    rows=[
      row(),
      row(source_id="QM-SRC-0002",work_id="WORK-2",course_role="ADVANCED_EXTENSION",
          related_source_ids=["QM-SRC-0001"])
    ]
    assert not v.validate_rows(sources,works,rows),v.validate_rows(sources,works,rows)

    bad=[rows[0],dict(rows[1],work_id="WORK-1")]
    issues=v.validate_rows(sources,works,bad)
    assert any("distinct work_ids" in msg for _,msg in issues),issues

    bad=[rows[0],dict(rows[1],related_source_ids=["QM-SRC-9999"])]
    issues=v.validate_rows(sources,works,bad)
    assert any("outside course family" in msg for _,msg in issues),issues
    print("k2-course-lineage-tests: PASS")

if __name__=="__main__":main()
