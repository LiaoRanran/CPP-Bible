"""636 2.2 · anti_windup_636 单测（纯标准库，≥5 例）。编号 2.2-1..2.2-6。"""
from __future__ import annotations

import anti_windup_636 as A


# 2.2-1：队列长度可读
def test_queue_len():
    assert A.queue_len() >= 0


# 2.2-2：饱和等级
def test_level():
    s = A.saturation()
    assert s["level"] in ("正常", "半饱和", "饱和")


# 2.2-3：三阈值布尔
def test_thresholds():
    s = A.saturation()
    assert all(isinstance(s[k], bool) for k in ("A", "B", "C"))


# 2.2-4：模拟有数字
def test_simulate():
    sim = A.simulate()
    assert sim["alerts"] >= 0 and sim["frozen_or_downgraded"] >= 0


# 2.2-5：预算上限
def test_budget():
    b = A.budget()
    assert b["weekly_cap"] == A.CAPACITY_PER_WEEK


# 2.2-6：--check 自检通过
def test_selftest():
    assert A.selftest() == 0
