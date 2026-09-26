"""646 阶段 A4 · 证据检索提速单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import evidence_index_646 as a4  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（索引与线性扫描命中一致）。"""
    assert a4.selftest() == 0


def test_index_has_entries():
    """索引非空且有倒排与等级索引。"""
    idx = a4.build_index()
    assert idx["inverted"] and idx["by_grade"]
    assert idx["records"]


def test_benchmark_meets_threshold():
    """真实基准：提速 ≥50% 且命中数一致。"""
    res = a4.run()
    assert res["bench"]["met"] is True
    assert res["bench"]["linear_hits"] == res["bench"]["indexed_hits"]
