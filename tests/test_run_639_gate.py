"""639 E1 单测：门禁工具（轻量，不触发全量 pytest）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import run_639_gate as G  # noqa: E402


def test_debts_table_complete():
    """12 债全部登记，状态合法。"""
    assert len(G.DEBTS) == 12
    assert {d[0] for d in G.DEBTS} == {f"D{i}" for i in range(1, 13)}
    for d in G.DEBTS:
        assert d[3] in ("已修", "登记留 640", "交人")


def test_controlled_dirs_match_spec():
    assert set(G.CONTROLLED) == {"atoms", "evidence", "Examples", "Book"}


def test_round_report_check_runs():
    r = G.check_round_reports()
    assert isinstance(r["ok"], bool)
    assert "existing" in r


def test_static_checks_green():
    """受控目录 / ruff / merkle / tool_integrity（不跑 pytest/mypy 全量）。"""
    assert G.check_controlled()["ok"]
    assert G.check_ruff()["ok"]
    assert G.check_merkle()["ok"]
    assert G.check_tool_integrity()["ok"]


def test_gate_logic_reflects_step_results(monkeypatch):
    """640c B1：锁**门禁机制**而非"当时仓库状态"（历史门禁的跨批脆弱反面教材）。

    任何一步失败 ⇒ `all_ok` 必须为 False 且 `main()` exit 1；全部成功 ⇒ True。
    不依赖仓库当前内容 ⇒ 正常演进（加工具/重算/人签）不会让它变红。
    """
    monkeypatch.setattr(G, "_run", lambda _cmd: (1, "boom"))
    assert G.build()["checks"]["all_ok"] is False
    assert G.main(["--check"]) == 1

    monkeypatch.setattr(G, "_run", lambda _cmd: (0, "ok"))
    checks = G.build()["checks"]
    assert checks["ruff"]["ok"] is True and checks["controlled"]["ok"] is True
    assert checks["merkle"]["ok"] is True and checks["tool_integrity"]["ok"] is True


def test_ledger_check_green():
    assert G.check_ledger()["ok"]
