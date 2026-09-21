#!/usr/bin/env python3
"""614 B1 回归测试：learner_behavior_logger（行为采集 + BKT 递推 + 推荐门槛）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_behavior_logger as b1  # noqa: E402

KC = "ATOM-CONC-FENCE-001"


def test_single_record(tmp_path: Path) -> None:
    store = tmp_path / "beh.jsonl"
    rec = b1.record(store, "default", KC, "correct", "exercise", None, False)
    assert rec["kc_id"] == KC and rec["action"] == "correct"
    all_recs = b1.load_all(store)
    assert len(all_recs) == 1
    assert set(all_recs[0].keys()) >= {"user_id", "kc_id", "action", "timestamp", "source"}


def test_batch_import(tmp_path: Path) -> None:
    store = tmp_path / "beh.jsonl"
    csv_path = tmp_path / "batch.csv"
    csv_path.write_text(
        "kc_id,action,source,difficulty\n"
        f"{KC},correct,exercise,2\n"
        f"{KC},incorrect,quiz,2\n"
        "ATOM-CONC-FENCE-002,hint,review,3\n",
        encoding="utf-8",
    )
    n = b1.import_file(store, csv_path, "default")
    assert n == 3
    recs = b1.load_all(store)
    assert len(recs) == 3
    # JSONL 导入路径
    jl = tmp_path / "batch.jsonl"
    jl.write_text(json.dumps({"kc_id": KC, "action": "skip", "source": "review"}) + "\n",
                  encoding="utf-8")
    n2 = b1.import_file(store, jl, "default")
    assert n2 == 1


def test_bkt_recurrence(tmp_path: Path) -> None:
    store = tmp_path / "beh.jsonl"
    # 5 连对 → 掌握度应显著高于初始 0.1
    for _ in range(5):
        b1.record(store, "default", KC, "correct", "exercise", None, False)
    mast = b1.replay(store)
    assert mast[KC] > 0.1
    # 连错应拉低
    store2 = tmp_path / "beh2.jsonl"
    for _ in range(5):
        b1.record(store2, "default", KC, "incorrect", "exercise", None, False)
    mast2 = b1.replay(store2)
    assert mast2[KC] < 0.1


def test_mastery_rises_after_simulate(tmp_path: Path) -> None:
    store = tmp_path / "beh.jsonl"
    b1.simulate(store, kcs_n=10, rounds=5, seed=7, acc_start=0.3, acc_end=0.8)
    mast = b1.replay(store)
    risen = [k for k, v in mast.items() if v >= 0.5]
    assert len(risen) >= 5


def test_recommendation_changes_with_mastery(tmp_path: Path) -> None:
    store = tmp_path / "beh.jsonl"
    before = set(b1.recommend_next(store, "default", 0.5))
    assert len(before) >= 1  # 至少根 KC（前置已满足、掌握度 0.1<0.5）被推荐
    kc = sorted(before)[0]  # 取一个初始被推荐的 KC（前置必然已满足）
    for _ in range(6):
        b1.record(store, "default", kc, "correct", "exercise", None, False)
    after = set(b1.recommend_next(store, "default", 0.5))
    # 该 KC 掌握度升至 ≥0.5 后不再被推荐（前置未达 0.5 的 KC 不再推荐）
    assert kc not in after
    # 推荐集合随掌握度变化而改变
    assert after != before
