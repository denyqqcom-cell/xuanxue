#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"]
ERAS = {"ANCIENT", "PRE_MODERN", "MODERN", "UNKNOWN"}
COPYRIGHT = {"PUBLIC_DOMAIN_TEXT_ONLY", "LICENSED", "RESEARCH_ONLY", "UNKNOWN", "FORBIDDEN_TO_PACKAGE"}
AUTHOR_BASIS = {"FILENAME", "EMBEDDED_METADATA", "TITLE_PAGE", "MANUAL_VERIFIED", "UNKNOWN"}
SCHOOL_BASIS = {"FILENAME", "TITLE_PAGE", "CONTENT_VERIFIED", "MANUAL_VERIFIED", "UNKNOWN"}
PAGES_BASIS = {"PDF_PAGE_COUNT", "DOCUMENT_PAGE_COUNT", "MANUAL_VERIFIED", "UNKNOWN"}
EVIDENCE_ROLES = {"TEXTUAL_SOURCE", "SECONDARY_NOTE", "IMPLEMENTATION_EVIDENCE", "AUXILIARY_INDEX"}
PROMO = re.compile(r"(?i)(?:https?://|www\.|加微信|微信[a-z0-9_-]*|更多教程|qq[:：]?\s*\d{5,})")
PATH_LEAK = re.compile(r"(?i)(?:[A-Z]:[\\/]|/(?:home|Users|mnt)/)")


def fail(msg: str):
    print(f"k1-source-quality: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"cannot parse {path}: {e}")


def load_jsonl(path: Path):
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as e:
            fail(f"invalid JSONL {path}:{n}: {e}")
        if not isinstance(row, dict):
            fail(f"row must be object {path}:{n}")
        rows.append(row)
    return rows


def author_tokens(author: str):
    return [x.strip() for x in re.split(r"\s*(?:/|、|，|,|;|；)\s*", author) if x.strip() and x.strip() != "UNKNOWN"]


def expected_role(source_type: str):
    if source_type == "CODE":
        return "IMPLEMENTATION_EVIDENCE"
    if source_type == "NOTE":
        return "SECONDARY_NOTE"
    if source_type == "OTHER":
        return "AUXILIARY_INDEX"
    return "TEXTUAL_SOURCE"


def inspect_row(row: dict, domain: str):
    sid = row.get("source_id", "<missing>")
    issues = []
    title = row.get("title")
    if not isinstance(title, str) or not title.strip():
        issues.append("title missing")
        title = ""
    if PATH_LEAK.search(json.dumps(row, ensure_ascii=False)):
        issues.append("local path leak")
    if PROMO.search(title):
        issues.append("title contains distribution/contact noise")

    era = row.get("era")
    if era not in ERAS:
        issues.append(f"era not canonical: {era!r}")
    cp = row.get("copyright")
    if cp not in COPYRIGHT:
        issues.append(f"copyright not canonical: {cp!r}")

    author = row.get("author")
    author_basis = row.get("author_basis")
    author_evidence = row.get("author_evidence")
    if author in (None, "", "UNKNOWN"):
        if author_basis not in (None, "UNKNOWN"):
            issues.append("UNKNOWN author has non-UNKNOWN author_basis")
    else:
        if author_basis not in AUTHOR_BASIS - {"UNKNOWN"}:
            issues.append("non-UNKNOWN author lacks trusted author_basis")
        if not isinstance(author_evidence, str) or not author_evidence.strip() or len(author_evidence) > 240:
            issues.append("non-UNKNOWN author lacks short author_evidence")
        if author_basis == "FILENAME":
            missing = [t for t in author_tokens(author) if t not in title]
            if missing:
                issues.append(f"FILENAME author tokens absent from title: {missing}")

    schools = row.get("school_ids")
    if not isinstance(schools, list):
        issues.append("school_ids must be array")
        schools = []
    non_unknown_schools = [x for x in schools if x != "UNKNOWN"]
    school_basis = row.get("school_basis")
    school_evidence = row.get("school_evidence")
    if non_unknown_schools:
        if school_basis not in SCHOOL_BASIS - {"UNKNOWN"}:
            issues.append("school_ids lack trusted school_basis")
        if not isinstance(school_evidence, str) or not school_evidence.strip() or len(school_evidence) > 240:
            issues.append("school_ids lack short school_evidence")

    pages = row.get("pages")
    pages_basis = row.get("pages_basis")
    if pages is not None:
        if not isinstance(pages, int) or pages < 1:
            issues.append("pages must be positive integer or null")
        if pages_basis not in PAGES_BASIS - {"UNKNOWN"}:
            issues.append("pages lacks trusted pages_basis")

    role = row.get("evidence_role")
    if role not in EVIDENCE_ROLES:
        issues.append("missing/invalid evidence_role")
    else:
        exp = expected_role(row.get("source_type"))
        if role != exp:
            issues.append(f"evidence_role {role} != expected {exp} for source_type {row.get('source_type')}")

    if row.get("record_scope") != "SANITIZED_METADATA_ONLY":
        issues.append("record_scope mismatch")
    if row.get("packaged") is not False:
        issues.append("packaged must be false")
    if row.get("local_only") is not True:
        issues.append("local_only must be true")

    return [(sid, issue) for issue in issues]


def main():
    parser = argparse.ArgumentParser(description="Validate semantic/provenance quality of sanitized K1 source registries")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--force", action="store_true", help="Require zero source-quality issues regardless of project state")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    k = repo / "knowledge"
    state = load_json(k / "PROJECT_STATE.json")

    issues = []
    total = 0
    for domain in DOMAINS:
        path = k / "domains" / domain / "sources.jsonl"
        if not path.is_file():
            fail(f"missing source registry: {path.relative_to(repo)}")
        rows = load_jsonl(path)
        total += len(rows)
        for row in rows:
            issues.extend(inspect_row(row, domain))

    quality_state = state.get("source_quality", "PENDING")
    if args.force or quality_state == "COMPLETE":
        if issues:
            sample = "; ".join(f"{sid}: {msg}" for sid, msg in issues[:12])
            fail(f"{len(issues)} issue(s) across {total} sources; sample: {sample}")
        print("k1-source-quality: PASS")
        print(f"sources={total} issues=0")
        return

    if quality_state == "REVIEW_REQUIRED":
        if not state.get("k2_blocked"):
            fail("source quality review requires k2_blocked=true")
        if not issues:
            fail("source_quality=REVIEW_REQUIRED but no issues remain; promote state to COMPLETE")
        print("k1-source-quality: REVIEW_REQUIRED")
        print(f"sources={total} issues={len(issues)}")
        for sid, msg in issues[:20]:
            print(f"- {sid}: {msg}")
        return

    if issues:
        fail(f"source quality issues exist while project state is {quality_state!r}; mark REVIEW_REQUIRED or remediate")
    print("k1-source-quality: PASS")
    print(f"sources={total} issues=0")


if __name__ == "__main__":
    main()
