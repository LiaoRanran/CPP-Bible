#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_dist_perf_670c2.py — 670c2 C2/C4 回归测试（dist 验证 + 性能基准）。

运行：python -m pytest tests/test_dist_perf_670c2.py -q
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import dist_verify_670c2 as dist  # noqa: E402
import perf_benchmark_670c2 as perf  # noqa: E402
import pytest  # noqa: E402  673j

# ---------------- C2 dist ----------------

def test_dist_dir_exists():
    assert os.path.isdir(dist.DIST)


def test_dist_defines_eight_pages():
    assert len(dist.PAGES) == 8


def test_dist_all_html_present():
    res = dist.run()
    assert not any("缺 HTML" in e for e in res["errors"]), res["errors"]


def test_dist_js_syntax_clean():
    res = dist.run()
    assert not any("JS 语法错误" in e for e in res["errors"]), res["errors"]


def test_dist_no_missing_refs():
    res = dist.run()
    assert not any("引用缺失" in e for e in res["errors"]), res["errors"]


def test_dist_home_budget_ok():
    res = dist.run()
    assert not any("首页体积" in e for e in res["errors"]), res["errors"]


def test_dist_reports_js_count():
    res = dist.run()
    assert res["js_files"] >= 10


def test_dist_overall_passes():
    assert dist.run()["errors"] == []


# ---------------- C4 perf ----------------

def test_perf_returns_measurements():
    res = perf.run()
    assert "measurements" in res and "thresholds" in res


def test_perf_gate_within_threshold():
    res = perf.run()
    assert not any("gate_run_ms" in w for w in res["warns"]), res["warns"]


def test_perf_paper_gate_within_threshold():
    res = perf.run()
    assert not any("paper_gate_ms" in w for w in res["warns"]), res["warns"]


def test_perf_data_parse_within_threshold():
    res = perf.run()
    assert not any("data_parse_ms" in w for w in res["warns"]), res["warns"]


def test_perf_has_honesty_notes():
    res = perf.run()
    assert len(res["notes"]) >= 2
