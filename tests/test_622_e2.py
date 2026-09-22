"""622 E2 · 历史版本验证能力曲线（v1–v7）单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import verification_horizon_622 as V  # noqa: E402

CURVE = os.path.join(ROOT, "data", "verification_horizon_curve_622.json")
V7 = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")


def _curve():
    if not os.path.exists(CURVE):
        return None
    return json.load(open(CURVE, encoding="utf-8"))


def test_measure_records_adapter():
    recs = [{"card": "atoms/a.md", "op": "M1", "verdict": "blocked",
             "new_block": ["ATOM-FM-REQUIRED:x"], "new_warn": []},
            {"card": "evidence/b.md", "op": "M9", "verdict": "escaped",
             "new_block": [], "new_warn": []},
            {"card": "atoms/c.md", "op": "M2", "verdict": "n_a",
             "new_block": [], "new_warn": []}]
    res = V.measure_records(recs)
    assert res["total"] == 3
    # n_a 不进分母 ⇒ 可施加 2 条
    assert res["applicable"] == 2


def test_curve_covers_v1_to_v7():
    c = _curve()
    if c is None:
        return
    assert [r["version"] for r in c] == [f"v{i}" for i in range(1, 8)]


def test_escape_rate_trend_down():
    c = _curve()
    if c is None:
        return
    by = {r["version"]: r for r in c}
    assert by["v1"]["escape_rate"] > 0.2      # v1 起点 23.7%
    assert by["v7"]["escape_rate"] < 0.01     # v7 终点 0.64%
    assert by["v1"]["escape_rate"] > by["v7"]["escape_rate"]


def test_denominator_excludes_na_and_equivalent():
    c = _curve()
    if c is None:
        return
    for r in c:
        assert r["denominator"] == r["n"] - r["n_a"] - r["equivalent"]


def test_horizon_is_insensitive_across_versions():
    """E2 的关键方法论发现：Horizon 在 v1–v7 上恒为同一桶（无判别力）。"""
    c = _curve()
    if c is None:
        return
    horizons = {r["horizon_band"] for r in c}
    assert len(horizons) == 1


def test_low_band_detect_rate_improved():
    """真正可比的指标：最低桶检出率 v1 << v7。"""
    c = _curve()
    if c is None:
        return
    by = {r["version"]: r for r in c}
    key = "20-40"
    assert by["v1"]["bands"][key] < by["v7"]["bands"][key]
    assert by["v1"]["bands"][key] < 0.6
    assert by["v7"]["bands"][key] > 0.95


def test_real_v7_records_measurable():
    if not os.path.exists(V7):
        return
    d = json.load(open(V7, encoding="utf-8"))
    recs = d.get("results") or []
    res = V.measure_records(recs)
    assert res["total"] == len(recs)
    assert res["applicable"] > 0
    assert res["horizon_band"] is not None


def test_report_contains_curve_sections():
    p = os.path.join(ROOT, "data", "verification_horizon_curve_622.md")
    if not os.path.exists(p):
        return
    md = open(p, encoding="utf-8").read()
    assert "历史版本验证能力曲线" in md
    assert "Horizon 在本数据上不敏感" in md


def test_selftest_passes():
    assert V.selftest() == 0
