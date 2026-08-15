#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
REQUIRED = ["ziwei", "bazi", "qimen", "liuyao", "liuren", "fengshui"]
LEVELS = [
    "L0_SOURCE_ONLY","L1_INDEXED","L2_CLAIM_EXTRACTED","L3_CROSS_VERIFIED",
    "L4_CONFLICT_MAPPED","L5_FIXTURE_VERIFIED","L6_ENGINE_VERIFIED",
    "L7_INTERPRETATION_READY","L8_FEEDBACK_VALIDATED",
]

def fail(msg):
    print(f"knowledge-gate: FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)

def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"cannot parse {path.relative_to(ROOT)}: {e}")

def main():
    state = load(K / "PROJECT_STATE.json")
    if state.get("schema_version") != "knowledge-engine-v1":
        fail("unexpected schema_version")
    if state.get("required_domains") != REQUIRED:
        fail("required_domains must contain exactly the six governed domains in canonical order")

    registry = load(K / "registry/domains.json")
    ids = [x.get("id") for x in registry if x.get("role") == "domain"]
    if ids != REQUIRED:
        fail("domain registry mismatch")

    for schema in ["source.schema.json", "claim.schema.json", "conflict.schema.json", "fixture.schema.json"]:
        doc = load(K / "schema" / schema)
        if doc.get("type") != "object" or not doc.get("required"):
            fail(f"schema lacks object/required contract: {schema}")

    levels = {}
    for d in REQUIRED:
        s = load(K / "domains" / d / "status.json")
        if s.get("domain") != d:
            fail(f"status domain mismatch: {d}")
        level = s.get("maturity_level")
        if level not in LEVELS:
            fail(f"invalid maturity level for {d}: {level}")
        levels[d] = LEVELS.index(level)
        for key in ["sources_indexed", "claims_extracted", "fixtures_total", "fixtures_verified"]:
            v = s.get(key)
            if not isinstance(v, int) or v < 0:
                fail(f"{d}.{key} must be non-negative integer")
        if s["fixtures_verified"] > s["fixtures_total"]:
            fail(f"{d}: verified fixtures exceeds total")

    qref = load(K / "domains/qimen/legacy_handoff.json")
    for p in [qref["manifest"], qref["rules"], qref["conflicts"], qref["fixtures"], qref["copyright"], qref["summary"]]:
        if not (ROOT / p).is_file():
            fail(f"qimen legacy reference missing: {p}")

    # K0 may expose the imbalance, but may not hide it. From K1 onward the six domains
    # must all reach L1 before any domain is allowed to advance beyond L2.
    if state.get("balance_gate") == "ENFORCE":
        if min(levels.values()) < 1 and max(levels.values()) > 2:
            fail("DOMAIN_IMBALANCE: a domain advanced beyond L2 while another is below L1")

    status_text = (K / "STATUS.md").read_text(encoding="utf-8")
    for d in ["紫微", "八字", "奇门", "六爻", "大六壬", "风水"]:
        if d not in status_text:
            fail(f"STATUS.md missing domain: {d}")
    if "DOMAIN_IMBALANCE" not in status_text:
        fail("K0 status must expose current domain imbalance")

    forbidden_ext = {".pdf", ".epub", ".doc", ".docx", ".ttf", ".otf", ".woff", ".woff2"}
    for p in K.rglob("*"):
        if p.is_file() and p.suffix.lower() in forbidden_ext:
            fail(f"copyright boundary: binary research asset under knowledge/: {p.relative_to(ROOT)}")

    print("knowledge-gate: PASS")
    print("phase=", state.get("phase"))
    print("levels=", {d: LEVELS[levels[d]] for d in REQUIRED})
    if min(levels.values()) < max(levels.values()):
        print("balance=DOMAIN_IMBALANCE_K1_REQUIRED")

if __name__ == "__main__":
    main()
