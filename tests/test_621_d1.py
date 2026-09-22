"""621 D1 · 30 条逐条复核 → Authority 待审条目 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import authority_pending_621 as P  # noqa: E402


def test_parse_615_30_rows():
    rows = P.parse_615()
    assert len(rows) == 30
    assert sum(1 for r in rows if r["current"] == "modify") == 17
    assert sum(1 for r in rows if r["current"] == "approve") == 13


def test_all_proposals_pending_not_decisions():
    props = P.build()
    assert len(props) == 30
    assert all(p["status"] == "pending" for p in props)
    assert all(p["type"] == "pending_review_proposal" for p in props)
    # 待审条目**不得**含 decision_id / power（那是决策日志的字段）
    assert all("decision_id" not in p and "power" not in p for p in props)


def test_suggestion_mapping():
    props = P.build()
    for p in props:
        assert p["suggested_decision"] in ("MODIFY", "ACCEPT")
    assert sum(1 for p in props if p["suggested_decision"] == "MODIFY") == 17
    assert sum(1 for p in props if p["suggested_decision"] == "ACCEPT") == 13


def test_proposal_ids_unique_and_sequential():
    ids = [p["proposal_id"] for p in P.build()]
    assert len(set(ids)) == 30
    assert ids[0] == "prop-621-001"
    assert ids[-1] == "prop-621-030"


def test_decision_log_not_written():
    """核心保证：生成待审条目前后，Authority 决策日志条目数不变（不代签）。"""
    before = P.decision_log_count()
    props = P.build()
    P.write(P.DEFAULT_OUT, props)
    after = P.decision_log_count()
    assert before == after


def test_output_file_exists_and_is_pending():
    if not os.path.exists(P.DEFAULT_OUT):
        return
    rows = [json.loads(ln) for ln in open(P.DEFAULT_OUT, encoding="utf-8") if ln.strip()]
    assert len(rows) == 30
    assert all(r["status"] == "pending" for r in rows)
    assert all(r["review_method"] == "item_by_item_proposed" for r in rows)


def test_report_declares_no_forgery():
    md = P.render_report(P.build(), 388, 388)
    assert "不代签证明" in md
    assert "未写入决策日志" in md


def test_empty_source_safe():
    assert P.parse_615("__missing__") == []


def test_selftest_passes():
    assert P.selftest() == 0
