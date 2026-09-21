#!/usr/bin/env python3
"""614 B3 回归测试：learner_ood_evaluator（OOD 题 + 跃迁判定 + 记录）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_behavior_logger as b1  # noqa: E402
import learner_ood_evaluator as b3  # noqa: E402


def test_ood_question_format(tmp_path: Path) -> None:
    qs = b3.bank()
    assert len(qs) >= 5
    for q in qs[:5]:
        assert {"kc_id", "question", "answer", "difficulty", "source"} <= set(q.keys())
        assert q["source"] in ("handcrafted", "generated")


def _learner_store_with_kc_mastered(tmp_path: Path, kc: str) -> Path:
    store = tmp_path / "beh.jsonl"
    for _ in range(10):
        b1.record(store, "default", kc, "correct", "exercise", None, False)
    return store


def test_jump_verdict(tmp_path: Path) -> None:
    kc0 = b1._kc_ids()[0]
    kc1 = b1._kc_ids()[1]
    learner = _learner_store_with_kc_mastered(tmp_path, kc0)
    jumps = tmp_path / "jumps.jsonl"
    # 掌握度≥0.8 且 OOD≥0.8 → 跃迁
    r1 = b3.evaluate(learner, jumps, kc0, 0.9)
    assert r1["verdict"] == "jump"
    # OOD<0.8 → 不跃迁
    r2 = b3.evaluate(learner, jumps, kc0, 0.5)
    assert r2["verdict"] == "no_jump"
    # 掌握度不足（kc1 未学）→ 不跃迁
    r3 = b3.evaluate(learner, jumps, kc1, 1.0)
    assert r3["verdict"] == "no_jump"


def test_jump_record_append_only(tmp_path: Path) -> None:
    kc0 = b1._kc_ids()[0]
    learner = _learner_store_with_kc_mastered(tmp_path, kc0)
    jumps = tmp_path / "jumps.jsonl"
    b3.evaluate(learner, jumps, kc0, 0.9)  # 应写入 1 条
    recs = b3.load_jumps(jumps)
    assert len(recs) == 1
    assert recs[0]["verdict"] == "jump"
    assert {"user_id", "kc_id", "jump_time", "pre_mastery", "ood_score",
            "post_mastery", "verdict"} <= set(recs[0].keys())
    b3.evaluate(learner, jumps, kc0, 0.5)  # 不写
    assert len(b3.load_jumps(jumps)) == 1  # 仍为 1（append-only，仅 jump 入）


def test_stats(tmp_path: Path) -> None:
    kc0 = b1._kc_ids()[0]
    learner = _learner_store_with_kc_mastered(tmp_path, kc0)
    jumps = tmp_path / "jumps.jsonl"
    b3.evaluate(learner, jumps, kc0, 0.95)
    s = b3.stats(jumps)
    assert s["total_records"] == 1 and s["jumps"] == 1
