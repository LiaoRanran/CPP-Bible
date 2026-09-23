"""628 B2 · VSA 凭证 单测（7 例）。"""
import hmac
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import vsa_attestation_628 as V
import vsa_verify_628 as W


def test_credential_generated_with_schema():
    p = V.save_credential(V.build_credential())
    cred = json.load(open(p, encoding="utf-8"))
    for k in ("vsa_version", "verifier_id", "verifier_sha256", "verified_at",
              "input_hashes", "results", "attestation"):
        assert k in cred
    assert cred["vsa_version"] == "1.0"
    assert cred["results"]["w2_in"] == 114


def test_hmac_verify_pass():
    p = V.latest_credential()
    r = V.verify_credential(p)
    assert r["hmac_valid"] and r["valid"]


def test_tampered_credential_fails():
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    key = V.load_or_create_key()
    bad = dict(cred, results=dict(cred["results"], pck_authorized=999))
    assert not hmac.compare_digest(bad["attestation"],
                                   V.compute_attestation(bad, key))


def test_input_hash_anchoring():
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    cur = V._sha256_file(V.LEDGER)
    assert cred["input_hashes"]["ledger_sha256"] == cur


def test_key_not_tracked_by_git():
    import subprocess
    proc = subprocess.run(["git", "check-ignore", "data/vsa_secret.key"],
                          cwd=V.ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, "vsa_secret.key 必须被 gitignore"
    # 凭证中不包含密钥本体
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    key_hex = V.load_or_create_key().hex()
    assert key_hex not in json.dumps(cred)


def test_traceability():
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    ver_sha = V._sha256_file(os.path.join(V.HERE, "independent_verifier_628.py"))
    assert cred["verifier_sha256"] == ver_sha      # 绑定验证者版本
    assert cred["input_hashes"]["ledger_sha256"] == V._sha256_file(V.LEDGER)


def test_verify_tool_all_pass():
    allr = W.verify_all()
    assert allr and all(x["valid"] for x in allr)
