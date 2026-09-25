"""636 V26-补1 · contamination_tracker_636 单测（纯标准库，≥5 例）。编号 VC1-1..VC1-6。"""
from __future__ import annotations

import contamination_tracker_636 as C


# VC1-1：taint 候选非空
def test_candidates():
    assert len(C.taint_candidates()) >= 1


# VC1-2：追踪目标非空
def test_target():
    assert C.trace()["target"]


# VC1-3：下游为 list
def test_downstream():
    assert isinstance(C.trace()["downstream"], list)


# VC1-4：三阀门 3 项
def test_valves():
    v = C.three_valves({"in_evidence": True})
    assert set(v) == {"独立来源", "必然发现", "善意"}


# VC1-5：tainted 为 list
def test_tainted():
    assert isinstance(C.trace()["tainted"], list)


# VC1-6：--check 自检通过
def test_selftest():
    assert C.selftest() == 0
