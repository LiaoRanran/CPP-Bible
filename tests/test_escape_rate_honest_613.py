#!/usr/bin/env python3
"""F1 回归测试：escape_rate_honest_613（逃逸率多口径 + 双侧 Wilson CI）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import escape_rate_honest_613 as f1  # noqa: E402


def test_baseline_is_v7_and_counts():
    p, d = f1.latest_baseline()
    assert "v7" in p.name
    assert int(d["blocked"]) == 1405 and int(d["escaped"]) == 1
    assert int(d["n_a"]) == 179 and int(d["equivalent"]) == 8


def test_official_rate_is_one_over_1406():
    _p, d = f1.latest_baseline()
    rs = {r["name"][0]: r for r in f1.rates(d)}
    assert rs["①"]["k"] == 1 and rs["①"]["n"] == 1406


def test_conservative_bound_is_much_larger():
    """诚实化的核心：官方口径与最保守上界差两个数量级。"""
    _p, d = f1.latest_baseline()
    rs = {r["name"][0]: r for r in f1.rates(d)}
    assert rs["④"]["p"] > rs["①"]["p"] * 50


def test_wilson_interval_edges():
    lo, hi = f1.wilson(0, 10)
    assert lo == 0.0 and 0 < hi < 1
    lo2, hi2 = f1.wilson(10, 10)
    assert abs(hi2 - 1.0) < 1e-9 and 0 < lo2 < 1
    lo3, hi3 = f1.wilson(0, 0)
    assert (lo3, hi3) == (0.0, 1.0)


def test_wilson_brackets_point_estimate():
    _p, d = f1.latest_baseline()
    for r in f1.rates(d):
        if r["n"]:
            assert r["lo"] <= r["p"] <= r["hi"]


def test_report_discloses_exclusions():
    p, d = f1.latest_baseline()
    page = f1.render(p, d, f1.rates(d))
    assert "冻结 TCE" in page
    assert "equivalent_invalid" in page
    assert "两个数量级" in page


def test_check_passes():
    assert f1.main(["--check"]) == 0
