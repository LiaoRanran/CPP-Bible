"""644 E3 头部层-尾端联动单测（H3-1..H3-4）。"""
from __future__ import annotations

import evidence_base_644 as base
import head_tail_bridge_644 as e3


def _rec(grade, verdict, vid):
    return base.EvidenceRecord(evidence_id=vid * 64, content="x", source_type="compiler_run"
                              if grade in ("L1",) else "single_blog", grade=grade,
                              credibility=0.9, acquired_at="2026-09-26",
                              acquisition_method="test", meta={"verdict": verdict})


# H3-1：L1 confirm → supports
def test_supports():
    r = e3.bridge("C1", [_rec("L1", "confirm", "a")])
    assert r["supports"] == 1 and r["conflicts"] == 0


# H3-2：refute → conflicts
def test_conflicts():
    r = e3.bridge("C2", [_rec("L4", "refute", "b")])
    assert r["conflicts"] == 1


# H3-3：尾端验证结果可追踪 + read_only
def test_read_only():
    r = e3.bridge("C1", [_rec("L1", "confirm", "c")])
    assert r["read_only"] is True
    assert r["results"][0]["impact"] == "supports"


# H3-4：只读不修改 + selftest
def test_no_modify_and_selftest():
    atom = base.list_atoms()[0]
    with open(atom["path"], encoding="utf-8") as fh:
        before = fh.read()
    e3.bridge("C1", [_rec("L1", "confirm", "d")])
    with open(atom["path"], encoding="utf-8") as fh:
        after = fh.read()
    assert before == after
    assert e3.selftest() == 0
