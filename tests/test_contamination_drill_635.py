"""635 V26-3 · contamination_drill_635 单测（纯标准库，≥5 例）。编号 V3-1..V3-6。"""
from __future__ import annotations

import contamination_drill_635 as C


# V3-1：6 通道
def test_channels():
    assert len(C.CHANNELS) == 6


# V3-2：控制方映射
def test_controller():
    assert C.CONTROLLER["cppreference"] == "external"
    assert C.CONTROLLER["direct_experiment"] == "self"


# V3-3：通道分类
def test_classify():
    assert C.classify_channel("见 cppreference 原文") == "cppreference"
    assert C.classify_channel("本系统直接实验") == "direct_experiment"


# V3-4：证据卡通道分布
def test_evidence_cards():
    ev = C.evidence_cards()
    assert len(ev) >= 1
    assert all(c["channel"] in C.CHANNELS for c in ev)


# V3-5：污染演练
def test_drill():
    t = C.taint_recommendation()
    assert t["target"] == C.TARGET
    assert isinstance(t["downstream"], list)
    assert len(C.three_valves()) == 3


# V3-6：--check 自检通过
def test_selftest():
    assert C.selftest() == 0
