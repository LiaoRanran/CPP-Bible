"""622 A5 · VFDR 计算 + 趋势 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import vfdr_calculator_622 as V  # noqa: E402


def _rounds():
    return [
        {"name": "a", "budget": 100, "escaped": 0, "source": "s", "verdict_mode": "v"},
        {"name": "b", "budget": 50, "escaped": 5, "source": "s", "verdict_mode": "v"},
        {"name": "c", "budget": 50, "escaped": 5, "source": "s", "verdict_mode": "v"},
    ]


def test_cumulative_totals():
    r = V.vfdr(_rounds())
    assert r["total_budget"] == 200
    assert r["total_escaped"] == 10
    assert r["vfdr_final"] == 0.05


def test_per_round_escape_rate():
    rows = V.vfdr(_rounds())["rows"]
    assert rows[0]["escape_rate"] == 0.0
    assert rows[1]["escape_rate"] == 0.1
    assert rows[2]["cum_escaped"] == 10


def test_trend_slope_and_series():
    r = V.vfdr(_rounds())
    assert r["series"] == [0, 5, 5]
    assert r["slope"] > 0
    assert r["flat_zero"] is False


def test_flat_zero_single_round():
    r = V.vfdr([{"name": "x", "budget": 10, "escaped": 0, "source": "s",
                 "verdict_mode": "v"}])
    assert r["flat_zero"] is True
    assert r["slope"] is None
    assert r["vfdr_final"] == 0.0


def test_empty_rounds_safe():
    r = V.vfdr([])
    assert r["total_budget"] == 0
    # 无预算 ⇒ VFDR 未定义（None），而不是伪装成 0
    assert r["vfdr_final"] is None


def test_load_real_rounds():
    rounds = V.load_rounds()
    assert len(rounds) >= 2
    assert rounds[0]["budget"] == 1406
    assert all("source" in r for r in rounds)


def test_real_report_is_flat_zero():
    res = V.vfdr(V.load_rounds())
    assert res["flat_zero"] is True
    assert res["vfdr_final"] == 0.0
    assert res["series"][-1] == 0


def test_render_contains_comparison():
    md = V.render(V.vfdr(V.load_rounds()))
    assert "VFDR 真正计算" in md
    assert "与 620/621 的 VFDR 对比" in md


def test_json_artifact_matches():
    p = os.path.join(ROOT, "data", "vfdr_report_622.json")
    if not os.path.exists(p):
        return
    d = json.load(open(p, encoding="utf-8"))
    assert d["flat_zero"] is True
    assert len(d["rows"]) >= 2


def test_selftest_passes():
    assert V.selftest() == 0
