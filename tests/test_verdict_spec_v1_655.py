#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""判决形式规格 v1 的**可执行对照**（655 B）。

`docs/verdict_formal_spec_v1.md` §3 的每条不变量都给出"可测试形式"；本文件把
**已实现**的那些落成用例，使规格不会随代码漂移而变成空话。未实现的（INV-4/11/15 等）
在规格 §7 显式登记为缺口，**此处不假装测试**。

覆盖：INV-1 / INV-2 / INV-3 / INV-5 / INV-6 / INV-7 / INV-8 / INV-9(结构) / INV-10 / INV-13 / INV-14。
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

kernel = importlib.import_module("queyi_core_v10_641")
fsv = importlib.import_module("four_state_verdict_638")
vex = importlib.import_module("verdict_extension_651")

LEDGER = ROOT / "data" / "authority" / "decision_event_v2_ledger.jsonl"


def _boundary() -> dict[str, object]:
    return {"mutation_set_hash": "d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57",
            "mutation_count": "1593", "generator_version": "mutation_fuzz@v7"}


# ── INV-1 四态封闭：非法态构造即失败 ────────────────────────────────────────
def test_inv1_state_is_closed_enum() -> None:
    assert tuple(kernel.FOUR_STATES) == ("pass", "pass_with_exception", "fail", "unknown")
    with pytest.raises(ValueError):
        kernel.Decision(decision_id="x", artifact_id="a", state="maybe")


# ── INV-2 边界三元组强制 ───────────────────────────────────────────────────
def test_inv2_boundary_required_for_pass_fail() -> None:
    b = _boundary()
    assert fsv.enforce({**b, "verdict": "pass"}) == "pass"
    assert fsv.enforce({**b, "verdict": "block"}) == "fail"
    assert fsv.enforce({"verdict": "pass"}) == "unknown", "缺边界必须降级"
    assert fsv.enforce({"mutation_set_hash": "zz", "mutation_count": 1,
                        "generator_version": "v"}) == "unknown", "畸形边界必须降级"
    for key in fsv.BOUNDARY_FIELDS:
        rec = {k: v for k, v in b.items() if k != key}
        rec["verdict"] = "pass"
        assert fsv.enforce(rec) == "unknown", f"缺 {key} 时必须降级"
        assert key in "".join(fsv.classify(rec)["reasons"]), "降级原因须点名缺失字段"


# ── INV-3 例外态必须有 explanation ─────────────────────────────────────────
def test_inv3_pass_with_exception_needs_explanation() -> None:
    b = _boundary()
    assert fsv.enforce({**b, "verdict": "pass", "exception": "条款X",
                        "explanation": "因为Y"}) == "pass_with_exception"
    assert fsv.enforce({**b, "verdict": "pass", "exception": "条款X"}) == "unknown"


# ── INV-5 conflict_state=resolved ⇒ conflict_detail ───────────────────────
def test_inv5_resolved_requires_detail() -> None:
    assert vex.validate({"conflict_state": "resolved"}) != []
    assert vex.validate({"conflict_state": "resolved",
                         "conflict_detail": {"left": "A", "right": "B",
                                             "c_value": 1.0,
                                             "evidence_both_sides": True}}) == []


# ── INV-6 / INV-7 回填不改不可变字段 + 幂等 ────────────────────────────────
def test_inv6_inv7_backfill_immutables_and_idempotent() -> None:
    v0 = {"decision_id": "D1", "state": "unknown", "result": "APPROVE",
          "event_id": "E1", "prev_hash": "GENESIS", "entry_hash": "deadbeef"}
    new, diff = vex.backfill(v0)
    for f in vex.IMMUTABLE:
        assert new[f] == v0[f], f"{f} 被回填改动"
    assert set(diff) <= {"schema_version", "conditions", "partial_atoms",
                         "conflict_state", "unknown_reason"}, "回填只允许新增 v1 字段"
    assert vex.backfill(new)[1] == {}, "二次回填必须无 diff（幂等）"
    assert new["unknown_reason"] == "other" and new.get("unknown_note"), "unknown ⇒ other + note"
    assert vex.backfill({"state": "pass"})[0]["unknown_reason"] is None, "非 unknown 不得臆测原因"


# ── INV-8 枚举 fail-closed ────────────────────────────────────────────────
@pytest.mark.parametrize("bad", [
    {"conflict_state": "maybe"},
    {"unknown_reason": "wat"},
    {"unknown_reason": "other"},
    {"conditions": [{"expr": "x"}]},
    {"conditions": [{"kind": "vibes"}]},
    {"partial_atoms": [{"atom_id": "A", "covered": "yes"}]},
])
def test_inv8_enum_fail_closed(bad: dict) -> None:
    assert vex.validate(bad) != [], f"{bad} 应被拒绝"
    assert vex.validate({"decision_id": "D", "state": "pass"}) == [], "v0 记录必须兼容通过"


# ── INV-9 账本结构链接（哈希链的完整复算见 651 checkpoint 工具）───────────
def test_inv9_ledger_chain_structure() -> None:
    rows = [json.loads(ln) for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert rows, "账本不应为空"
    assert rows[0]["prev_hash"] == "GENESIS"
    seqs = [r["seq"] for r in rows]
    assert seqs == list(range(1, len(rows) + 1)), "seq 必须从 1 连续递增"
    for prev, cur in zip(rows, rows[1:]):
        assert cur["prev_hash"] == prev["self_hash"], f"seq={cur['seq']} 链断"
    assert all(r.get("self_hash") for r in rows), "每条必须有 self_hash"


# ── INV-10 判决 ID 确定性且与时间无关 ─────────────────────────────────────
def test_inv10_decision_id_deterministic() -> None:
    a = kernel.Decision.make("A1", "pass", ["r"], ["E1"], ["R1"], "p", decided_at="2000-01-01T00:00:00")
    b = kernel.Decision.make("A1", "pass", ["r"], ["E1"], ["R1"], "p", decided_at="2026-09-27T00:00:00")
    c = kernel.Decision.make("A1", "fail", ["r"], ["E1"], ["R1"], "p")
    assert a.decision_id == b.decision_id, "时间不得影响 ID"
    assert a.decision_id != c.decision_id, "状态必须影响 ID"
    assert len(a.decision_id) == 64


# ── INV-13 判决四态 ⊥ 卡状态轴（verified 不蕴含 pass）────────────────────
def test_inv13_verified_card_is_not_pass_by_default() -> None:
    cards = sorted((ROOT / "atoms").rglob("*.md"))
    checked = 0
    for p in cards:
        text = p.read_text(encoding="utf-8", errors="replace")
        if "status: verified" not in text:
            continue
        out = fsv.classify_card(str(p))
        checked += 1
        assert (out["state"] == "unknown") is (not out["boundary_ok"]), \
            f"{out['file']}: 缺边界却未 unknown"
    assert checked > 0, "至少应有一张 verified 卡参与断言"


# ── INV-14 回填 dry-run 不改原文件 ────────────────────────────────────────
def test_inv14_backfill_dry_run_keeps_file(tmp_path: Path) -> None:
    f = tmp_path / "ledger.jsonl"
    f.write_text('{"decision_id": "D1", "state": "pass"}\n', encoding="utf-8")
    before = f.read_bytes()
    rep = vex.backfill_file(f)
    assert rep["unchanged"] is True and rep["would_change"] == 1
    assert f.read_bytes() == before, "dry-run 不得写盘"
