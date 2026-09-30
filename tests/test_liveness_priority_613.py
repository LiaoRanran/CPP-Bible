#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""A1 回归测试：liveness_priority_613（活性锚优先级排序，只读）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import liveness_priority_613 as a1  # noqa: E402


def test_all_missing_props_enumerated():
    # 612 已知坑③：C 类命题在候选 jsonl 无行，必须从审计真源枚举
    # 670a 去写死：条数不再冻结 60，取事实源现算（== OBSERVATION-LIVENESS warn 数）
    import liveness_impact as li  # noqa: E402
    rows = a1.build()
    n = li.current_warn_count()
    assert len(rows) == n, f"应枚举 {n} 条缺锚命题，实测 {len(rows)}"
    assert len(a1.load_all_props()) == n


def test_cost_distribution_matches_612_b1():
    """670a 去写死：原写死 9/26/25（612 时点快照）。改为**划分性 + 定义性**断言：
    三档互斥且合计 == 命题总数；每档与 `cost_of` 的 class/confidence 判据一一对应。
    """
    rows = a1.build()
    n = {c: len([r for r in rows if r["cost"] == c]) for c in ("low", "medium", "high")}
    assert sum(n.values()) == len(rows)
    assert all(v > 0 for v in n.values()), n
    assert n["low"] == sum(1 for r in rows if r["class"] == "A"
                           or (r["class"] == "B" and r["confidence"] == "high"))
    assert n["medium"] == sum(1 for r in rows
                              if r["class"] == "B" and r["confidence"] == "medium")
    assert n["high"] == sum(1 for r in rows if r["class"] == "C")


def test_c_class_props_have_no_anchor():
    rows = a1.build()
    for r in rows:
        if r["class"] == "C":
            assert r["best_symbol"] == ""
            assert r["cost"] == "high"


def test_cost_of_rules():
    assert a1.cost_of("A", "medium") == "low"
    assert a1.cost_of("B", "high") == "low"
    assert a1.cost_of("B", "medium") == "medium"
    assert a1.cost_of("C", "low") == "high"


def test_sorted_desc_and_deterministic():
    rows = a1.build()
    ps = [r["priority"] for r in rows]
    assert ps == sorted(ps, reverse=True)
    assert [r["proposition_id"] for r in rows] == [r["proposition_id"] for r in a1.build()]


def test_check_passes():
    assert a1.main(["--check"]) == 0


def test_render_has_sections():
    page = a1.render(a1.build())
    assert "活性锚补全优先级清单" in page
    assert "低成本可批量补全集合" in page
