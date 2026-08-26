#!/usr/bin/env python3
import json,tempfile
from pathlib import Path

from generate_k2_unknown_textual_backlog import raw_unknown_ids,validate_corrections


def write_jsonl(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n" for r in rows),encoding="utf-8")


def base_row(**updates):
    row={
        "routing_id":"R-A",
        "source_id":"A",
        "canonical_sha256":"a"*64,
        "routing_mode":"SOURCE_WIDE",
        "raw_knowledge_domains":["UNKNOWN"],
        "resolved_routes":["qimen"],
        "routing_basis":"DEEP_VISUAL_REVIEW",
        "evidence_locators":["pdf:p2"],
        "segment_ids":[],
        "review_status":"REVIEWED",
        "empirical_credit":"NONE",
        "claim_extraction_blocked":True,
    }
    row.update(updates);return row


def main():
    sources={
        "A":{"source_id":"A","file_sha256":"a"*64,"evidence_role":"TEXTUAL_SOURCE","knowledge_domains":["UNKNOWN"]},
        "B":{"source_id":"B","file_sha256":"b"*64,"evidence_role":"TEXTUAL_SOURCE","knowledge_domains":["UNKNOWN"]},
        "C":{"source_id":"C","file_sha256":"c"*64,"evidence_role":"TEXTUAL_SOURCE","knowledge_domains":["qimen"]},
    }
    assert raw_unknown_ids(sources)=={"A","B"}

    with tempfile.TemporaryDirectory() as td:
        root=Path(td);k=root/"knowledge";k.mkdir()
        write_jsonl(k/"K2_DEEP_READING_LEDGER.jsonl",[
            {"source_id":"A","read_status":"COMPLETE","verification_mode":"VISUAL_PAGE","page_end":10},
            {"source_id":"B","read_status":"COMPLETE","verification_mode":"VISUAL_PAGE","page_end":20},
        ])
        write_jsonl(k/"K2_SOURCE_SEGMENTS.jsonl",[
            {"source_id":"B","segment_id":"B#1","review_status":"REVIEWED","verification_mode":"VISUAL_PAGE","domain_routes":["qimen"]},
            {"source_id":"B","segment_id":"B#2","review_status":"REVIEWED","verification_mode":"VISUAL_PAGE","domain_routes":["OUT_OF_SCOPE"]},
        ])

        source_wide=base_row()
        assert validate_corrections(root,sources,[source_wide])==[]

        segmented=base_row(
            routing_id="R-B",source_id="B",canonical_sha256="b"*64,
            routing_mode="SEGMENTED",routing_basis="SEGMENT_REGISTRY_VISUAL_REVIEW",
            resolved_routes=["OUT_OF_SCOPE","qimen"],evidence_locators=["pdf:p1","pdf:p11"],segment_ids=["B#1","B#2"],
        )
        assert validate_corrections(root,sources,[segmented])==[]

        bad=base_row(claim_extraction_blocked=False)
        assert any("Claim Extraction" in m or "claim_extraction_blocked" in m for _,m in validate_corrections(root,sources,[bad]))

        bad=base_row(source_id="C",canonical_sha256="c"*64)
        assert any("raw TEXTUAL_SOURCE" in m for _,m in validate_corrections(root,sources,[bad]))

        bad=dict(segmented);bad["segment_ids"]=["B#1"]
        assert any("full registered segment set" in m for _,m in validate_corrections(root,sources,[bad]))

        bad=dict(segmented);bad["resolved_routes"]=["qimen"]
        assert any("segment route union" in m for _,m in validate_corrections(root,sources,[bad]))

        bad=base_row(evidence_locators=["pdf:p99"])
        assert any("outside deep review" in m for _,m in validate_corrections(root,sources,[bad]))

    print("k2-semantic-discovery-routing-tests: PASS")


if __name__=="__main__":main()
