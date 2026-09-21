#!/usr/bin/env python3
"""614 E2 回归测试：oracle_verification_614（验证流程机制）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import oracle_verification_614 as e2  # noqa: E402


def test_plan_and_assignment() -> None:
    cards = e2.load_plan()
    assert len(cards) == 83
    planned = e2.assign_verifiers(cards, 2)
    assert len(planned) == 83
    for p in planned:
        assert len(p["verifiers"]) >= 2
        assert len(set(p["verifiers"])) == len(p["verifiers"])  # 互不相同


def test_record_append_only(tmp_path: Path) -> None:
    store = tmp_path / "rec.jsonl"
    e2.record(store, "ATOM-X", "oracle-tsan", "confirm")
    e2.record(store, "ATOM-X", "oracle-gcc", "refute")
    assert len(e2.load_records(store)) == 2


def test_verifier_independence(tmp_path: Path) -> None:
    store = tmp_path / "rec.jsonl"
    e2.record(store, "ATOM-X", "oracle-tsan", "confirm")
    e2.record(store, "ATOM-X", "oracle-tsan", "confirm")  # 同一验证者重复
    assert e2.verdict_for(store, "ATOM-X", 2) == "pending"  # 不叠加


def test_fail_closed_verdict(tmp_path: Path) -> None:
    store = tmp_path / "rec.jsonl"
    e2.record(store, "ATOM-X", "oracle-tsan", "confirm")
    e2.record(store, "ATOM-X", "oracle-gcc", "confirm")
    assert e2.verdict_for(store, "ATOM-X", 2) == "confirmed"
    e2.record(store, "ATOM-X", "oracle-replay", "refute")
    assert e2.verdict_for(store, "ATOM-X", 2) == "refuted"
    store2 = tmp_path / "rec2.jsonl"
    e2.record(store2, "ATOM-X", "oracle-tsan", "abstain")
    assert e2.verdict_for(store2, "ATOM-X", 2) == "pending"
