"""620 A3 · 攻击目标函数权重校准实验 单测"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import adversarial_loop_620 as L  # noqa: E402
import adversarial_weight_calibration_620 as C  # noqa: E402

MINI = L._mini()


def test_六种权重全覆盖():
    cal = C.calibrate(MINI, top_n=3)
    assert set(cal) == {"W1", "W2", "W3", "W4", "W5", "W6"}


def test_w1_重叠率为基准_none():
    cal = C.calibrate(MINI, top_n=3)
    assert cal["W1"]["overlap_with_w1"] is None
    assert cal["W2"]["overlap_with_w1"] is not None


def test_w3_na_权重与_w1_排序一致():
    cal = C.calibrate(MINI, top_n=3)
    assert cal["W3"]["top20"] == cal["W1"]["top20"]


def test_w6_帕累托无单一排名():
    cal = C.calibrate(MINI, top_n=3)
    assert cal["W6"]["escape_rank"] is None
    assert cal["W6"]["pareto"]["front_size"] >= 1


def test_分布统计字段完整():
    d = C.calibrate(MINI, top_n=3)["W1"]["dist"]
    assert {"n", "mean", "max", "min", "gt_0_4"} <= set(d)


def test_确定性同输入同输出():
    assert C.calibrate(MINI, top_n=3) == C.calibrate(MINI, top_n=3)


def test_空输入不崩溃():
    cal = C.calibrate([], top_n=5)
    assert cal["W1"]["top20"] == []
    assert cal["W1"]["dist"]["n"] == 0


def test_真实基线_w2_真逃逸排第一():
    if not os.path.exists(C.DEFAULT_BASELINE):
        return
    cal = C.calibrate(L.load_baseline(), top_n=20)
    assert cal["W2"]["escape_rank"] == 1
    assert cal["W1"]["escape_rank"] == 57


def test_各权重_top20_长度不超_top_n():
    cal = C.calibrate(MINI, top_n=2)
    for k in ("W1", "W2", "W3", "W4", "W5"):
        assert len(cal[k]["top20"]) <= 2


def test_selftest_通过():
    assert C.selftest() == 0
