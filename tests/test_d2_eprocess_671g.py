# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D2：e-process 序贯检验（10 条；含 H0 Ville 一类错误仿真）。"""
from __future__ import annotations

import json

import eprocess_671g as E


def test_first_e_is_one():
    assert E.e_value_sequence([], 0.5) == [1.0]
    assert E.e_value_sequence([1, 0, 1], 0.5)[0] == 1.0


def test_symmetric_mu0_first_step_invariant():
    # mu0=0.5 + 对称网格混合：第一步 0/1 似然比混合后仍为 1（H0 鞅起点）
    s = E.e_value_sequence([1], 0.5)
    assert abs(s[1] - 1.0) < 1e-9


def test_grows_under_sustained_success():
    s = E.e_value_sequence([1] * 6, 0.5)
    assert s[-1] > s[0] and s[-1] > 5.0


def test_shrinks_under_balanced_mixture():
    # 平衡序列（H0=0.5 的典型实现）：复合备择的似然混合随 n 衰减（极端 μ1 衰减更快）
    s = E.e_value_sequence([1, 0] * 20, 0.5)
    assert s[-1] < 1.0


def test_mixture_is_nondecreasing_under_fixed_mu1():
    # 固定单点备择 μ1=0.8：连成功单调增（复合混合在极端序列也能给出方向性）
    fixed = [0.8]
    s = E.e_value_sequence([1] * 5, 0.5, mu1_grid=fixed)
    assert all(b >= a - 1e-12 for a, b in zip(s, s[1:]))


def test_h1_power_eventually_rejects():
    # 真率 0.8 vs H0 0.5，200 个样本大概率在早期越过 20
    import random
    rng = random.Random(7)
    xs = [1 if rng.random() < 0.8 else 0 for _ in range(200)]
    s = E.e_value_sequence(xs, 0.5)
    assert E.stop_at(s, 0.05) is not None
    assert max(s) >= 20


def test_stop_none_under_no_evidence():
    # 恰好 mu0=0.5 的一段对称波动，e 不会爆炸到 20
    assert E.stop_at(E.e_value_sequence([1, 0] * 5, 0.5), 0.05) is None


def test_invalid_mu_raises():
    import pytest
    with pytest.raises(ValueError):
        E.log_lr(1, 0.0, 0.5)
    with pytest.raises(ValueError):
        E.log_lr(2, 0.5, 0.6)


def test_type1_error_controlled_under_h0():
    # Ville：H0 下任意 peek 越阈概率 ≤ α（1000 次，n=100；给 Monte Carlo 噪声余量）
    rep = E.type1_simulation(0.5, n=100, reps=1000, alpha=0.05, seed=42)
    assert rep["bound_ok"] and rep["type1_rate"] <= 0.05 + 0.02


def test_ledger_append_chain(tmp_path):
    p = tmp_path / "e.jsonl"
    e1 = E.append_event(p, 1, 0.5)
    e2 = E.append_event(p, 0, 0.5)
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 2 and rows[0]["seq_index"] == 0 and rows[1]["seq_index"] == 1
    assert abs(e1["e_value_after"] - 1.0) < 1e-9 and e2["e_value_after"] >= 0
    # 累计 e 与重算一致（同一 outcomes 重放）
    s = E.e_value_sequence([1, 0], 0.5)
    assert abs(rows[1]["e_value_after"] - s[-1]) < 1e-9


def test_ledger_is_append_only_api():
    # 模块只暴露 append 写接口（不提供改历史函数）
    assert hasattr(E, "append_event")
    assert not hasattr(E, "rewrite_event")
    assert not hasattr(E, "delete_event")
