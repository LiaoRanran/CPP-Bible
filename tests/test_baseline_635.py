"""635 任务0 · baseline_635 单测（纯标准库，≥5 例）。编号 T0-1..T0-6。"""
from __future__ import annotations

import baseline_635 as B


# T0-1：工具/测试计数
def test_counts():
    assert B.count_tools() > 100
    assert B.count_tests() > 100


# T0-2：规则数 = 67
def test_rules():
    assert B.count_rules() == 67


# T0-3：atom/verified 统计
def test_atom_stats():
    a = B.atom_stats()
    assert a["atom_cards"] >= 1 and a["verified_cards"] >= 1


# T0-4：coverage / horizon / na 可读
def test_metrics_readable():
    assert B.coverage_pct() == 100.0
    assert B.horizon_60_80() == 1.0
    assert B.na_rate_pct() == 11.24


# T0-5：snapshot 结构完整（14 键）
def test_snapshot():
    s = B.snapshot()
    assert set(s) >= {"gate_rules", "coverage_pct", "tools_total", "tests_total",
                      "commits", "local_ahead", "dirty_files", "verified_cards",
                      "baseline_files", "exception_clause_hits"}


# T0-6：--check 自检通过
def test_selftest():
    assert B.selftest() == 0
