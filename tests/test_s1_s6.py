"""S4/S5/S6 机器判定回归（S1/S2/S3 规则由 test_gate_engine.py 覆盖）。

覆盖（红绿成对，正例触发 + 反例不触发）：
  S4 黄金锁：无漂移放行 · block 上升红 · verified 下降红 · --accept 留痕后放行
  S5 债务台账：到期红 · 超 90 天红 · Agent 自批红 · 负债率超限红 · 干净台账绿
  S6 毒样例演练：3 毒样例全拦截 + 阴性放行（真编译）
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import debt_ledger as dl
import golden_lock as gl
import poison_drill as pd

METRICS = {"block_findings": 0, "warn_findings": 1, "atoms_total": 0,
           "evidence_total": 1, "verified_atoms": 0, "replay_confirm": 1}


# ── S4 黄金锁 ──────────────────────────────────────────────────────────────
def _gold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, measure: dict) -> None:
    monkeypatch.setattr(gl, "STATE", tmp_path / "golden_state.json")
    monkeypatch.setattr(gl, "measure", lambda: dict(measure))
    assert gl.cmd_sync() == 0


def test_golden_no_drift_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _gold(tmp_path, monkeypatch, METRICS)
    assert gl.cmd_check(None) == 0


def test_golden_block_increase_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _gold(tmp_path, monkeypatch, METRICS)
    monkeypatch.setattr(gl, "measure", lambda: dict(METRICS, block_findings=2))
    assert gl.cmd_check(None) == 1, "block 0→2 必须红"


def test_golden_verified_drop_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    base = dict(METRICS, verified_atoms=1)
    _gold(tmp_path, monkeypatch, base)
    monkeypatch.setattr(gl, "measure", lambda: dict(METRICS))     # verified 1→0
    assert gl.cmd_check(None) == 1, "verified 数下降必须红"


def test_golden_accept_leaves_audit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _gold(tmp_path, monkeypatch, METRICS)
    monkeypatch.setattr(gl, "measure", lambda: dict(METRICS, warn_findings=3))
    rc = gl.cmd_check("口径变更：新增 2 条 warn 级规则")
    state = json.loads(gl.STATE.read_text(encoding="utf-8"))
    assert rc == 0 and len(state["accepted"]) == 1
    assert "口径变更" in state["accepted"][0]["reason"]


# ── S5 债务台账 ────────────────────────────────────────────────────────────
def _debt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tickets: list[dict]) -> None:
    p = tmp_path / "debt_ledger.json"
    p.write_text(json.dumps({"schema": dl.SCHEMA, "tickets": tickets}, ensure_ascii=False),
                 encoding="utf-8")
    monkeypatch.setattr(dl, "LEDGER", p)


def _tk(**over: str) -> dict:
    t = {"id": "DEBT-001", "cause": "c", "risk": "r", "compensation": "cp",
         "owner": "human:liaoranran", "opened": "2026-09-10", "due": "2026-09-20"}
    t.update(over)
    return t


def test_clean_ledger_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk()])
    assert dl.cmd_check() == 0


def test_expired_ticket_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk(due="2026-08-01")])
    assert dl.cmd_check() == 1, "到期未清必须停线"


def test_over_90_days_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk(opened="2026-01-01", due="2026-06-01")])
    assert dl.cmd_check() == 1, "超 90 天 = 永久豁免，必须停线"


def test_agent_owner_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk(owner="agent:claude")])
    assert dl.cmd_check() == 1, "Agent 自批豁免必须停线"


def test_ratio_over_limit_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    many = [_tk(id=f"DEBT-{i:03d}") for i in range(1, 6)]       # 5/20 = 25% > 15%
    _debt(tmp_path, monkeypatch, many)
    assert dl.cmd_check() == 1, "负债率超限必须停线"


def test_add_rejects_agent_owner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(dl, "LEDGER", tmp_path / "debt_ledger.json")
    argv = ["add", "--cause", "c", "--risk", "r", "--compensation", "cp",
            "--owner", "agent:x", "--days", "30"]
    assert dl.main(argv) == 2, "Agent 不得自批（S1 同源）"


# ── S6 毒样例演练（真编译，含阴性对照）────────────────────────────────────
@pytest.mark.skipif(not (Path("C:/Qt/Tools/mingw1530_64/bin/g++.exe").exists()
                         or __import__("shutil").which("g++")),
                    reason="本机无 g++")
def test_poison_drill_all_caught_and_negative_passes():
    assert pd.drill() == 0, "毒样例必须全部拦截且阴性对照放行（G3 验收门自证）"
