"""622 C2 · 原子卡 verdict 提取 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import atom_verdict_extractor_622 as E  # noqa: E402

OUT = os.path.join(ROOT, "data", "atom_verdict_extraction_622.jsonl")


def test_extract_by_status():
    assert E.extract({"status": "verified"})["verdict"] == "SUPPORTED"
    assert E.extract({"status": "red-team-verified"})["verdict"] == "SUPPORTED"
    assert E.extract({"status": "refuted"})["verdict"] == "REFUTED"
    assert E.extract({"status": "rejected"})["verdict"] == "REFUTED"


def test_extract_draft_with_observation_evidence():
    r = E.extract({"status": "draft", "evidence": ["E1"],
                   "claim_structured": [{"claim_type": "observation"}]})
    assert r["verdict"] == "SUPPORTED" and r["confidence"] == "medium"
    assert r["basis"] == "draft+observation+evidence"


def test_extract_draft_inference_falls_to_evidence_only():
    r = E.extract({"status": "draft", "evidence": ["E1"],
                   "claim_structured": [{"claim_type": "inference"}]})
    assert r["basis"] == "evidence_only" and r["confidence"] == "low"


def test_extract_empty_is_undecided():
    r = E.extract({})
    assert r["verdict"] == "UNDECIDED" and r["basis"] == "no_signal"


def test_card_verdict_field_takes_precedence():
    assert E.extract({"verdict": "confirm"})["basis"] == "card_verdict"
    assert E.extract({"verdict": "refute"})["verdict"] == "REFUTED"
    assert E.extract({"verdict": "weird"})["verdict"] == "UNDECIDED"


def test_status_history_refuted_detected():
    r = E.extract({"status": "draft",
                   "status_history": [{"level": "draft"}, {"level": "refuted"}]})
    assert r["verdict"] == "REFUTED"


def test_discover_27_atoms():
    assert len(E.discover_atoms()) == 27


def test_extract_all_and_index():
    rows = E.extract_all()
    assert len(rows) == 27
    assert all(r["verdict"] in ("SUPPORTED", "REFUTED", "UNDECIDED") for r in rows)
    idx = E.verdict_index(rows)
    assert len(idx) == 27


def test_artifact_matches_tool():
    if not os.path.exists(OUT):
        return
    rows = [json.loads(ln) for ln in open(OUT, encoding="utf-8") if ln.strip()]
    assert len(rows) == 27
    assert sum(1 for r in rows if r["verdict"] == "SUPPORTED") == 27
    assert all(r["basis"] for r in rows)


def test_report_renders():
    md = E.render_report(E.extract_all())
    assert "原子卡 verdict 提取" in md
    assert "与 621 C2 的对比" in md


def test_selftest_passes():
    assert E.selftest() == 0
