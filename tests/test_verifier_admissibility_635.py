"""635 V26-5 · verifier_admissibility_635 单测（纯标准库，≥5 例）。编号 V5-1..V5-6。"""
from __future__ import annotations

import verifier_admissibility_635 as V


# V5-1：68 验证器
def test_rows():
    assert len(V.rows()) == 68


# V5-2：五问字段齐
def test_daubert_fields():
    r = V.daubert({"id": "X", "title": "", "scope": "atom", "kind": "fact"})
    assert set(r) >= {"testable", "peer_reviewed", "known_error_rate",
                      "operational_standard", "community_acceptance", "observation_state"}


# V5-3：规则观察态
def test_rule_observation():
    r = V.daubert({"id": "X", "title": "", "scope": "evidence", "kind": "fact"})
    assert r["observation_state"] is True and r["known_error_rate"] is False


# V5-4：生成器非观察态
def test_generator():
    g = V.mutation_generator()
    assert g["known_error_rate"] is True and g["observation_state"] is False


# V5-5：统计
def test_stats():
    s = V.stats()
    assert s["total"] == 68
    assert s["n_observation"] == 67
    assert len(s["missing_known_error_rate"]) == 67


# V5-6：--check 自检通过
def test_selftest():
    assert V.selftest() == 0
