"""620 C3 · Authority 与 PCK 集成 单测"""
from __future__ import annotations

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import authority_log_620 as AL  # noqa: E402
import pck_authority_sync_620 as S  # noqa: E402
import pck_certificate_verifier_619 as B2  # noqa: E402
import yaml  # noqa: E402


def _cert(cert_id: str) -> dict:
    return {
        "schema_version": B2.SCHEMA_VERSION,
        "claim": {"id": cert_id, "statement": "s", "domain": "mem", "type": "inference"},
        "evidence": [{"type": "replay", "ref": "evidence/mem/EV-MEM-001.md"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": "pending", "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
        "provenance": {"commit": "abc", "first_authorized_at": "unknown"},
    }


def _entries() -> list[dict]:
    return [{
        "decision_id": "dec-000001", "seq": 1,
        "target": {"type": "attack_edge",
                   "id": "ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-3"},
        "power": "ACCEPT", "reviewer": "human:LiaoRanran", "reason": "r",
        "review_method": "batch_authorization", "decided_at": "2026-09-19",
        "prev_hash": AL.GENESIS, "self_hash": "x",
    }]


def _setup(td, ids):
    cdir = os.path.join(td, "certs")
    os.makedirs(cdir)
    for i in ids:
        with open(os.path.join(cdir, f"{i}.pck.yaml"), "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(_cert(i), allow_unicode=True))
    lpath = os.path.join(td, "log.jsonl")
    with open(lpath, "w", encoding="utf-8") as fh:
        for e in _entries():
            fh.write(AL._canonical(e) + "\n")
    return cdir, lpath


def test_match_embedded_card_id():
    assert len(S.match_decisions("ATOM-MEM-PERF-003", _entries())) == 1
    assert S.match_decisions("EV-CONC-001", _entries()) == []


def test_power_to_status_mapping():
    assert S.POWER_TO_STATUS["ACCEPT"] == "approved"
    assert S.POWER_TO_STATUS["REJECT"] == "rejected"
    assert S.POWER_TO_STATUS["ABSTAIN"] == "pending"  # 弃权 != 接受


def test_sync_updates_matched_cert():
    with tempfile.TemporaryDirectory() as td:
        cdir, lpath = _setup(td, ["ATOM-MEM-PERF-003"])
        res = S.sync(cdir, lpath, write=True)
        assert res["synced"] == 1
        with open(os.path.join(cdir, "ATOM-MEM-PERF-003.pck.yaml"), encoding="utf-8") as fh:
            after = yaml.safe_load(fh.read())
        assert after["human_authority"]["status"] == "approved"
        assert after["human_authority"]["authority_ref"] == "dec-000001"
        assert B2.validate_cert(after)["ok"]


def test_unmatched_cert_stays_pending_no_forgery():
    with tempfile.TemporaryDirectory() as td:
        cdir, lpath = _setup(td, ["EV-CONC-001"])
        res = S.sync(cdir, lpath, write=True)
        assert res["synced"] == 0
        assert res["unmatched"] == 1
        with open(os.path.join(cdir, "EV-CONC-001.pck.yaml"), encoding="utf-8") as fh:
            after = yaml.safe_load(fh.read())
        assert after["human_authority"]["status"] == "pending"
        assert after["human_authority"]["authority_ref"] is None


def test_idempotent_sync():
    with tempfile.TemporaryDirectory() as td:
        cdir, lpath = _setup(td, ["ATOM-MEM-PERF-003", "EV-CONC-001"])
        a = S.sync(cdir, lpath, write=True)["status_after"]
        b = S.sync(cdir, lpath, write=True)["status_after"]
        assert a == b


def test_full_sync_against_real_log_and_certs():
    if not os.path.isdir(S.DEFAULT_CERT_DIR) or not os.path.exists(S.DEFAULT_LOG):
        return
    res = S.sync(S.DEFAULT_CERT_DIR, S.DEFAULT_LOG, write=False)
    assert res["total"] == 83
    assert res["synced"] + res["unmatched"] == 83
    assert res["log_entries"] == 418   # 624 D3：622 D1 逐条人审后 Authority 日志 388→418（存量修正）


def test_report_renders():
    with tempfile.TemporaryDirectory() as td:
        cdir, lpath = _setup(td, ["ATOM-MEM-PERF-003"])
        res = S.sync(cdir, lpath, write=False)
        assert "同步统计" in S.render_report(res)


def test_selftest_passes():
    assert S.selftest() == 0
