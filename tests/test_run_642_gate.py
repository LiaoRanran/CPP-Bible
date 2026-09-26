"""642 D1 · 收工门禁回归测试（沿用 640c/641 经验：机制测试与重型真实检查分离）。

重型子项（ruff / mypy / 641 收尾 / tool_integrity）留给 `run_642_gate` 收工时跑一次；
测试只覆盖**机制**与**快而稳定**的真实子项。
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import run_642_gate as G  # noqa: E402


def test_eight_checks_registered():
    r = G.build()
    assert len(r["checks"]) == 8
    assert "all_ok" in r
    assert all("ok" in v and "detail" in v for v in r["checks"].values())


def test_gate_reflects_failing_subprocess(monkeypatch):
    """机制：子进程挂了 ⇒ 该项 ok=False（否则门禁恒绿 == 没有门禁）。"""
    monkeypatch.setattr(G, "_run", lambda *a, **k: (1, "boom"))
    assert G.check_new_tools()["ok"] is False
    assert G.check_ruff()["ok"] is False
    assert G.check_controlled()["ok"] is False
    assert G.check_integrity()["ok"] is False


def test_gate_reflects_ok_subprocess(monkeypatch):
    monkeypatch.setattr(G, "_run", lambda *a, **k: (0, "ok"))
    assert G.check_new_tools()["ok"] is True
    assert G.check_ruff()["ok"] is True
    assert G.check_mypy()["ok"] is True
    assert G.check_integrity()["ok"] is True


def test_controlled_clean_check():
    assert G.check_controlled()["ok"] is True


def test_kernel_purity_check():
    assert G.check_kernel_purity()["ok"] is True


def test_protector_rollout_check():
    """真实子项：五保护器灰度联调必须零漂移、零改判、可回滚到底。"""
    r = G.check_protector_rollout()
    assert r["ok"] is True, r["detail"]


def test_641_closure_check_is_reported():
    """641 收尾项的**结构**正确（真实结果由收工时跑一次判定，避免跨批脆弱）。"""
    r = G.check_641_closure()
    assert set(r) == {"ok", "detail"}
    assert isinstance(r["detail"], str) and r["detail"]


def test_new_tools_have_check_flag():
    for name in list(G.NEW_TOOLS) + ["run_642_gate"]:
        src = open(os.path.join(ROOT, "tools", name + ".py"), encoding="utf-8").read()
        assert "--check" in src, f"{name} 缺 --check"


def test_cli_smoke(monkeypatch):
    """只跑快的子项 + stub 重型项，验证 CLI 汇总逻辑本身。"""
    for heavy in ("check_ruff", "check_mypy", "check_new_tools", "check_integrity",
                  "check_641_closure"):
        monkeypatch.setattr(G, heavy, lambda: {"ok": True, "detail": "stub"})
    assert G.main(["--check"]) == 0
