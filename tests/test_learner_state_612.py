#!/usr/bin/env python3
"""D3 回归测试：用户掌握度存储（append-only + BKT 递推 + 模拟）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import learner_state as d3  # noqa: E402


def _init(tmp_path):
    store = tmp_path / "learner.jsonl"
    d3.init(store)
    return store


def test_init_all_kc_01(tmp_path):
    store = _init(tmp_path)
    recs = d3.load_all(store)
    assert len(recs) == 27
    assert all(abs(r["mastery_prob"] - 0.1) < 1e-9 for r in recs)
    assert all(r["kind"] == "init" for r in recs)


def test_init_idempotent(tmp_path):
    store = _init(tmp_path)
    added = d3.init(store)  # 已存在 ⇒ 不再添加
    assert added == 0
    assert len(d3.load_all(store)) == 27


def test_update_changes_mastery(tmp_path):
    store = _init(tmp_path)
    r = d3.update(store, "ATOM-MEM-ALLOC-001", True)
    assert r["mastery_prob"] > 0.1


def test_update_wrong_lowers(tmp_path):
    store = _init(tmp_path)
    up = d3.update(store, "ATOM-MEM-ALLOC-001", True)
    after = d3.update(store, "ATOM-MEM-ALLOC-001", False)
    assert after["mastery_prob"] < up["mastery_prob"]


def test_check_passes(tmp_path):
    store = _init(tmp_path)
    d3.update(store, "ATOM-MEM-ALLOC-001", True)
    d3.simulate(store, 5, seed=1)
    assert d3.main(["--check", "--store", str(store)]) == 0


def test_append_only(tmp_path):
    store = _init(tmp_path)
    before = store.read_text(encoding="utf-8")
    n_before = len(before.splitlines())
    d3.update(store, "ATOM-MEM-ALLOC-001", True)
    after = store.read_text(encoding="utf-8")
    n_after = len(after.splitlines())
    # 行数增加 1，且原有 init 内容完全保留（未被修改）
    assert n_after == n_before + 1
    assert before in after


def test_simulate_success(tmp_path):
    store = _init(tmp_path)
    n = d3.simulate(store, 8, seed=42)
    assert n == 8
    recs = [r for r in d3.load_all(store) if r.get("kind") == "update"]
    assert any(r.get("simulated") for r in recs)


def test_query_single(tmp_path):
    store = _init(tmp_path)
    d3.update(store, "ATOM-MEM-ALLOC-001", True)
    recs = d3.query(store, "ATOM-MEM-ALLOC-001")
    assert len(recs) == 1
    assert recs[0]["kc_id"] == "ATOM-MEM-ALLOC-001"
