"""644 E1 全库证据不足扫描单测（G1-1..G1-4）。"""
from __future__ import annotations

import evidence_base_644 as base
import evidence_gap_scanner_644 as e1


# G1-1：扫描覆盖全量卡片
def test_scan_coverage():
    s = e1.scan()
    assert s["n_cards"] == len(base.list_atoms())


# G1-2：零证据卡必判不足且缺 L1/L2
def test_zero_evidence_gap():
    s = e1.scan()
    zero = [g for g in s["gaps"] if g["n_evidence"] == 0]
    if zero:
        assert all("L1/L2 权威证据" in g["missing"] for g in zero)


# G1-3：优先级排序合理（降序）且 Top 10 非空（当存在 gap）
def test_priority_and_top10():
    s = e1.scan()
    if s["gaps"]:
        assert len(s["top10"]) <= 10 and len(s["top10"]) > 0
        pris = [g["priority"] for g in s["gaps"]]
        assert pris == sorted(pris, reverse=True)


# G1-4：selftest 通过
def test_selftest():
    assert e1.selftest() == 0
