#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""652 工具测试（W4+ 建设批）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import backfill_verified_at_652 as bv  # noqa: E402
import challenger_652 as ch  # noqa: E402
import embedded_adapter_652 as em  # noqa: E402
import pck_export_652 as px  # noqa: E402
import probe_assembler_652 as pa  # noqa: E402
import rats_closure_652 as rc  # noqa: E402


# ── A 交人项自动化 ──────────────────────────────────────────────────────────
def test_backfill_selftest_and_verified_at_now_present():
    assert bv.selftest() == 0
    # A1 执行后：atoms+evidence 中不应再有缺 verified_at 的卡
    assert bv.plan() == []


def test_backfill_git_date_lookup():
    d = bv.git_first_commit_date("README.md")
    assert d and len(d) == 10, d


def test_handoff_t1_backfill_is_add_only():
    import verdict_extension_651 as ve
    new, diff = ve.backfill({"decision_id": "D", "state": "pass"})
    assert new["decision_id"] == "D" and "schema_version" in diff


def test_handoff_m7_alias_migration():
    import human_review_queue_651 as hr
    ad, log = hr.adapt_item({"proposal_id": "p1", "atom_card": "A", "suggested_reason": "复核 approve"})
    assert ad["item_id"] == "p1" and ad["reason"] == "needs_human" and log


# ── B W4+ 头部 ─────────────────────────────────────────────────────────────
def test_probe_assembler_selftest_and_assembly():
    assert pa.selftest() == 0
    src = pa.assemble()
    assert "int main(void){" in src and all(f"blk_{n}()" in src for n in pa.BLOCKS)


def test_probe_assembler_unknown_block_raises():
    try:
        pa.assemble(["nope"])
        raise AssertionError("应抛 KeyError")
    except KeyError:
        pass


# ── C W4+ 中间 ─────────────────────────────────────────────────────────────
def test_challenger_selftest_and_mutations_apply():
    assert ch.selftest() == 0
    t = "claim_boundary: x\nnext: y\n"
    assert "claim_boundary" not in ch.mutate(t, "M1_delete_boundary")


def test_embedded_adapter_selftest_and_scan():
    assert em.selftest() == 0
    vio = em.scan_text("p = malloc(4);")
    assert any(v.rule == "no_heap" for v in vio)
    assert em.LLM_EMBEDDED_PASS_AT_1 == 0.556


# ── D W4+ 尾部 ─────────────────────────────────────────────────────────────
def test_rats_closure_three_stores():
    assert rc.selftest() == 0
    rep = rc.export_closure()
    assert set(rep["stores"]) == {"reference_values", "endorsements", "verifier_code"}


def test_pck_export_hard_binding_mapping():
    assert px.selftest() == 0
    cert = {"claim": {"id": "X"}, "evidence": [{"ref": "e.md", "hash": "sha256:abc"}]}
    link = px.to_intoto_link(cert)
    c2pa = px.to_c2pa(cert)
    hard = [a for a in c2pa["assertions"] if a["label"] == "c2pa.hash.data"]
    assert link["materials"]["e.md"] == "abc" and hard[0]["data"]["hash"] == "abc"
