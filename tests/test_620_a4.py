"""620 A4 · VFDR 实时计算 单测"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import adversarial_loop_620 as L  # noqa: E402
import vfdr_realtime_620 as V  # noqa: E402

MINI = L._mini()


def test_轮数与序列长度一致():
    r = V.compute_vfdr(MINI, rounds=3, top_n=2, weights_name="W1")
    assert len(r["rounds"]) == 3
    assert len(r["vfdr_series"]) == 3


def test_空输入不崩溃():
    r = V.compute_vfdr([], rounds=2, top_n=5)
    assert r["total_verified"] == 0
    assert r["vfdr_cumulative_final"] == 0.0


def test_累计等于各轮之和():
    r = V.compute_vfdr(MINI, rounds=2, top_n=2, weights_name="W1")
    assert r["total_verified"] == sum(x["verified"] for x in r["rounds"])
    assert r["total_new_escapes"] == sum(x["new_escapes"] for x in r["rounds"])


def test_等价变异不计入():
    ranked_ids = [L.A.variant_id(x["rec"]) for x in L.rank(MINI, L._weights("W1"))]
    assert not any("M6" in i for i in ranked_ids)


def test_已知逃逸不计入新发现():
    recs = MINI + [{"card": "evidence/conc/EV-CONC-001.md", "op": "M1",
                    "point": "删 negative_controls", "verdict": "escaped",
                    "kind": None, "new_block": [], "new_warn": [], "equivalent": False}]
    r = V.compute_vfdr(recs, rounds=1, top_n=10, weights_name="W2")
    # W2 下该逃逸排第 1，应命中 known_hits 而非 new_escapes
    assert r["total_known_hits"] >= 1


def test_确定性同输入同输出():
    assert V.compute_vfdr(MINI, rounds=2, top_n=2, weights_name="W2") == \
           V.compute_vfdr(MINI, rounds=2, top_n=2, weights_name="W2")


def test_真实基线_vfdr_结构恒为零():
    if not os.path.exists(V.LOOP.DEFAULT_BASELINE):
        return
    for w in ("W1", "W2"):
        r = V.compute_vfdr(L.load_baseline(), rounds=3, top_n=20, weights_name=w)
        assert r["total_new_escapes"] == 0
        assert r["vfdr_cumulative_final"] == 0.0
        assert r["converged"] is True


def test_真实基线_已知逃逸命中_w1_晚于_w2():
    if not os.path.exists(V.LOOP.DEFAULT_BASELINE):
        return
    w1 = V.compute_vfdr(L.load_baseline(), rounds=3, top_n=20, weights_name="W1")
    w2 = V.compute_vfdr(L.load_baseline(), rounds=3, top_n=20, weights_name="W2")
    r1 = next(i for i, x in enumerate(w1["rounds"], 1) if x["known_hits"])
    r2 = next(i for i, x in enumerate(w2["rounds"], 1) if x["known_hits"])
    assert r2 < r1  # W2 更早命中


def test_报告渲染含汇总表():
    md = V.render_markdown({"W1": V.compute_vfdr(MINI, rounds=1, top_n=2)})
    assert "VFDR" in md and "累计" in md


def test_selftest_通过():
    assert V.selftest() == 0
