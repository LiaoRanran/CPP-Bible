"""644 B3 证据冲突检测器单测（C3-1..C3-5）。"""
from __future__ import annotations

import evidence_base_644 as base
import evidence_conflict_644 as b3


# C3-1：已知冲突必检出（L1 confirm vs L2 refute → high）
def test_known_conflict():
    evs = [
        {"id": "E1", "grade": "L1", "verdict": "confirm", "source_type": "compiler_run", "compilers": 2},
        {"id": "E2", "grade": "L2", "verdict": "refute", "source_type": "iso_standard", "compilers": 1},
    ]
    cs = b3.detect_conflicts("C", evs)
    assert any(c["type"] == "L1_vs_L2" and c["severity"] == "high" for c in cs)


# C3-2：两条 L2 矛盾 → medium
def test_l2_vs_l2():
    evs = [
        {"id": "A", "grade": "L2", "verdict": "confirm", "source_type": "iso_standard", "compilers": 1},
        {"id": "B", "grade": "L2", "verdict": "refute", "source_type": "committee", "compilers": 1},
    ]
    cs = b3.detect_conflicts("C", evs)
    assert any(c["type"] == "L2_vs_L2" for c in cs)


# C3-3：无冲突不误报
def test_no_false_positive():
    evs = [
        {"id": "P", "grade": "L1", "verdict": "confirm", "source_type": "compiler_run", "compilers": 2},
        {"id": "Q", "grade": "L2", "verdict": "confirm", "source_type": "iso_standard", "compilers": 1},
    ]
    assert b3.detect_conflicts("C", evs) == []


# C3-4：冲突分类合理（含 severity 与 suggestion）
def test_conflict_fields():
    evs = [
        {"id": "E1", "grade": "L1", "verdict": "confirm", "source_type": "compiler_run", "compilers": 2},
        {"id": "E2", "grade": "L2", "verdict": "refute", "source_type": "iso_standard", "compilers": 1},
    ]
    cs = b3.detect_conflicts("C", evs)
    c = cs[0]
    assert c["severity"] in ("high", "medium", "low")
    assert c["suggestion"]


# C3-5：全量检测可跑
def test_detect_all():
    assert isinstance(b3.detect_all(), dict)
    assert b3.selftest() == 0
