"""643 B1 · coverage_gap_scanner_643 单测（矩阵/四类盲区/优先级/热力图/只读）。
编号 B1-1..B1-8。
"""
from __future__ import annotations

import coverage_gap_scanner_643 as B1


def _synth():
    """构造说明（与 selftest 一致，便于复核）：
    R1=block 零命中；R2=只命中 card_b（单卡）；R3=命中 card_b+card_d；
    R4..R15 各命中 card_b+card_d；card_a 零命中；card_b/card_d 各被 >10 条命中。
    """
    rl = [{"id": f"R{i}", "title": "", "severity": "block" if i == 1 else "warn",
           "scope": "atom", "kind": "fact"} for i in range(1, 16)]
    cl = ["card_a", "card_b", "card_d"]
    m = {r["id"]: {} for r in rl}
    m["R2"]["card_b"] = 1
    m["R3"]["card_b"] = 1
    m["R3"]["card_d"] = 1
    for i in range(4, 16):
        m[f"R{i}"] = {"card_b": 1, "card_d": 1}
    return m, rl, cl


# B1-1：已知盲区必检出
def test_known_blind_spot_detected():
    m, rl, cl = _synth()
    assert B1.analyze(m, rl, cl)["cards_no_rule_hit"] == ["card_a"]


# B1-2：已知全覆盖不报错（无零命中卡、无零命中规则）
def test_full_coverage_reports_nothing():
    _, rl, cl = _synth()
    full = B1.analyze({r["id"]: {c: 1 for c in cl} for r in rl}, rl, cl)
    assert full["cards_no_rule_hit"] == []
    assert full["rules_never_hit"] == []
    assert full["rules_single_card"] == []


# B1-3：矩阵维度正确（合成 + 真实 67×27）
def test_matrix_dimensions():
    m, rl, cl = _synth()
    a = B1.analyze(m, rl, cl)
    assert (a["n_rules"], a["n_cards"]) == (15, 3)
    real = B1.report()["analysis"]
    assert (real["n_rules"], real["n_cards"]) == (67, 27)


# B1-4：四类判据各自成立（block 零命中 / 单卡 / 超阈值）
def test_four_categories():
    m, rl, cl = _synth()
    a = B1.analyze(m, rl, cl)
    assert a["block_rules_zero_hit"] == ["R1"]
    assert a["rules_single_card"] == ["R2"]
    assert a["cards_over_10_rules"] == ["card_b", "card_d"]


# B1-5：优先级分级与计数自洽
def test_priority_levels():
    m, rl, cl = _synth()
    a = B1.analyze(m, rl, cl)
    assert a["by_level"] == {"P0": 2, "P1": 1, "P2": 2}
    assert sum(a["by_level"].values()) == len(a["priorities"])


# B1-6：矩阵只统计落在卡集合里的 target（不把 evidence 目标算进来）
def test_matrix_filters_non_card_targets():
    rl = [{"id": "R1", "title": "", "severity": "block", "scope": "atom", "kind": "fact"}]
    m = B1.build_matrix([{"rule_id": "R1", "target": "evidence/x.md", "severity": "block"},
                         {"rule_id": "R1", "target": "card_a", "severity": "block"},
                         {"rule_id": "R9", "target": "card_a", "severity": "block"}],
                        ["card_a"], rl)
    assert m == {"R1": {"card_a": 1}}


# B1-7：热力图覆盖全部规则且带列号映射
def test_heatmap_text():
    m, rl, cl = _synth()
    txt = B1.heatmap_text(m, cl)
    assert txt.count("| `R") == 15
    assert "`c00` = `card_a`" in txt


# B1-8：只读自检通过
def test_selftest():
    assert B1.selftest() == 0
