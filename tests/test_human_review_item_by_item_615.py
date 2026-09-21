#!/usr/bin/env python3
"""615 A2 回归测试：human_review_item_by_item_615（逐条复核决策清单）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import human_review_item_by_item_615 as a2  # noqa: E402


def test_selection_no_duplicates() -> None:
    items = a2.select(a2._load(a2.ANNOTATIONS), {})
    assert len(items) == 30
    ids = [it["edge_id"] for it in items]
    assert len(set(ids)) == 30  # 无重复


def test_decision_list_format() -> None:
    assert a2.OUT.is_file()
    text = a2.OUT.read_text(encoding="utf-8")
    assert "逐条复核决策清单" in text
    assert "需人回答" in text          # 每条含待人回答的是非题
    assert "判断要点" in text
    # 表格里 30 行边
    assert sum(1 for ln in text.splitlines() if ln.startswith("| ") and "`ae-" in ln) >= 30


def test_out_mis_edges_all_selected() -> None:
    recs = a2._load(a2.ANNOTATIONS)
    items = a2.select(recs, {})
    ids = {it["edge_id"] for it in items}
    out_fwd = {r["edge_id"] for r in recs
               if (p := a2.parse_edge(r["edge_id"])) and p["direction"] == "fwd"
               and p["mis"] in a2.OUT_MIS}
    assert out_fwd, "OUT7 应至少有正向边"
    assert out_fwd <= ids, "OUT7 正向攻击边必须全部入选"
