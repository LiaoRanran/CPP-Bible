"""636 2.1 · conflict_detector_636 单测（纯标准库，≥5 例）。编号 2.1-1..2.1-6。"""
from __future__ import annotations

import conflict_detector_636 as C

_RULES = [{"id": "A", "severity": "block", "scope": "atom"},
          {"id": "B", "severity": "warn", "scope": "atom"}]


# 2.1-1：RR 检测（block+warn 共存）
def test_rr():
    d = C.detect("status: verified\nevidence: [EV-X-001]\nartifact_sha256: a\n", _RULES)
    assert d["rr"] == 1


# 2.1-2：欠定（verified 无证据）
def test_underdetermined():
    d = C.detect("status: verified\n", _RULES)
    assert d["und"] == 1


# 2.1-3：ER（强反证标记）
def test_er():
    d = C.detect("status: verified\nfalsification: fail\nevidence: [EV-A-001]\n", _RULES)
    assert d["er"] == 1


# 2.1-4：EE（≥2 证据但有悬挂引用）
def test_ee():
    d = C.detect("status: verified\nevidence: [EV-X-001, EV-X-002]\n", _RULES,
                 ev_index={"EV-X-001"})
    assert d["ee"] == 1


# 2.1-5：强度 C 公式
def test_strength():
    d = C.detect("status: verified\n", _RULES)
    assert d["C"] == round(d["conflict_raw"] * (1 - d["agreement"]), 3)


# 2.1-6：--check 自检通过
def test_selftest():
    assert C.selftest() == 0
