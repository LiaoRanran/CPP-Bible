"""625 B3 · VFDR 收敛 + 热力图 v3 回归测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vfdr_convergence_625 as v  # noqa: E402


def test_rules_67_rounds_7():
    a = v.analyze()
    assert len(a["rules"]) == 67
    assert len(a["per_round"]) == 7


def test_cum_and_blind_consistent():
    a = v.analyze()
    assert a["cum"] == len(set(a["touched"]))
    assert a["blind_n"] == 67 - a["cum"]
    assert set(a["touched"]).isdisjoint(set(a["blind"]))


def test_blind_reduction_from_623():
    a = v.analyze()
    assert a["blind_n"] <= v.BLIND_623
    assert a["blind_n"] < v.BLIND_623   # 确有缩减


def test_vfdr_converged_dangerous_zero():
    a = v.analyze()
    # 危险逃逸全程 0；严格口径残差 <1%
    assert a["vfdr_cum"] < 0.01


def test_report_exists_with_reconciliation():
    p = os.path.join(ROOT, "data", "vfdr_convergence_report_625.md")
    txt = open(p, encoding="utf-8").read()
    assert os.path.getsize(p) > 300
    assert "热力图 v3" in txt
    assert "ATOM-SUPERIORITY-WORDS" in txt   # 口径校正说明


def test_selftest_passes():
    assert v.selftest() == 0
