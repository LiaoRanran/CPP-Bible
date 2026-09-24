"""632 E1 · L4.2 探针单测（纯标准库，≥5 例）。

聚焦 `coverage_probe_l4_2_632`：阈值边界歧义的结构性覆盖探针。
编号 E1-L4.2-1..E1-L4.2-6。
"""
from __future__ import annotations

import tools.coverage_probe_l4_2_632 as m

_SRC = (
    "def check_a(self):\n    return n > 2\n"
    "def check_b(self):\n    # 边界：>= 3 视为达标（inclusive）\n    return n >= 3\n"
    "def check_c(self):\n    if x == 1:\n        return y < 5\n"
)


# E1-L4.2-1：函数切分得到 3 个
def test_split_functions_count():
    bodies = m._split_functions(_SRC)
    assert len(bodies) == 3, bodies


# E1-L4.2-2：未说明边界被判定为未说明
def test_undocumented_boundary():
    bodies = m._split_functions(_SRC)
    a = m.analyze_threshold(bodies[0])
    assert a["has_threshold"] is True
    assert a["boundary_documented"] is False


# E1-L4.2-3：已说明边界被判定为已说明
def test_documented_boundary():
    bodies = m._split_functions(_SRC)
    b = m.analyze_threshold(bodies[1])
    assert b["has_threshold"] is True
    assert b["boundary_documented"] is True


# E1-L4.2-4：无阈值比较的函数不被记为阈值规则
def test_no_threshold_function():
    bodies = m._split_functions("def check_d(self):\n    return True\n")
    d = m.analyze_threshold(bodies[0])
    assert d["has_threshold"] is False


# E1-L4.2-5：真实 gate_engine 含阈值规则（>=1）
def test_real_gate_has_thresholds():
    out = m.measure()
    assert out.get("gate_exists") is True
    assert out.get("threshold_rules", 0) >= 1


# E1-L4.2-6：--check 自检通过（exit 0）
def test_selftest_passes():
    assert m.selftest() == 0
