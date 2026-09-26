"""646 阶段 B2 · 反例搜索补全单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counterexample_searcher_646 as b2  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（扩展 KB 命中）。"""
    assert b2.selftest() == 0


def test_full_coverage():
    """真实搜索：覆盖全部 27 卡。"""
    res = b2.run_search()
    assert res["cards_total"] == 27
    assert res["cards_with_candidate"] == 27


def test_candidates_have_source():
    """每个候选都带标准章节与判定标注（只搜不判）。"""
    res = b2.run_search()
    for hits in res["per_card"].values():
        for h in hits:
            assert h["standard_section"] and h["verdict"] == "需人审（只搜不判）"
