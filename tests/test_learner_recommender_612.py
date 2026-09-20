#!/usr/bin/env python3
"""D4 回归测试：基于掌握度的内容推荐原型（只读）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import learner_recommender as d4  # noqa: E402
import learner_state as d3  # noqa: E402


def _store_all(tmp_path, prob):
    store = tmp_path / "learner.jsonl"
    d3.init(store, initial_prob=prob)
    return store


def test_recommend_produces_cards(tmp_path):
    store = _store_all(tmp_path, 0.1)
    rec = d4.recommend(store, top_n=5)
    assert len(rec["recommendations"]) >= 1


def test_prereq_hard_constraint(tmp_path):
    # 默认 store 全 0.1 ⇒ 前置未达 0.5 的 KC 不应被推荐
    store = _store_all(tmp_path, 0.1)
    rec = d4.recommend(store, top_n=27)
    mast = d4._mastery(store)
    inv = d4._kc_inventory()
    by_id = {k["id"]: k for k in inv["kcs"]}
    rec_ids = {r["kc"] for r in rec["recommendations"]}
    for cid in rec_ids:
        for p in by_id[cid]["prerequisites"]:
            assert mast.get(p, 0.1) > 0.5, f"推荐了前置未达 0.5 的 KC：{cid}←{p}"


def test_mastered_message(tmp_path):
    # 所有 KC 掌握度 > 0.9 ⇒ 输出已掌握提示且 return 0
    store = _store_all(tmp_path, 0.95)
    rc = d4.main(["--check", "--store", str(store)])
    assert rc == 0


def test_check_passes(tmp_path):
    store = _store_all(tmp_path, 0.1)
    assert d4.main(["--check", "--store", str(store)]) == 0


def test_learning_path_runs(tmp_path):
    store = _store_all(tmp_path, 0.1)
    path = d4.learning_path(store, 5)
    assert len(path) >= 1
    ids = [p["kc"] for p in path]
    assert len(ids) == len(set(ids))  # 无重复


def test_top_n_respected(tmp_path):
    store = _store_all(tmp_path, 0.1)
    rec = d4.recommend(store, top_n=3)
    assert len(rec["recommendations"]) <= 3
