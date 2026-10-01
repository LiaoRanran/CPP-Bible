# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_fast_gate.py — fast_gate 的单元测试（≥10 条断言，全部桩化、不跑真门禁）。

用法（两种都行）：
    python -m pytest tools/test_fast_gate.py -q
    python tools/test_fast_gate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fast_gate as FG  # noqa: E402


# ── 基础契约 ──────────────────────────────────────────────────────────────────

def test_gates_cover_three_deliverable_doors():
    names = " ".join(n for n, _ in FG.GATES)
    assert "658" in names
    assert "669d" in names
    assert "guard" in names or "671a" in names
    assert len(FG.GATES) == 3          # 不许多、不许少（多=变慢，少=漏测）


def test_budget_and_timeouts_are_declared():
    assert FG.BUDGET_S == 300.0        # <5 分钟
    assert FG.DEFAULT_TIMEOUT_TESTS >= FG.DEFAULT_TIMEOUT_GATE > 0


def test_fail_summary_prefers_error_lines():
    item = {"tail": ["普通行", "FAILED tests/a.py::t", "rc=1", "普通行2"]}
    out = FG._fail_summary(item)
    assert "FAILED tests/a.py::t" in out
    assert out.startswith("      ")    # 缩进对齐，便于人读


# ── pytest 子命令构造 ─────────────────────────────────────────────────────────

def test_run_tests_all_fast_uses_repo_wide_not_slow(monkeypatch):
    seen = {}

    def fake_run(name, cmd, timeout):
        seen["cmd"] = cmd
        return {"name": name, "cmd": "", "rc": 0, "seconds": 0.1, "tail": []}

    monkeypatch.setattr(FG, "_run", fake_run)
    FG.run_tests([], all_fast=True)
    assert "tests" in seen["cmd"]
    assert "not slow" in seen["cmd"]
    assert "-m" in seen["cmd"]


def test_run_tests_specified_files_only(monkeypatch):
    seen = {}

    def fake_run(name, cmd, timeout):
        seen["cmd"] = cmd
        return {"name": name, "cmd": "", "rc": 0, "seconds": 0.1, "tail": []}

    monkeypatch.setattr(FG, "_run", fake_run)
    FG.run_tests(["tests/test_a.py", "tests/test_b.py"], all_fast=False)
    assert "tests/test_a.py" in seen["cmd"] and "tests/test_b.py" in seen["cmd"]
    assert "tests" not in [c for c in seen["cmd"] if c == "tests"]   # 不是全量
    assert "not slow" in seen["cmd"]                                 # 也带 slow 过滤


def test_run_tests_no_files_no_all_is_skipped():
    item = FG.run_tests([], all_fast=False)
    assert item.get("skipped") is True and item["rc"] == 0


def test_run_tests_jobs_auto_adds_xdist(monkeypatch):
    seen = {}

    def fake_run(name, cmd, timeout):
        seen["cmd"] = cmd
        return {"name": name, "cmd": "", "rc": 0, "seconds": 0.1, "tail": []}

    monkeypatch.setattr(FG, "_run", fake_run)
    monkeypatch.setattr(FG, "_xdist_available", lambda: True)
    FG.run_tests([], all_fast=True, jobs="auto")
    assert "-n" in seen["cmd"] and "auto" in seen["cmd"]


def test_run_tests_jobs_zero_is_serial(monkeypatch):
    seen = {}
    monkeypatch.setattr(FG, "_run", lambda n, c, t: (
        seen.update(cmd=c) or {"name": n, "cmd": "", "rc": 0, "seconds": 0.1, "tail": []}))
    FG.run_tests([], all_fast=True, jobs="0")
    assert "-n" not in seen["cmd"]                         # 显式串行
    assert "-m" in seen["cmd"] and "not slow" in seen["cmd"]


