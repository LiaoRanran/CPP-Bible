"""642 A4 · calibration_tracker_642 单测（推翻计数 / 未推翻计数 / error_rate / ECE / 代理标注）。
编号 A4-1..A4-8。
"""
from __future__ import annotations

import calibration_tracker_642 as C


# A4-1：推翻 ⇒ error_count + 1（total 也已 + 1）
def test_overturn_increments_error():
    t = C.CalibrationTracker(["R1"])
    t.record(["R1"], "APPROVE", "D1")
    t.overturn(["R1"], "D1")
    st = t.stats["R1"]
    assert (st.total_count, st.error_count) == (1, 1)


# A4-2：未推翻 ⇒ 只涨 total_count
def test_not_overturned_only_counts_total():
    t = C.CalibrationTracker(["R1"])
    for i in range(3):
        t.record(["R1"], "APPROVE", f"D{i}")
    st = t.stats["R1"]
    assert (st.total_count, st.error_count) == (3, 0)
    assert st.known_error_rate == 0.0


# A4-3：error_rate = error / total（并验证四舍五入口径）
def test_error_rate_arithmetic():
    t = C.CalibrationTracker(["R1"])
    for i in range(4):
        t.record(["R1"], "APPROVE", f"X{i}")
    t.overturn(["R1"], "X0")
    t.overturn(["R1"], "X1")
    assert t.stats["R1"].known_error_rate == 0.5

    t2 = C.CalibrationTracker(["R2"])
    for i in range(3):
        t2.record(["R2"], "APPROVE", f"Y{i}")
    t2.overturn(["R2"], "Y0")
    assert t2.stats["R2"].known_error_rate == 0.3333


# A4-4：无自身样本 ⇒ 回退全库代理，且显式标 is_proxy=True（不冒充实测）
def test_proxy_fallback_is_labelled():
    t = C.CalibrationTracker(["R1"], proxy_rate=0.1881, proxy_source="全库代理")
    st = t.stats["R1"]
    assert st.is_proxy is True
    assert st.known_error_rate == 0.1881
    assert st.proxy_source == "全库代理"
    t.record(["R1"], "APPROVE", "D1")
    assert st.is_proxy is False, "有自身样本后必须切换为实测口径"


# A4-5：无规则归属的判决 ⇒ 记入未归属桶（不静默丢弃）
def test_unattributed_bucket():
    t = C.CalibrationTracker(["R1"])
    t.record([], "APPROVE", "D1")
    assert C.UNATTRIBUTED in t.stats
    assert t.stats[C.UNATTRIBUTED].total_count == 1


# A4-6：日志 append-only（record 只追加；overturn 只回标，不改条目数量与数值）
def test_log_is_append_only():
    t = C.CalibrationTracker(["R1"])
    t.record(["R1"], "APPROVE", "D1")
    t.record(["R1"], "MODIFY", "D2")
    n_before = len(t.log)
    snap_before = [dict(e) for e in t.log]
    t.overturn(["R1"], "D1")
    assert len(t.log) == n_before, "overturn 不得增删日志条目"
    for before, after in zip(snap_before, t.log):
        assert {k: v for k, v in after.items() if k != "overturned"} == \
               {k: v for k, v in before.items() if k != "overturned"}


# A4-7：ECE 三级降级格式（3 级 + 阈值递增 + 本批不启用）
def test_ece_three_level_format():
    ece = C.CalibrationTracker.ece_format()
    assert len(ece["degradation"]) == 3
    assert C.ECE_L1 < C.ECE_L2 < C.ECE_L3
    assert ece["enabled"] is False
    assert ece["domains"] == ["简单", "中等", "复杂"]


# A4-8：代理重建——ledger/人审可复算，逃逸率为冻结契约；67 规则全代理 + 自检
def test_history_proxies_and_selftest():
    prox = C.history_proxies()
    lm = prox["ledger_modify_rate"]
    assert lm["recomputable"] is True and lm["numerator"] == 85 and lm["denominator"] == 452
    assert lm["value"] == 0.1881
    assert prox["human_modify_rate"]["value"] == 0.0876
    assert prox["escape_rate"]["recomputable"] is False, "逃逸率分母无单一数据源，必须标不可复算"

    snap = C.build_tracker().snapshot()
    assert snap["n_rules"] == 67
    assert snap["n_with_samples"] == 0 and snap["n_proxy"] == 67
    assert all(r["is_proxy"] is True for r in snap["rows"])
    assert C.selftest() == 0
