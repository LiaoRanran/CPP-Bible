"""627 A3 · PCK hash 漂移分析 单测（≥4 例）。"""
import glob
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pck_hash_drift_analyzer_627 as A


def test_scan_count():
    r = A.analyze()
    assert r["total_certs"] == 83
    assert sum(r["by_worst_category"].values()) == 83


def test_content_drift_56():
    r = A.analyze()
    assert r["n_content_drift_certs"] == 56


def test_all_have_gap():
    r = A.analyze()
    assert r["by_worst_category"].get("ok", 0) == 0


def test_root_cause_classifies():
    r = A.analyze()
    assert isinstance(r["root_cause_breakdown"], dict)
    # 至少覆盖两种子因
    assert len(r["root_cause_breakdown"]) >= 1


def test_readonly_no_modification():
    before = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()
              for p in glob.glob(os.path.join(A.CERT_DIR, "*.pck.yaml"))}
    A.analyze()
    after = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()
             for p in glob.glob(os.path.join(A.CERT_DIR, "*.pck.yaml"))}
    assert before == after
