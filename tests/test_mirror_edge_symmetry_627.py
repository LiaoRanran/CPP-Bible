"""627 A4 · 镜像边对称性验证 单测（≥4 例）。"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import mirror_edge_symmetry_checker_627 as M


def test_mirror_count_194():
    r = M.check()
    assert r["mirror_edges"] == 194


def test_classification_complete():
    r = M.check()
    assert r["symmetric"] + r["asymmetric"] == 194


def test_all_need_human_verification():
    r = M.check()
    assert all(row["needs_human_verification"] for row in r["rows"])
    assert len(r["rows"]) == 194


def test_readonly_no_write():
    before = hashlib.sha256(open(M.CAND, "rb").read()).hexdigest()
    M.check()
    after = hashlib.sha256(open(M.CAND, "rb").read()).hexdigest()
    assert before == after
