"""619 B2 单测：PCK 证书验证器（tools/pck_certificate_verifier_619.py）

纯函数验证：合法/非法证书、诚实注释、顶层非 mapping、--check 自检。不写盘。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pck_certificate_verifier_619 as B2  # noqa: E402


def _valid():
    return {
        "schema_version": B2.SCHEMA_VERSION,
        "claim": {"id": "ATOM-CONC-FENCE-001", "statement": "fence", "domain": "conc", "type": "inference"},
        "evidence": [{"type": "replay", "ref": "evidence/conc/EV-CONC-001.md"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": "approved", "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
        "provenance": {"commit": "e050b00", "first_authorized_at": "2026-09-20"},
    }


def test_valid_cert_ok():
    assert B2.validate_cert(_valid())["ok"] is True


def test_valid_cert_notes_honest():
    r = B2.validate_cert(_valid())
    assert any("单验证器" in n for n in r["notes"])
    assert any("batch_authorization" in n for n in r["notes"])


def test_invalid_schema_version():
    c = _valid()
    c["schema_version"] = "old"
    assert not B2.validate_cert(c)["ok"]


def test_empty_evidence_rejected():
    c = _valid()
    c["evidence"] = []
    assert not B2.validate_cert(c)["ok"]


def test_bad_claim_type_rejected():
    c = _valid()
    c["claim"]["type"] = "bogus"
    assert not B2.validate_cert(c)["ok"]


def test_negative_cs_rejected():
    c = _valid()
    c["uncertainty"]["cs_upper_bound"] = -1
    assert not B2.validate_cert(c)["ok"]


def test_missing_provenance_commit_rejected():
    c = _valid()
    del c["provenance"]["commit"]
    assert not B2.validate_cert(c)["ok"]


def test_top_level_not_mapping():
    assert B2.validate_cert([1, 2])["ok"] is False


def test_check_runs_clean():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "pck_certificate_verifier_619.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout + r.stderr)
