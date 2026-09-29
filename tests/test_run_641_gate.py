# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""641 E1 · 收工门禁回归测试。

遵循 640c B1 的经验：历史门禁容易退化成"断言当时仓库全绿"的跨批脆弱测试。
因此这里**两类**断言分开：

1. **机制测试**（与仓库当前状态无关）：每项检查返回 `{ok, detail}` 结构；
   `check_new_tools` 在"工具挂了"时必须 ok=False（用 monkeypatch 注入）；
2. **真实仓库**：只跑**快且稳定**的子项（内核纯净 / 受控零污染 / 闭包 / 通用性），
   重型子项（ruff / mypy / 全量 C++ 对账）留给 `run_641_gate` 在收工时跑一次。
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import run_641_gate as G  # noqa: E402


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


def test_gate_reflects_ok_subprocess(monkeypatch):
    monkeypatch.setattr(G, "_run", lambda *a, **k: (0, "ok"))
    assert G.check_new_tools()["ok"] is True
    assert G.check_ruff()["ok"] is True
    assert G.check_mypy()["ok"] is True


def test_kernel_purity_check():
    assert G.check_kernel_purity()["ok"] is True


def test_controlled_clean_check():
    assert G.check_controlled()["ok"] is True


def test_closure_check():
    r = G.check_closure()
    assert r["ok"] is True, r["detail"]


def test_generality_check():
    r = G.check_generality()
    assert r["ok"] is True, r["detail"]


def test_new_tools_have_check_flag():
    """666 A1：660 B6 拆仓后本仓 `queyi_core_*.py` 是**薄 wrapper**（只做 importlib 转发），
    它当然没有 `--check` —— 原来的字面检查会假红。改为：wrapper 追到 canonical 再判
    （非 wrapper 行为逐字不变）。"""
    for name in G.NEW_TOOLS:
        p = os.path.join(ROOT, "tools", name + ".py")
        src = open(p, encoding="utf-8").read()
        if "薄 wrapper" in src[:400]:
            d = os.path.join(ROOT, "tools")
            for _ in range(8):
                cand = os.path.join(d, "queyi-verifier", "tools", name + ".py")
                if os.path.isfile(cand):
                    src = open(cand, encoding="utf-8").read()
                    break
                d = os.path.dirname(d)
        assert "--check" in src, f"{name} 缺 --check"


def test_cli_smoke(monkeypatch):
    """只跑快的子项，验证 CLI 汇总逻辑本身（不跑 ruff/mypy/全量对账）。"""
    monkeypatch.setattr(G, "check_ruff", lambda: {"ok": True, "detail": "stub"})
    monkeypatch.setattr(G, "check_mypy", lambda: {"ok": True, "detail": "stub"})
    monkeypatch.setattr(G, "check_cpp_reconcile", lambda: {"ok": True, "detail": "stub"})
    assert G.main(["--check"]) == 0
