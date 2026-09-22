"""622 C3 · 全量 83 张 ABSTAIN 重新分类 + PCK 交叉验证 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import abstain_classifier_621 as A  # noqa: E402
import atom_verdict_extractor_622 as E  # noqa: E402
import pck_batch_migrator_620 as M  # noqa: E402

OUT = os.path.join(ROOT, "data", "abstain_realignment_622.jsonl")
SUM = os.path.join(ROOT, "data", "abstain_realignment_622.json")


def _rows():
    if not os.path.exists(OUT):
        return None
    return [json.loads(ln) for ln in open(OUT, encoding="utf-8") if ln.strip()]


def test_all_83_cards_classified():
    rows = _rows()
    if rows is None:
        return
    assert len(rows) == 83
    assert all(r["state"] in A.STATES for r in rows)
    assert all(r.get("basis") for r in rows)


def test_abstain_zero_after_upgrade():
    rows = _rows()
    if rows is None:
        return
    assert sum(1 for r in rows if r["state"] in A.MACHINE_ABSTAIN_STATES) == 0
    assert all(r["state"] == "SUPPORTED" for r in rows)


def test_reverse_correlation_resolved():
    rows = _rows()
    if rows is None:
        return
    ct = A.alignment_crosstab(rows)
    assert ct["machine_abstain_human_approved"] == 0
    assert ct["cross"].get("SUPPORTED×approved") == 27
    assert ct["cross"].get("SUPPORTED×pending") == 56


def test_alignment_crosstab_math():
    rows = [{"state": "SUPPORTED", "authority": "approved"},
            {"state": "SUPPORTED", "authority": "pending"},
            {"state": "UNDECIDED", "authority": "approved"},
            {"state": "REFUTED", "authority": "rejected"}]
    ct = A.alignment_crosstab(rows)
    assert ct["total"] == 4
    assert ct["aligned"] == 2              # SUPPORTED×approved + REFUTED×rejected
    assert ct["machine_supported_human_pending"] == 1
    assert ct["machine_abstain_human_approved"] == 1
    assert ct["abstain_count"] == 1


def test_pck_authority_map_covers_83():
    amap = A.pck_authority_map()
    assert len(amap) == 83
    assert sum(1 for v in amap.values() if v == "approved") == 27
    assert sum(1 for v in amap.values() if v == "pending") == 56


def test_classify_all_v2_uses_pck_map():
    cards = M.discover_cards()
    rows = A.classify_all_v2(cards, extracted=E.verdict_index(E.extract_all()))
    assert len(rows) == 83
    assert all(r["authority_source"] == "pck_human_authority" for r in rows)


def test_summary_json_matches():
    if not os.path.exists(SUM):
        return
    d = json.load(open(SUM, encoding="utf-8"))
    assert d["total"] == 83
    assert d["state_distribution"] == {"SUPPORTED": 83}
    assert d["alignment"]["machine_abstain_human_approved"] == 0


def test_selftest_passes():
    assert A.selftest() == 0
