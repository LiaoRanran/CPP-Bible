"""629 C1 · VSA 非对称签名 单测（8 例）。

用 module 级 fixture 生成一次 RSA-1024 密钥（自检速度；报告用 2048）。
"""
import hashlib
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import vsa_asymmetric_signer_629 as S


@pytest.fixture(scope="module")
def keys():
    priv = S.generate_keypair(1024)
    return priv, S.public_of(priv)


def test_miller_rabin_known_values():
    assert all(S.is_probable_prime(p) for p in (2, 3, 97, 7919, 104729))
    assert not any(S.is_probable_prime(c) for c in (0, 1, 4, 9, 21, 104730))
    assert not S.is_probable_prime(7919 * 104729)


def test_keypair_math_properties(keys):
    priv, pub = keys
    n, e, d = int(priv["n"]), int(priv["e"]), int(priv["d"])
    assert priv["bits"] == 1024 and e == 65537
    for m in (2, 12345, n - 2):
        assert pow(pow(m, d, n), e, n) == m, "RSA 逆运算必须还原"


def test_public_key_has_no_private_fields(keys):
    _priv, pub = keys
    assert set(pub) == {"scheme", "n", "e", "bits"}
    assert not any(k in pub for k in ("d", "p", "q"))


def test_sign_verify_roundtrip_and_attacks(keys):
    priv, pub = keys
    msg = b"queyi-629"
    sig = S.sign(priv, msg)
    assert S.verify(pub, msg, sig)
    assert not S.verify(pub, msg + b"!", sig), "篡改消息必须失败"
    assert not S.verify(S.public_of(S.generate_keypair(1024)), msg, sig), "换公钥必须失败"
    assert not S.verify(pub, msg, "00" * 256), "伪造签名必须失败"
    assert not S.verify(pub, msg, "not-hex")


def test_emsa_structure(keys):
    _priv, pub = keys
    k = S._em_len(int(pub["n"]))
    em = S.emsa_pkcs1_v15(b"x", k)
    assert len(em) == k and em[:2] == b"\x00\x01"
    ps_len = k - 3 - len(S.SHA256_DER_PREFIX) - 32
    assert em[2:2 + ps_len] == b"\xff" * ps_len and em[2 + ps_len] == 0
    assert em[3 + ps_len:] == S.SHA256_DER_PREFIX + hashlib.sha256(b"x").digest()
    with pytest.raises(ValueError):
        S.emsa_pkcs1_v15(b"x", 16)          # 过短密钥必须报错


def test_credential_payload_deterministic_and_excludes_signature(keys):
    priv, pub = keys
    cred = {"b": 2, "a": 1, "attestation": "hmac"}
    assert S.credential_payload(cred) == S.credential_payload({"a": 1, "b": 2,
                                                              "attestation": "x"})
    up = S.upgrade_credential(cred, priv)
    assert up["attestation"] == "hmac" and up["signature_scheme"] == priv["scheme"]
    assert S.verify_credential_sig(up, pub)
    assert not S.verify_credential_sig(dict(up, a=99), pub), "改内容必须失败"


def test_repo_key_scan_has_no_false_positive():
    hits = S.repo_key_files()
    assert hits == [], f"仓库不应有私钥文件：{hits}"
    assert not any("adversarial" in h for h in hits), "adversarial_* 不是密钥（首版踩过）"


def test_selftest_passes():
    assert S.selftest() == 0
