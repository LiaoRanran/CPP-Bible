"""635 1.3 · four_questions_635 单测（纯标准库，≥5 例）。编号 1.3-1..1.3-6。"""
from __future__ import annotations

import four_questions_635 as F


# 1.3-1：Q1 返回布尔 blind
def test_q1():
    r = F.q1_blind()
    assert isinstance(r["blind"], bool)
    assert "evidence" in r


# 1.3-2：Q2 origin 分布
def test_q2():
    r = F.q2_ai_first()
    assert r["total"] >= 1
    assert "human_observed" in r["origins"]


# 1.3-3：Q3 返回 records 列表
def test_q3():
    r = F.q3_calibration()
    assert isinstance(r["records"], list)
    assert isinstance(r["has_calibration"], bool)


# 1.3-4：Q4 reviewer 分布
def test_q4():
    r = F.q4_assignment()
    assert r["total"] >= 1
    assert set(r["reviewers"]) >= {"human:LiaoRanran"}


# 1.3-5：Q4 单一评审人判定
def test_q4_single():
    assert F.q4_assignment()["single_reviewer"] is True


# 1.3-6：--check 自检通过
def test_selftest():
    assert F.selftest() == 0
