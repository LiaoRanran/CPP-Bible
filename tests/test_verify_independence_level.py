#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""617 B1 · verify_independence_level 单测（纯标准库）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import verify_independence_level as m  # noqa: E402


def test_default_level_1():
    r = m.compute_level(dict(m.DEFAULT_FACTS))
    assert r["discrete_level"] == 1
    # verifier=1 ⇒ scalar 封顶 0.2，且 > 0（内部缓解 + checksum 积分）
    assert 0.0 < r["continuity_scalar"] <= 0.2
    assert r["factors"]["verifier_independence"] == 0.0
    assert r["factors"]["checksum"] == 1.0


def test_no_second_impl_level_0():
    f = dict(m.DEFAULT_FACTS)
    f["second_implementation_rules"] = 0
    r = m.compute_level(f)
    assert r["discrete_level"] == 0


def test_level_2_with_external_interface():
    f = dict(m.DEFAULT_FACTS)
    f["external_verifiable_interface"] = True
    r = m.compute_level(f)
    assert r["discrete_level"] == 2
    # verifier 仍为 1 ⇒ scalar 仍封顶 0.2
    assert r["continuity_scalar"] <= 0.2


def test_level_3_with_third_party():
    f = dict(m.DEFAULT_FACTS)
    f["verifier_count"] = 2
    f["external_verifiable_interface"] = True
    f["third_party_review"] = True
    f["trust_root_anchored"] = True
    r = m.compute_level(f)
    assert r["discrete_level"] == 3
    # verifier>1 解除封顶，scalar 应显著高于 0.2
    assert r["continuity_scalar"] > 0.2
    assert r["factors"]["verifier_independence"] == 1.0


def test_second_impl_ratio():
    f = dict(m.DEFAULT_FACTS)
    r = m.compute_level(f)
    assert abs(r["factors"]["second_implementation"] - 1 / 63) < 1e-3


if __name__ == "__main__":
    test_default_level_1()
    test_no_second_impl_level_0()
    test_level_2_with_external_interface()
    test_level_3_with_third_party()
    test_second_impl_ratio()
    print("ALL B1 TESTS PASSED")
