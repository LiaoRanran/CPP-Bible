"""623 A5 · 规则触达热力图 + VFDR 验证（可复现）"""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAT = os.path.join(ROOT, "data", "rule_touch_heatmap_623.md")
SUMMARY = os.path.join(ROOT, "data", "_heatmap_summary.json")
A2 = os.path.join(ROOT, "data", "high_complexity_sandbox_run_623.json")
R3 = os.path.join(ROOT, "data", "adversarial_loop_round3_sandbox_run_623.json")
RULES = os.path.join(ROOT, "data", "_gate_rules.json")


def test_heatmap_exists_and_summarizes():
    assert os.path.exists(HEAT)
    txt = open(HEAT, encoding="utf-8").read()
    assert "26/63" in txt or "累计触达" in txt


def test_summary_consistent():
    s = json.load(open(SUMMARY, encoding="utf-8"))
    assert s["total_rules"] == 63
    assert s["touched_cumulative"] == 26
    # 未触达 = 总数 - 触达
    assert len(s["untouched"]) == 63 - s["touched_cumulative"]


def test_cumulative_matches_runs():
    a2 = json.load(open(A2, encoding="utf-8"))
    r3 = json.load(open(R3, encoding="utf-8"))
    rules = json.load(open(RULES, encoding="utf-8"))
    cum = set()
    for res in (a2, r3):
        for r in res["rows"]:
            cum.update(r.get("new_block_rules", []))
            cum.update(r.get("new_nonblock_rules", []))
    assert len(cum) == 26
    assert len(rules) == 63
