"""643 E4 · whitelist_expand_decision_643 单测（条件触发/边界/护栏/不代执行）。
编号 E4-1..E4-8。
"""
from __future__ import annotations

import whitelist_expand_decision_643 as E4


# E4-1：低于门槛 ⇒ 不扩展且登记原因
def test_below_threshold_no_expansion():
    d = E4.decide(0.10)
    assert d["expanded"] is False and d["plan"] == []
    assert "不扩展" in d["reason"]


# E4-2：达标 ⇒ 允许扩展
def test_above_threshold_expands():
    d = E4.decide(0.65)
    assert d["expanded"] is True and d["plan"]


# E4-3：扩展 2–3 类
def test_expansion_size():
    d = E4.decide(0.99)
    assert E4.MIN_ADD <= len(d["plan"]) <= E4.MAX_ADD, len(d["plan"])


# E4-4：每类都带护栏与回滚
def test_plan_has_guardrails_and_rollback():
    for p in E4.decide(0.99)["plan"]:
        assert p["guardrails"] and p["rollback"] and p["category"]


# E4-5：按 score 升序（最低风险优先）
def test_plan_sorted_by_score():
    scores = [p["score"] for p in E4.decide(0.99)["plan"]]
    assert scores == sorted(scores)


# E4-6：边界（恰好 0.60 达标；None 不拍板）
def test_threshold_edges():
    assert E4.THRESHOLD == 0.60
    assert E4.decide(0.60)["expanded"] is True
    assert E4.decide(0.5999)["expanded"] is False
    assert E4.decide(None)["expanded"] is False


# E4-7：不达标必给"补齐条件"（不是只说不行）
def test_no_expansion_gives_path():
    d = E4.decide(0.10)
    assert "校准度需" in d["what_would_be_needed"]


# E4-8：**即使达标也不代执行** + 只读自检
def test_never_executes():
    assert E4.decide(0.99)["executed"] is False
    assert E4.decide(0.10)["executed"] is False
    assert E4.selftest() == 0
