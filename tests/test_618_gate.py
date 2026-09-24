#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 F2 · run_618_gate 单测（≥3 例）

测试卫生：打桩一律走 `pytest.MonkeyPatch.context()`（**必自恢复**）。
**不要**用 `monkeypatch=None` 形式的参数——带默认值的参数不会被 pytest 注入，
会静默退化为不恢复的 `_Stub`，把 `subprocess.check_output` 桩泄漏给后续测试
（实测：泄漏导致 `test_snapshot_manifest.py` 报 `ValueError: invalid literal for int()`）。
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import run_618_gate as g  # noqa: E402
import soft_baseline_634 as SB  # 634 A3  # noqa: E402


def test_controlled_clean_real_repo():
    # 当前仓库未改受控目录 ⇒ 应返回空
    hits = g.check_controlled_clean()
    assert hits == [], "受控目录不应被改动: %s" % hits


def test_controlled_clean_detects():
    fake = b" M atoms/foo.md\n M evidence/bar.md\n?? data/x.md\n"
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(g.subprocess, "check_output", lambda *a, **k: fake)
        hits = g.check_controlled_clean()
    assert "atoms/foo.md" in hits and "evidence/bar.md" in hits
    assert "data/x.md" not in hits


def test_collect_tests_present():
    tests = g.collect_tests()
    assert "tests/test_618_a3.py" in tests
    assert "tests/test_escape_rate_estimand.py" in tests
    assert "tests/test_snapshot_manifest.py" in tests
    assert "tests/test_618_gate.py" in tests


def test_run_tests_invokes_pytest():
    captured = {}

    class _Res:
        returncode = 0

    def fake_run(cmd, cwd=None, **kwargs):
        captured["cmd"] = cmd
        return _Res()

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(g.subprocess, "run", fake_run)
        code = g.run_tests()
    assert captured.get("cmd") is not None
    assert code == 0


def test_check_tools_all_exist():
    for name in g.CHECK_TOOLS:
        assert os.path.exists(os.path.join(ROOT, "tools", name + ".py")), name
    # 634 A3：单调指标（检查工具只增），读单一基线
    assert len(g.CHECK_TOOLS) >= SB.soft("check_tools_min", len(g.CHECK_TOOLS))


def test_run_tool_checks_ok():
    seen = []

    class _Res:
        returncode = 0

    def fake_run(cmd, cwd=None, **kwargs):
        seen.append(cmd)
        return _Res()

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(g.subprocess, "run", fake_run)
        rc = g.run_tool_checks()
    assert rc == 0
    assert len(seen) == len(g.CHECK_TOOLS)
    assert all(c[-1] == "--check" for c in seen)


def test_run_tool_checks_detects_failure():
    class _Res:
        returncode = 1

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(g.subprocess, "run", lambda cmd, cwd=None, **k: _Res())
        rc = g.run_tool_checks()
    assert rc == 1


def test_stubs_are_restored():
    """回归：打桩后 subprocess.run / check_output 必须复原（防跨文件污染）。"""
    import subprocess
    run0, co0 = subprocess.run, subprocess.check_output
    test_run_tool_checks_ok()
    test_run_tool_checks_detects_failure()
    test_controlled_clean_detects()
    assert subprocess.run is run0 and subprocess.check_output is co0


if __name__ == "__main__":
    test_controlled_clean_real_repo()
    test_controlled_clean_detects()
    test_collect_tests_present()
    test_run_tests_invokes_pytest()
    test_check_tools_all_exist()
    test_run_tool_checks_ok()
    test_run_tool_checks_detects_failure()
    test_stubs_are_restored()
    print("ALL F2 GATE TESTS PASSED")
