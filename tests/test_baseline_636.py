"""636 任务0 · baseline_636 单测（纯标准库，≥5 例）。编号 T0-1..T0-6。"""
from __future__ import annotations

import baseline_636 as B


# T0-1：规则数 67
def test_rules():
    assert B.count_rules() == 67


# T0-2：coverage 复算 100
def test_coverage():
    assert B.coverage_pct() == 100.0


# T0-3：接地率 35.8
def test_grounding():
    assert abs(float(B.grounding_pct()) - 35.8) < 0.1


# T0-4：击败器覆盖率 + taint
def test_defeater():
    d = B.defeater_stats()
    assert d["coverage_pct"] == 100.0 and d["taint_cards"] == 8


# T0-5：Daubert 观察态 67
def test_daubert():
    assert B.daubert_observation() == 67


# T0-6：--check 自检通过
def test_selftest():
    assert B.selftest() == 0
