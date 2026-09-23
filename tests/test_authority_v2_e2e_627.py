"""627 B1 · feature flag 端到端验证 单测（≥4 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import authority_v2_e2e_627 as B


def test_all_five_projections_listed():
    r = B.run_e2e()
    assert len(r["rows"]) == 5
    assert {x["projection"] for x in r["rows"]} == {
        "w2", "pck", "golden", "dashboard", "textbook"}


def test_v2_all_ok():
    r = B.run_e2e()
    assert r["all_v2_ok"]
    assert all(x["v2_ok"] for x in r["rows"])


def test_v2_summaries_nonempty():
    r = B.run_e2e()
    for row in r["rows"]:
        assert row["v2_ok"]
        assert row["v2_summary"] is not None


def test_v1_legacy_reference_for_w2_and_pck():
    w2 = B.v1_legacy_reference("w2")
    pck = B.v1_legacy_reference("pck")
    assert w2["ok"] and w2["mode"] == "legacy_grounded_labels"
    assert pck["ok"] and pck["mode"] == "legacy_pck_certificates"


def test_v2_only_projections_flagged():
    for p in ("golden", "dashboard", "textbook"):
        ref = B.v1_legacy_reference(p)
        assert ref["mode"] == "v2_only"
