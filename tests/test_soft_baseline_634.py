"""634 A3 · soft_baseline 单测（纯标准库，≥5 例）。编号 A3-1..A3-6。"""
from __future__ import annotations

import json

import soft_baseline_634 as SB


# A3-1：缺文件 ⇒ 兜底 current
def test_missing_file_fallback(tmp_path):
    assert SB.soft("k", 42, path=str(tmp_path / "none.json")) == 42


# A3-2：有基线 ⇒ 取基线值
def test_soft_uses_baseline(tmp_path):
    p = tmp_path / "b.json"
    p.write_text(json.dumps({"k": 7}), encoding="utf-8")
    assert SB.soft("k", 999, path=str(p)) == 7


# A3-3：无 key ⇒ 兜底 current
def test_soft_missing_key(tmp_path):
    p = tmp_path / "b.json"
    p.write_text(json.dumps({"k": 7}), encoding="utf-8")
    assert SB.soft("z", 5, path=str(p)) == 5


# A3-4：at_least 取 min
def test_at_least(tmp_path):
    p = tmp_path / "b.json"
    p.write_text(json.dumps({"m": 100}), encoding="utf-8")
    assert SB.at_least("m", 50, path=str(p)) == 50
    assert SB.at_least("m", 200, path=str(p)) == 100


# A3-5：真实基线文件可加载（含约定 key）
def test_real_baseline_loads():
    b = SB.load()
    assert "authority_log_entries" in b and "_note" in b


# A3-6：--check 自检通过
def test_selftest():
    assert SB.selftest() == 0
