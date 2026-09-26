"""644 B4 证据质量联调报告单测（R4-1..R4-4）。"""
from __future__ import annotations

import evidence_base_644 as base
import evidence_grade_report_644 as b4


# R4-1：报告非空且统计准确
def test_build_consistent():
    r = b4.build()
    assert r["n_evidence"] > 0
    assert sum(r["grade_distribution"].values()) == r["n_evidence"]
    sc = r["sufficiency_counts"]
    assert sc["充分"] + sc["不足"] + sc["需人审"] == r["n_cards"]


# R4-2：Top 10 合理（≤10）
def test_top10():
    r = b4.build()
    assert len(r["weakest_top10"]) <= 10
    assert len(r["weakest_top10"]) > 0


# R4-3：冲突统计非负
def test_conflict_counts():
    r = b4.build()
    assert r["n_conflicts"] >= 0
    assert r["conflict_cards"] >= 0


# R4-4：selftest 通过
def test_selftest():
    assert b4.selftest() == 0
