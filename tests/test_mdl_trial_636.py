"""636 2.5 · mdl_trial_636 单测（纯标准库，≥5 例）。编号 2.5-1..2.5-6。"""
from __future__ import annotations

import mdl_trial_636 as M


# 2.5-1：67 规则
def test_rules():
    assert len(M.rules()) == 67


# 2.5-2：cost 计算
def test_cost():
    assert M.rule_cost({"id": "AB", "title": "T"}) == 8 * 2 + 8 * 1 + M.FIXED_BITS


# 2.5-3：零触达 reject
def test_zero_touch_reject():
    assert M.admit({"id": "X", "title": "T"}, {})["admit"] is False


# 2.5-4：高触达 admit
def test_high_touch_admit():
    hm = {"X": {f"R{i}": True for i in range(1, 7)}}
    assert M.admit({"id": "X", "title": "T"}, hm)["admit"] is True


# 2.5-5：trial 分区
def test_trial():
    t = M.trial()
    assert t["admitted"] + t["rejected"] == t["total"] == 67


# 2.5-6：--check 自检通过
def test_selftest():
    assert M.selftest() == 0
