#!/usr/bin/env python3
"""615 D3 回归测试：learner_transition_detector（跃迁触发条件机器判定）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_transition_detector as d3  # noqa: E402


def test_status_logic() -> None:
    assert d3.status_of(0.9, 0.9) == "triggered"
    assert d3.status_of(0.8, 0.8) == "triggered"
    assert d3.status_of(0.9, 0.5) == "ready"
    assert d3.status_of(0.5, 0.9) == "not_ready"


def test_gate_thresholds() -> None:
    assert d3.gate_status(0) == "closed"
    assert d3.gate_status(1) == "opening"
    assert d3.gate_status(4) == "opening"
    assert d3.gate_status(5) == "open"


def test_real_events_exclude_simulated() -> None:
    # 现有 behaviors 全为 simulated ⇒ 真实事件 0
    assert d3.real_event_count() == 0


def test_check_consistency() -> None:
    assert d3.check() == []
