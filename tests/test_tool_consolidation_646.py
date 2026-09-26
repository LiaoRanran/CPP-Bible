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
    """合并后工具数 ≤12。"""
    res = b4.analyze()
    assert res["core_645_count"] == 15
    assert res["after_merge"] <= 12
    assert res["executed"] is False  # 诚实：只分析不执行
