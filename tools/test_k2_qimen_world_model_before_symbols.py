#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"


def main():
    protocol=K/"K2_QIMEN_WORLD_MODEL_BEFORE_SYMBOLS_PROTOCOL.md"
    assert protocol.exists(),"missing World Model Before Symbols protocol"
    text=protocol.read_text(encoding="utf-8")

    required=[
        "WORLD_MODEL_BEFORE_SYMBOLS",
        "M0_INPUT_FREEZE",
        "M1_REALITY_ONLY",
        "M2_SYMBOL_MAPPING",
        "M3_FROZEN_PREDICTION",
        "M4_NARRATIVE_IMMUTABLE_PREDICTION",
        "KEEP / MERGE / DOWNGRADE / SPLIT / DELETE",
        "LATENT_FACTOR_NOT_REQUIRED",
        "WAVE1_PROGRESS_NOT_SINGLE_EXPERIMENT_THRESHOLD",
        "NO_PSEUDO_PRECISION_SCORE",
        "COGNITIVE / EMPIRICAL / PRODUCT",
        "CORE / KNOWLEDGE / EMULATOR / PHYSICAL",
        "INHERITED",
    ]
    missing=[token for token in required if token not in text]
    assert not missing,f"World Model Before Symbols protocol missing invariants: {missing}"

    charter=(K/"K2_QIMEN_COGNITIVE_RECONSTRUCTION_CHARTER.md").read_text(encoding="utf-8")
    forbidden=[
        "新组件如果不能改善预注册指标，就删除或降级",
        "无增量价值的组件删除",
    ]
    leaked=[phrase for phrase in forbidden if phrase in charter]
    assert not leaked,f"charter still contains forced-deletion KPI language: {leaked}"

    print("k2-qimen-world-model-before-symbols-tests: PASS")


if __name__=="__main__":main()
