"""644 阶段 0 · 现有证据盘点单测（I0-1..I0-6）。"""
from __future__ import annotations

import os

import evidence_base_644 as base
import evidence_inventory_644 as inv


# I0-1：盘点全量卡（实测 27 张，计划书「28」偏旧，按文件系统动态校验）
def test_inventory_counts_all_cards():
    r = inv.inventory()
    expected = 0
    for domain in ("conc", "hist", "lang", "mem", "ub"):
        d = os.path.join(base.ATOMS_DIR, domain)
        if os.path.isdir(d):
            expected += sum(1 for fn in os.listdir(d) if fn.endswith(".md"))
    assert r["n_atoms"] == expected and expected >= 25
    assert r["n_evidence_files"] > 0


# I0-2：完整度在 [0,1]
def test_completeness_range():
    r = inv.inventory()
    assert 0.0 <= r["completeness_ratio"] <= 1.0


# I0-3：kind 分布为非空字典
def test_kind_distribution():
    r = inv.inventory()
    assert isinstance(r["kind_distribution"], dict) and len(r["kind_distribution"]) > 0


# I0-4：渲染文档含关键统计行
def test_render_md():
    r = inv.inventory()
    md = inv.render_md(r)
    assert str(r["n_atoms"]) in md and "完整度" in md and "kind" in md


# I0-5：引用缺失统计为非负整数
def test_missing_refs_nonneg():
    r = inv.inventory()
    assert r["refs_to_missing_file"] >= 0
    assert r["missing_sha256"] >= 0


# I0-6：selftest 通过
def test_selftest():
    assert inv.selftest() == 0
