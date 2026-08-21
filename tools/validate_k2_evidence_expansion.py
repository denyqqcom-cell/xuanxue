#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
sys.path.insert(0, str(ROOT / "tools"))

import validate_k2_evidence as base
import validate_k2_book_distillates as distillate_validator

MANIFEST = "K2_EVIDENCE_EXPANSION.json"
LEDGER_DIR = "K2_READING_LEDGER_EXPANSION.d"
EVIDENCE_DIR = "K2_EVIDENCE_EXPANSION.d"
DISTILLATE_DIR = "K2_BOOK_DISTILLATES_EXPANSION.d"
PATH_RE = re.compile(r"(?:/home/|/mnt/|[A-Za-z]:\\\\)")
PDF_LOC_RE = re.compile(r"(?:^|\|)pdf:p(\d+)(?:-p?(\d+))?(?:$|\|)")


def fail(msg: str) -> None:
    print(f"k2-evidence-expansion: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse {path}: {exc}")


def load_jsonl(path: Path):
    rows = []
    if not path.exists():
        return rows
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:
            fail(f"invalid JSONL {path}:{line_no}: {exc}")
        if not isinstance(row, dict):
            fail(f"row must be object {path}:{line_no}")
        rows.append(row)
    return rows


def covered_pages(row, pages, issues, sid):
    return base.range_union(row.get("page_ranges"), pages, issues, sid)


def validate_manifest(manifest, sources, lineage):
    issues = []
    allowed = {"schema_version", "status", "source_ids", "selection_rule", "review_status"}
    extra = set(manifest) - allowed
    if extra:
        issues.append(("<manifest>", f"unexpected fields: {sorted(extra)}"))
    if manifest.get("schema_version") != "k2-evidence-expansion-v1":
        issues.append(("<manifest>", "unsupported schema_version"))
    if manifest.get("status") != "ACTIVE":
        issues.append(("<manifest>", "status must be ACTIVE"))
    if manifest.get("review_status") != "REVIEWED":
        issues.append(("<manifest>", "review_status must be REVIEWED"))
    source_ids = manifest.get("source_ids")
    if not isinstance(source_ids, list) or not source_ids:
        issues.append(("<manifest>", "source_ids must be non-empty array"))
        return issues, []
    if len(source_ids) != len(set(source_ids)):
        issues.append(("<manifest>", "duplicate source_ids"))
    wave1 = base.wave1_expected(sources, lineage)
    for sid in source_ids:
        src = sources.get(sid)
        lin = lineage.get(sid)
        if not src or not lin:
            issues.append((sid, "unknown source or lineage"))
            continue
        if sid in wave1:
            issues.append((sid, "source already belongs to base Wave1; expansion must not duplicate credit"))
        if lin.get("k2_eligible") is not True:
            issues.append((sid, "expansion source must be k2_eligible=true"))
        if lin.get("relation") not in base.UNIQUE_REL:
            issues.append((sid, "expansion source must be textual UNIQUE_REL"))
        if not base.governed(src):
            issues.append((sid, "expansion source must be governed textual source"))
        if src.get("evidence_role") != "TEXTUAL_SOURCE":
            issues.append((sid, "expansion source must have evidence_role=TEXTUAL_SOURCE"))
    return issues, source_ids


