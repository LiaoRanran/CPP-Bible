"""635 1.4 · grounding_inventory_635 单测（纯标准库，≥5 例）。编号 1.4-1..1.4-6。"""
from __future__ import annotations

import grounding_inventory_635 as G


# 1.4-1：67 条规则
def test_rules():
    assert len(G.get_rules()) == 67


# 1.4-2：evidence 接地
def test_classify_evidence():
    assert G.classify({"scope": "evidence", "kind": "fact"}) == ("已接地", "即时性")


# 1.4-3：pedagogy 未接地
def test_classify_pedagogy():
    assert G.classify({"scope": "atom", "kind": "pedagogy"}) == ("未接地", "权威性")


# 1.4-4：repo 常规性
def test_classify_repo():
    assert G.classify({"scope": "repo", "kind": "fact"}) == ("部分接地", "常规性")


# 1.4-5：统计结构
def test_stats():
    s = G.stats()
    assert s["total"] == 67
    assert sum(s["grounding"].values()) == 67
    assert isinstance(s["ungrounded"], list)


# 1.4-6：--check 自检通过
def test_selftest():
    assert G.selftest() == 0
