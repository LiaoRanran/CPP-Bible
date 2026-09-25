"""635 V26-1 · error_cost_ratio_635 单测（纯标准库，≥5 例）。编号 V1-1..V1-6。"""
from __future__ import annotations

import error_cost_ratio_635 as E


# V1-1：逃逸率计算
def test_escape():
    assert abs(E.metrics()["escape_pct"] - 0.0711) < 0.001


# V1-2：当前误报 0
def test_autoimmune_now():
    assert E.metrics()["autoimmune_now_pct"] == 0.0


# V1-3：历史误报 ≈14.29
def test_autoimmune_hist():
    assert abs(E.metrics()["autoimmune_hist_pct"] - 14.2857) < 0.01


# V1-4：配比无界
def test_ratio():
    assert "∞" in E.metrics()["ratio_now"]
    assert ":1" in E.metrics()["ratio_hist"]


# V1-5：有明确立场
def test_verdict():
    assert "可接受" in E.verdict(E.metrics())


# V1-6：--check 自检通过
def test_selftest():
    assert E.selftest() == 0
