"""622 E1 · Verification Horizon 测量 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import verification_horizon_622 as V  # noqa: E402


def _row(mid, verdict, card="atoms/a.md", **kw):
    r = {"mutation_id": mid, "card": card, "verdict": verdict}
    r.update(kw)
    return r


def _mut(mid, op, card="atoms/a.md"):
    return {"mutation_id": mid,
            "content": json.dumps({"op": op, "target_card": card})}


def test_weights_sum_to_one():
    assert round(sum(V.WEIGHTS.values()), 10) == 1.0


def test_rule_complexity_monotonic():
    assert V.rule_complexity(0) == 0.0
    assert V.rule_complexity(1) < V.rule_complexity(2) < V.rule_complexity(3)


def test_complexity_dims_and_range():
    cx = V.complexity(_row("x", "blocked", new_block_rules=["R1"]), _mut("x", "M1"))
    assert set(cx) >= {"syntax", "semantic", "evidence", "rule", "complexity_score"}
    for k in ("syntax", "semantic", "evidence", "rule"):
        assert 0.0 <= cx[k] <= 1.0
    assert 0 <= cx["complexity_score"] <= 100


def test_band_of():
    assert V.band_of(0) == "0-20"
    assert V.band_of(19.9) == "0-20"
    assert V.band_of(45) == "40-60"
    assert V.band_of(85) == "80-100"


def test_is_detected_semantics():
    assert V.is_detected("blocked") is True
    assert V.is_detected("escaped") is False
    assert V.is_detected("neutral") is False
    assert V.is_detected("infra_error") is None


def test_measure_bands_and_horizon():
    rows = [_row("a", "blocked", new_block_rules=["R1"]),
            _row("b", "blocked", new_block_rules=["R1"]),
            _row("c", "neutral")]
    by = {"a": _mut("a", "M1"), "b": _mut("b", "M1"), "c": _mut("c", "M9")}
    res = V.measure(rows, by)
    assert res["total"] == 3
    assert res["applicable"] == 3
    assert isinstance(res["bands"], dict) and res["bands"]
    assert res["horizon_band"] is None or "-" in res["horizon_band"]


def test_infra_error_excluded_from_denominator():
    rows = [_row("a", "blocked"), _row("b", "infra_error")]
    by = {"a": _mut("a", "M1"), "b": _mut("b", "M1")}
    res = V.measure(rows, by)
    assert res["total"] == 2
    assert res["applicable"] == 1


def test_real_artifacts():
    p = os.path.join(ROOT, "data", "verification_horizon_622.json")
    if not os.path.exists(p):
        return
    d = json.load(open(p, encoding="utf-8"))
    assert d["total"] == 80
    assert d["threshold"] == 0.5
    assert "60-80" in d["bands"]
    assert d["bands"]["60-80"]["detect_rate"] == 0.0


def test_render_contains_horizon():
    rows = [_row("a", "blocked")]
    by = {"a": _mut("a", "M1")}
    md = V.render(V.measure(rows, by))
    assert "Verification Horizon" in md
    assert "Horizon 桶" in md


def test_selftest_passes():
    assert V.selftest() == 0
