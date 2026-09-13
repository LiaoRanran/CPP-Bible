"""412 成本追踪回归锁：record/report/cpva/backfill 与 token 估算口径。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import cost_tracker as ct
import gate_engine as ge


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ct, "COST_DIR", tmp_path / "cost")
    return tmp_path


def test_token_estimation():
    """chars=3000 → tokens_est=1000（chars/3 口径）。"""
    assert ct.tokens_est(3000) == 1000
    assert ct.tokens_est(3) == 1


def test_record_and_report(sb: Path):
    ct.record("ATOM-T-001", "fixture", 15000, windows=2, duration_min=30)
    ct.record("ATOM-T-001", "redteam", 30000)
    d = ct.report("ATOM-T-001")
    assert d["stages"]["fixture"]["tokens_est"] == 5000
    assert d["total_chars"] == 45000
    assert d["total_tokens_est"] == 15000
    assert d["total_windows"] == 3 and d["total_duration_min"] == 30
    assert d["cpva"] == 15000


def test_record_accumulates_same_stage(sb: Path):
    ct.record("ATOM-T-002", "gate_fix", 3000)
    ct.record("ATOM-T-002", "gate_fix", 6000, windows=2)
    d = ct.report("ATOM-T-002")
    assert d["stages"]["gate_fix"]["chars"] == 9000
    assert d["stages"]["gate_fix"]["windows"] == 3


def test_cpva_calculation(sb: Path):
    for i, (aid, dom, chars) in enumerate(
            [("ATOM-A", "mem", 9000), ("ATOM-B", "mem", 12000), ("ATOM-C", "conc", 6000)]):
        ct.record(aid, "fixture", chars)
        f = ct.COST_DIR / f"{aid}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        d["domain"] = dom
        f.write_text(json.dumps(d), encoding="utf-8")
    c = ct.cpva()
    assert c["total_verified_atoms"] == 3
    assert c["total_tokens_est"] == 9000
    assert c["cpva_overall"] == 3000
    assert c["cpva_by_domain"]["mem"] == 3500 and c["cpva_by_domain"]["conc"] == 2000
    assert c["cpva_by_stage"]["fixture"] == 3000
    assert c["trend"] in ("improving", "stable", "worsening")


def test_backfill_from_git(sb: Path):
    """对真实原子回填（git log 粗估）——数据非空且落盘。"""
    d = ct.backfill("ATOM-MEM-RAII-001")
    assert d["total_tokens_est"] > 0
    assert d["stages"]["fixture"]["windows"] >= 1
    assert (ct.COST_DIR / "ATOM-MEM-RAII-001.json").is_file()


def test_json_report_format(sb: Path):
    r = ct.report()
    assert r["tool"] == "cost_tracker" and "timestamp" in r
    assert "atoms" in r and "total_tokens_est" in r
