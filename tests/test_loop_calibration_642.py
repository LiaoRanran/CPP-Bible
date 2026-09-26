"""642 C2 · loop_calibration_642 单测（校准度计算 / 趋势 / 门槛 / 台账 append-only）。
编号 C2-1..C2-7。
"""
from __future__ import annotations

import json

import loop_calibration_642 as L


# C2-1：R1 校准度 = 3/8 = 37.5%（来自 637 审计）
def test_r1_calibration():
    assert L.calibration(L.round_637()) == 0.375


# C2-2：R2 校准度 = 2/4 = 50.0%（来自 638 调参派生）
def test_r2_calibration():
    r = L.round_638()
    assert r["derived"] is True
    assert L.calibration(r) == 0.5


# C2-3：R3 校准度为 None（未代决，不假精确）；采纳数 0（不代签）
def test_r3_is_none_not_zero():
    r = L.round_642()
    assert L.calibration(r) is None
    assert r["adopted"] == 0 and r["decided"] == 0
    assert sum(r["breakdown"].values()) == r["candidates"]


# C2-4：除零保护 + 误报不计入成立
def test_calibration_math():
    assert L.calibration({"decided": 0, "reliable": 0}) is None
    assert L.calibration({"decided": 4, "reliable": 2}) == 0.5
    assert L.calibration({"decided": 3, "reliable": 3}) == 1.0


# C2-5：趋势表含三轮且口径逐条标注（R1/R2 口径不同已登记）
def test_trend_table():
    t = L.table()
    assert [r["round"] for r in t] == ["R1", "R2", "R3"]
    assert t[0]["metric"] != t[1]["metric"], "R1/R2 口径不同必须体现，不能混为一谈"
    assert t[0]["source_present"] is True and t[1]["source_present"] is True


# C2-6：门槛判定 —— 最高观测 50% ≤ 60% ⇒ 未达 ⇒ 不扩大白名单
def test_expansion_gate():
    g = L.expansion_gate()
    assert g["threshold"] == 0.60
    assert g["best_observed"] == 0.5
    assert g["passed"] is False
    assert "不扩大" in g["verdict"]
    assert "不足以判趋势" in g["caveat"]


# C2-7：台账 append-only + 幂等（写盘重定向到 tmp，不污染 data/）
def test_ledger_append_only_and_idempotent(tmp_path, monkeypatch):
    led = tmp_path / "cal.json"
    monkeypatch.setattr(L, "LEDGER", str(led))
    first = L.record(L.round_642())
    assert first["appended"] is True and first["n_entries"] == 1
    second = L.record(L.round_642())
    assert second["appended"] is False, "同 (round,batch) 必须幂等"
    assert second["n_entries"] == 1
    payload = json.loads(led.read_text(encoding="utf-8"))
    assert payload["append_only"] is True
    assert payload["entries"][0]["round"] == "R3"
    assert payload["entries"][0]["calibration"] is None


# C2-8：--check 自检通过（未打补丁的模块状态）
def test_selftest():
    assert L.selftest() == 0
