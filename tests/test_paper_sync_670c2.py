#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_paper_sync_670c2.py — 670c2 论文管线五工具的回归测试。

覆盖：paper_sync_check / bib_audit / figure_data_check / anonymity_check / paper_quality_gate。
运行：python -m pytest tests/test_paper_sync_670c2.py -q
"""
from __future__ import annotations

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import paper_sync_check_670c2 as sync  # noqa: E402
import bib_audit_670c2 as bib  # noqa: E402
import figure_data_check_670c2 as fig  # noqa: E402
import anonymity_check_670c2 as anon  # noqa: E402
import paper_quality_gate_670c2 as gate  # noqa: E402


# ---------------- paper_sync_check ----------------

def test_sync_normalize_percent():
    assert sync.normalize("87.5\\%") == "87.5%"


def test_sync_normalize_fullwidth_parens_and_whitespace():
    assert sync.normalize("（14/16）  和\n\t多空格") == "(14/16) 和 多空格"


def test_sync_normalize_dashes():
    assert sync.normalize("A−B–C—D") == "A-B-C-D"


def test_sync_facts_nonempty():
    assert len(sync.FACTS) >= 20


def test_sync_real_docs_consistent():
    res = sync.check()
    assert res["mismatches"] == 0, [r for r in res["rows"] if not r["ok"]]


def test_sync_detects_injected_mismatch(tmp_path, monkeypatch):
    bad_md = tmp_path / "bad.md"
    bad_md.write_text("holdout 0.0% 0/0", encoding="utf-8")
    monkeypatch.setattr(sync, "MD", str(bad_md))
    res = sync.check()
    assert res["mismatches"] >= 1


def test_sync_checks_holdout_ci():
    # 671a 修复：FACTS 的条目在后续批次里从 2 元组变成 3 元组（登记的事实变多），
    # 用例只关心**事实名**，所以按第 0 位取，不再写死解包宽度。
    names = [str(f[0]) for f in sync.FACTS]
    assert names, "FACTS 不该为空"
    assert any("CI" in n for n in names)


# ---------------- bib_audit ----------------

def test_bib_parse_counts():
    text = open(os.path.join(ROOT, "research", "latex", "queyi_refs.bib"), encoding="utf-8").read()
    entries = bib.parse_bib(text)
    assert len(entries) == 48


def test_bib_all_have_title():
    res = bib.audit()
    assert not any("缺字段 title" in e for e in res["errors"])


def test_bib_no_errors():
    res = bib.audit()
    assert res["errors"] == [], res["errors"]


def test_bib_cite_keys_defined():
    res = bib.audit()
    assert not any("不存在" in e for e in res["errors"])


def test_bib_no_unused_entries():
    res = bib.audit()
    assert res["unused_keys"] == [], res["unused_keys"]


def test_bib_doi_format_check_runs():
    # 真实 bib 无格式错误 DOI
    res = bib.audit()
    assert not any("DOI 格式可疑" in e for e in res["errors"])


# ---------------- figure_data_check ----------------

def test_figure_parse_two_plots():
    tex = open(os.path.join(ROOT, "research", "latex", "queyi_neurips2027.tex"), encoding="utf-8").read()
    plots = fig.parse_plots(tex)
    assert len(plots) >= 2


def test_figure_data_passes():
    res = fig.check()
    assert res["errors"] == [], res["errors"]


def test_figure_fig3_matches_holdout_product():
    res = fig.check()
    assert any("holdout_reveal_3_665.json" in s for s in res["ok"])


def test_figure_fig4_values_sourced():
    res = fig.check()
    assert any("660=80.0" in s for s in res["ok"])


# ---------------- anonymity_check ----------------

def test_anonymity_split_main():
    assert anon.split_main("abc\\appendix xyz") == "abc"


def test_anonymity_main_text_clean():
    res = anon.scan()
    assert res["hits"] == [], res["hits"]


def test_anonymity_detects_injected_name(tmp_path, monkeypatch):
    f = tmp_path / "x.tex"
    f.write_text("author LiaoRanran here", encoding="utf-8")
    monkeypatch.setattr(anon, "TEX", str(f))
    res = anon.scan()
    assert res["strict_hits"] >= 1


def test_anonymity_strict_and_main_lists_nonempty():
    assert len(anon.STRICT) >= 5
    assert len(anon.MAIN_ONLY) >= 4


# ---------------- paper_quality_gate ----------------

def test_gate_sections_have_labels():
    res = gate.run()
    c = next(x for x in res["checks"] if "section" in x["check"])
    assert c["ok"], c["detail"]


def test_gate_refs_resolve():
    res = gate.run()
    c = next(x for x in res["checks"] if "ref" in x["check"])
    assert c["ok"], c["detail"]


def test_gate_abstract_word_limit():
    res = gate.run()
    c = next(x for x in res["checks"] if "摘要" in x["check"])
    assert c["ok"], c["detail"]


def test_gate_no_residual_todo():
    res = gate.run()
    c = next(x for x in res["checks"] if "TODO" in x["check"])
    assert c["ok"], c["detail"]


def test_gate_has_at_least_six_checks():
    assert len(gate.run()["checks"]) >= 6
