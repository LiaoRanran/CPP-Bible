#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 F2 · run_618_gate 单测（≥3 例）"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import run_618_gate as g  # noqa: E402


class _Stub:
    def setattr(self, obj, name, val):
        setattr(obj, name, val)


def test_controlled_clean_real_repo():
    # 当前仓库未改受控目录 ⇒ 应返回空
    hits = g.check_controlled_clean()
    assert hits == [], "受控目录不应被改动: %s" % hits


def test_controlled_clean_detects(monkeypatch=None):
    mp = monkeypatch or _Stub()
    fake = b" M atoms/foo.md\n M evidence/bar.md\n?? data/x.md\n"
    mp.setattr(g.subprocess, "check_output", lambda *a, **k: fake)
    hits = g.check_controlled_clean()
    assert "atoms/foo.md" in hits and "evidence/bar.md" in hits
    assert "data/x.md" not in hits


def test_collect_tests_present():
    tests = g.collect_tests()
    assert "tests/test_618_a3.py" in tests
    assert "tests/test_escape_rate_estimand.py" in tests
    assert "tests/test_snapshot_manifest.py" in tests


def test_run_tests_invokes_pytest(monkeypatch=None):
    mp = monkeypatch or _Stub()
    captured = {}

    class _Res:
        returncode = 0

    def fake_run(cmd, cwd=None):
        captured["cmd"] = cmd
        return _Res()

    mp.setattr(g.subprocess, "run", fake_run)
    code = g.run_tests()
    assert captured.get("cmd") is not None
    assert code == 0


if __name__ == "__main__":
    test_controlled_clean_real_repo()
    test_controlled_clean_detects()
    test_collect_tests_present()
    test_run_tests_invokes_pytest()
    print("ALL F2 GATE TESTS PASSED")
