"""620 A1 · 攻击-验证迭代闭环沙箱 单测"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import adversarial_loop_620 as L  # noqa: E402

MINI = [
    {"card": "c", "op": "M1", "point": "删 negative_controls", "verdict": "escaped",
     "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
    {"card": "c", "op": "M2", "point": "路径转大写", "verdict": "blocked",
     "kind": "warn_only", "new_block": [], "new_warn": ["CARD-PATH-NOT-CANONICAL:x"],
     "equivalent": False},
    {"card": "c", "op": "M7", "point": "sha256 改一位", "verdict": "blocked",
     "kind": "strict", "new_block": ["EV-ARTIFACT-PRODUCER:x"], "new_warn": [],
     "equivalent": False},
    {"card": "c", "op": "M7", "point": "-", "verdict": "n_a",
     "kind": None, "new_block": [], "new_warn": [], "equivalent": False},
    {"card": "c", "op": "M6", "point": "块式→flow", "verdict": "escaped",
     "kind": None, "new_block": [], "new_warn": [], "equivalent": True},
]


def test_determinism_同输入同输出():
    assert L.run_loop(MINI, rounds=2, top_n=2, weights_name="W1") == \
           L.run_loop(MINI, rounds=2, top_n=2, weights_name="W1")


def test_空输入不崩溃():
    r = L.run_loop([], rounds=2, top_n=5)
    assert r["n_ranked"] == 0
    assert all(x["selected"] == 0 for x in r["rounds"])


def test_单轮与多轮轮数正确():
    assert len(L.run_loop(MINI, rounds=1, top_n=3)["rounds"]) == 1
    assert len(L.run_loop(MINI, rounds=3, top_n=2)["rounds"]) == 3


def test_窗口逐轮推进不重叠():
    # MINI 5 条中：n_a 1 条、equivalent 1 条均不入 ranked ⇒ ranked=3
    r = L.run_loop(MINI, rounds=2, top_n=2)
    assert r["n_ranked"] == 3
    assert r["rounds"][0]["window"] == [0, 2]
    assert r["rounds"][1]["window"] == [2, 3]


def test_vfdr_事件被登记为_triaged():
    r = L.run_loop(MINI, rounds=1, top_n=5)
    assert r["vfdr_open"] >= 1
    assert all(e["state"] == "TRIAGED" for e in r["vfdr_events"])
    assert all(e["source"] in ("MATRIX", "REDTEAM", "GOV", "PARSE") for e in r["vfdr_events"])


def test_等效变异被剔出_ranked():
    r = L.run_loop(MINI, rounds=1, top_n=5)
    ids = [i["id"] for rr in r["rounds"] for i in rr["items"]]
    # MINI 中唯一的 equivalent 是 M6「块式→flow」，不得出现在 ranked 窗口内
    assert not any("M6" in i for i in ids)
    assert not any("块式→flow" in i for i in ids)


def test_w3_na_权重与_w1_排序一致():
    a = [i["id"] for i in L.run_loop(MINI, rounds=1, top_n=5, weights_name="W1")["rounds"][0]["items"]]
    b = [i["id"] for i in L.run_loop(MINI, rounds=1, top_n=5, weights_name="W3")["rounds"][0]["items"]]
    assert a == b


def test_w6_帕累托无权重仍可运行():
    r = L.run_loop(MINI, rounds=1, top_n=3, weights_name="W6")
    assert r["weights_vector"] is None
    assert len(r["rounds"][0]["items"]) == 3


def test_排名给出已知逃逸位置():
    recs = MINI + [{"card": "evidence/conc/EV-CONC-001.md", "op": "M1",
                    "point": "删 negative_controls", "verdict": "escaped",
                    "kind": None, "new_block": [], "new_warn": [], "equivalent": False}]
    r = L.run_loop(recs, rounds=1, top_n=10)
    assert r["known_escape_rank"] is not None


def test_报告渲染含关键字段():
    md = L.render_markdown(L.run_loop(MINI, rounds=1, top_n=2))
    assert "闭环运行报告" in md and "VFDR" in md


def test_selftest_通过():
    assert L.selftest() == 0
