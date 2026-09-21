"""620 B2 · 全量 83 张 PCK 证书迁移 可复现性单测"""
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
CERT_DIR = M.DEFAULT_OUT_DIR


def test_全量83张全部通过验证():
    prev = M.migrate_preview(CARDS)
    assert prev["total"] == 83
    assert prev["ok"] == 83
    assert prev["fail"] == 0


def test_迁移可复现_两次输出内容一致():
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        M.migrate(CARDS, d1)
        M.migrate(CARDS, d2)
        f1 = {f: open(os.path.join(d1, f), encoding="utf-8").read() for f in os.listdir(d1)}
        f2 = {f: open(os.path.join(d2, f), encoding="utf-8").read() for f in os.listdir(d2)}
        assert f1 == f2
        assert len(f1) == 83


def test_迁移产物落在非受控目录():
    assert CERT_DIR.replace("\\", "/").endswith("data/pck/certificates")
    assert not CERT_DIR.replace("\\", "/").startswith("atoms")
    assert not CERT_DIR.replace("\\", "/").startswith("evidence")


def test_已生成证书文件存在且可通过验证():
    if not os.path.isdir(CERT_DIR):
        return
    files = [f for f in os.listdir(CERT_DIR) if f.endswith(".pck.yaml")]
    assert len(files) == 83
    bad = []
    for f in files:
        cert = B2.load_cert(os.path.join(CERT_DIR, f))
        if not B2.validate_cert(cert)["ok"]:
            bad.append(f)
    assert bad == []


def test_证据卡human_authority全为pending_如实反映():
    ev_cards = [c for c in CARDS if c.startswith("evidence/")]
    assert len(ev_cards) == 56
    for c in ev_cards:
        assert M.build_cert(c)["human_authority"]["status"] == "pending"


def test_原子卡approved数23():
    at_cards = [c for c in CARDS if c.startswith("atoms/")]
    appr = sum(1 for c in at_cards
               if M.build_cert(c)["human_authority"]["status"] == "approved")
    assert appr == 23


def test_negative_tests丢弃数为0():
    dropped = 0
    for c in CARDS:
        dropped += len(M.build_cert(c).get("migration_dropped_negative_tests", []))
    assert dropped == 0
