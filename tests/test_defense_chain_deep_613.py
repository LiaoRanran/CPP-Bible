#!/usr/bin/env python3
"""D3 回归测试：defense_chain_deep_613（防御深度 / 单点依赖 / 共同依赖）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import defense_chain_deep_613 as d3  # noqa: E402


def test_node_count():
    assert len(d3.load_nodes()) == 121


def test_depth_covers_all_nodes_and_is_deterministic():
    c = d3.compute(d3.load_nodes())
    assert len(c["depth"]) == c["n_nodes"] == 121
    assert c["depth"] == d3.compute(d3.load_nodes())["depth"]
    assert all(v >= 0 for v in c["depth"].values())


def test_cycle_is_cut_not_infinite():
    nodes = {"A": {"DEFENDERS": ["B"]}, "B": {"DEFENDERS": ["A"]}}
    c = d3.compute(nodes)
    assert set(c["depth"]) == {"A", "B"}, "环必须被截断而非死循环"
    assert c["max_depth"] <= 2


def test_bare_node_has_zero_depth():
    nodes = {"A": {"DEFENDERS": []}, "B": {"DEFENDERS": ["A"]}}
    c = d3.compute(nodes)
    assert c["depth"]["A"] == 0 and c["depth"]["B"] == 1
    assert "A" in c["bare"] and "B" in c["single_point"]


def test_chain_depth_is_multi_hop():
    nodes = {"A": {"DEFENDERS": []}, "B": {"DEFENDERS": ["A"]}, "C": {"DEFENDERS": ["B"]}}
    c = d3.compute(nodes)
    assert c["depth"]["C"] == 2, "C→B→A 应为 2 跳"


def test_load_bearing_shared_defenders():
    nodes = {f"N{i}": {"DEFENDERS": ["SHARED"]} for i in range(4)}
    c = d3.compute(nodes)
    assert c["load"]["SHARED"] == 4
    assert "SHARED" in c["shared"]


def test_render_sections():
    page = d3.render(d3.compute(d3.load_nodes()))
    assert "辩护链深化报告" in page
    assert "防御深度分布" in page and "承重辩护者" in page and "单点依赖" in page


def test_check_passes():
    assert d3.main(["--check"]) == 0
