#!/usr/bin/env python3
"""615 C3 回归测试：goodhart_monitor（Goodhart 漂移监控）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import goodhart_monitor as gm  # noqa: E402


def test_metric_computation() -> None:
    d = gm.compute()
    assert 0.0 <= d["score"] <= 100.0
    for v in d["subscores"].values():
        assert v is None or (0.0 <= v <= 20.0)
    assert d["known_subscores"] >= 3


def test_trend_analysis() -> None:
    d = gm.compute()
    ws = d["warn_series"]
    if len(ws) >= 2:
        expect = round((ws[-1] - ws[0]) / (len(ws) - 1), 2)
        assert d["warn_growth_per_batch"] == expect
    assert d["legacy_rules"] >= 1


def test_check_consistency() -> None:
    assert gm.check() == []
