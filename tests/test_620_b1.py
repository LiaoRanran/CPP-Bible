"""620 B1 · PCK 批量迁移工具 单测"""
from __future__ import annotations

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import pck_batch_migrator_620 as M  # noqa: E402
import pck_certificate_verifier_619 as B2  # noqa: E402

CARDS = M.discover_cards()


def test_discover_83_cards():
    assert len(CARDS) == 83
    assert sum(1 for c in CARDS if c.startswith("atoms/")) == 27
    assert sum(1 for c in CARDS if c.startswith("evidence/")) == 56


def test_single_migration_passes_validator():
    cert = M.build_cert(CARDS[0])
    res = B2.validate_cert(cert)
    assert res["ok"], res["errors"]
    assert cert["schema_version"] == B2.SCHEMA_VERSION


def test_batch_migration_all_pass():
    prev = M.migrate_preview(CARDS)
    assert prev["total"] == 83
    assert prev["fail"] == 0
    assert prev["ok"] == 83


def test_missing_fields_marked_unknown():
    for c in CARDS[:10]:
        cert = M.build_cert(c)
        assert cert["provenance"]["first_authorized_at"]
        assert cert["provenance"]["commit"]
        assert cert["human_authority"]["status"] in ("approved", "pending")


def test_idempotent_build():
    assert M.build_cert(CARDS[5]) == M.build_cert(CARDS[5])


def test_evidence_ref_normalization():
    path_ref = "evidence/conc/EV-CONC-001.md"
    assert M._norm_evidence_ref(path_ref, "conc") == path_ref
    assert M._norm_evidence_ref("EV-CONC-002", "conc") == "evidence/conc/EV-CONC-002.md"


def test_negative_tests_domain_safe():
    for c in CARDS:
        cert = M.build_cert(c)
        for t in cert["negative_tests"]:
            assert t["result"] in M.ALLOWED_NT_RESULTS


def test_migrate_writes_files_and_is_idempotent():
    with tempfile.TemporaryDirectory() as td:
        r1 = M.migrate(CARDS[:5], td)
        assert r1["total"] == 5 and r1["fail"] == 0
        first = {f: open(os.path.join(td, f), encoding="utf-8").read() for f in os.listdir(td)}
        r2 = M.migrate(CARDS[:5], td)
        second = {f: open(os.path.join(td, f), encoding="utf-8").read() for f in os.listdir(td)}
        assert r1["ok"] == r2["ok"]
        assert first == second


def test_selftest_passes():
    assert M.selftest() == 0
