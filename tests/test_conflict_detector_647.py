"""647 B1 · 冲突检测器真上岗回归锁（编号 B1-1..B1-8）。"""
from __future__ import annotations

import json
import os

import conflict_detector_647 as C
import protector_mode_647 as M
import queyi_core_v10_641 as core

RULES = [{"id": "A", "severity": "block", "scope": "atom"},
         {"id": "B", "severity": "warn", "scope": "atom"}]
EV = {"EV-OK-1"}
HI = "status: verified\nfalsification: fail\nevidence: [EV-NOPE-1, EV-NOPE-2]\n"
MID = "status: verified\nevidence: [EV-NOPE-1]\n"
LOW = "status: verified\nevidence: [EV-OK-1]\n"


def _dec():
    a = core.Artifact.from_bytes(b"x", "atom_card", uri="t.md")
    return core.Decision.make(a.artifact_id, "pass", reasons=["r"])


def test_b1_1_three_tiers():
    assert C.evaluate(HI, RULES, EV)["action"] == "block"
    assert C.evaluate(MID, RULES, EV)["action"] == "warn"
    assert C.evaluate(LOW, RULES, EV)["action"] == "pass"
    assert C.THETA_WARN < C.THETA_BLOCK


def test_b1_2_rr_alone_does_not_count_as_both_sides():
    assert C.both_sides_have_evidence("evidence: [EV-OK-1]\n",
                                      {"rr": 1, "er": 0, "ee": 0, "und": 0})[0] is False
    assert C.both_sides_have_evidence("evidence: [EV-OK-1]\n",
                                      {"rr": 0, "er": 0, "ee": 0, "und": 1})[0] is True


def test_b1_3_enforce_blocks(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    r = C.apply_new(_dec(), HI, RULES, ev_index=EV, card_rel="t.md")
    assert r["enforced"] is True and r["decision_after"]["state"] == "fail"
    assert r["verdict_changed"] is True
    assert any("647 B1" in x for x in r["decision_after"]["reasons"])


def test_b1_4_shadow_only_marks(monkeypatch):
    monkeypatch.setenv(M.ENV, "shadow")
    r = C.apply_new(_dec(), HI, RULES, ev_index=EV, card_rel="t.md")
    assert r["enforced"] is False and r["decision_after"]["state"] == "pass"
    assert C.verdict_unchanged(r["decision_before"], r["decision_after"]) is True
    assert r["decision_after"]["conflict_action"] == "block", "意图仍被标记"


def test_b1_5_low_never_changes_verdict(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    r = C.apply_new(_dec(), LOW, RULES, ev_index=EV, card_rel="t.md")
    assert r["verdict_changed"] is False and r["enforced"] is False


def test_b1_6_real_card_block_is_registered():
    """**真实卡有高置信样本**（ATOM-MEM-PERF-003）：这条断言防止把生产影响写成"0 条"。"""
    r = C.run_new()
    assert r["n"] == 23
    assert r["n_verdict_changed"] == r["n_blocked"] >= 1
    assert "ATOM-MEM-PERF-003" in " ".join(x["card"] for x in r["rows"] if x["action"] == "block")


def test_b1_7_history_not_rescanned():
    """只处理新判决：run_new 只消费 verified 卡清单，不写任何账本。"""
    import hashlib
    led = os.path.join(C.ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
    before = hashlib.sha256(open(led, "rb").read()).hexdigest()
    C.run_new()
    assert hashlib.sha256(open(led, "rb").read()).hexdigest() == before


def test_b1_8_report_and_selftest():
    assert C.selftest() == 0
    assert C.main(["--report"]) == 0
    doc = json.load(open(C.OUT_JSON, encoding="utf-8"))
    assert doc["theta_block"] == 0.8 and doc["by_action"]
    assert all(s["ok"] for s in doc["synthetic"])
