"""622 D2 · W2 重算（基于 418 条 Authority 日志）单测"""
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

LABELS = os.path.join(ROOT, "data", "grounded_labels_w2.json")


def _executed():
    return [e for e in AL.load_entries(P.DECISION_LOG)
            if e.get("review_method") == P.REVIEW_METHOD]


def test_current_labels_match_artifact():
    if not os.path.exists(LABELS):
        return
    lbl = json.load(open(LABELS, encoding="utf-8"))
    nodes = lbl["nodes"]
    cnt: dict[str, int] = {}
    for v in nodes.values():
        cnt[v.get("label")] = cnt.get(v.get("label"), 0) + 1
    # 640 A1：签署后权威产物重算（IN79/OUT42，误解层全部 OUT）
    assert cnt.get("IN") == 79
    assert cnt.get("OUT") == 42
    assert cnt.get("UNDEC", 0) == 0


def test_labels_node_composition():
    if not os.path.exists(LABELS):
        return
    lbl = json.load(open(LABELS, encoding="utf-8"))
    kinds: dict[str, int] = {}
    for v in lbl["nodes"].values():
        kinds[v.get("kind")] = kinds.get(v.get("kind"), 0) + 1
    assert sum(kinds.values()) == 121


def test_30_decisions_are_same_direction_as_annotations():
    ex = _executed()
    assert len(ex) == 30
    cmp = P.compare_with_annotations(ex)
    assert cmp["missing"] == 0
    assert cmp["diff"] == 0
    assert cmp["all_same_direction"] is True
    assert cmp["same"] == 30


def test_compare_detects_difference_and_missing():
    with tempfile.TemporaryDirectory() as td:
        ann = os.path.join(td, "ann.jsonl")
        with open(ann, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"edge_id": "e1", "action": "modify"}) + "\n")
        decs = [{"target": {"id": "e1"}, "power": "ACCEPT"},      # 与 modify 不同向
                {"target": {"id": "e2"}, "power": "ACCEPT"}]      # annotations 无此边
        cmp = P.compare_with_annotations(decs, ann)
        assert cmp["diff"] == 1 and cmp["missing"] == 1
        assert cmp["all_same_direction"] is False


def test_action_power_mapping():
    assert P.ACTION_FOR_POWER["ACCEPT"] == "approve"
    assert P.ACTION_FOR_POWER["OVERRIDE"] == "modify"
    assert P.ACTION_FOR_POWER["REJECT"] == "reject"


def test_authority_log_has_418_and_annotations_unchanged_388():
    assert P.decision_log_count() == 418
    ann = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
    n = sum(1 for ln in open(ann, encoding="utf-8") if ln.strip())
    assert n == 388          # D1 未改 annotations（硬边界）


def test_selftest_passes():
    assert P.selftest() == 0
