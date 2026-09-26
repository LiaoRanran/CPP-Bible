"""645 B4 反例语义搜索单测（fast 组：真实语义匹配，只搜不判）。"""
import sys

sys.path.insert(0, "tools")

import counterexample_searcher_645 as b4


def test_selftest_passes():
    assert b4.selftest() == 0


def test_search_matches_topics():
    hits = b4.search_card("move semantics and iterator invalidation and data race")
    topics = {h["topic"] for h in hits}
    assert {"move", "iterator", "race"} <= topics


def test_only_search_not_judge():
    res = b4.run_search()
    # 每条候选都只搜不判（verdict 固定需人审），不自动标真/假
    for hits in res["per_card"].values():
        for h in hits:
            assert h["verdict"] == "需人审（只搜不判）"


def test_real_cards_have_candidates():
    res = b4.run_search()
    # 真实原子卡中应有相当数量命中语义反例候选（B4 目标 ≥10）
    assert res["cards_with_candidate"] >= 10, (
        f"有候选卡仅 {res['cards_with_candidate']}，未达 B4 ≥10")
