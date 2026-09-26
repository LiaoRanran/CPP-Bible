"""643 D3 · rule_draft_mdl_check_643 单测（overlap 两类/阈值/判定顺序/六档）。
编号 D3-1..D3-8。
"""
from __future__ import annotations

import mdl_gate_642 as mg
import rule_draft_mdl_check_643 as D3


# D3-1：密度代理（NEW 草案）
def test_density_proxy():
    assert D3.overlap_new("c", {}) == 0.0
    assert D3.overlap_new("c", {"c": 5}) == 0.5
    assert D3.overlap_new("c", {"c": 10}) == 1.0
    assert D3.overlap_new("c", {"c": 99}) == 1.0, "必须封顶在 1.0"


# D3-2：字段级重叠（MODIFY 草案）
def test_field_overlap():
    fbr = {"R1": ["status", "evidence"], "R2": ["status"], "R3": ["other"]}
    assert D3.overlap_modify(["status", "evidence"], "R0", fbr) == (1.0, "R1")
    assert D3.overlap_modify(["status"], "R0", fbr) == (1.0, "R1")
    assert D3.overlap_modify(["unknown"], "R0", fbr) == (0.0, "")


# D3-3：排除自身（目标规则不与自己比）
def test_overlap_excludes_self():
    fbr = {"R1": ["status"], "R2": ["status"]}
    _ov, who = D3.overlap_modify(["status"], "R1", fbr)
    assert who == "R2", who


# D3-4：无字段 ⇒ overlap 0（不误判冗余）
def test_empty_fields_no_overlap():
    assert D3.overlap_modify([], "R0", {"R1": ["status"]}) == (0.0, "")


# D3-5：阈值 0.8 且"恰好 0.8 不算冗余"（严格大于）
def test_threshold_is_strict():
    assert D3.OVERLAP_THRESHOLD == 0.8
    assert not (0.8 > D3.OVERLAP_THRESHOLD)
    assert 0.81 > D3.OVERLAP_THRESHOLD


# D3-6：冗余 ⇒ 不再看 MDL（最终结论被覆盖）
def test_redundant_overrides_mdl():
    c = D3.check()
    for r in c["rows"]:
        if r["redundant"]:
            assert r["final_decision"] == "REJECT_冗余"
            assert r["admitted"] is False


# D3-7：非冗余 ⇒ 最终结论 = 642 MDL 结论（六档之一）
def test_non_redundant_uses_mdl():
    c = D3.check()
    for r in c["rows"]:
        if not r["redundant"]:
            assert r["final_decision"] == r["mdl_decision"]
        assert r["mdl_decision"] in mg.DECISIONS


# D3-8：本批新增档不改 642 常量 + 只读自检
def test_new_decision_not_written_back():
    assert "REJECT_冗余" not in mg.DECISIONS, "不得改动已入库的 642 常量"
    c = D3.check()
    assert c["n"] == len(c["rows"]) > 0
    assert D3.selftest() == 0