def test_run_tests_xdist_missing_falls_back_visibly(monkeypatch):
    monkeypatch.setattr(FG, "_run", lambda n, c, t: {
        "name": n, "cmd": "", "rc": 0, "seconds": 0.1, "tail": []})
    monkeypatch.setattr(FG, "_xdist_available", lambda: False)
    item = FG.run_tests([], all_fast=True, jobs="auto")
    assert any("xdist 不可用" in ln for ln in item["tail"])   # 落回串行必须显形


# ── 前端开关 ─────────────────────────────────────────────────────────────────

def test_skip_frontend_flag():
    item = FG.run_frontend(skip=True)
    assert item.get("skipped") is True and item["rc"] == 0
    assert "skip-frontend" in item["name"]


def test_frontend_missing_runner_is_visible_skip(monkeypatch, tmp_path):
    monkeypatch.setattr(FG, "ROOT", tmp_path)          # 空目录 ⇒ 无 web/run_tests.mjs
    item = FG.run_frontend(skip=False)
    assert item.get("skipped") is True
    assert "不静默" in item["tail"][0]                  # 跳过得显形


# ── 失败路径 ─────────────────────────────────────────────────────────────────

def test_run_captures_timeout(monkeypatch):
    cmd = [sys.executable, "-c", "import time; time.sleep(5)"]
    item = FG._run("假装超时", cmd, timeout=0.3)
    assert item["rc"] == -9
    assert "timeout" in item["tail"][0]


def test_main_pass_all_stubbed(monkeypatch, capsys):
    monkeypatch.setattr(FG, "run_gates", lambda t: [
        {"name": "g1", "cmd": "", "rc": 0, "seconds": 0.1, "tail": []}])
    monkeypatch.setattr(FG, "run_tests", lambda files, all_fast, t, jobs="":
                        {"name": "t", "cmd": "", "rc": 0, "seconds": 0.1, "tail": []})
    monkeypatch.setattr(FG, "run_frontend", lambda skip, t, wd=None:
                        {"name": "f", "cmd": "", "rc": 0, "seconds": 0.1,
                         "tail": [], "skipped": True})
    rc = FG.main(["--skip-frontend"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "overall=PASS" in out


def test_main_fail_reports_evidence(monkeypatch, capsys):
    monkeypatch.setattr(FG, "run_gates", lambda t: [
        {"name": "g-bad", "cmd": "x y", "rc": 1, "seconds": 0.1,
         "tail": ["[BLOCK] 三方数字不一致"]}])
    monkeypatch.setattr(FG, "run_tests", lambda files, all_fast, t, jobs="":
                        {"name": "t", "cmd": "", "rc": 0, "seconds": 0.1, "tail": []})
    monkeypatch.setattr(FG, "run_frontend", lambda skip, t, wd=None:
                        {"name": "f", "cmd": "", "rc": 0, "seconds": 0.1,
                         "tail": [], "skipped": True})
    rc = FG.main([])
    out = capsys.readouterr().out
    assert rc == 1
    assert "overall=FAIL" in out
    assert "[BLOCK] 三方数字不一致" in out      # FAIL 必须给证据


def test_main_json_output_is_machine_readable(monkeypatch, capsys):
    import json
    monkeypatch.setattr(FG, "run_gates", lambda t: [
        {"name": "g1", "cmd": "", "rc": 0, "seconds": 0.1, "tail": []}])
    monkeypatch.setattr(FG, "run_tests", lambda files, all_fast, t, jobs="":
                        {"name": "t", "cmd": "", "rc": 0, "seconds": 0.1, "tail": []})
    monkeypatch.setattr(FG, "run_frontend", lambda skip, t, wd=None:
                        {"name": "f", "cmd": "", "rc": 0, "seconds": 0.1,
                         "tail": [], "skipped": True})
    rc = FG.main(["--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0 and payload["ok"] is True
    assert isinstance(payload["items"], list) and payload["total_seconds"] >= 0


def test_web_has_changes_returns_bool_or_none():
    v = FG.web_has_changes()
    assert v is None or isinstance(v, bool)


if __name__ == "__main__":                      # 直接运行 = 自跑自身测试
    raise SystemExit(pytest.main([__file__, "-q"]))
