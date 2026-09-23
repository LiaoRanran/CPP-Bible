"""627 C1 · Blind Review 执行包 单测（≥4 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import blind_review_execution_pack_627 as C

LEAK = {"current_decision_id", "result", "authority_result", "recommendation",
        "ai_recommendation", "decision", "status"}


def test_top10_generated():
    p = C.build_pack()
    assert p["top_n"] == 10


def test_blindness_no_leak():
    p = C.build_pack()
    for it in p["items"]:
        assert not any(f in it for f in LEAK)


def test_blank_decision_slot():
    p = C.build_pack()
    for it in p["items"]:
        assert "human_decision" in it
        assert it["human_decision"] is None


def test_uses_real_ledger_source():
    p = C.build_pack()
    assert "review_item_ledger" in p["source"]
