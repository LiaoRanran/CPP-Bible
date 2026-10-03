# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""646 阶段 A3 · 性能优化基准单测（fast）。"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import performance_optimizer_646 as a3  # noqa: E402


def _kernel_repo_available() -> bool:
    """兄弟仓 `queyi-verifier/tools/queyi_core_v10_641.py` 是否可探测到。

    与 `tests/conftest.py::_kernel_canonical_available` 同口径（自 `tools/` 起向上 8 级）。
    """
    d = os.path.join(ROOT, "tools")
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "queyi-verifier", "tools", "queyi_core_v10_641.py")):
            return True
        d = os.path.dirname(d)
    return False


def test_selftest_passes():
    """--check 只读自检。"""
    assert a3.selftest() == 0


def test_benchmark_all_met():
    """真实基准：全部工作负载提速 ≥30%。"""
    # 674d：`benchmark()` 经 `queyi_data_models_645` 读拆仓内核 ⇒ 单仓检出/CI 上必然
    # RuntimeError（工具 fail-loud 是设计）。条件 skip；双仓布局下行为不变。
    if not _kernel_repo_available():
        pytest.skip("拆仓 queyi-verifier 未检出 ⇒ benchmark() 需内核 canonical（fail-loud）")
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
