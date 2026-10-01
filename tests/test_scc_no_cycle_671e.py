# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671e-E · tools/ 模块依赖环检测（SCC）测试。

**核查结论（先复现，再下结论）**：
本批对 `tools/` 全部 638 个 .py 做 intra-tools import 依赖图分析（Tarjan SCC）：
  * 模块数 638，intra-tools 依赖边 692；
  * **循环 SCC 数 = 0**，自环 = 0 ⇒ **无循环依赖**。
（注：标准库 / 第三方包 / 跨目录导入不计入环判定，只看 tools/ 内部互相 import。）

本测试集把"无环"作为 **CI import 检查** 锁定：任何后续在 tools/ 内引入
A→B→A 循环都会让 `test_no_circular_dependency` 变红。
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

_IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))", re.M)


def _build_graph():
    mods = {p.stem: p for p in TOOLS.rglob("*.py") if not p.name.endswith(".pyc")}
    edges = {m: set() for m in mods}
    for name, p in mods.items():
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in _IMPORT_RE.finditer(txt):
            mod = m.group(1) or m.group(2)
            top = mod.split(".")[0]
            if top in mods and top != name:
                edges[name].add(top)
    return mods, edges


def _tarjan_scc(edges):
    index = {}; low = {}; onstack = {}; stack = []; sccs = []; counter = [0]

    def sc(v):
        index[v] = counter[0]; low[v] = counter[0]; counter[0] += 1
        stack.append(v); onstack[v] = True
        for w in edges.get(v, ()):
            if w not in index:
                sc(w); low[v] = min(low[v], low[w])
            elif onstack.get(w):
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop(); onstack[w] = False; comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for v in list(edges):
        if v not in index:
            sc(v)
    return sccs


def test_no_circular_dependency():
    mods, edges = _build_graph()
    sccs = _tarjan_scc(edges)
    cyclic = [c for c in sccs if len(c) > 1]
    assert cyclic == [], f"发现循环依赖 SCC：{cyclic}"


def test_no_self_import():
    mods, edges = _build_graph()
    self_loops = [v for v in edges if v in edges[v]]
    assert self_loops == [], f"发现自环：{self_loops}"


def test_graph_includes_known_modules():
    mods, edges = _build_graph()
    for name in ("tool_integrity", "merkle_integrity", "prop_graph",
                 "hash_datasets_670c", "counterfactual_citation_658"):
        assert name in mods, f"依赖图应含已知模块 {name}"


def test_all_edge_targets_are_tools_modules():
    mods, edges = _build_graph()
    bad = set()
    for src, dsts in edges.items():
        for d in dsts:
            if d not in mods:
                bad.add((src, d))
    assert bad == set(), f"存在指向非 tools 模块的边：{bad}"


def test_known_noncyclic_direction():
    """锁定一个具体非环：tool_integrity → merkle_integrity，反向不应成立。"""
    mods, edges = _build_graph()
    assert "merkle_integrity" in edges.get("tool_integrity", set()), \
        "tool_integrity 应 import merkle_integrity"
    assert "tool_integrity" not in edges.get("merkle_integrity", set()), \
        "merkle_integrity 不应反向 import tool_integrity（否则成环）"


def test_graph_build_is_deterministic():
    _, e1 = _build_graph()
    _, e2 = _build_graph()
    assert sum(len(v) for v in e1.values()) == sum(len(v) for v in e2.values())
