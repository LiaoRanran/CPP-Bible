#!/usr/bin/env python3
"""C2 回归测试：learner_mastery_update_613（BKT 真实递推）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_mastery_update_613 as c2  # noqa: E402
import learner_state as ls  # noqa: E402


def _store(tmp_path: Path) -> Path:
    p = tmp_path / "state.jsonl"
    ls.init(p)
    return p


def _events(n_true: int, n_false: int, kc: str = "ATOM-MEM-ALLOC-001") -> list[dict]:
    ev = []
    for i in range(n_true):
        ev.append({"timestamp": f"2026-09-20T{i:02d}:00:00", "kc_id": kc,
                   "action_type": "answer", "correct": True})
    for i in range(n_false):
        ev.append({"timestamp": f"2026-09-21T{i:02d}:00:00", "kc_id": kc,
                   "action_type": "answer", "correct": False})
    return ev


def test_no_events_means_no_recurrence(tmp_path):
    p = _store(tmp_path)
    ev = c2.load_events(tmp_path / "none.jsonl")
    assert ev == []
    good, skipped, unknown = c2.usable(ev)
    assert good == [] and skipped == 0
    before = c2.snapshot(p)
    assert c2.apply_events(p, good) == 0
    assert c2.snapshot(p) == before


def test_review_events_do_not_drive_recurrence(tmp_path):
    ev = [{"timestamp": "2026-09-20T01:00:00", "kc_id": "ATOM-MEM-ALLOC-001",
           "action_type": "review", "correct": None}]
    good, skipped, unknown = c2.usable(ev)
    assert good == [] and skipped == 1, "review 不带正确性 ⇒ 不参与递推且被计数"


def test_unknown_kc_counted_not_recurred(tmp_path):
    ev = [{"timestamp": "2026-09-20T01:00:00", "kc_id": "ATOM-NOPE",
           "action_type": "answer", "correct": True}]
    good, skipped, unknown = c2.usable(ev)
    assert good == [] and unknown == 1


def test_all_correct_raises_mastery(tmp_path):
    p = _store(tmp_path)
    kc = "ATOM-MEM-ALLOC-001"
    before = c2.snapshot(p)[kc]
    c2.apply_events(p, _events(5, 0, kc))
    assert c2.snapshot(p)[kc] > before


def test_all_wrong_lowers_mastery(tmp_path):
    p = _store(tmp_path)
    kc = "ATOM-MEM-ALLOC-001"
    c2.apply_events(p, _events(3, 0, kc))
    mid = c2.snapshot(p)[kc]
    c2.apply_events(p, _events(0, 3, kc))
    assert c2.snapshot(p)[kc] < mid


def test_events_sorted_by_timestamp(tmp_path):
    f = tmp_path / "b.jsonl"
    rows = [{"timestamp": "2026-09-22T01:00:00", "kc_id": "X", "action_type": "answer", "correct": True},
            {"timestamp": "2026-09-20T01:00:00", "kc_id": "X", "action_type": "answer", "correct": True}]
    f.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    ev = c2.load_events(f)
    assert [e["timestamp"] for e in ev] == ["2026-09-20T01:00:00", "2026-09-22T01:00:00"]


def test_append_only_state_grows(tmp_path):
    p = _store(tmp_path)
    n0 = len([ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()])
    c2.apply_events(p, _events(2, 1))
    n1 = len([ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()])
    assert n1 == n0 + 3


def test_check_passes():
    assert c2.main(["--check"]) == 0
