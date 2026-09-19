"""609 C1 · 论证可视化回归锁（自包含 HTML + SVG 圆形布局 + 仪表盘 + Top10）。

锁五件事（任务书 5 例 + 2 例自加）：
  1. 真出图：`render` 写出的 HTML **含 SVG/doctype/内联样式**，且 `<script>` 零出现（不引外部 JS）；
  2. 节点数：SVG 里的图形元素个数 == 文档节点数（命题圆 + 误解方）；
  3. 攻击边/支持边：数量与 `defeated_attackers` / `defenders` 派生结果一致；
  4. 仪表盘：IN/OUT/UNDEC 三条 bar 都在；
  5. Top10：最多 10 行且按攻击者数降序；
  +. HTML 转义：节点名含 `<script>` 也不许原样落盘（评审现场不许被注入）；
  +. 结构破 ⇒ `check` 报错、`render` 拒绝出半成品图。
"""
from __future__ import annotations

import json
from pathlib import Path

import grounded_visualizer as gv
import pytest

DOC = gv.load_doc()
NODES = DOC["nodes"]


def test_render_produces_selfcontained_html(tmp_path: Path):
    out = tmp_path / "net.html"
    assert gv.main(["--labels", str(gv.DEFAULT_LABELS), "--out", str(out)]) == 0
    html = out.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in html and "<svg" in html
    assert "<style>" in html and "</style>" in html
    assert "<script" not in html.lower(), "图必须自包含：不许引外部脚本"
    assert "http://" not in html.replace("http://www.w3.org/2000/svg", ""), "不许拉外部资源"


def test_svg_shape_count_matches_nodes(tmp_path: Path):
    svg = gv.build_svg(NODES)
    circles = svg.count("<circle")
    rects = svg.count("<rect") - 1            # 减掉背景底色 rect
    assert circles + rects == len(NODES), f"图形数 {circles + rects} ≠ 节点数 {len(NODES)}"
    props = sum(1 for v in NODES.values() if v["type"] == "proposition")
    assert circles == props and rects == len(NODES) - props


def test_edge_counts_match_derived_relations():
    assert len(gv.attack_edges(NODES)) == sum(
        len(v["defeated_attackers"]) for v in NODES.values())
    assert len(gv.support_edges(NODES)) == sum(
        1 for v in NODES.values() for d in v["defenders"] if d in NODES)


def test_dashboard_and_top10(tmp_path: Path):
    out = tmp_path / "net.html"
    gv.render(out=out)
    html = out.read_text(encoding="utf-8")
    for k in ("IN", "OUT", "UNDEC"):
        assert f'class="k">{k}</td>' in html, f"仪表盘缺 {k}"
    rows = gv.top_targets(NODES)
    assert len(rows) <= gv.TOP_N
    assert all(rows[i]["attackers"] >= rows[i + 1]["attackers"] for i in range(len(rows) - 1))
    assert "Top10" in html


def test_node_names_are_html_escaped(tmp_path: Path):
    """节点名里塞 `<script>` ⇒ 必须被转义，不许原样进 HTML。"""
    nodes = {"<script>alert(1)</script>": {"type": "proposition", "label": "IN",
                                          "credibility": 2, "attackers": [],
                                          "defended": [], "defenders": [],
                                          "defeated_attackers": []},
             "X": {"type": "misconception", "label": "OUT", "credibility": 1,
                   "attackers": ["<script>alert(1)</script>"], "defenders": [],
                   "defeated_attackers": []}}
    html = gv.render_html({"nodes": nodes, "summary": {"nodes": 2, "IN": 1, "OUT": 1,
                                                       "UNDEC": 0}, "rounds": 1,
                           "defeating_edges": 0, "edges": 0})
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_check_rejects_broken_doc(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"nodes": {"A": {"type": "who-knows", "label": "MAYBE"}},
                               "summary": {"nodes": 2}}), encoding="utf-8")
    assert gv.check(bad) != []
    with pytest.raises(SystemExit):
        gv.load_doc(tmp_path / "missing.json")


def test_real_labels_document_checks_green():
    assert gv.check() == []
    assert len(NODES) == 121
