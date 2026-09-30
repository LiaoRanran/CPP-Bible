#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_gate_rules_670g.py — 670g 六条 P0 门禁的回归测试（每条 ≥1 正 1 反）。

运行：python -m pytest tests/test_gate_rules_670g.py -q
"""
from __future__ import annotations

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import gate_rules_670g as g  # noqa: E402


def mk(tmp_path, paper_text=None, baseline=True, caliber=True):
    """构造一个最小仓库根。"""
    (tmp_path / "research").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data" / "experiments").mkdir(parents=True, exist_ok=True)
    if paper_text is not None:
        (tmp_path / "research" / "paper_v0.8.md").write_text(paper_text, encoding="utf-8")
    if caliber:
        (tmp_path / "research" / "669d_统计口径.md").write_text("CP 口径", encoding="utf-8")
    if baseline:
        for name in ("baseline_fd", "baseline_static", "baseline_random"):
            (tmp_path / "data" / "experiments" / f"{name}.json").write_text(
                json.dumps({"schema": "queyi-baseline/v1"}), encoding="utf-8")
    return tmp_path


GOOD_PAPER = (
    "holdout 87.5% (14/16) [61.7, 98.4]；Static 6.2% (1/16)；corpus 43.8% (14/32) / 12.5% (4/32)。"
    "统计口径见 research/669d_统计口径.md，区间为 Clopper–Pearson。"
    "semantic scope 完整度 0/26。**优于**静态口径臂。IRR：第二标注者 0 人（缺口）。"
)


# ── 正例：真实仓库应 0 block ──
def test_real_repo_no_block():
    from pathlib import Path
    findings = g.run_all(Path(ROOT))
    blocks = [f for f in findings if f["severity"] == "block"]
    assert blocks == [], blocks


def test_real_repo_has_six_rules():
    assert len(g.RULES) == 6


# ── G-RATE-CONSISTENCY ──
def test_rate_consistency_pass(tmp_path):
    assert g.check_rate_consistency(mk(tmp_path, GOOD_PAPER)) == []


def test_rate_consistency_missing_kn(tmp_path):
    r = g.check_rate_consistency(mk(tmp_path, "holdout 87.5% 但没有计数"))
    assert any(f["rule"] == "G-RATE-CONSISTENCY" for f in r)


def test_rate_consistency_warn_without_baseline(tmp_path):
    r = g.check_rate_consistency(mk(tmp_path, GOOD_PAPER, baseline=False))
    assert any(f["severity"] == "warn" for f in r)


# ── G-DENOMINATOR ──
def test_denominator_pass(tmp_path):
    assert g.check_denominator(mk(tmp_path, "holdout 87.5% (14/16)")) == []


def test_denominator_flags_bare_pct(tmp_path):
    r = g.check_denominator(mk(tmp_path, "corpus 检出 43.8 个百分点，没有分母"))
    assert isinstance(r, list)   # 结构正确
    r2 = g.check_denominator(mk(tmp_path, "检出率 43.8%，未给分母"))
    assert any(f["rule"] == "G-DENOMINATOR" for f in r2)


def test_denominator_skips_ci_context(tmp_path):
    assert g.check_denominator(mk(tmp_path, "区间 CP 95% 置信水平")) == []


def test_denominator_skips_code_fence(tmp_path):
    assert g.check_denominator(mk(tmp_path, "```\n# 87.5% 注释\n```")) == []


# ── G-STATS-FROZEN ──
def test_stats_frozen_pass(tmp_path):
    assert g.check_stats_frozen(mk(tmp_path, GOOD_PAPER)) == []


def test_stats_frozen_blocks_without_ref(tmp_path):
    r = g.check_stats_frozen(mk(tmp_path, "本文用了一些统计方法。"))
    assert any(f["severity"] == "block" for f in r)


def test_stats_frozen_warns_missing_doc(tmp_path):
    r = g.check_stats_frozen(mk(tmp_path, GOOD_PAPER, caliber=False))
    assert any(f["severity"] == "warn" for f in r)


# ── G-BOUNDARY-REQUIRED ──
def test_boundary_pass(tmp_path):
    assert g.check_boundary_required(mk(tmp_path, GOOD_PAPER)) == []


def test_boundary_blocks_without_gap_note(tmp_path):
    r = g.check_boundary_required(mk(tmp_path, "scope 全部完成。"))
    assert any(f["severity"] == "block" for f in r)


# ── G-BASELINE-EXISTS ──
def test_baseline_exists_pass(tmp_path):
    assert g.check_baseline_exists(mk(tmp_path, GOOD_PAPER)) == []


def test_baseline_blocks_claim_without_data(tmp_path):
    r = g.check_baseline_exists(mk(tmp_path, "本方法显著优于现有方法。", baseline=False))
    assert any(f["severity"] == "block" for f in r)


def test_baseline_no_claim_no_finding(tmp_path):
    assert g.check_baseline_exists(mk(tmp_path, "本文只描述机制。", baseline=False)) == []


# ── G-IRR ──
def test_irr_pass_with_gap_registered(tmp_path):
    assert g.check_irr(mk(tmp_path, GOOD_PAPER)) == []


def test_irr_warns_without_registration(tmp_path):
    r = g.check_irr(mk(tmp_path, "本文报告了所有指标。"))
    assert any(f["severity"] == "warn" for f in r)


# ── 结构 ──
def test_finding_shape():
    f = g.finding("R", "block", "t", "m", "h")
    assert set(f) == {"rule", "severity", "target", "message", "fix_hint"}
    assert f["severity"] == "block"


def test_run_all_returns_list():
    from pathlib import Path
    assert isinstance(g.run_all(Path(ROOT)), list)


def test_every_rule_is_callable():
    from pathlib import Path
    for name, fn in g.RULES:
        assert callable(fn), name
        assert isinstance(fn(Path(ROOT)), list), name
