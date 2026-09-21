"""621 A4 · 闭环第二轮（新 mutation）单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import mutation_generator_621 as MG  # noqa: E402
import mutation_quality_621 as Q  # noqa: E402

ROUND1 = os.path.join(ROOT, "data", "mutation", "new_mutations_621_round1.jsonl")
CARDS = ["atoms/mem/ATOM-MEM-LEAK-001.md", "evidence/conc/EV-CONC-001.md"]


def _muts():
    if os.path.exists(ROUND1):
        return [json.loads(ln) for ln in open(ROUND1, encoding="utf-8") if ln.strip()]
    return MG.generate(CARDS, count=6, strategy="all")


def test_to_v7_records_shape():
    recs = Q.to_v7_records(_muts(), MG.load_v7())
    assert recs
    for r in recs:
        assert {"card", "op", "point", "verdict", "equivalent"} <= set(r)
        assert r["verdict"] in ("blocked", "escaped", "n_a", "infra_error")


def test_round2_runs_three_rounds():
    res = Q.run_round2(_muts(), MG.load_v7(), rounds=3, top_n=10, weights="W2")
    assert len(res["rounds"]) == 3
    assert res["candidate_total"] == len(_muts())


def test_round2_deterministic():
    a = Q.run_round2(_muts(), MG.load_v7(), rounds=3, top_n=10, weights="W2")
    b = Q.run_round2(_muts(), MG.load_v7(), rounds=3, top_n=10, weights="W2")
    assert a == b


def test_round2_windows_advance():
    res = Q.run_round2(_muts(), MG.load_v7(), rounds=3, top_n=10, weights="W2")
    assert [r["window"] for r in res["rounds"]] == [[0, 10], [10, 20], [20, 30]]


def test_round2_no_new_escape_when_all_blocked():
    res = Q.run_round2(_muts(), MG.load_v7(), rounds=3, top_n=10, weights="W2")
    # 本轮预测判决全为 blocked/n_a ⇒ 不应出现新逃逸
    assert res["new_escapes"] == []
    assert res["vfdr_open"] == 0
    assert res["converged"] is True


def test_round2_empty_input():
    res = Q.run_round2([], MG.load_v7(), rounds=2, top_n=5, weights="W2")
    assert res["candidate_total"] == 0
    assert all(r["selected"] == 0 for r in res["rounds"])


def test_selftest_passes():
    assert Q.selftest() == 0
