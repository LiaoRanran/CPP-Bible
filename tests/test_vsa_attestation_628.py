"""628 B2 · VSA 凭证 单测（8 例）。

幂等性说明：**生成类用例写临时目录**（`save_credential(out_dir=)`），
生产 `data/vsa/` 不新增凭证（旧实现每跑一次就留一张未入册凭证，导致
"凭证全部入册" 不变量被打破、下游 `--check` 随机失败）。
"""
import hmac
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import vsa_attestation_628 as V
import vsa_verify_628 as W


def test_credential_generated_with_schema(tmp_path):
    p = V.save_credential(V.build_credential(), out_dir=str(tmp_path))
    cred = json.load(open(p, encoding="utf-8"))
    for k in ("vsa_version", "verifier_id", "verifier_sha256", "verified_at",
              "input_hashes", "results", "attestation"):
        assert k in cred
    assert cred["vsa_version"] == "1.0"
    assert cred["results"]["w2_in"] == 114


def test_same_second_does_not_overwrite(tmp_path):
    p1 = V.save_credential(V.build_credential(), out_dir=str(tmp_path))
    p2 = V.save_credential(V.build_credential(), out_dir=str(tmp_path))
    assert p1 != p2 and os.path.exists(p1) and os.path.exists(p2)


def test_production_dir_not_polluted_by_check():
    before = sorted(os.listdir(V.VSA_DIR))
    assert V.selftest() == 0
    assert sorted(os.listdir(V.VSA_DIR)) == before, "--check 不得写入生产凭证目录"


def test_hmac_verify_pass():
    r = V.verify_credential(V.latest_credential())
    assert r["hmac_valid"] and r["valid"]


def test_tampered_credential_fails():
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    key = V.load_or_create_key()
    bad = dict(cred, results=dict(cred["results"], pck_authorized=999))
    assert not hmac.compare_digest(bad["attestation"],
                                   V.compute_attestation(bad, key))


def test_input_hash_anchoring():
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    assert cred["input_hashes"]["ledger_sha256"] == V._sha256_file(V.LEDGER)


def test_key_not_tracked_by_git():
    proc = subprocess.run(["git", "check-ignore", "data/vsa_secret.key"],
                          cwd=V.ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, "vsa_secret.key 必须被 gitignore"
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    assert V.load_or_create_key().hex() not in json.dumps(cred)


def test_traceability_and_independent_verifier():
    cred = json.load(open(V.latest_credential(), encoding="utf-8"))
    ver_sha = V._sha256_file(os.path.join(V.HERE, "independent_verifier_628.py"))
    assert cred["verifier_sha256"] == ver_sha      # 绑定验证者版本
    assert cred["input_hashes"]["ledger_sha256"] == V._sha256_file(V.LEDGER)
    # 独立验证端：零 import 本项目工具（含不 import 签发端）+ 全部凭证验证通过
    assert W._project_imports() == []
    allr = W.verify_all()
    assert allr and all(x["valid"] for x in allr)
