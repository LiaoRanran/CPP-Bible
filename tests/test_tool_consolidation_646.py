"""646 阶段 B4 · 工具合并分析单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import tool_consolidation_646 as b4  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert b4.selftest() == 0


def test_analysis_reaches_target():
    """**647 D1 已执行合并**：15 → 10，现存数即合并后数。"""
    res = b4.analyze()
    assert res["core_645_count"] == 10, "647 D1 合并 15→10 后，现存工具数应为 10"
    assert res["after_merge"] <= 12
    assert res["executed"] == "647 D1（已执行）"
    assert len(res["merged_away"]) == 5, res["merged_away"]
