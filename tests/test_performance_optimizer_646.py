"""646 阶段 A3 · 性能优化基准单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import performance_optimizer_646 as a3  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert a3.selftest() == 0


def test_benchmark_all_met():
    """真实基准：全部工作负载提速 ≥30%。"""
    res = a3.benchmark()
    assert res["total"] >= 3
    assert res["all_met"] is True, res["workloads"]


def test_write_report(tmp_path, monkeypatch):
    """报告写入临时路径。"""
    md = tmp_path / "p.md"
    js = tmp_path / "p.json"
    monkeypatch.setattr(a3, "REPORT_MD", str(md))
    monkeypatch.setattr(a3, "REPORT_JSON", str(js))
    a3.write_report({"workloads": [], "threshold_pct": 30.0, "met_count": 0,
                     "total": 0, "all_met": True})
    assert md.exists() and js.exists()
