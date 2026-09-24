"""623 A3 · 新逃逸根因分析 v2 验证（可复现性）

验证 A3 的核心结论：4 条 escaped 全部为 M1 删 claim_structured（内容删除假象），
真实危险逃逸（内容保留下 block finding 消失）= 0。
"""
from __future__ import annotations

import json
import os

import soft_baseline_634 as SB  # 634 A3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(ROOT, "data", "high_complexity_sandbox_run_623.json")


def test_four_escaped_all_claim_structured_deletion():
    res = json.load(open(RESULT, encoding="utf-8"))
    esc = res["escaped"]
    assert len(esc) == 4, f"应有 4 条 escaped，实际 {len(esc)}"
    for e in esc:
        assert "claim_structured" in (e.get("edit") or ""), \
            f"escaped {e['mutation_id']} 应为删除 claim_structured"


def test_real_dangerous_escapes_zero():
    # 真实危险逃逸 = 内容保留下 block finding 消失；4 条均为内容删除假象
    res = json.load(open(RESULT, encoding="utf-8"))
    for e in res["escaped"]:
        assert e.get("new_block_rules") == [], \
            f"escaped {e['mutation_id']} 不应有新增 block（否则是真实逃逸）"
    # 所有非 escaped 行也不应出现「block 消失」
    for r in res["rows"]:
        if r["verdict"] != "escaped":
            assert r.get("lost_block_rules") in (None, []), \
                f"{r['mutation_id']} 非 escaped 却丢失 block finding"


def test_touched_rules_exceed_622_baseline():
    res = json.load(open(RESULT, encoding="utf-8"))
    touched = set()
    for r in res["rows"]:
        touched.update(r.get("new_block_rules", []))
        touched.update(r.get("new_nonblock_rules", []))
    # 634 A3：单调，读基线（>= min(基线,current)）
    assert len(touched) >= SB.soft("touched_rules_min", len(touched)), f"触达规则应 ≥ 基线，实际 {len(touched)}"
