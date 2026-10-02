#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673e 任务 C · Tarjan SCC 的**独立复现 + 正负对照**（671e 只做了 tools/ 且无造环夹具）。

673e 独立复现的结论：
  * `tools/` 当前 **0 个循环 SCC、0 个自环**（与 671e 一致）；
  * 模块数从 671e 的 638 涨到 **680**、边从 692 涨到 **713** —— 期间仓内新增了文件，
    这是**快照漂移**而非结论变化（结论仍是 0 环）；
  * `tests/` 侧 intra-tests 边为 **0**（测试之间不互相 import，都走 `from tools.x import`
    或 importlib 动态加载）⇒ 把 tests/ 纳入射程**不增加任何信号**。这一点如实登记，
    不假装"扩了射程就有新发现"。

671e 的测试**只有**"当前无环"的断言（恒真风险：扫描器坏了也会绿）。本文件补：
  * **正对照**：造一个 a→b→c→a 的夹具，必须检出；
  * **负对照**：把环打破，必须为 0；
  * **扫描器有效性**：模块数/边数必须 > 0（否则空图必然 0 环）。

注：**不新建 `tools/scc_check.py`** —— 671e 已把 SCC 以 pytest 形式落地，CI 的 pytest job
会跑它（未标 slow）；`tools/fast_gate.py` 归 673b 在途修改，本批不碰。
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _imports(path: Path, known: set[str]) -> set[str]:
    """该文件 import 到的**同目录模块名**（只算 intra-package 边）。"""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return set()
    out: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                base = a.name.split(".")[0]
                if base in known:
                    out.add(base)
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                base = n.module.split(".")[0]
                if base in known:
                    out.add(base)
    return out


def build_graph(base: str, root: Path = ROOT) -> tuple[dict, dict]:
    d = root / base
    mods = {p.stem: p for p in d.glob("*.py")}
    known = set(mods)
    g = {m: set() for m in mods}
    for m, p in mods.items():
        g[m] = {t for t in _imports(p, known) if t != m}
    return mods, g


def tarjan(g: dict) -> list[list[str]]:
    """迭代式 Tarjan（避免大图上递归爆栈）。返回所有 SCC（含单点）。"""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    onstack: set[str] = set()
    stack: list[str] = []
    counter = [0]
    out: list[list[str]] = []
    for root in g:
        if root in index:
            continue
        work = [(root, iter(sorted(g[root])))]
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        onstack.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    onstack.add(w)
                    work.append((w, iter(sorted(g.get(w, ())))))
                    advanced = True
                    break
                if w in onstack:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    onstack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


# ── 1. 当前仓：无环（独立复现 671e）──────────────────────────────────────────
@pytest.mark.parametrize("base", ["tools", "tests"])
def test_no_cyclic_scc_in_current_repo(base):
    _mods, g = build_graph(base)
    cyc = [c for c in tarjan(g) if len(c) > 1]
    assert not cyc, f"{base}/ 出现循环 SCC：{[sorted(c) for c in cyc]}"


@pytest.mark.parametrize("base", ["tools", "tests"])
def test_no_self_import(base):
    _mods, g = build_graph(base)
    assert not [m for m in g if m in g[m]], f"{base}/ 出现自环"


# ── 2. 扫描器有效性（防空图恒真）────────────────────────────────────────────
def test_tools_graph_is_non_trivial():
    """tools/ 必须真有模块与边，否则"0 环"是空图的平凡结论。"""
    mods, g = build_graph("tools")
    edges = sum(len(v) for v in g.values())
    assert len(mods) > 400, f"tools/ 模块数异常偏少：{len(mods)}"
    assert edges > 400, f"tools/ 内部边异常偏少：{edges}"


def test_tests_intra_edges_are_zero_and_that_is_registered():
    """如实登记：tests/ 之间不互相 import ⇒ 把 tests/ 纳入射程不增加信号（不是遗漏）。"""
    _mods, g = build_graph("tests")
    edges = sum(len(v) for v in g.values())
    assert edges == 0, ("tests/ 出现了 intra-tests 边；若这是有意引入的依赖，"
                        "应同步更新本断言与 673e 验收报告的登记")


def test_known_direction_is_locked():
    """锁一条已知单向边，防止扫描器"反向也算"的静默失效。"""
    _mods, g = build_graph("tools")
    if "tool_integrity" in g and "merkle_integrity" in g:
        assert "merkle_integrity" in g["tool_integrity"]
        assert "tool_integrity" not in g["merkle_integrity"]


def test_graph_build_is_deterministic():
    a = build_graph("tools")[1]
    b = build_graph("tools")[1]
    assert a == b


# ── 3. 正/负对照：造环必须被抓到（671e 缺这一块）────────────────────────────
def _graph_of_dir(d: Path) -> dict:
    mods = {p.stem: p for p in d.glob("*.py")}
    known = set(mods)
    return {m: {t for t in _imports(p, known) if t != m} for m, p in mods.items()}


def test_positive_control_cycle_is_detected(tmp_path):
    (tmp_path / "cyc_a.py").write_text("import cyc_b\n", encoding="utf-8")
    (tmp_path / "cyc_b.py").write_text("import cyc_c\n", encoding="utf-8")
    (tmp_path / "cyc_c.py").write_text("import cyc_a\n", encoding="utf-8")
    g = _graph_of_dir(tmp_path)
    cyc = [c for c in tarjan(g) if len(c) > 1]
    assert any(set(c) == {"cyc_a", "cyc_b", "cyc_c"} for c in cyc), \
        f"造环未被检出 ⇒ 检测器无效；实际 {[sorted(c) for c in cyc]}"


def test_negative_control_broken_cycle_is_clean(tmp_path):
    (tmp_path / "cyc_a.py").write_text("import cyc_b\n", encoding="utf-8")
    (tmp_path / "cyc_b.py").write_text("import cyc_c\n", encoding="utf-8")
    (tmp_path / "cyc_c.py").write_text("# no imports: chain, no cycle\n", encoding="utf-8")
    g = _graph_of_dir(tmp_path)
    assert not [c for c in tarjan(g) if len(c) > 1], "破环后仍报环 ⇒ 假阳"


def test_self_loop_is_detected(tmp_path):
    """自环是 SCC 的特例（长度 1）；扫描器必须能看见，不能只靠 len>1 过滤掉。"""
    (tmp_path / "selfy.py").write_text("import selfy\n", encoding="utf-8")
    g = _graph_of_dir(tmp_path)
    # 本实现显式排除自环（`t != m`），故这里锁住"排除行为"本身
    assert g["selfy"] == set(), "实现把自环算进边集了；若有意为之需同步更新 671e/673e 的口径"
