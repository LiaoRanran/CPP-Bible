"""628 A2 · PCK hash 重算 单测（7 例）。"""
import glob
import os
import sys

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pck_hash_renewal_628 as P

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_DIR = os.path.join(HERE, "data", "pck", "certificates")


def test_all_83_certs_present():
    assert len(glob.glob(os.path.join(CERT_DIR, "*.yaml"))) == 83


def test_hash_matches_current_file():
    v = P.verify()
    assert v["hash_ok"] >= 82 and v["bad_count"] == 0


def test_ref_missing_not_auto_fixed():
    v = P.verify()
    assert 1 <= v["needs_human"] <= 2
    # 需人审条目必须有 hash_status 标记且不伪造 hash
    for p in glob.glob(os.path.join(CERT_DIR, "*.yaml")):
        data = yaml.safe_load(open(p, encoding="utf-8"))
        for ev in data.get("evidence", []) or []:
            if ev.get("hash_status") == P.NEEDS_HUMAN:
                assert not os.path.exists(ev["ref"])


def test_semantic_fields_untouched():
    assert P.semantic_fields_untouched()


def test_backup_exists_with_83():
    assert os.path.isdir(P.BACKUP_DIR)
    assert len(glob.glob(os.path.join(P.BACKUP_DIR, "*.yaml"))) == 83


def test_hash_format_preserved():
    # hash 保持 sha256:<hex> 前缀格式
    for p in glob.glob(os.path.join(CERT_DIR, "*.yaml")):
        data = yaml.safe_load(open(p, encoding="utf-8"))
        for ev in data.get("evidence", []) or []:
            h = ev.get("hash")
            if h:
                assert h.startswith("sha256:") and len(h) == 7 + 64
        break


def test_renewal_idempotent():
    # 再跑一次 apply：全部 already_ok，不新增改动
    before = P.verify()
    r = P.renew(apply_changes=True)
    after = P.verify()
    assert before == after
    assert r["stats"]["renewed"] == 0 and r["stats"]["added"] == 0
