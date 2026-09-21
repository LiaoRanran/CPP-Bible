"""621 C1 · ABSTAIN 六态分类器 单测"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import abstain_classifier_621 as A  # noqa: E402

NOW = datetime(2026, 9, 22, tzinfo=timezone.utc)


def test_supported():
    r = A.classify({"evidence_count": 2, "verdict": "confirm"}, NOW)
    assert r["state"] == "SUPPORTED"
    assert r["is_abstain"] is False


def test_refuted():
    r = A.classify({"evidence_count": 2, "verdict": "refute"}, NOW)
    assert r["state"] == "REFUTED"
    assert r["is_abstain"] is False


def test_undecided_missing_verdict():
    r = A.classify({"evidence_count": 2, "verdict": None}, NOW)
    assert r["state"] == "UNDECIDED"
    assert r["is_abstain"] is True


def test_undecided_infra_error():
    r = A.classify({"evidence_count": 2, "verdict": "infra_error"}, NOW)
    assert r["state"] == "UNDECIDED"
    assert r["is_abstain"] is True


def test_insufficient_evidence():
    r = A.classify({"evidence_count": 0, "verdict": "confirm"}, NOW)
    assert r["state"] == "INSUFFICIENT_EVIDENCE"
    assert r["is_abstain"] is True


def test_conflicted():
    r = A.classify({"evidence_count": 2, "verdict": "confirm", "conflicted": True}, NOW)
    assert r["state"] == "CONFLICTED"
    assert r["is_abstain"] is True


def test_stale_over_90_days():
    r = A.classify({"evidence_count": 2, "verdict": "confirm",
                    "verified_at": "2026-01-01"}, NOW)
    assert r["state"] == "STALE"
    assert r["is_abstain"] is True


def test_not_stale_within_90_days():
    r = A.classify({"evidence_count": 2, "verdict": "confirm",
                    "verified_at": "2026-09-01"}, NOW)
    assert r["state"] == "SUPPORTED"


def test_priority_insufficient_beats_conflicted():
    r = A.classify({"evidence_count": 0, "conflicted": True}, NOW)
    assert r["state"] == "INSUFFICIENT_EVIDENCE"


def test_six_states_and_four_abstain():
    assert len(A.STATES) == 6
    assert set(A.ABSTAIN_STATES) == {"UNDECIDED", "INSUFFICIENT_EVIDENCE",
                                     "CONFLICTED", "STALE"}
    assert len(A.ABSTAIN_STATES) == 4


def test_days_since_parsing():
    assert A._days_since("2026-09-01", NOW) == 21
    assert A._days_since("unknown", NOW) is None
    assert A._days_since(None, NOW) is None


def test_build_state_atom_and_evidence():
    st = A.build_state({"claim_structured": [{"evidence": ["EV-CONC-001", "EV-CONC-002"]}],
                        "verdict": "confirm", "verified_at": "2026-09-01"},
                       "atoms/conc/ATOM-CONC-FENCE-001.md", NOW)
    assert st["evidence_count"] == 2
    assert st["days_since_verify"] == 21
    st2 = A.build_state({"artifact_sha256": "abc"}, "evidence/conc/EV-CONC-001.md", NOW)
    assert st2["evidence_count"] == 1
    st3 = A.build_state({}, "evidence/conc/EV-CONC-002.md", NOW)
    assert st3["evidence_count"] == 0


def test_classify_card_real_atom():
    r = A.classify_card("atoms/conc/ATOM-CONC-FENCE-001.md", NOW)
    assert r["state"] in A.STATES
    assert r["kind"] == "atom"
    assert r["card_id"]


def test_selftest_passes():
    assert A.selftest() == 0
