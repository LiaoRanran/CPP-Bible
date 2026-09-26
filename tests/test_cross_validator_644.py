"""644 D4 多源交叉验证器单测（V4-1..V4-4）。"""
from __future__ import annotations

import cross_validator_644 as d4


# V4-1：已知一致（全 support）
def test_consistent():
    assert d4.consistency_of(["support", "support"]) == "consistent"


# V4-2：已知冲突（support + refute）
def test_conflict():
    assert d4.consistency_of(["support", "refute"]) == "conflict"


# V4-3：报告带各来源证据
def test_validate_structure():
    r = d4.validate("signed integer overflow")
    assert r["verdict"] in ("consistent", "partial", "conflict")
    assert len(r["sources"]) >= 2
    assert "stances" in r


# V4-4：selftest 通过
def test_selftest():
    assert d4.selftest() == 0
