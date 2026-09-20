#!/usr/bin/env python3
"""C1 回归测试：learner_behavior_ingest（真实学习行为接入 · append-only / fail-closed）。"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_behavior_ingest as c1  # noqa: E402

GOOD = {"timestamp": "2026-09-20T23:00:00", "kc_id": "ATOM-MEM-ALLOC-001",
        "action_type": "answer", "correct": True, "duration_s": 12.5, "source": "flashcard"}


def _tmp(tmp_path: Path) -> Path:
    p = tmp_path / "behavior.jsonl"
    p.write_text("", encoding="utf-8")
    return p


def test_validate_accepts_good():
    assert c1.validate(dict(GOOD), c1.known_kcs()) == []


def test_validate_rejects_missing_and_bad_type():
    assert c1.validate({"timestamp": "2026-09-20T23:00:00"}, None)
    assert c1.validate({**GOOD, "action_type": "sleep"}, None)
    assert c1.validate({**GOOD, "timestamp": "not-a-date"}, None)
    assert c1.validate({**GOOD, "correct": "yes"}, None)
    assert c1.validate({**GOOD, "duration_s": -1}, None)


def test_answer_requires_correct():
    assert c1.validate({**GOOD, "correct": None}, None), "answer 必须给 correct"
    assert c1.validate({**GOOD, "action_type": "review", "correct": None}, None) == []


def test_unknown_kc_rejected():
    bad = {**GOOD, "kc_id": "ATOM-DOES-NOT-EXIST"}
    assert c1.validate(bad, c1.known_kcs())


def test_fail_closed_aborts_whole_batch(tmp_path):
    p = _tmp(tmp_path)
    res = c1.ingest([dict(GOOD), {"timestamp": "2026-09-20T23:00:00"}], path=p, write=True)
    assert res["aborted"] and res["written"] == 0
    assert p.read_text(encoding="utf-8") == "", "fail-closed 后不得写入任何字节"


def test_dedup_within_batch_and_against_existing(tmp_path):
    p = _tmp(tmp_path)
    r1 = c1.ingest([dict(GOOD), dict(GOOD)], path=p, write=True)
    assert r1["accepted"] == 1 and r1["duplicates"] == 1
    r2 = c1.ingest([dict(GOOD)], path=p, write=True)
    assert r2["accepted"] == 0 and r2["duplicates"] == 1, "与已有行重复应被丢弃"


def test_append_only_grows(tmp_path):
    p = _tmp(tmp_path)
    a = {**GOOD, "timestamp": "2026-09-20T01:00:00"}
    b = {**GOOD, "timestamp": "2026-09-20T02:00:00"}
    c1.ingest([a], path=p, write=True)
    c1.ingest([b], path=p, write=True)
    lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 2
    assert json.loads(lines[0])["timestamp"] == "2026-09-20T01:00:00"


def test_csv_roundtrip(tmp_path):
    src = tmp_path / "in.csv"
    with src.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["timestamp", "kc_id", "action_type", "correct", "duration_s"])
        w.writeheader()
        w.writerow({"timestamp": "2026-09-20T03:00:00", "kc_id": "ATOM-MEM-ALLOC-001",
                    "action_type": "test", "correct": "false", "duration_s": "3"})
    recs = c1.load_records(src)
    assert len(recs) == 1 and recs[0]["correct"] is False
    assert recs[0]["duration_s"] == 3.0


def test_stats_empty(tmp_path):
    s = c1.stats(_tmp(tmp_path))
    assert s["exists"] and s["n"] == 0


def test_check_passes():
    assert c1.main(["--check"]) == 0
