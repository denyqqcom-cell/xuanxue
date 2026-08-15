#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K = ROOT / "knowledge"
DOMAINS = [
    ("ziwei", "紫微"),
    ("bazi", "八字"),
    ("qimen", "奇门"),
    ("liuyao", "六爻"),
    ("liuren", "大六壬"),
    ("fengshui", "风水"),
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def render() -> str:
    state = load(K / "PROJECT_STATE.json")
    lines = [
        f"# Knowledge Engine Status — {state['phase']}",
        "",
        "| Domain | Level | Sources | Claims | Fixtures verified | Next gate |",
        "|---|---|---:|---:|---:|---|",
    ]
    levels = []
    for domain, label in DOMAINS:
        s = load(K / "domains" / domain / "status.json")
        levels.append(s["maturity_level"])
        lines.append(
            f"| {label} | {s['maturity_level']} | {s['sources_indexed']} | "
            f"{s['claims_extracted']} | {s['fixtures_verified']} | {s['next_gate']} |"
        )
    lines += [
        "",
        "`DOMAIN_IMBALANCE` 当前是预期状态，不代表允许继续只强化奇门。K1 的目标是六域全部达到 `L1_INDEXED`；在此之前不新增任何领域的 Interpretation production rule。",
        "",
        "紫微现有 iztro fixture 属于实现 parity 证据，不计为本 Knowledge Engine 的独立来源吸收率。",
        "",
        f"Generated from `knowledge/domains/*/status.json`; balance gate = `{state['balance_gate']}`.",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = K / "STATUS.md"
    expected = render()
    if args.check:
        actual = target.read_text(encoding="utf-8") if target.exists() else ""
        if actual != expected:
            raise SystemExit("knowledge status drift: run tools/generate_knowledge_status.py")
        print("knowledge-status: PASS")
    else:
        target.write_text(expected, encoding="utf-8")
        print(target)

if __name__ == "__main__":
    main()
