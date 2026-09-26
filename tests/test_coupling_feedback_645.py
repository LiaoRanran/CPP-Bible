"""645 C4 耦合反馈单测（fast 组：真实反馈分类）。"""
import sys

import pytest

sys.path.insert(0, "tools")

import three_layer_orchestrator_645 as c4  # 647 D1：C4 已并入三层耦合套件


def test_selftest_passes():
    assert c4.feedback_selftest() == 0


def test_feedback_classifies_correctly():
    chains = [
        {"issue": "I1", "verification": {"verdict": "pass"}, "evidence_count": 1},
        {"issue": "I2", "verification": {"verdict": "needs_human"}, "evidence_count": 0},
        {"issue": "I3", "verification": {"verdict": "fail"}, "evidence_count": 0},
        {"issue": "I4", "verification": {"verdict": "fail"}, "evidence_count": 2},
    ]
    fb = c4.generate_feedback(chains)
    assert fb["verified_ok"] == ["I1"]
    assert "I2" in fb["needs_human"]
    assert "I3" in fb["needs_evidence"]
    assert "I4" in fb["needs_human"]
    # 密度计算正确
    assert fb["vulnerability_density"] == pytest.approx(0.75)


def test_feedback_priority_scales():
    many = [{"issue": f"I{i}", "verification": {"verdict": "fail", "evidence_count": 0}}
            for i in range(10)]
    fb = c4.generate_feedback(many)
    assert fb["head_layer_priority"] == "high"
