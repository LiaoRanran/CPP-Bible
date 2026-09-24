"""632 E1 · L4.4 探针单测（纯标准库，≥5 例）。

聚焦 `coverage_probe_l4_4_632`：规则优先级冲突的结构性覆盖探针。
编号 E1-L4.4-1..E1-L4.4-6。
"""
from __future__ import annotations

import tools.coverage_probe_l4_4_632 as m

_SRC = (
    'register(Rule(id="EV-A", severity="block", scope="evidence"))\n'
    'register(Rule(id="EV-B", severity="block", scope="evidence"))\n'
    'register(Rule(id="AT-C", severity="warn", scope="atom"))\n'
    'PRIORITY = {"EV-A": 1, "EV-B": 2}\n'
)


# E1-L4.4-1：静态解析得到 3 条规则
def test_parse_rules_count():
    rules = m.parse_rules(_SRC)
    assert len(rules) == 3


# E1-L4.4-2：潜在冲突对构造（同 scope + 同为 block/warn）
def test_potential_conflicts():
    rules = m.parse_rules(_SRC)
    pairs = m.potential_conflicts(rules)
    assert pairs == [("EV-A", "EV-B")]


# E1-L4.4-3：优先级策略被识别
def test_policy_detected():
    assert bool(m._POLICY_RE.search(_SRC)) is True


# E1-L4.4-4：无策略源码不误报策略
def test_no_policy_not_detected():
    assert bool(m._POLICY_RE.search('register(Rule(id="X", severity="block", scope="atom"))')) is False


# E1-L4.4-5：measure 结构完整（真实读取 gate_engine.RULES）
def test_measure_structure():
    out = m.measure()
    assert out.get("vector") == "L4.4"
    assert out.get("rules_parsed", 0) >= 1
    assert "conflict_pairs" in out


# E1-L4.4-6：--check 自检通过（exit 0）
def test_selftest_passes():
    assert m.selftest() == 0
