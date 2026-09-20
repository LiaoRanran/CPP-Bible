#!/usr/bin/env python3
"""D2 回归测试：BKT 最小实现（纯标准库）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import bkt_solver as d2  # noqa: E402


def test_run_sequence_length_and_bounds():
    m = d2.BKTModel()
    r = m.run_sequence([1, 0, 1, 1, 0])
    assert len(r["mastery_after"]) == 5
    assert all(0.0 <= v <= 1.0 for v in r["mastery_after"])
    assert all(0.0 <= v <= 1.0 for v in r["predict_correct_before"])


def test_predict_in_range():
    m = d2.BKTModel()
    assert 0.0 <= m.predict_correct(0.5) <= 1.0
    assert 0.0 <= m.predict_correct(0.0) <= 1.0
    assert 0.0 <= m.predict_correct(1.0) <= 1.0


def test_all_correct_monotonic_increasing():
    m = d2.BKTModel()
    seq = m.run_sequence([1] * 15)["mastery_after"]
    assert all(seq[i + 1] >= seq[i] for i in range(len(seq) - 1))
    assert seq[-1] > seq[0]


def test_all_wrong_monotonic_decreasing():
    m = d2.BKTModel()
    seq = m.run_sequence([0] * 15)["mastery_after"]
    assert all(seq[i + 1] <= seq[i] for i in range(len(seq) - 1))
    assert seq[-1] < seq[0]


def test_learner_state_update():
    m = d2.BKTModel()
    st = d2.LearnerState(kc_id="ATOM-MEM-ALLOC-001", mastery_prob=0.1)
    before = st.mastery_prob
    after_correct = st.update(m, True)
    # 答对后掌握度应上升
    assert after_correct > before
    after_wrong = st.update(m, False)
    # 答错后掌握度应下降（相对上一步）
    assert after_wrong < after_correct


def test_fit_reasonable():
    # 多数答对的数据，拟合参数应在合法范围
    seqs = [[1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 0, 1, 1], [1, 1, 1, 1]]
    m = d2.fit(seqs)
    for name in ("p_l0", "p_t", "p_s", "p_g"):
        assert 0.0 <= getattr(m, name) <= 1.0


def test_check_passes():
    assert d2.main(["--check"]) == 0
