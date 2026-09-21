"""620 E1 · 收工门禁 run_620_gate 单测"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import run_620_gate as G  # noqa: E402


def test_five_checks_registered():
    assert len(G.CHECKS) == 5
    assert all(callable(fn) for _label, fn in G.CHECKS)


def test_controlled_dirs_list():
    assert set(G.CONTROLLED) == {"atoms/", "evidence/", "Examples/", "Book/"}


def test_new_tools_and_tests_lists():
    assert len(G.NEW_TOOLS) == 7
    assert len(G.NEW_TESTS) == 9
    for name in G.NEW_TOOLS:
        assert os.path.exists(os.path.join(ROOT, "tools", f"{name}.py"))
    for t in G.NEW_TESTS:
        assert os.path.exists(os.path.join(ROOT, t))


def test_gate_regex_parses():
    m = G.GATE_RE.search("命中 191 (block=0 warn=186 advice=5)")
    assert m is not None
    assert [int(x) for x in m.groups()] == [191, 0, 186, 5]


def test_check_controlled_dirs_clean():
    ok, msg = G.check_controlled_dirs()
    assert ok, msg
    assert isinstance(msg, str) and msg


def test_check_ruff_passes():
    ok, msg = G.check_ruff()
    assert ok, msg


def test_check_gate_block_zero():
    ok, msg = G.check_gate()
    assert ok, msg
    assert "block=0" in msg


def test_check_pytest_all_green():
    ok, msg = G.check_pytest()
    assert ok, msg
    assert "passed" in msg


def test_each_tool_check_passes():
    for name in G.NEW_TOOLS:
        rc, out = G._run([G.PY, os.path.join("tools", f"{name}.py"), "--check"])
        assert rc == 0, f"{name} --check 失败：{out[-300:]}"


def test_selftest_passes():
    assert G.selftest() == 0
