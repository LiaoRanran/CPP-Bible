"""643 E2 · rule_aging_detector_643 单测（趋势/建议/不判档/数据缺口）。
编号 E2-1..E2-8。
"""
from __future__ import annotations

import rule_aging_detector_643 as E2


# E2-1：趋势计算（后半 − 前半）
def test_trend():
    row = {"R1": True, "R2": True, "R3": False, "R4": False, "R5": False, "R6": False}
    assert E2.trend_of(row) == -2
    assert E2.trend_of({f"R{i}": True for i in range(1, 7)}) == 0
    assert E2.trend_of({f"R{i}": (i > 3) for i in range(1, 7)}) == 3


# E2-2：趋势不可算 ⇒ None（不猜）
def test_trend_none_cases():
    assert E2.trend_of({"R1": True}) is None
    assert E2.trend_of({}) is None


# E2-3：零触达零关联 ⇒ insufficient_data（**不判**）
def test_no_evidence_means_no_verdict():
    assert E2.verdict(0, None, 0)[0] == "insufficient_data"
    assert "不判" in E2.verdict(0, None, 0)[1]


# E2-4：退役候选（零触达 + 有逃逸关联）
def test_retire_candidate():
    assert E2.verdict(0, None, 1)[0] == "退役候选"
    assert E2.verdict(0, -3, 2)[0] == "退役候选", "零触达优先于拆分"


# E2-5：拆分候选（≥2 条逃逸关联）优先于收紧
def test_split_precedes_tighten():
    assert E2.verdict(3, -5, 2)[0] == "拆分候选"
    assert E2.verdict(3, -5, 1)[0] == "收紧候选"


# E2-6：收紧阈值边界（-2 触发，-1 不触发）
def test_tighten_threshold_edge():
    assert E2.TREND_THRESHOLD == -2
    assert E2.verdict(3, -2, 0)[0] == "收紧候选"
    assert E2.verdict(3, -1, 0)[0] == "保留"


# E2-7：真实规模与分布自洽
def test_real_scale():
    a = E2.assess()
    assert a["n_rules"] == 67
    assert sum(a["by_verdict"].values()) == 67
    assert set(a["by_verdict"]) <= {"退役候选", "拆分候选", "收紧候选", "保留",
                                    "insufficient_data"}


# E2-8：数据缺口显式登记（日历轴不可用）+ 只读自检
def test_data_gaps_registered():
    a = E2.assess()
    assert len(a["unavailable"]) >= 3
    assert any("30 天" in u for u in a["unavailable"])
    assert E2.selftest() == 0
