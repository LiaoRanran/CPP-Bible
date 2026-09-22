"""621 C3 · ABSTAIN 与 PCK 集成 单测"""
from __future__ import annotations

import json
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import pck_abstain_sync_621 as S  # noqa: E402
import pck_certificate_verifier_619 as B2  # noqa: E402

BASE = {
    "schema_version": B2.SCHEMA_VERSION,
    "claim": {"id": "ATOM-CONC-FENCE-001", "statement": "s", "domain": "conc",
              "type": "inference"},
    "evidence": [{"type": "replay", "ref": "evidence/conc/EV-CONC-001.md"}],
    "verifiers": [{"name": "gate_engine", "result": "pass"}],
    "human_authority": {"status": "approved", "review_method": "batch_authorization"},
    "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
    "provenance": {"commit": "abc", "first_authorized_at": "unknown"},
}


def _setup(td, states):
    cdir = os.path.join(td, "certs")
    os.makedirs(cdir)
    for cid, st in states.items():
        c = dict(BASE)
        c["claim"] = dict(BASE["claim"], id=cid)
        with open(os.path.join(cdir, f"{cid}.pck.yaml"), "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(c, allow_unicode=True))
    cpath = os.path.join(td, "cls.jsonl")
    with open(cpath, "w", encoding="utf-8") as fh:
        for cid, st in states.items():
            fh.write(json.dumps({"card_id": cid, "state": st, "reason": "r",
                                 "is_abstain": st != "SUPPORTED"},
                                ensure_ascii=False) + "\n")
    return cdir, cpath


def test_sync_writes_abstain_state():
    with tempfile.TemporaryDirectory() as td:
        cdir, cpath = _setup(td, {"ATOM-CONC-FENCE-001": "UNDECIDED"})
        res = S.sync(cdir, cpath, write=True)
        assert res["synced"] == 1
        with open(os.path.join(cdir, "ATOM-CONC-FENCE-001.pck.yaml"), encoding="utf-8") as fh:
            after = yaml.safe_load(fh.read())
        assert after["uncertainty"]["abstain_state"] == "UNDECIDED"


def test_human_authority_untouched():
    with tempfile.TemporaryDirectory() as td:
        cdir, cpath = _setup(td, {"ATOM-CONC-FENCE-001": "SUPPORTED"})
        S.sync(cdir, cpath, write=True)
        with open(os.path.join(cdir, "ATOM-CONC-FENCE-001.pck.yaml"), encoding="utf-8") as fh:
            after = yaml.safe_load(fh.read())
        assert after["human_authority"] == BASE["human_authority"]


def test_still_valid_after_sync():
    with tempfile.TemporaryDirectory() as td:
        cdir, cpath = _setup(td, {"ATOM-CONC-FENCE-001": "UNDECIDED"})
        res = S.sync(cdir, cpath, write=True)
        assert res["validation_ok_after"] == 1
        with open(os.path.join(cdir, "ATOM-CONC-FENCE-001.pck.yaml"), encoding="utf-8") as fh:
            assert B2.validate_cert(yaml.safe_load(fh.read()))["ok"]


def test_unmatched_marks_unknown():
    with tempfile.TemporaryDirectory() as td:
        cdir, cpath = _setup(td, {"ATOM-CONC-FENCE-001": "UNDECIDED"})
        c2 = dict(BASE)
        c2["claim"] = dict(BASE["claim"], id="EV-CONC-999")
        with open(os.path.join(cdir, "EV-CONC-999.pck.yaml"), "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(c2, allow_unicode=True))
        res = S.sync(cdir, cpath, write=True)
        assert res["unmatched"] == 1
        with open(os.path.join(cdir, "EV-CONC-999.pck.yaml"), encoding="utf-8") as fh:
            after = yaml.safe_load(fh.read())
        assert after["uncertainty"]["abstain_state"] == "UNKNOWN"


def test_idempotent():
    with tempfile.TemporaryDirectory() as td:
        cdir, cpath = _setup(td, {"ATOM-CONC-FENCE-001": "UNDECIDED"})
        a = S.sync(cdir, cpath, write=True)["by_state"]
        b = S.sync(cdir, cpath, write=True)["by_state"]
        assert a == b


def test_real_83_certs_sync():
    if not os.path.isdir(S.DEFAULT_CERT_DIR) or not os.path.exists(S.DEFAULT_CLASSIFICATION):
        return
    res = S.sync(S.DEFAULT_CERT_DIR, S.DEFAULT_CLASSIFICATION, write=False)
    assert res["total"] == 83
    assert res["synced"] + res["unmatched"] == 83
    assert res["ha_before"] == res["ha_after"]  # 不代签


def test_report_renders():
    with tempfile.TemporaryDirectory() as td:
        cdir, cpath = _setup(td, {"ATOM-CONC-FENCE-001": "UNDECIDED"})
        res = S.sync(cdir, cpath, write=False)
        assert "ABSTAIN 与 PCK 集成" in S.render_report(res)


def test_selftest_passes():
    assert S.selftest() == 0
