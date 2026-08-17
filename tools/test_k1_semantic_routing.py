#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_k1_semantic_routing as v


def base(**overrides):
    row = {
        "source_id": "BZ-SRC-0001",
        "domain": "bazi",
        "knowledge_domains": ["bazi"],
        "domain_basis": "TITLE_FILENAME",
        "domain_evidence": "title contains 八字",
        "title": "八字基础",
        "author": "UNKNOWN",
        "author_basis": "UNKNOWN",
        "source_type": "BOOK",
    }
    row.update(overrides)
    return row


def main():
    assert not v.inspect_row(base(), "bazi")

    issues = v.inspect_row(base(title="梁湘润-火珠林密本（古本）", knowledge_domains=["bazi"], domain_evidence="folder says bazi"), "bazi")
    assert any("liuyao" in msg for _, msg in issues), issues

    issues = v.inspect_row(base(source_id="FS-SRC-0012", domain="fengshui", title="揭露铁板神数之内幕", knowledge_domains=["fengshui"], domain_evidence="folder says fengshui"), "fengshui")
    assert any("out-of-scope" in msg for _, msg in issues), issues

    issues = v.inspect_row(base(source_id="LR-SRC-0001", domain="liuren", title="袁树珊撰 谢路军主编 邓同校", author="袁树珊 / 谢路军 / 邓同", author_basis="FILENAME", knowledge_domains=["liuren"], domain_evidence="title contains 六壬"), "liuren")
    assert any("non-author contributor" in msg for _, msg in issues), issues

    issues = v.inspect_row(base(knowledge_domains=None, domain_basis=None, domain_evidence=None), "bazi")
    assert any("knowledge_domains" in msg for _, msg in issues), issues

    print("k1-semantic-routing-tests: PASS")


if __name__ == "__main__":
    main()
