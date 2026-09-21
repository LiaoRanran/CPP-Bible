#!/usr/bin/env python3
"""615 D2 回归测试：学习者镜像闭环验证（**模拟数据**，不写 learner_state.json）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_argument_link as b4  # noqa: E402
import learner_behavior_logger as b1  # noqa: E402
import learner_ood_evaluator as b3  # noqa: E402


def test_bkt_recurrence(tmp_path: Path) -> None:
    kc = b1._kc_ids()[0]
    up = tmp_path / "up.jsonl"
    for _ in range(6):
        b1.record(up, "default", kc, "correct", "exercise", None, False)
    assert b1.replay(up)[kc] > 0.1                      # 正确 → 上升
    down = tmp_path / "down.jsonl"
    for _ in range(6):
        b1.record(down, "default", kc, "incorrect", "exercise", None, False)
    assert b1.replay(down)[kc] < 0.1                    # 错误 → 下降


def test_recommendation_threshold(tmp_path: Path) -> None:
    store = tmp_path / "b.jsonl"
    before = b1.recommend_next(store, "default", 0.5)
    assert len(before) >= 1
    kc = sorted(before)[0]
    for _ in range(6):
        b1.record(store, "default", kc, "correct", "exercise", None, False)
    after = b1.recommend_next(store, "default", 0.5)
    assert kc not in after                               # 掌握后不再推荐


def test_transition_condition(tmp_path: Path) -> None:
    kc = b1._kc_ids()[0]
    learner = tmp_path / "l.jsonl"
    for _ in range(10):
        b1.record(learner, "default", kc, "correct", "exercise", None, False)
    jumps = tmp_path / "j.jsonl"
    assert b3.evaluate(learner, jumps, kc, 0.9)["verdict"] == "jump"      # ≥0.8 且 OOD≥0.8
    assert b3.evaluate(learner, jumps, kc, 0.5)["verdict"] == "no_jump"   # OOD<0.8


def test_argument_link(tmp_path: Path) -> None:
    # 用真实命题库（只读）验证 KC→论证链→复盘推荐
    chain = b4.chains_for_kc("ATOM-CONC-FENCE-001")
    assert chain and chain[0]["claim_type"] == "observation"
    learner = tmp_path / "l.jsonl"
    for _ in range(10):
        b1.record(learner, "default", "ATOM-CONC-FENCE-001", "correct", "exercise", None, False)
    store = tmp_path / "u.jsonl"
    recs = b4.recommend_argument_review(learner, store, "default", 0.5)
    assert "ATOM-CONC-FENCE-001" in recs                 # 已掌握但论证未理解 ⇒ 复盘推荐
    for c in chain:
        b4.record(store, "default", "ATOM-CONC-FENCE-001", c["prop_key"], True)
    recs2 = b4.recommend_argument_review(learner, store, "default", 0.5)
    assert "ATOM-CONC-FENCE-001" not in recs2            # 理解后移出
