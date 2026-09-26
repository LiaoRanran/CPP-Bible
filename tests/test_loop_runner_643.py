"""643 E3 · loop_runner_643 单测（R4 口径/复算/门槛/不并入 642 台账/637 复用）。
编号 E3-1..E3-8。
"""
from __future__ import annotations

import loop_runner_643 as E3


# E3-1：候选 = B5 Top10 + D2 草案（两来源都在）
def test_candidates_from_two_sources():
    r = E3.run()
    assert r["by_source"]["B5"] > 0 and r["by_source"]["D2"] > 0
    assert r["candidates"] == r["by_source"]["B5"] + r["by_source"]["D2"]


# E3-2：采纳数恒为 0（机器不代签）
def test_adopted_is_zero():
    assert E3.run()["adopted"] == 0


# E3-3：校准度可复算（= 兑现/可验证子集）
def test_calibration_recomputable():
    r = E3.run()
    if r["calibration"] is None:
        assert r["verified_subset"] == 0
    else:
        assert abs(r["calibration"] - r["realized"] / r["verified_subset"]) < 0.02


# E3-4：口径标注（不得与 R1–R3 混同）
def test_caliber_is_flagged():
    r = E3.run()
    assert "可验证子集" in r["caliber"] or "可验证子集" in r["calibration_why"]


# E3-5：门槛判定一致（≥60%）
def test_threshold_consistency():
    r = E3.run()
    assert r["meets_threshold"] == (r["calibration"] is not None
                                    and r["calibration"] >= E3.EXPANSION_THRESHOLD)
    assert E3.EXPANSION_THRESHOLD == 0.60


# E3-6：**不并入 642 台账**（跨批边界）
def test_not_merged_into_642():
    r = E3.run()
    assert r["merged_into_642_ledger"] is False
    assert "643" in E3.OUT_JSON and "642" not in E3.OUT_JSON


# E3-7：替代项写实际（B5 替 observer、C2 替 generator）
def test_replaces_documented():
    r = E3.run()
    assert "issue_dispatcher_643" in r["replaces"]["observer"]
    assert "targeted_mutator_643" in r["replaces"]["generator"]


# E3-8：637 打分被复用（或明确记错）+ 只读自检
def test_reuses_637_scoring():
    rows = E3.run()["candidate_rows"]
    assert rows and all("score_637" in c for c in rows)
    assert all(c["score_637"] is not None or "score_637_error" in c for c in rows)
    assert E3.selftest() == 0
