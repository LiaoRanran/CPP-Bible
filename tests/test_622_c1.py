"""622 C1 · ABSTAIN 分类器升级（v2：verdict 识别 + Authority 交叉验证）单测"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import abstain_classifier_621 as A  # noqa: E402

NOW = datetime(2026, 9, 22, tzinfo=timezone.utc)


def test_authority_approved_flips_undecided_to_supported():
    r = A.classify_v2({"evidence_count": 3, "verdict": None},
                      authority="approved", now=NOW)
    assert r["state"] == "SUPPORTED"
    assert r["is_abstain"] is False
    assert r["basis"] == "authority_approved"


def test_authority_pending_keeps_undecided():
    r = A.classify_v2({"evidence_count": 3, "verdict": None},
                      authority="pending", now=NOW)
    assert r["state"] == "UNDECIDED"
    assert r["is_abstain"] is True
    assert r["basis"] == "no_signal"


def test_authority_rejected_gives_refuted():
    r = A.classify_v2({"evidence_count": 3, "verdict": None},
                      authority="rejected", now=NOW)
    assert r["state"] == "REFUTED"
    assert r["is_abstain"] is False


def test_priority_card_verdict_over_extracted_over_authority():
    r = A.classify_v2({"evidence_count": 3, "verdict": "refute"},
                      authority="approved", extracted_verdict="supported", now=NOW)
    assert r["state"] == "REFUTED" and r["basis"] == "card_verdict"
    r2 = A.classify_v2({"evidence_count": 3, "verdict": None},
                       authority="approved", extracted_verdict="refuted", now=NOW)
    assert r2["state"] == "REFUTED" and r2["basis"] == "extracted_verdict"


def test_hard_preconditions_still_first():
    assert A.classify_v2({"evidence_count": 0, "verdict": "confirm"},
                         authority="approved", now=NOW)["state"] == "INSUFFICIENT_EVIDENCE"
    assert A.classify_v2({"evidence_count": 2, "conflicted": True, "verdict": "confirm"},
                         now=NOW)["state"] == "CONFLICTED"
    assert A.classify_v2({"evidence_count": 2, "verdict": "confirm",
                          "verified_at": "2020-01-01"}, now=NOW)["state"] == "STALE"


def test_every_state_has_basis():
    cases = [{"evidence_count": 0}, {"evidence_count": 1, "conflicted": True},
             {"evidence_count": 1, "verified_at": "2020-01-01"},
             {"evidence_count": 1, "verdict": "confirm"},
             {"evidence_count": 1, "verdict": "refute"},
             {"evidence_count": 1, "verdict": None}]
    for c in cases:
        r = A.classify_v2(c, now=NOW)
        assert r["basis"] and r["reason"]
        assert r["state"] in A.STATES


def test_six_states_preserved():
    assert set(A.STATES) == {"SUPPORTED", "REFUTED", "UNDECIDED",
                             "INSUFFICIENT_EVIDENCE", "CONFLICTED", "STALE"}
    assert set(A.ABSTAIN_STATES) == {"UNDECIDED", "INSUFFICIENT_EVIDENCE",
                                     "CONFLICTED", "STALE"}


def test_authority_status_for_matching():
    entries = [
        {"target": {"id": "ae-A->ATOM-MEM-PERF-003::prop-1"}, "power": "ACCEPT"},
        {"target": {"id": "ae-B->ATOM-MEM-PERF-003::prop-2"}, "power": "REJECT"},
    ]
    assert A.authority_status_for("ATOM-MEM-PERF-003", entries) == "rejected"  # 取最后一条
    assert A.authority_status_for("ATOM-NOPE-999", entries) is None
    assert A.authority_status_for("", entries) is None


def test_authority_status_power_mapping():
    def st(power):
        return A.authority_status_for("X", [{"target": {"id": "ae->X::p"}, "power": power}])
    assert st("ACCEPT") == "approved"
    assert st("OVERRIDE") == "approved"
    assert st("REJECT") == "rejected"
    assert st("ABSTAIN") == "abstained"


def test_classify_card_v2_real_atom_uses_authority():
    """真实原子卡：v1 判 UNDECIDED，v2 应因 Authority 批准而判 SUPPORTED。"""
    card = "atoms/conc/ATOM-CONC-FENCE-001.md"
    if not os.path.exists(os.path.join(ROOT, card)):
        return
    entries = A.load_authority_entries()
    r = A.classify_card_v2(card, authority_entries=entries, now=NOW)
    assert r["state"] in A.STATES
    assert "basis" in r
    if r["authority"] == "approved":
        assert r["state"] == "SUPPORTED"


def test_v2_selftest_passes():
    assert A.selftest() == 0
