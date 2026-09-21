"""620 A2 · 第一轮闭环实际运行 可复现性单测（依赖真实 v7 基线）"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import adversarial_loop_620 as L  # noqa: E402

BASELINE = L.DEFAULT_BASELINE


def _load():
    if not os.path.exists(BASELINE):
        return None
    return L.load_baseline(BASELINE)


def test_真实基线可加载且规模正确():
    recs = _load()
    assert recs is not None, "v7 基线缺失"
    assert len(recs) == 1593


def test_w1_三轮可复现_已知逃逸排57():
    r = L.run_loop(_load(), rounds=3, top_n=20, weights_name="W1")
    assert r["n_ranked"] == 1406
    assert r["known_escape_rank"] == 57
    assert len(r["rounds"]) == 3


def test_w2_三轮可复现_已知逃逸排1_且首轮即命中():
    r = L.run_loop(_load(), rounds=3, top_n=20, weights_name="W2")
    assert r["known_escape_rank"] == 1
    assert r["rounds"][0]["escaped"] == 1
    assert r["rounds"][0]["known_escapes"] == [L.KNOWN_ESCAPE]


def test_w1_需三轮才命中已知逃逸():
    r = L.run_loop(_load(), rounds=3, top_n=20, weights_name="W1")
    assert sum(len(x["known_escapes"]) for x in r["rounds"][:2]) == 0
    assert r["rounds"][2]["known_escapes"] == [L.KNOWN_ESCAPE]


def test_闭环零新逃逸_结构必然():
    for w in ("W1", "W2"):
        r = L.run_loop(_load(), rounds=3, top_n=20, weights_name=w)
        assert r["new_escapes"] == []
        assert r["vfdr_open"] == 0
        assert r["converged"] is True


def test_两次运行结果完全一致():
    recs = _load()
    assert L.run_loop(recs, rounds=3, top_n=20, weights_name="W2") == \
           L.run_loop(recs, rounds=3, top_n=20, weights_name="W2")


def test_窗口严格推进不重叠():
    r = L.run_loop(_load(), rounds=3, top_n=20, weights_name="W1")
    assert [x["window"] for x in r["rounds"]] == [[0, 20], [20, 40], [40, 60]]
