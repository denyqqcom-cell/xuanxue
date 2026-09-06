#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_k2_local_page_packets as packets


def main():
    # Page-preserving text-layer output is part of the TEXT_DIRECT contract.
    # A returned page set with the wrong page count is not a parser failure:
    # extraction returned data, but the text layer is unusable for source-bound
    # page review and must remain an execution-only diagnostic.
    code, reason = packets.classify_text_layer_page_count(["p1", "p2"], 2)
    assert code is None and reason is None, (code, reason)

    code, reason = packets.classify_text_layer_page_count(["p1", "p2"], 3)
    assert code == "TEXT_LAYER_UNUSABLE", (code, reason)
    assert "page count 2" in reason
    assert "registered PDF pages 3" in reason
    assert code != "TEXT_EXTRACTION_FAILED"

    # Unpaged/unknown-count sources preserve current behavior.
    code, reason = packets.classify_text_layer_page_count(["body"], None)
    assert code is None and reason is None, (code, reason)

    print("k2-text-page-count-contract-tests: PASS")


if __name__ == "__main__":
    main()
