"""636 2.4 · calibration_tracker_636 单测（纯标准库，≥5 例）。编号 2.4-1..2.4-6。"""
from __future__ import annotations

import calibration_tracker_636 as C


# 2.4-1：67 规则清单
def test_rows():
    assert len(C.known_error_rate_rows()) == 67


# 2.4-2：全部无数据（不编造）
def test_no_data():
    rows = C.known_error_rate_rows()
    assert all(r["known_error_rate"] is None for r in rows)
    assert all(r["data_state"] == "无数据" for r in rows)


# 2.4-3：观察态 = 67
def test_observation():
    assert C.stats()["observation_state"] == 67


# 2.4-4：ECE 三级降级
def test_ece():
    e = C.ece_format()
    assert set(e["degradation"]) == {"L1 重校准", "L2 禁言", "L3 降级"}
    assert e["domains"] == ["简单", "中等", "复杂"]


# 2.4-5：判决数
def test_decisions():
    assert C.decisions_count() >= 1


# 2.4-6：--check 自检通过
def test_selftest():
    assert C.selftest() == 0
