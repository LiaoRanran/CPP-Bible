#!/usr/bin/env python3
"""C3 回归测试：learner_path_graph_613（推荐路径图 · 拓扑排序）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_path_graph_613 as c3  # noqa: E402


def test_all_kc_present_and_unique():
    kcs = c3.load_kcs()
    adj, indeg = c3.build_graph(kcs)
    order, cyc = c3.topo_sort(kcs, adj, indeg)
    assert len(kcs) == 27
    assert len(order) == 27 and len(set(order)) == 27


def test_no_dependency_inversion():
    kcs = c3.load_kcs()
    adj, indeg = c3.build_graph(kcs)
    order, cyc = c3.topo_sort(kcs, adj, indeg)
    pos = {k: i for i, k in enumerate(order)}
    for k in kcs:
        for p in (k.get("prerequisites") or []):
            if p in pos and p != k["id"] and p not in cyc:
                assert pos[p] < pos[k["id"]], f"{p} 应排在 {k['id']} 之前"


def test_deterministic_order():
    kcs = c3.load_kcs()
    adj, indeg = c3.build_graph(kcs)
    a = c3.topo_sort(kcs, adj, indeg)[0]
    b = c3.topo_sort(kcs, adj, indeg)[0]
    assert a == b


def test_cycle_nodes_are_appended_not_dropped():
    kcs = [{"id": "A", "prerequisites": ["B"], "difficulty": 1},
           {"id": "B", "prerequisites": ["A"], "difficulty": 1},
           {"id": "C", "prerequisites": [], "difficulty": 1}]
    adj, indeg = c3.build_graph(kcs)
    order, cyc = c3.topo_sort(kcs, adj, indeg)
    assert set(order) == {"A", "B", "C"}, "环内节点不得丢失"
    assert set(cyc) == {"A", "B"}


def test_self_loop_ignored():
    kcs = [{"id": "A", "prerequisites": ["A"], "difficulty": 1}]
    adj, indeg = c3.build_graph(kcs)
    assert adj["A"] == set() and indeg["A"] == 0


def test_dangling_prereq_ignored():
    kcs = [{"id": "A", "prerequisites": ["NOPE"], "difficulty": 2}]
    adj, indeg = c3.build_graph(kcs)
    assert indeg["A"] == 0, "悬空前置不应计入入度"


def test_render_contains_path_and_mermaid():
    kcs = c3.load_kcs()
    adj, indeg = c3.build_graph(kcs)
    order, cyc = c3.topo_sort(kcs, adj, indeg)
    page = c3.render(kcs, order, cyc, {}, adj, 0.5)
    assert "推荐学习路径图" in page
    assert "```mermaid" in page
    assert "下一步建议" in page


def test_check_passes():
    assert c3.main(["--check"]) == 0
