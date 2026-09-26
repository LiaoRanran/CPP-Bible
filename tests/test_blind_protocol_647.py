"""647 B3 · blind_protocol 真上岗回归锁（编号 B3-1..B3-8）。"""
from __future__ import annotations

import hashlib
import json
import os

import blind_protocol_647 as B
import protector_mode_647 as M


def test_b3_1_enforce_forces_blind_for_every_method(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    for method in ("BATCH_AUTH", "ITEM_OPEN", "MIRROR_DERIVED", "ITEM_BLIND"):
        j = B.new_judgment(f"T-{method}", 1.0, method)
        assert j.review_method_effective == B.BLIND_METHOD
        assert j.item.blinded is True
        assert "ai_recommendation" not in j.visible_view()


def test_b3_2_unrevealed_read_raises(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    j = B.new_judgment("T-X", 35.8, "BATCH_AUTH")
    try:
        j.recommendation()
        assert False, "应抛 BlindViolation"
    except B.BlindViolation:
        pass


def test_b3_3_reveal_restores_and_disagreement(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    j = B.new_judgment("T-Y", 35.8, "BATCH_AUTH")
    done = j.reveal(40.0)
    assert done.recommendation() == 35.8
    assert (done.disagreement() or {}).get("disagree") is True
    assert B.disagreement_rate([done]) == 1.0
    assert B.disagreement_rate([B.new_judgment("T-Z", 1.0)]) is None


def test_b3_4_shadow_falls_back_to_642(monkeypatch):
    monkeypatch.setenv(M.ENV, "shadow")
    plain = B.new_judgment("S-1", 9.0, "BATCH_AUTH")
    assert plain.item.blinded is False
    assert plain.visible_view().get("ai_recommendation") == 9.0
    assert plain.recommendation() == 9.0
    assert B.new_judgment("S-2", 3.0, "ITEM_BLIND").item.blinded is True


def test_b3_5_history_marked_not_modified():
    led = B.base.LEDGER
    before = hashlib.sha256(open(led, "rb").read()).hexdigest()
    h = B.history_marks()
    assert h["n_decisions"] == 452 and h["n_violations"] == 258
    assert h["ledger_unchanged"] is True
    assert hashlib.sha256(open(led, "rb").read()).hexdigest() == before


def test_b3_6_demo_blinds_all(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    d = B.run_new_demo()
    assert d["n_blinded"] == d["n"] == 3
    assert all(r["effective"] == B.BLIND_METHOD for r in d["rows"])


def test_b3_7_no_ledger_write_on_reveal(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    led = B.base.LEDGER
    before = open(led, "rb").read()
    B.new_judgment("T-W", 1.0).reveal(2.0)
    assert open(led, "rb").read() == before


def test_b3_8_report_and_selftest():
    assert B.selftest() == 0
    assert B.main(["--report"]) == 0
    doc = json.load(open(B.OUT_JSON, encoding="utf-8"))
    assert doc["history"]["n_decisions"] == 452
    assert doc["demo"]["n_blinded"] == 3
    assert os.path.isfile(B.OUT_MD)
