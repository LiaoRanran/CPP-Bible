#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""617 A1 · escape_rate_estimand 单测（纯标准库）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import escape_rate_estimand as m  # noqa: E402


def test_l1_blocked():
    l1 = m.layer_l1("blocked")
    assert l1["k"] == 1 and l1["n"] == 1406
    assert abs(l1["rate"] - 1 / 1406) < 1e-12
    assert l1["validity"] == "valid_descriptive"


def test_l1_escaped_and_equivalent():
    assert m.layer_l1("escaped")["rate"] == 0.0
    eq = m.layer_l1("equivalent")
    assert eq["k"] == 8 and eq["n"] == 1593


def test_l2_blocked_cs():
    l2 = m.layer_l2("blocked")
    assert l2["anytime_cs_upper_95"] == 0.009062
    assert l2["fixed_endpoint_cp_upper_95"] == 0.003370
    assert 0.0 < l2["fixed_endpoint_wilson_upper_95_approx"] < 1.0


def test_l2_escaped_invalid_fixed():
    l2 = m.layer_l2("escaped")
    # 顺序场景下固定终点无效，标 None
    assert l2["fixed_endpoint_cp_upper_95"] is None
    assert l2["anytime_cs_upper_95"] is None


def test_l3_shrinkage():
    # independence=1 时 L3 退化为 L1；independence=0 时收缩到先验 0.05
    full = m.layer_l3("blocked", 1.0)
    zero = m.layer_l3("blocked", 0.0)
    l1 = m.layer_l1("blocked")["rate"]
    assert abs(full["deployment_extrapolation_rate"] - l1) < 1e-12
    assert abs(zero["deployment_extrapolation_rate"] - 0.05) < 1e-12
    mid = m.layer_l3("blocked", 0.5)
    assert l1 < mid["deployment_extrapolation_rate"] < 0.05


def test_enumerate_keys():
    out = m.enumerate_layers("blocked", 0.8)
    assert set(out.keys()) == {"escape_type", "L1_descriptive", "L2_inferential", "L3_causal_extrapolation"}


def test_invalid_escape_type():
    try:
        m.layer_l1("bogus")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_invalid_independence_level():
    try:
        m.layer_l3("blocked", 1.5)
        assert False, "expected ValueError"
    except ValueError:
        pass


if __name__ == "__main__":
    test_l1_blocked()
    test_l1_escaped_and_equivalent()
    test_l2_blocked_cs()
    test_l2_escaped_invalid_fixed()
    test_l3_shrinkage()
    test_enumerate_keys()
    test_invalid_escape_type()
    test_invalid_independence_level()
    print("ALL A1 TESTS PASSED")
