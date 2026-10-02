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
    monkeypatch.setattr(FG, "run_tests", lambda files, all_fast, t, jobs="", maxfail=0:
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
    monkeypatch.setattr(FG, "run_tests", lambda files, all_fast, t, jobs="", maxfail=0:
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
    monkeypatch.setattr(FG, "run_tests", lambda files, all_fast, t, jobs="", maxfail=0:
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


# ── 673b C1：三路并发（门禁 / pytest / 前端）与摘要顺序 ──────────────────────────

def _stub_three_phases(monkeypatch, log, gate_rc=0, test_rc=0, front_rc=0, sleep=0.20):
    import time as _t

    def fake_gates(timeout):
        log.append("gates:start")
        _t.sleep(sleep)
        log.append("gates:end")
        return [{"name": FG.GATES[0][0], "cmd": "c1", "rc": gate_rc,
                 "seconds": 0.1, "tail": ["FAILED x"] if gate_rc else []}]

    def fake_tests(files, all_fast, timeout, jobs="", maxfail=0):
        log.append("tests:start")
        _t.sleep(sleep)
        log.append("tests:end")
        return {"name": "pytest（全部非 slow）（xdist）", "cmd": "c2", "rc": test_rc,
                "seconds": 0.1, "tail": []}

    def fake_frontend(skip, timeout, wd=None):
        log.append("front:start")
        _t.sleep(sleep)
        log.append("front:end")
        return {"name": "前端自测 node web/run_tests.mjs", "cmd": "c3", "rc": front_rc,
                "seconds": 0.1, "tail": [], "skipped": False}

    monkeypatch.setattr(FG, "run_gates", fake_gates)
    monkeypatch.setattr(FG, "run_tests", fake_tests)
    monkeypatch.setattr(FG, "run_frontend", fake_frontend)


def test_phases_overlap_when_not_serial(monkeypatch, capsys):
    """默认并发：三段各睡 0.20s ⇒ 总墙钟应显著小于串行 0.60s。"""
    import time as _t
    log: list[str] = []
    _stub_three_phases(monkeypatch, log)
    t0 = _t.monotonic()
    rc = FG.main(["--json"])
    wall = _t.monotonic() - t0
    assert rc == 0
    assert wall < 0.50, f"三路没有并发（墙钟 {wall:.2f}s ≥ 0.50s）"
    # 三个 start 必须都出现在第一个 end 之前（否则就是串行）
    first_end = min(i for i, k in enumerate(log) if k.endswith(":end"))
    starts_before = sum(1 for k in log[:first_end] if k.endswith(":start"))
    assert starts_before >= 2, f"并发证据不足：{log}"


def test_serial_phases_preserve_order(monkeypatch, capsys):
    """--serial-phases：回到老顺序（门禁 → pytest → 前端），用于排查争用。"""
    log: list[str] = []
    _stub_three_phases(monkeypatch, log)
    rc = FG.main(["--json", "--serial-phases"])
    assert rc == 0
    assert log == ["gates:start", "gates:end", "tests:start", "tests:end",
                   "front:start", "front:end"], log


def test_summary_item_order_is_stable(monkeypatch, capsys):
    """并发下完成顺序不定，但 --json 的 items 顺序必须稳定（门禁 → pytest → 前端）。"""
    import json as _json
    log: list[str] = []
    _stub_three_phases(monkeypatch, log)
    FG.main(["--json"])
    payload = _json.loads(capsys.readouterr().out)
    names = [i["name"] for i in payload["items"]]
    assert names[0] == FG.GATES[0][0]
    assert "pytest" in names[1]
    assert "前端" in names[2]


def test_concurrent_failure_still_reports_evidence(monkeypatch, capsys):
    """并发不改变判定：任一路红 ⇒ overall=FAIL 且打印证据。"""
    log: list[str] = []
    _stub_three_phases(monkeypatch, log, test_rc=1)
    rc = FG.main([])
    out = capsys.readouterr().out
    assert rc == 1 and "overall=FAIL" in out and "FAILED x" in out or "pytest" in out


# ── 673b C4：--maxfail 透传（本地默认 0=不限，CI 用 1）──────────────────────────

def _capture_cmd(monkeypatch) -> dict:
    seen: dict = {}

    def fake_run(name, cmd, timeout):
        seen["cmd"] = cmd
        seen["name"] = name
        return {"name": name, "cmd": "", "rc": 0, "seconds": 0.1, "tail": []}

    monkeypatch.setattr(FG, "_run", fake_run)
    return seen


def test_maxfail_forwarded_when_positive(monkeypatch):
    seen = _capture_cmd(monkeypatch)
    FG.run_tests([], True, jobs="0", maxfail=1)
    assert "--maxfail=1" in seen["cmd"]
    assert "maxfail=" in seen["name"]          # 名字里显形，便于事后审计


def test_maxfail_zero_means_unlimited(monkeypatch):
    seen = _capture_cmd(monkeypatch)
    FG.run_tests([], True, jobs="0", maxfail=0)
    assert not any(c.startswith("--maxfail") for c in seen["cmd"])


def test_worksteal_is_default_for_parallel(monkeypatch):
    """C4 口径锁定：并行时必须带 --dist worksteal（672h 实测 343s → 270s）。"""
    seen = _capture_cmd(monkeypatch)
    monkeypatch.setattr(FG, "_xdist_available", lambda: True)
    FG.run_tests([], True, jobs="auto")
    assert "-n" in seen["cmd"] and "auto" in seen["cmd"]
    assert "--dist" in seen["cmd"] and "worksteal" in seen["cmd"]


if __name__ == "__main__":                      # 直接运行 = 自跑自身测试
    raise SystemExit(pytest.main([__file__, "-q"]))
