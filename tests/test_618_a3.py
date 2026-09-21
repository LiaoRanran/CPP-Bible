#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 A3 · escape_rate_l2b_618 单测（纯标准库；确定性，固定公式）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import escape_rate_l2b_618 as m  # noqa: E402


def test_eprocess_escaped_n1593():
    # 声称零逃逸 k=0, n=1593：L2b 应为正、保守，约 0.65%
    u = m.eprocess_upper_bound(0, 1593)
    assert 0.0 < u < 0.05
    assert abs(u - 0.0065) < 1e-2


def test_eprocess_equivalent_n1593():
    # equivalent k=8, n=1593：L2b 应 > L1(≈0.5%) 且 < 0.1，落在增支
    l1 = 8 / 1593
    u = m.eprocess_upper_bound(8, 1593)
    assert u > l1
    assert u < 0.1


def test_eprocess_self_consistency():
    # 解出的 θ 应满足 M(θ)≈1/α（自洽）
    k, n = 0, 1593
    u = m.eprocess_upper_bound(k, n)
    coef = m._beta(k + 1, n - k + 1)
    M = coef / ((u ** k) * ((1.0 - u) ** (n - k)))
    assert abs(M - 1 / 0.05) < 1e-2


def test_eprocess_monotone_n():
    # 固定 k=0：n 越大上界越小
    u_small = m.eprocess_upper_bound(0, 100)
    u_big = m.eprocess_upper_bound(0, 1593)
    assert u_small > u_big > 0.0


def test_layer_l3_escaped():
    # escaped L1=0, scalar=0.153, prior=0.05 → L3 = 0.847*0.05 = 0.04235
    assert abs(m.layer_l3(0.0) - 0.04235) < 1e-5


def test_layer_l3_equivalent():
    # equivalent L1=8/1593≈0.0050207 → L3≈0.043122
    l1 = 8 / 1593
    assert abs(m.layer_l3(l1) - 0.043122) < 1e-4


def test_compute_keys():
    r = m.compute()
    assert set(r.keys()) >= {"escaped", "equivalent", "n_variants"}
    assert r["n_variants"] == 1593
    assert r["escaped"]["k"] == 0
    assert r["equivalent"]["k"] == 8
    # L2b 均为正（禁填 0）
    assert r["escaped"]["L2b_eprocess_anytime_upper_95"] > 0
    assert r["equivalent"]["L2b_eprocess_anytime_upper_95"] > 0


if __name__ == "__main__":
    test_eprocess_escaped_n1593()
    test_eprocess_equivalent_n1593()
    test_eprocess_self_consistency()
    test_eprocess_monotone_n()
    test_layer_l3_escaped()
    test_layer_l3_equivalent()
    test_compute_keys()
    print("ALL A3 TESTS PASSED")
