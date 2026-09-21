"""619 A3 单测：VFDR 状态机（tools/vfdr_619.py）

纯函数验证：状态转移、闭环、历史教训可达 CLOSED、异常抛错、`--check` 自检。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vfdr_619 as V  # noqa: E402

CANONICAL = ("TRIAGE", "START_FIX", "FIX_SHIPPED", "VERIFY_PASS")


def test_all_transition_targets_valid():
    assert all(nxt in V.STATES for d in V.TRANSITIONS.values() for nxt in d.values())


def test_invalid_transition_rejected():
    assert not V.can_transition("OPEN", "FIX_SHIPPED")
    assert not V.can_transition("CLOSED", "TRIAGE")


def test_determinism():
    assert V.transition("OPEN", "TRIAGE") == "TRIAGED"
    assert V.transition("VERIFYING", "VERIFY_FAIL") == "FIXING"
    assert V.transition("CLOSED", "REOPEN") == "FIXING"


def test_simulate_close():
    v = {"state": "OPEN", "history": []}
    final = V.simulate(v, CANONICAL)
    assert final == "CLOSED"
    assert v["history"][-1]["to"] == "CLOSED"


def test_seed_lessons_reach_closed():
    for vuln in V.seed_lessons():
        sim = dict(vuln)
        assert V.simulate(sim, CANONICAL) == "CLOSED"


def test_illegal_event_raises():
    import pytest
    with pytest.raises(ValueError):
        V.transition("OPEN", "FIX_SHIPPED")


def test_render_contains_state_table():
    md = V.render_markdown()
    assert "OPEN" in md and "VERIFY_FAIL" in md


def test_check_runs_clean():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "vfdr_619.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout + r.stderr)
