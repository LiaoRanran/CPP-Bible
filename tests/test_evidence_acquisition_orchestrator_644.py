"""644 D5 证据获取编排器单测（O5-1..O5-4）。"""
from __future__ import annotations

import evidence_acquisition_orchestrator_644 as d5
import evidence_base_644 as base


def _stub_acquire(topic, section=None):
    return {"ok": False, "fetched": [], "errors": ["stub"], "topic": topic}


def _stub_probe(snippet, opts=None, compiler="g++"):
    return {"ok": False, "error": "stub", "sandbox": None}


# O5-1：编排流程正确（返回结构完整）
def test_orchestrate_structure():
    r = d5.orchestrate("signed integer overflow", max_rounds=2,
                       d1_acquire=_stub_acquire, d2_probe=_stub_probe)
    assert "evidence_package" in r and "sufficiency" in r and "log" in r
    assert r["log"][0]["round"] == 1


# O5-2：充分性触发继续获取（不足→跑到上限）
def test_continues_until_cap():
    r = d5.orchestrate("topic x", max_rounds=3,
                       d1_acquire=_stub_acquire, d2_probe=_stub_probe)
    assert r["rounds"] == 3
    assert r["rounds"] <= r["max_rounds"]


# O5-3：N 轮上限生效
def test_round_cap():
    r = d5.orchestrate("topic y", max_rounds=1,
                       d1_acquire=_stub_acquire, d2_probe=_stub_probe)
    assert r["rounds"] <= 1


# O5-4：不修改卡片 + selftest
def test_no_card_modify_and_selftest():
    atom = base.list_atoms()[0]
    with open(atom["path"], encoding="utf-8") as fh:
        before = fh.read()
    r = d5.orchestrate("signed integer overflow", max_rounds=2,
                       d1_acquire=_stub_acquire, d2_probe=_stub_probe)
    with open(atom["path"], encoding="utf-8") as fh:
        after = fh.read()
    assert before == after
    assert r["cards_untouched"] is True
    assert d5.selftest() == 0
