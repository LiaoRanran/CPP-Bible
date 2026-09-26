"""646 阶段 B5 · 注释质量单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import docstring_quality_646 as b5  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert b5.selftest() == 0


def test_audit_avg_high():
    """真实抽查：平均分 ≥4（改进后）。647 D1 合并删除的成员**自动跳过并登记**。"""
    res = b5.audit()
    assert res["sample"] >= 15
    assert res["avg_score"] >= 4.0
    assert len(res["skipped_missing"]) == 5, res["skipped_missing"]


def test_no_low_scores():
    """无低于 4 分的工具（改进后）。"""
    res = b5.audit()
    low = [n for n, r in res["rows"].items() if r["score"] < 4]
    assert low == [], low
