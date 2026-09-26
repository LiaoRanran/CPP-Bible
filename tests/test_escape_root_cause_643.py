"""643 D1 · escape_root_cause_643 单测（归因映射/C3 并入/可行动划分/只读）。
编号 D1-1..D1-7。
"""
from __future__ import annotations

import escape_root_cause_643 as D1


# D1-1：四类归因映射
def test_cause_mapping():
    assert D1.cause_of({"attribution": "规则缺失"})[0] == "规则缺失"
    assert D1.cause_of({"attribution": "规则太弱"})[0] == "规则太弱"
    assert D1.cause_of({"attribution": "规则冲突"})[0] == "规则冲突"
    assert D1.cause_of({"attribution": "验证器能力天花板"})[0] == "验证器能力天花板"


# D1-2：未知归因 ⇒ 保守归"能力天花板"（不自动化）
def test_unknown_cause_is_conservative():
    c, why = D1.cause_of({"attribution": "???"})
    assert c == "验证器能力天花板" and "保守" in why


# D1-3：C3 verdict → 根因映射（只取非兑现项）
def test_c3_mapping_filters_realized():
    synth = {"rows": [
        {"mutation_id": "m1", "verdict": "evaded", "target_rule": "R1", "card": "c",
         "op": "field_delete", "why": "w"},
        {"mutation_id": "m2", "verdict": "not_triggered", "target_rule": "R2", "card": "c",
         "op": "x", "why": "w"},
        {"mutation_id": "m3", "verdict": "oracle_mismatch", "target_rule": "R3", "card": "c",
         "op": "y", "why": "w"},
        {"mutation_id": "m4", "verdict": "blocked", "target_rule": "R4", "card": "c",
         "op": "z", "why": "w"},
        {"mutation_id": "m5", "verdict": "noop", "target_rule": "R5", "card": "c",
         "op": "w", "why": "w"},
    ]}
    got = {c["case_id"]: c["cause"] for c in D1.from_c3(synth)}
    assert got == {"m1": "规则太弱", "m2": "不可达", "m3": "责任错配"}, got


# D1-4：不可行动类（能力天花板/责任错配/冲突）不进 actionable
def test_actionable_only_missing_or_weak():
    a = D1.attributable()
    for c in a["actionable"]:
        assert c["cause"] in ("规则缺失", "规则太弱")
    for c in a["non_actionable"]:
        assert c["cause"] not in ("规则缺失", "规则太弱")


# D1-5：划分完备（可行动 + 不可行动 = 全部）
def test_partition_complete():
    a = D1.attributable()
    assert len(a["actionable"]) + len(a["non_actionable"]) == a["n"]
    assert sum(a["by_cause"].values()) == a["n"]


# D1-6：B4 案例无目标规则 ⇒ target 记 `—`（不伪造归属）
def test_b4_cases_have_no_rule_attribution():
    a = D1.attributable()
    b4 = [c for c in a["cases"] if c["source"] == "B4"]
    assert b4 and all(c["target"] == "—" for c in b4)


# D1-7：方向映射六类齐备 + 只读自检
def test_directions_and_selftest():
    assert set(D1.DIRECTION) == {"规则缺失", "规则太弱", "规则冲突",
                                 "验证器能力天花板", "责任错配", "不可达"}
    assert D1.selftest() == 0
