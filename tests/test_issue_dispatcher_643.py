"""643 B5 · issue_dispatcher_643 单测（合并去重/优先级公式/Top10/下一步映射/只读）。
编号 B5-1..B5-8。
"""
from __future__ import annotations

import issue_dispatcher_643 as B5


# B5-1：公式含严重度（这是对 637 优先级倒挂缺陷的修法）
def test_score_formula_contains_severity():
    it = B5.issue("B4", "escape_rule_missing", "x", 3, 2, "w")
    assert it["score"] == round(it["severity"] * 3 / 2, 4)


# B5-2：高严重度压过低严重度（同 impact/cost 下）
def test_severity_dominates_at_equal_scale():
    hi = B5.issue("X", "escape_rule_missing", "t", 5, 1, "")   # sev 3
    lo = B5.issue("X", "rule_single_card", "t", 5, 1, "")      # sev 1
    assert hi["score"] > lo["score"]


# B5-3：成本越高 score 越低
def test_cost_discounts_score():
    cheap = B5.issue("X", "escape_rule_missing", "t", 5, 1, "")
    pricey = B5.issue("X", "escape_rule_missing", "t", 5, 3, "")
    assert cheap["score"] > pricey["score"]


# B5-4：未知 kind ⇒ 默认档 + 人审（不静默丢弃）
def test_unknown_kind_default():
    it = B5.issue("X", "not_a_kind", "t", 1, 1, "")
    assert it["severity"] == 1 and it["next_step"] == "人审"


# B5-5：去重 —— 同 issue_id 只留一条，且保留 impact 更大者
def test_dedup():
    a = B5.issue("B4", "escape_rule_missing", "x", 1, 1, "")
    b = B5.issue("B4", "escape_rule_missing", "x", 9, 1, "")
    out = B5.dedup([a, b])
    assert len(out) == 1 and out[0]["impact"] == 9


# B5-6：合并结果无重复 + 优先级降序
def test_dispatch_sorted_and_unique():
    d = B5.dispatch()
    assert len({i["issue_id"] for i in d["issues"]}) == d["n"]
    scores = [i["score"] for i in d["issues"]]
    assert scores == sorted(scores, reverse=True)


# B5-7：Top 10 非空且不超过 10；四来源都有条目
def test_top10_and_sources():
    d = B5.dispatch()
    assert 0 < len(d["top"]) <= B5.TOP_N
    assert all(v > 0 for v in d["by_source"].values()), str(d["by_source"])


# B5-8：数据缺口类 issue 在册 + 下一步映射齐备 + 只读自检
def test_missing_dimension_issue_and_mapping():
    d = B5.dispatch()
    assert any(i["kind"] == "missing_dimension" for i in d["issues"])
    assert all(i["next_step"] for i in d["issues"])
    assert set(B5.NEXT_STEP) >= {"escape_rule_missing", "escape_rule_weak",
                                 "missing_dimension"}
    assert B5.selftest() == 0
