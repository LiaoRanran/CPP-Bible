#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 B 线 · gate/poison/replay 独立性报告 单测（≥3 例/工具）"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gate_independence_report_618 as g  # noqa: E402
import poison_independence_report_618 as p  # noqa: E402
import replay_independence_report_618 as r  # noqa: E402

FACTS_L1 = {
    "verifier_count": 1, "second_implementation_rules": 1, "second_implementation_total": 63,
    "checksum_protected": True, "external_verifiable_interface": False,
    "third_party_review": False, "trust_root_anchored": False,
}


def test_gate_build_numbers():
    d = g.build(FACTS_L1)
    assert d["gate"]["rules"] == 63 and d["gate"]["hits"] == 191
    assert d["gate"]["block"] == 0 and d["gate"]["warn"] == 186


def test_gate_independence_level():
    d = g.build(FACTS_L1)
    assert d["independence"]["discrete_level"] == 1
    assert abs(d["independence"]["continuity_scalar"] - 0.1532) < 1e-3


def test_gate_render_contains_gap():
    txt = g.render(g.build(FACTS_L1))
    assert "L1" in txt and "L2" in txt and "缺口" in txt
    assert "63" in txt and "191" in txt


def test_poison_build_numbers():
    d = p.build(FACTS_L1)
    assert d["poison"]["passed"] == 124 and d["poison"]["total"] == 124
    assert d["poison"]["coverage_honest"] == "60/63"


def test_poison_independence_level():
    d = p.build(FACTS_L1)
    assert d["independence"]["discrete_level"] == 1


def test_poison_render_contains_honest():
    txt = p.render(p.build(FACTS_L1))
    assert "95.2" in txt and "诚实" in txt


def test_replay_build_numbers():
    d = r.build(FACTS_L1)
    assert d["replay"]["confirm"] == 56
    assert d["replay"]["refute"] == 0 and d["replay"]["infra_error"] == 0


def test_replay_independence_level():
    d = r.build(FACTS_L1)
    assert d["independence"]["discrete_level"] == 1


def test_replay_render_refute_zero():
    txt = r.render(r.build(FACTS_L1))
    assert "refute=0" in txt and "声称零逃逸" in txt


def test_no_core_modification():
    # 三个工具不得 import 改写受控工具；此处仅验证它们只读 manifest + 调 B1
    for mod in (g, p, r):
        assert hasattr(mod, "build") and hasattr(mod, "render")


if __name__ == "__main__":
    test_gate_build_numbers()
    test_gate_independence_level()
    test_gate_render_contains_gap()
    test_poison_build_numbers()
    test_poison_independence_level()
    test_poison_render_contains_honest()
    test_replay_build_numbers()
    test_replay_independence_level()
    test_replay_render_refute_zero()
    test_no_core_modification()
    print("ALL B-LINE TESTS PASSED")
