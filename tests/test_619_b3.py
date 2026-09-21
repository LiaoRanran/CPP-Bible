"""619 B3 单测：PCK 试点证书生成器（tools/pck_pilot_generator_619.py）

验证：10 张源卡存在、样本证书过 B2、已生成的 10 张证书全部过 B2、`--check` 自检。不写盘。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pck_pilot_generator_619 as G  # noqa: E402
import pck_certificate_verifier_619 as B2  # noqa: E402


def test_ten_pilot_cards_exist():
    assert all(os.path.exists(os.path.join(ROOT, c)) for c in G.PILOT_CARDS)


def test_sample_cert_validates():
    cert = G.build_cert(G.PILOT_CARDS[0])
    assert B2.validate_cert(cert)["ok"] is True


def test_sample_cert_honest_notes():
    cert = G.build_cert(G.PILOT_CARDS[0])
    r = B2.validate_cert(cert)
    assert any("单验证器" in n for n in r["notes"])
    assert any("batch_authorization" in n for n in r["notes"])


def test_generated_certs_all_present_and_valid():
    out_dir = os.path.join(ROOT, "data", "pck_pilot")
    assert os.path.isdir(out_dir)
    count = 0
    for card in G.PILOT_CARDS:
        fname = os.path.basename(card).replace(".md", ".pck.yaml")
        path = os.path.join(out_dir, fname)
        assert os.path.exists(path), fname
        cert = B2.load_cert(path)
        assert B2.validate_cert(cert)["ok"], fname
        count += 1
    assert count == 10


def test_check_runs_clean():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "pck_pilot_generator_619.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout + r.stderr)
