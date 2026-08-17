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
    local_validation_path = K / "K1_LOCAL_VALIDATION.json"
    local_validation = load(local_validation_path) if local_validation_path.exists() else None

    lines = [
        f"# Knowledge Engine Status — {state['phase']}",
        "",
        "| Domain | Engine level | Local K1 sources | K1 index | K2 readiness | Claims | Fixtures verified | Next gate |",
        "|---|---|---:|---|---|---:|---:|---|",
    ]
    levels = []
    for domain, label in DOMAINS:
        s = load(K / "domains" / domain / "status.json")
        levels.append(s["maturity_level"])
        local = (local_validation or {}).get("domains", {}).get(domain, {})
        local_sources = local.get("sources", "-")
        k1_index = local.get("k1_index_status", "PENDING")
        k2 = local.get("k2_readiness", "PENDING")
        next_gate = "K1_SANITIZED_IMPORT" if state.get("sanitized_import") == "PENDING" else s["next_gate"]
        lines.append(
            f"| {label} | {s['maturity_level']} | {local_sources} | {k1_index} | {k2} | "
            f"{s['claims_extracted']} | {s['fixtures_verified']} | {next_gate} |"
        )

    if local_validation and local_validation.get("result") == "PASS":
        lines += [
            "",
            "本地 K1 Source Index 已通过项目 validator 的机器验收并完成 accounting 对账；当前剩余 Gate 是 **sanitized metadata import**。在 `knowledge/domains/*/sources.jsonl` 被导入并通过仓库端验证以前，不把本地 source 数直接冒充为仓库已吸收的 `L1_INDEXED`。",
        ]
    else:
        lines += [
            "",
            "本地 K1 Source Index 尚未完成机器验收。",
        ]

    lines += [
        "",
        "`ENGINE_MATURITY_IMBALANCE` 仍然存在：奇门已有 legacy claim/fixture，而其他领域尚未进入同等 claim maturity。这不允许用模型知识补齐，也不允许绕过六域共同 Gate。",
        "",
        "六爻/大六壬的 `THIN_CORPUS` 与风水的 `READING_REQUIRED` 是 K2 readiness 风险，不否定其 K1 索引完整性，但会限制后续交叉验证与解释层开放。",
        "",
        "紫微现有 iztro fixture 属于实现 parity 证据，不计为独立传统术理真值。",
        "",
        f"Generated from `knowledge/domains/*/status.json`, `knowledge/K1_LOCAL_VALIDATION.json` and `knowledge/PROJECT_STATE.json`; balance gate = `{state['balance_gate']}`.",
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
