# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""646 阶段 B2 · 反例搜索补全单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counterexample_searcher_646 as b2  # noqa: E402
import counts_659 as counts  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（扩展 KB 命中）。"""
    assert b2.selftest() == 0


def test_full_coverage():
    """670a 去写死：卡片域取权威源现算；"全覆盖"锁为 `cards_with_candidate == cards_total`。"""
    res = b2.run_search()
    assert res["cards_total"] == counts.ATOMS_REAL
    assert res["cards_with_candidate"] == res["cards_total"]


def test_candidates_have_source():
    """每个候选都带标准章节与判定标注（只搜不判）。"""
    res = b2.run_search()
    for hits in res["per_card"].values():
        for h in hits:
            assert h["standard_section"] and h["verdict"] == "需人审（只搜不判）"
