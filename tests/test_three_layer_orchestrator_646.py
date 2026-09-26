"""646 阶段 A2 · 三层耦合打通单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import three_layer_orchestrator_646 as c2  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert c2.selftest() == 0


def test_coupling_reaches_targets():
    """真实编排：≥5 链证据≠0、归因可复核率 ≥0.5。"""
    res = c2.orchestrate(min_chains=5)
    assert res["chain_count"] >= 5
    assert res["chains_with_evidence"] >= 5
    assert res["attribution_rate"] >= 0.5
    assert res["met"] is True


def test_every_chain_has_rule_and_verdict():
    """每条链都带规则 id 与尾端判决。"""
    res = c2.orchestrate()
    for c in res["chains"]:
        assert c["rule"] and c["verification"]["verdict"] in (
            "pass", "fail", "escape", "needs_human", "false_positive", "unknown")
