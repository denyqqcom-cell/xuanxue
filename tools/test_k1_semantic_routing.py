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

    issues = v.inspect_row(
        base(
            title="梁湘润-火珠林密本（古本）",
            author="梁湘润",
            author_basis="FILENAME",
            knowledge_domains=["bazi"],
            domain_evidence="folder says bazi",
        ),
        "bazi",
    )
    assert any("liuyao" in msg for _, msg in issues), issues

    issues = v.inspect_row(
        base(
            source_id="FS-SRC-0012",
            domain="fengshui",
            title="揭露铁板神数之内幕",
            knowledge_domains=["fengshui"],
            domain_evidence="folder says fengshui",
        ),
        "fengshui",
    )
    assert any("out-of-scope" in msg for _, msg in issues), issues

    issues = v.inspect_row(
        base(
            source_id="LR-SRC-0001",
            domain="liuren",
            title="大六壬探原 袁树珊撰 谢路军主编 邓同校",
            author="袁树珊 / 谢路军 / 邓同",
            author_basis="FILENAME",
            knowledge_domains=["liuren"],
            domain_evidence="title contains 六壬",
        ),
        "liuren",
    )
    assert any("non-author contributor" in msg for _, msg in issues), issues

    issues = v.inspect_row(base(knowledge_domains=None, domain_basis=None, domain_evidence=None), "bazi")
    assert any("knowledge_domains" in msg for _, msg in issues), issues

    # Author names can contain domain words. 紫微杨 is an author token, not
    # evidence that a work named 清室气数录 belongs to ziwei.
    issues = v.inspect_row(
        base(
            source_id="ZW-SRC-0028",
            domain="ziwei",
            title="紫微杨+《清室气数录》b",
            author="紫微杨",
            author_basis="FILENAME",
            knowledge_domains=["ziwei"],
            domain_evidence="title contains ziwei system token",
        ),
        "ziwei",
    )
    assert any("lacks matching work-title signal" in msg for _, msg in issues), issues

    # The same author prefix must not prevent a genuine fengshui work-title
    # signal from being recognized once the author token is removed.
    row = base(
        source_id="ZW-SRC-0030",
        domain="ziwei",
        title="紫微杨+《破解大清风水密码》b",
        author="紫微杨",
        author_basis="FILENAME",
        knowledge_domains=["fengshui"],
        domain_basis="TITLE_FILENAME",
        domain_evidence="work title contains 风水",
    )
    assert not v.inspect_row(row, "ziwei"), v.inspect_row(row, "ziwei")

    # Legacy mixed Chinese/pinyin filenames still carry an explicit ziwei work-title signal.
    row = base(
        source_id="ZW-SRC-0020",
        domain="ziwei",
        title="王亭之-紫wei斗shu讲义补注(上册)",
        author="王亭之",
        author_basis="FILENAME",
        knowledge_domains=["ziwei"],
        domain_evidence="title contains ziwei system token",
    )
    assert not v.inspect_row(row, "ziwei"), v.inspect_row(row, "ziwei")

    # Code identifiers can be direct filename evidence when they explicitly name a domain.
    row = base(
        source_id="ZW-SRC-0130",
        domain="ziwei",
        title="BaziRulesTest",
        author="UNKNOWN",
        author_basis="UNKNOWN",
        source_type="CODE",
        knowledge_domains=["bazi"],
        domain_evidence="code title/filename names bazi",
    )
    assert not v.inspect_row(row, "ziwei"), v.inspect_row(row, "ziwei")

    # Explicitly named out-of-scope systems beyond the first two examples must remain routable.
    row = base(
        source_id="FS-SRC-0011",
        domain="fengshui",
        title="周易變占法引論",
        knowledge_domains=["OUT_OF_SCOPE"],
        domain_evidence="title/filename contains 周易變占",
    )
    assert not v.inspect_row(row, "fengshui"), v.inspect_row(row, "fengshui")

    print("k1-semantic-routing-tests: PASS")


if __name__ == "__main__":
    main()
