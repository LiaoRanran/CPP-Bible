"""622 D1 · 30 条逐条人审执行 单测"""
from __future__ import annotations

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import authority_log_620 as AL  # noqa: E402
import authority_pending_621 as P  # noqa: E402

EXEC_MD = os.path.join(ROOT, "data", "human_review_item_by_item_executed_622.md")
EXEC_JSONL = os.path.join(ROOT, "data", "human_review_item_by_item_executed_622.jsonl")


def test_build_decision_has_source_annotations():
    prop = P.build()[0]
    dec = P.build_decision(prop, prev_id="dec-000001")
    assert dec["source"] == P.SOURCE
    assert dec["authorized_by"] == P.AUTHORIZATION
    assert dec["review_method"] == P.REVIEW_METHOD
    assert dec["reviewer"].startswith("human:")
    assert dec["proposal_id"] == prop["proposal_id"]
    assert "615决策清单" in dec["reason"]


def test_modify_maps_to_override_with_target():
    props = P.build()
    mod = next(p for p in props if p["suggested_decision"] == "MODIFY")
    dec = P.build_decision(mod, prev_id="dec-000007")
    assert dec["power"] == "OVERRIDE"
    assert dec["overrides"] == "dec-000007"
    # 无既有决策时用 legacy 锚点（不编造 decision_id）
    dec2 = P.build_decision(mod, prev_id=None)
    assert str(dec2["overrides"]).startswith("legacy:pre_annotation:")


def test_approve_maps_to_accept():
    props = P.build()
    appr = next(p for p in props if p["suggested_decision"] == "ACCEPT")
    dec = P.build_decision(appr, prev_id=None)
    assert dec["power"] == "ACCEPT"
    assert "overrides" not in dec


def test_execute_all_appends_and_verifies_chain():
    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "log.jsonl")
        props = P.build()
        res = P.execute_all(props[:5], log_path=log)
        assert res["executed"] == 5
        assert res["before"] == 0 and res["after"] == 5
        assert res["chain_ok"] is True
        assert len(AL.load_entries(log)) == 5
        # 全部带来源标注
        for e in AL.load_entries(log):
            assert e["review_method"] == P.REVIEW_METHOD
            assert e["source"] == P.SOURCE


def test_execute_all_is_append_only_increment():
    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "log.jsonl")
        props = P.build()
        P.execute_all(props[:3], log_path=log)
        res2 = P.execute_all(props[:2], log_path=log)
        assert res2["before"] == 3 and res2["after"] == 5


def test_real_log_grew_to_418():
    assert P.decision_log_count() == 418
    ok, errs = AL.verify(P.DECISION_LOG)
    assert ok, errs[:3]


def test_real_log_has_30_executed_entries():
    entries = AL.load_entries(P.DECISION_LOG)
    ex = [e for e in entries if e.get("review_method") == P.REVIEW_METHOD]
    assert len(ex) == 30
    assert sum(1 for e in ex if e["power"] == "OVERRIDE") == 17
    assert sum(1 for e in ex if e["power"] == "ACCEPT") == 13
    assert all(e.get("authorized_by") == P.AUTHORIZATION for e in ex)
    assert all(e.get("source") == P.SOURCE for e in ex)


def test_artifacts_exist():
    if not os.path.exists(EXEC_MD):
        return
    md = open(EXEC_MD, encoding="utf-8").read()
    assert "388 → 418" in md
    assert "不是系统自动决策" in md
    rows = [json.loads(ln) for ln in open(EXEC_JSONL, encoding="utf-8") if ln.strip()]
    assert len(rows) == 30


def test_selftest_passes():
    assert P.selftest() == 0
