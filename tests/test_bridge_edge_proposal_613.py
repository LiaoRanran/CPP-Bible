#!/usr/bin/env python3
"""D1 回归测试：bridge_edge_proposal_613（桥接边画像/提案/apply）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bridge_edge_proposal_613 as d1  # noqa: E402


def test_candidate_count():
    assert len(d1.load_candidates()) == 98


def test_all_candidates_are_weak_without_shared_evidence():
    rows = d1.profile(d1.load_candidates())
    assert sum(1 for r in rows if r["grade"] == "A") == 0, "无一条有共享证据/原子"
    assert sum(1 for r in rows if r["grade"] == "B") == 98
    assert all("NO_SHARED_EVIDENCE" in r["flags"] for r in rows)


def test_sorted_by_pair_heat_desc():
    rows = d1.profile(d1.load_candidates())
    heats = [r["pair_heat"] for r in rows]
    assert heats == sorted(heats, reverse=True)


def test_deterministic_profile():
    assert d1.profile(d1.load_candidates()) == d1.profile(d1.load_candidates())


def test_grade_rules():
    c = [{"edge_id": "e1", "components": [1, 2], "basis": {"shared_evidence": ["EV-1"], "topic": "X"}},
         {"edge_id": "e2", "components": [1, 2], "basis": {"topic_match": True, "topic": "X"}},
         {"edge_id": "e3", "components": [3, 4], "basis": {"topic": "Y"}}]
    rows = {r["edge_id"]: r for r in d1.profile(c)}
    assert rows["e1"]["grade"] == "A"
    assert rows["e2"]["grade"] == "B"
    assert rows["e3"]["grade"] == "C"
    assert rows["e2"]["pair_heat"] == 2


def test_apply_is_append_only_and_idempotent(tmp_path, monkeypatch):
    target = tmp_path / "applied.jsonl"
    monkeypatch.setattr(d1, "APPLIED", target)
    monkeypatch.setattr(d1, "OUT", tmp_path / "report.md")
    d1.main(["--apply"])
    n1 = len([ln for ln in target.read_text(encoding="utf-8").splitlines() if ln.strip()])
    d1.main(["--apply"])
    n2 = len([ln for ln in target.read_text(encoding="utf-8").splitlines() if ln.strip()])
    assert n1 == 98 and n2 == 98, "重复 apply 不得重复写入（按 edge_id 去重）"
    ids = [json.loads(ln)["edge_id"] for ln in target.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(set(ids)) == len(ids)


def test_check_passes():
    assert d1.main(["--check"]) == 0
