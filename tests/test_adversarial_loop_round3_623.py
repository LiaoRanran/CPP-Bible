"""623 A4 · 闭环第三轮 单元测试（可复现性 / 关键结论）"""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R3 = os.path.join(ROOT, "data", "adversarial_loop_round3_sandbox_run_623.json")
A2 = os.path.join(ROOT, "data", "high_complexity_sandbox_run_623.json")


def test_round3_40_mutations():
    res = json.load(open(R3, encoding="utf-8"))
    assert res["total"] == 40
    d = res["distribution"]
    assert sum(d.values()) == 40


def test_round3_no_escaped():
    res = json.load(open(R3, encoding="utf-8"))
    assert res["distribution"]["escaped"] == 0


def test_cumulative_touched_ge_25():
    a2 = json.load(open(A2, encoding="utf-8"))
    r3 = json.load(open(R3, encoding="utf-8"))
    cum = set()
    for r in a2["rows"]:
        cum.update(r.get("new_block_rules", [])); cum.update(r.get("new_nonblock_rules", []))
    for r in r3["rows"]:
        cum.update(r.get("new_block_rules", [])); cum.update(r.get("new_nonblock_rules", []))
    assert len(cum) >= 25, f"累计触达应 ≥25，实际 {len(cum)}"


def test_round3_touched_rules_listed():
    res = json.load(open(R3, encoding="utf-8"))
    touched = set()
    for r in res["rows"]:
        touched.update(r.get("new_block_rules", [])); touched.update(r.get("new_nonblock_rules", []))
    # 至少包含 gate 必拦的基础规则
    assert "ATOM-FM-REQUIRED" in touched or "EV-FM-YAML-HARDENING" in touched
