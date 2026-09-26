"""644 B2 证据充分性判定器单测（S2-1..S2-6）。"""
from __future__ import annotations

import evidence_base_644 as base
import evidence_sufficiency_644 as b2


def _good(n=3):
    return [{"id": f"E{i}", "grade": "L1", "verdict": "confirm", "acquired_at": None,
             "artifact_sha256_present": True, "falsification": False} for i in range(n)]


# S2-1：已知充分卡必判充分
def test_known_sufficient():
    r = b2.judge("C", _good(3))
    assert r["verdict"] == "充分" and r["missing"] == []


# S2-2：已知不足卡必判不足（无 L1/L2 且 1 条）
def test_known_insufficient():
    r = b2.judge("C", [{"id": "E1", "grade": "L4", "verdict": "confirm",
                        "acquired_at": None, "artifact_sha256_present": True,
                        "falsification": False}])
    assert r["verdict"] in ("不足", "需人审")
    miss = "".join(r["missing"])
    assert "缺少 L1/L2 权威证据" in miss
    assert "独立证据不足" in miss


# S2-3：反例未处理 → 需人审
def test_refute_unhandled():
    r = b2.judge("C", _good(3) + [{"id": "E9", "grade": "L2", "verdict": "refute",
                                   "acquired_at": None, "artifact_sha256_present": True,
                                   "falsification": False}])
    assert r["verdict"] == "需人审"
    assert "存在反例但未处理" in "".join(r["missing"])


# S2-4：hash 缺失 → 需人审
def test_hash_missing():
    r = b2.judge("C", [dict(_good(1)[0], artifact_sha256_present=False)])
    assert r["verdict"] == "需人审"
    assert "artifact_sha256" in "".join(r["missing"])


# S2-5：边界（恰好 3 条独立判充分，2 条判不足）
def test_boundary_three():
    assert b2.judge("C", _good(3))["verdict"] == "充分"
    assert "独立证据不足" in "".join(b2.judge("C", _good(2))["missing"])


# S2-6：全量判定覆盖 28(27) 张卡且不抛错
def test_judge_all():
    allr = b2.judge_all()
    assert len(allr) == len(base.list_atoms())
    assert b2.selftest() == 0
