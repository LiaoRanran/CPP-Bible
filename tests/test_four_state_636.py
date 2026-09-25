"""636 V26-补2 · four_state_636 单测（纯标准库，≥5 例）。编号 VC2-1..VC2-6。"""
from __future__ import annotations

import four_state_636 as F


# VC2-1：pass 分类
def test_pass():
    assert F.classify("一切正常通过") == "pass"


# VC2-2：fail 分类
def test_fail():
    assert F.classify("被 block 拒绝") == "fail"


# VC2-3：pass_with_exception 分类
def test_exception():
    assert F.classify("整体通过但有豁免条款") == "pass_with_exception"


# VC2-4：unknown 分类
def test_unknown():
    assert F.classify("无数据，无法判定") == "unknown"


# VC2-5：模拟分布自洽
def test_simulate():
    s = F.simulate()
    assert s["n"] >= 30
    assert sum(s["four_state"].values()) == s["n"]
    assert isinstance(s["fake_pass"], int)


# VC2-6：--check 自检通过
def test_selftest():
    assert F.selftest() == 0
