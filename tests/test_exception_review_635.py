"""635 V26-4 · exception_review_635 单测（纯标准库，≥5 例）。编号 V4-1..V4-6。"""
from __future__ import annotations

import exception_review_635 as E


# V4-1：来源清单非空
def test_sources():
    assert len(E.SOURCES) >= 6


# V4-2：每条有复审日期
def test_review_dates():
    assert all(r["has_review_date"] for r in E.clauses())


# V4-3：无期豁免 = 0
def test_no_period_waiver():
    assert E.stats()["no_period_waiver"] == []


# V4-4：计数可用
def test_count_entries():
    assert E._count_entries("tools/artifact_producer_exempt.txt") >= 1


# V4-5：stats 结构
def test_stats():
    s = E.stats()
    assert set(s) >= {"total", "existing", "no_period_waiver", "total_entries"}
    assert s["total"] >= 6


# V4-6：--check 自检通过
def test_selftest():
    assert E.selftest() == 0
