"""621 C2 · 全量 83 张卡 ABSTAIN 分类 单测"""
from __future__ import annotations

import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import abstain_classifier_621 as A  # noqa: E402

OUT = os.path.join(ROOT, "data", "abstain_classification_621.jsonl")


def _rows():
    if not os.path.exists(OUT):
        return None
    return [json.loads(ln) for ln in open(OUT, encoding="utf-8") if ln.strip()]


def test_classification_has_83_rows():
    rows = _rows()
    if rows is None:
        return
    assert len(rows) == 83
    assert all(r["state"] in A.STATES for r in rows)


def test_distribution_supported_56_undecided_27():
    rows = _rows()
    if rows is None:
        return
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    assert counts.get("SUPPORTED") == 56
    assert counts.get("UNDECIDED") == 27


def test_atoms_all_undecided_evidence_all_supported():
    rows = _rows()
    if rows is None:
        return
    assert all(r["state"] == "UNDECIDED" for r in rows if r["kind"] == "atom")
    assert all(r["state"] == "SUPPORTED" for r in rows if r["kind"] == "evidence")


def test_rows_are_json_serializable_fields():
    rows = _rows()
    if rows is None:
        return
    for r in rows:
        # verified_at 在 input 子字典里；yaml 的 date 必须已被归一为字符串
        assert isinstance(r["input"]["verified_at"], (str, type(None)))
        json.dumps(r, ensure_ascii=False)  # 不得再抛 date 不可序列化


def test_cross_with_pck_shows_inverse_relation():
    rows = _rows()
    if rows is None:
        return
    cert_dir = os.path.join(ROOT, "data", "pck", "certificates")
    if not os.path.isdir(cert_dir):
        return
    ha = {}
    for p in os.listdir(cert_dir):
        if p.endswith(".pck.yaml"):
            c = yaml.safe_load(open(os.path.join(cert_dir, p), encoding="utf-8").read())
            ha[c["claim"]["id"]] = (c.get("human_authority") or {}).get("status")
    sup_pending = sum(1 for r in rows
                      if r["state"] == "SUPPORTED" and ha.get(r["card_id"]) == "pending")
    und_approved = sum(1 for r in rows
                       if r["state"] == "UNDECIDED" and ha.get(r["card_id"]) == "approved")
    assert sup_pending == 56
    assert und_approved == 27


def test_classify_all_is_deterministic():
    from datetime import datetime, timezone
    now = datetime(2026, 9, 22, tzinfo=timezone.utc)
    cards = ["atoms/conc/ATOM-CONC-FENCE-001.md", "evidence/conc/EV-CONC-001.md"]
    a = A.classify_all(cards, now)
    b = A.classify_all(cards, now)
    assert a == b


def test_write_jsonl_roundtrip():
    import tempfile
    rows = _rows() or A.classify_all(["atoms/conc/ATOM-CONC-FENCE-001.md"])
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "x.jsonl")
        A.write_jsonl(rows, p)
        back = [json.loads(ln) for ln in open(p, encoding="utf-8") if ln.strip()]
        assert len(back) == len(rows)


def test_selftest_passes():
    assert A.selftest() == 0
