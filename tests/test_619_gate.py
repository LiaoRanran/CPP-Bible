"""619 D1 单测：收工门禁（tools/run_619_gate.py）

遵循 618 教训：pytest **不注入带默认值参数**；stub 必须用 `pytest.MonkeyPatch.context()` 保证恢复，
并加回归断言 `test_stubs_are_restored`（防止 subprocess.run 泄漏把其它测试搞坏）。

不跑监工门禁（gate/poison/replay/tool_integrity 的 --check）——与 619 §六 一致，本测试只验证门禁自身逻辑。
"""
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import run_619_gate as G  # noqa: E402


def test_check_tools_all_exist():
    assert all(os.path.exists(os.path.join(ROOT, "tools", t)) for t in G.CHECK_TOOLS)


def test_gate_tests_all_exist():
    assert all(os.path.exists(os.path.join(ROOT, t)) for t in G.GATE_TESTS)


def test_controlled_clean_on_clean_tree():
    ok, dirty = G.check_controlled_clean()
    assert ok, dirty  # 当前工作区受控目录须零污染


def test_run_tool_checks_ok(monkeypatch):
    class _R:  # 替身：所有工具 --check 立即成功
        returncode = 0
        stdout = ""
        stderr = ""

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(subprocess, "run", lambda *a, **k: _R())
        ok, res = G.run_tool_checks()
        assert ok
        assert all(v == 0 for v in res.values())


def test_run_tool_checks_detects_failure(monkeypatch):
    class _Fail:
        returncode = 1
        stdout = ""
        stderr = "boom"

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(subprocess, "run", lambda *a, **k: _Fail())
        ok, res = G.run_tool_checks()
        assert not ok


def test_stubs_are_restored():
    # 回归：context 退出后 subprocess.run 必须是真实函数（防止泄漏到其它测试）
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(subprocess, "run", lambda *a, **k: None)
    real = subprocess.run([sys.executable, "--version"], capture_output=True)
    assert real.returncode == 0


def test_selftest_passes():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "run_619_gate.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout + r.stderr)
