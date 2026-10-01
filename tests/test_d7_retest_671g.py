# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D7：单人隔周重标 κ（5 条）。"""
from __future__ import annotations

import pytest

import retest_reliability_671g as R


def test_perfect_agreement():
    r1 = ["a", "b", "a", "c", "b"] * 2
    r2 = list(r1)
    rep = R.evaluate(r1, r2, gap_days=10, min_samples=10)
    assert rep["kappa"] == 1.0 and rep["status"] == "pass"


def test_chance_level_blocks():
    # 完全不一致 ⇒ κ≈0（两轮完全对立）
    r1 = ["a"] * 10
    r2 = ["b"] * 10
    rep = R.evaluate(r1, r2, gap_days=10, min_samples=10)
    assert rep["kappa"] <= 0.6 and rep["status"] == "block"


def test_moderate_warns():
    # 70% 一致，边际均匀 ⇒ κ≈0.4 ⇒ block；构造 ~0.7 一致性的非均匀标签 ⇒ warn 区间
    r1 = ["a", "a", "a", "a", "a", "a", "a", "b", "b", "b"]
    r2 = ["a", "a", "a", "a", "a", "a", "b", "b", "b", "b"]
    rep = R.evaluate(r1, r2, gap_days=10, min_samples=10)
    assert rep["status"] in ("warn", "block")
    assert rep["disagreements"][0]["id"] == 6


def test_small_sample_inconclusive():
    rep = R.evaluate(["a", "b"], ["a", "b"], gap_days=10, min_samples=10)
    assert rep["status"] == "inconclusive"


def test_gap_required_and_length_mismatch():
    rep = R.evaluate(["a"] * 10, ["a"] * 10, gap_days=3, min_samples=10)
    assert rep["status"] == "rejected" and "7" in rep["why"]
    with pytest.raises(ValueError):
        R.cohen_kappa(["a"], ["a", "b"])
    rep2 = R.evaluate(["a"], ["a"], gap_days=10, min_samples=10)
    assert rep2["status"] == "inconclusive"


def test_kappa_known_value():
    # 经典教科书例：10 个样本，80% 一致，边际各 50% ⇒ po=.8 pe=.5 κ=.6
    r1 = ["a"] * 5 + ["b"] * 5
    r2 = ["a"] * 4 + ["b"] * 1 + ["a"] * 1 + ["b"] * 4
    assert abs(R.cohen_kappa(r1, r2) - 0.6) < 1e-9
