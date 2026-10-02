#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673e 任务 E · undefined / zero_division 的**独立复现 + 射程扩大**。

671e 只查了**反事实算子**（结论：全项目 0 处 sklearn，P/R/F1 是纯算术且已 `else 0.0` 防除零）。
673e 独立复现确认了这一点，并把射程扩到**全仓所有指标计算站点**，新发现：

  * 全仓 `sklearn` / `zero_division` 只出现在 671e 自己的测试文件里（作为**被断言的字符串**），
    没有任何生产代码依赖它们 —— 复现成立；
  * 除反事实算子外，其余算 rate / P / R / F1 的站点**也都做了除零保护**
    （`if n else 0.0`、`max(1, n)`、`if denom else 0.0`）；
  * 有 **2 处** 除以**冻结常量**（`escape_rate_estimand.FROZEN`、`autoimmune_dashboard_629.ESCAPE`），
    没有显式守卫 —— 但常量恒 > 0 ⇒ **不是缺陷**，只是"靠构造成立"。按最小修复原则，
    本批**不改代码**，改为**加测试锁住"常量 > 0"**（把隐式前提变成显式断言）。
"""
from __future__ import annotations

import ast
import importlib.util
import json
import math
import sqlite3  # noqa: F401  (占位：保持与 671e 同风格的可导入面)
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def _load(name: str, filename: str):
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(name, TOOLS / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ── 1. 全仓：sklearn / zero_division 不存在于生产代码 ────────────────────────
def test_no_sklearn_in_production_code():
    hits = []
    for base in ("tools",):
        for p in (ROOT / base).rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            if "sklearn" in p.read_text(encoding="utf-8", errors="ignore"):
                hits.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    assert not hits, f"生产代码出现 sklearn（zero_division 机制会被引入）：{hits}"


def test_no_zero_division_param_in_production_code():
    hits = []
    for base in ("tools",):
        for p in (ROOT / base).rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            if "zero_division" in p.read_text(encoding="utf-8", errors="ignore"):
                hits.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    assert not hits, f"生产代码出现 zero_division 参数：{hits}"


#: 扫描时要跳过的目录（实测：不过滤 `.venv` 会让本文件的整仓扫描跑 4 分钟以上）。
SKIP_DIRS = frozenset({
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".ruff_cache", ".pytest_tmp", "dist", "build", "site-packages",
})


def _iter_py(base: Path):
    """按目录剪枝遍历 .py（`rglob` 无法剪枝，会爬进 .venv ⇒ 本文件曾因此跑 4min+）。"""
    stack = [base]
    while stack:
        d = stack.pop()
        try:
            entries = list(d.iterdir())
        except OSError:
            continue
        for e in entries:
            if e.is_dir():
                if e.name not in SKIP_DIRS:
                    stack.append(e)
            elif e.suffix == ".py":
                yield e


def test_sklearn_only_mentioned_inside_test_files():
    """射程说明：全仓出现 sklearn 的地方只应是测试文件里的**字符串断言**。"""
    hits = []
    for p in _iter_py(ROOT):
        if "sklearn" in p.read_text(encoding="utf-8", errors="ignore"):
            hits.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    assert all(h.startswith("tests/") for h in hits), f"非测试文件出现 sklearn：{hits}"


# ── 2. 反事实算子：真实计数 + 纯算术防除零 ───────────────────────────────────
def test_counterfactual_extend_guards_all_three_denominators():
    src = (TOOLS / "counterfactual_extend_665.py").read_text(encoding="utf-8")
    assert "prec = tp / (tp + fp) if (tp + fp) else 0.0" in src
    assert "rec = tp / (tp + fn) if (tp + fn) else 0.0" in src
    assert "f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0" in src


def test_counterfactual_calibration_guards_all_three_denominators():
    """673e 新增射程：另一处算 P/R/F1 的站点也必须防除零。"""
    src = (TOOLS / "counterfactual_calibration_662.py").read_text(encoding="utf-8")
    assert "prec = tp / (tp + fp) if (tp + fp) else 0.0" in src
    assert "rec = tp / (tp + fn) if (tp + fn) else 0.0" in src
    assert "f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0" in src


def test_guard_returns_zero_not_nan_on_empty_confusion_matrix():
    """PoC：tp=fp=fn=0（全空）时，守卫必须给 0.0，绝不能是 NaN 或抛异常。"""
    tp = fp = fn = 0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    assert (prec, rec, f1) == (0.0, 0.0, 0.0)
    assert not math.isnan(f1)


def test_bare_division_would_raise_so_the_guard_is_necessary():
    """对照：裸除法确实会抛 ⇒ 守卫不是装饰。"""
    tp = fp = 0
    with pytest.raises(ZeroDivisionError):
        _ = tp / (tp + fp)


def test_counterfactual_dataset_counts_are_reproducible():
    """不抄报告：从落盘数据现算混淆矩阵。"""
    data = json.loads((ROOT / "data" / "counterfactual_cases_665.json").read_text(encoding="utf-8"))
    cases = data if isinstance(data, list) else data.get("cases", [])
    assert len(cases) == 10, f"案例数应为 10，实际 {len(cases)}"
    conf = data.get("confusion") if isinstance(data, dict) else None
    if conf:
        tp, fp, tn, fn = conf["tp"], conf["fp"], conf["tn"], conf["fn"]
        assert (tp + fp + tn + fn) == len(cases), "混淆矩阵总数与案例数不符"
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
        assert round(prec, 6) == round(float(data["scores"]["precision"]), 6)
        assert round(rec, 6) == round(float(data["scores"]["recall"]), 6)
        assert round(f1, 6) == round(float(data["scores"]["f1"]), 6), \
            "落盘 F1 与现算不一致 ⇒ 数字来源存疑"


# ── 3. 673e 新发现：两处"除以冻结常量"（非缺陷，加测试把隐式前提显式化）────────
def test_escape_rate_frozen_denominators_are_positive():
    """`escape_rate_estimand.layer_l1` 的 `k / n` 没有守卫 ⇒ n 必须恒 > 0（锁住这个前提）。"""
    m = _load("_ere_673e", "escape_rate_estimand.py")
    for t in ("blocked", "escaped", "equivalent"):
        l1 = m.layer_l1(t)
        assert l1["n"] > 0, f"{t} 的 n={l1['n']} ⇒ k/n 会 ZeroDivisionError"
        assert 0 <= l1["k"] <= l1["n"]
        assert abs(l1["rate"] - l1["k"] / l1["n"]) < 1e-12


def test_escape_rate_selftest_passes():
    m = _load("_ere2_673e", "escape_rate_estimand.py")
    assert m.selftest() == [], "escape_rate_estimand 自检未通过"


def test_autoimmune_dashboard_escape_total_is_positive():
    """`autoimmune_dashboard_629._card_escape` 的 `hits / total` 无守卫 ⇒ total 必须 > 0。"""
    src = (TOOLS / "autoimmune_dashboard_629.py").read_text(encoding="utf-8")
    assert 'ESCAPE["total"]' in src, "站点形态变了，本测试需同步更新"
    import re
    m = re.search(r"ESCAPE\s*=\s*\{(.*?)\}", src, re.S)
    assert m, "未找到 ESCAPE 常量定义"
    total = re.search(r"[\"']total[\"']\s*:\s*(\d+)", m.group(1))
    assert total and int(total.group(1)) > 0, f"ESCAPE['total'] 不是正数：{total}"


# ── 4. 其余 rate 站点的保护形态（抽查，防将来改坏）──────────────────────────
@pytest.mark.parametrize("tool,needle", [
    ("external_corpus_reveal_665.py", "if denom else 0.0"),
    ("defect_fixture_658.py", "if total_re else 0.0"),
    ("ev_matrix_dual_impl_lock.py", "if applicable else 0.0"),
    ("atom_coverage_map.py", "max(1, total)"),
])
def test_rate_sites_keep_their_guards(tool, needle):
    src = (TOOLS / tool).read_text(encoding="utf-8")
    assert needle in src, f"{tool} 的除零保护形态变了（期望含 {needle!r}）"


def test_no_expression_actually_divides_by_a_zero_literal():
    """**AST 级**检查：只认真正的除法表达式（`ast.BinOp` + `ast.Div` + 常量 0 除数）。

    为什么不用正则（673e 实测踩到）：正则 `/\\s*0` 会把字符串与文档里的 `0/0`、`tools/ 0 errors`
    之类全判成"除零"，一次跑出几十条假阳 —— 正是"调研阶段候选必须提高复现阈值"的反例。
    """
    bad = []
    for p in _iter_py(ROOT / "tools"):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)):
                continue
            r = node.right
            if isinstance(r, ast.Constant) and isinstance(r.value, (int, float)) and r.value == 0:
                bad.append(f"{p.relative_to(ROOT)}:{node.lineno}")
    assert not bad, "发现真·除零表达式：\n" + "\n".join(bad)


def test_ast_scanner_is_not_vacuous():
    """扫描器有效性：至少扫到一批除法表达式，否则"零命中"是平凡结论。"""
    divs = 0
    for p in _iter_py(ROOT / "tools"):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        divs += sum(1 for n in ast.walk(tree)
                    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div))
    assert divs > 100, f"tools/ 只扫到 {divs} 个除法表达式 ⇒ 扫描器可能失效"
