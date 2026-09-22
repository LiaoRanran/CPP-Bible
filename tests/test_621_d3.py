"""621 D3 · 人审数据脱敏 单测"""
from __future__ import annotations

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import human_review_anonymize_621 as A  # noqa: E402

ENTRY = {
    "decision_id": "dec-1", "reviewer": "LiaoRanran", "reason": "用户授权批量通过",
    "decided_at": "2026-09-19T23:16:04", "seq": 1,
    "prev_hash": "a" * 64, "self_hash": "b" * 64,
    "target": {"id": "ae-A->B::prop-1"}, "power": "ACCEPT",
}


def test_removes_real_name():
    out = A.anonymize_entry(ENTRY)
    assert "reviewer" not in out
    assert out["reviewer_pseudo"].startswith("R-")
    assert "LiaoRanran" not in json.dumps(out, ensure_ascii=False)


def test_truncates_timestamp_to_date():
    out = A.anonymize_entry(ENTRY)
    assert out["decided_at"] == "2026-09-19"
    assert "T" not in out["decided_at"]


def test_removes_chain_fields_by_default():
    out = A.anonymize_entry(ENTRY)
    for f in ("self_hash", "prev_hash", "seq"):
        assert f not in out
    kept = A.anonymize_entry(ENTRY, keep_chain=True)
    assert "self_hash" in kept and "seq" in kept


def test_pseudonym_stable_and_distinct():
    assert A.pseudonym("LiaoRanran") == A.pseudonym("LiaoRanran")
    assert A.pseudonym("LiaoRanran") != A.pseudonym("SomeoneElse")
    assert A.pseudonym("") == "R-unknown"


def test_scrub_user_home_paths():
    assert "<user>" in A.scrub_text(r"C:\Users\ASUS\proj\x.md")
    assert "<user>" in A.scrub_text("/home/alice/x")
    assert A.scrub_text("plain text") == "plain text"


def test_residual_scan():
    assert A.residual_identity_scan([{"a": "no names"}], ["LiaoRanran"])["clean"] is True
    r = A.residual_identity_scan([{"a": "LiaoRanran"}], ["LiaoRanran"])
    assert r["clean"] is False and r["residual_hits"]["LiaoRanran"] == 1


def test_anonymize_all_and_write():
    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "log.jsonl")
        with open(log, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(ENTRY, ensure_ascii=False) + "\n")
        res = A.anonymize_all(log, "__missing__")
        assert res["authority_count"] == 1
        assert len(res["rows"]) == 1
        out = os.path.join(td, "anon.jsonl")
        A.write_jsonl(res["rows"], out)
        rows = [json.loads(ln) for ln in open(out, encoding="utf-8") if ln.strip()]
        assert len(rows) == 1
        assert "LiaoRanran" not in json.dumps(rows, ensure_ascii=False)


def test_real_artifact_is_anonymous():
    if not os.path.exists(A.DEFAULT_OUT):
        return
    blob = open(A.DEFAULT_OUT, encoding="utf-8").read()
    for name in ("LiaoRanran",):
        assert name not in blob


def test_report_renders():
    res = {"authority_count": 1, "legacy_count": 0, "rows": [{"a": 1}], "keep_chain": False,
           "residual_identity_scan": {"known_names": 1, "residual_hits": {}, "clean": True}}
    md = A.render_report(res)
    assert "脱敏方法" in md and "残留身份扫描" in md


def test_selftest_passes():
    assert A.selftest() == 0
