#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"]
ALLOWED = set(DOMAINS + ["common", "OUT_OF_SCOPE", "UNKNOWN"])
DOMAIN_BASIS = {"TITLE_FILENAME", "CONTENT_VERIFIED", "MANUAL_VERIFIED", "PROJECT_CODE_PATH", "UNKNOWN"}

# High-precision routing hints only. These are not metaphysical truth rules; they prevent obvious folder-based contamination.
HINTS = [
    (re.compile(r"奇门"), "qimen"),
    (re.compile(r"紫微|斗数"), "ziwei"),
    (re.compile(r"大六壬|六壬"), "liuren"),
    (re.compile(r"六爻|卜筮正宗|增.?卜易|火珠林"), "liuyao"),
    (re.compile(r"八字|子平|滴天髓|命稿"), "bazi"),
    (re.compile(r"风水|凤水|堪舆|玄空|阳宅"), "fengshui"),
]
OUT_OF_SCOPE_HINT = re.compile(r"梅花心易|梅花易数|铁板神数")
EDITOR_ROLE = re.compile(r"(?:主编|点校|校(?:订|注|者)?|译(?:者)?|整理|编校)")
AUTHOR_ROLE = re.compile(r"(?:著|撰|编著|作者)")


def fail(msg: str):
    print(f"k1-semantic-routing: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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
    if not isinstance(author, str):
        return []
    return [x.strip() for x in re.split(r"\s*(?:/|、|，|,|;|；)\s*", author) if x.strip() and x.strip() != "UNKNOWN"]


def inspect_row(row: dict, registry_domain: str):
    sid = row.get("source_id", "<missing>")
    title = row.get("title") if isinstance(row.get("title"), str) else ""
    issues = []

    kd = row.get("knowledge_domains")
    if not isinstance(kd, list) or not kd:
        issues.append("missing knowledge_domains")
        kd = []
    else:
        bad = [x for x in kd if x not in ALLOWED]
        if bad:
            issues.append(f"invalid knowledge_domains: {bad}")
        if len(kd) != len(set(kd)):
            issues.append("knowledge_domains contains duplicates")
        if "UNKNOWN" in kd and len(kd) > 1:
            issues.append("UNKNOWN cannot be mixed with resolved knowledge_domains")
        if "OUT_OF_SCOPE" in kd and len(kd) > 1:
            issues.append("OUT_OF_SCOPE cannot be mixed with in-scope domains")

    basis = row.get("domain_basis")
    evidence = row.get("domain_evidence")
    if basis not in DOMAIN_BASIS:
        issues.append("missing/invalid domain_basis")
    if basis not in (None, "UNKNOWN"):
        if not isinstance(evidence, str) or not evidence.strip() or len(evidence) > 240:
            issues.append("resolved semantic domain lacks short domain_evidence")
    if basis == "UNKNOWN" and kd and kd != ["UNKNOWN"]:
        issues.append("resolved knowledge_domains cannot use domain_basis=UNKNOWN")

    # Explicit title clues must not be contradicted by registry-folder routing.
    if kd:
        for pattern, expected in HINTS:
            if pattern.search(title) and expected not in kd and "OUT_OF_SCOPE" not in kd and "UNKNOWN" not in kd:
                issues.append(f"title strongly signals {expected} but knowledge_domains={kd}")
        if OUT_OF_SCOPE_HINT.search(title) and "OUT_OF_SCOPE" not in kd and "UNKNOWN" not in kd:
            issues.append(f"title strongly signals out-of-scope system but knowledge_domains={kd}")

    # Project code may use registry/module path as direct routing evidence; textual books may not use folder location alone.
    if row.get("source_type") == "CODE" and basis == "PROJECT_CODE_PATH" and registry_domain not in kd:
        issues.append("project code routing must include its registry domain")

    # A filename token is not automatically an author when the same title explicitly labels the person as editor/proofreader/etc.
    author = row.get("author")
    if row.get("author_basis") == "FILENAME" and author not in (None, "", "UNKNOWN"):
        for token in author_tokens(author):
            pos = title.find(token)
            if pos >= 0:
                tail = title[pos + len(token): pos + len(token) + 6]
                if EDITOR_ROLE.search(tail) and not AUTHOR_ROLE.search(tail):
                    issues.append(f"author token {token} is explicitly a non-author contributor in title")

    return [(sid, issue) for issue in issues]


def main():
    parser = argparse.ArgumentParser(description="Validate K1 semantic domain routing independently from physical registry location")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    k = repo / "knowledge"
    state = load_json(k / "PROJECT_STATE.json")

    issues = []
    total = 0
    for domain in DOMAINS:
        rows = load_jsonl(k / "domains" / domain / "sources.jsonl")
        total += len(rows)
        for row in rows:
            issues.extend(inspect_row(row, domain))

    routing_state = state.get("semantic_routing", "PENDING")
    if args.force or routing_state == "COMPLETE":
        if issues:
            sample = "; ".join(f"{sid}: {msg}" for sid, msg in issues[:16])
            fail(f"{len(issues)} issue(s) across {total} sources; sample: {sample}")
        print("k1-semantic-routing: PASS")
        print(f"sources={total} issues=0")
        return

    if routing_state == "REVIEW_REQUIRED":
        if not state.get("k2_blocked"):
            fail("semantic routing review requires k2_blocked=true")
        if not issues:
            fail("semantic_routing=REVIEW_REQUIRED but no issues remain; promote state to COMPLETE")
        print("k1-semantic-routing: REVIEW_REQUIRED")
        print(f"sources={total} issues={len(issues)}")
        for sid, msg in issues[:24]:
            print(f"- {sid}: {msg}")
        return

    if issues:
        fail(f"semantic routing issues exist while project state is {routing_state!r}")
    print("k1-semantic-routing: PASS")
    print(f"sources={total} issues=0")


if __name__ == "__main__":
    main()
