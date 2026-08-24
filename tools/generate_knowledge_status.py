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
    lineage_state_path = K / "K2_SOURCE_LINEAGE_STATE.json"
    lineage_state = load(lineage_state_path) if lineage_state_path.exists() else None
    evidence_state_path = K / "K2_EVIDENCE_STATE.json"
    evidence_state = load(evidence_state_path) if evidence_state_path.exists() else None
    levels=[]

    lines = [
        f"# Knowledge Engine Status — {state['phase']}",
        "",
        "| Domain | Engine level | Local K1 sources | K1 index | K2 readiness | Claims | Fixtures verified | Next gate |",
        "|---|---|---:|---|---|---:|---:|---|",
    ]
    for domain, label in DOMAINS:
        s = load(K / "domains" / domain / "status.json")
        levels.append(s["maturity_level"])
        local = (local_validation or {}).get("domains", {}).get(domain, {})
        local_sources = local.get("sources", "-")
        k1_index = local.get("k1_index_status", "PENDING")
        k2 = local.get("k2_readiness", "PENDING")
        if state.get("phase") == "K2_SOURCE_LINEAGE":
            reason=(lineage_state or {}).get("review_reason")
            next_gate = "K2_LINEAGE_COVERAGE_REVIEW" if reason == "PART_VS_VARIANT_COVERAGE_REVIEW" else "K2_SOURCE_LINEAGE"
        elif state.get("phase") == "K2_EVIDENCE_EXTRACTION":
            next_gate = f"K2_EVIDENCE_WAVE{(evidence_state or {}).get('wave', 1)}"
        elif state.get("semantic_routing") == "REVIEW_REQUIRED":
            next_gate = "K1_SEMANTIC_ROUTING_REVIEW"
        elif state.get("source_quality") == "REVIEW_REQUIRED":
            next_gate = "K1_ATTRIBUTION_REVIEW"
        elif state.get("sanitized_import") == "PENDING":
            next_gate = "K1_SANITIZED_IMPORT"
        else:
            next_gate = s["next_gate"]
        lines.append(
            f"| {label} | {s['maturity_level']} | {local_sources} | {k1_index} | {k2} | "
            f"{s['claims_extracted']} | {s['fixtures_verified']} | {next_gate} |"
        )

    if state.get("k1_acceptance") == "PROJECT_VERIFIED":
        lines += [
            "",
            "K1 已完成项目端闭环：本地 accounting、515 条 sanitized registry、attribution/source-quality、semantic routing precision、版权二进制边界与 stable core 回归均通过。六术当前统一从 `L1_INDEXED` 起跑。",
        ]
    elif local_validation and local_validation.get("result") == "PASS":
        lines += ["", "本地 K1 Source Index 已通过项目 validator 的机器验收并完成 accounting 对账。"]
    else:
        lines += ["", "本地 K1 Source Index 尚未完成机器验收。"]

    if state.get("phase") == "K2_SOURCE_LINEAGE":
        lines += [
            "",
            "当前进入 `K2_SOURCE_LINEAGE`：先建立 underlying work / edition / commentary / note / implementation 的谱系，再开始 Evidence/Claim Extraction。`claim_extraction_blocked=true` 是有意的 fail-closed Gate。",
            "",
            "同一本书的不同扫描、整洁版、排印版，以及由它派生的笔记/代码，不得按文件数计算为多个独立支持来源。",
        ]
        if (lineage_state or {}).get("review_reason") == "PART_VS_VARIANT_COVERAGE_REVIEW":
            lines += [
                "",
                "项目端复验发现第一版 lineage 把部分互补卷册/分页与真正的同内容版本都标成 `SAME_WORK_VARIANT`。当前必须完成 `K2_LINEAGE_COVERAGE_REVIEW`：互补卷册使用 `WORK_PART` 并保持可读；真正重复载体使用 `SAME_WORK_VARIANT + variant_of_source_id`。Claim Extraction 继续锁定。",
            ]
    elif state.get("phase") == "K2_EVIDENCE_EXTRACTION":
        lanes=(evidence_state or {}).get("expected_execution_lanes", {})
        identity_rule=(evidence_state or {}).get("canonical_identity_rule")
        lines += [
            "",
            "K2A Source Lineage 已由项目端验收为 `COMPLETE`。当前进入 `K2_EVIDENCE_EXTRACTION`：开始逐页/逐段读取本地文本，形成页级 Evidence 与 Reading Ledger，但仍禁止把多个 Evidence 合成为 Claim。",
            "",
            "K2B 工程执行权由项目主 Agent 持有；本地 AI 仅负责 GitHub→本地 fast-forward 同步，以及 canonical 本地资料/page packet 的定位、SHA256/页数/完整性校验和明确点名的单文件发布。它不运行测试/Gradle/instrumentation，不写代码或知识树，不做工程判断，也不 commit/push。",
            "",
            f"Wave 1 execution lanes：TEXT_DIRECT = {lanes.get('TEXT_DIRECT','?')}；VISUAL_REQUIRED = {lanes.get('VISUAL_REQUIRED','?')}；ACCESS_REVIEW = {lanes.get('ACCESS_REVIEW','?')}。SCAN/OCR_WEAK/OCR_FAIL 没有原页视觉能力时必须诚实 BLOCKED，不得用 OCR 冒充视觉核验。",
            "",
            "Windows/WSL/Linux 的 source 定位不再依赖固定 private intake 路径；允许在显式 corpus roots 中按 official canonical SHA256 查找完全相同的源字节。文件名相似不能替代 hash identity。" if identity_rule else "",
            "",
            "Wave 1 按 work coverage 而不是文件数排程：所有 P0 work family 展开到完整 PRIMARY_WORK/WORK_PART coverage；六爻与大六壬薄 corpus 的全部 governed unique textual coverage同步进入。`claim_extraction_blocked=true` 保持。",
            "",
            f"当前 K2B 账面：unique textual coverage units = {(evidence_state or {}).get('unique_textual_coverage_units','?')}；semantic UNKNOWN textual backlog = {(evidence_state or {}).get('unknown_textual_resolution_backlog','?')}。UNKNOWN 不会被遗忘，后续必须经过 content review 后路由或保留有依据的 UNKNOWN。",
        ]

    if len(set(levels)) > 1:
        lines += ["", "`ENGINE_MATURITY_IMBALANCE` 仍存在，不允许成熟域绕过其他领域继续升级。"]
    else:
        lines += ["", "六个正式术数域当前成熟度一致；Balance Gate 已从‘限制失衡’转为‘保持同步推进’。"]

    lines += [
        "",
        "六爻/大六壬的 `THIN_CORPUS` 与风水的 `READING_REQUIRED` 是 K2 readiness 风险，不否定其 K1 索引完整性，但会限制后续交叉验证与解释层开放。",
        "",
        "奇门既有 36 claims / 17 fixtures 被保留为 legacy pending re-audit，不再因为旧 handoff 自动占据高于其他五域的当前成熟度。",
        "",
        "紫微现有 iztro fixture 属于实现 parity 证据，不计为独立传统术理真值。",
        "",
        f"Generated from `knowledge/domains/*/status.json`, `knowledge/K1_LOCAL_VALIDATION.json`, `knowledge/K2_SOURCE_LINEAGE_STATE.json`, `knowledge/K2_EVIDENCE_STATE.json` and `knowledge/PROJECT_STATE.json`; balance gate = `{state['balance_gate']}`.",
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
