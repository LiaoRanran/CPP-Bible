"""622 F2 · 收工门禁 run_622_gate 单测"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import run_622_gate as G  # noqa: E402


def test_six_checks_registered():
    assert len(G.CHECKS) == 6
    assert all(callable(fn) for _l, fn in G.CHECKS)


def test_tool_and_test_lists():
    assert len(G.NEW_TOOLS_622) == 5
    assert len(G.TOOLS_REGRESSION) == 9
    assert len(G.NEW_TESTS_622) == 12
    for n in G.NEW_TOOLS_622:
        assert os.path.exists(os.path.join(ROOT, "tools", f"{n}.py"))
    for n in G.TOOLS_REGRESSION:
        assert os.path.exists(os.path.join(ROOT, "tools", f"{n}.py"))
    for t in G.NEW_TESTS_622:
        assert os.path.exists(os.path.join(ROOT, t))


def test_controlled_dirs_clean():
    ok, msg = G.check_controlled_dirs()
    assert ok, msg


def test_new_tools_pass():
    ok, msg = G.check_new_tools()
    assert ok, msg


def test_regression_pass():
    ok, msg = G.check_regression()
    assert ok, msg


def test_ci_yml_valid_and_race_fix_in_place():
    ok, msg = G.check_ci_yml()
    assert ok, msg
    assert "并发安全检查通过" in msg


def test_ruff_passes():
    ok, msg = G.check_ruff()
    assert ok, msg


def test_pytest_passes():
    ok, msg = G.check_pytest()
    assert ok, msg
    assert "passed" in msg


def test_monitor_gates_explicitly_not_run():
    assert len(G.NOT_RUN) == 4
    assert any("tool_integrity" in x for x in G.NOT_RUN)
    assert any("atom_evidence_replay" in x for x in G.NOT_RUN)


def test_interpreter_exists():
    assert os.path.exists(G.pick_python())


def test_selftest_passes():
    assert G.selftest() == 0
