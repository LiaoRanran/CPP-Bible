"""644 D3 反例搜索器单测（X3-1..X3-4）。"""
from __future__ import annotations

import counterexample_searcher_644 as d3


# X3-1：已知有反例的结论必检出候选
def test_known_counterexample():
    hits = d3.search("signed integer overflow behavior")
    assert any("溢出" in h["statement"] or "overflow" in h["statement"].lower() for h in hits)


# X3-2：无反例的结论不误报
def test_no_false_positive():
    assert d3.search("the sky is blue and unrelated") == []


# X3-3：候选带来源与可信度
def test_candidate_has_source():
    for h in d3.search("vector push_back iterator invalidation"):
        assert h["source"] and h["credibility"] > 0


# X3-4：selftest 通过
def test_selftest():
    assert d3.selftest() == 0
