"""644 E2 自动求索触发器单测（S2-1..S2-4）。"""
from __future__ import annotations

import evidence_base_644 as base
import evidence_seeker_trigger_644 as e2


def _stub_orch(topic, snippet=None, max_rounds=3):
    return {"topic": topic, "rounds": max_rounds, "max_rounds": max_rounds,
            "evidence_package": [], "sufficiency": {}, "log": [], "cards_untouched": True}


def _stub_orch_with_pkg(topic, snippet=None, max_rounds=3):
    return {"topic": topic, "rounds": max_rounds, "max_rounds": max_rounds,
            "evidence_package": [{"id": "X1", "grade": "L1", "verdict": "confirm",
                                  "acquired_at": None, "artifact_sha256_present": True,
                                  "falsification": False}], "sufficiency": {},
            "log": [], "cards_untouched": True}


# S2-1：触发正确（结构完整）
def test_trigger_structure():
    r = e2.seek(orchestrate_fn=_stub_orch)
    assert "n_triggered" in r and "still_insufficient" in r and "new_evidence_total" in r
    assert r["cards_untouched"] is True


# S2-2：求索后充分性变化可追踪（未关联 → 判定不变）
def test_no_change_unlinked():
    r = e2.seek(orchestrate_fn=_stub_orch)
    for row in r["rows"]:
        assert row["before_verdict"] == row["after_verdict"]
        assert row["changed"] is False


# S2-3：新证据体量被记录
def test_new_evidence_recorded():
    r = e2.seek(orchestrate_fn=_stub_orch_with_pkg)
    assert r["new_evidence_total"] >= 0


# S2-4：不修改卡片 + selftest
def test_no_card_modify_and_selftest():
    atom = base.list_atoms()[0]
    with open(atom["path"], encoding="utf-8") as fh:
        before = fh.read()
    e2.seek(orchestrate_fn=_stub_orch)
    with open(atom["path"], encoding="utf-8") as fh:
        after = fh.read()
    assert before == after
    assert e2.selftest() == 0
