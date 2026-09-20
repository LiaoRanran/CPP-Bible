#!/usr/bin/env python3
"""A1 回归测试：liveness_priority_613（活性锚优先级排序，只读）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import liveness_priority_613 as a1  # noqa: E402


def test_all_50_props_enumerated():
    # 612 已知坑③：C 类命题在候选 jsonl 无行，必须从审计真源枚举
    rows = a1.build()
    assert len(rows) == 50, f"应枚举 50 条缺锚命题，实测 {len(rows)}"


def test_cost_distribution_matches_612_b1():
    rows = a1.build()
    n = {c: len([r for r in rows if r["cost"] == c]) for c in ("low", "medium", "high")}
    assert n["low"] == 9 and n["medium"] == 26 and n["high"] == 15


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