def validate_source(repo, sid, sources, lineage):
    issues = []
    src = sources[sid]
    lin = lineage[sid]
    lp = repo / "knowledge" / LEDGER_DIR / f"{sid}.jsonl"
    ep = repo / "knowledge" / EVIDENCE_DIR / f"{sid}.jsonl"
    dp = repo / "knowledge" / DISTILLATE_DIR / f"{sid}.jsonl"
    ledger_rows = load_jsonl(lp)
    evidence = load_jsonl(ep)
    distillates = load_jsonl(dp)

    if len(ledger_rows) != 1:
        issues.append((sid, "expansion ledger must contain exactly one row"))
        return issues, ledger_rows, evidence, distillates
    ledger = ledger_rows[0]
    if ledger.get("source_id") != sid:
        issues.append((sid, "ledger source_id mismatch"))
    if ledger.get("work_id") != lin.get("work_id"):
        issues.append((sid, "ledger work_id mismatch"))
    if ledger.get("relation") != lin.get("relation"):
        issues.append((sid, "ledger relation mismatch"))
    expected_lane = base.expected_execution_lane(src)
    if ledger.get("execution_lane") != expected_lane:
        issues.append((sid, f"execution_lane mismatch: expected {expected_lane}"))
    if ledger.get("read_status") != "COMPLETE":
        issues.append((sid, "expansion source must be COMPLETE before admission"))
    if ledger.get("review_status") != "REVIEWED":
        issues.append((sid, "ledger must be REVIEWED"))
    verification = ledger.get("verification_mode")
    base.validate_verification_for_reviewed_source(sid, expected_lane, verification, issues)
    pages = src.get("pages")
    covered = covered_pages(ledger, pages, issues, sid)
    if isinstance(pages, int):
        if ledger.get("coverage_mode") not in {"PDF_PAGES", "DOCUMENT_PAGES"}:
            issues.append((sid, "paged COMPLETE source requires page coverage mode"))
        if len(covered) != pages or not covered or min(covered) != 1 or max(covered) != pages:
            issues.append((sid, f"COMPLETE coverage must span all {pages} pages"))
        if ledger.get("pages_reviewed_count") != pages:
            issues.append((sid, "pages_reviewed_count mismatch"))

    ev_ids = set()
    for e in evidence:
        eid = e.get("evidence_id")
        if not isinstance(eid, str) or not eid:
            issues.append((sid, "missing evidence_id"))
            continue
        if eid in ev_ids:
            issues.append((eid, "duplicate evidence_id"))
        ev_ids.add(eid)
        if e.get("source_id") != sid:
            issues.append((eid, "evidence source_id mismatch"))
        if e.get("work_id") != lin.get("work_id"):
            issues.append((eid, "evidence work_id mismatch"))
        if e.get("domain") not in (src.get("knowledge_domains") or []) and e.get("domain") != "common":
            issues.append((eid, "evidence domain unsupported"))
        if e.get("evidence_type") not in base.EVIDENCE_TYPES:
            issues.append((eid, "invalid evidence_type"))
        if e.get("scope") not in base.SCOPES:
            issues.append((eid, "invalid scope"))
        basis = e.get("extraction_basis")
        if basis not in base.BASES:
            issues.append((eid, "invalid extraction_basis"))
        if expected_lane == "VISUAL_REQUIRED" and basis not in {"VISUAL_PAGE", "TABLE_READ", "DIAGRAM_READ"}:
            issues.append((eid, "VISUAL_REQUIRED expansion evidence must be visually grounded"))
        if e.get("claim_readiness") not in base.CLAIM_READY:
            issues.append((eid, "invalid claim_readiness"))
        fact = e.get("normalized_fact")
        if not isinstance(fact, str) or not fact.strip() or len(fact) > 800:
            issues.append((eid, "normalized_fact invalid"))
        loc = e.get("source_location")
        if not isinstance(loc, str) or not loc.strip() or len(loc) > 120 or PATH_RE.search(loc):
            issues.append((eid, "source_location invalid or leaks local path"))
        if e.get("verbatim_quote") not in (None, ""):
            issues.append((eid, "non-public expansion source must not export verbatim_quote"))
        if e.get("copyright_class") != "DERIVED_FACT_SAFE":
            issues.append((eid, "expansion evidence must use DERIVED_FACT_SAFE"))
        if e.get("review_status") not in {"REVIEWED", "CONFLICTED"}:
            issues.append((eid, "evidence must be REVIEWED or CONFLICTED"))
        match = PDF_LOC_RE.search(loc or "")
        if match:
            a = int(match.group(1)); b = int(match.group(2) or a)
            if any(p not in covered for p in range(a, b + 1)):
                issues.append((eid, "evidence locator outside reviewed coverage"))

    if ledger.get("evidence_count") != len(evidence):
        issues.append((sid, "ledger evidence_count does not match Evidence rows"))

    dist_issues = distillate_validator.validate_rows(ledger_rows, evidence, distillates)
    issues.extend(dist_issues)
    return issues, ledger_rows, evidence, distillates


def validate_repo(repo=ROOT):
    sources = base.source_index(repo)
    lineage = base.lineage_index(repo)
    manifest = load_json(repo / "knowledge" / MANIFEST)
    issues, source_ids = validate_manifest(manifest, sources, lineage)

    selected = set(source_ids)
    for dirname in (LEDGER_DIR, EVIDENCE_DIR, DISTILLATE_DIR):
        d = repo / "knowledge" / dirname
        actual = {p.stem for p in d.glob("*.jsonl")} if d.exists() else set()
        extra = actual - selected
        missing = selected - actual
        if extra:
            issues.append((f"<{dirname}>", f"unexpected shards: {sorted(extra)}"))
        if missing:
            issues.append((f"<{dirname}>", f"missing shards: {sorted(missing)}"))

    total_evidence = 0
    complete = 0
    for sid in source_ids:
        if sid not in sources or sid not in lineage:
            continue
        local_issues, ledger, evidence, _ = validate_source(repo, sid, sources, lineage)
        issues.extend(local_issues)
        total_evidence += len(evidence)
        if ledger and ledger[0].get("read_status") == "COMPLETE":
            complete += 1

    return issues, source_ids, complete, total_evidence


def main():
    issues, source_ids, complete, evidence_count = validate_repo(ROOT)
    if issues:
        sample = "; ".join(f"{sid}: {msg}" for sid, msg in issues[:20])
        fail(f"issues={len(issues)}; {sample}")
    print("k2-evidence-expansion: PASS")
    print(f"selected={len(source_ids)} complete={complete} evidence_rows={evidence_count} issues=0")
    print("credit_scope=CORPUS_EXPANSION; empirical_support_unchanged=true")


if __name__ == "__main__":
    main()
