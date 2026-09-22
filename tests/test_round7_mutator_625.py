"""625 B1 · 闭环第 7 轮回归测试（≥5 例）。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import round7_mutator_625 as m  # noqa: E402


def test_all_rules_67_and_blind_nonempty():
    assert len(m.all_rules()) == 67
    blind = m.blind_rules()
    assert 0 < len(blind) < 40


def test_generate_about_100():
    muts = m.generate_round7(m.cc.load_inventory())
    assert 95 <= len(muts) <= 110
    assert {x["strategy"] for x in muts} == {"Y1", "Y2", "Y3"}


def test_y1_covers_all_blind_rules():
    muts = m.generate_round7(m.cc.load_inventory())
    y1 = {x["predicted_rules"][0] for x in muts if x["strategy"] == "Y1"}
    assert y1 == set(m.blind_rules())


def test_run_artifact_escaped_zero_and_touched():
    p = os.path.join(ROOT, "data", "adversarial_loop_round7_sandbox_run_625.json")
    d = json.load(open(p, encoding="utf-8"))
    assert d["total"] >= 95
    assert d["escaped"] == []
    assert d["distribution"].get("escaped", 0) == 0
    assert d["touched_all"]


def test_new_rules_this_round():
    p = os.path.join(ROOT, "data", "adversarial_loop_round7_sandbox_run_625.json")
    d = json.load(open(p, encoding="utf-8"))
    new = set(d["touched_all"]) - m.TOUCHED
    assert new == {"ATOM-STATUS-TRANSITION", "S1-AUTHOR-SELF-VERIFY"}


def test_selftest_passes():
    assert m.selftest() == 0
