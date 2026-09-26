"""646 阶段 A6 · R5 扩样本单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import loop_r5_runner_646 as a6  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert a6.selftest() == 0


def test_run_reports_both_calibers():
    """扩样本重算：两个口径都返回，且与样本数一致。"""
    res = a6.run()
    assert res["rules"] == 67
    assert 0.0 <= res["R5_expanded_modify"] <= 1.0
    assert 0.0 <= res["R5_expanded_independent"] <= 1.0
    assert res["R5_645_narrow"] == 1.0
